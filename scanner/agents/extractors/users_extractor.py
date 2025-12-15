"""
File: users_extractor.py
Author: Noelia Carrasco Vilar
Date: 2025-12-13
Description:
    Extract Users related data.
"""
import psutil
import platform
import subprocess

def extract(agent=None):
    logged_users = []
    system_users = []

    system = platform.system().lower()

    # ==================================================
    # 1) Logged users (sessions) — ALL OS
    # ==================================================
    try:
        for u in psutil.users():
            logged_users.append({
                "user": u.name,
                "terminal": u.terminal,
                "host": u.host,
                "started": u.started,
            })
    except Exception:
        pass

    # ==================================================
    # 2) System users — OS specific
    # ==================================================

    # ---------- LINUX ----------
    if system == "linux":
        try:
            with open("/etc/passwd", "r") as f:
                for line in f:
                    if not line.strip() or line.startswith("#"):
                        continue
                    parts = line.split(":")
                    if len(parts) < 7:
                        continue

                    username, _, uid, gid, gecos, home, shell = parts[:7]
                    system_users.append({
                        "user": username,
                        "uid": int(uid),
                        "gid": int(gid),
                        "home": home,
                        "shell": shell.strip(),
                    })
        except Exception:
            pass

    # ---------- MACOS ----------
    elif system == "darwin":
        try:
            result = subprocess.run(
                ["dscl", ".", "-list", "/Users"],
                capture_output=True,
                text=True,
                timeout=5
            )
            for user in result.stdout.splitlines():
                if user and not user.startswith("_"):
                    system_users.append({
                        "user": user,
                        "source": "dscl"
                    })
        except Exception:
            pass

    # ---------- WINDOWS ----------
    elif system == "windows":
        try:
            result = subprocess.run(
                ["net", "user"],
                capture_output=True,
                text=True,
                timeout=5,
                shell=True
            )
            parsing = False
            for line in result.stdout.splitlines():
                if "----" in line:
                    parsing = not parsing
                    continue
                if parsing:
                    for user in line.split():
                        system_users.append({
                            "user": user,
                            "source": "net user"
                        })
        except Exception:
            pass

    return {
        "logged_users": logged_users,
        "system_users": system_users,
        "os": platform.system(),
    }
