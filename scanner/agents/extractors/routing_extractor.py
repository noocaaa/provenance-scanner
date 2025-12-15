"""
File: routing_extractor.py
Author: Noelia Carrasco Vilar
Date: 2025-12-14
Description:
    Extract routing, forwarding and NAT construction data.
"""

import platform
import subprocess

def _cmd(cmd):
    try:
        return subprocess.check_output(
            cmd, stderr=subprocess.DEVNULL, text=True
        ).strip()
    except Exception:
        return None


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
            data["nat"]["enabled"] = True
            data["nat"]["rules"] = nat.splitlines()

    # ----------------------------
    # Windows
    # ----------------------------
    elif system == "Windows":
        routes = _cmd(["route", "print"])
        if routes:
            data["routing_table"] = routes.splitlines()
            data["default_routes"] = [
                l for l in routes.splitlines() if "0.0.0.0" in l
            ]

    return data