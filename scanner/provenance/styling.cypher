/*
File: styling.cyper
Author: Noelia Carrasco Vilar
Date: 2025-12-10
Description:
    Styling query for the node4j graph.
*/

// ------ SNAPSHOT / TOPOLOGY ------

// Snapshot → Hosts
MATCH (s:Snapshot)-[R:OBSERVED]->(h:Host)
RETURN s, R, h;

// Global network topology
MATCH (n:Network)<-[A:IN_NETWORK]-(ip:IP)<-[B:HAS_IP]-(h:Host)
RETURN n, ip, A, B, h;

// ------ HOST VIEWS ------

// Host list
MATCH (h:Host)
RETURN h.ip, h.hostname, h.role;

// Specific host
MATCH (h:Host {ip:"10.0.2.15"})-->(n)
RETURN h, n;

// ------ PORTS & EXPOSURE ------

// Ports exposed by host
MATCH (h:Host)-[R:EXPOSES]->(p:Port)
RETURN h, R, p;

// Publicly exposed ports
MATCH (h:Host)-[:EXPOSES]->(p:Port)
WHERE p.exposure = "public"
RETURN h.ip, p.port, p.bind_ip;

// High-risk ports
MATCH (h:Host)-[R:EXPOSES]->(p:Port)
WHERE p.port IN [22, 3389, 445, 3306, 5432]
RETURN h, R, p;

// ------ PROCESS / SOCKET / CONNECTIONS ------

// Host → Process
MATCH (h:Host)-[R:RUNS]->(p:Process)
RETURN h, R,  p;

// Process → Socket → Port
MATCH (p:Process)-[A:USES_SOCKET]->(s:Socket)-[B:BINDS_TO]->(port:Port)
RETURN p, s, A, B, port;

// Outgoing connections
MATCH (s:Socket)-[R:CONNECTS_TO]->(ip:IP)
RETURN s, R, ip;

// ------ OS (UPDATED) ------

// OS per host
MATCH (h:Host)-[A:RUNS_OS]->(osi:OSInstance)-[B:INSTANCE_OF]->(osf:OSFamily)
RETURN h, osi, A, B, osf;

// ------ SOFTWARE (UPDATED) ------

// Installed software per host
MATCH (h:Host)-[:HAS_INSTALLED]->(si:SoftwareInstance)-[:INSTANCE_OF]->(sf:SoftwareFamily)
RETURN h.ip AS host, sf.name AS software, si.version;

// Software families across hosts
MATCH (sf:SoftwareFamily)<-[:INSTANCE_OF]-(si:SoftwareInstance)<-[:HAS_INSTALLED]-(h:Host)
RETURN sf.name, collect(h.ip) AS hosts;

// ------ EXECUTION CHAIN ------

// Executable → Software family → Process
MATCH (p:Process)-[A:EXECUTES]->(e:Executable)-[B:PART_OF]->(sf:SoftwareFamily)
RETURN p, e, A, B, sf;

// Software exposed publicly
MATCH (sf:SoftwareFamily)<-[:PART_OF]-(e:Executable)<-[:EXECUTES]-(p:Process)
MATCH (p)-[:USES_SOCKET]->(:Socket)-[:BINDS_TO]->(port:Port)
WHERE port.exposure = "public"
RETURN sf.name, p.name, port.port;

// Software families that have processes on host that expose public ports
MATCH (sf:SoftwareFamily)<-[:PART_OF]-(e:Executable)<-[:EXECUTES]-(p:Process)
MATCH (p)-[:USES_SOCKET]->(:Socket)
MATCH (h:Host)-[:EXPOSES]->(port:Port)
WHERE port.exposure = "public"
RETURN DISTINCT sf.name, p.name, port.port;

// ------ USERS ------

// Users and their processes
MATCH (u:User)-[:RUNS_PROCESS]->(p:Process)
RETURN u.name, p.name, p.pid;

// Logged-in sessions
MATCH (h:Host)-[:HAS_SESSION]->(s:Session)-[:SESSION_USER]->(u:User)
RETURN h.ip, u.name, s.started;

// ------ METRICS ------

// Metrics per snapshot
MATCH (s:Snapshot)-[:HAS_METRICS]->(m:Metrics)
RETURN m;

// Attack surface summary
MATCH (m:Metrics)
RETURN
  m.public_ports,
  m.local_ports,
  m.internal_ports,
  m.public_exposure_ratio;

// Graph complexity
MATCH (m:Metrics)
RETURN
  m.total_nodes,
  m.total_edges,
  m.edge_types;

// ------ PROCESS TRESS ------

// Full process tree
MATCH path = (root:Process {pid: 1})<-[:SPAWNED_BY*]-(child)
RETURN path;

// Suspicious shell chains
MATCH (a:Process)-[:SPAWNED_BY]->(b:Process)-[:SPAWNED_BY]->(c:Process)
WHERE b.name IN ["bash", "sh", "zsh"]
RETURN a.name, b.name, c.name;
