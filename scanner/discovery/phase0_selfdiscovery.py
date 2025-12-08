"""
File: phase0_selfdiscovery.py
Author: Noelia Carrasco Vilar
Date: 2025-12-08
Description:
    Understand the current environment. Fixed for Windows.
"""

import socket
import psutil
import platform
import subprocess
import re

def get_hostname():
    return socket.gethostname()

def get_domain():
    fqdn = socket.getfqdn()
    hostname = socket.gethostname()
    domain = fqdn.replace(hostname, "").strip(".")

    return domain if domain else "No domain"

def get_network_info():
    info = {
        "ip": "",
        "netmask": "",
        "gateway": "",
        "dns": []
    }

    # ---------------------
    # 1. IP + Netmask
    # ---------------------
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET and not addr.address.startswith("127."):
                info["ip"] = addr.address
                info["netmask"] = addr.netmask

    # ---------------------
    # 2. GATEWAY (FAST + UNIVERSAL)
    # ---------------------
    system = platform.system()

    if system == "Windows":
        try:
            out = subprocess.check_output("ipconfig", shell=True).decode(errors="ignore")
            match = re.search(r"Default Gateway[ .:]+([\d.]+)", out)
            if match:
                info["gateway"] = match.group(1)
        except:
            pass

    else:  
        # Linux + macOS: parse /proc/net/route
        try:
            with open("/proc/net/route") as f:
                for line in f:
                    fields = line.strip().split()
                    if fields[1] != '00000000':
                        continue
                    gw_hex = fields[2]
                    gw_str = socket.inet_ntoa(bytes.fromhex(gw_hex)[::-1])
                    info["gateway"] = gw_str
                    break
        except:
            pass

    # ---------------------
    # 3. DNS (FAST)
    # ---------------------
    if system == "Windows":
        try:
            out = subprocess.check_output("ipconfig /all", shell=True).decode(errors="ignore")
            capture = False
            for line in out.splitlines():
                if "DNS Servers" in line:
                    capture = True
                    ip = line.split(":")[-1].strip()
                    info["dns"].append(ip)
                elif capture:
                    m = re.match(r"\s*([\d.]+)", line)
                    if m:
                        info["dns"].append(m.group(1))
                    else:
                        break
        except:
            pass

    else:
        # Linux/MacOS: resolv.conf
        try:
            with open("/etc/resolv.conf") as f:
                for line in f:
                    if line.startswith("nameserver"):
                        info["dns"].append(line.split()[1])
        except:
            pass

    return info


def get_active_connections():
    conns = psutil.net_connections()
    results = []
    for c in conns:
        laddr = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else ""
        raddr = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else ""
        status = c.status
        results.append((laddr, raddr, status))
    return results

def get_arp_cache():
    try:
        if platform.system() == "Windows":
            out = subprocess.check_output("arp -a", shell=True).decode()
        else:
            out = subprocess.check_output("arp -n", shell=True).decode()
        return out.strip()
    except:
        return ""

def run_phase0():
    """Run Phase 0 discovery and return structured data."""
    
    print("\n=== PHASE 0: SELF DISCOVERY ===\n")
    
    # Collect data
    hostname = get_hostname()
    print(f"Hostname: {hostname}")
    
    domain = get_domain()
    print(f"Domain: {domain}\n")
    
    net = get_network_info()
    print(f"IP Address: {net['ip']}")
    print(f"Subnet Mask: {net['netmask']}")
    print(f"Default Gateway: {net['gateway']}")
    print(f"DNS Servers: {net['dns']}\n")
    
    conns = get_active_connections()
    print("[+] Active Connections")
    for c in conns[:10]:  # show only first 10
        print(f"  {c}")
    
    arp = get_arp_cache()
    print("\n[+] ARP Cache")
    print(arp)
    
    # Return all collected data as a dictionary
    return {
        "hostname": hostname,
        "domain": domain,
        "ip": net['ip'],
        "netmask": net['netmask'],
        "gateway": net['gateway'],
        "dns": net['dns'],
        "active_connections": conns[:10],
        "arp_cache": arp
    }