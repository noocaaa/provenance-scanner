"""
File: packages_extractor.py
Author: Noelia Carrasco Vilar
Date: 2025-12-13
Description:
    Extract Packages related data.
"""

import platform
import subprocess

def extract(agent=None):
    pkgs = []
    system = platform.system()

    try:
        if system == "Linux":
            r = subprocess.run(
                ["pip", "list", "--format=json"],
                capture_output=True, text=True
            )
            if r.returncode == 0:
                pkgs = r.stdout

        elif system == "Windows":
            r = subprocess.run(
                ["pip", "list", "--format=json"],
                capture_output=True, text=True
            )
            if r.returncode == 0:
                pkgs = r.stdout
    except:
        pass

    return {
        "python_packages": pkgs,
        "note": "system-level packages collected in later phase",
    }
