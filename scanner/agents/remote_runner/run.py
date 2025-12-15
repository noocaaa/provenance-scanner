"""
File: run.py
Author: Noelia Carrasco Vilar
Date: 2025-12-14
Description:
    Entrypoint executed on the remote node.
"""

import json
import yaml
from  scanner.agents.remote_runner.runner import run_all

def main():
    data = run_all()

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("output.yml", "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f)

if __name__ == "__main__":
    main()