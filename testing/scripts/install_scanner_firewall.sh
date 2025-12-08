#!/bin/bash
apt update -y
apt install -y ufw python3 python3-pip
ufw allow 22
ufw enable
pip3 install psutil
echo "[OK] Firewall ready"
