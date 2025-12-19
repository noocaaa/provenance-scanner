# Enable OpenSSH Server
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# Start and enable SSH
Start-Service sshd
Set-Service -Name sshd -StartupType Automatic

# Allow SSH in firewall
New-NetFirewallRule `
  -Name sshd `
  -DisplayName "OpenSSH Server" `
  -Enabled True `
  -Direction Inbound `
  -Protocol TCP `
  -Action Allow `
  -LocalPort 22

Write-Host "Installing Chocolatey..."
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

Write-Host "Installing Python 3.11..."
choco install python --version=3.11.0 -y

# Refresh PATH for current session
$env:Path += ";C:\Python311;C:\Python311\Scripts"

python --version
