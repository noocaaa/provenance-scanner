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

# Optional: install Python
winget install --id Python.Python.3.11 -e --silent
