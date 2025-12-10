/*
File: styling.cyper
Author: Noelia Carrasco Vilar
Date: 2025-12-10
Description:
    Styling query for the node4j graph.
*/

// HOST: Display hostname or IP
MATCH (h:Host)
SET h.name = coalesce(h.hostname, h.ip, h.id);

// NETWORK: Display CIDR
MATCH (n:Network)
SET n.name = n.cidr;

// INTERFACE: Display interface name
MATCH (i:Interface)
SET i.name = i.name;

// PORT: Display protocol/port
MATCH (p:Port)
SET p.name = p.id;

// SNAPSHOT: Display timestamp
MATCH (s:Snapshot)
SET s.name = s.collected_at;

// GRAPH VISUALIZATION. For run this manually on the Neo4j Web Browser or Desktop app.
MATCH (n)-[r]->(m) RETURN n, r,m