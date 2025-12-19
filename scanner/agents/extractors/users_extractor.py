"""
File: users_extractor.py
Author: Noelia Carrasco Vilar
Date: 2025-12-13
Description:
    Extract Users related data, including roles and group membership.
"""

import platform
import subprocess

try:
    import grp
except ImportError:
    grp = None

WINDOWS_GPO_ROLE_MAP = {
    "Administrators": "admin",
    "Domain Admins": "domain_admin",
    "Enterprise Admins": "enterprise_admin",
    "Remote Desktop Users": "rdp",
    "Backup Operators": "backup",
    "Account Operators": "account_operator",
}

def infer_linux_roles(username, uid, gid, shell):
    roles = set()
    groups = set()

    if uid == 0:
        roles.add("root")
    elif uid < 1000:
        roles.add("system")
    else:
        roles.add("human")

    if shell in ("/usr/sbin/nologin", "/bin/false", "nologin"):
        roles.add("service")
    else:
        roles.add("interactive")

    if grp:
        try:
            for g in grp.getgrall():
                if username in g.gr_mem or g.gr_gid == gid:
                    groups.add(g.gr_name)
                    if g.gr_name in ("sudo", "wheel"):
                        roles.add("admin")
        except Exception:
            pass

    return sorted(roles), sorted(groups)

def infer_macos_roles(username):
    roles = {"human"}
    groups = set()

    # macOS admin group
    try:
        result = subprocess.run(
            ["dscl", ".", "-read", "/Groups/admin", "GroupMembership"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if username in result.stdout:
            roles.add("admin")
    except Exception:
        pass

    return sorted(roles), sorted(groups)

def infer_windows_local_roles():
    roles_map = {
        "Administrators": "admin",
        "Users": "user",
        "Remote Desktop Users": "rdp",
        "Backup Operators": "backup",
    }

    users = {}

    for group, role in roles_map.items():
        try:
            result = subprocess.run(
                ["net", "localgroup", group],
                capture_output=True,
                text=True,
                shell=True,
                timeout=5
            )
            parsing = False
            for line in result.stdout.splitlines():
                if "----" in line:
                    parsing = not parsing
                    continue
                if parsing:
                    for u in line.split():
                        users.setdefault(u, {"roles": set(), "groups": set()})
                        users[u]["roles"].add(role)
                        users[u]["groups"].add(group)
        except Exception:
            pass

    return users

def windows_users_with_sid_and_domain():
    ps = r"""
    $results = @()

    # Local users
    Get-LocalUser | ForEach-Object {
        $results += [PSCustomObject]@{
            Username = $_.Name
            SID = $_.SID.Value
            Domain = $env:COMPUTERNAME
            Scope = "local"
        }
    }

    # Logged-in users (may include domain users)
    try {
        quser | Select-Object -Skip 1 | ForEach-Object {
            $u = ($_ -split '\s+')[0]
            if ($u -match '\\') {
                $parts = $u -split '\\'
                $results += [PSCustomObject]@{
                    Username = $parts[1]
                    SID = $null
                    Domain = $parts[0]
                    Scope = "domain"
                }
            }
        }
    } catch {}

    $results | Sort-Object Username -Unique | ConvertTo-Json
    """

    try:
        out = subprocess.check_output(
            ["powershell", "-Command", ps],
            stderr=subprocess.DEVNULL,
            text=True
        )
        import json
        data = json.loads(out)
        if isinstance(data, dict):
            data = [data]
        return data
    except Exception:
        return []

def extract(agent=None):
    import psutil

    system = platform.system().lower()

    logged_users = []
    system_users = []

    # --------------- LOGGED-IN SESSIONS ---------------
    try:
        for u in psutil.users():
            logged_users.append({
                "username": u.name,
                "terminal": u.terminal,
                "host": u.host,
                "started": u.started,
            })
    except Exception:
        pass

    # --------------- USERS, ROLES AND GROUP PER SYSTEM ---------------
    if system == "linux":
        try:
            with open("/etc/passwd", "r") as f:
                for line in f:
                    if not line.strip() or line.startswith("#"):
                        continue

                    parts = line.split(":")
                    if len(parts) < 7:
                        continue

                    username, _, uid, gid, _, home, shell = parts[:7]

                    roles, groups = infer_linux_roles(
                        username=username,
                        uid=int(uid),
                        gid=int(gid),
                        shell=shell.strip()
                    )

                    system_users.append({
                        "username": username,
                        "uid": int(uid),
                        "gid": int(gid),
                        "home": home,
                        "shell": shell.strip(),
                        "roles": roles,
                        "groups": groups,
                        "source": "passwd"
                    })
        except Exception:
            pass

    elif system == "darwin":
        try:
            result = subprocess.run(
                ["dscl", ".", "-list", "/Users"],
                capture_output=True,
                text=True,
                timeout=5
            )
            for username in result.stdout.splitlines():
                if not username or username.startswith("_"):
                    continue

                roles, groups = infer_macos_roles(username)

                system_users.append({
                    "username": username,
                    "roles": roles,
                    "groups": groups,
                    "source": "dscl"
                })
        except Exception:
            pass

    elif system == "windows":
        base_users = windows_users_with_sid_and_domain()
        local_roles = infer_windows_local_roles()

        for u in base_users:
            username = u.get("Username")
            info = local_roles.get(username, {"roles": set(), "groups": set()})

            # GPO-inferred roles (from group membership)
            gpo_roles = {
                WINDOWS_GPO_ROLE_MAP[g]
                for g in info.get("groups", [])
                if g in WINDOWS_GPO_ROLE_MAP
            }

            system_users.append({
                "username": username,
                "sid": u.get("SID"),
                "domain": u.get("Domain"),
                "scope": u.get("Scope"),
                "roles": sorted(set(info.get("roles", [])) | gpo_roles),
                "groups": sorted(info.get("groups", [])),
                "gpo_inferred_roles": sorted(gpo_roles),
                "source": "windows_security"
            })

    return {
        "os": platform.system(),
        "logged_users": logged_users,
        "system_users": system_users
    }