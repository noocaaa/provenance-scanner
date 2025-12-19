"""
File: phase1_localnetworkdiscovery.py
Author: Noelia Carrasco Vilar
Date: 2025-12-09
Description:
    Phase 1 - Fast Local Network Discovery.  L2/L3 reachability.
"""

import ipaddress
import platform
import subprocess
import socket
import netifaces
import re
from concurrent.futures import ThreadPoolExecutor

DISCOVERY_PORTS = {
    "printer": [9100, 515, 631],
    "server":  [22, 80, 443, 445, 3306, 5432, 3389, 5985, 5986],
    "switch":  [23, 161]
}

COMMON_TCP_PORTS = [22, 80, 443, 3389, 5985, 5986]
COMMON_UDP_PORTS = [53, 67, 161, 123]

# ------- Helpers -------
def calculate_subnet_range(ip: str, netmask: str) -> ipaddress.IPv4Network:
    return ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)

def scan_open_ports(ip, ports=None, timeout=0.2):
    ports = ports or DISCOVERY_PORTS["server"] + DISCOVERY_PORTS["printer"] + DISCOVERY_PORTS["switch"]
    open_p = []
    for p in ports:
        if tcp_probe(ip, p, timeout):
            open_p.append(p)
    return open_p


def is_valid_host(ip_str: str, network: ipaddress.IPv4Network) -> bool:
    try:
        ip = ipaddress.IPv4Address(ip_str)
    except Exception:
        return False

    if ip.is_multicast or ip.is_unspecified or ip.is_loopback:
        return False
    if ip == network.network_address or ip == network.broadcast_address:
        return False

    return ip in network

# ------- ARP SCAN -------
def arp_scan_local(network: ipaddress.IPv4Network):
    """Read ARP cache and return entries that belong to subnet."""
    try:
        system = platform.system()
        cmd = "arp -a" if system == "Windows" else "arp -n"
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode(errors="ignore")
    except Exception:
        return []

    hosts = []
    for line in out.splitlines():
        parts = line.strip().split()
        if not parts:
            continue
        candidate = parts[0]
        if candidate.count('.') != 3:
            continue
        if is_valid_host(candidate, network):
            hosts.append(candidate)
    return hosts

# ------- TCP SYN Discovery -------
def tcp_probe(ip: str, port: int, timeout=0.15) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex((ip, port)) == 0
    except Exception:
        return False


def tcp_discovery(network: ipaddress.IPv4Network, ports=None, workers=60, max_hosts=1024):
    ports = ports or COMMON_TCP_PORTS

    all_hosts = list(network.hosts())
    if len(all_hosts) > max_hosts:
        ips_to_scan = [str(ip) for ip in all_hosts[:max_hosts]]
    else:
        ips_to_scan = [str(ip) for ip in all_hosts]

    def scan_one(ip_str):
        for p in ports:
            if tcp_probe(ip_str, p):
                return ip_str
        return None

    found = set()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(scan_one, ip): ip for ip in ips_to_scan}
        for fut in futures:
            try:
                result = fut.result(timeout=0.4)
                if result and is_valid_host(result, network):
                    found.add(result)
            except Exception:
                continue

    return sorted(found)

# ------- ICMP fallback -------
def icmp_ping(ip: str) -> str | None:
    system = platform.system()
    cmd = f"ping -n 1 -w 300 {ip}" if system == "Windows" else f"ping -c 1 -W 1 {ip}"
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode(errors="ignore")
        if "TTL=" in out or "ttl=" in out:
            return ip
    except Exception:
        return None
    return None


def icmp_sweep_parallel(network: ipaddress.IPv4Network, workers=80, max_hosts=1024):
    all_hosts = list(network.hosts())
    if len(all_hosts) > max_hosts:
        ips = [str(ip) for ip in all_hosts[:max_hosts]]
    else:
        ips = [str(ip) for ip in all_hosts]

    found = set()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for result in ex.map(icmp_ping, ips):
            if result and is_valid_host(result, network):
                found.add(result)

    return sorted(found)

# ------- UDP Reachability (LIGHTWEIGHT) -------
def udp_probe(ip: str, port: int, timeout=0.2) -> bool:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(timeout)
        s.sendto(b"", (ip, port))
        try:
            s.recvfrom(1024)
            return True   # service responded
        except socket.timeout:
            return False
    except Exception:
        return False

# ------- OS Fingerprinting (TTL-based) -------
def guess_os(ip: str) -> str:
    try:
        system = platform.system()
        cmd = f"ping -c 1 -W 1 {ip}" if system != "Windows" else f"ping -n 1 -w 300 {ip}"
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode(errors="ignore")

        m = re.search(r"ttl[=:](\d+)", out, re.I)
        if not m:
            return "unknown"

        ttl = int(m.group(1))
        if ttl <= 70:
            return "linux_like"
        if ttl <= 130:
            return "windows_like"
        if ttl > 200:
            return "network_device_like"
    except:
        pass

    return "unknown"

def classify_host(ip, tcp_ports, udp_ports, os_guess):
    default_gw = netifaces.gateways().get('default', {}).get(netifaces.AF_INET, [None])[0]

    if ip == default_gw:
        return "gateway"

    if os_guess == "network_device_like":
        return "network_device"

    if 9100 in tcp_ports or 631 in tcp_ports:
        return "printer"

    if 80 in tcp_ports or 443 in tcp_ports:
        return "web_service"

    if 22 in tcp_ports:
        return "ssh_service"

    if 53 in udp_ports:
        return "dns_like"

    return "unknown"

def run_phase1(
    ip: str,
    netmask: str,
    methods=None,
    skip_arp=False,
    tcp_ports=None,
    workers=60,
    fallback_icmp=False
):
    print("\n=== PHASE 1: Local Network Discovery ===\n")

    network = calculate_subnet_range(ip, netmask)
    print(f"[*] Subnet calculated: {network}\n")

    if ip.startswith("169.254."):
        print("[!] Warning: APIPA (169.254.x.x). Discovery will be limited.\n")

    methods = methods or ["tcp"]
    discovered = set()

    # 1) ARP
    if "arp" in methods and not skip_arp:
        print("[+] ARP scan...")
        arp_ips = arp_scan_local(network)
        print(f"    ARP: {arp_ips}")
        discovered.update(arp_ips)

    # 2) TCP SYN
    if "tcp" in methods:
        print("[+] TCP discovery...")
        tcp_hosts = tcp_discovery(network, ports=tcp_ports, workers=workers)
        print(f"    TCP responders: {tcp_hosts}")
        discovered.update(tcp_hosts)

    # 3) ICMP fallback
    if fallback_icmp:
        print("[+] ICMP sweep...")
        icmp_hosts = icmp_sweep_parallel(network, workers=workers)
        print(f"    ICMP responders: {icmp_hosts}")
        discovered.update(icmp_hosts)

    validated = sorted([h for h in discovered if is_valid_host(h, network)])

    # Classification
    discovered_devices = {}
    print("\n[+] Classifying discovered hosts...")

    for host in validated:
        tcp_open = scan_open_ports(host := host)
        os_guess = guess_os(host)

        udp_open = []
        for p in COMMON_UDP_PORTS:
            if udp_probe(host, p):
                udp_open.append({
                    "port": p,
                    "evidence": "packet_response",
                    "confidence": "very_low"
                })

        discovered_devices[host] = {
            "tcp": tcp_open,
            "udp": udp_open,
            "os_hint": os_guess,
            "type": classify_host(host, tcp_open, udp_open, os_guess)
        }

        print(f"    {host} → TCP:{tcp_open} UDP:{udp_open} OS:{os_guess} TYPE:{discovered_devices[host]['type']}")

    print("\n[+] Phase 1 complete.\n")
    return {
        "network": str(network),
        "discovered_hosts": validated,
        "details": discovered_devices,
        "methods": methods,
        "scanner_ip": ip,
        "scanner_role": "active_discovery_node",
    }