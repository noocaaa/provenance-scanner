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
            "details": [],
            "confidence": "low"
        }
    }

    system = platform.system()

    # ------ LINUX ------
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
            elif virt == "microsoft":
                data["provider"] = "hyperv"

        uuid = _cmd(["cat", "/sys/class/dmi/id/product_uuid"])
        if uuid:
            data["vm_uuid"] = uuid

        # Guest tools
        if shutil.which("VBoxControl"):
            data["guest_tools"]["installed"] = True
            data["guest_tools"]["details"].append("virtualbox-guest-additions")

        if shutil.which("vmtoolsd"):
            data["guest_tools"]["installed"] = True
            data["guest_tools"]["details"].append("vmware-tools")

        if shutil.which("qemu-ga"):
            data["guest_tools"]["installed"] = True
            data["guest_tools"]["details"].append("qemu-guest-agent")

        if data["guest_tools"]["details"]:
            data["guest_tools"]["confidence"] = "high"

    # ------ WINDOWS ------
    elif system == "Windows":
        hv = _cmd(["powershell", "-Command",
                   "(Get-CimInstance Win32_ComputerSystem).Manufacturer + ' ' + (Get-CimInstance Win32_ComputerSystem).Model"
                   ])

        if hv:
            data["virtualized"] = True
            data["hypervisor"] = hv.lower()


            if "vmware" in hv.lower():
                data["provider"] = "vmware"
            elif "virtualbox" in hv.lower():
                data["provider"] = "virtualbox"
            elif "microsoft" in hv.lower():
                data["provider"] = "hyperv"

        uuid = _cmd([
            "powershell",
            "-Command",
            "(Get-CimInstance Win32_ComputerSystemProduct).UUID"
        ])
        if uuid:
            data["vm_uuid"] = uuid

        # Guest tools
        services = _cmd([
            "powershell",
            "-Command",
            "Get-Service | Select Name"
        ]) or ""

        if "vmtools" in services.lower():
            data["guest_tools"]["installed"] = True
            data["guest_tools"]["details"].append("vmware-tools")

        if "vboxservice" in services.lower():
            data["guest_tools"]["installed"] = True
            data["guest_tools"]["details"].append("virtualbox-guest-additions")

        if "vmicheartbeat" in services.lower():
            data["guest_tools"]["installed"] = True
            data["guest_tools"]["details"].append("hyperv-integration-services")

        if data["guest_tools"]["details"]:
            data["guest_tools"]["confidence"] = "high"

    # ------ macOS ------
    elif system == "Darwin":
        hv = _cmd(["sysctl", "-n", "machdep.cpu.features"])
        if hv:
            data["virtualized"] = "unknown"
            data["hypervisor"] = "unknown"
            data["provider"] = "unknown"

    return data

