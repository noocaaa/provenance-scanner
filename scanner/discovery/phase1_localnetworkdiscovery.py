"""
File: phase1_localnetworkdiscovery.py
Author: Noelia Carrasco Vilar
Date: 2025-12-08
Description:
    Map immediate surroundings.
"""

import platform
import ipaddress
from concurrent.futures import ThreadPoolExecutor
from scanner.discovery.utils import extract_regex, run

# ---------------------------
# PHASE 1: LOCAL NETWORK DISCOVERY
# ---------------------------

def calculate_subnet(ip, mask):
    try:
        net = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
        return net
    except:
        return None

def ping_host(ip):
    ping_cmd = f"ping -n 1 -w 300 {ip}" if platform.system() == "Windows" else f"ping -c 1 -W 1 {ip}"
    output = run(ping_cmd)
    if "TTL=" in output or "ttl=" in output:
        return ip
    return None

def arp_scan():
    return run("arp -a" if platform.system() == "Windows" else "arp -n")

def reverse_dns(ip):
    out = run(f"nslookup {ip}")
    m = extract_regex(r"name = ([^\s]+)\.", out)
    return m if m else None

def phase1_network_discovery(ip, mask, gateway):
    print("\n=== PHASE 1: LOCAL NETWORK DISCOVERY ===\n")

    subnet = calculate_subnet(ip, mask)
    if not subnet:
        print("Could not calculate subnet automatically.")
        return

    print(f"[*] Scanning subnet: {subnet}")

    alive_hosts = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(ping_host, [str(host) for host in subnet.hosts()])
        alive_hosts = [r for r in results if r]

    print("\n[+] Alive hosts found:")
    for h in alive_hosts:
        print(" -", h)

    print("\n[+] ARP Scan Results:")
    print(arp_scan())

    print("\n[+] Common Key Infrastructure (guesses):")
    def mark(ip_addr):
        return "[FOUND]" if ip_addr in alive_hosts else "[?]"

    net = list(subnet.hosts())
    common = {
        "Gateway (.1)": str(net[0]),
        "Likely Server (.10)": f"{subnet.network_address + 10}",
        "Likely Printer (.100)": f"{subnet.network_address + 100}",
        "Likely Switch (.254)": f"{subnet.network_address + 254}",
    }

    for name, ip_addr in common.items():
        print(f"{name}: {ip_addr} {mark(ip_addr)}")

    print("\n[+] Reverse DNS for alive hosts:")
    for h in alive_hosts:
        host = reverse_dns(h)
        if host:
            print(f"{h} -> {host}")

    print("\nFinished PHASE 1.")
