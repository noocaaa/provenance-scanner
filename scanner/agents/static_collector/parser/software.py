import winreg

def get_installed_software():
    software_list = []
    registry_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
    ]

    try:
        for hive, path in registry_paths:
            try:
                with winreg.OpenKey(hive, path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            sub = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, sub) as subkey:
                                try:
                                    name = winreg.QueryValueEx(subkey, 'DisplayName')[0]
                                    version = winreg.QueryValueEx(subkey, 'DisplayVersion')[0] if winreg.QueryValueEx(subkey, 'DisplayVersion') else 'N/A'
                                    publisher = winreg.QueryValueEx(subkey, 'Publisher')[0] if winreg.QueryValueEx(subkey, 'Publisher') else 'N/A'

                                    software_list.append({
                                        'name': name,
                                        'version': version,
                                        'publisher': publisher
                                    })
                                except FileNotFoundError:
                                    continue
                        except WindowsError:
                            continue
            except FileNotFoundError:
                continue

        # Remove duplicates
        seen = set()
        unique = []
        for s in software_list:
            key = (s['name'], s['version'])
            if key not in seen:
                seen.add(key)
                unique.append(s)

        return unique[:50]

    except Exception as e:
        print(f"[ERROR] Installed software: {e}")
        return []