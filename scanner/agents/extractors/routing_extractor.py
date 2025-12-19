"""
File: routing_extractor.py
Author: Noelia Carrasco Vilar
Date: 2025-12-14
Description:
    Extract routing, forwarding and NAT construction data.
"""

import platform
import subprocess
import re

def windows_ip_forwarding():
    out = _cmd(["powershell", "-Command", "Get-NetIPInterface | Select InterfaceAlias, Forwarding"])
    if not out:
        return None

    for line in out.splitlines():
        if "Enabled" in line:
            return True

    return False

def _cmd(cmd):
    try:
        return subprocess.check_output(
            cmd, stderr=subprocess.DEVNULL, text=True
        ).strip()
    except Exception:
        return None

def windows_nat_status():
    # Check WinNAT
    nat = _cmd(["powershell", "-Command", "Get-NetNat"])
    if nat:
        return {
            "enabled": True,
            "rules": nat.splitlines()
        }

    # Check Internet Connection Sharing
    ics = _cmd([
        "powershell",
        "-Command",
        "Get-Service SharedAccess -ErrorAction SilentlyContinue"
    ])
    if ics and "Running" in ics:
        return {
            "enabled": True,
            "rules": ["Internet Connection Sharing enabled"]
        }

    return {
        "enabled": False,
        "rules": []
    }

def extract(agent=None):
    data = {
        "ip_forwarding": None,
        "default_routes": [],
        "routing_table": [],
        "nat": {
            "enabled": False,
            "rules": []
        }
    }

    system = platform.system()

    # ----------------------------
    # Linux
    # ----------------------------
    if system == "Linux":
        # IP forwarding
        fwd = _cmd(["sysctl", "-n", "net.ipv4.ip_forward"])
        if fwd is not None:
            data["ip_forwarding"] = (fwd == "1")

        # Default routes
        routes = _cmd(["ip", "route"])
        if routes:
            for line in routes.splitlines():
                data["routing_table"].append(line)
                if line.startswith("default"):
                    data["default_routes"].append(line)

        # NAT rules (best effort)
        nat = _cmd(["iptables", "-t", "nat", "-L", "-n"])
        if nat:
            data["nat"]["enabled"] = "unknown"
            data["nat"]["rules"] = nat.splitlines()

    # ----------------------------
    # Windows
    # ----------------------------
    elif system == "Windows":
        data["ip_forwarding"] = windows_ip_forwarding()

        routes = _cmd(["route", "print"])
        if routes:
            lines = routes.splitlines()
            data["routing_table"] = lines
            data["default_routes"] = [
                l for l in lines if re.search(r"^\s*0\.0\.0\.0\s+0\.0\.0\.0", l)
            ]

        data["nat"] = windows_nat_status()

    return data