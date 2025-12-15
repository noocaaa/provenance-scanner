"""
File: hardware_extractor.py
Author: Noelia Carrasco Vilar
Date: 2025-12-13
Description:
    Extract Hardware related data.
"""

import psutil
import platform

def extract(agent=None):
    return {
        "cpu": {
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "architecture": platform.processor(),
        },
        "memory": {
            "total": psutil.virtual_memory().total,
            "available": psutil.virtual_memory().available,
            "used": psutil.virtual_memory().used,
            "percent": psutil.virtual_memory().percent,
        },
        "disk": [
            {
                "device": d.device,
                "mountpoint": d.mountpoint,
                "fstype": d.fstype,
                "total": psutil.disk_usage(d.mountpoint).total,
                "used": psutil.disk_usage(d.mountpoint).used,
            }
            for d in psutil.disk_partitions(all=False)
            if d.mountpoint
        ],
        "boot_time": psutil.boot_time(),
        "virtualized": platform.system() != platform.node(),
    }