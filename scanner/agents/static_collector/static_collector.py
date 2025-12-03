from scanner.agents.static_collector.parser.system_info import get_system_info
from scanner.agents.static_collector.parser.processes import get_processes_categorized
from scanner.agents.static_collector.parser.software import get_installed_software
from scanner.agents.static_collector.parser.network import get_network_info
from scanner.agents.static_collector.parser.services import get_running_services
from scanner.agents.static_collector.exporter.yaml_exporter import save_yaml

import os

class StaticCollector:
    def __init__(self):
        self.data = {
            'static': {
                'system_info': {},
                'processes': {},
                'installed_software': [],
                'network_info': {},
                'users': [],
                'services': []
            }
        }

    def collect_network(self):
        print("[+] Collecting all network info...")
        self.data['static']['network_info'] = get_network_info()

    def collect_all(self):
        print("[+] Collecting system info...")
        self.data['static']['system_info'] = get_system_info()

        print("[+] Collecting processes...")
        self.data['static']['processes'] = get_processes_categorized()

        print("[+] Collecting installed software...")
        self.data['static']['installed_software'] = get_installed_software()

        print("[+] Collecting network info...")
        self.data['static']['network_info'] = get_network_info()

        print("[+] Collecting running services...")
        self.data['static']['services'] = get_running_services()

        return self.data

    def save_to_yaml(self, filename="static_file.yml"):
        output_dir = "scanner/data/output"
        os.makedirs(output_dir, exist_ok=True)
        full_path = os.path.join(output_dir, filename)
        save_yaml(self.data, full_path)
