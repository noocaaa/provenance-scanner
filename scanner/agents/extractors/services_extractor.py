"""
File: services_extractor.py
Author: Noelia Carrasco Vilar
Date: 2025-12-13
Description:
    Extract Services related data.
"""

import psutil

def extract(agent=None):
    return {
        "processes_preview": [
            {
                "pid": p.pid,
                "name": p.name(),
                "username": p.username(),
            }
            for p in psutil.process_iter(attrs=["pid", "name", "username"])
        ][:300],
        "listening_ports_preview": [
            {
                "port": c.laddr.port,
                "ip": c.laddr.ip,
                "status": c.status,
            }
            for c in psutil.net_connections(kind="inet")
            if c.laddr
        ][:200],
    }
