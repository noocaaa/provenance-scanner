# Distributed System Data Collection Specification

*Version*: 1.0

*Project*: Provenance Scanner

*Purpose*: Map, analyze, and secure distributed systems using structured, automated data collection.

## **1) Asset Inventory (Static)**
### Asset Identity
- **Hostname**
- **IP address(es) and network range(s)**
- **OS + version**
- **Location** (on-premises, cloud, hybrid)
- **Role** (app server, DB, proxy, firewall, NAS, printer, etc.)

### Hardware Specifications
- **CPU, RAM, storage** specifications
- **Server/device model**
- **Virtual or physical** deployment
- **Hypervisor** (if applicable)

### Installed Software
- **List of packages/programs**
- **Exact versions**
- **Known dependencies**
- **Firmware** (for printers, routers, firewalls)

### Exposed Services
- **Open ports**
- **Used protocols**
- **Active services and versions**

### Additional Considerations
- **Interdependencies between assets** (e.g., app server → database server)
- **Asset lifecycle** tracking (decommissioned or upgraded assets)

---

## **2) System Configuration (Static)**
### OS Configuration
- **Authentication policies**
- **Local firewall configuration**
- **Enabled/disabled services**
- **Auto-start programs**

### User Management
- **Local users**
- **User groups**
- **Permissions per user**
- **Admin roles**
- **SSH keys**
- **Password policies**

### Sensitive Files
- **Critical paths** (/etc, logs, config files)
- **Folder permissions**
- **Server configs** (nginx.conf, my.cnf, etc.)

### Security Controls
- **Security patches and updates** (focus on pending patches)
- **Critical patches** (zero-day vulnerabilities)
- **System hardening** (baseline security configurations)

---

## **3) Network Architecture (Static + Dynamic)**
### Topology
- **Subnets**
- **VLANs**
- **Gateways**
- **Routers and switches**
- **NAT/PAT** configurations
- **Security zones** (DMZ, internal, guest, IoT…)

### Firewalls
- **Rules** (source, destination, protocol, action)
- **Policies by zone**
- **Active inspections** (IPS/IDS, WAF…)

### Communications
- **Traffic flows** between services (app → DB, app → cache, etc.)
- **Used protocols** (HTTP, gRPC, SSH, SMB…)
- **Relevant ports**
- **Latencies** (optional)

### Security Monitoring
- **Intrusion detection/prevention systems** (IDS/IPS)
- **Anomalous traffic monitoring**
- **Lateral movement detection**
- **Data exfiltration pattern detection**

---

## **4) Applications and Services (Static + Dynamic)**
### Basic Information
- **Service name**
- **Function**
- **Internal and external dependencies**

### Exposed Endpoints
- **URLs/routes**
- **API types** (REST, SOAP, GraphQL)
- **Versioning** (v1, v2…)

### Configuration
- **Environment variables**
- **.env files**
- **Deployment parameters**
- **Log configurations**
- **Cache/session configurations**

### Containers and Orchestration
- **Images and versions**
- **Volumes**
- **Secrets and configmaps**
- **Pods, deployments, services** (Kubernetes)

### Security Enhancements
- **Access control policies**
- **Third-party services** (OAuth providers, API integrations)

---

## **5) Databases (Static + Dynamic)**
### DB Identity
- **Type** (MySQL, PostgreSQL, MongoDB, etc.)
- **Version**
- **Host and port**

### Configuration
- **Users and roles**
- **Permissions per database**
- **Password policies**
- **Encryption** in transit and at rest
- **Critical configs** (max_connections, replica settings…)

### Dynamic Data
- **Active connections**
- **Slow queries/logs**
- **Replication/lag status**
- **Backup configurations and periodicity**

### Security Auditing
- **Database audit** information
- **Encryption details**

---

## **6) Security and Access (Static + Dynamic)**
### Authentication
- **Authentication systems** (LDAP, AD, OAuth, JWT, SSO)
- **Token expiration rules**
- **SSH key management** / API keys

### Encryption
- **TLS certificates**
- **Supported TLS/SSL versions**
- **Cipher suites**
- **Expired or soon-to-expire certificates**

### Logs
- **Types of logs**
- **Storage locations**
- **Retention policies**
- **Access controls**

### Policies
- **MFA enabled/disabled status**
- **Hardening policies**
- **Role-based access control** (RBAC)

### Advanced Security
- **Privileged access management** (PAM)
- **Just-in-time access** for sensitive systems
- **Endpoint detection and response** (EDR: CrowdStrike, Carbon Black)

---

## **7) Monitoring and Metrics (Dynamic)**
### System Health
- **CPU, RAM, I/O usage**
- **Network usage**
- **Load average**

### Service Status
- **Uptime**
- **Latency per service**
- **4xx/5xx errors** (APIs)

### Relevant Events
- **Retries**
- **Connection drops**
- **APM alerts** (Application Performance Monitoring)

### Alerting and Response
- **Alerting mechanisms**
- **Response plans** (CPU spikes, memory consumption)
- **Anomalous logins detection**
- **Failed login attempts monitoring**

---

## **8) External Dependencies (Static + Dynamic)**
### External APIs
- **List of APIs**
- **Authentication types**
- **Frequency of use**
- **Error rates**

### Cloud Services
- **Load balancers**
- **Storage buckets**
- **Serverless functions**
- **CDN services**

### Risk Management
- **Third-party risk tracking**
- **Vulnerability monitoring** for external APIs

---

## **9) Special Devices (e.g., Printers)**
### Useful Data
- **Model and firmware**
- **Network configuration** (IP, port)
- **Enabled protocols** (IPP, LPD)
- **Authentication options**
- **Basic logs available**

### Security Considerations
- **Peripheral device security**
- **Access logs** for non-traditional IT assets
- **Unusual behavior monitoring**
- **Firmware vulnerability management**
- **IoT device firmware updates**

---

## **C) Company Related Data**

### **C.1) Identity & Access Governance**
#### Infrastructure Identification
- **Federated identity sources** (IdP: Okta, Azure AD, Keycloak)
- **Trust relationships** between domains
- **Privileged accounts** (domain admin, cloud admin)
- **Service accounts** (machine identities)
- **Credential scanning** (weak SSH keys, leaked tokens, hardcoded secrets)

### **C.2) Attack Surface & Vulnerability Mapping**
#### Known Vulnerabilities
- **CVE matching**
- **CVSS score**
- **Exploit availability** (Metasploit, ExploitDB)
- **Patch status** (fixed / vulnerable / exploitable)

#### Misconfigurations
- **Insecure default configurations**
- **Dangerous protocols** (FTP, Telnet, SMBv1)
- **Over-permissive firewall rules**
- **Publicly reachable assets** (attack surface)

### **C.3) Behavioral & Zero-Trust Signals**
#### User Behavior Analysis
- **User behavior anomalies** (UBEA)
- **Device trust level** (OS updates, EDR installation)
- **Network trust segmentation** (microsegmentation)
- **Least privilege compliance**

#### Zero Trust Architecture
- **Zero Trust implementation status**
- **Continuous verification mechanisms**
- **Policy enforcement points**

### **C.4) Resilience & Reliability Data**
#### Distributed Systems Requirements
- **Failover mechanisms**
- **Replication health**
- **Leader election status** (distributed DBs, Kubernetes)
- **Cluster membership changes**
- **Network partitions**
- **Disaster recovery and backup** recovery-test status

#### Failure Pattern Detection
- **Subtle failure patterns**
- **Academic research applicability**

### **C.5) Supply Chain Security**
#### Dependency Scanning
- **Software Bill of Materials** (SBOM)
- **Docker image provenance**
- **Package signatures** (Sigstore, Cosign)
- **Dependency vulnerabilities**
- **Malicious packages detection**

### **C.6) Policy Compliance & Governance**
#### Compliance Checks
- **CIS benchmarks** compliance
- **ISO27001 controls** alignment
- **NIST CSF** implementation
- **Custom company policies**
- **Compliance drift tracking**

### **C.7) Endpoint Security Posture**
#### Detection Capabilities
- **Antivirus/EDR status**
- **Agent health** (CrowdStrike sensors, Elastic agents)
- **Tampering attempts**
- **Security logs collection status**
- **Missing audit policies**

### **C.8) Cloud-Specific Metadata**
#### Cloud Platform Coverage
- **Azure** architecture metadata
- **AWS** environment data
- **GCP** infrastructure information
- **Multi-cloud** integration details

