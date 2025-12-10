"""
File: graph_builder.py
Author: Noelia Carrasco Vilar
Date: 2025-12-09
Description:
    Graph Builder with Hierarchical Provenance Graph
"""
"""
Graph Builder with Clean Node IDs and Neo4j-Friendly Properties
"""
"""
Graph Builder with Clean Node IDs and Neo4j-Friendly Properties
"""

import networkx as nx

class GraphBuilder:
    def __init__(self):
        self.G = nx.MultiDiGraph()

    def _node_id(self, kind: str, key: str) -> str:
        """Return a clean string ID: Host:10.0.0.5"""
        return f"{kind}:{key}"

    def build(self, snapshot: dict):
        G = self.G

        # ----- Snapshot -----
        snap_id = self._node_id("Snapshot", snapshot["snapshot_id"])
        G.add_node(
            snap_id,
            label="Snapshot",
            id=snapshot["snapshot_id"],
            collected_at=snapshot["collected_at"],
            kind="Snapshot"
        )

        # ----- Scanner Host -----
        sh = snapshot["scanner_host"]
        scanner_ip = sh["network"]["ip"]
        scanner_id = self._node_id("Host", scanner_ip)

        G.add_node(
            scanner_id,
            label="Host",
            id=scanner_ip,
            hostname=sh["hostname"],
            domain=sh.get("domain"),
            role="scanner",
            is_scanner=True,
            kind="Host"
        )

        G.add_edge(snap_id, scanner_id, rel_type="ON_HOST")

        # ----- Interfaces of Scanner -----
        iface_nodes = {}
        for iface in sh.get("interfaces", []):
            iface_key = f"{scanner_ip}:{iface['name']}"
            iface_id = self._node_id("Interface", iface_key)

            G.add_node(
                iface_id,
                label="Interface",
                id=iface_key,
                name=iface["name"],
                ip=iface["ip"],
                mac=iface["mac"],
                iface_type=iface["type"],
                kind="Interface"
            )

            G.add_edge(scanner_id, iface_id, rel_type="HAS_INTERFACE")
            iface_nodes[iface["name"]] = iface_id

        # ----- Phase 1 Discovery -----
        lnd = snapshot.get("local_network_discovery", {})
        results = lnd.get("results", {})
        interfaces_scanned = lnd.get("interfaces_scanned", [])

        for iface_scan in interfaces_scanned:
            iface_name = iface_scan["interface"]
            iface_res = results.get(iface_name)
            if not iface_res:
                continue

            # NETWORK NODE
            cidr = iface_res["network"]
            network_id = self._node_id("Network", cidr)

            G.add_node(
                network_id,
                label="Network",
                id=cidr,
                cidr=cidr,
                kind="Network"
            )

            # link interface -> network
            if iface_name in iface_nodes:
                G.add_edge(iface_nodes[iface_name], network_id, rel_type="IN_NETWORK")

            # HOSTS FOUND
            for host_ip, details in iface_res.get("details", {}).items():
                host_id = self._node_id("Host", host_ip)

                G.add_node(
                    host_id,
                    label="Host",
                    id=host_ip,
                    ip=host_ip,
                    os=details.get("os"),
                    host_type=details.get("type"),
                    discovered_by="phase1",
                    kind="Host"
                )

                G.add_edge(network_id, host_id, rel_type="HAS_HOST")

                # TCP ports
                for port in details.get("tcp", []):
                    pid = self._node_id("Port", f"tcp/{port}")
                    G.add_node(pid, label="Port", id=f"tcp/{port}", protocol="tcp", port=port, kind="Port")
                    G.add_edge(host_id, pid, rel_type="EXPOSES")

                # UDP ports
                for port in details.get("udp", []):
                    pid = self._node_id("Port", f"udp/{port}")
                    G.add_node(pid, label="Port", id=f"udp/{port}", protocol="udp", port=port, kind="Port")
                    G.add_edge(host_id, pid, rel_type="EXPOSES")

        return G
