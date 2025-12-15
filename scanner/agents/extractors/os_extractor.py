"""
File: os_extractor.py
Author: Noelia Carrasco Vilar
Date: 2025-12-13
Description:
    Extract OS related data.
"""

import platform
import socket

def extract(agent=None):
    data = {
        "hostname": socket.gethostname(),
        "fqdn": socket.getfqdn(),
        "os": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
    }

    # Linux distro info
    if platform.system() == "Linux":
        try:
            with open("/etc/os-release") as f:
                data["os_release_file"] = f.read()
        except:
            pass

    # Windows specific
    if platform.system() == "Windows":
        data["windows_edition"] = platform.win32_edition()
        data["windows_version"] = platform.win32_ver()

    return data
