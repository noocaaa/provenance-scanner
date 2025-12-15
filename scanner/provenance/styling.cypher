/*
File: styling.cyper
Author: Noelia Carrasco Vilar
Date: 2025-12-10
Description:
    Styling query for the node4j graph.
*/

// Global topology (default view)
MATCH (n:Network)<-[r1:IN_NETWORK]-(ip:IP)<-[r2:HAS_IP]-(h:Host)
RETURN n, ip, h, r1, r2

// Full Graph
MATCH (n)-[r]->(m) RETURN n, r,m

// Discovery relationship
MATCH (h:Host)-[r1:PERFORMED]->(d:Discovery)-[r2:DISCOVERED]->(r:Host)
RETURN h, d, r, r1, r2

// All information for a specific host (2-hop view)
MATCH (h:Host {ip: "192.168.56.1"})-[*1..2]->(x)
RETURN h, x

// Host - Interface - IP
MATCH (h:Host)-[r1:HAS_INTERFACE]->(i:Interface)-[r2:HAS_IP]->(ip:IP)
RETURN h, i, ip, r1, r2

// OS
MATCH (h:Host)-[r:RUNS_OS]->(os:OS)
RETURN h, os, r

// Logged users
MATCH (h:Host)-[r:LOGGED_IN_AS]->(u:User)
RETURN h, u, r

// Installed software
MATCH (h:Host)-[r:INSTALLED]->(s:Software)
RETURN h, s, r

// Hardware
MATCH (h:Host)-[r:HAS_HARDWARE]->(hw)
RETURN h, r, hw

// CPU
MATCH (h:Host)-[r:HAS_HARDWARE]->(c:CPU)
RETURN h, r, c

// Memory
MATCH (h:Host)-[r:HAS_HARDWARE]->(m:Memory)
RETURN h,r,  m

// Disk
MATCH (h:Host)-[r:HAS_HARDWARE]->(d:Disk)
RETURN h, r, d

// Host - Process
MATCH (h:Host)-[r:RUNS]->(p:Process)
RETURN h, p, r

// Process - Port (LISTENS_ON)
MATCH (h:Host)-[r1:RUNS]->(p:Process)-[r2:LISTENS_ON]->(port:Port)
RETURN h, p, port, r1, r2

// Ports exposed by host
MATCH (h:Host)-[r:EXPOSES]->(p:Port)
RETURN h, p, r

///////////////////////
//  ADVANCED QUERIES //
///////////////////////

// Open Ports per host
MATCH (h:Host)-[:EXPOSES]->(p:Port)
RETURN h.ip AS host, collect(p.port) AS open_ports

// Host with open SSH
MATCH (h:Host)-[:EXPOSES]->(p:Port {port: 22})
RETURN h

// Host with >3 open ports
MATCH (h:Host)-[:EXPOSES]->(p:Port)
WITH h, count(p) AS ports
WHERE ports > 3
RETURN h, ports

// Software per Host
MATCH (h:Host)-[:INSTALLED]->(s:Software)
RETURN h.ip AS host, collect(s.name) AS software

// Full attack surface per host (process + port)
MATCH (h:Host)-[:RUNS]->(p:Process)-[:LISTENS_ON]->(port:Port)
RETURN h.ip, p.pid, p.name, port.port

// High-risk ports
MATCH (h:Host)-[r:EXPOSES]->(p:Port)
WHERE p.port IN [22, 3389, 445, 3306, 5432]
RETURN h, r, p
