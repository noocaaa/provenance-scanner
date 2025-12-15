$ErrorActionPreference = "Stop"

$AGENT_NAME = "provenance_agent"
$ROOT = Get-Location
$AGENT_DIR = "$ROOT\scanner\agents\remote_runner"
$OUT_DIR = "$ROOT\build\windows"

# ---------- Cleanup Environment ----------
$env:HTTP_PROXY=""
$env:HTTPS_PROXY=""
$env:http_proxy=""
$env:https_proxy=""

# ---------- Build env ----------
python -m venv .venv_build
. .venv_build\Scripts\Activate.ps1

python -m pip install `
    -i https://mirrors.aliyun.com/pypi/simple/ `
    --trusted-host mirrors.aliyun.com `
    pyinstaller pyyaml

# ---------- Build ----------
Set-Location $AGENT_DIR

python -m PyInstaller `
  --onefile `
  --clean `
  --name $AGENT_NAME `
  --distpath "$OUT_DIR" `
  --workpath "$ROOT\.tmp_build" `
  --specpath "$ROOT\.tmp_build" `
  run.py

# ---------- Cleanup ----------
deactivate
Set-Location $ROOT

Remove-Item -Recurse -Force .tmp_build

Write-Host "Built: build/windows/$AGENT_NAME.exe"
