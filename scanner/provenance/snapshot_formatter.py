"""
File: snapshot_formatter.py
Author: Noelia Carrasco Vilar
Date: 2025-12-09
Description:
    Converts Phase 0 + Phase 1 results into a hierarchical snapshot
    for visual and provenance-friendly graph building.
"""

# scanner/provenance/snapshot_formatter.py
import uuid
from datetime import datetime, timezone

def build_snapshot(all_results: dict) -> dict:
    """Normalize phase0 + phase1 into a single snapshot dict."""
    phase0 = all_results.get("phase0", {}) or {}
    phase1 = all_results.get("phase1", {}) or {}

    snapshot = {
        "snapshot_id": str(uuid.uuid4()),
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "scanner_host": {
            "hostname": phase0.get("hostname"),
            "domain": phase0.get("domain"),
            "network": phase0.get("network", {}),
            "interfaces": phase0.get("interfaces", []),
            "active_connections": phase0.get("active_connections", []),
            # keep raw ARP if you want it for provenance/debug
            "arp_cache_raw": phase0.get("arp_cache_raw"),
        },
        "local_network_discovery": phase1,
    }

    return snapshot