"""
File: interface_selector.py
Author: Noelia Carrasco Vilar
Description:
    Enterprise-grade interface selection for network discovery.
    Decides *which* network interfaces Phase 1 should scan.

    Key logic:
    - Detect whether running inside VM (VirtualBox/VMware/Hyper-V/KVM)
    - Ignore virtual/tunnel interfaces
    - Ignore NAT adapters on host machines
    - Allow NAT adapters *only* inside VMs
    - Ignore public Wi-Fi (unsafe to scan)
    - Identify enterprise/private networks
    - Score interfaces and return sorted list
"""

import psutil
import socket
import ipaddress
import netifaces
import platform
import subprocess

# -------------------------------------------------------------------
# Virtual interface MAC prefixes
# -------------------------------------------------------------------
VIRTUAL_MAC_PREFIXES = [
    "02:42",        # Docker
    "00:15:5d",     # Hyper-V
    "08:00:27",     # VirtualBox
    "00:0c:29", "00:05:69", "00:50:56",  # VMware
]

# -------------------------------------------------------------------
# Names that indicate virtual or tunnel interfaces
# -------------------------------------------------------------------
IGNORED_INTERFACE_PREFIXES = [
    "lo", "loopback",
    "docker", "br-", "veth", "virbr", "vboxnet",
    "vmnet", "tap", "tun", "zt", "tailscale",
]


# ===================================================================
# VM DETECTION
# ===================================================================
def running_inside_vm() -> bool:
    """Detect if this machine is inside a VM."""
    system = platform.system()

    try:
        if system == "Windows":
            out = subprocess.check_output(
                "wmic computersystem get model", shell=True
            ).decode().lower()
            if any(x in out for x in ["virtual", "vmware", "vbox"]):
                return True

        elif system == "Linux":
            # Check DMI product name
            with open("/sys/class/dmi/id/product_name") as f:
                prod = f.read().lower()
                if any(v in prod for v in ["virtualbox", "vmware", "kvm", "qemu"]):
                    return True

            # Check system vendor
            with open("/sys/class/dmi/id/sys_vendor") as f:
                vendor = f.read().lower()
                if any(v in vendor for v in ["innotek", "vmware", "microsoft"]):
                    return True

    except:
        pass

    return False


# ===================================================================
# HELPER CLASSIFIERS
# ===================================================================
def _is_virtual_mac(mac: str) -> bool:
    if not mac:
        return False
    mac = mac.lower()
    return any(mac.startswith(p) for p in VIRTUAL_MAC_PREFIXES)


def _is_ignored_name(name: str) -> bool:
    name = name.lower()
    return any(name.startswith(prefix) for prefix in IGNORED_INTERFACE_PREFIXES)


def is_apipa(ip: str) -> bool:
    return ip.startswith("169.254.")


def is_nat_interface(ip: str, mac: str) -> bool:
    """Detect VirtualBox/VMware NAT adapters."""
    if not mac:
        return False

    mac = mac.lower()

    if mac.startswith("08:00:27"):  # VirtualBox
        return True
    if any(mac.startswith(p) for p in ["00:50:56", "00:0c:29", "00:05:69"]):  # VMware
        return True

    # IP-based NAT detection (VirtualBox default)
    if ip.startswith("10.0.2."):
        return True

    return False


def is_public_wifi(name: str, ip: str, netmask: str) -> bool:
    """Detect if Wi-Fi is likely a public network."""
    lname = name.lower()
    if "wi-fi" not in lname and "wlan" not in lname:
        return False  # Not Wi-Fi

    # Large subnets (20 bits or lower) typical of hotels/universities/public hotspots
    try:
        net = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
        if net.prefixlen <= 20:
            return True
    except:
        pass

    # If no DNS suffix → likely public Wi-Fi
    try:
        suffix = netifaces.gateways().get("dns_suffix")
        if not suffix:
            return True
    except:
        pass

    return False


def _count_arp_neighbors(ip: str) -> int:
    """Count ARP neighbors in same IP block (Linux only)."""
    try:
        neighbors = 0
        with open("/proc/net/arp") as f:
            for line in f.readlines()[1:]:
                if ip.split('.')[0] in line:
                    neighbors += 1
        return neighbors
    except:
        return 0

def running_inside_vagrant():
    try:
        # Detect user "vagrant"
        if "vagrant" in open("/etc/passwd").read():
            return True
    except:
        pass

    try:
        # Detect VirtualBox + Vagrant env variables
        env = open("/proc/1/environ", "rb").read().decode(errors="ignore").lower()
        if "vagrant" in env:
            return True
    except:
        pass

    return False


# ===================================================================
# SCORING LOGIC
# ===================================================================
def score_interface(name: str, ip: str, netmask: str, mac: str):
    """Return (score, reason) so user sees why interface was selected or rejected."""

    # ---------- 0. Reject non-IPv4 ----------
    if not ip or not netmask:
        return -999, "No IPv4 address"

    # ---------- 1. Reject APIPA ----------
    if is_apipa(ip):
        return -999, "APIPA address"

    # ------- Special handling for Vagrant -------
    if running_inside_vagrant():
        # Host-Only
        if ip.startswith("192.168.56."):
            return 100, "Vagrant Host-Only network"

        # NAT for testing purpose
        if ip.startswith("10.0.2."):
            return 80, "Vagrant NAT network"

        # Skip other interfaces
        return -999, "Non-Vagrant interface skipped inside VM"


    # ---------- 2. Reject virtual/tunnel interfaces ----------
    if _is_ignored_name(name):
        return -999, "Ignored interface name"

    if _is_virtual_mac(mac):
        return -999, "Virtual MAC detected"

    # ---------- 3. Detect NAT interfaces ----------
    nat = is_nat_interface(ip, mac)
    inside_vm = running_inside_vm()

    if nat and not inside_vm:
        return -999, "NAT adapter on host OS (skipped)"
    if nat and inside_vm:
        score = 15  # NAT is good inside VM
        return score, "NAT adapter inside VM"

    # ---------- 4. Detect public Wi-Fi ----------
    if is_public_wifi(name, ip, netmask):
        return -999, "Public Wi-Fi (unsafe to scan)"

    # ---------- 5. Basic scoring for remaining interfaces ----------
    score = 0
    reason = []

    # Private subnets score higher
    if ipaddress.ip_address(ip).is_private:
        score += 4
        reason.append("Private network")

    # Network density (ARP neighbors)
    arp_n = _count_arp_neighbors(ip)
    if arp_n >= 3:
        score += 3
        reason.append(f"{arp_n} ARP neighbors")
    elif arp_n == 0:
        score -= 2
        reason.append("Empty ARP table")

    # Check if this interface has the default gateway
    gateways = netifaces.gateways()
    default_gw = gateways.get('default', {}).get(netifaces.AF_INET)

    if default_gw and default_gw[1] == name:
        score += 3
        reason.append("Default gateway reachable")

    # Avoid scanning very large networks (e.g., /16 Wi-Fi)
    try:
        net = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
        if net.prefixlen <= 20:
            score -= 3
            reason.append("Very large subnet (/20 or larger)")
    except:
        pass

    if not reason:
        reason.append("Generic interface")

    return score, "; ".join(reason)


# ===================================================================
# MAIN EXPORT
# ===================================================================
def select_best_interfaces():
    """Return list of valid interfaces sorted by score."""
    results = []

    for name, addrs in psutil.net_if_addrs().items():
        ipv4 = None
        netmask = None
        mac = None

        for addr in addrs:
            if addr.family == socket.AF_INET:
                ipv4 = addr.address
                netmask = addr.netmask
            if addr.family == psutil.AF_LINK:
                mac = addr.address

        if not ipv4:
            continue

        score, reason = score_interface(name, ipv4, netmask, mac)

        if score > -999:
            results.append({
                "name": name,
                "ip": ipv4,
                "netmask": netmask,
                "mac": mac,
                "score": score,
                "reason": reason
            })

    # Sort by descending score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results
