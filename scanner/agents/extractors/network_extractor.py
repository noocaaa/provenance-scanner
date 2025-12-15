"""
File: network_extractor.py
Author: Noelia Carrasco Vilar
Date: 2025-12-13
Description:
    Extract Network related data.
"""

import psutil
import socket

def extract(agent=None):
    interfaces = {}

    for iface, addrs in psutil.net_if_addrs().items():
        iface_data = {"ipv4": [], "ipv6": [], "mac": None}

        for addr in addrs:
            if addr.family == socket.AF_INET:
                iface_data["ipv4"].append({
                    "ip": addr.address,
                    "netmask": addr.netmask
                })
            elif addr.family == socket.AF_INET6:
                iface_data["ipv6"].append(addr.address)
            elif addr.family == psutil.AF_LINK:
                iface_data["mac"] = addr.address

        interfaces[iface] = iface_data

    return {
        "interfaces": interfaces,
        "connections_preview": [
            {
                "laddr": {
                    "ip": c.laddr.ip,
                    "port": c.laddr.port,
                } if c.laddr else None,
                "raddr": {
                    "ip": c.raddr.ip,
                    "port": c.raddr.port,
                } if c.raddr else None,
                "status": c.status,
                "pid": c.pid,
            }
            for c in psutil.net_connections(kind="inet")[:200]
        ],
    }
