#!/usr/bin/env bash
set -e

AGENT_NAME="provenance_agent"
OUT_DIR="build/macos"

python3 -m venv .venv_build
source .venv_build/bin/activate

pip install --upgrade pip
python -m pip install `
    --index-url https://mirrors.aliyun.com/pypi/simple/ `
    --trusted-host mirrors.aliyun.com `
    pyinstaller pyyaml
cd scanner/agents/remote_runner/

pyinstaller \
  --onefile \
  --clean \
  --name "$AGENT_NAME" \
  run.py

mkdir -p ../$OUT_DIR
mv dist/$AGENT_NAME ../$OUT_DIR/

deactivate
