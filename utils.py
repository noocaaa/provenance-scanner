"""
File: utils.py
Author: Noelia Carrasco Vilar
Date: 2025-12-08
Description:
    Utils file
"""

import os
import json
import yaml
from datetime import datetime
from scanner.discovery.phase0_selfdiscovery import run_phase0

def save_phase0_results(results):
    """Save Phase 0 results to JSON and YAML files."""
    
    print(results)

    # Create output directory
    output_dir = os.path.join("testing", "data")
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save to JSON
    json_file = os.path.join(output_dir, f"phase0_{timestamp}.json")
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    # Save to YAML
    yaml_file = os.path.join(output_dir, f"phase0_{timestamp}.yml")
    with open(yaml_file, 'w') as f:
        yaml.dump(results, f, default_flow_style=False)
    
    print(f"[+] Results saved to:")
    print(f"    JSON: {json_file}")
    print(f"    YAML: {yaml_file}")
    
    return json_file, yaml_file