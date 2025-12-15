"""
File: virtualization_extractor.py
Author: Noelia Carrasco Vilar
Date: 2025-12-14
Description:
    Extraction of virtualization / hypervisor information
"""

import platform
import subprocess
import shutil

def _cmd(cmd):
    try:
        return subprocess.check_output(
            cmd, stderr=subprocess.DEVNULL, text=True
        ).strip()
    except Exception:
        return None


def extract(agent=None):
    data = {
        "virtualized": False,
        "hypervisor": None,
        "provider": None,
        "vm_uuid": None,
        "guest_tools": {
            "installed": False,
            "details": None
        }
    }

    system = platform.system()

    # ----------------------------
    # Linux
    # ----------------------------
    if system == "Linux":
        virt = _cmd(["systemd-detect-virt"])
        if virt and virt != "none":
            data["virtualized"] = True
            data["hypervisor"] = virt

            if virt == "oracle":
                data["provider"] = "virtualbox"
            elif virt in ("kvm", "qemu"):
                data["provider"] = "kvm"
            elif virt == "vmware":
                data["provider"] = "vmware"

        # DMI UUID
        uuid = _cmd(["cat", "/sys/class/dmi/id/product_uuid"])
        if uuid:
            data["vm_uuid"] = uuid

        # Guest tools
        if shutil.which("VBoxControl"):
            data["guest_tools"]["installed"] = True
            data["guest_tools"]["details"] = "virtualbox-guest-utils"

    # ----------------------------
    # Windows
    # ----------------------------
    elif system == "Windows":
        hv = _cmd(["powershell", "-Command",
                   "(Get-CimInstance Win32_ComputerSystem).Model"])
        if hv:
            data["virtualized"] = True
            data["hypervisor"] = hv
            data["provider"] = hv

        uuid = _cmd(["powershell", "-Command",
                     "(Get-CimInstance Win32_ComputerSystemProduct).UUID"])
        if uuid:
            data["vm_uuid"] = uuid

    # ----------------------------
    # macOS
    # ----------------------------
    elif system == "Darwin":
        hv = _cmd(["sysctl", "-n", "machdep.cpu.features"])
        if hv:
            data["virtualized"] = True
            data["hypervisor"] = "unknown"
            data["provider"] = "unknown"

    return data

