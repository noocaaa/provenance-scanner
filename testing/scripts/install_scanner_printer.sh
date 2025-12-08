#!/bin/bash
apt update -y
apt install -y cups python3 python3-pip
pip3 install psutil
echo "[OK] Printer node ready"
