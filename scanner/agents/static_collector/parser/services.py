import psutil

def get_running_services():
    services = []

    try:
        for service in psutil.win_service_iter():
            if service.status() == 'running':
                services.append({
                    'name': service.name(),
                    'display_name': service.display_name(),
                    'status': service.status(),
                    'pid': service.pid() if service.pid() else 'N/A'
                })

    except Exception as e:
        print(f"[ERROR] Services: {e}")

    return services
