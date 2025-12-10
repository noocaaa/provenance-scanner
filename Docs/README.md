# Provenance Scanner
A research project designed to collect **static and dynamic system information**, store it in **YAML format**, and generate a **Provenance Graph** for security analysis and future APT detection.

This project provides:
- A **Static Collector Agent** (processes, services, packages, filesystem metadata)
- A **Dynamic Collector Agent** (runtime events, syscalls, logs) — coming soon
- A **YAML-based data model**
- A foundation for building a **Provenance Graph Engine**
- A reproducible **Vagrant VM development environment**

---

## Project Structure
```
provenance-scanner/ 
│
├── agents/
│ ├── static_collector/
│ ├── dynamic_collector/
│ └── README.md
│
├── orchestrator/
├── data/
├── graphs/
├── ui/
├── scripts/
├── vagrant/
├── tests/
├── requirements.txt
└── README.md
```


## Quick Start (Local)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python agents/static_collector/static_collector.py
```

Output will be stored in:

```bash
data/output/static.yml
```

## Status

| Component         | Status        |
| ----------------- | ------------- |
| Static Collector  | ⏳ In progress   |
| Dynamic Collector | ⏳ Planned  |
| Provenance Engine | ⏳ Planned     |
| Web Visualization | ⏳ Planned     |

## Tech Stack

- Python 3.x
- PyYAML, psutil
- systemd for service enumeration
- Vagrant + VirtualBox for reproducible testing