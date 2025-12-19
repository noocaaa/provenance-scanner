Write-Host "Configuring SSH authorized_keys for vagrant user"

$sshDir = "C:\Users\vagrant\.ssh"
$authKeys = "$sshDir\authorized_keys"
$pubKeyPath = "C:\vagrant\cluster_key.pub"

New-Item -ItemType Directory -Force -Path $sshDir | Out-Null

if (-not (Test-Path $authKeys)) {
    New-Item -ItemType File -Path $authKeys | Out-Null
}

$pubKey = Get-Content $pubKeyPath
if (-not (Select-String -Path $authKeys -Pattern [regex]::Escape($pubKey) -Quiet)) {
    Add-Content -Path $authKeys -Value $pubKey
}

icacls $sshDir /inheritance:r
icacls $sshDir /grant "vagrant:(OI)(CI)F"
icacls $authKeys /inheritance:r
icacls $authKeys /grant "vagrant:F"

Write-Host "SSH key installed successfully"
