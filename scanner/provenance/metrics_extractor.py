import math
import networkx as nx
from collections import Counter

def extract_internal_metrics(G: nx.MultiDiGraph, snapshot_id: str):

    nodes = list(G.nodes(data=True))
    edges = list(G.edges(data=True))

    # -------- NODE COUNTS --------

    total_nodes = len(nodes)
    total_edges = len(edges)

    # -------- PORT METRICS --------
    ports = [(n, a) for n, a in nodes if a.get("kind") == "Port"]

    total_ports = len(ports)

    public_ports = sum(1 for _, a in ports if a.get("exposure") == "public")
    local_ports = sum(1 for _, a in ports if a.get("exposure") == "local")
    internal_ports = sum(1 for _, a in ports if a.get("exposure") == "internal")

    # -------- PROCESS METRICS --------
    processes = [(n, a) for n, a in nodes if a.get("kind") == "Process"]

    total_processes = len(processes)
    system_processes = sum(
        1 for _, a in processes if a.get("user") in ("root", "SYSTEM")
    )

    processes_without_user = sum(
        1 for _, a in processes if not a.get("user")
    )

    # -------- LISTENING / PID COVERAGE --------
    listens_edges = [
        (u, v) for u, v, a in edges
        if a.get("rel_type") == "BINDS_TO"
    ]

    ports_with_pid = len({v for _, v in listens_edges})

    pid_coverage = (
        ports_with_pid / total_ports if total_ports > 0 else 0.0
    )

    # -------- PROCESS DENSITY --------
    hosts = [n for n, a in nodes if a.get("kind") == "Host"]
    process_density = (
        total_processes / len(hosts) if hosts else 0.0
    )

    # -------- PUBLIC EXPOSURE RATIO --------
    public_exposure_ratio = (
        public_ports / total_ports if total_ports > 0 else 0.0
    )

    # -------- PRIVILEGE RISK --------
    privileged_listeners = 0
    for u, v, a in listens_edges:
        proc = G.nodes[u]
        port = G.nodes[v]
        if proc.get("user") in ("root", "SYSTEM") and port.get("exposure") == "public":
            privileged_listeners += 1

    # -------- EDGE DISTRIBUTION --------
    edge_types = Counter(a.get("rel_type") for _, _, a in edges)

    # -------- ATTACK SURFACE ENTROPY --------
    exposure_counts = [public_ports, local_ports, internal_ports]
    exposure_total = sum(exposure_counts)

    entropy = 0.0
    if exposure_total > 0:
        for c in exposure_counts:
            if c > 0:
                p = c / exposure_total
                entropy -= p * math.log2(p)

    # -------- ATTRIBUTION CONFIDENCE --------
    attribution_confidence = (
        pid_coverage +
        (1 - processes_without_user / total_processes if total_processes else 1)
    ) / 2

    return {
        "neo_id": f"Metrics:{snapshot_id}",
        "kind": "Metrics",

        # Core
        "total_nodes": total_nodes,
        "total_edges": total_edges,

        # Ports
        "ports_total": total_ports,
        "public_ports": public_ports,
        "local_ports": local_ports,
        "internal_ports": internal_ports,
        "public_exposure_ratio": public_exposure_ratio,

        # Processes
        "processes_total": total_processes,
        "system_processes": system_processes,
        "process_density": process_density,

        # Attribution
        "ports_with_pid": ports_with_pid,
        "pid_coverage": pid_coverage,
        "attribution_confidence": attribution_confidence,

        # Risk
        "privileged_public_listeners": privileged_listeners,

        # Graph
        "edge_types": dict(edge_types),
        "attack_surface_entropy": entropy,
    }