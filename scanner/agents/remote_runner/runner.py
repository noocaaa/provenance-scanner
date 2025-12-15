"""
File: runner.py
Author: Noelia Carrasco Vilar
Date: 2025-12-14
Description:
    Runs all extractors locally on the remote node.
"""

from typing import Dict, Any

from scanner.agents.extractors import (
    os_extractor,
    hardware_extractor,
    network_extractor,
    users_extractor,
    packages_extractor,
    services_extractor,
)

EXTRACTOR_ORDER = [
    ("os", os_extractor),
    ("hardware", hardware_extractor),
    ("network", network_extractor),
    ("users", users_extractor),
    ("packages", packages_extractor),
    ("services", services_extractor),
]


def run_all() -> Dict[str, Any]:
    results: Dict[str, Any] = {}

    for name, extractor in EXTRACTOR_ORDER:
        try:
            results[name] = extractor.extract()
        except Exception as e:
            results[name] = {
                "error": str(e),
                "extractor": name,
            }

    return results
