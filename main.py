"""
File: main.py
Author: Noelia Carrasco Vilar
Date: 2025-12-07
Description:
    Entrypoint to execute the discovery phase.
"""

from scanner.discovery.phase0_selfdiscovery import run_phase0
from scanner.discovery.phase1_localnetworkdiscovery import run_phase1
from scanner.network.interface_selector import select_best_interfaces
from scanner.provenance.snapshot_formatter import build_snapshot
from scanner.provenance.graph_builder import GraphBuilder
from scanner.provenance.neo4j_push import Neo4jConnector
from dotenv import load_dotenv
from utils import save_results
from utils import save_results

import os

if __name__ == "__main__":

    all_results = {}

    # -----------------------
    # PHASE 0 — SELF DISCOVERY
    # -----------------------
    print("\n=== Running Phase 0: Self-Discovery ===")
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

        # Add interface to list of scanned interfaces
        all_phase1["interfaces_scanned"].append({
            "interface": name,
            "ip": ip,
            "netmask": netmask,
            "score": iface["score"],
            "reason": iface["reason"]
        })

        # Save per-interface results (in memory)
        all_phase1["results"][name] = phase1_result

        # Aggregate global data
        for h in phase1_result["discovered_hosts"]:
            unique_hosts.add(h)

        networks_discovered.add(phase1_result["network"])

    # -----------------------
    # BUILD OVERALL SUMMARY
    # -----------------------
    all_phase1["overall_summary"] = {
        "total_interfaces_scanned": len(all_phase1["interfaces_scanned"]),
        "total_unique_hosts": len(unique_hosts),
        "unique_hosts": sorted(unique_hosts),
        "networks_discovered": sorted(networks_discovered)
    }

    # Add to global results
    all_results["phase1"] = all_phase1

    # Save Phase 1 as ONE file
    save_results(all_phase1, label="phase1")


    snapshot = build_snapshot(all_results)
    # -----------------------
    # GRAPH BUILDING
    # -----------------------
    # import json
    #
    # snapshot_file ="testing/data/snapshot_20251209_111238.json"
    #
    # with open(snapshot_file, "r", encoding="utf-8") as f:
    #     snapshot = json.load(f)
    #
    builder = GraphBuilder()
    G = builder.build(snapshot)

    load_dotenv()

    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")

    neo = Neo4jConnector(uri, user, password)
    neo.clear_database()
    neo.push_graph(G)
    neo.close()

    print("\n=== Discovery Completed ===")
