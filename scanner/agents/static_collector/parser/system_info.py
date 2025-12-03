import psutil
import platform
import socket
from datetime import datetime

def get_system_info():
    try:
        return {
            'hostname': socket.gethostname(),
            'os': {
                'system': platform.system(),
                'version': platform.version(),
                'release': platform.release(),
                'architecture': platform.architecture()[0],
                'machine': platform.machine()
            },
            'processor': {
                'name': platform.processor(),
                'cores': psutil.cpu_count(logical=False),
                'logical_cores': psutil.cpu_count(logical=True)
            },
            'memory': {
                'total_gb': round(psutil.virtual_memory().total / (1024**3), 2),
                'available_gb': round(psutil.virtual_memory().available / (1024**3), 2)
            },
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        print(f"[ERROR] System info: {e}")
        return {}
