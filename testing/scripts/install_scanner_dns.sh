#!/bin/bash
apt update -y
apt install -y bind9 dnsutils python3 python3-pip
pip3 install psutil
echo "[OK] DNS configured"
