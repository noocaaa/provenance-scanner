"""
File: network_extractor.py
Author: Noelia Carrasco Vilar
Date: 2025-12-13
Description:
    Extract Network related data.
"""

import socket
import platform
import subprocess

_exec_cache = {}

# ----- HELPERS -----

def is_windows():
    return platform.system().lower() == "windows"

def is_private_ip(ip):
    return (
        ip.startswith("10.") or
        ip.startswith("192.168.") or
        ip.startswith("172.")
    )

def infer_direction(state, raddr):
    s = str(state).strip().lower() if state is not None else ""
    if s in ("listen", "listening"):
        return "listening"
    if raddr and raddr not in ("0.0.0.0", "::", "*"):
        return "outbound"
    return "unknown"


def enrich_process(pid):
    import psutil

    if not pid:
        return None
    try:
        p = psutil.Process(pid)
        return {
            "pid": pid,
            "name": p.name(),
            "exe": p.exe() if p.exe() else None, # fallback only
            "username": p.username(),
        }
    except Exception:
        return {"pid": pid}


# ----- WINDOWS -----

def windows_tcp_connections():
    ps = """
    Get-NetTCPConnection |
      Select LocalAddress, LocalPort, RemoteAddress, RemotePort, State, OwningProcess |
      ConvertTo-Json
    """

    try:
        out = subprocess.check_output(
            ["powershell", "-Command", ps],
            stderr=subprocess.DEVNULL,
            text=True
        )
        import json
        data = json.loads(out)
        if isinstance(data, dict):
            data = [data]
        return data
    except Exception:
        return []

def normalize_laddr(ip, port):
    if ip in ("0.0.0.0", "::"):
        return {
            "bind": "all_interfaces",
            "port": port,
            "exposure": "public",
            "network_scope": "external"
        }

    if ip.startswith("127.") or ip == "::1":
        return {
            "bind": "loopback",
            "port": port,
            "exposure": "local",
            "network_scope": "local"
        }

    return {
        "ip": ip,
        "port": port,
        "exposure": "internal",
        "network_scope": "internal"
    }

def windows_executable_path(pid: int):
    if not pid:
        return None

    ps = f"""
    try {{
      (Get-CimInstance Win32_Process -Filter "ProcessId={pid}").ExecutablePath
    }} catch {{
      $null
    }}
    """

    try:
        out = subprocess.check_output(
            ["powershell", "-Command", ps],
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()

        if pid in _exec_cache:
            return _exec_cache[pid]

        _exec_cache[pid] = out or None
        return _exec_cache[pid]

    except Exception:
        return None

def extract(agent=None, max_connections=50):
    import psutil

    interfaces = {}
    connections = []
    listening = {}

    # ---------------- INTERFACES ----------------
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

    # ---------------- LINUX ----------------
    if not is_windows():
        for c in psutil.net_connections(kind="inet"):
            if not c.laddr:
                continue

            direction = infer_direction(c.status, c.raddr.ip if c.raddr else None)

            entry = {
                "laddr": {
                    "ip": c.laddr.ip,
                    "port": c.laddr.port
                },
                "raddr": (
                    {"ip": c.raddr.ip, "port": c.raddr.port}
                    if c.raddr else None
                ),
                "protocol": "tcp",
                "status": c.status,
                "pid": c.pid,
                "process": enrich_process(c.pid),
                "direction": direction,
                "confidence": "high" if c.pid else "medium",
                "source": "psutil"
            }

            entry["nat_suspected"] = (
                    entry["direction"] == "outbound"
                    and entry["laddr"].get("ip")
                    and entry["raddr"]
                    and is_private_ip(entry["laddr"]["ip"])
                    and not is_private_ip(entry["raddr"]["ip"])
            )

            if direction == "listening":
                entry["laddr"] = normalize_laddr(c.laddr.ip, c.laddr.port)
                listening[(c.laddr.ip, c.laddr.port)] = entry
            else:
                connections.append(entry)

    # ---------------- WINDOWS ----------------
    else:
        for c in windows_tcp_connections():
            pid = c.get("OwningProcess")
            laddr = c.get("LocalAddress")
            lport = c.get("LocalPort")
            raddr = c.get("RemoteAddress")
            rport = c.get("RemotePort")

            direction = infer_direction(c.get("State"), raddr)

            entry = {
                "laddr": {
                    "ip": laddr,
                    "port": lport
                },
                "raddr": (
                    {"ip": raddr, "port": rport}
                    if raddr and raddr != "0.0.0.0" else None
                ),
                "protocol": "tcp",
                "status": c.get("State"),
                "pid": pid,
                "process": enrich_process(pid),
                "direction": direction,
                "confidence": "high" if pid else "low",
                "source": "powershell"
            }

            proc = enrich_process(pid)
            if proc:
                proc["executable_path"] = windows_executable_path(pid)

            entry["process"] = proc

            entry["nat_suspected"] = (
                    entry["direction"] == "outbound"
                    and entry["laddr"].get("ip")
                    and entry["raddr"]
                    and is_private_ip(entry["laddr"]["ip"])
                    and not is_private_ip(entry["raddr"]["ip"])
            )

            if direction == "listening":
                listening[(c.laddr.ip, c.laddr.port)] = entry
                entry["laddr"] = normalize_laddr(laddr, lport)
            else:
                connections.append(entry)

    return {
        "interfaces": interfaces,
        "listening_ports_preview": list(listening.values()),
        "connections_preview": connections[:max_connections]
    }