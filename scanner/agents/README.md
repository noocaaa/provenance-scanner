# Agents

This folder contains all system collectors used by the Provenance Scanner.

## Static Collector
Located at: ``agents/static_collector/``

The static collector gathers:
- Running processes (via psutil)
- Systemd services
- Installed packages (dpkg on Ubuntu)
- OS metadata
- Hostname, OS type

Output is written to: ``data/output/static.yml``


Run manually:

```bash
python agents/static_collector/static_collector.py
```

## Dynamic Collector

Will capture:

- Syscalls (via eBPF)
- Log activity
- Process creation events
- File modifications
- Network connections

This will later feed the Provenance Graph Engine.

## Architecture

Each agent has:

- ``/parser`` → functions to extract raw data
- ``/exporter`` → YAML/JSON exporters
- ``/utils`` → helpers for system commands
- ``*_collector.py `` → main entrypoint

### Core dependencies for the Provenance Scanner project
- pytest==8.1.0
- psutil==5.9.8
- PyYAML==6.0.2