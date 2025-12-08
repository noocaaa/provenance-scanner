# Testing Environment Setup

## Overview
This testing environment provides a controlled lab for network security testing and reconnaissance exercises using Vagrant virtual machines.

## Prerequisites

### Required Software

- Vagrant (2.2.0 or later)
- VirtualBox (6.0 or later) or VMware Workstation/Fusion
- Git (for cloning the repository)

### System Requirements

- Minimum 8GB RAM (16GB recommended)
- 20GB free disk space
- Virtualization enabled in BIOS

## Quick Start

1. Clone and Setup
2. Access the Lab Environment

``` bash 
# SSH into a specific machine
vagrant ssh linux1

# Or access all machines
vagrant ssh linux1
vagrant ssh linux2
vagrant ssh printer
# ...etc
```
3. Stop/Cleanup

```bash
# Suspend VMs (save state)
vagrant suspend

# Halt VMs (shutdown)
vagrant halt

# Destroy VMs (delete)
vagrant destroy -f
```