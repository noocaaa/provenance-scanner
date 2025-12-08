Set-ExecutionPolicy Bypass -Scope Process -Force

# Install Python if missing
if (-not (Get-Command python.exe -ErrorAction SilentlyContinue)) {
    Write-Output "Python not found, please install manually or add automatic installer."
}

New-Item -ItemType Directory -Path "C:\scanner" -Force
Copy-Item -Path "C:\vagrant\scanner\*" -Destination "C:\scanner" -Recurse -Force

pip install -r C:\scanner\requirements.txt
