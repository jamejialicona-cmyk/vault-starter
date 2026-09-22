# VAULT-STARTER — Arranca tu proyecto con un Vault dirigido por IA (v4)

> **Qué es esto:** un archivo único y autocontenido para arrancar un proyecto
> bajo el método **VDD × LLM-WIKI**, con **dieta de arranque** — el
> conocimiento vive en un Vault de markdown versionado, no en las
> conversaciones; el agente lo mantiene y el humano lo dirige; y el arranque
> de cada sesión se mide y se mantiene barato a propósito, no por accidente.
> Destilado de **dos despliegues independientes** de meses bajo este esquema,
> en dominios distintos (operaciones de empresa y producción de un videojuego),
> y de tres fuentes: *LLM-WIKI* (A. Karpathy), *Vault-Driven Development v1.0*,
> y el playbook de optimización de contexto `project-context`.
>
> **Cómo usarlo:** copia este archivo a la raíz de tu repositorio y dile a
> tu agente (Claude Code o equivalente):
> *"Lee VAULT-STARTER.md e inicializa el Vault de este proyecto."*
> La sección §10 contiene las instrucciones de bootstrap que el agente debe
> ejecutar, incluyendo extraer el script de auditoría de §9 a un archivo real.
> Todo lo demás es la teoría y los contratos que gobiernan el sistema
> después del arranque.

---

## §1 — La tesis (por qué existe esto)

**El problema con el desarrollo asistido por IA basado en conversaciones:**
el contexto vive dentro del chat; las decisiones importantes quedan
enterradas entre cientos de mensajes; los prompts crecen sin límite; y cada
sesión nueva arranca en frío re-explicándole al modelo cómo funciona el
proyecto. No escala para proyectos de meses o años.

**El problema con las wikis personales:** capturar es fácil, mantener es lo
que nadie sostiene. Cincuenta notas interlinkeadas, consistentes y al día
son un trabajo de editor que las wikis humanas no pagan — por eso se pudren.

**El problema con los Vaults que sí se mantienen:** un Vault que crece sano
en *contenido* puede pudrirse en *costo* — cada sesión nueva puede terminar
pagando 100k+ tokens de arranque antes del primer mensaje, aunque la
auditoría de completitud salga perfecta. Un Vault completo y caro de leer
falla exactamente igual que uno incompleto: el humano deja de confiar en
que abrir sesión sea barato, y empieza a evitarlo.

**La síntesis (tres ideas, un sistema):**

1. **LLM-WIKI (Karpathy):** usa al modelo como *compilador*, no como capa de
   búsqueda. A diferencia de RAG — que re-deriva las mismas relaciones en
   cada consulta y no acumula nada — aquí la síntesis se paga UNA vez al
   ingerir cada fuente, y queda escrita en una wiki interlinkeada que
   *compone* con cada fuente nueva. El costo de mantenimiento que mata a las
   wikis humanas es casi cero para un LLM: no se aburre, no olvida
   cross-referencias, y puede tocar quince archivos en una pasada.
2. **VDD:** el Vault no documenta el desarrollo — **lo dirige**. Es el
   sistema operativo del proyecto: conocimiento, estado y procedimientos
   viven en él; el agente solo lo consulta, interpreta el estado actual y
   ejecuta el siguiente procedimiento. Los prompts son efímeros; los
   procesos (loops) son permanentes. El verdadero activo no es el entregable
   ni los prompts: es el sistema capaz de producir ambos.
3. **Dieta de arranque (project-context):** un Vault correcto puede seguir
   siendo un Vault caro. La completitud del contenido y el costo de leerlo
   son dos ejes independientes — se auditan y se optimizan por separado.
   Solo lo que de verdad se necesita en CADA sesión se auto-carga; el resto
   vive a una ruta de distancia. Esto se mide, no se estima a ojo.

**Separación estricta de roles** (el principio que sostiene todo):
**el humano cura y decide; el agente escribe, enlaza, reconcilia y vigila
el peso.**

**Principios VDD irrenunciables:**

- *Single Source of Truth* — la información permanente existe SOLO en el
  Vault. Nunca solo en conversaciones, ni solo en la memoria del modelo, ni
  solo en los entregables.
- *Reproducibilidad* — cualquier agente (incluso de otro proveedor, vía
  `AGENTS.md` — ver §5.5) debe poder continuar el proyecto leyendo
  únicamente el Vault. El sistema es agnóstico de modelo por diseño.
- *Mínimo cambio* — cambios pequeños, reversibles, fáciles de revisar.
- *Evidencia* — lo que no puede justificarse con información del Vault no se
  asume: se documenta o se pregunta.
- *Instrumento validado* — **un instrumento sin control no mide, y un
  reporte en verde no es lo mismo que una medición.** Antes de creerle a
  cualquier medición, prueba que el instrumento puede detectar el efecto que
  busca (§8.5). Este principio se pagó con tres conclusiones dadas vuelta y
  escritas en el Vault antes de descubrirse.
- *La fuente manda sobre la derivada* — una review, un resumen o un QA que
  parafrasea una fuente es **una capa de traducción con pérdida**. Ante
  conflicto entre una derivada y la fuente original, gana la fuente (§6.6).
- *Sincronización* — entregables, documentación, estado y backlog
  representan la misma realidad SIEMPRE.
- *Arranque barato* — el costo de abrir sesión es una métrica de primera
  clase, con semáforo propio (§9), no un efecto colateral que se revisa
  cuando "se siente lento".
- *Los techos son contratos* — un techo que se sube para que quepa el
  archivo dejó de ser un techo (§7). Moverlo es una decisión que se registra.
- *Diagnóstico antes que acción* — confirmar que algo pasó (o que "se ve
  bien") no autoriza a escribir/ajustar. Un dato 0% o 100% poblado es
  sospechoso por igual: antes de concluir "nadie lo hace" o "no aplica",
  probar UNA escritura/lectura de prueba — a veces la causa es que es
  *imposible*, no que falte disciplina. Presenta el diagnóstico y espera luz
  verde explícita antes de tocar nada que otros dependan de leer.

---

## §2 — Regla de oro

> **Toda sesión empieza leyendo el `Current-State.md` de SU eje. Toda
> operación sigue un loop. Ningún loop termina sin actualizar `00-Index.md`,
> `LOG.md` y `Current-State.md`. El Vault no documenta el desarrollo: lo
> dirige — y su arranque se mantiene barato a propósito.**

(Versión VDD: *antes de modificar el proyecto, comprender el estado; antes
de cambiar el estado, seguir un loop; antes de finalizar un loop, actualizar
el Vault; antes de dar por sano el Vault, medir cuánto pesa arrancarlo.*)

---

## §3 — Estructura y capas

```
<TuProyecto>/
├── CLAUDE.md                  ← reglas de arranque (ver §10) — se auto-carga (hard)
├── AGENTS.md                  ← índice corto para otras IA (ver §5.5) — bajo demanda
├── VAULT-STARTER.md           ← este archivo (queda como referencia)
├── vault-config.json          ← opcional: techos y ejes declarados (ver §9.1)
├── src/                       ← tu trabajo (código, manuscrito, análisis…)
└── Vault/
    ├── SCHEMA.md              ← el modelo de trabajo (este contenido, §2–§9) — bajo demanda
    ├── 00-Index.md            ← catálogo: una línea por página — bajo demanda
    ├── LOG.md                 ← bitácora append-only, EQUIPO (curada) — techo ~40k tokens (§4)
    ├── LOG-Archivo/           ← tramos viejos del LOG, rotados (§4)
    ├── 10-Knowledge/          ← QUÉ es el proyecto (diseño, dominio) — bajo demanda
    ├── 20-State/
    │   ├── Current-State.md   ← punto de entrada de TODA sesión — se auto-carga (soft), techo ~2,500 tokens
    │   ├── Task-Board.md      ← tablero de tareas por frente — bajo demanda
    │   ├── Lecciones.md       ← anti-patrones + entorno técnico — lectura obligatoria antes de ejecutar
    │   ├── Notas-Privadas.md  ← 🔴 PRIVADO, gitignored: estrategia, contexto crudo (ver §5.5)
    │   ├── Bitacora-Privada.md← 🔴 PRIVADO, gitignored: diario crudo append-only (ver §5.5)
    │   └── Decisiones/        ← ADRs (decisiones estructurales) — bajo demanda
    ├── 30-Loops/              ← CÓMO se trabaja (procedimientos) — bajo demanda
    ├── 90-Raw/                ← fuentes inmutables (nadie las edita jamás)
    └── scripts/
        ├── check_vault.py     ← auditoría de peso de arranque (§9), extraído en bootstrap
        └── check_<dominio>.py ← auditoría de consistencia de contenido (§6.7), si aplica
```

| Capa | Dónde | Qué contiene | Quién escribe | Nivel |
|---|---|---|---|---|
| **Raw** | `90-Raw/` | Fuentes originales: documentos, transcripts, referencias, specs congeladas, reviews del humano *verbatim*, versiones superadas de este método | El humano deposita; **nadie edita jamás** | 🟢 equipo* |
| **Schema** | `SCHEMA.md` | Convenciones, plantillas, contratos de loop | Co-autoría humano+agente; cambia despacio | 🟢 equipo |
| **Knowledge** | `10-Knowledge/` | Páginas atómicas del diseño/dominio, compiladas desde raw. Cambia lento. Describe cómo FUNCIONA el proyecto, nunca su progreso | El agente compila; **el humano ratifica** | 🟢 equipo |
| **State** | `20-State/` | Dónde está el proyecto: milestone, tareas, bloqueos, deuda, decisiones recientes, próxima prioridad. Nunca explica el diseño | El agente, después de **cada** tarea | mixto (ver abajo) |
| **Execution** | `30-Loops/` | Procedimientos operativos reutilizables. No contiene conocimiento: contiene procesos | Co-autoría; evolucionan por retroalimentación | 🟢 equipo |
| **Navegación** | `00-Index.md`, `LOG.md` | Catálogo + bitácora curada | El agente, en cada operación | 🟢 equipo |
| **Privado** | `20-State/Notas-Privadas.md`, `Bitacora-Privada.md` | Estrategia cruda, contexto de cliente, diario honesto — nunca se comparte | El agente, a pedido; el humano, libremente | 🔴 privado |
| **Torre de control** | `PROYECTOS.md` (fuera del repo, en tu carpeta de trabajo) | Panorama de TODOS tus proyectos | El humano principalmente | 🔴 privado |

`*` — si una fuente en `90-Raw/` contiene información sensible (ej. una
review con contexto de cliente crudo), táchala como 🔴 en `00-Index.md` y
no la subas a un repo compartido; el resto de Raw es equipo por defecto.

**El Vault como máquina de estados:** cada loop es una transición
`Estado A → Loop → Estado B`, con estado de entrada, condiciones,
resultados esperados y estado de salida. El agente nunca ejecuta un loop
cuyo estado de entrada no se cumple.

### §3.5 — Acceso al Vault: filesystem antes que el MCP de tu app de notas

Si tu Vault vive en una app con su propio MCP (Obsidian, Notion, etc.), **el
agente debería tocarlo por filesystem** (leer/escribir el `.md` directamente)
en vez de por ese MCP, salvo que necesites una función que solo el MCP
expone. Motivo, pagado en un proyecto real: el MCP de una app de notas puede
**desincronizarse a media sesión sin ningún error visible** — devuelve
contenido fantasma (un archivo que en disco tiene páginas de historia
aparece con solo el último párrafo, un listado de directorio muestra 2 de 24
archivos) mientras el resto del Vault sigue intacto en disco. Si algo se ve
raro (pocos archivos, contenido corto) tras usar el MCP, **verifica contra
el filesystem antes de asumir pérdida de datos** — probablemente el MCP es
el que está roto, no el Vault.

Segundo riesgo de la misma familia: un **Vault anidado** (una subcarpeta del
repo que la app trata como Vault independiente, ej. `.obsidian/` propio en
`Proyectos/<X>/`) puede quedar registrado en la configuración **global** de
la app aunque lo borres del filesystem — cada arranque de la app se lo
reabre y regenera la carpeta de la nada, semanas después de haberlo dado por
resuelto. Cuando el síntoma es "algo que ya se había borrado vuelve a
aparecer solo", sospecha de un registro externo al repo (el archivo de
config global de la app), no solo del filesystem/git; la corrección real se
hace desde el selector de Vaults de la app, nunca editando su config a mano
mientras puede estar corriendo.

### §3.6 — Repos multi-eje: varios Vaults independientes bajo un techo

**Nuevo en v4.** Un repositorio puede alojar **varios Vaults independientes**
— llámalos *ejes*. No es una hipótesis: el segundo despliegue de este método
corre tres (un videojuego, una cartera personal, la planeación de un evento),
dos de ellos fuera de git.

Un eje es cualquier carpeta con su **propio `Current-State.md`**. Cada eje
tiene su estado, su LOG, su índice, sus loops y su propio archivo de método
(`SCHEMA.md` o `METODO.md`). No comparten nada salvo el `CLAUDE.md` de la
raíz, que es el único archivo que se auto-carga siempre.

**La regla que hace que funcione: no se cargan dos ejes a la vez.** Mezclar
ejes desperdicia contexto en ambos sentidos — el agente paga el arranque de
un dominio que no va a tocar, y arrastra vocabulario ajeno al que sí. El
`CLAUDE.md` debe nombrar los ejes, decir cuál es el default cuando la sesión
es ambigua, y decir explícitamente que las reglas de un eje no aplican a los
otros.

**Consecuencias operativas:**

- **El arranque se mide por eje, no por repo.** El número que importa es el
  peor caso: `CLAUDE.md` + el `Current-State.md` más pesado + los `@imports`.
  El script de §9.1 los descubre y los mide por separado.
- **Un eje puede estar en `.gitignore` completo.** Un eje personal o con
  datos de cliente vive en el mismo árbol de carpetas sin llegar nunca al
  repo compartido. Verifica con `git check-ignore`, nunca leyendo el
  `.gitignore` a ojo.
- **Un eje puede no existir en un clon.** Documenta esa posibilidad en
  `CLAUDE.md` para que un agente que no encuentra la carpeta no lo trate
  como corrupción.
- **El `Current-State.md` no tiene por qué estar en `20-State/`.** En un eje
  con varias carteras o expedientes vive más abajo (ej.
  `10-Portafolios/<cartera>/Current-State.md`). Por eso el script busca por
  **nombre**, no por ruta.
- **Un eje con dos `Current-State.md` es un error de diseño**, no una
  variante: el punto de entrada debe ser uno. El script lo reporta.

---

## §4 — Navegación: Index y LOG

- **`00-Index.md`** — una línea por página con resumen, agrupada por capa.
  **Se lee primero en toda consulta.** A escala moderada (~300 páginas)
  sustituye cualquier infraestructura de búsqueda/embeddings — no la
  construyas antes de necesitarla.
- **`LOG.md`** — bitácora **append-only** (las entradas nuevas van arriba;
  las viejas no se reescriben), **curada y de equipo** (🟢). Formato
  parseable:

  ```
  ## [YYYY-MM-DD] op | título corto
  Párrafo(s) con lo que pasó, decisiones y punteros.
  ```

  donde `op ∈ {ingest, design, build, review, lint, state}` (adapta el
  conjunto a tu dominio). Distinto de `Bitacora-Privada.md` (§5.5): el LOG
  es lo que el equipo necesita saber que pasó; la bitácora privada es tu
  diario crudo — de ahí puede salir, curado, una entrada del LOG.

### §4.1 — El LOG también tiene techo (nuevo en v4)

v3 le ponía techo a `Current-State.md` y al LOG no le ponía ninguno. El
resultado, medido en un Vault real de dos meses: **un LOG de 190,000
tokens**, once mil líneas. No golpea el arranque de sesión porque es de
lectura bajo demanda — pero *"bajo demanda"* deja de significar algo cuando
el archivo ya no se puede leer de una pasada. Un LOG que nadie puede abrir
entero es un LOG que en la práctica no existe, y su función (que la sesión
siguiente sepa qué pasó) la pierde en silencio.

**Techo sugerido: ~40,000 tokens.** Es el umbral aproximado de "todavía se
lee completo sin partirlo". Al superarlo:

- **Rota, no borres.** Los tramos viejos van a `LOG-Archivo/<periodo>.md`
  (por trimestre o por milestone, lo que corte natural en tu proyecto). El
  archivo rotado se registra en `00-Index.md` como cualquier otra página.
- **El `LOG.md` vivo conserva el periodo en curso** y un encabezado que diga
  a qué archivo fue lo anterior.
- **La rotación es append-only también:** un tramo archivado no se reescribe
  ni se resume al rotarlo. Resumir el LOG al archivarlo destruye justamente
  el detalle por el que existe.

El script de §9.1 mide el LOG de cada eje y marca el exceso.

---

## §5 — Plantilla de página (Knowledge y State)

```markdown
---
status: ratificado | propuesto | borrador
source: "de dónde viene (fuente raw, sesión, decisión)"
updated: YYYY-MM-DD
access: equipo | privado        <!-- default: equipo. Márcalo privado explícitamente -->
---

# Título

Contenido. Enlazar densamente con [[wikilinks]] a toda página relacionada.
```

- `ratificado` = bendecido por el humano; **solo un Design Loop lo cambia**.
- `propuesto` = escrito por el agente, esperando ratificación.
- `borrador` = trabajo en curso, muta libremente.
- Un `[[wikilink]]` a una página inexistente **no es un error**: marca
  trabajo pendiente (el Lint Loop lo recoge).
- `access: privado` en una página de `10-Knowledge/` es una señal de alerta:
  casi siempre esa página debería vivir en `Notas-Privadas.md` en lugar de
  mezclarse con conocimiento compartido. Úsalo solo como bandera transitoria
  mientras la mueves.

### §5.5 — Niveles de acceso: equipo vs privado

- 🟢 **Equipo** (git-tracked, todo el Vault salvo lo listado abajo): lo que
  cualquier colaborador o IA del equipo necesita. Sin secretos, sin
  estrategia cruda, sin contexto de cliente sin filtrar.
- 🔴 **Privado** (gitignored o fuera del repo): `20-State/Notas-Privadas.md`
  (estrategia real, contexto de cliente/político, pendientes personales),
  `20-State/Bitacora-Privada.md` (diario crudo, append-only, de donde sale
  el resumen curado del LOG), `PROYECTOS.md` (torre de control — vive fuera
  de cualquier repo), y **ejes completos** cuando aplique (§3.6).

**Seguridad de los privados:**
- **`.gitignore` con glob, no línea literal:** `Notas-Privadas*` y
  `Bitacora-Privada*` cubren el archivo y cualquier split futuro
  (`Bitacora-Privada-archivo/2026-07.md`) de una vez. Una línea literal es
  el diseño frágil que filtra confidenciales al crear variantes.
- **Verifica con `git check-ignore -q <archivo>`**, no leyendo el
  `.gitignore` a ojo — un glob no aparece como string literal en el
  archivo. El script de §9 lo hace por ti.
- **Nunca credenciales en ningún `.md`** — solo *referencias* a dónde viven
  (gestor de secretos). Si una credencial ya se filtró a git: **rótala y
  purga el historial** — estar en un commit viejo es estar comprometida
  aunque borres el archivo hoy.

**AGENTS.md (opcional, puente multi-herramienta):** si tu equipo mezcla
Claude Code con Codex, Cursor, Gemini u otros, genera un `AGENTS.md` corto
en la raíz — apunta a `Current-State.md` → `CLAUDE.md`/`SCHEMA.md` →
`Lecciones.md`, sin duplicar reglas. Las reglas viven en un solo lugar
(`CLAUDE.md`); `AGENTS.md` es solo el índice de entrada para quien no lee
formato Claude-específico.

### §5.6 — La frontera de idioma se declara en el bootstrap (nuevo en v4)

Si el proyecto produce contenido para un público distinto del idioma en que
tú y el agente conversan, **decláralo el día uno y escríbelo en
`CLAUDE.md`**: qué se escribe en cada idioma y dónde pasa la frontera.

Lo típico es que el Vault (prosa de diseño, análisis, nombres de sección)
viva en tu idioma de trabajo, mientras el contenido de cara al usuario
(guión, UI, copy, documentación pública) viva en el idioma del público. Es
una frontera perfectamente sana — lo que no es sano es descubrirla tarde.

Costo real de no declararla: en un proyecto se decidió a los tres meses, con
diálogo ya escrito en el idioma equivocado, y quedó **deuda de traducción**
anotada y sin fecha. La deuda no bloqueó nada, pero nadie sabe cuánto pesa
hasta que toca pagarla. Decidir tarde es barato; decidir tarde *y no
registrar qué quedó del lado viejo de la frontera* es lo que la vuelve
sorpresa.

---

## §6 — Los loops (contratos, no conversaciones)

Cada archivo en `30-Loops/` define: **Objetivo · Estado de entrada · Fases ·
Validación · Artefactos que actualiza · Estado de salida**. Si un loop
produce errores repetidos, **se mejora el loop, no solo el resultado** — el
sistema aprende de sí mismo. Estructura interna típica de cualquier loop
(VDD): leer estado → leer docs relevantes → planear (impacto/riesgos/
archivos) → implementar → validar → actualizar Vault → notificar siguiente
estado.

Los 5 loops base (adapta nombres a tu dominio):

**Ingest Loop** — fuente nueva → conocimiento compilado.
Entrada: archivo nuevo en `90-Raw/`. Fases: leer Current-State + Index;
leer la fuente completa (NUNCA editarla); crear/actualizar las páginas
Knowledge afectadas (un ingest puede tocar 10–15 páginas) con status
`propuesto` (o `ratificado` solo si la fuente ya viene bendecida);
interlinkear; **señalar contradicciones explícitamente, jamás resolverlas
en silencio**; si la fuente no encaja claramente en ninguna página/categoría
existente, márcala "sin categorizar" en el LOG — **no la adivines**. Salida:
conocimiento compilado; contradicción → Design Loop.
- **Fuentes recurrentes y homogéneas** (dailies, standups, el mismo tipo de
  reporte cada semana) van a una **bitácora** (una página que crece
  cronológicamente), no a una página nueva por ocurrencia — páginas sueltas
  por sesión duplican y ensucian el Index. Reserva la página individual para
  fuentes densas y distintas entre sí (ej. una sesión de diseño larga).
- **Un resumen automático de la fuente (transcripción, meeting notes) puede
  subcubrir sesiones largas o densas sin avisarlo.** Antes de compilar desde
  un `summary`, revisa el tamaño del verbatim disponible; si la fuente es
  larga o estratégica, lee el verbatim por rangos y compila de ahí — el
  resumen automático sirve para fuentes cortas y homogéneas, no para todas.

**Design Loop** — frente de diseño abierto → decisión ratificada.
Entrada: un ítem elegido por el humano o una contradicción detectada.
Fases: leer estado + páginas afectadas + raw relevante; **proponer con
recomendación** (opciones argumentadas, no encuestas exhaustivas); iterar
con el humano; escribir el resultado como `propuesto`; **ratificación
explícita del humano** → `ratificado`; propagar coherencia a toda página
enlazada. Decisión estructural → ADR en `20-State/Decisiones/` (título,
fecha, contexto, alternativas, razón, consecuencias, estado).

**Build Loop** — tarea de trabajo → entregable con gates verdes.
Entrada: tarea del Task-Board con criterios de aceptación y specs
`ratificado`. Fases: leer Current-State + **Lecciones (obligatorio antes de
empezar)** + specs; planear; ejecutar en branch propio con cambios
mínimos; **gates de validación** (los checks propios del proyecto —
defínelos y automatízalos pronto); actualizar Task-Board + Current-State +
LOG + Lecciones si algo dolió; checkpoint. Salida: tarea ✅.

**Review Loop** — de "funciona" a "está bien" (calidad subjetiva).
Entrada: entregable con gates verdes cuyo valor es cualitativo (UX,
estética, redacción, tono). Fases: generar evidencia revisable barata
(capturas, borradores, prototipos, demos — iterar sobre artefactos, no en
vivo); ajustar; cuando convence, **revisión en vivo del humano**; capturar
su feedback como ítems concretos; iterar. Cierre = aceptación explícita
registrada.

**Lint Loop** — salud del Vault (periódico). **Tres ejes independientes**
(v4 añade el tercero):
1. *Completitud/coherencia* — contradicciones (entre páginas, y entre
   páginas y los entregables); wikilinks rotos (= backlog, listar sin
   borrar) y páginas huérfanas; status desactualizados; Index vs. realidad
   (toda página en el Index y viceversa); State vs. repo (Current-State
   refleja el branch/commit real).
2. *Peso de arranque* (§9) — corre `check_vault.py`; si el semáforo sale
   🟡/🔴, es trabajo de este mismo loop aunque no falte ni sobre ningún
   archivo. Ver §9 para las palancas ordenadas por fricción.
3. *Consistencia del contenido* (§6.7) — lo que un linter mecánico puede
   verificar del dominio mismo: citas rotas, aritmética, fuente única,
   rangos, clases incompletas.

Fixes menores en el momento; contradicciones de diseño → Design Loop; peso
de arranque alto → aplicar palancas de §9.

### §6.5 — Loops automatizados (tareas programadas/cron)

Cuando un loop corre solo, sin humano en el prompt (una tarea programada,
un cron), su definición canónica suele vivir **fuera del Vault** (en el
scheduler de tu herramienta de IA), y el archivo espejo en `30-Loops/` es
solo de lectura para el humano. Esto crea un riesgo específico que un loop
manual no tiene: **el espejo puede driftear del schema real sin que nadie lo
note**, porque nadie edita el archivo fuente en cada cambio de estructura
del Vault (ej. una migración de layout). Señal típica: una corrida instruye
leer una ruta que ya no existe, y en vez de corregir el archivo fuente,
cada corrida "lo parcha al vuelo" — el mismo error reaparece semanas después
porque el archivo fuente sigue apuntando a lo viejo. Cuando una corrida
detecta que su propia definición apunta a algo obsoleto, no basta con
improvisar esa corrida: **corrige el archivo fuente** (o dilo como tarea
explícita) para que no se repita. Si tu scheduler no permite elegir modelo
por tarea, documenta en Lecciones cuál es el modelo mínimo viable con el que
SÍ corren todas las rutinas — no asumas que puedes bajar de ahí.

Vale la pena, además, un lugar para **patrones compartidos entre varios
loops** — no todo conocimiento operativo es un loop completo (Objetivo →
Fases → Estado de salida); a veces son 3-5 pasos que 2-3 loops distintos
repiten con la misma fricción (ej. "cómo generar un correo desde el estado
del Vault", usado por tres rutinas de distinto horario). Documentarlo una
vez en un archivo de patrón (`30-Loops/Patrones/<nombre>.md`, referenciado
por los loops que lo usan) evita que cada loop nuevo reinvente los mismos
pasos y la misma fricción.

### §6.6 — Cómo se actúa sobre un hallazgo (nuevo en v4)

v3 decía cómo *detectar* problemas y no decía nada de cómo *repararlos*.
Cuatro rondas de QA seguidas fallaron en un proyecto real por la misma
razón, así que aquí va explícito:

> **Todo fix va a la FUENTE del dato, nunca a la línea reportada. Y antes de
> cerrarlo, se barre la CLASE ENTERA de menciones en todo el Vault.**

Un linter o un QA te reportan **un síntoma con coordenadas**: archivo y
línea. Eso no es el problema. El problema es la página que originó el dato
equivocado y se propagó por wikilinks a otras seis. Corregir la línea
reportada deja la fuente intacta, así que el siguiente barrido vuelve a
encontrarlo — en otra línea, y parece un hallazgo nuevo.

El procedimiento, en orden:

1. **Localiza la fuente.** ¿De dónde salió este dato? ¿Qué página lo declara
   por primera vez, y con qué `source:`?
2. **Corrige ahí.** La página fuente primero, con su `updated:`.
3. **Grep de la clase completa** en todo el Vault, no de la cadena exacta
   reportada. Si el error era una fecha, busca todas las fechas de ese
   evento; si era una cifra, todas las menciones de esa cifra y sus
   derivadas aritméticas.
4. **Solo entonces cierra el hallazgo**, y anota en el LOG cuántas
   ocurrencias tenía la clase — es el número que dice si el fix valió.

**Corolario, el principio de la fuente sobre la derivada (§1):** cuando el
hallazgo viene de una review humana o de un QA de IA que *describe* una
fuente en vez de citarla, y esa descripción contradice la fuente original,
**gana la fuente**. Dos incidentes reales del mismo proyecto: una review
pidió un ajuste que contradecía la referencia visual original y se
implementó la review, fosilizando el error durante dos rondas; y un QA
parafraseó una imagen en texto, la paráfrasis se implementó literal, y al
mirar la imagen directamente resultó ser otra cosa. Para forma, geometría o
cifras específicas, **mirar la fuente gana** — toda paráfrasis es traducción
con pérdida.

### §6.7 — El linter mecánico va antes que el juicio caro (nuevo en v4)

Si tu dominio tiene reglas de consistencia que una máquina puede verificar,
**escríbelas como script y córrelo antes de gastar un subagente de juicio.**

En el segundo despliegue esto es `check_canon.py`: casi mil líneas que
barren citas rotas, aritmética que no cuadra, violaciones de fuente única,
rangos fuera de norma, clases incompletas y duplicados. Sale con código 1 si
hay críticos. La regla del proyecto es que **no se auditan contenidos con
subagentes hasta que el linter pasa**.

La razón es de tiering, el mismo principio de §8: un chequeo determinista es
barato, reproducible y no alucina. Un subagente de juicio es caro, lento y
su valor está en lo que *no* se puede mecanizar — tono, coherencia
narrativa, si una decisión de diseño se sostiene. Gastarlo en encontrar una
cita rota es desperdiciarlo, y además introduce ruido: un QA que reporta
veinte hallazgos mecánicos entierra los tres de juicio que sí importaban.

Qué suele ser mecanizable en cualquier dominio:

- **Integridad referencial** — toda cita apunta a algo que existe, todo
  wikilink resuelve, todo lo que está en el Index existe y viceversa.
- **Aritmética** — los números que se derivan de otros, cuadran.
- **Fuente única** — un mismo dato declarado en dos páginas es un error de
  diseño, no una redundancia útil.
- **Completitud de clase** — si el dominio define ocho categorías, las ocho
  aparecen donde deben aparecer.
- **Frescura** — `updated:` contra la última modificación real del archivo.

---

## §7 — Current-State, Lecciones y la rutina de cierre de sesión

Estos tres mecanismos son los que hacen que el sistema sobreviva al cambio
de sesión, de contexto y hasta de modelo. Son la parte más importante de
todo el método.

### Current-State.md — el punto de entrada (y la pieza que se auto-carga)

Describe SOLO dónde está el proyecto (milestone, qué se cerró, qué está en
curso, qué está bloqueado y con qué sospecha, deuda visible, riesgos) y
**termina siempre con una sección "ARRANQUE DE LA PRÓXIMA SESIÓN"**: qué
sigue, en qué orden, y **qué decisiones esperan al humano** (lista
explícita). Un agente que arranca en frío — posiblemente OTRO modelo — debe
poder continuar leyendo solo `CLAUDE.md → Current-State.md`, sin perder
ninguna decisión.

**Techo ~2,500 tokens.** Se lee al abrir cada sesión (por instrucción/
protocolo, aunque el harness no lo auto-inyecte como a `CLAUDE.md` — es
"soft-load": el costo real es el mismo si el protocolo se respeta). Es la
palanca más sensible de la dieta de arranque (§9): un `Current-State.md`
que narra CÓMO llegamos aquí crece sin techo. Si te descubres narrando
historia aquí, muévela a `LOG.md` (curado) o a `Vault/20-State/
Estado-Historico.md` (archivo, opcional). Se **sobrescribe** (refleja el
presente); la historia vive en el LOG.

### §7.1 — Un techo es un contrato, no una sugerencia (nuevo en v4)

Auditando un Vault real apareció esto: el `Current-State.md` medía 2,662
tokens, y el script local tenía el techo en 3,000 con un comentario que lo
justificaba. El techo de referencia son 2,500. Nadie hizo nada malo a
propósito — pero el archivo creció, el techo se movió detrás, y el semáforo
quedó en verde sin que nada se hubiera recortado.

**Un techo que se sube para que quepa el archivo dejó de ser un techo.** Es
la forma más silenciosa de perder una métrica: no falla, no avisa, y sigue
saliendo verde para siempre.

La regla de v4:

- **Los techos viven en un solo lugar** (`vault-config.json`, §9.1), no
  editados a mano dentro de una copia del script.
- **Un techo modificado se REPORTA** en cada corrida, diciendo cuál es el
  default y cuánto se movió. El script de §9.1 lo hace.
- **Moverlo es una decisión**, y como toda decisión se registra en el LOG
  con su porqué. Si el porqué es "el archivo no cabía", la decisión correcta
  casi siempre era recortar el archivo.

### Lecciones.md — la memoria dura

Anti-patrones técnicos y datos del entorno, ganados con dolor real. Cada
entrada es una regla accionable con su porqué (ej.: "nunca X — en tal fecha
causó Y; hacer Z en su lugar"). Reglas de mantenimiento:

- **Lectura obligatoria antes de empezar a ejecutar** (todo Build Loop, y en
  el brief de todo subagente ejecutor) — deliberadamente NO se auto-carga:
  es de bajo-demanda pero de lectura forzada por protocolo, no por harness.
- Si una sesión paga una lección nueva, **se escribe ANTES de cerrar** — una
  lección no escrita se volverá a pagar.
- Se **sobrescribe/refina**: si una lección resulta incompleta o queda
  obsoleta, se corrige o retira en el momento (no es append-only; es la
  versión VIVA del cuidado operativo). Incluye también una sección "Entorno"
  (rutas, comandos de build/test, gates de calidad, peculiaridades de la
  máquina).

### Disciplina de fecha

**La fecha de "hoy" nunca sale del prompt, del nombre de un archivo ni de la
memoria del agente — se corre el comando de fecha del sistema en el primer
turno que vaya a escribir algo fechado** (un archivo en `90-Raw/`, una
entrada de `LOG.md`, un `updated:` de frontmatter, una nota en un sistema
externo). Un prompt escrito el viernes y ejecutado el lunes es una fuente de
fecha tan desactualizada como un reloj de sesión — y una corrida larga
(reintentos, fallos de red) puede cruzar medianoche a mitad de ejecución, así
que si la sesión se alarga mucho, vuelve a correr el comando de fecha antes
de fijar la fecha de captura de cualquier snapshot nuevo. Cuando el artefacto
fechado ya salió a un sistema externo (un comentario posteado, un correo
enviado) con la fecha equivocada, corregirlo cuesta una escritura en
producción — razón de más para verificar la fecha ANTES del primer `create`,
no después.

### La rutina de cierre de sesión (checklist de 7 pasos)

Ejecutar al final de cada sesión — y en versión reducida (checkpoint) tras
CADA tarea, porque las sesiones largas mueren por compaction, límites de
tokens o cambios de modelo sin avisar:

1. **`Current-State.md` refleja la realidad** — incluida la sección de
   ARRANQUE (qué sigue, qué decisión espera al humano, qué quedó bloqueado
   y con qué sospecha) — y sigue bajo el techo de ~2,500 tokens.
2. **`LOG.md`**: una entrada por operación de la sesión (`op | título`), y
   rotación si pasó el techo de §4.1.
3. **`00-Index.md`**: al día si hubo páginas nuevas, movidas o re-descritas.
4. **`Lecciones.md`**: si la sesión pagó una lección, se escribe antes de
   cerrar.
5. **`Bitacora-Privada.md`** (si la usas): una entrada cruda de la sesión —
   nunca se sube al repo.
6. **Working tree limpio**: commit descriptivo + push del branch de trabajo.
   Nada queda sin commitear salvo decisión explícita del humano (y se anota
   en Current-State como WIP).
7. **Nada se reporta como terminado sin evidencia** — gates verdes o
   artefactos revisables; lo no verificado se marca "pendiente de VoBo". Y
   **la evidencia solo vale si el instrumento está validado** (§8.5).

---

## §8 — Orquestación (opcional pero rentable)

- **Un solo orquestador** (el modelo más capaz disponible): lee el Vault,
  selecciona el loop, planifica, divide el trabajo, elige modelos, integra
  resultados y actualiza el estado. No debe implementarlo todo él mismo.
- **Tiering de modelos**: cada tarea usa el modelo más adecuado, no el más
  grande — lógica/arquitectura al modelo grande; ejecución mecánica
  (boilerplate, formateo, inventarios, QA repetitivo) a modelos
  medianos/chicos como subagentes. Paraleliza lo independiente. **Y antes
  del modelo más chico está el script determinista** (§6.7): si una regla se
  puede verificar con código, no gastes un modelo en ella.
- **Gate de validación antes de aprobar cualquier cambio**: los checks del
  proyecto en verde, documentación actualizada, State actualizado, backlog
  consistente. Solo entonces la máquina de estados avanza.
- **Verifica que un reintento anunciado en el chat de verdad se ejecutó** —
  no solo que se redactó la intención. Es fácil que un agente orquestador
  "diga" que va a relanzar un subagente y nunca emita la llamada. Confirma
  con evidencia externa (¿el archivo que ese subagente debía escribir
  existe?), no con la propia narración del turno anterior.
- **Un subagente en background que se estanca no predice su tamaño de
  tarea** — uno con datos triviales puede colgarse igual que uno que pagina
  miles de registros. Tras **2 reintentos fallidos** (error o timeout) del
  mismo agente, deja de relanzarlo a ciegas y ejecuta la consulta
  **directamente en el hilo principal** (misma llamada, mismo procesamiento
  determinista si el resultado excede el límite de tokens) — es más rápido
  que un tercer intento, y evita que el agente fantasma reaparezca después
  e intente sobrescribir un archivo que ya arreglaste a mano.
- **Si tu orquestación corre como tarea programada (cron/scheduler) sobre el
  mismo filesystem que usas interactivamente, verifica que SÍ pueda escribir
  sobre archivos preexistentes del Vault**, no solo crear archivos nuevos —
  algunos entornos (permisos de sesión heredados del SO) dejan crear pero no
  editar, y el síntoma es un error de permisos silencioso o poco claro en
  Read/Edit/git sobre archivos que ya existían antes de que la tarea
  programada corriera por primera vez. Pruébalo con una escritura trivial
  antes de confiarle un loop completo.

### §8.5 — Instrumentación: el capítulo que v3 no tenía (nuevo en v4)

Todo lo anterior asume que cuando mides algo, la medición significa algo.
Esa suposición falló tantas veces en un despliegue real que merece sección
propia. Nada de esto es específico de programar: aplica a cualquier medición
que dirija una decisión.

**1. Un instrumento sin CONTROL no mide.** Un barrido probó nueve
configuraciones distintas de un componente y las nueve dieron cero efecto.
La conclusión obvia — "el componente no sirve" — habría sido una de tres
causas posibles; las otras dos eran que el banco de pruebas estuviera mal
armado. Lo que convirtió esos nueve ceros en evidencia fue **una décima
fila: un control que producía el efecto por otra vía**, y sí midió. Sin esa
fila, nueve ceros no prueban nada.

> **Regla: toda suite de medición lleva un caso de control con efecto
> conocido. Si el control no mide, ninguna otra fila significa nada.**

**2. Verde no es lo mismo que medido.** Un test imprimió éxito total con un
bloque entero muerto adentro: el componente que instanciaba no compilaba,
devolvió basura, el bloque murió con error en la salida, y el contador de
fallas nunca se movió porque un error de ese tipo no lo tocaba. Fue la
cuarta vez en dos días que un instrumento reportaba verde sin haber medido.
El patrón no es el bug puntual: es **confiar en el veredicto sin mirar la
salida completa**.

> **Regla: antes de creerle a un verde, verifica que el instrumento
> realmente ejecutó lo que dice haber ejecutado.**

**3. Una A/B solo prueba algo si cambia UNA variable.** El intento de
validar un instrumento dio una diferencia medible que pareció confirmarlo.
Era falsa: entre las dos capturas había quedado corriendo otra cosa, así que
la diferencia era esa otra cosa. Con la única variable aislada, la
diferencia era exactamente cero. Media jornada.

**4. Tras dos iteraciones que no cierran, sospecha del ANDAMIAJE.** Dos
rondas de ajuste fino fallaron seguidas; a la tercera se descubrió que el
trabajo fino estaba correcto y el parámetro estructural de abajo estaba mal
desde el principio. Ninguna cantidad de pulido de superficie arregla un
cimiento equivocado.

> **Regla: si dos intentos razonados no cierran, deja de refinar y cuestiona
> el nivel de abajo — la proporción, el pivote, la suposición de entrada.
> Seguir iterando sin hipótesis nueva quema presupuesto sin converger.**

Es el mismo número que el límite de reintentos de un subagente colgado
(§8), y no es casualidad: dos fracasos son la señal más barata de que el
modelo mental del problema, y no el intento, es lo que hay que cambiar.

**5. Prefiere una señal positiva a una ausencia.** Para encontrar cuál de
ocho piezas causaba un defecto, se fueron ocultando una por una: el
resultado salió idéntico las ocho veces, lo que no distingue "esta pieza no
es la culpable" de "mi cambio no se está aplicando". Se llegó a dudar de si
el código recargaba. Marcar cada pieza con un color imposible de confundir,
en vez de ocultarla, identificó la culpable al primer intento. **Una
ausencia es ambigua; una señal positiva no.**

**6. El defecto puede vivir en la COSTURA, no en las piezas.** Dos
componentes revisados línea por línea, ambos correctos, y el defecto estaba
en el contrato entre ellos: uno generaba en una convención de ejes y el otro
consumía en la contraria. Ninguna revisión estática lo detectó porque no
había nada mal en ningún archivo. Solo lo mostró una construcción
end-to-end.

> **Regla: al escribir un par generador/consumidor, escribe el contrato en
> la documentación de AMBOS, y verifica UNA construcción completa antes de
> autorar veinte encima.**

---

## §9 — Dieta de arranque: auditoría, semáforo y palancas

Esto es lo que aporta `project-context` al método: una métrica objetiva
para "¿este Vault pesa demasiado?" — en vez de esperar a que la sesión "se
sienta lenta".

### 9.1 — Medir (solo lectura)

Extrae el script de abajo a `Vault/scripts/check_vault.py` (paso de
bootstrap, §10) y corre:

```bash
python3 Vault/scripts/check_vault.py           # tabla legible
python3 Vault/scripts/check_vault.py --json    # para que lo consuma el agente
python3 Vault/scripts/check_vault.py --eje Boda
```

**Qué cambió en v4.** La versión de v3 traía las rutas del Vault
**incrustadas en una constante**. En la práctica eso obliga a cada proyecto
a editar el script a mano, y ahí empieza el drift: en el despliegue donde se
detectó, la copia local había cambiado además el techo de `Current-State`
sin que nadie lo notara. Esta versión **descubre los ejes** buscando por
nombre de archivo, así que funciona sin editarla; y los techos viven en un
`vault-config.json` opcional, cuyos cambios el reporte declara en voz alta.

`vault-config.json` (opcional, en la raíz):

```json
{
  "techos": { "current_state": 2500, "log": 40000 }
}
```

```python
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
```

### 9.2 — Leer el diagnóstico

El semáforo de **arranque** es la métrica que importa, no si algún archivo
individual "se ve grande". 🟢 < 10,000 · 🟡 10,000–30,000 · 🔴 más de 30,000.

En un repo multi-eje (§3.6) el número que manda es el **peor caso**: el eje
más caro de abrir. Un promedio esconde justo al que duele.

Si sale 🟡/🔴, es trabajo del Lint Loop (§6) **aunque la auditoría de
completitud salga perfecta y no falte ningún archivo**.

Y lee también los **HALLAZGOS**, no solo el semáforo: un techo modificado, un
LOG sin rotar o un eje con dos `Current-State.md` no mueven el color y son
igual de importantes.

### 9.3 — Palancas, ordenadas por fricción (ataca primero la de fricción cero)

1. **`@imports` → bajo demanda.** Quita `@` de los docs de `10-Knowledge/`
   que no se necesitan cada sesión (arquitectura ya construida, specs de
   features cerradas). Suele ser la palanca grande y de fricción cero: solo
   edita `CLAUDE.md`, no toca ningún contenido.
2. **Sacar `Bitacora-Privada.md`/`LOG.md` del hábito de auto-lectura** si tu
   protocolo los está leyendo completos cada vez. El ahorro viene de NO
   auto-cargarlos, no de recortarlos — pídele al agente que lea solo la
   última entrada.
3. **Rotar el LOG** a `LOG-Archivo/` si pasó el techo de §4.1. No baja el
   arranque (el LOG no se auto-carga), pero devuelve la legibilidad que es
   su razón de existir. Fricción nula: es append-only, nada se pierde.
4. **`Notas-Privadas.md`:** separa lo vivo de lo histórico/pesado a
   `Notas-Privadas-Archivo.md` (cubierto por el mismo glob). Fricción nula
   (es privado, tuyo).
5. **`Current-State.md` → techo.** Recorta a solo-presente; histórico
   verbatim a `Vault/20-State/Estado-Historico.md`. **Mayor fricción** si el
   Vault es colaborativo (ver 9.4). **Nunca subas el techo en vez de
   recortar** (§7.1).

### 9.4 — Ajustar por modo del Vault

- **Individual:** libertad para reestructurar.
- **Colaborativo** (el script lo marca vía autores en el historial de
  `Current-State.md`/`LOG.md`/`CLAUDE.md`): **NO reestructures
  `Current-State.md`/`LOG.md`** — son append/edición compartida;
  reestructurarlos choca con el próximo cambio de otro colaborador. Solo
  sácalos del auto-load, recorta con cuidado, y documenta el patrón nuevo en
  `CLAUDE.md`. Si el cambio va a la rama principal, avisa al equipo antes
  (sincronicen ramas).

### 9.5 — Salvaguardas al ejecutar

- **Cero pérdida de dato:** nada sale de un archivo sin aparecer íntegro en
  su destino; verifica con diff de contenido. Para archivos trackeados,
  contra `git show HEAD:`; para gitignored, contra una copia temporal.
- **Cero fuga de dato:** todo destino de contenido confidencial verificado
  con `git check-ignore` ANTES de escribirlo.
- **Trabaja en rama aparte** si es colaborativo (`chore/optimizar-vault`),
  no en la rama principal.
- **Presenta el plan y espera OK** antes de tocar nada; muestra el diff
  antes de commitear.
- **Verificar:** re-corre el script — confirma que el arranque bajó al
  verde, que los techos se respetan **sin haberlos movido**, y que
  `git status` deja a los privados fuera de git.

### 9.6 — Puentes (ofrecer, no imponer)

- **claude.ai / Projects:** genera `_contexto_para_chat.md` concatenando
  `CLAUDE.md` + `Current-State.md` + `SCHEMA.md`, para subir como knowledge
  a un Project. En repo multi-eje, **uno por eje** — nunca los tres juntos.
  Avisa si algún archivo viene inflado (> ~5k tokens por archivo).
- **Hook de cierre de sesión (opcional):** un script no-bloqueante que
  recuerda los 7 pasos de §7 al terminar (evento `Stop`/`SessionEnd` en
  `.claude/settings.json`).
- **Aviso en `SessionStart` (opt-in):** solo si lo piden explícitamente.

---

## §10 — BOOTSTRAP (instrucciones para el agente)

Si un humano te pidió inicializar el Vault desde este archivo:

1. Pregunta (una sola tanda):
   - nombre del proyecto y dominio (software, investigación, escritura,
     producto, operaciones… lo que sea);
   - qué fuentes raw existen ya;
   - cómo se valida un entregable aquí (tests, revisión, criterios de
     aceptación…), **y con qué caso de control se comprueba que ese
     instrumento de validación de verdad mide** (§8.5);
   - si el proyecto será **individual o colaborativo** (cambia §9.4 desde el
     día 1);
   - **si este repo va a alojar más de un eje** (§3.6), y cuál es el default
     cuando la sesión sea ambigua;
   - **cuál es la frontera de idioma** (§5.6): qué se escribe en el idioma de
     trabajo y qué en el idioma del público.
2. Crea la estructura de §3 (carpeta `Vault/` o en la raíz, a gusto del
   humano — respeta lo que ya exista). Si hay varios ejes, una carpeta por
   eje, cada una con su propio `Current-State.md`.
3. Genera `SCHEMA.md` con el contenido de §2–§9 de este archivo (adaptando
   nombres de loops al dominio). En multi-eje, un `SCHEMA.md`/`METODO.md`
   por eje.
4. Genera semillas: `00-Index.md` (catálogo inicial), `LOG.md` (primera
   entrada: `state | Vault inicializado`), `Current-State.md` (estado real
   actual + ARRANQUE, bajo el techo de ~2,500 tokens), `Task-Board.md`
   (frentes vacíos o migrando el backlog existente), `Lecciones.md`
   (sección Entorno con build/test/rutas), los 5 loops de §6 como archivos
   en `30-Loops/`, y `AGENTS.md` si el proyecto mezclará herramientas de IA.
5. Extrae el script de §9.1 a `Vault/scripts/check_vault.py` **sin
   editarlo** — descubre los ejes solo. Si necesitas cambiar un techo, crea
   `vault-config.json` (§7.1). Córrelo una vez para la línea base.
6. Genera o actualiza `CLAUDE.md` con el bloque de §11.
7. **Privacidad:** si hay repo git, asegura que `.gitignore` use los globs
   `Notas-Privadas*` y `Bitacora-Privada*` (crea el archivo si no existe), y
   las carpetas de los ejes privados completos; verifica con
   `git check-ignore`, no a ojo. `PROYECTOS.md` vive fuera del repo.
8. Si hay fuentes existentes (README, specs, docs): ejecuta un primer
   Ingest Loop para compilarlas a Knowledge.
9. Si el dominio tiene reglas de consistencia mecanizables (§6.7), propón un
   `check_<dominio>.py` — aunque arranque con dos o tres chequeos.
10. Ofrece los puentes de §9.6 (no los impongas).
11. Cierra con la rutina de §7 (incluido el primer commit) y muestra el
    reporte de `check_vault.py` como línea base de arranque.

---

## §11 — CLAUDE.md sugerido (copia y adapta)

```markdown
# <PROYECTO> — reglas del repo

1. Toda sesión empieza leyendo el `Current-State.md` de SU eje.
   <Si hay un solo eje, borra el resto de este punto.>
   Este repo tiene N ejes independientes:
   - **<Eje A>** → `<ruta>/20-State/Current-State.md`. Es el default: si no
     está claro de qué trata la sesión, es este.
   - **<Eje B>** → `<ruta>/…/Current-State.md`, con su método propio en
     `<ruta>/METODO.md`. Carpeta en `.gitignore`: puede no existir en un clon.
   **No se cargan dos a la vez.** Las reglas de un eje no aplican a los otros.
2. El modelo de trabajo (capas, loops, plantillas, dieta de arranque) está
   en `Vault/SCHEMA.md` — toda operación sigue un loop de `Vault/30-Loops/`.
3. Las fuentes de `Vault/90-Raw/` son inmutables — jamás se editan. La
   verdad viva vive en `10-Knowledge/`; el estado, en `20-State/`.
4. Ningún loop termina sin actualizar `00-Index.md`, `LOG.md` y
   `Current-State.md` (checkpoint tras CADA tarea; rutina completa de
   cierre en SCHEMA §7).
5. Lecciones obligatorias antes de empezar a ejecutar:
   `Vault/20-State/Lecciones.md`.
6. Arranque de sesión barato por diseño: nada pesado se auto-carga vía
   `@import` salvo lo que se necesita en CADA sesión (SCHEMA §9). Si
   `check_vault.py` marca amarillo/rojo, es trabajo del Lint Loop. Los
   techos no se suben para que quepa el archivo (SCHEMA §7.1).
7. Antes de auditar contenido con subagentes, corre el linter mecánico
   (`check_<dominio>.py`). Los subagentes de juicio se reservan para lo que
   exige juicio (SCHEMA §6.7).
8. Todo fix va a la FUENTE del dato, no a la línea reportada; grep de la
   clase completa antes de cerrarlo (SCHEMA §6.6).
9. Ninguna medición vale sin control, y un verde no es una medición
   (SCHEMA §8.5).
10. Lo sensible va a `Vault/20-State/Notas-Privadas.md` o
    `Bitacora-Privada.md` (gitignored), nunca a un archivo de equipo.
11. Idioma: <el Vault en X; el contenido de cara al usuario en Y>
    (SCHEMA §5.6).
12. El humano cura y decide; el agente escribe, enlaza, reconcilia y vigila
    el peso. Nada `ratificado` se cambia sin Design Loop.
13. Otras IA (Codex, Cursor…) entran por `AGENTS.md`, que apunta aquí — las
    reglas viven en un solo lugar.
```

---

## §12 — Consejos de campo (pagados con sesiones reales)

- **Las reviews del humano se archivan *verbatim* en `90-Raw/`** y se usan
  como checklist de aceptación — no las parafrasees al compilarlas. Y si una
  review contradice la fuente original, **gana la fuente** (§6.6).
- **El LOG lleva lo que pasó (curado, equipo); Current-State lleva lo que
  ES; la Bitácora Privada lleva lo crudo (tuyo).** Si te descubres narrando
  historia en Current-State, muévela al LOG o a la bitácora privada según
  si es de equipo o personal.
- **Un LOG que ya no se puede leer entero dejó de cumplir su función.**
  Rótalo por periodo (§4.1) antes de que llegue ahí, no después.
- **Registra también los WIP y los bloqueos** con la sospecha diagnóstica
  ("se cuelga; sospecha: contención de recursos; próximo paso: X") — la
  sesión siguiente arranca investigando, no redescubriendo.
- **Sesiones paralelas se sincronizan por el Vault**, no por chat: la que
  decide escribe en Current-State/LOG y commitea; la otra hace pull y lee.
- **Nada se muestra al humano como terminado sin evidencia** (captura, test
  verde, demo). Marca "pendiente de VoBo" sin vergüenza. **Y antes valida el
  instrumento** — un verde sin control no es evidencia (§8.5).
- **Si dos intentos razonados no cierran, cuestiona el andamiaje**, no sigas
  puliendo la superficie (§8.5).
- **Prefiere una señal positiva a una ausencia** cuando busques una causa:
  una ausencia no distingue "no es esto" de "mi cambio no se aplicó" (§8.5).
- **Edita archivos del Vault solo con herramientas que preserven encoding**
  (UTF-8); los one-liners de shell tipo `Get-Content | Set-Content` en
  Windows corrompen acentos. Lección pagada.
- **Un `[[wikilink]]` roto es backlog, no basura.** El Lint Loop vive de
  ellos.
- **Un Vault completo puede seguir siendo un Vault caro.** Completitud y
  peso de arranque son dos ejes distintos — audítalos por separado (§9) y no
  confundas "no falta nada" con "arranca barato". Y ninguno de los dos te
  dice si el contenido es *consistente*: ese es un tercer eje (§6.7).
- **En Vault colaborativo, nunca reestructures `Current-State.md`/`LOG.md`
  para ahorrar tokens** — solo sácalos del auto-load. Reestructurar un
  archivo de append/edición compartida choca con el próximo cambio de otro
  colaborador; ya causó conflictos reales.
- La ratificación del humano es **explícita o no es** — "me gusta" en chat
  no cambia un status; pídela y regístrala con fecha.
- **Trabaja el Vault por filesystem, no por el MCP de tu app de notas**
  (ver §3.5) — es más rápido y no se desincroniza a media sesión.
- **La fecha de "hoy" se corre, nunca se hereda** de un prompt, un nombre de
  archivo o la memoria del agente (ver §7, Disciplina de fecha).
- **`write_uid`/"última modificación" dice quién tocó el registro AL
  ÚLTIMO, no quién ejecutó una acción concreta** — para atribuir una acción
  a una persona, busca el log de auditoría/actividad con autor y hora
  (chatter, audit log), no el campo de última escritura.

---

## §13 — Registro de cambios

**v4 — generada 2026-09-11.** Auditoría de v3 contra un **segundo
despliegue independiente** del método: un Vault de producción de videojuego
con dos meses de operación, 693 líneas de Lecciones, tres ADRs y siete
loops. La v3 se había destilado de un despliegue de operaciones de empresa;
que un segundo Vault en un dominio completamente distinto validara el
esqueleto y encontrara once huecos es, en sí, el dato más fuerte a favor del
método. Los once hallazgos, todos trazables a incidentes medidos:

1. **§4.1 — El LOG no tenía techo.** Se midió uno de 190,000 tokens. Techo
   de ~40,000 y rotación append-only a `LOG-Archivo/`.
2. **§7.1 — Los techos son contratos.** Se encontró el techo de
   `Current-State` subido de 2,500 a 3,000 para que cupiera el archivo.
   Ahora los techos viven en `vault-config.json` y toda modificación se
   reporta en voz alta.
3. **§9.1 — El script dejó de traer rutas incrustadas.** La versión de v3
   obligaba a editarlo por proyecto, y en esa edición se coló el hallazgo 2.
   Ahora descubre los ejes buscando por nombre de archivo.
4. **§3.6 — Repos multi-eje.** Varios Vaults independientes bajo un repo,
   con la regla de no cargar dos a la vez, medición de arranque por eje y
   peor caso como número rector.
5. **§6.7 — Tercer eje del Lint Loop: consistencia de contenido.** El linter
   mecánico del dominio corre ANTES de gastar subagentes de juicio.
6. **§6.6 — Cómo se actúa sobre un hallazgo.** Todo fix va a la fuente del
   dato, nunca a la línea reportada, con grep de la clase entera. Cuatro
   rondas de QA fallaron por ignorarlo.
7. **§8.5 y §1 — Un instrumento sin control no mide.** Nueve resultados en
   cero solo significaron algo cuando apareció la fila de control.
8. **§8.5 — Verde no es lo mismo que medido.** Un test reportó éxito con un
   bloque muerto adentro; cuarta vez en dos días.
9. **§8.5 — Tras dos iteraciones fallidas, sospecha del andamiaje.** Dos
   rondas puliendo la superficie sobre un parámetro estructural equivocado.
10. **§1, §6.6 y §12 — La fuente manda sobre la derivada.** Una review y un
    QA parafrasearon sus fuentes y ambas paráfrasis se implementaron mal.
11. **§5.6 — La frontera de idioma se declara en el bootstrap.** Decidirla
    tarde dejó deuda de traducción sin dimensionar.

Además, §8.5 recoge dos corolarios de la misma familia (preferir una señal
positiva a una ausencia; el defecto que vive en la costura entre dos piezas
correctas) y §10 incorpora las preguntas nuevas al bootstrap.

**v3 — generada 2026-09-11**, a partir de ~2 meses de operación real de un
Vault de operaciones (29 lecciones pagadas, 9 ADRs, 7 loops automatizados
corriendo por scheduler). Adiciones sobre v2: principio de diagnóstico antes
que acción; acceso por filesystem y Vault anidado (§3.5); bitácora vs.
página-por-sesión en el Ingest; loops automatizados y drift del espejo
(§6.5); disciplina de fecha (§7); verificación de reintentos y límite de dos
para subagentes estancados (§8).

**v2 — generada 2026-07-20**, fusionando el VAULT-STARTER original
(2026-07-13) con el playbook de optimización de contexto `project-context`
(auditoría de tokens, niveles equipo/privado, puentes).

Las versiones superadas se archivan en `90-Raw/` como cualquier otra fuente
inmutable: `VAULT-STARTER-v2.md`, `VAULT-STARTER-v3.md`.

Fuentes teóricas: "LLM-WIKI — A Self-Maintaining Personal Knowledge Base
Architecture Using LLMs" (A. Karpathy), "Vault-Driven Development v1.0", y
el patrón probado de proyectos reales con arranque de sesión medido en
tokens. Licencia: compártelo y adáptalo libremente.
