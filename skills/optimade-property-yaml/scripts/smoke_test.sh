#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/../../.." && pwd)
PYTHON=${PYTHON:-python3}
VENV="$REPO_ROOT/.venv"

if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "ERROR: python3 was not found" >&2
  exit 1
fi

if [ ! -d "$REPO_ROOT/external/OPTIMADE/.git" ] && [ ! -f "$REPO_ROOT/external/OPTIMADE/.git" ]; then
  echo "WARN: external/OPTIMADE is absent or not initialized" >&2
fi
if [ ! -d "$REPO_ROOT/external/optimade-property-tools/.git" ] && [ ! -f "$REPO_ROOT/external/optimade-property-tools/.git" ]; then
  echo "WARN: external/optimade-property-tools is absent or not initialized" >&2
fi

if [ ! -d "$VENV" ]; then
  "$PYTHON" -m venv "$VENV"
fi
"$VENV/bin/python" -m pip install --quiet PyYAML
"$VENV/bin/python" "$SCRIPT_DIR/validate_yaml.py" "$REPO_ROOT/skills/optimade-property-yaml/assets/starter-property.yaml"
"$VENV/bin/python" "$SCRIPT_DIR/select_examples.py" "magnetic moment"
echo "Smoke test passed"
