#!/usr/bin/env bash
# Hook de PostToolUse (Edit|Write). Si el archivo tocado es Current-State.md,
# corre check_vault.py y devuelve el semáforo de arranque + si el archivo
# quedó sobre su techo blando como contexto adicional del mismo turno — así
# la compresión deja de ser una revisión reactiva al cierre de sesión.
#
# v4 (2026-09-11): el script vive en `scripts/check_vault.py` (herramienta
# única del repo, ya no una copia por eje) y descubre los ejes solo. El hook
# le pasa `--eje` deducido de la ruta editada, para no reportar los tres
# vaults cuando solo se tocó uno.
#
# Usa Python para el JSON (no jq: no está instalado en este Git Bash).
# Se asume cwd = raíz del repo (así corre siempre en esta sesión).
export PYTHONIOENCODING=utf-8
file="$(python -c '
import json, sys
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
f = (d.get("tool_input") or {}).get("file_path") or (d.get("tool_response") or {}).get("filePath") or ""
print(f)
')"

case "$file" in
  *Current-State.md)
    # Primer componente de la ruta relativa al repo = nombre del eje.
    eje="$(python -c '
import os, sys
ruta = sys.argv[1]
try:
    rel = os.path.relpath(ruta, os.getcwd())
except ValueError:
    rel = ruta
partes = rel.replace("\\", "/").split("/")
print(partes[0] if partes and partes[0] not in ("", ".", "..") else "")
' "$file")"

    if [ -n "$eje" ]; then
      out="$(python scripts/check_vault.py --eje "$eje" 2>&1 | grep -E "ARRANQUE|Current-State\.md|\[AVISO\]|\[ERROR\]" || true)"
    else
      out="$(python scripts/check_vault.py 2>&1 | grep -E "ARRANQUE|Current-State\.md|\[AVISO\]|\[ERROR\]" || true)"
    fi

    if [ -n "$out" ]; then
      python -c '
import json, sys
print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": sys.stdin.read()}}))
' <<< "$out"
    fi
    ;;
esac
exit 0
