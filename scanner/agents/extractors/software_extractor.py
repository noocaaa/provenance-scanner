"""
File: software_extractor.py
Author: Noelia Carrasco Vilar
Date: 2025-12-16
Description:
    Extract installed software/packages from the system.
"""

import platform
import subprocess
import shutil
import json
import os

# ----- HELPERS -----

def _run(cmd):
    try:
        return subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True)
    except Exception:
        return None

# ----- LINUX -----

def _linux_dpkg():
    out = _run(["dpkg-query", "-W", "-f=${Package}\t${Version}\n"])
    if not out:
        return []

    return [
        {
            "name": name,
            "version": version,
            "source": "dpkg",
            "scope": "system",
            "confidence": "high"
        }
        for name, version in
        (line.split("\t") for line in out.splitlines())
    ]

def _linux_rpm():
    out = _run(["rpm", "-qa", "--qf", "%{NAME}\t%{VERSION}\n"])
    if not out:
        return []

    return [
        {
            "name": name,
            "version": version,
            "source": "rpm",
            "scope": "system",
            "confidence": "high"
        }
        for name, version in
        (line.split("\t") for line in out.splitlines())
    ]

# ----- WINDOWS -----

def _windows_registry_installed():
    ps = r"""
    $paths = @(
      "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*",
      "HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*",
      "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*"
    )

    $results = @()

    foreach ($p in $paths) {
      try {
        Get-ItemProperty $p -ErrorAction SilentlyContinue |
          Where-Object { $_.DisplayName } |
          ForEach-Object {
            $results += [PSCustomObject]@{
              Name = $_.DisplayName
              Version = $_.DisplayVersion
              InstallLocation = $_.InstallLocation
              Scope = if ($p.StartsWith("HKCU")) { "user" } else { "system" }
            }
          }
      } catch {}
    }

    $results | ConvertTo-Json
    """

    out = _run(["powershell", "-Command", ps])
    if not out:
        return []

    try:
        data = json.loads(out)
    except Exception:
        return []

    if isinstance(data, dict):
        data = [data]

    return [
        {
            "name": d.get("Name"),
            "version": d.get("Version"),
            "install_path": d.get("InstallLocation"),
            "source": "registry",
            "scope": d.get("Scope"),
            "confidence": "medium"
        }
        for d in data
        if d.get("Name")
    ]


def _windows_msi_installed():
    ps = r"""
    Get-WmiObject Win32_Product |
      Select Name, Version |
      ConvertTo-Json
    """

    out = _run(["powershell", "-Command", ps])
    if not out:
        return []

    try:
        data = json.loads(out)
    except Exception:
        return []

    if isinstance(data, dict):
        data = [data]

    return [
        {
            "name": d.get("Name"),
            "version": d.get("Version"),
            "source": "msi",
            "scope": "system",
            "confidence": "medium"
        }
        for d in data
        if d.get("Name")
    ]


def _windows_portable_heuristic():
    candidates = []
    paths = [
        os.environ.get("PROGRAMFILES"),
        os.environ.get("PROGRAMFILES(X86)"),
        os.environ.get("LOCALAPPDATA")
    ]

    for base in filter(None, paths):
        try:
            for name in os.listdir(base):
                full = os.path.join(base, name)
                if os.path.isdir(full):
                    exe = os.path.join(full, f"{name}.exe")
                    if os.path.exists(exe):
                        candidates.append({
                            "name": name,
                            "version": None,
                            "install_path": full,
                            "source": "portable_heuristic",
                            "scope": "user",
                            "confidence": "low"
                        })
        except Exception:
            continue

    return candidates

# ----- MACOS -----

def _macos_brew():
    if not shutil.which("brew"):
        return []

    out = _run(["brew", "list", "--versions"])
    if not out:
        return []

    return [
        {
            "name": parts[0],
            "version": parts[1],
            "source": "brew",
            "scope": "user",
            "confidence": "high"
        }
        for parts in (line.split() for line in out.splitlines())
    ]



def extract(agent=None):
    system = platform.system().lower()
    software = []

    if system == "linux":
        software.extend(_linux_dpkg())
        software.extend(_linux_rpm())

    elif system == "windows":
        software.extend(_windows_registry_installed())
        software.extend(_windows_msi_installed())
        software.extend(_windows_portable_heuristic())

    elif system == "darwin":
        software.extend(_macos_brew())

    return {
        "installed_software": software
    }
