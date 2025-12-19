"""
File: graph_builder.py
Author: Noelia Carrasco Vilar
Date: 2025-12-10
Description:
    Graph builder
"""

import networkx as nx
import json
from scanner.provenance.metrics_extractor import extract_internal_metrics

class GraphBuilder:
    def __init__(self):
        self.G = nx.MultiDiGraph()

    def _id(self, kind, value):
        return f"{kind}:{value}"

    def _process_id(self, host, pid):
        return self._id("Process", f"{host}:{pid}")

    def _port_id(self, host, port, proto="tcp", bind_ip=None):
        return self._id("Port", f"{host}:{proto}:{bind_ip}:{port}")

    def _socket_id(self, host, pid, laddr, raddr, proto, status):
        return self._id(
            "Socket",
            f"{host}:{pid}:{proto}:{self._addr_key(laddr)}:{self._addr_key(raddr)}:{status}"
        )

    def _software_family_id(self, name: str):
        norm = self._normalize_exe_name(name.lower())
        return self._id("SoftwareFamily", norm)

    def _os_family_id(self, name: str):
        return self._id("OSFamily", name.lower())

    def _os_instance_id(self, host, name, version):
        return self._id("OSInstance", f"{host}:{name}:{version}")

    def _normalize_exe_name(self, exe_name: str) -> str:
        exe = exe_name.lower()

        exe = exe.rstrip("0123456789.-")

        aliases = {
            "python": {"python", "python3"},
            "sshd": {"sshd"},
            "ssh": {"ssh"},
            "nginx": {"nginx"},
            "node": {"node", "nodejs"},
        }

        for pkg, names in aliases.items():
            if exe in names:
                return pkg

        return exe

    def _addr_key(self, addr):
        if not isinstance(addr, dict):
            return "none"
        ip = addr.get("ip")
        port = addr.get("port")
        return f"{ip}:{port}"

    def _add_listening_ports(self, host_id, network, proc_index):
        for lp in (network or {}).get("listening_ports_preview", []):
            laddr = lp.get("laddr") or {}
            port = laddr.get("port")
            bind = laddr.get("bind")
            pid = lp.get("pid")
            proto = lp.get("protocol", "tcp")

            if port is None:
                continue

            if bind == "all_interfaces":
                bind_ip = "0.0.0.0"
            elif bind == "loopback":
                bind_ip = "127.0.0.1"
            else:
                bind_ip = laddr.get("ip")  # or None

            port_id = self._port_id(host_id, port, proto, bind_ip)

            if bind_ip:
                ip_id = self._id("IP", bind_ip)
                if ip_id in self.G:
                    self._add_unique_edge(port_id, ip_id, "BINDS_IP")

            if port_id not in self.G:
                self.G.add_node(
                    port_id,
                    label="Port",
                    port=int(port),
                    protocol=proto,
                    bind_ip=bind_ip,
                    exposure=self._classify_exposure(bind_ip),
                    kind="Port",
                )

            self._add_unique_edge(host_id, port_id, "EXPOSES")

            if pid is not None and pid in proc_index:
                proc_id = proc_index[pid]

                sock_id = self._socket_id(
                    host_id,
                    pid,
                    laddr,
                    None,
                    proto,
                    "LISTEN"
                )

                if sock_id not in self.G:
                    self.G.add_node(
                        sock_id,
                        label="Socket",
                        protocol=proto,
                        status="LISTEN",
                        laddr=str(laddr),
                        kind="Socket"
                    )

                self._add_unique_edge(proc_id, sock_id, "USES_SOCKET")
                self._add_unique_edge(sock_id, port_id, "BINDS_TO")

    def _classify_exposure(self, bind_ip: str | None):
        if bind_ip in ("0.0.0.0", "::"):
            return "public"
        if bind_ip and bind_ip.startswith("127."):
            return "local"
        return "internal"

    def _canon_user_id(self, host_id: str, username: str) -> str:
        return self._id("User", f"{host_id}:{username}")

    def _add_user_roles_groups(self, user_node_id: str, user_rec: dict):
        roles = user_rec.get("roles") or []
        groups = user_rec.get("groups") or []

        # Roles
        for r in roles:
            if not r:
                continue
            role_id = self._id("Role", r.lower())
            if role_id not in self.G:
                self.G.add_node(
                    role_id,
                    label="Role",
                    name=r.lower(),
                    kind="Role"
                )
            self.G.add_edge(user_node_id, role_id, rel_type="HAS_ROLE")

        # Groups
        for g in groups:
            if not g:
                continue

            group_key = str(g)
            group_id = self._id("Group", group_key)
            if group_id not in self.G:
                self.G.add_node(
                    group_id,
                    label="Group",
                    name=group_key,
                    kind="Group"
                )
            self.G.add_edge(user_node_id, group_id, rel_type="MEMBER_OF")

    def _add_connections(self, host_id, net, proc_index):
        for c in (net or {}).get("connections_preview", []):
            laddr = c.get("laddr")
            raddr = c.get("raddr")
            pid = c.get("pid")
            proto = c.get("protocol", "tcp")
            status = c.get("status")

            if not laddr or pid is None:
                continue

            proc_id = proc_index.get(pid)
            if not proc_id or proc_id not in self.G:
                continue

            sock_id = self._socket_id(
                host_id,
                pid,
                laddr,
                raddr,
                proto,
                status
            )

            if sock_id not in self.G:
                self.G.add_node(
                    sock_id,
                    label="Socket",
                    protocol=proto,
                    status=status,
                    laddr=str(laddr),
                    raddr=str(raddr),
                    kind="Socket"
                )

            self._add_unique_edge(proc_id, sock_id, "USES_SOCKET")

            # Remote endpoint
            if raddr:
                remote_ip = raddr.get("ip")
                ip_id = self._id("IP", remote_ip)

                if ip_id not in self.G:
                    self.G.add_node(
                        ip_id,
                        label="IP",
                        address=remote_ip,
                        kind="IP"
                    )

                self._add_unique_edge(sock_id, ip_id, "CONNECTS_TO")

    def get_or_create_host(self, *, ip=None, hostname=None, role="unknown"):
        for nid, a in self.G.nodes(data=True):
            if a.get("kind") == "Host":
                if ip and a.get("ip") == ip:
                    return nid
                if hostname and a.get("hostname") == hostname:
                    return nid

        key = ip or hostname
        hid = self._id("Host", key)
        if hid not in self.G:
            self.G.add_node(
                hid,
                label="Host",
                ip=ip,
                hostname=hostname,
                role=role,
                kind="Host"
            )
        return hid

    def _add_hardware(self, host_id, hardware):
        if not hardware:
            return

        # ---- META ----
        if hardware.get("virtualized") is not None:
            self.G.nodes[host_id]["virtualized"] = bool(hardware["virtualized"])
        if hardware.get("boot_time") is not None:
            self.G.nodes[host_id]["boot_time"] = float(hardware["boot_time"])

        # -------- CPU --------
        cpu = hardware.get("cpu")
        if cpu:
            cpu_id = self._id("CPU",  f"{host_id}:cpu")
            if cpu_id not in self.G:
                self.G.add_node(
                    cpu_id,
                    label="CPU",
                    physical_cores=cpu.get("physical_cores"),
                    logical_cores=cpu.get("logical_cores"),
                    architecture=cpu.get("architecture"),
                    kind="CPU"
                )
            self.G.add_edge(host_id, cpu_id, rel_type="HAS_HARDWARE")

        # -------- MEMORY --------
        mem = hardware.get("memory")
        if mem:
            mem_id = self._id("Memory",  f"{host_id}:memory")
            if mem_id not in self.G:
                self.G.add_node(
                    mem_id,
                    label="Memory",
                    total=mem.get("total"),
                    available=mem.get("available"),
                    used=mem.get("used"),
                    percent=mem.get("percent"),
                    kind="Memory"
                )
            self.G.add_edge(host_id, mem_id, rel_type="HAS_HARDWARE")

        # -------- DISKS --------
        for d in hardware.get("disk", []):
            disk_id = self._id("Disk", f"{host_id}:{d.get('device')}")
            if disk_id not in self.G:
                self.G.add_node(
                    disk_id,
                    label="Disk",
                    device=d.get("device"),
                    mountpoint=d.get("mountpoint"),
                    fstype=d.get("fstype"),
                    total=d.get("total"),
                    used=d.get("used"),
                    kind="Disk"
                )
            self.G.add_edge(host_id, disk_id, rel_type="HAS_HARDWARE")

    def _add_unique_edge(self, src, dst, rel_type):
        for _, v, data in self.G.out_edges(src, data=True):
            if v == dst and data.get("rel_type") == rel_type:
                return
        self.G.add_edge(src, dst, rel_type=rel_type)

    def build(self, snapshot: dict):
        snap_id = self._id("Snapshot", snapshot["snapshot_id"])
        if snap_id not in self.G:
            self.G.add_node(
                snap_id,
                label="Snapshot",
                collected_at=snapshot["collected_at"],
                kind="Snapshot"
            )

        scanner = snapshot["scanner_host"]
        scanner_host = self.get_or_create_host(
            ip=scanner["network"]["ip"],
            hostname=scanner["hostname"],
            role="scanner"
        )
        self.G.nodes[scanner_host]["is_scanner"] = True
        self.G.nodes[scanner_host]["domain"] = scanner.get("domain")

        self.G.add_edge(snap_id, scanner_host, rel_type="ON_HOST")

        self.scanner_host = scanner_host
        self.current_snapshot = snap_id

        return self.G


    def add_phase0(self, phase0: dict):
        host = self.scanner_host

        for iface in phase0.get("interfaces", []):
            iface_id = self._id("Interface", f"{host}:{iface['name']}")
            if iface_id not in self.G:
                self.G.add_node(
                    iface_id,
                    label="Interface",
                    name=iface["name"],
                    mac=iface.get("mac"),
                    kind="Interface"
                )
            self.G.add_edge(host, iface_id, rel_type="HAS_INTERFACE")

            ip = iface.get("ip")
            if not ip:
                continue

            ip_id = self._id("IP", ip)
            if ip_id not in self.G:
                self.G.add_node(ip_id, label="IP", address=ip, kind="IP")

            self.G.add_edge(iface_id, ip_id, rel_type="HAS_IP")
            self.G.add_edge(host, ip_id, rel_type="HAS_IP")

    def add_phase1(self, phase1: dict):
        host = self.scanner_host

        for iface, result in phase1.get("results", {}).items():
            network = result["network"]
            net_id = self._id("Network", network)

            if net_id not in self.G:
                self.G.add_node(
                    net_id,
                    label="Network",
                    cidr=network,
                    kind="Network"
                )

            # attach scanner IPs to network
            for _, ip_id, data in self.G.out_edges(host, data=True):
                if self.G.nodes[ip_id].get("kind") == "IP":
                    self.G.add_edge(ip_id, net_id, rel_type="IN_NETWORK")

            # discovery provenance
            disc_id = self._id("Discovery", f"{iface}:{network}")

            if disc_id not in self.G:
                self.G.add_node(
                    disc_id,
                    label="Discovery",
                    interface=iface,
                    network=network,
                    kind="Discovery"
                )

            self.G.add_edge(host, disc_id, rel_type="PERFORMED")

            for ip in result.get("discovered_hosts", []):
                remote = self.get_or_create_host(ip=ip, role="discovered")

                ip_id = self._id("IP", ip)
                if ip_id not in self.G:
                    self.G.add_node(ip_id, label="IP", address=ip, kind="IP")

                self.G.add_edge(remote, ip_id, rel_type="HAS_IP")
                self.G.add_edge(ip_id, net_id, rel_type="IN_NETWORK")
                self.G.add_edge(disc_id, remote, rel_type="DISCOVERED")

                details = result.get("details", {}).get(ip, {})
                self.G.nodes[remote]["os_guess"] = details.get("os_hint")
                self.G.nodes[remote]["type_guess"] = details.get("type")

    def add_phase2(self, phase2: dict):
        seen_hosts = set()

        for ip, host_phase2 in phase2.items():
            host_id = self.get_or_create_host(ip=ip)

            if host_id in seen_hosts:
                continue

            seen_hosts.add(host_id)
            self.add_phase2_per_host(host_id, host_phase2)

        self.add_metrics()

    def add_phase2_per_host(self, host, phase2: dict):
        if not phase2:
            return

        if hasattr(self, "current_snapshot"):
            self.G.add_edge(
                self.current_snapshot,
                host,
                rel_type="OBSERVED"
            )

        # =====================================================
        # OS
        # =====================================================
        os_data = phase2.get("os", {})
        os_name = os_data.get("os")
        os_version = os_data.get("os_version")

        if os_name:
            family_id = self._os_family_id(os_name)
            instance_id = self._os_instance_id(host, os_name, os_version)

            # OS Family (global)
            if family_id not in self.G:
                self.G.add_node(
                    family_id,
                    label="OSFamily",
                    name=os_name.lower(),
                    kind="OSFamily"
                )

            # OS Instance (host-scoped)
            if instance_id not in self.G:
                self.G.add_node(
                    instance_id,
                    label="OSInstance",
                    name=os_name,
                    version=os_version,
                    arch=os_data.get("architecture"),
                    host=host,
                    kind="OSInstance"
                )

            self._add_unique_edge(host, instance_id, "RUNS_OS")
            self._add_unique_edge(instance_id, family_id, "INSTANCE_OF")

        # =====================================================
        # HARDWARE
        # =====================================================
        self._add_hardware(host, phase2.get("hardware"))

        # =====================================================
        # PROCESSES (source of truth: services_extractor)
        # =====================================================
        proc_index = {}

        for p in phase2.get("services", {}).get("processes_preview", []):
            pid = p.get("pid")
            if pid is None:
                continue

            p_id = self._process_id(host, pid)
            if p_id not in self.G:
                self.G.add_node(
                    p_id,
                    label="Process",
                    pid=int(pid),
                    name=p.get("name"),
                    user=p.get("username"),
                    ppid=p.get("ppid"),
                    create_time=p.get("create_time"),
                    kind="Process"
                )
            self.G.add_edge(host, p_id, rel_type="RUNS")
            proc_index[pid] = p_id

        self._add_listening_ports(
            host,
            phase2.get("network", {}),
            proc_index
        )

        self._add_connections(
            host_id=host,
            net=phase2.get("network", {}),
            proc_index=proc_index
        )

        # =====================================================
        # PROCESS LINEAGE (PPID)
        # =====================================================

        for p in phase2.get("services", {}).get("processes_preview", []):
            pid = p.get("pid")
            ppid = p.get("ppid")

            if pid is None or ppid is None:
                continue

            child_id = self._process_id(host, pid)
            parent_id = self._process_id(host, ppid)

            # Parent may not be in preview (kernel / short-lived)
            if child_id in self.G and parent_id in self.G:
                self._add_unique_edge(
                    child_id,
                    parent_id,
                    "SPAWNED_BY"
                )

        # =====================================================
        # INSTALLED SYSTEM SOFTWARE (dpkg / rpm)
        # =====================================================
        software_blob = phase2.get("software", {}).get("installed_software", [])

        seen = set()

        for s in software_blob:
            name = s.get("name")
            version = s.get("version")
            source = s.get("source")

            if not name or name in seen:
                continue
            seen.add(name)

            family_id = self._software_family_id(name)
            instance_id = self._id(
                "SoftwareInstance",
                f"{host}:{name}:{version or 'unknown'}"
            )

            # Family (global)
            if family_id not in self.G:
                self.G.add_node(
                    family_id,
                    label="SoftwareFamily",
                    name=name.lower(),
                    kind="SoftwareFamily"
                )

            # Instance (host-scoped)
            if instance_id not in self.G:
                self.G.add_node(
                    instance_id,
                    label="SoftwareInstance",
                    name=name,
                    version=version,
                    source=source,
                    host=host,
                    kind="SoftwareInstance"
                )

            self._add_unique_edge(host, instance_id, "HAS_INSTALLED")
            self._add_unique_edge(instance_id, family_id, "INSTANCE_OF")

        # =====================================================
        # PROCESS → EXECUTES → SOFTWARE
        # =====================================================
        for p in phase2.get("services", {}).get("processes_preview", []):
            pid = p.get("pid")
            exe = p.get("exe")

            if not pid or not exe:
                continue

            proc_id = self._process_id(host, pid)
            if proc_id not in self.G:
                continue

            exe_name = exe.split("/")[-1]
            norm_exe = self._normalize_exe_name(exe_name)

            exe_id = self._id("Executable", f"{host}:{exe_name}")

            if exe_id not in self.G:
                self.G.add_node(
                    exe_id,
                    label="Executable",
                    name=exe_name,
                    normalized_name=norm_exe,
                    kind="Executable"
                )

            self._add_unique_edge(proc_id, exe_id, "EXECUTES")

            family_id = self._software_family_id(norm_exe)

            if family_id not in self.G:
                self.G.add_node(
                    family_id,
                    label="SoftwareFamily",
                    name=norm_exe,
                    kind="SoftwareFamily"
                )

            self._add_unique_edge(exe_id, family_id, "PART_OF")

        # =====================================================
        # USERS (sessions) + SYSTEM USERS (accounts) with roles/groups
        # =====================================================
        users_blob = (phase2.get("users") or {})

        # ---- 1) Create/merge local accounts (system_users) as source of truth
        # Use per-host canonical id: User:{host}:{username}
        for u in users_blob.get("system_users", []) or []:
            if not isinstance(u, dict):
                continue
            username = u.get("username")
            if not username:
                continue

            user_id = self._canon_user_id(host, username)

            if user_id not in self.G:
                self.G.add_node(
                    user_id,
                    label="User",
                    name=username,
                    uid=u.get("uid"),
                    gid=u.get("gid"),
                    home=u.get("home"),
                    shell=u.get("shell"),
                    source=u.get("source"),
                    kind="User"
                )
            self.G.add_edge(host, user_id, rel_type="HAS_ACCOUNT")

            self._add_user_roles_groups(user_id, u)

        for s in users_blob.get("logged_users", []) or []:
            if not isinstance(s, dict):
                continue
            username = s.get("username")
            if not username:
                continue

            user_id = self._canon_user_id(host, username)

            if user_id not in self.G:
                self.G.add_node(
                    user_id,
                    label="User",
                    name=username,
                    kind="User"
                )

            self.G.add_edge(host, user_id, rel_type="HAS_ACCOUNT")


            sess_key = f"{host}:{username}:{s.get('terminal')}:{s.get('host')}:{s.get('started')}"
            sess_id = self._id("Session", sess_key)

            if sess_id not in self.G:
                self.G.add_node(
                    sess_id,
                    label="Session",
                    user=username,
                    terminal=s.get("terminal"),
                    remote_host=s.get("host"),
                    started=s.get("started"),
                    kind="Session"
                )

            self.G.add_edge(host, sess_id, rel_type="HAS_SESSION")
            self.G.add_edge(sess_id, user_id, rel_type="SESSION_USER")

        # =====================================================
        # USER → PROCESS RELATIONSHIP
        # =====================================================
        # Map username -> user node
        user_index = {}
        for u in users_blob.get("system_users", []) or []:
            username = u.get("username")
            if username:
                user_index[username] = self._canon_user_id(host, username)

        for p in phase2.get("services", {}).get("processes_preview", []):
            pid = p.get("pid")
            username = p.get("username")
            if not pid or not username:
                continue

            proc_id = self._process_id(host, pid)
            user_id = user_index.get(username)

            if user_id and proc_id in self.G:
                self._add_unique_edge(
                    user_id,
                    proc_id,
                    "RUNS_PROCESS"
                )

        # =====================================================
        # PYTHON PACKAGES
        # =====================================================
        blob = phase2.get("packages", {}).get("python_packages_preview")
        if blob:
            try:
                pkgs = json.loads(blob)
            except Exception:
                pkgs = []

            for p in pkgs:
                name = p.get("name")
                ver = p.get("version")
                source = p.get("source")
                if not name:
                    continue

                family_id = self._software_family_id(name)
                instance_id = self._id("SoftwareInstance", f"{host}:{name}")

                # Family
                if family_id not in self.G:
                    self.G.add_node(
                        family_id,
                        label="SoftwareFamily",
                        name=name.lower(),
                        kind="SoftwareFamily"
                    )

                # Instance
                if instance_id not in self.G:
                    self.G.add_node(
                        instance_id,
                        label="SoftwareInstance",
                        name=name,
                        version=ver,
                        source=source,
                        host=host,
                        kind="SoftwareInstance"
                    )

                self._add_unique_edge(host, instance_id, "HAS_INSTALLED")
                self._add_unique_edge(instance_id, family_id, "INSTANCE_OF")

    def add_metrics(self):
        metrics = extract_internal_metrics(
            self.G,
            snapshot_id=self.current_snapshot
        )

        mid = metrics["neo_id"]

        self.G.add_node(
            mid,
            label="Metrics",
            kind="Metrics",
            **{k: v for k, v in metrics.items() if k not in ("neo_id", "kind")}
        )

        self.G.add_edge(
            self.current_snapshot,
            mid,
            rel_type="HAS_METRICS"
        )
