"""
File: phase0_selfdiscovery.py
Author: Noelia Carrasco Vilar
Date: 2025-12-08
Description:
    Phase 0: Understand the current local environment.
    Clean, robust, cross-platform implementation + mejoras.
"""

import socket
import psutil
import platform
import subprocess
import re
from typing import List, Dict, Optional


# ============================================================================
# MEJORA 2: Detectar interfaz primaria usando default route
# ============================================================================
def get_primary_interface() -> Optional[str]:
    try:
        system = platform.system()

        if system == "Linux":
            out = subprocess.check_output(
                ["ip", "route"],
                stderr=subprocess.DEVNULL
            ).decode()
            for line in out.splitlines():
                if line.startswith("default"):
                    return line.split()[4]

        elif system == "Darwin":  # macOS
            out = subprocess.check_output(
                ["route", "-n", "get", "default"],
                stderr=subprocess.DEVNULL
            ).decode()

            for line in out.splitlines():
                if "interface:" in line:
                    return line.split(":")[-1].strip()

        elif system == "Windows":
            out = subprocess.check_output([
                "powershell",
                "-Command",
                "(Get-NetRoute -DestinationPrefix 0.0.0.0/0 | "
                "Sort-Object RouteMetric | Select -First 1).InterfaceAlias"
            ]).decode().strip()

            return out

    except Exception as e:
        print(f"[Phase0:WARN] get_primary_interface failed: {e}")

    return None


# ============================================================================
# MEJORA 1: ARP Parsing cross-platform
# ============================================================================
def parse_arp_cache() -> List[Dict]:
    system = platform.system()
    entries = []

    try:
        if system == "Linux":
            raw = subprocess.check_output(["arp", "-n"]).decode()
            for line in raw.splitlines()[1:]:  # skip header
                parts = line.split()
                if len(parts) >= 5:
                    entries.append({
                        "ip": parts[0],
                        "mac": parts[2],
                        "iface": parts[-1]
                    })

        elif system == "Darwin":  # macOS
            raw = subprocess.check_output(["arp", "-a"]).decode()
            for line in raw.splitlines():
                m = re.search(r"\((.*?)\) at ([0-9a-f:]+)", line)
                if m:
                    entries.append({
                        "ip": m.group(1),
                        "mac": m.group(2),
                        "iface": "unknown"
                    })

        elif system == "Windows":
            raw = subprocess.check_output(
                ["arp", "-a"],
                errors="ignore"
            ).decode("windows-1252")

            for line in raw.splitlines():
                m = re.search(
                    r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-f-]+)\s+(\w+)",
                    line,
                    re.IGNORECASE,
                )
                if m:
                    entries.append({
                        "ip": m.group(1),
                        "mac": m.group(2),
                        "iface": m.group(3)
                    })

    except Exception as e:
        print(f"[Phase0:ERROR] parse_arp_cache failed: {e}")

    return entries


# ============================================================================
# MEJORA 3: Información detallada de interfaces
# ============================================================================
def classify_interface(name: str) -> str:
    name_l = name.lower()

    if "virtual" in name_l or "vbox" in name_l or name_l.startswith("veth"):
        return "Virtual"
    if "wifi" in name_l or "wlan" in name_l:
        return "Wireless"
    if "bridge" in name_l or "br-" in name_l:
        return "Bridge"
    return "Physical"


def get_all_interfaces() -> List[Dict]:
    interfaces = []

    for name, info in psutil.net_if_addrs().items():
        ipv4, mac = None, None

        for addr in info:
            if addr.family == psutil.AF_LINK:
                mac = addr.address
            if addr.family == socket.AF_INET:
                ipv4 = addr.address

        interfaces.append({
            "name": name,
            "ip": ipv4,
            "mac": mac,
            "type": classify_interface(name),
        })

    return interfaces


# ============================================================================
# BASIC SYSTEM INFO
# ============================================================================
def get_hostname():
    return socket.gethostname()


def get_domain():
    fqdn = socket.getfqdn()
    host = socket.gethostname()
    if fqdn == host:
        return "No domain"
    return fqdn.replace(host, "").strip(".")


# ============================================================================
# NETWORK INFO (IP + Mask + Gateway + DNS)
# ============================================================================
def _get_primary_ipv4():
    """First non-loopback IPv4."""
    for interfaces in psutil.net_if_addrs().values():
        for addr in interfaces:
            if addr.family == socket.AF_INET and not addr.address.startswith("127."):
                return addr.address, addr.netmask
    return "", ""


def _get_gateway():
    system = platform.system()

    try:
        if system == "Windows":
            out = subprocess.check_output(
                "ipconfig", shell=True, text=True, errors="ignore")
            m = re.search(r"Default Gateway[ .:]+([\d.]+)", out)
            return m.group(1) if m else ""

        # Linux method
        try:
            with open("/proc/net/route") as f:
                for line in f.readlines()[1:]:
                    fields = line.split()
                    if fields[1] == "00000000":
                        gw_hex = fields[2]
                        return socket.inet_ntoa(bytes.fromhex(gw_hex)[::-1])
        except:
            pass

        # macOS fallback
        out = subprocess.run(
            ["route", "-n", "get", "default"],
            capture_output=True, text=True, errors="ignore"
        )
        m = re.search(r"gateway:\s+([\d.]+)", out.stdout)
        return m.group(1) if m else ""
    except:
        return ""


def _get_dns():
    dns = []
    system = platform.system()

    try:
        if system == "Windows":
            out = subprocess.check_output("ipconfig /all", shell=True, text=True)
            capture = False
            for line in out.splitlines():
                if "DNS Servers" in line:
                    capture = True
                    ip = line.split(":")[-1].strip()
                    if re.match(r"\d+\.\d+\.\d+\.\d+", ip):
                        dns.append(ip)
                elif capture:
                    m = re.match(r"\s*([\d.]+)", line)
                    if m:
                        dns.append(m.group(1))
                    else:
                        break

        else:  # Linux + macOS
            with open("/etc/resolv.conf") as f:
                for line in f:
                    if line.startswith("nameserver"):
                        dns.append(line.split()[1])

    except:
        pass

    return dns


def get_network_info():
    ip, mask = _get_primary_ipv4()
    return {
        "ip": ip,
        "netmask": mask,
        "gateway": _get_gateway(),
        "dns": _get_dns(),
        "primary_interface": get_primary_interface(),
    }


# ============================================================================
# ACTIVE CONNECTIONS
# ============================================================================
def get_active_connections(max_results=10):
    results = []
    for c in psutil.net_connections(kind="inet"):
        l = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else ""
        r = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else ""
        results.append((l, r, c.status))
        if len(results) >= max_results:
            break
    return results


# ============================================================================
# MAIN PHASE 0
# ============================================================================
def run_phase0():
    print("\n=== PHASE 0: SELF DISCOVERY ===\n")

    data = {
        "hostname": get_hostname(),
        "domain": get_domain(),
        "network": get_network_info(),
        "interfaces": get_all_interfaces(),
        "active_connections": get_active_connections(),
        "arp_cache_raw": get_arp_cache(),
        "arp_parsed": parse_arp_cache(),
    }

    return data


# raw ARP for display
def get_arp_cache():
    try:
        cmd = "arp -a" if platform.system() == "Windows" else "arp -n"
        return subprocess.check_output(
            cmd, shell=True, text=True, errors="ignore"
        ).strip()
    except:
        return ""
