$ErrorActionPreference = "Stop"

$AGENT_NAME = "provenance_agent"
$ROOT = Get-Location
$OUT_DIR = "$ROOT\build\windows"
$VENV = "$ROOT\.venv_build"

Write-Host "[*] Building Windows agent"
Write-Host "    Root: $ROOT"

Remove-Item Env:HTTP_PROXY -ErrorAction SilentlyContinue
Remove-Item Env:HTTPS_PROXY -ErrorAction SilentlyContinue
Remove-Item Env:http_proxy -ErrorAction SilentlyContinue
Remove-Item Env:https_proxy -ErrorAction SilentlyContinue

if (Test-Path $VENV) {
    Remove-Item -Recurse -Force $VENV
}
python -m venv $VENV
. "$VENV\Scripts\Activate.ps1"

python -m pip install --upgrade pip setuptools wheel
python -m pip install pyinstaller pyyaml psutil

python -m PyInstaller `
  --onefile `
  --clean `
  --name $AGENT_NAME `
  --collect-submodules scanner `
  --collect-all psutil `
  scanner/agents/remote_runner/run.py

New-Item -ItemType Directory -Force -Path $OUT_DIR | Out-Null
Move-Item "dist\$AGENT_NAME.exe" "$OUT_DIR\" -Force

Remove-Item -Recurse -Force dist, *.spec -ErrorAction SilentlyContinue
deactivate

Write-Host "[X] Built: build/windows/$AGENT_NAME.exe"
