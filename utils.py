"""
File: utils.py
Author: Noelia Carrasco Vilar
Date: 2025-12-08
Description:
    Utils file with general save function for any dict.
"""

import os
import json
import yaml
from datetime import datetime

def save_results(results: dict, label: str = "data", output_dir: str = "testing/data"):
    """
    Save any dictionary to JSON and YAML files.
    
    Args:
        results (dict): The dictionary to save.
        label (str): Label to prefix the filename (default 'data').
        output_dir (str): Directory to save files (default 'testing/data').
    
    Returns:
        Tuple[str, str]: Paths to the JSON and YAML files.
    """
    
    if not isinstance(results, dict):
        raise ValueError("Results must be a dictionary")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save JSON
    json_file = os.path.join(output_dir, f"{label}_{timestamp}.json")
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    # Save YAML
    yaml_file = os.path.join(output_dir, f"{label}_{timestamp}.yml")
    with open(yaml_file, 'w') as f:
        yaml.dump(results, f, default_flow_style=False)
    
    print(f"[+] Results saved to:")
    print(f"    JSON: {json_file}")
    print(f"    YAML: {yaml_file}")
    
    return json_file, yaml_file
