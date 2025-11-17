# Detailed Work Plan (4 Weeks)

## Week 1 — Design and Technical Basis

### Objective

Ensure that the architecture, data format, and agents are fully defined.

### Tasks

1. Define all system components:
    - Orchestrator
    - Static Analyzer Agent
    - Dynamic Monitor Agent
    - Data Store (YAML)
    - Provenance Engine
    - Visualizer

2. Define the YML schema

3. Decide on technologies:
    - Python for agents
    - gRPC or REST for communication
    - NetworkX or Neo4j for provenance
    - D3.js for visualization

4. Mock data for testing the pipeline.

## Week 2 - Implementation of Scanners

### Objective

Ensure your agents collect real data.

### Tasks

1. Static Analyzer Agent
    - Enumerate processes
    - Enumerate services
    - File inventory
    - Dependencies, packages, users

2. Dynamic Monitor Agent
    - Capture syscalls (eBPF if Linux)
    - Real-time logs (journalctl, auditd)
    - Process activity
    - Network connections

3. Define structured output format:
    - static.yml
    - dynamic.yml

4. API to send data to the Orchestrator.

## Week 3 - Provenance Engine

### Objective

Convert the data into a navigable graph.

### Tasks

1. Parser for ingesting .yml files.

2. Normalization:
    - nodes: process, file, connection, user.
    - edges: read, write, execute, spawn, connect.

3. Graph construction:

    - NetworkX (fast for prototyping).
    - Exporter to JSON format for UI

4. Basic rules:

    - “process X modified file Y”
    - “process A generated process B”

5. Mock viewer to validate nodes and edges.

## Week 4 — Visualization + Total Integration

### Objective

Have a working prototype that goes through the entire pipeline.

### Tasks

1. Web UI with:
    - Node view
    - Edge view
    - Filters (time, node type)
    - Zoom + highlight paths

2. Integration:
    - Agents → Orchestrator → YAML Store → Graph Engine → UI

3. Write documentation:
    - Architecture
    - YAML schema
    - Installation steps
    - Examples of generated graphs