#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$SCRIPT_DIR
SKILL_SRC="$REPO_ROOT/skills/optimade-property-yaml"
DEST_DIR="$HOME/.agents/skills"
DEST="$DEST_DIR/optimade-property-yaml"

if [ -d "$REPO_ROOT/.git" ] || git -C "$REPO_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git -C "$REPO_ROOT" submodule update --init --recursive || true
fi

mkdir -p "$DEST_DIR"
if [ -e "$DEST" ] || [ -L "$DEST" ]; then
  if [ -L "$DEST" ]; then
    rm "$DEST"
  else
    echo "ERROR: $DEST exists and is not a symlink; not overwriting" >&2
    exit 1
  fi
fi
ln -s "$SKILL_SRC" "$DEST"
cat <<EOF
Installed Codex skill symlink:
  $DEST -> $SKILL_SRC

Next steps:
  make deps
  make smoke

Codex prompt example:
  Use the optimade-property-yaml skill. Generate one OPTIMADE property-definition source YAML file for band_gap. Output YAML only.
EOF
