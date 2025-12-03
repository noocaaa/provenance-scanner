"""
Initial data for Provenance Scanner Dashboard
Contains all items from the Distributed System Data Collection Specification
"""

def get_full_initial_data():
    """Retorna todos los datos iniciales basados en la especificación completa"""
    
    categories = []
    
    # ===== 1) ASSET INVENTORY (STATIC) =====
    categories.extend([
        # Asset Identity
        {"Category": "Asset Inventory", "Subcategory": "Asset Identity", "Item": "Hostname", 
         "Description": "Hostname of the asset", "Type": "Static", "Priority": "High", "Risk Level": "Low"},
        {"Category": "Asset Inventory", "Subcategory": "Asset Identity", "Item": "IP addresses", 
         "Description": "IP address(es) and network range(s)", "Type": "Static", "Priority": "High", "Risk Level": "Medium"},
        {"Category": "Asset Inventory", "Subcategory": "Asset Identity", "Item": "OS + version", 
         "Description": "Operating system and version", "Type": "Static", "Priority": "High", "Risk Level": "Medium"},
        {"Category": "Asset Inventory", "Subcategory": "Asset Identity", "Item": "Location", 
         "Description": "Location (on-premises, cloud, hybrid)", "Type": "Static", "Priority": "Medium", "Risk Level": "Low"},
        {"Category": "Asset Inventory", "Subcategory": "Asset Identity", "Item": "Role", 
         "Description": "Role (app server, DB, proxy, firewall, NAS, printer, etc.)", "Type": "Static", "Priority": "High", "Risk Level": "Medium"},
        
        # Hardware Specifications
        {"Category": "Asset Inventory", "Subcategory": "Hardware Specifications", "Item": "CPU specifications", 
         "Description": "CPU specifications", "Type": "Static", "Priority": "Medium", "Risk Level": "Low"},
        {"Category": "Asset Inventory", "Subcategory": "Hardware Specifications", "Item": "RAM specifications", 
         "Description": "RAM specifications", "Type": "Static", "Priority": "Medium", "Risk Level": "Low"},
        {"Category": "Asset Inventory", "Subcategory": "Hardware Specifications", "Item": "Storage specifications", 
         "Description": "Storage specifications", "Type": "Static", "Priority": "Medium", "Risk Level": "Low"},
        {"Category": "Asset Inventory", "Subcategory": "Hardware Specifications", "Item": "Server/device model", 
         "Description": "Server/device model", "Type": "Static", "Priority": "Low", "Risk Level": "Low"},
        {"Category": "Asset Inventory", "Subcategory": "Hardware Specifications", "Item": "Virtual or physical", 
         "Description": "Virtual or physical deployment", "Type": "Static", "Priority": "Medium", "Risk Level": "Low"},
        {"Category": "Asset Inventory", "Subcategory": "Hardware Specifications", "Item": "Hypervisor", 
         "Description": "Hypervisor (if applicable)", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        
        # Installed Software
        {"Category": "Asset Inventory", "Subcategory": "Installed Software", "Item": "List of packages/programs", 
         "Description": "List of packages/programs", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Asset Inventory", "Subcategory": "Installed Software", "Item": "Exact versions", 
         "Description": "Exact versions of software", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Asset Inventory", "Subcategory": "Installed Software", "Item": "Known dependencies", 
         "Description": "Known dependencies between software", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Asset Inventory", "Subcategory": "Installed Software", "Item": "Firmware", 
         "Description": "Firmware (for printers, routers, firewalls)", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        
        # Exposed Services
        {"Category": "Asset Inventory", "Subcategory": "Exposed Services", "Item": "Open ports", 
         "Description": "Open ports on the asset", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Asset Inventory", "Subcategory": "Exposed Services", "Item": "Used protocols", 
         "Description": "Used protocols on open ports", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Asset Inventory", "Subcategory": "Exposed Services", "Item": "Active services and versions", 
         "Description": "Active services and their versions", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        
        # Additional Considerations
        {"Category": "Asset Inventory", "Subcategory": "Additional Considerations", "Item": "Interdependencies between assets", 
         "Description": "Interdependencies between assets (e.g., app server → database server)", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Asset Inventory", "Subcategory": "Additional Considerations", "Item": "Asset lifecycle tracking", 
         "Description": "Asset lifecycle tracking (decommissioned or upgraded assets)", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
    ])
    
    # ===== 2) SYSTEM CONFIGURATION (STATIC) =====
    categories.extend([
        # OS Configuration
        {"Category": "System Configuration", "Subcategory": "OS Configuration", "Item": "Authentication policies", 
         "Description": "Authentication policies", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "System Configuration", "Subcategory": "OS Configuration", "Item": "Local firewall configuration", 
         "Description": "Local firewall configuration", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "System Configuration", "Subcategory": "OS Configuration", "Item": "Enabled/disabled services", 
         "Description": "Enabled/disabled services", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "System Configuration", "Subcategory": "OS Configuration", "Item": "Auto-start programs", 
         "Description": "Auto-start programs", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        
        # User Management
        {"Category": "System Configuration", "Subcategory": "User Management", "Item": "Local users", 
         "Description": "Local users on the system", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "System Configuration", "Subcategory": "User Management", "Item": "User groups", 
         "Description": "User groups", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "System Configuration", "Subcategory": "User Management", "Item": "Permissions per user", 
         "Description": "Permissions per user", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "System Configuration", "Subcategory": "User Management", "Item": "Admin roles", 
         "Description": "Admin roles", "Type": "Static", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "System Configuration", "Subcategory": "User Management", "Item": "SSH keys", 
         "Description": "SSH keys", "Type": "Static", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "System Configuration", "Subcategory": "User Management", "Item": "Password policies", 
         "Description": "Password policies", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        
        # Sensitive Files
        {"Category": "System Configuration", "Subcategory": "Sensitive Files", "Item": "Critical paths", 
         "Description": "Critical paths (/etc, logs, config files)", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "System Configuration", "Subcategory": "Sensitive Files", "Item": "Folder permissions", 
         "Description": "Folder permissions", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "System Configuration", "Subcategory": "Sensitive Files", "Item": "Server configs", 
         "Description": "Server configs (nginx.conf, my.cnf, etc.)", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        
        # Security Controls
        {"Category": "System Configuration", "Subcategory": "Security Controls", "Item": "Security patches and updates", 
         "Description": "Security patches and updates (focus on pending patches)", "Type": "Static", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "System Configuration", "Subcategory": "Security Controls", "Item": "Critical patches", 
         "Description": "Critical patches (zero-day vulnerabilities)", "Type": "Static", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "System Configuration", "Subcategory": "Security Controls", "Item": "System hardening", 
         "Description": "System hardening (baseline security configurations)", "Type": "Static", "Priority": "High", "Risk Level": "High"},
    ])
    
    # ===== 3) NETWORK ARCHITECTURE (STATIC + DYNAMIC) =====
    categories.extend([
        # Topology
        {"Category": "Network Architecture", "Subcategory": "Topology", "Item": "Subnets", 
         "Description": "Subnets", "Type": "Static", "Priority": "High", "Risk Level": "Medium"},
        {"Category": "Network Architecture", "Subcategory": "Topology", "Item": "VLANs", 
         "Description": "VLANs", "Type": "Static", "Priority": "High", "Risk Level": "Medium"},
        {"Category": "Network Architecture", "Subcategory": "Topology", "Item": "Gateways", 
         "Description": "Gateways", "Type": "Static", "Priority": "High", "Risk Level": "Medium"},
        {"Category": "Network Architecture", "Subcategory": "Topology", "Item": "Routers and switches", 
         "Description": "Routers and switches", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Network Architecture", "Subcategory": "Topology", "Item": "NAT/PAT configurations", 
         "Description": "NAT/PAT configurations", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Network Architecture", "Subcategory": "Topology", "Item": "Security zones", 
         "Description": "Security zones (DMZ, internal, guest, IoT)", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        
        # Firewalls
        {"Category": "Network Architecture", "Subcategory": "Firewalls", "Item": "Firewall rules", 
         "Description": "Rules (source, destination, protocol, action)", "Type": "Static+Dynamic", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "Network Architecture", "Subcategory": "Firewalls", "Item": "Policies by zone", 
         "Description": "Policies by zone", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Network Architecture", "Subcategory": "Firewalls", "Item": "Active inspections", 
         "Description": "Active inspections (IPS/IDS, WAF)", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
        
        # Communications
        {"Category": "Network Architecture", "Subcategory": "Communications", "Item": "Traffic flows", 
         "Description": "Traffic flows between services (app → DB, app → cache, etc.)", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
        {"Category": "Network Architecture", "Subcategory": "Communications", "Item": "Used protocols", 
         "Description": "Used protocols (HTTP, gRPC, SSH, SMB)", "Type": "Dynamic", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Network Architecture", "Subcategory": "Communications", "Item": "Relevant ports", 
         "Description": "Relevant ports", "Type": "Static+Dynamic", "Priority": "High", "Risk Level": "High"},
        {"Category": "Network Architecture", "Subcategory": "Communications", "Item": "Latencies", 
         "Description": "Latencies (optional)", "Type": "Dynamic", "Priority": "Low", "Risk Level": "Low"},
        
        # Security Monitoring
        {"Category": "Network Architecture", "Subcategory": "Security Monitoring", "Item": "Intrusion detection/prevention systems", 
         "Description": "Intrusion detection/prevention systems (IDS/IPS)", "Type": "Dynamic", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "Network Architecture", "Subcategory": "Security Monitoring", "Item": "Anomalous traffic monitoring", 
         "Description": "Anomalous traffic monitoring", "Type": "Dynamic", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "Network Architecture", "Subcategory": "Security Monitoring", "Item": "Lateral movement detection", 
         "Description": "Lateral movement detection", "Type": "Dynamic", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "Network Architecture", "Subcategory": "Security Monitoring", "Item": "Data exfiltration pattern detection", 
         "Description": "Data exfiltration pattern detection", "Type": "Dynamic", "Priority": "Critical", "Risk Level": "Critical"},
    ])
    
    # ===== 4) APPLICATIONS AND SERVICES (STATIC + DYNAMIC) =====
    categories.extend([
        # Basic Information
        {"Category": "Applications and Services", "Subcategory": "Basic Information", "Item": "Service name", 
         "Description": "Service name", "Type": "Static", "Priority": "High", "Risk Level": "Medium"},
        {"Category": "Applications and Services", "Subcategory": "Basic Information", "Item": "Function", 
         "Description": "Function", "Type": "Static", "Priority": "Medium", "Risk Level": "Low"},
        {"Category": "Applications and Services", "Subcategory": "Basic Information", "Item": "Internal and external dependencies", 
         "Description": "Internal and external dependencies", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        
        # Exposed Endpoints
        {"Category": "Applications and Services", "Subcategory": "Exposed Endpoints", "Item": "URLs/routes", 
         "Description": "URLs/routes", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Applications and Services", "Subcategory": "Exposed Endpoints", "Item": "API types", 
         "Description": "API types (REST, SOAP, GraphQL)", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Applications and Services", "Subcategory": "Exposed Endpoints", "Item": "Versioning", 
         "Description": "Versioning (v1, v2)", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        
        # Configuration
        {"Category": "Applications and Services", "Subcategory": "Configuration", "Item": "Environment variables", 
         "Description": "Environment variables", "Type": "Static", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "Applications and Services", "Subcategory": "Configuration", "Item": ".env files", 
         "Description": ".env files", "Type": "Static", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "Applications and Services", "Subcategory": "Configuration", "Item": "Deployment parameters", 
         "Description": "Deployment parameters", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Applications and Services", "Subcategory": "Configuration", "Item": "Log configurations", 
         "Description": "Log configurations", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Applications and Services", "Subcategory": "Configuration", "Item": "Cache/session configurations", 
         "Description": "Cache/session configurations", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        
        # Containers and Orchestration
        {"Category": "Applications and Services", "Subcategory": "Containers and Orchestration", "Item": "Images and versions", 
         "Description": "Images and versions", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Applications and Services", "Subcategory": "Containers and Orchestration", "Item": "Volumes", 
         "Description": "Volumes", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Applications and Services", "Subcategory": "Containers and Orchestration", "Item": "Secrets and configmaps", 
         "Description": "Secrets and configmaps", "Type": "Static", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "Applications and Services", "Subcategory": "Containers and Orchestration", "Item": "Pods, deployments, services", 
         "Description": "Pods, deployments, services (Kubernetes)", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        
        # Security Enhancements
        {"Category": "Applications and Services", "Subcategory": "Security Enhancements", "Item": "Access control policies", 
         "Description": "Access control policies", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Applications and Services", "Subcategory": "Security Enhancements", "Item": "Third-party services", 
         "Description": "Third-party services (OAuth providers, API integrations)", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
    ])
    
    # ===== 5) DATABASES (STATIC + DYNAMIC) =====
    categories.extend([
        # DB Identity
        {"Category": "Databases", "Subcategory": "DB Identity", "Item": "Type", 
         "Description": "Type (MySQL, PostgreSQL, MongoDB, etc.)", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Databases", "Subcategory": "DB Identity", "Item": "Version", 
         "Description": "Version", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Databases", "Subcategory": "DB Identity", "Item": "Host and port", 
         "Description": "Host and port", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        
        # Configuration
        {"Category": "Databases", "Subcategory": "Configuration", "Item": "Users and roles", 
         "Description": "Users and roles", "Type": "Static", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "Databases", "Subcategory": "Configuration", "Item": "Permissions per database", 
         "Description": "Permissions per database", "Type": "Static", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "Databases", "Subcategory": "Configuration", "Item": "Password policies", 
         "Description": "Password policies", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Databases", "Subcategory": "Configuration", "Item": "Encryption in transit and at rest", 
         "Description": "Encryption in transit and at rest", "Type": "Static", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "Databases", "Subcategory": "Configuration", "Item": "Critical configs", 
         "Description": "Critical configs (max_connections, replica settings)", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        
        # Dynamic Data
        {"Category": "Databases", "Subcategory": "Dynamic Data", "Item": "Active connections", 
         "Description": "Active connections", "Type": "Dynamic", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Databases", "Subcategory": "Dynamic Data", "Item": "Slow queries/logs", 
         "Description": "Slow queries/logs", "Type": "Dynamic", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Databases", "Subcategory": "Dynamic Data", "Item": "Replication/lag status", 
         "Description": "Replication/lag status", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
        {"Category": "Databases", "Subcategory": "Dynamic Data", "Item": "Backup configurations and periodicity", 
         "Description": "Backup configurations and periodicity", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        
        # Security Auditing
        {"Category": "Databases", "Subcategory": "Security Auditing", "Item": "Database audit information", 
         "Description": "Database audit information", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
        {"Category": "Databases", "Subcategory": "Security Auditing", "Item": "Encryption details", 
         "Description": "Encryption details", "Type": "Static", "Priority": "Critical", "Risk Level": "Critical"},
    ])
    
    # ===== 6) SECURITY AND ACCESS (STATIC + DYNAMIC) =====
    categories.extend([
        # Authentication
        {"Category": "Security and Access", "Subcategory": "Authentication", "Item": "Authentication systems", 
         "Description": "Authentication systems (LDAP, AD, OAuth, JWT, SSO)", "Type": "Static", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "Security and Access", "Subcategory": "Authentication", "Item": "Token expiration rules", 
         "Description": "Token expiration rules", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Security and Access", "Subcategory": "Authentication", "Item": "SSH key management", 
         "Description": "SSH key management / API keys", "Type": "Static+Dynamic", "Priority": "Critical", "Risk Level": "Critical"},
        
        # Encryption
        {"Category": "Security and Access", "Subcategory": "Encryption", "Item": "TLS certificates", 
         "Description": "TLS certificates", "Type": "Static", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "Security and Access", "Subcategory": "Encryption", "Item": "Supported TLS/SSL versions", 
         "Description": "Supported TLS/SSL versions", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Security and Access", "Subcategory": "Encryption", "Item": "Cipher suites", 
         "Description": "Cipher suites", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Security and Access", "Subcategory": "Encryption", "Item": "Expired or soon-to-expire certificates", 
         "Description": "Expired or soon-to-expire certificates", "Type": "Dynamic", "Priority": "Critical", "Risk Level": "Critical"},
        
        # Logs
        {"Category": "Security and Access", "Subcategory": "Logs", "Item": "Types of logs", 
         "Description": "Types of logs", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Security and Access", "Subcategory": "Logs", "Item": "Storage locations", 
         "Description": "Storage locations", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Security and Access", "Subcategory": "Logs", "Item": "Retention policies", 
         "Description": "Retention policies", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Security and Access", "Subcategory": "Logs", "Item": "Access controls", 
         "Description": "Access controls for logs", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        
        # Policies
        {"Category": "Security and Access", "Subcategory": "Policies", "Item": "MFA enabled/disabled status", 
         "Description": "MFA enabled/disabled status", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Security and Access", "Subcategory": "Policies", "Item": "Hardening policies", 
         "Description": "Hardening policies", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Security and Access", "Subcategory": "Policies", "Item": "Role-based access control", 
         "Description": "Role-based access control (RBAC)", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        
        # Advanced Security
        {"Category": "Security and Access", "Subcategory": "Advanced Security", "Item": "Privileged access management", 
         "Description": "Privileged access management (PAM)", "Type": "Static+Dynamic", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "Security and Access", "Subcategory": "Advanced Security", "Item": "Just-in-time access", 
         "Description": "Just-in-time access for sensitive systems", "Type": "Dynamic", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "Security and Access", "Subcategory": "Advanced Security", "Item": "Endpoint detection and response", 
         "Description": "Endpoint detection and response (EDR: CrowdStrike, Carbon Black)", "Type": "Dynamic", "Priority": "Critical", "Risk Level": "Critical"},
    ])
    
    # ===== 7) MONITORING AND METRICS (DYNAMIC) =====
    categories.extend([
        # System Health
        {"Category": "Monitoring and Metrics", "Subcategory": "System Health", "Item": "CPU usage", 
         "Description": "CPU, RAM, I/O usage", "Type": "Dynamic", "Priority": "High", "Risk Level": "Medium"},
        {"Category": "Monitoring and Metrics", "Subcategory": "System Health", "Item": "Network usage", 
         "Description": "Network usage", "Type": "Dynamic", "Priority": "Medium", "Risk Level": "Low"},
        {"Category": "Monitoring and Metrics", "Subcategory": "System Health", "Item": "Load average", 
         "Description": "Load average", "Type": "Dynamic", "Priority": "Medium", "Risk Level": "Medium"},
        
        # Service Status
        {"Category": "Monitoring and Metrics", "Subcategory": "Service Status", "Item": "Uptime", 
         "Description": "Uptime", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
        {"Category": "Monitoring and Metrics", "Subcategory": "Service Status", "Item": "Latency per service", 
         "Description": "Latency per service", "Type": "Dynamic", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Monitoring and Metrics", "Subcategory": "Service Status", "Item": "4xx/5xx errors", 
         "Description": "4xx/5xx errors (APIs)", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
        
        # Relevant Events
        {"Category": "Monitoring and Metrics", "Subcategory": "Relevant Events", "Item": "Retries", 
         "Description": "Retries", "Type": "Dynamic", "Priority": "Low", "Risk Level": "Low"},
        {"Category": "Monitoring and Metrics", "Subcategory": "Relevant Events", "Item": "Connection drops", 
         "Description": "Connection drops", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
        {"Category": "Monitoring and Metrics", "Subcategory": "Relevant Events", "Item": "APM alerts", 
         "Description": "APM alerts (Application Performance Monitoring)", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
        
        # Alerting and Response
        {"Category": "Monitoring and Metrics", "Subcategory": "Alerting and Response", "Item": "Alerting mechanisms", 
         "Description": "Alerting mechanisms", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Monitoring and Metrics", "Subcategory": "Alerting and Response", "Item": "Response plans", 
         "Description": "Response plans (CPU spikes, memory consumption)", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Monitoring and Metrics", "Subcategory": "Alerting and Response", "Item": "Anomalous logins detection", 
         "Description": "Anomalous logins detection", "Type": "Dynamic", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "Monitoring and Metrics", "Subcategory": "Alerting and Response", "Item": "Failed login attempts monitoring", 
         "Description": "Failed login attempts monitoring", "Type": "Dynamic", "Priority": "Critical", "Risk Level": "Critical"},
    ])
    
    # ===== 8) EXTERNAL DEPENDENCIES (STATIC + DYNAMIC) =====
    categories.extend([
        # External APIs
        {"Category": "External Dependencies", "Subcategory": "External APIs", "Item": "List of APIs", 
         "Description": "List of APIs", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "External Dependencies", "Subcategory": "External APIs", "Item": "Authentication types", 
         "Description": "Authentication types", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "External Dependencies", "Subcategory": "External APIs", "Item": "Frequency of use", 
         "Description": "Frequency of use", "Type": "Dynamic", "Priority": "Low", "Risk Level": "Low"},
        {"Category": "External Dependencies", "Subcategory": "External APIs", "Item": "Error rates", 
         "Description": "Error rates", "Type": "Dynamic", "Priority": "Medium", "Risk Level": "Medium"},
        
        # Cloud Services
        {"Category": "External Dependencies", "Subcategory": "Cloud Services", "Item": "Load balancers", 
         "Description": "Load balancers", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "External Dependencies", "Subcategory": "Cloud Services", "Item": "Storage buckets", 
         "Description": "Storage buckets", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "External Dependencies", "Subcategory": "Cloud Services", "Item": "Serverless functions", 
         "Description": "Serverless functions", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "External Dependencies", "Subcategory": "Cloud Services", "Item": "CDN services", 
         "Description": "CDN services", "Type": "Static", "Priority": "Low", "Risk Level": "Low"},
        
        # Risk Management
        {"Category": "External Dependencies", "Subcategory": "Risk Management", "Item": "Third-party risk tracking", 
         "Description": "Third-party risk tracking", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
        {"Category": "External Dependencies", "Subcategory": "Risk Management", "Item": "Vulnerability monitoring", 
         "Description": "Vulnerability monitoring for external APIs", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
    ])
    
    # ===== 9) SPECIAL DEVICES (E.G., PRINTERS) =====
    categories.extend([
        # Useful Data
        {"Category": "Special Devices", "Subcategory": "Useful Data", "Item": "Model and firmware", 
         "Description": "Model and firmware", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Special Devices", "Subcategory": "Useful Data", "Item": "Network configuration", 
         "Description": "Network configuration (IP, port)", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Special Devices", "Subcategory": "Useful Data", "Item": "Enabled protocols", 
         "Description": "Enabled protocols (IPP, LPD)", "Type": "Static", "Priority": "Low", "Risk Level": "Low"},
        {"Category": "Special Devices", "Subcategory": "Useful Data", "Item": "Authentication options", 
         "Description": "Authentication options", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Special Devices", "Subcategory": "Useful Data", "Item": "Basic logs available", 
         "Description": "Basic logs available", "Type": "Static", "Priority": "Low", "Risk Level": "Low"},
        
        # Security Considerations
        {"Category": "Special Devices", "Subcategory": "Security Considerations", "Item": "Peripheral device security", 
         "Description": "Peripheral device security", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Special Devices", "Subcategory": "Security Considerations", "Item": "Access logs", 
         "Description": "Access logs for non-traditional IT assets", "Type": "Dynamic", "Priority": "Low", "Risk Level": "Low"},
        {"Category": "Special Devices", "Subcategory": "Security Considerations", "Item": "Unusual behavior monitoring", 
         "Description": "Unusual behavior monitoring", "Type": "Dynamic", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Special Devices", "Subcategory": "Security Considerations", "Item": "Firmware vulnerability management", 
         "Description": "Firmware vulnerability management", "Type": "Static+Dynamic", "Priority": "High", "Risk Level": "High"},
        {"Category": "Special Devices", "Subcategory": "Security Considerations", "Item": "IoT device firmware updates", 
         "Description": "IoT device firmware updates", "Type": "Dynamic", "Priority": "Medium", "Risk Level": "Medium"},
    ])
    
    # ===== C) COMPANY RELATED DATA =====
    categories.extend([
        # C.1 Identity & Access Governance
        {"Category": "Company Related Data", "Subcategory": "Identity & Access Governance", "Item": "Federated identity sources", 
         "Description": "Federated identity sources (IdP: Okta, Azure AD, Keycloak)", "Type": "Static", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "Company Related Data", "Subcategory": "Identity & Access Governance", "Item": "Trust relationships", 
         "Description": "Trust relationships between domains", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Company Related Data", "Subcategory": "Identity & Access Governance", "Item": "Privileged accounts", 
         "Description": "Privileged accounts (domain admin, cloud admin)", "Type": "Static+Dynamic", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "Company Related Data", "Subcategory": "Identity & Access Governance", "Item": "Service accounts", 
         "Description": "Service accounts (machine identities)", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Company Related Data", "Subcategory": "Identity & Access Governance", "Item": "Credential scanning", 
         "Description": "Credential scanning (weak SSH keys, leaked tokens, hardcoded secrets)", "Type": "Dynamic", "Priority": "Critical", "Risk Level": "Critical"},
        
        # C.2 Attack Surface & Vulnerability Mapping
        {"Category": "Company Related Data", "Subcategory": "Attack Surface & Vulnerability Mapping", "Item": "CVE matching", 
         "Description": "CVE matching", "Type": "Dynamic", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "Company Related Data", "Subcategory": "Attack Surface & Vulnerability Mapping", "Item": "CVSS score", 
         "Description": "CVSS score", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
        {"Category": "Company Related Data", "Subcategory": "Attack Surface & Vulnerability Mapping", "Item": "Exploit availability", 
         "Description": "Exploit availability (Metasploit, ExploitDB)", "Type": "Dynamic", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "Company Related Data", "Subcategory": "Attack Surface & Vulnerability Mapping", "Item": "Patch status", 
         "Description": "Patch status (fixed / vulnerable / exploitable)", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
        {"Category": "Company Related Data", "Subcategory": "Attack Surface & Vulnerability Mapping", "Item": "Insecure default configurations", 
         "Description": "Insecure default configurations", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Company Related Data", "Subcategory": "Attack Surface & Vulnerability Mapping", "Item": "Dangerous protocols", 
         "Description": "Dangerous protocols (FTP, Telnet, SMBv1)", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Company Related Data", "Subcategory": "Attack Surface & Vulnerability Mapping", "Item": "Over-permissive firewall rules", 
         "Description": "Over-permissive firewall rules", "Type": "Static", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "Company Related Data", "Subcategory": "Attack Surface & Vulnerability Mapping", "Item": "Publicly reachable assets", 
         "Description": "Publicly reachable assets (attack surface)", "Type": "Dynamic", "Priority": "Critical", "Risk Level": "Critical"},
        
        # C.3 Behavioral & Zero-Trust Signals
        {"Category": "Company Related Data", "Subcategory": "Behavioral & Zero-Trust Signals", "Item": "User behavior anomalies", 
         "Description": "User behavior anomalies (UBEA)", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
        {"Category": "Company Related Data", "Subcategory": "Behavioral & Zero-Trust Signals", "Item": "Device trust level", 
         "Description": "Device trust level (OS updates, EDR installation)", "Type": "Dynamic", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Company Related Data", "Subcategory": "Behavioral & Zero-Trust Signals", "Item": "Network trust segmentation", 
         "Description": "Network trust segmentation (microsegmentation)", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Company Related Data", "Subcategory": "Behavioral & Zero-Trust Signals", "Item": "Least privilege compliance", 
         "Description": "Least privilege compliance", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
        {"Category": "Company Related Data", "Subcategory": "Behavioral & Zero-Trust Signals", "Item": "Zero Trust implementation status", 
         "Description": "Zero Trust implementation status", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Company Related Data", "Subcategory": "Behavioral & Zero-Trust Signals", "Item": "Continuous verification mechanisms", 
         "Description": "Continuous verification mechanisms", "Type": "Dynamic", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Company Related Data", "Subcategory": "Behavioral & Zero-Trust Signals", "Item": "Policy enforcement points", 
         "Description": "Policy enforcement points", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        
        # C.4 Resilience & Reliability Data
        {"Category": "Company Related Data", "Subcategory": "Resilience & Reliability Data", "Item": "Failover mechanisms", 
         "Description": "Failover mechanisms", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Company Related Data", "Subcategory": "Resilience & Reliability Data", "Item": "Replication health", 
         "Description": "Replication health", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
        {"Category": "Company Related Data", "Subcategory": "Resilience & Reliability Data", "Item": "Leader election status", 
         "Description": "Leader election status (distributed DBs, Kubernetes)", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
        {"Category": "Company Related Data", "Subcategory": "Resilience & Reliability Data", "Item": "Cluster membership changes", 
         "Description": "Cluster membership changes", "Type": "Dynamic", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Company Related Data", "Subcategory": "Resilience & Reliability Data", "Item": "Network partitions", 
         "Description": "Network partitions", "Type": "Dynamic", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "Company Related Data", "Subcategory": "Resilience & Reliability Data", "Item": "Disaster recovery and backup", 
         "Description": "Disaster recovery and backup recovery-test status", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
        {"Category": "Company Related Data", "Subcategory": "Resilience & Reliability Data", "Item": "Subtle failure patterns", 
         "Description": "Subtle failure patterns", "Type": "Dynamic", "Priority": "Medium", "Risk Level": "Medium"},
        
        # C.5 Supply Chain Security
        {"Category": "Company Related Data", "Subcategory": "Supply Chain Security", "Item": "Software Bill of Materials", 
         "Description": "Software Bill of Materials (SBOM)", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        {"Category": "Company Related Data", "Subcategory": "Supply Chain Security", "Item": "Docker image provenance", 
         "Description": "Docker image provenance", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Company Related Data", "Subcategory": "Supply Chain Security", "Item": "Package signatures", 
         "Description": "Package signatures (Sigstore, Cosign)", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Company Related Data", "Subcategory": "Supply Chain Security", "Item": "Dependency vulnerabilities", 
         "Description": "Dependency vulnerabilities", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
        {"Category": "Company Related Data", "Subcategory": "Supply Chain Security", "Item": "Malicious packages detection", 
         "Description": "Malicious packages detection", "Type": "Dynamic", "Priority": "Critical", "Risk Level": "Critical"},
        
        # C.6 Policy Compliance & Governance
        {"Category": "Company Related Data", "Subcategory": "Policy Compliance & Governance", "Item": "CIS benchmarks compliance", 
         "Description": "CIS benchmarks compliance", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
        {"Category": "Company Related Data", "Subcategory": "Policy Compliance & Governance", "Item": "ISO27001 controls alignment", 
         "Description": "ISO27001 controls alignment", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
        {"Category": "Company Related Data", "Subcategory": "Policy Compliance & Governance", "Item": "NIST CSF implementation", 
         "Description": "NIST CSF implementation", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
        {"Category": "Company Related Data", "Subcategory": "Policy Compliance & Governance", "Item": "Custom company policies", 
         "Description": "Custom company policies", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Company Related Data", "Subcategory": "Policy Compliance & Governance", "Item": "Compliance drift tracking", 
         "Description": "Compliance drift tracking", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
        
        # C.7 Endpoint Security Posture
        {"Category": "Company Related Data", "Subcategory": "Endpoint Security Posture", "Item": "Antivirus/EDR status", 
         "Description": "Antivirus/EDR status", "Type": "Dynamic", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "Company Related Data", "Subcategory": "Endpoint Security Posture", "Item": "Agent health", 
         "Description": "Agent health (CrowdStrike sensors, Elastic agents)", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
        {"Category": "Company Related Data", "Subcategory": "Endpoint Security Posture", "Item": "Tampering attempts", 
         "Description": "Tampering attempts", "Type": "Dynamic", "Priority": "Critical", "Risk Level": "Critical"},
        {"Category": "Company Related Data", "Subcategory": "Endpoint Security Posture", "Item": "Security logs collection status", 
         "Description": "Security logs collection status", "Type": "Dynamic", "Priority": "High", "Risk Level": "High"},
        {"Category": "Company Related Data", "Subcategory": "Endpoint Security Posture", "Item": "Missing audit policies", 
         "Description": "Missing audit policies", "Type": "Static", "Priority": "High", "Risk Level": "High"},
        
        # C.8 Cloud-Specific Metadata
        {"Category": "Company Related Data", "Subcategory": "Cloud-Specific Metadata", "Item": "Azure architecture metadata", 
         "Description": "Azure architecture metadata", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Company Related Data", "Subcategory": "Cloud-Specific Metadata", "Item": "AWS environment data", 
         "Description": "AWS environment data", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Company Related Data", "Subcategory": "Cloud-Specific Metadata", "Item": "GCP infrastructure information", 
         "Description": "GCP infrastructure information", "Type": "Static", "Priority": "Medium", "Risk Level": "Medium"},
        {"Category": "Company Related Data", "Subcategory": "Cloud-Specific Metadata", "Item": "Multi-cloud integration details", 
         "Description": "Multi-cloud integration details", "Type": "Static", "Priority": "High", "Risk Level": "High"},
    ])
    
    return categories