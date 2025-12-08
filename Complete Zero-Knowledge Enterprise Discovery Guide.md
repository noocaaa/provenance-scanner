# **COMPLETE ZERO-KNOWLEDGE ENTERPRISE DISCOVERY GUIDE**

## **STARTING POSITION: You Know NOTHING**

You have:
- A computer
- Network access
- Zero information about the enterprise

---

## **PHASE 0: SELF-DISCOVERY (5 minutes)**

**Goal:** Understand YOUR environment first

### **Step 0.1: Check Your Own System**
```
# Windows
ipconfig /all
systeminfo | findstr /B /C:"Domain"
net config workstation

# Linux/Mac
ifconfig -a  OR  ip addr show
cat /etc/resolv.conf
hostname -f
domainname
```

**Look for:**
- Your IP address: ________________
- Subnet mask: ________________
- Default gateway: ________________
- DNS servers: ________________
- Domain name: ________________
- Hostname: ________________

### **Step 0.2: Check Network Connections**
```
# Windows
netstat -ano
arp -a

# Linux/Mac
netstat -tulpn
arp -n
ss -tulpn
```

**Look for:**
- Established connections to: ________________
- ARP cache entries: ________________
- Listening ports on YOUR machine: ________________

---

## **PHASE 1: LOCAL NETWORK DISCOVERY (15 minutes)**

**Goal:** Map your immediate surroundings

### **Step 1.1: Discover Local Subnet**
```
# Calculate your subnet range
Your IP: ___________
Subnet Mask: ___________
Network Range: ___________

# Example: 192.168.1.100/24 = 192.168.1.0-255
```

### **Step 1.2: Quick Active Host Discovery**
```
# ARP Scan (fastest, local network only)
# Windows:
arp -a  # Shows already known hosts

# Linux:
arp-scan --localnet

# Ping sweep your subnet:
for ip in {1..254}; do ping -c 1 -W 1 192.168.1.$ip | grep "from"; done

# Or use fping (faster):
fping -a -g 192.168.1.0/24 2>/dev/null
```

**Found hosts (write down):**
1. ___________
2. ___________
3. ___________
4. ___________
5. ___________

### **Step 1.3: Identify Key Infrastructure**
**Check these common IPs in your subnet:**

- **.1** (Gateway): ___________
- **.10** (Common for servers): ___________
- **.100** (Common for printers): ___________
- **.200+** (Common for clients): ___________
- **.254** (Common for switches): ___________

**Test if they respond:**
```
ping -c 2 [EACH_IP]
```

---

## **PHASE 2: DNS RECONNAISSANCE (20 minutes)**

**Goal:** Use DNS to discover more than scanning ever could

### **Step 2.1: Query Your DNS Server**
```
# Get DNS server from ipconfig/resolv.conf
DNS Server: ___________

# Test DNS server
nslookup google.com [DNS_SERVER]

# Try zone transfer (GOLD if it works)
dig axfr @[DNS_SERVER] [DOMAIN_NAME]
nslookup -type=any -query=AXFR [DOMAIN_NAME] [DNS_SERVER]

# If zone transfer fails, continue...
```

### **Step 2.2: DNS Brute Force Common Names**
```
# Common naming conventions in enterprises:

Prefixes:
- web, www, app, api, portal
- mail, exchange, smtp, imap
- db, sql, oracle, mysql
- fs, file, nas, storage
- vpn, proxy, gateway
- git, svn, repo
- jenkins, build, ci, cd
- monitor, nagios, zabbix
- dc, ad, domain, ldap
- print, printer, scan

Suffixes:
- 01, 02, 03, -prod, -test, -dev
- .local, .internal, .corp, .lan

# Try combinations:
nslookup web01.[DOMAIN] [DNS_SERVER]
nslookup mail.[DOMAIN] [DNS_SERVER]
nslookup vpn.[DOMAIN] [DNS_SERVER]
nslookup dc01.[DOMAIN] [DNS_SERVER]
```

### **Step 2.3: Reverse DNS Lookup**
```
# For each IP in your local subnet, try:
nslookup [IP] [DNS_SERVER]

# Common finds:
- router.corp.local
- switch1.building3.corp.local  
- printer-floor2.corp.local
- dc01.ad.corp.local
- fileserver.corp.local
```

### **Step 2.4: DNS Record Enumeration**
```
# Check different record types:
dig @[DNS_SERVER] [DOMAIN] ANY
dig @[DNS_SERVER] [DOMAIN] MX      # Mail servers
dig @[DNS_SERVER] [DOMAIN] NS      # Name servers
dig @[DNS_SERVER] [DOMAIN] TXT     # SPF, DKIM records
dig @[DNS_SERVER] [DOMAIN] SRV     # Service records (AD, LDAP)
```

**DNS Discoveries (write down):**
```
Hostnames found:
1. ________________ : ________________ (IP)
2. ________________ : ________________ (IP)
3. ________________ : ________________ (IP)
4. ________________ : ________________ (IP)
5. ________________ : ________________ (IP)

Special finds:
- Mail server: ________________
- Domain controller: ________________
- Web server: ________________
- VPN: ________________
```

---

## **PHASE 3: PASSIVE DISCOVERY (30 minutes)**

**Goal:** Listen without sending - be invisible

### **Step 3.1: Monitor Network Traffic**
```
# Linux (tcpdump):
sudo tcpdump -i any -n -c 1000

# Look for:
# - DHCP requests (clients getting IPs)
# - NetBIOS broadcasts (Windows machines)
# - mDNS/Bonjour (Apple/Linux)
# - SSDP/UPnP (printers, IoT)
# - ARP requests (who's looking for who)

# Save to file and analyze:
sudo tcpdump -i any -w capture.pcap
```

### **Step 3.2: Analyze Broadcast Traffic**
```
# Common broadcast/multicast addresses:
# 255.255.255.255 - General broadcast
# 224.0.0.1 - All hosts
# 224.0.0.2 - All routers
# 224.0.0.251 - mDNS
# 239.255.255.250 - SSDP

# Filter for specific traffic:
sudo tcpdump -n port 67 or port 68    # DHCP
sudo tcpdump -n port 137 or port 138  # NetBIOS
sudo tcpdump -n port 5353             # mDNS
```

### **Step 3.3: Check Local Service Discovery**
```
# Windows: (shows local network shares, printers)
net view

# mDNS/Bonjour:
dns-sd -B _services._dns-sd._udp local.

# SSDP/UPnP:
# Use Wireshark or tcpdump filter for port 1900
```

**Passive Discoveries:**
```
Devices heard talking:
1. MAC: __________ IP: __________ Type: __________
2. MAC: __________ IP: __________ Type: __________
3. MAC: __________ IP: __________ Type: __________

Services discovered:
- DHCP Server: __________
- Network Shares: __________
- Printers: __________
- Media Devices: __________
```

---

## **PHASE 4: ACTIVE PROBING (45 minutes)**

**Goal:** Now that you know some targets, probe intelligently

### **Step 4.1: Service Discovery on Known Hosts**
```
# For each discovered IP, scan common ports:
nmap -sS -T4 -F [IP]   # Fast SYN scan top 100 ports

# OR use masscan for very fast scanning:
masscan -p1-1000 [IP_RANGE] --rate=1000

# Common enterprise ports to check:
# 22(SSH), 23(Telnet), 25(SMTP), 53(DNS), 80(HTTP), 443(HTTPS)
# 135-139(NetBIOS), 445(SMB), 1433(MSSQL), 3306(MySQL)
# 3389(RDP), 5985-5986(WinRM), 8080-8090(Web apps)
```

### **Step 4.2: Banner Grabbing**
```
# Connect to open ports and grab banners:
nc -nv [IP] 22        # SSH
nc -nv [IP] 80        # HTTP (then type "HEAD / HTTP/1.0\n\n")
telnet [IP] 25        # SMTP
openssl s_client -connect [IP]:443 -servername [HOSTNAME]

# Automated:
nmap -sV --script=banner [IP]
```

**Service Information:**
```
IP: __________
Port 22: SSH-2.0-OpenSSH_7.4 Ubuntu
Port 80: Apache/2.4.41 (Unix)
Port 443: Microsoft-IIS/10.0
Port 445: Windows 10 Professional
```

### **Step 4.3: SNMP Discovery**
```
# Try common community strings:
community_strings = ["public", "private", "snmp", "read", "write", "admin"]

for community in community_strings:
    snmpwalk -c [community] -v 2c [IP] system
    snmpwalk -c [community] -v 2c [IP] interfaces
    snmpwalk -c [community] -v 2c [IP] ipRouteTable

# SNMP reveals:
# - System name, location, contact
# - Network interfaces (IPs, MACs)
# - Routing tables (OTHER NETWORKS!)
# - ARP tables (other hosts)
# - Processes running
```

### **Step 4.4: Network Path Discovery**
```
# Trace route to discovered hosts:
tracert [IP]        # Windows
traceroute [IP]     # Linux/Mac
mtr [IP]            # Continuous trace

# Look for:
# - Hops through different subnets
# - Internal routers (10.x, 172.16.x, 192.168.x)
# - Network segmentation

# Example discovery:
Your IP: 192.168.1.100
Target: 10.10.50.100
Path: 192.168.1.1 → 172.16.1.1 → 10.10.1.1 → 10.10.50.100

# You just discovered THREE networks!
# 192.168.1.0/24, 172.16.1.0/24, 10.10.0.0/16
```

---

## **PHASE 5: SNOWBALL DISCOVERY (60+ minutes)**

**Goal:** Each discovery leads to more discoveries

### **Step 5.1: Query Infrastructure Servers**
**If you found a DNS server:**
```
# Query it for everything:
dig @[DNS_SERVER] axfr corp.local
dig @[DNS_SERVER] any corp.local

# Try internal domain variations:
corp.local, internal.corp, ad.corp, private.corp
```

**If you found an LDAP/AD server:**
```
# Anonymous LDAP bind (often works):
ldapsearch -x -h [IP] -b "dc=corp,dc=local"

# Returns: ALL users, computers, groups, servers
```

**If you found a web server:**
```
# Spider the site:
wget --spider -r http://[IP]/

# Check virtual hosts:
gobuster vhost -u http://[IP] -w common-vhosts.txt

# Check for exposed files:
robots.txt, sitemap.xml, .git/, .svn/, backup.zip
```

### **Step 5.2: Follow Network Protocols**
**Check routing protocols:**
```
# Listen for OSPF, EIGRP, RIP
sudo tcpdump -n port 89 or port 88 or port 520

# These reveal ALL network routes!
```

**Check for NetBIOS:**
```
# Windows network enumeration:
nbtscan [SUBNET]
nmblookup -A [IP]

# Shows: computer names, domains, users
```

### **Step 5.3: Check Cloud & External Presence**
```
# Even if internal, check external:
# 1. Certificate Transparency logs
curl "https://crt.sh/?q=%.corp.local&output=json"

# 2. Search engines
site:corp.local intitle:"login"
site:corp.local inurl:"admin"
site:*.corp.local -www

# 3. GitHub/GitLab search
"corp.local" "password" "api_key" "config"
```

### **Step 5.4: Check for Misconfigurations**
```
# Common misconfigurations that reveal everything:

# 1. Jenkins without auth (port 8080)
http://[IP]:8080/computer/api/json

# 2. Docker API exposed (port 2375)
curl http://[IP]:2375/containers/json

# 3. Redis without auth (port 6379)
redis-cli -h [IP] keys *

# 4. Elasticsearch (port 9200)
curl http://[IP]:9200/_cat/indices

# 5. Memcached (port 11211)
echo "stats items" | nc [IP] 11211
```

---

## **PHASE 6: CORRELATION & MAPPING (30 minutes)**

**Goal:** Create a complete map from all discoveries

### **Step 6.1: Create Asset Inventory**
```
ASSETS FOUND:

NETWORK RANGES:
1. __________ / ___ (Discovered via: __________)
2. __________ / ___ (Discovered via: __________)
3. __________ / ___ (Discovered via: __________)

CRITICAL SERVERS:
- Domain Controllers: __________
- DNS Servers: __________
- DHCP Servers: __________
- File Servers: __________
- Database Servers: __________
- Web Servers: __________
- Mail Servers: __________
- VPN Servers: __________

NETWORK DEVICES:
- Routers: __________
- Switches: __________
- Firewalls: __________
- Load Balancers: __________

USER DEVICES:
- Desktops: __________
- Laptops: __________
- Printers: __________
- Phones: __________
- IoT: __________
```

### **Step 6.2: Map Network Segmentation**
```
Draw a simple network diagram:

[Internet]
    |
[Firewall] - External IP: __________
    |
[Core Router] - __________
    |
    |--- [DMZ Network] - __________
    |       |
    |       |-- Web Server: __________
    |       |-- VPN: __________
    |
    |--- [Internal Network 1] - __________
    |       |
    |       |-- Domain Controller: __________
    |       |-- File Server: __________
    |
    |--- [Internal Network 2] - __________
            |
            |-- User Devices: __________
            |-- Printers: __________
```

### **Step 6.3: Identify Security Posture**
```
SECURITY OBSERVATIONS:

1. Open ports found: __________
2. Services with default credentials: __________
3. Exposed management interfaces: __________
4. Outdated software versions: __________
5. Misconfigurations found: __________
6. Information leaks found: __________
```

---

## **PHASE 7: DEEP DISCOVERY (Ongoing)**

**Goal:** Continuous improvement of your map

### **Step 7.1: Set Up Continuous Monitoring**
```
# 1. Regular ping sweeps (daily)
# 2. Port change detection (weekly)
# 3. New host detection (real-time)
# 4. Service change detection

# Simple script example:
while true; do
    nmap -sn [NETWORK_RANGE] > scan-$(date +%Y%m%d).txt
    diff scan-yesterday.txt scan-today.txt
    sleep 3600  # 1 hour
done
```

### **Step 7.2: Discover Hidden Networks**
```
# Check for:
# 1. VLAN hopping possibilities
# 2. Wireless networks (scan for SSIDs)
# 3. VPN connections (check routing tables)
# 4. Tunnels (GRE, IPsec)

# Command to check routing table:
netstat -rn          # Windows
route -n             # Linux
```

### **Step 7.3: Discover Through Logs**
```
# If you get access to any system, check:
# - Event logs (Windows Event Viewer)
# - Auth logs (/var/log/auth.log)
# - Web logs (/var/log/apache2/)
# - DHCP logs
# - Firewall logs

# Common locations of interest:
Windows: C:\Windows\System32\winevt\Logs\
Linux: /var/log/
```

---

## **TOOLS CHECKLIST**

### **Must-Have Tools:**
```
# Discovery:
- nmap (port scanning)
- masscan (fast scanning)
- arp-scan (layer 2)
- tcpdump (packet capture)
- dig/nslookup (DNS)

# Analysis:
- Wireshark (packet analysis)
- tshark (command-line Wireshark)
- netcat (manual connections)
- curl/wget (web interactions)

# Enumeration:
- enum4linux (Windows/SMB)
- snmpwalk (SNMP)
- ldapsearch (LDAP)
- smbclient (SMB shares)
```

### **Advanced Tools (if available):**
```
- nessus/openvas (vulnerability scanning)
- bloodhound (Active Directory mapping)
- crackmapexec (Windows networks)
- theHarvester (OSINT)
- shodan.io (Internet-facing devices)
```

---

## **RED FLAGS & IMMEDIATE FINDINGS**

**Stop and investigate if you find:**

1. **Domain Controller without firewall** - Critical
2. **Database with public access** - Critical  
3. **Default credentials on anything** - High
4. **Out-of-date critical services** - High
5. **Exposed management interfaces** - Medium
6. **Unauthorized devices** - Medium
7. **Clear-text protocols** - Low (but fix)

---

## **REPORT TEMPLATE**

```
ENTERPRISE DISCOVERY REPORT
===========================
Date: __________
Scanner: __________
Duration: __________

EXECUTIVE SUMMARY:
- Total networks discovered: ___
- Total hosts discovered: ___
- Critical findings: ___
- High-risk findings: ___

NETWORK TOPOLOGY:
[Diagram or description]

ASSET INVENTORY:
[Table of assets]

FINDINGS BY RISK LEVEL:
CRITICAL:
1. __________
2. __________

HIGH:
1. __________
2. __________

MEDIUM:
1. __________
2. __________

RECOMMENDATIONS:
1. Immediate actions: __________
2. Short-term fixes: __________
3. Long-term improvements: __________
```

---

## **REMEMBER:**

1. **Document everything** - Notes are your best friend
2. **Correlate data** - One source lies, multiple sources reveal truth
3. **Start small, grow big** - One IP leads to a network
4. **Be patient** - Discovery takes time
5. **Stay legal** - Only scan what you're authorized to scan
6. **Assume nothing** - Verify everything

**You started knowing NOTHING. Now you have a complete map of the enterprise.**