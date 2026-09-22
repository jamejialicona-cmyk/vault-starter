#!/usr/bin/env python3
"""Auditoria de salud y peso de arranque del Vault (VAULT-STARTER v4, §9).

Solo lectura. Nunca escribe nada.

Novedades de v4 frente a v3:
  - DESCUBRE los ejes en vez de traer rutas incrustadas. Un repo puede tener
    varios vaults independientes (§3.6); cada uno se mide por separado.
  - Techo tambien para el LOG, no solo para Current-State.
  - Un techo bajado/subido por configuracion se REPORTA como hallazgo, para
    que mover el contrato sea una decision visible y no un ajuste silencioso.

Uso:
    python3 check_vault.py [ruta]            # tabla legible (default: cwd)
    python3 check_vault.py [ruta] --json     # JSON para que lo consuma el LLM
    python3 check_vault.py [ruta] --eje Boda # solo ese eje
"""
import os, sys, re, json, subprocess, datetime

# La consola de Windows abre en cp1252 y destroza acentos y simbolos.
# Forzar UTF-8 en la salida es la misma leccion de encoding que el Vault
# aplica a sus archivos.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass

# ─── Techos por defecto (§7, §4). Se pueden sobrescribir en vault-config.json,
#     pero hacerlo queda registrado en el reporte como TECHO MODIFICADO.
TECHOS_DEFAULT = {
    "current_state": 2500,   # se lee al abrir cada sesion
    "log": 40000,            # umbral de "todavia se puede leer de una pasada"
}
OLD_DAYS = 14
ARRANQUE_VERDE = 10000
ARRANQUE_AMARILLO = 30000
MAX_PROFUNDIDAD_EJE = 3

DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
IMPORT_RE = re.compile(r"^@(\S+)", re.MULTILINE)  # sintaxis @import de Claude Code

# Nombres que identifican las piezas de un eje. El descubrimiento busca por
# NOMBRE, no por ruta, que es lo que hace al script portable entre proyectos.
NOMBRE_CURRENT_STATE = "Current-State.md"
NOMBRES_METODO = ("SCHEMA.md", "METODO.md")
NOMBRE_LOG = "LOG.md"
NOMBRE_INDEX = "00-Index.md"
NOMBRE_LECCIONES = "Lecciones.md"
GLOBS_PRIVADOS = ("Notas-Privadas", "Bitacora-Privada")

IGNORAR_DIRS = {".git", ".obsidian", "node_modules", "__pycache__", "dist",
                "build", ".venv", "venv", ".next"}


def estimar_tokens(path):
    try:
        return os.path.getsize(path) // 4
    except OSError:
        return 0


def fecha_mas_reciente(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            head = f.read(4000)
    except OSError:
        return None
    fechas = []
    for y, m, d in DATE_RE.findall(head):
        try:
            fechas.append(datetime.date(int(y), int(m), int(d)))
        except ValueError:
            pass
    return max(fechas) if fechas else None


def edad_en_dias(path):
    fecha = fecha_mas_reciente(path)
    if fecha is None:
        return None, None
    return fecha, (datetime.date.today() - fecha).days


def buscar(raiz, nombre, max_depth=MAX_PROFUNDIDAD_EJE):
    """Rutas absolutas de todos los archivos `nombre` bajo `raiz`, por profundidad."""
    encontrados = []
    raiz = os.path.abspath(raiz)
    for actual, dirs, archivos in os.walk(raiz):
        dirs[:] = [d for d in dirs if d not in IGNORAR_DIRS]
        rel = os.path.relpath(actual, raiz)
        profundidad = 0 if rel == "." else rel.count(os.sep) + 1
        if profundidad > max_depth:
            dirs[:] = []
            continue
        if nombre in archivos:
            encontrados.append(os.path.join(actual, nombre))
    return sorted(encontrados)


def buscar_prefijo(raiz, prefijo, max_depth=MAX_PROFUNDIDAD_EJE):
    encontrados = []
    raiz = os.path.abspath(raiz)
    for actual, dirs, archivos in os.walk(raiz):
        dirs[:] = [d for d in dirs if d not in IGNORAR_DIRS]
        rel = os.path.relpath(actual, raiz)
        profundidad = 0 if rel == "." else rel.count(os.sep) + 1
        if profundidad > max_depth:
            dirs[:] = []
            continue
        for a in archivos:
            if a.startswith(prefijo):
                encontrados.append(os.path.join(actual, a))
    return sorted(encontrados)


def descubrir_ejes(root):
    """Un eje es cualquier carpeta con su propio Current-State.md.

    Cubre los dos layouts: el clasico de un solo vault (`Vault/` o la raiz) y
    el multi-eje de §3.6 (varias carpetas hermanas, cada una su vault).
    """
    ejes = []
    candidatos = [os.path.join(root, d) for d in sorted(os.listdir(root))
                  if os.path.isdir(os.path.join(root, d)) and d not in IGNORAR_DIRS]
    for carpeta in candidatos:
        estados = buscar(carpeta, NOMBRE_CURRENT_STATE)
        if estados:
            ejes.append({"nombre": os.path.basename(carpeta), "raiz": carpeta,
                         "estados": estados})
    if not ejes:
        estados = buscar(root, NOMBRE_CURRENT_STATE)
        if estados:
            ejes.append({"nombre": os.path.basename(root) or "raiz",
                         "raiz": root, "estados": estados})
    return ejes


def cargar_config(root):
    """vault-config.json opcional: techos y ejes declarados a mano."""
    ruta = os.path.join(root, "vault-config.json")
    if not os.path.isfile(ruta):
        return {}, []
    try:
        with open(ruta, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return {}, [{"nivel": "error", "msg": "vault-config.json ilegible; usando defaults"}]
    hallazgos = []
    techos = dict(TECHOS_DEFAULT)
    for clave, valor in (data.get("techos") or {}).items():
        if clave in techos and isinstance(valor, int) and valor != techos[clave]:
            hallazgos.append({
                "nivel": "aviso",
                "msg": (f"TECHO MODIFICADO: {clave} = {valor:,} "
                        f"(default {TECHOS_DEFAULT[clave]:,}). "
                        "Mover un techo es una decision: registrala en el LOG."),
            })
            techos[clave] = valor
    data["_techos"] = techos
    return data, hallazgos


def detectar_imports(root):
    claude = os.path.join(root, "CLAUDE.md")
    if not os.path.isfile(claude):
        return []
    try:
        with open(claude, encoding="utf-8", errors="replace") as f:
            texto = f.read()
    except OSError:
        return []
    out = []
    for ruta in IMPORT_RE.findall(texto):
        full = os.path.join(root, ruta)
        existe = os.path.isfile(full)
        out.append({"ruta": ruta, "existe": existe,
                    "tokens": estimar_tokens(full) if existe else 0})
    return out


def git_check_ignore(root, archivo):
    try:
        r = subprocess.run(["git", "-C", root, "check-ignore", "-q", archivo],
                           capture_output=True, timeout=5)
        return r.returncode == 0
    except (subprocess.SubprocessError, OSError):
        return None


def autores_de(root, archivo):
    try:
        r = subprocess.run(["git", "-C", root, "log", "--format=%an", "--", archivo],
                           capture_output=True, text=True, timeout=10)
        if r.returncode == 0:
            return {l.strip() for l in r.stdout.splitlines() if l.strip()}
    except (subprocess.SubprocessError, OSError):
        pass
    return set()


def semaforo(tokens):
    if tokens < ARRANQUE_VERDE:
        return "verde"
    if tokens < ARRANQUE_AMARILLO:
        return "amarillo"
    return "rojo"


def analizar_eje(root, eje, techos, claude_tokens, imports_tokens):
    raiz, hallazgos, piezas = eje["raiz"], [], []
    rel = lambda p: os.path.relpath(p, root).replace(os.sep, "/")

    estados = eje["estados"]
    if len(estados) > 1:
        hallazgos.append({
            "nivel": "aviso",
            "msg": (f"{len(estados)} archivos Current-State.md en este eje. "
                    "El punto de entrada debe ser UNO: "
                    + ", ".join(rel(e) for e in estados)),
        })
    estado = estados[0]
    tokens_estado = estimar_tokens(estado)
    fecha, edad = edad_en_dias(estado)
    pieza = {"file": rel(estado), "rol": "current-state", "autoload": "soft",
             "tokens": tokens_estado,
             "nota": f"ultima fecha {fecha.isoformat()} ({edad}d)" if fecha else None,
             "viejo": bool(edad is not None and edad > OLD_DAYS)}
    if tokens_estado > techos["current_state"]:
        pieza["sobre_techo"] = tokens_estado - techos["current_state"]
        hallazgos.append({
            "nivel": "aviso",
            "msg": (f"Current-State {tokens_estado:,}t supera el techo de "
                    f"{techos['current_state']:,}t. Mueve historia al LOG."),
        })
    piezas.append(pieza)

    for nombre, rol in ((NOMBRE_LOG, "log"), (NOMBRE_INDEX, "index"),
                        (NOMBRE_LECCIONES, "lecciones")):
        for ruta in buscar(raiz, nombre):
            tokens = estimar_tokens(ruta)
            p = {"file": rel(ruta), "rol": rol, "autoload": "no", "tokens": tokens,
                 "nota": None, "viejo": False}
            if rol == "log" and tokens > techos["log"]:
                p["sobre_techo"] = tokens - techos["log"]
                hallazgos.append({
                    "nivel": "aviso",
                    "msg": (f"{rel(ruta)} pesa {tokens:,}t, sobre el techo de "
                            f"{techos['log']:,}t. Ya no se lee de una pasada: "
                            "rota lo viejo a LOG-Archivo/."),
                })
            piezas.append(p)

    metodo = None
    for nombre in NOMBRES_METODO:
        encontrados = buscar(raiz, nombre)
        if encontrados:
            metodo = encontrados[0]
            piezas.append({"file": rel(metodo), "rol": "metodo", "autoload": "no",
                           "tokens": estimar_tokens(metodo), "nota": None,
                           "viejo": False})
            break
    if metodo is None:
        hallazgos.append({"nivel": "aviso",
                          "msg": "Sin SCHEMA.md ni METODO.md: el eje no declara su modelo de trabajo."})

    privados = []
    for prefijo in GLOBS_PRIVADOS:
        for ruta in buscar_prefijo(raiz, prefijo):
            ignorado = git_check_ignore(root, rel(ruta))
            privados.append({"file": rel(ruta), "tokens": estimar_tokens(ruta),
                             "ignorado": ignorado})
            if ignorado is False:
                hallazgos.append({"nivel": "error",
                                  "msg": f"FUGA: {rel(ruta)} NO esta ignorado por git."})

    arranque = claude_tokens + tokens_estado + imports_tokens
    return {"nombre": eje["nombre"], "raiz": rel(raiz), "piezas": piezas,
            "privados": privados, "arranque_tokens": arranque,
            "arranque_semaforo": semaforo(arranque), "hallazgos": hallazgos}


def construir_reporte(root, filtro_eje=None):
    config, hallazgos = cargar_config(root)
    techos = config.get("_techos", dict(TECHOS_DEFAULT))

    claude = os.path.join(root, "CLAUDE.md")
    claude_tokens = estimar_tokens(claude) if os.path.isfile(claude) else 0
    if claude_tokens == 0:
        hallazgos.append({"nivel": "aviso", "msg": "No hay CLAUDE.md en la raiz."})

    imports = detectar_imports(root)
    imports_tokens = sum(i["tokens"] for i in imports)
    for imp in imports:
        if not imp["existe"]:
            hallazgos.append({"nivel": "error",
                              "msg": f"@{imp['ruta']} se auto-carga pero no existe."})

    ejes = descubrir_ejes(root)
    if filtro_eje:
        ejes = [e for e in ejes if e["nombre"].lower() == filtro_eje.lower()]
    if not ejes:
        hallazgos.append({"nivel": "error", "msg": "No se encontro ningun Current-State.md."})

    analizados = [analizar_eje(root, e, techos, claude_tokens, imports_tokens)
                  for e in ejes]

    if len(analizados) > 1:
        hallazgos.append({
            "nivel": "info",
            "msg": (f"Repo multi-eje: {len(analizados)} vaults independientes. "
                    "Cada sesion carga UNO (ver seccion 3.6)."),
        })

    es_git = os.path.isdir(os.path.join(root, ".git"))
    autores = set()
    if es_git:
        autores |= autores_de(root, "CLAUDE.md")
        for a in analizados:
            for p in a["piezas"]:
                if p["rol"] in ("current-state", "log"):
                    autores |= autores_de(root, p["file"])

    peor = max((a["arranque_tokens"] for a in analizados), default=0)
    return {"root": root, "ejes": analizados, "imports": imports,
            "imports_tokens": imports_tokens, "claude_tokens": claude_tokens,
            "techos": techos, "techos_default": TECHOS_DEFAULT,
            "arranque_peor_caso": peor, "arranque_semaforo": semaforo(peor),
            "git": es_git, "colaborativo": len(autores) > 1,
            "autores_contexto": sorted(autores), "hallazgos": hallazgos}


def imprimir_tabla(r):
    sem = {"verde": "VERDE", "amarillo": "AMARILLO", "rojo": "ROJO"}
    marca = {"error": "[ERROR]", "aviso": "[AVISO]", "info": "[INFO ]"}
    print(f"\nVault: {r['root']}")
    print(f"CLAUDE.md (hard autoload): {r['claude_tokens']:,}t\n")

    for eje in r["ejes"]:
        print(f"EJE: {eje['nombre']}  ({eje['raiz']}/)")
        for p in sorted(eje["piezas"], key=lambda x: (x["rol"] != "current-state", x["file"])):
            carga = {"soft": "soft", "hard": "hard", "no": "-"}[p["autoload"]]
            estado = "VIEJO" if p["viejo"] else "OK"
            nota = f"  - {p['nota']}" if p["nota"] else ""
            sobre = f"  +{p['sobre_techo']:,}t SOBRE TECHO" if p.get("sobre_techo") else ""
            print(f"  [{estado:>5}] {carga:>4} {p['tokens']:>8,}t  {p['file']}{nota}{sobre}")
        for pv in eje["privados"]:
            tag = {True: "ignorado", False: "NO IGNORADO (fuga)", None: "?"}[pv["ignorado"]]
            print(f"  [PRIV ]    - {pv['tokens']:>8,}t  {pv['file']}  - {tag}")
        print(f"  -> ARRANQUE: ~{eje['arranque_tokens']:,}t "
              f"[{sem[eje['arranque_semaforo']]}]\n")

    print(f"[{sem[r['arranque_semaforo']]}] ARRANQUE PEOR CASO: ~{r['arranque_peor_caso']:,} tokens")
    if r["imports"]:
        print(f"\n@imports en CLAUDE.md (se auto-cargan): {r['imports_tokens']:,}t")
        for imp in r["imports"]:
            print(f"   @{imp['ruta']} - {imp['tokens']:,}t"
                  + ("" if imp["existe"] else "  NO EXISTE"))

    print(f"\nRepo git: {'si' if r['git'] else 'no'}")
    if r["colaborativo"]:
        print(f"   COLABORATIVO - autores: {', '.join(r['autores_contexto'])}")
        print("      -> NO reestructures Current-State.md/LOG.md; solo sacalos del auto-load.")

    todos = r["hallazgos"] + [h for e in r["ejes"] for h in e["hallazgos"]]
    if todos:
        print("\nHALLAZGOS")
        for h in todos:
            print(f"   {marca[h['nivel']]} {h['msg']}")
    print()


def main():
    argv = sys.argv[1:]
    as_json = "--json" in argv
    filtro = None
    if "--eje" in argv:
        i = argv.index("--eje")
        if i + 1 < len(argv):
            filtro = argv[i + 1]
            argv = argv[:i] + argv[i + 2:]
    pos = [a for a in argv if not a.startswith("--")]
    root = os.path.abspath(pos[0]) if pos else os.getcwd()
    reporte = construir_reporte(root, filtro)
    print(json.dumps(reporte, ensure_ascii=False, indent=2)) if as_json else imprimir_tabla(reporte)


if __name__ == "__main__":
    main()
