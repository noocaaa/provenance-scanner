"""
File: run.py
Author: Noelia Carrasco Vilar
Date: 2025-12-14
Description:
    Entrypoint executed on the remote node.
"""

import json
import yaml
import sys
from pathlib import Path
from scanner.agents.remote_runner.runner import run_all


def main():
    data = run_all()

    base_dir = Path(sys.executable).parent
    json_path = base_dir / "output.json"
    yaml_path = base_dir / "output.yml"

    json_path.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8"
    )

    yaml_path.write_text(
        yaml.safe_dump(data),
        encoding="utf-8"
    )

if __name__ == "__main__":
    main()
