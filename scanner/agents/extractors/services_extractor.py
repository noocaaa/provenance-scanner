"""
File: services_extractor.py
Author: Noelia Carrasco Vilar
Date: 2025-12-13
Description:
    Extract Services and Processes related data.
"""

import socket
import subprocess
import platform

SOCK_STREAM = socket.SOCK_STREAM

# ------- HELPERS -------

def classify_process(username: str | None) -> str:
    if not username:
        return "unknown"

    system_users = {
        "root",
        "SYSTEM",
        "LOCAL SERVICE",
        "NETWORK SERVICE"
    }

    return "system" if username in system_users else "user"

def detect_process_role(cmdline: list[str]) -> str | None:
    joined = " ".join(cmdline).lower()

    if "main.py" in joined or "scanner" in joined:
        return "scanner"

    if any(s in joined for s in ["bash", "sh", "zsh", "powershell", "cmd.exe"]):
        return "shell"

    return None

# ------- LINUX -------

def extract_linux_services():
    services = []

    try:
        out = subprocess.check_output(
            ["systemctl", "list-units", "--type=service", "--no-pager", "--all"],
            stderr=subprocess.DEVNULL,
            text=True
        )
    except Exception:
        return services

    for line in out.splitlines():
        if not line.endswith(".service"):
            continue

        name = line.split()[0]

        try:
            show = subprocess.check_output(
                ["systemctl", "show", name,
                 "--property=MainPID,ExecStart,User,ActiveState"],
                stderr=subprocess.DEVNULL,
                text=True
            )
        except Exception:
            continue

        props = {}
        for l in show.splitlines():
            if "=" in l:
                k, v = l.split("=", 1)
                props[k] = v

        pid = int(props.get("MainPID", "0")) or None

        services.append({
            "service_name": name,
            "pid": pid,
            "exec": props.get("ExecStart"),
            "username": props.get("User"),
            "state": props.get("ActiveState"),
            "platform": "linux",
            "confidence": "high" if pid else "medium"
        })

    return services

# ------- WINDOWS -------

def windows_token_info(pid: int):
    if not pid:
        return None

    ps = f"""
    try {{
      $integrity = "unknown"
      $elevated = $false

      $groups = whoami /groups

      if ($groups -match "Mandatory Label\\\\System Mandatory Level") {{
        $integrity = "system"
      }} elseif ($groups -match "Mandatory Label\\\\High Mandatory Level") {{
        $integrity = "high"
      }} elseif ($groups -match "Mandatory Label\\\\Medium Mandatory Level") {{
        $integrity = "medium"
      }} elseif ($groups -match "Mandatory Label\\\\Low Mandatory Level") {{
        $integrity = "low"
      }}

      if ($groups -match "S-1-16-12288") {{
        $elevated = $true
      }}

      @{{ 
        integrity_level = $integrity
        token_elevated = $elevated
        source = "mandatory_label"
      }} | ConvertTo-Json
    }} catch {{
      $null
    }}
    """

    try:
        out = subprocess.check_output(
            ["powershell", "-Command", ps],
            stderr=subprocess.DEVNULL,
            text=True
        )
        if not out:
            return None
        import json
        return json.loads(out)
    except Exception:
        return None

def extract_windows_services():
    services = []

    ps = (
        "Get-CimInstance Win32_Service | "
        "Select Name, State, StartMode, ProcessId, StartName, PathName | "
        "ConvertTo-Json"
    )

    try:
        out = subprocess.check_output(
            ["powershell", "-Command", ps],
            stderr=subprocess.DEVNULL,
            text=True
        )
    except Exception:
        return services

    try:
        import json
        data = json.loads(out)
    except Exception:
        return services

    if isinstance(data, dict):
        data = [data]

    for svc in data:
        pid = svc.get("ProcessId") or None
        services.append({
            "service_name": svc.get("Name"),
            "pid": pid if pid != 0 else None,
            "exec": svc.get("PathName"),
            "username": svc.get("StartName"),
            "state": svc.get("State"),
            "start_mode": svc.get("StartMode"),
            "platform": "windows",
            "confidence": "high" if pid else "medium"
        })

    return services

# ------- LINUX + WINDOWS -------


def extract(agent=None, max_processes=300):
    import psutil

    system = platform.system().lower()

    processes = []
    listening_ports = []
    services = []

    # ---- PROCESSES ----

    for p in psutil.process_iter(attrs=[], ad_value=None):
        try:
            cmd = p.cmdline() or []

            try:
                parent = p.parent()
                parent_pid = parent.pid if parent else None
                parent_name = parent.name() if parent else None
            except Exception:
                parent_pid = None
                parent_name = None

            security_context = None

            if system == "windows" and p.username() in ("NT AUTHORITY\\SYSTEM", "LocalSystem"):
                security_context = windows_token_info(p.pid)

            processes.append({
                "pid": p.pid,
                "ppid": p.ppid(),
                "parent_pid": parent_pid,
                "parent_name": parent_name,
                "name": p.name(),
                "exe": p.exe() if p.exe() else None,
                "username": p.username(),
                "cmdline": cmd,
                "cmdline_joined": " ".join(cmd),
                "create_time": p.create_time(),
                "process_type": classify_process(p.username()),
                "process_role": detect_process_role(cmd),
                "security_context": security_context,
            })

            if len(processes) >= max_processes:
                break

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # ---- LISTENING PORTS ----

    for c in psutil.net_connections(kind="inet"):
        if c.status != psutil.CONN_LISTEN or not c.laddr:
            continue

        listening_ports.append({
            "pid": c.pid,
            "laddr": {
                "ip": c.laddr.ip,
                "port": c.laddr.port,
                "bind": (
                    "all_interfaces"
                    if c.laddr.ip in ("0.0.0.0", "::")
                    else "loopback"
                    if c.laddr.ip.startswith("127.")
                    else "specific"
                )
            },
            "protocol": "tcp" if c.type == SOCK_STREAM else "udp",
            "status": c.status,
        })

    # ---- SERVICES ----

    if system == "linux":
        services = extract_linux_services()

    elif system == "windows":
        services = extract_windows_services()

    return {
        "processes_preview": processes,
        "listening_ports_preview": listening_ports,
        "services_preview": services
    }