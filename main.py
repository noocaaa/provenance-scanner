"""
File: main.py
Author: Noelia Carrasco Vilar
Date: 2025-12-07
Description:
    Entrypoint to execute the discovery phase.
"""

from scanner.discovery.phase0_selfdiscovery import run_phase0
from utils import save_phase0_results

if __name__ == "__main__":
    results = run_phase0()
    save_phase0_results(results)
    