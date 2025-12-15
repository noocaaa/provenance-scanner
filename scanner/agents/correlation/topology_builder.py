"""
File: topology_builder.py
Author: Noelia Carrasco Vilar
Date: 2025-12-14
Description:
    Produces an inferred system topology.
"""

class TopologyBuilder:
    def __init__(self, results: dict):
        self.phase0 = results.get("phase0", {})
        self.phase1 = results.get("phase1", {})
        self.phase2 = results.get("phase2", {})

    # =====================================================
    # PUBLIC
    # =====================================================
    def build(self) -> dict:
        return {
            "system": self._system(),
            "network": self._network(),
            "nodes": self._nodes(),
        }

    # =====================================================
    # SYSTEM
    # =====================================================
    def _system(self):
        virtualized, evidence = self._detect_virtualization()
        provider, prov_evidence, prov_conf = self._detect_provider()

        return {
            "type": "virtual_machine" if virtualized else "bare_metal",
            "confidence": 0.95 if virtualized else 0.8,
            "provider": {
                "name": provider,
                "confidence": prov_conf,
                "evidence": prov_evidence,
            },
            "evidence": evidence,
        }

    def _detect_virtualization(self):
        local_ip = self.phase0.get("network", {}).get("ip")
        hw = (self.phase2.get(local_ip) or {}).get("hardware", {})
        evidence = []

        if hw.get("virtualized"):
            evidence.append("hardware.virtualized flag")

        cpu_model = str(hw.get("cpu", {}).get("model", ""))
        if any(k in cpu_model.lower() for k in ["virtual", "vbox", "kvm", "vmware"]):
            evidence.append(f"cpu model contains '{cpu_model}'")

        return bool(evidence), evidence

    def _detect_provider(self):
        evidence = []
        score = 0.0

        local_ip = self.phase0.get("network", {}).get("ip")
        host_p2 = self.phase2.get(local_ip) or {}

        users = host_p2.get("users", {}).get("logged_users", [])
        if any(u.get("user") == "vagrant" for u in users):
            score += 0.4
            evidence.append("vagrant user present")

        networks = self.phase1.get("overall_summary", {}).get("networks_discovered", [])
        if any(n.startswith("192.168.56.") for n in networks):
            score += 0.3
            evidence.append("192.168.56.0/24 private network")

        gateway = self.phase0.get("network", {}).get("gateway")
        if gateway == "10.0.2.2":
            score += 0.2
            evidence.append("VirtualBox NAT gateway 10.0.2.2")

        provider = "virtualbox" if score >= 0.6 else "unknown"
        return provider, evidence, round(score, 2)

    # =====================================================
    # NETWORK
    # =====================================================
    def _network(self):
        return {
            "cidrs": self.phase1.get("overall_summary", {}).get("networks_discovered", []),
            "gateway": self.phase0.get("network", {}).get("gateway"),
            "dns": self.phase0.get("network", {}).get("dns"),
        }

    # =====================================================
    # NODES
    # =====================================================
    def _nodes(self):
        """
        Builds one node per discovered host if possible.
        Falls back to local node only.
        """
        nodes = []

        discovered = self.phase1.get("overall_summary", {}).get("unique_hosts", [])
        local_ip = self.phase0.get("network", {}).get("ip")

        if not discovered:
            discovered = [local_ip]

        for ip in discovered:
            nodes.append(self._build_node(ip))

        return nodes

    def _build_node(self, ip: str):
        local_ip = self.phase0.get("network", {}).get("ip")
        hostname = self.phase0.get("hostname") if ip == local_ip else ip
        host_p2 = self.phase2.get(ip) or {}

        return {
            "name": hostname,
            "hostname": hostname,
            "ip": ip,
            "os": host_p2.get("os", {}).get("os"),
            "role": self._infer_role(ip),
            "resources": self._resources(ip),
            "services": self._services(ip),
            "users": self._users(ip),
        }

    # =====================================================
    # NODE DETAILS
    # =====================================================
    def _resources(self, ip: str):
        host_p2 = self.phase2.get(ip) or {}
        cpu = host_p2.get("hardware", {}).get("cpu", {})
        mem = host_p2.get("hardware", {}).get("memory", {})

        total_bytes = mem.get("total")
        memory_mb = int(total_bytes / 1024 / 1024) if total_bytes else None

        return {
            "cpus": cpu.get("logical_cores"),
            "memory_mb": memory_mb,
        }

    def _services(self, ip: str):
        host_p2 = self.phase2.get(ip) or {}
        ports = host_p2.get("services", {}).get("listening_ports_preview", [])

        open_ports = sorted({
            p["port"]
            for p in ports
            if p.get("status") == "LISTEN" and p.get("port")
        })

        return {
            "open_ports": open_ports if open_ports else None
        }

    def _users(self, ip: str):
        host_p2 = self.phase2.get(ip) or {}
        users = host_p2.get("users", {}).get("logged_users", [])
        return sorted({u["user"] for u in users if "user" in u})

    # =====================================================
    # ROLE INFERENCE
    # =====================================================
    def _infer_role(self, ip: str):
        ports = self._services(ip).get("open_ports") or []

        if 53 in ports:
            return "dns"
        if 9100 in ports or 631 in ports:
            return "printer"
        if 22 in ports:
            return "linux_node"
        return "generic"