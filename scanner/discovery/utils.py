"""
File: utils.py
Author: Noelia Carrasco Vilar
Date: 2025-12-08
Description:
    Useful functions. 
"""

import subprocess
import re
import netifaces
import ipaddress

def run(cmd):
    """Run a shell command and return output as string."""
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode()
    except:
        return ""

def extract_regex(pattern, text, default=""):
    m = re.search(pattern, text, re.MULTILINE)
    return m.group(1).strip() if m else default

def get_local_subnet():
    """
    Returns the best local subnet as an ipaddress.IPv4Network object.
    Works on Windows, Linux, and macOS.
    """

    interfaces = netifaces.interfaces()
    best_subnet = None

    for iface in interfaces:
        addrs = netifaces.ifaddresses(iface)

        if netifaces.AF_INET in addrs:
            ipv4_info = addrs[netifaces.AF_INET][0]
            ip = ipv4_info.get('addr')
            netmask = ipv4_info.get('netmask')

            if ip and netmask and not ip.startswith("169.254"):
                try:
                    network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)

                    # pick the largest usable subnet or the first valid one
                    if best_subnet is None or network.num_addresses > best_subnet.num_addresses:
                        best_subnet = network

                except ValueError:
                    continue

    if best_subnet is None:
        raise RuntimeError("Could not determine local subnet")

    return best_subnet
