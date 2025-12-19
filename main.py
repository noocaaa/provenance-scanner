"""
File: main.py
Author: Noelia Carrasco Vilar
Date: 2025-12-07
Description:
    Entrypoint to execute the discovery phase.
"""
from scanner.agents.ssh_agent import SSHAgent
from scanner.discovery.phase0_selfdiscovery import run_phase0
from scanner.discovery.phase1_localnetworkdiscovery import run_phase1
from scanner.network.interface_selector import select_best_interfaces
from scanner.provenance.snapshot_formatter import build_snapshot
from scanner.provenance.graph_builder import GraphBuilder
from scanner.provenance.neo4j_push import Neo4jConnector
from scanner.agents.correlation.topology_builder import TopologyBuilder
from scanner.agents.remote_runner.runner import run_all
from scanner.agents.winrm_agent import WinRMAgent

from dotenv import load_dotenv
from utils import save_results

import os

def select_phase2_targets(phase1: dict, local_ips: set[str], local_hostname: str | None):
    valid_hosts = set()

    iface_meta = {i["interface"]: i for i in phase1.get("interfaces_scanned", [])}

    for iface, result in phase1.get("results", {}).items():
        meta = iface_meta.get(iface, {})
        reason = (meta.get("reason") or "").lower()
        network_role = "laboratory" if "host-only" in reason else "egress"

        if network_role != "laboratory":
            continue

        for ip in result.get("discovered_hosts", []):
            if ip in local_ips:
                continue

            details = result.get("details", {}).get(ip, {})

            if details.get("hostname") == local_hostname:
                continue

            tcp = details.get("tcp", [])
            type_guess = details.get("type")

            if type_guess in ("gateway", "network_device"):
                continue

            if 22 in tcp or 5985 in tcp or 5986 in tcp:
                valid_hosts.add(ip)

    return sorted(valid_hosts)

if __name__ == "__main__":

    all_results = {}

    # -----------------------
    # PHASE 0 — SELF DISCOVERY
    # -----------------------
    phase0 = run_phase0()
    all_results["phase0"] = phase0
    save_results(phase0, label="phase0")

    # -----------------------
    # INTERFACE SELECTION
    # -----------------------
    print("\n=== Selecting interfaces for Phase 1 ===")
    interfaces = select_best_interfaces()

    print("\nRanked Interfaces:")
    for iface in interfaces:
        print(f"  {iface['name']:20} {iface['ip']:15} score={iface['score']}")

    # -----------------------
    # PHASE 1 — LOCAL DISCOVERY ON BEST INTERFACES
    # -----------------------
    all_phase1 = {
        "interfaces_scanned": [],
        "results": {},
        "overall_summary": {}
    }

    unique_hosts = set()
    networks_discovered = set()

    for iface in interfaces:
        name = iface["name"]
        ip = iface["ip"]
        netmask = iface["netmask"]

        print(f"\n--- Running Phase 1 on {name} ({ip}/{netmask}) ---")

        phase1_result = run_phase1(
            ip=ip,
            netmask=netmask,
            methods=["arp", "tcp"],
            skip_arp=False,
            fallback_icmp=False
        )

        all_phase1["interfaces_scanned"].append({
            "interface": name,
            "ip": ip,
            "netmask": netmask,
            "score": iface["score"],
            "reason": iface["reason"]
        })

        all_phase1["results"][name] = phase1_result

        for h in phase1_result["discovered_hosts"]:
            unique_hosts.add(h)

        networks_discovered.add(phase1_result["network"])

    all_phase1["overall_summary"] = {
        "total_interfaces_scanned": len(all_phase1["interfaces_scanned"]),
        "total_unique_hosts": len(unique_hosts),
        "unique_hosts": sorted(unique_hosts),
        "networks_discovered": sorted(networks_discovered)
    }

    all_results["phase1"] = all_phase1

    save_results(all_phase1, label="phase1")

    # -----------------------
    # PHASE 2 — EXTRACTOR
    # -----------------------

    print("\n=== PHASE 2: LOCAL EXTRACTION ===")

    all_phase2 = {}

    local_ip = phase0.get("network", {}).get("ip")
    local_ips = {
        i["ip"]
        for i in all_results["phase1"].get("interfaces_scanned", [])
        if i.get("ip")
    }

    local_hostname = (
            phase0.get("system", {}).get("hostname")
            or phase0.get("os", {}).get("hostname")
            or phase0.get("hostname")
    )

    phase2_targets = select_phase2_targets(
        all_results["phase1"],
        local_ips=local_ips,
        local_hostname=local_hostname
    )

    all_phase2[local_ip] = run_all()

    for ip in phase2_targets:
        print(f"[+] Deploying agent to {ip}")

        if ip in local_ips:
            continue

        details = None
        for iface, res in all_results["phase1"]["results"].items():
            details = res.get("details", {}).get(ip)
            if details:
                break

        tcp = details.get("tcp", []) if details else []

        if 5985 in tcp or 5986 in tcp:
            agent = WinRMAgent(
                host=ip,
                user="vagrant",
                password="vagrant"
            )
        else:
            agent = SSHAgent(
                host=ip,
                user="vagrant",
                key_path="~/.ssh/cluster_key"
            )

        agent.deploy()
        agent.execute()
        result = agent.collect(local_output_dir="testing/data")
        agent.cleanup()

        all_phase2[ip] = result


    all_results["phase2"] = all_phase2
    save_results(all_phase2, label="phase2_distributed")

    # -----------------------
    # PHASE 3 — SYSTEM TOPOLOGY / CONSTRUCTION
    # -----------------------

    print("\n=== PHASE 3: SYSTEM CONSTRUCTION ===")

    topology_builder = TopologyBuilder(all_results)
    system_model = topology_builder.build()

    save_results(system_model, label="system_construction")

    # -----------------------
    # GRAPH BUILDING
    # -----------------------
    snapshot = build_snapshot(all_results)

    builder = GraphBuilder()
    builder.build(snapshot)

    builder.add_phase0(all_results["phase0"])
    builder.add_phase1(all_results["phase1"])
    builder.add_phase2(all_results["phase2"])

    load_dotenv()

    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")

    neo = Neo4jConnector(uri, user, password)
    neo.clear_database()
    neo.push_graph(builder.G)
    neo.close()

    print("\n=== Discovery Completed ===")
