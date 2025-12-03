import yaml

def save_yaml(data, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, indent=2)
        print(f"[OK] Saved YAML → {filename}")
    except Exception as e:
        print(f"[ERROR] Saving YAML: {e}")
