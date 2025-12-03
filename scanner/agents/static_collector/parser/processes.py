import psutil

def get_processes_categorized():
    processes = {
        'system_core': [],
        'user_applications': [],
        'background': []
    }

    try:
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cmdline']):
            try:
                info = proc.info
                p = {
                    'pid': info['pid'],
                    'name': info['name'],
                    'user': info['username'],
                    'cmd': ' '.join(info['cmdline']) if info['cmdline'] else None
                }

                username = info['username'] or ''

                if not username or 'SYSTEM' in username or 'AUTHORITY' in username:
                    processes['system_core'].append(p)
                elif info['cmdline']:
                    processes['user_applications'].append(p)
                else:
                    processes['background'].append(p)

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    except Exception as e:
        print(f"[ERROR] Processes: {e}")

    return processes