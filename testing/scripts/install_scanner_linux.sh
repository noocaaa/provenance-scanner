#!/bin/bash
apt update -y
apt install -y python3 python3-pip nmap iputils-ping net-tools
pip3 install psutil
echo "[OK] Scanner installed on $(hostname)"
