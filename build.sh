#!/usr/bin/env bash
set -euo pipefail

# build.sh - Crear/usar venv, (re)instalar dependencias y ejecutar PyInstaller
# Usage: ./build.sh [--recreate-venv] [--python PYTHON_BIN]

RECREATE_VENV=false
PYBIN=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --recreate-venv|-r)
      RECREATE_VENV=true
      shift
      ;;
    --python)
      PYBIN="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: $0 [--recreate-venv] [--python PYTHON_BIN]"
      exit 0
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

# Prefer python3.12 if available
if [[ -z "$PYBIN" ]]; then
  if command -v python3.12 >/dev/null 2>&1; then
    PYBIN=python3.12
  elif command -v python3 >/dev/null 2>&1; then
    PYBIN=python3
  else
    PYBIN=python
  fi
fi

VENV_DIR=".venv"
PY_VENV="$VENV_DIR/bin/python"
PIP_VENV="$VENV_DIR/bin/pip"
PYI_VENV="$VENV_DIR/bin/pyinstaller"

echo "[build] Using Python: $PYBIN"
echo "[build] Venv dir: $VENV_DIR"

if [[ "$RECREATE_VENV" == "true" ]]; then
  echo "[build] Removing existing venv..."
  rm -rf "$VENV_DIR"
fi

if [[ ! -d "$VENV_DIR" ]]; then
  echo "[build] Creating virtual environment with $PYBIN..."
  $PYBIN -m venv "$VENV_DIR"
fi

echo "[build] venv python: $($PY_VENV --version 2>&1 | head -n1)"

echo "[build] Ensuring pip/setuptools/wheel are up-to-date..."
"$PIP_VENV" install --upgrade pip setuptools wheel

# Determine whether to install requirements
NEED_INSTALL=false
if ! "$PY_VENV" -c "import numpy" >/dev/null 2>&1; then
  NEED_INSTALL=true
fi
if [[ ! -x "$PYI_VENV" ]]; then
  NEED_INSTALL=true
fi

if [[ "$NEED_INSTALL" = true ]]; then
  echo "[build] Installing requirements into venv (this may take a while)..."
  "$PIP_VENV" install --no-cache-dir -r requirements.txt
  "$PIP_VENV" install --no-cache-dir pyinstaller==6.20.0
else
  echo "[build] Dependencies and PyInstaller already present in venv; skipping install."
fi

echo "[build] Running PyInstaller..."
"$PYI_VENV" --clean bpm-calculator.spec

echo "[build] Build finished: dist/bpm-calculator"
exit 0
