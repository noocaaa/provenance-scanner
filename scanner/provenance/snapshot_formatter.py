"""
File: snapshot_formatter.py
Author: Noelia Carrasco Vilar
Date: 2025-12-09
Description:
    Converts Phase 0 + Phase 1 results into a hierarchical snapshot
    for visual and provenance-friendly graph building.
"""

import uuid
from datetime import datetime, timezone

NAT_CIDRS = {"10.0.2.0/24"}
NAT_GATEWAY_IPS = {"10.0.2.2"}

def is_nat_ip(ip: str) -> bool:
    return ip.startswith("10.0.2.")

def build_snapshot(all_results: dict) -> dict:
    """Normalize phase0 + phase1 into a single snapshot dict."""
    phase0 = all_results.get("phase0", {}) or {}
    phase1 = all_results.get("phase1", {}) or {}

    # --- Collapse NAT noise into a single infrastructure node ---

    nat_detected = False
    nat_gateway = None

    cleaned_phase1 = {
        "interfaces_scanned": phase1.get("interfaces_scanned", []),
        "results": {},
        "overall_summary": phase1.get("overall_summary", {}).copy(),
    }

    for iface, result in phase1.get("results", {}).items():
        network = result.get("network")

        # Skip pure NAT network results
        if network in NAT_CIDRS:
            nat_detected = True
            continue

        cleaned_hosts = []
        cleaned_details = {}

        for ip in result.get("discovered_hosts", []):
            if is_nat_ip(ip):
                nat_detected = True
                if ip in NAT_GATEWAY_IPS:
                    nat_gateway = ip
                continue

            cleaned_hosts.append(ip)
            cleaned_details[ip] = result.get("details", {}).get(ip, {})

        cleaned_phase1["results"][iface] = {
            **result,
            "discovered_hosts": cleaned_hosts,
            "details": cleaned_details,
        }
    snapshot = {
        "snapshot_id": str(uuid.uuid4()),
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "scanner_host": {
            "hostname": phase0.get("hostname"),
            "domain": phase0.get("domain"),
            "network": phase0.get("network", {}),
            "interfaces": phase0.get("interfaces", []),
            "active_connections": phase0.get("active_connections", []),
            "arp_cache_raw": phase0.get("arp_cache_raw"),
        },
        "local_network_discovery": cleaned_phase1,
        "infrastructure": {
            "nat": {
                "present": nat_detected,
                "cidr": "10.0.2.0/24" if nat_detected else None,
                "gateway": nat_gateway,
                "type": "virtualbox_nat",
                "role": "egress",
            }
        } if nat_detected else {},
    }

    return snapshot