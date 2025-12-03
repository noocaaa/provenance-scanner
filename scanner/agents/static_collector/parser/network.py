import psutil
import socket
import subprocess
import re
from collections import defaultdict

def get_network_info():
    network_info = {
        'interfaces': {},
        'connections_summary': {},
        'detailed_connections': [],
        'dns_servers': []
    }

    try:
        # 1. INTERFACES DE RED (igual que antes)
        for iface, addrs in psutil.net_if_addrs().items():
            ipv4_list = []
            for a in addrs:
                if a.family == socket.AF_INET:
                    ipv4_list.append({
                        'address': a.address,
                        'netmask': a.netmask,
                        'broadcast': a.broadcast
                    })

            if ipv4_list:
                network_info['interfaces'][iface] = ipv4_list

        # 2. CONEXIONES - RESUMEN POR PROCESO
        process_connections = defaultdict(list)
        
        for conn in psutil.net_connections(kind='inet'):
            if conn.status in ['ESTABLISHED', 'LISTEN'] and conn.laddr:
                try:
                    process_name = "Unknown"
                    process_cmdline = ""
                    
                    if conn.pid:
                        process = psutil.Process(conn.pid)
                        process_name = process.name()
                        process_cmdline = ' '.join(process.cmdline()) if process.cmdline() else ""
                    
                    conn_info = {
                        'protocol': 'TCP' if conn.type == 1 else 'UDP',
                        'local_address': f"{conn.laddr.ip}:{conn.laddr.port}",
                        'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                        'status': conn.status,
                        'pid': conn.pid
                    }
                    
                    # Agrupar por proceso para el resumen
                    process_connections[process_name].append(conn_info)
                    
                    # Guardar conexión detallada
                    detailed_conn = conn_info.copy()
                    detailed_conn['process_name'] = process_name
                    detailed_conn['process_cmdline'] = process_cmdline
                    network_info['detailed_connections'].append(detailed_conn)
                    
                except Exception as e:
                    print(f"[WARN] Could not process connection for PID {conn.pid}: {e}")

        # 3. CREAR RESUMEN ORGANIZADO
        connections_summary = {}
        for process_name, connections in process_connections.items():
            connections_summary[process_name] = {
                'total_connections': len(connections),
                'listening_ports': [],
                'established_connections': [],
                'pid': connections[0]['pid'] if connections else None
            }
            
            for conn in connections:
                if conn['status'] == 'LISTEN':
                    connections_summary[process_name]['listening_ports'].append({
                        'address': conn['local_address'],
                        'protocol': conn['protocol']
                    })
                elif conn['status'] == 'ESTABLISHED':
                    connections_summary[process_name]['established_connections'].append({
                        'local': conn['local_address'],
                        'remote': conn['remote_address'],
                        'protocol': conn['protocol']
                    })
        
        network_info['connections_summary'] = dict(connections_summary)

        # 4. DNS SERVERS (mejor captura)
        dns_servers = []
        try:
            if psutil.WINDOWS:
                result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
                
                current_interface = ""
                for line in result.stdout.split('\n'):
                    line = line.strip()
                    
                    # Detectar interfaz
                    if line.endswith(':') and 'adapter' not in line.lower():
                        current_interface = line.replace(':', '')
                    
                    # Buscar DNS para la interfaz actual (solo Wi-Fi/Ethernet)
                    if current_interface and ('DNS Servers' in line or 'Servidores DNS' in line):
                        ip_matches = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)
                        for ip in ip_matches:
                            if ip not in dns_servers and not ip.startswith('169.254'):  # Filtrar IPs link-local
                                dns_servers.append({
                                    'server': ip,
                                    'interface': current_interface
                                })
                
        except Exception as e:
            print(f"[WARN] Could not get DNS servers: {e}")
        
        network_info['dns_servers'] = dns_servers

        # 5. INFORMACIÓN ADICIONAL ÚTIL
        network_info['statistics'] = {
            'total_interfaces': len(network_info['interfaces']),
            'total_connections': len(network_info['detailed_connections']),
            'total_processes_with_connections': len(network_info['connections_summary']),
            'established_count': len([c for c in network_info['detailed_connections'] if c['status'] == 'ESTABLISHED']),
            'listening_count': len([c for c in network_info['detailed_connections'] if c['status'] == 'LISTEN'])
        }

    except Exception as e:
        print(f"[ERROR] Network info: {e}")

    return network_info