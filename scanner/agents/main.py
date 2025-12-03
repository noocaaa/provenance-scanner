import sys, os
from scanner.agents.static_collector.static_collector import StaticCollector

def main():
    collector = StaticCollector()
    data = collector.collect_network()
    collector.save_to_yaml("static_network.yml")

    print("\n=== SUMMARY ===")
    print(f"Hostname: {data['static']['system_info'].get('hostname', 'N/A')}")
    print(f"OS: {data['static']['system_info']['os'].get('system')}")
    print(f"System processes: {len(data['static']['processes']['system_core'])}")
    print(f"User processes: {len(data['static']['processes']['user_applications'])}")
    print(f"Installed software: {len(data['static']['installed_software'])}")
    print(f"Running services: {len(data['static']['services'])}")


if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

    main()

