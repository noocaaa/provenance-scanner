#!/usr/bin/env bash
set -e

AGENT_NAME="provenance_agent"
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="$ROOT_DIR/build/linux"

echo "[*] Building Linux agent"
echo "    Root: $ROOT_DIR"

# -------------------------
# System deps FIRST (no venv yet)
# -------------------------
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv

# -------------------------
# Virtualenv
# -------------------------
python3 -m venv "$ROOT_DIR/.venv_build"
source "$ROOT_DIR/.venv_build/bin/activate"

pip install --upgrade pip
pip install pyinstaller pyyaml psutil

# -------------------------
# Build (from repo root)
# -------------------------
cd "$ROOT_DIR"

pyinstaller \
  --onefile \
  --clean \
  --name "$AGENT_NAME" \
  --hidden-import=runner \
  --hidden-import=extractors \
  scanner/agents/remote_runner/run.py

# -------------------------
# Output
# -------------------------
mkdir -p "$OUT_DIR"
mv "$ROOT_DIR/dist/$AGENT_NAME" "$OUT_DIR/"

# -------------------------
# Cleanup (DO NOT DELETE build/)
# -------------------------
rm -rf "$ROOT_DIR/dist" "$ROOT_DIR/$AGENT_NAME.spec"

deactivate

echo "Linux agent built at: $OUT_DIR/$AGENT_NAME"
