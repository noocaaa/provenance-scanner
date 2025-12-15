import networkx as nx
import json
import re

class GraphBuilder:
    def __init__(self):
        self.G = nx.MultiDiGraph()

    def _id(self, kind, value):
        return f"{kind}:{value}"

    def _add_connections(self, host_id, net: dict):
        conns = (net or {}).get("connections_preview") or []

        for c in conns:
            pid = c.get("pid")
            status = c.get("status")
            raddr = c.get("raddr")
            laddr = c.get("laddr")

            if laddr:
                ip = laddr.get("ip")
                port = laddr.get("port")
            else:
                ip, port = None, None

            # 1) Always create a Socket node (because we do have laddr/status)
            sock_key = f"{host_id}:{pid}:{laddr}:{raddr}:{status}"
            sock_id = self._id("Socket", sock_key)

            self.G.add_node(
                sock_id,
                label="Socket",
                pid=pid,
                laddr=str(laddr) if laddr is not None else None,
                raddr=str(raddr) if raddr is not None else None,
                status=status,
                kind="Socket"
            )
            self.G.add_edge(host_id, sock_id, rel_type="HAS_SOCKET")

            # 2) If there is a real port -> Port node
            if port is not None:
                port_id = self._id("Port", f"{host_id}:tcp:{port}")
                self.G.add_node(
                    port_id,
                    label="Port",
                    port=int(port),
                    protocol="tcp",
                    bind_ip=ip,
                    kind="Port"
                )
                self.G.add_edge(host_id, port_id, rel_type="EXPOSES")
                self.G.add_edge(sock_id, port_id, rel_type="USES_PORT")


    def get_or_create_host(self, *, ip=None, hostname=None, role="unknown"):
        for nid, a in self.G.nodes(data=True):
            if a.get("kind") == "Host":
                if ip and a.get("ip") == ip:
                    return nid
                if hostname and a.get("hostname") == hostname:
                    return nid

        key = ip or hostname
        hid = self._id("Host", key)
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

        # ---- meta ----
        if hardware.get("virtualized") is not None:
            self.G.nodes[host_id]["virtualized"] = bool(hardware["virtualized"])
        if hardware.get("boot_time") is not None:
            self.G.nodes[host_id]["boot_time"] = float(hardware["boot_time"])

        # -------- CPU --------
        cpu = hardware.get("cpu")
        if cpu:
            cpu_id = self._id("CPU",  f"{host_id}:cpu")
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

    def _link_processes_to_ports(self, host_id, proc_index, port_index, connections):
        for c in connections:
            pid = c.get("pid")
            laddr = c.get("laddr") or {}
            port = laddr.get("port")
            ip = laddr.get("ip")

            if not pid or not port:
                continue

            proc_id = proc_index.get(pid)
            port_id = port_index.get(port)

            if proc_id and port_id:
                self.G.add_edge(proc_id, port_id, rel_type="LISTENS_ON")

    def _classify_network_role(self, iface_meta: dict) -> str:
        """
        Decide el rol de la red según el reason del interface selector
        """
        reason = (iface_meta.get("reason") or "").lower()
        if "host-only" in reason:
            return "laboratory"
        if "nat" in reason:
            return "egress"
        return "unknown"

    def _host_is_valid(self, *, ip, details: dict, network_role: str, local_ip: str) -> bool:
        """
        Decide si un host debe entrar en el grafo
        """
        tcp_ports = details.get("tcp", [])
        os_guess = details.get("os")
        type_guess = details.get("type")

        # Siempre incluir el host local
        if ip == local_ip:
            return True

        # Infraestructura (gateways, network devices)
        if type_guess in ("gateway", "network_device"):
            return True

        # Host confirmado por capa transporte / OS
        if tcp_ports or (os_guess and os_guess != "unknown"):
            return True

        # Ruido típico de NAT
        if network_role == "egress":
            return False

        # En laboratorio (host-only) se puede incluir con baja confianza
        return False

    def build(self, snapshot: dict):
        snap_id = self._id("Snapshot", snapshot["snapshot_id"])
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
        return self.G


    def add_phase0(self, phase0: dict):
        host = self.scanner_host

        for iface in phase0.get("interfaces", []):
            iface_id = self._id("Interface", f"{host}:{iface['name']}")
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
            self.G.add_node(ip_id, label="IP", address=ip, kind="IP")

            self.G.add_edge(iface_id, ip_id, rel_type="HAS_IP")
            self.G.add_edge(host, ip_id, rel_type="HAS_IP")

    def add_phase1(self, phase1: dict):
        host = self.scanner_host

        for iface, result in phase1.get("results", {}).items():
            network = result["network"]
            net_id = self._id("Network", network)

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
                self.G.add_node(ip_id, label="IP", address=ip, kind="IP")

                self.G.add_edge(remote, ip_id, rel_type="HAS_IP")
                self.G.add_edge(ip_id, net_id, rel_type="IN_NETWORK")
                self.G.add_edge(disc_id, remote, rel_type="DISCOVERED")

                details = result.get("details", {}).get(ip, {})
                self.G.nodes[remote]["os_guess"] = details.get("os")
                self.G.nodes[remote]["type_guess"] = details.get("type")

    def add_phase2(self, phase2: dict):
        for ip, host_phase2 in phase2.items():
            host_id = self.get_or_create_host(ip=ip)
            self.add_phase2_per_host(host_id, host_phase2)

    def add_phase2_per_host(self, host, phase2: dict):
        if not phase2:
            return

        # =====================================================
        # OS
        # =====================================================
        os_data = phase2.get("os", {})
        if os_data.get("os"):
            os_id = self._id("OS", f"{os_data['os']}:{os_data.get('os_version')}")
            self.G.add_node(
                os_id,
                label="OS",
                name=os_data.get("os"),
                version=os_data.get("os_version"),
                arch=os_data.get("architecture"),
                kind="OS"
            )
            self.G.add_edge(host, os_id, rel_type="RUNS_OS")

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

            p_id = self._id("Process", f"{host}:{pid}")
            self.G.add_node(
                p_id,
                label="Process",
                pid=int(pid),
                name=p.get("name"),
                user=p.get("username"),
                kind="Process"
            )
            self.G.add_edge(host, p_id, rel_type="RUNS")
            proc_index[pid] = p_id

        # =====================================================
        # PORTS (source of truth: services_extractor)
        # =====================================================
        port_index = {}

        for lp in phase2.get("services", {}).get("listening_ports_preview", []):
            port = lp.get("port")
            ip = lp.get("ip")
            status = lp.get("status")

            if port is None:
                continue

            port_id = self._id("Port", f"{host}:tcp:{port}")

            self.G.add_node(
                port_id,
                label="Port",
                port=int(port),
                protocol="tcp",
                bind_ip=ip,
                state=status,
                kind="Port"
            )

            self.G.add_edge(host, port_id, rel_type="EXPOSES")
            port_index[port] = port_id

        # =====================================================
        # PROCESS → PORT ATTRIBUTION
        # =====================================================
        connections = phase2.get("network", {}).get("connections_preview", [])
        self._link_processes_to_ports(
            host,
            proc_index,
            port_index,
            connections
        )

        self._add_connections(
            host_id=host,
            net=phase2.get("network", {})
        )

        # =====================================================
        # USERS
        # =====================================================
        for u in phase2.get("users", {}).get("logged_users", []):
            if not isinstance(u, dict):
                continue
            user = u.get("user")
            if not user:
                continue

            uid = self._id("User", user)
            self.G.add_node(
                uid,
                label="User",
                name=user,
                kind="User"
            )
            self.G.add_edge(host, uid, rel_type="LOGGED_IN_AS")

        # =====================================================
        # SYSTEM USERS (local accounts)
        # =====================================================
        for u in phase2.get("users", {}).get("system_users", []):
            if not isinstance(u, dict):
                continue

            user = u.get("user")
            if not user:
                continue

            uid = self._id("User", f"{host}:{user}")

            self.G.add_node(
                uid,
                label="User",
                name=user,
                uid=u.get("uid"),
                home=u.get("home"),
                shell=u.get("shell"),
                kind="User"
            )

            self.G.add_edge(host, uid, rel_type="HAS_ACCOUNT")

        # =====================================================
        # PYTHON PACKAGES
        # =====================================================
        blob = phase2.get("packages", {}).get("python_packages")
        if blob:
            try:
                pkgs = json.loads(blob)
            except Exception:
                pkgs = []

            for p in pkgs:
                name = p.get("name")
                ver = p.get("version")
                if not name:
                    continue

                sid = self._id("Software", f"{name}:{ver}")
                self.G.add_node(
                    sid,
                    label="Software",
                    name=name,
                    version=ver,
                    kind="Software"
                )
                self.G.add_edge(host, sid, rel_type="INSTALLED")
