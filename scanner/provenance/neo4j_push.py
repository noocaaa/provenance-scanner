"""
File: neo4j_push.py
Author: Noelia Carrasco Vilar
Date: 2025-12-09
Description:
    Pushes the provenance graph into Neo4j using MERGE 
"""
from neo4j import GraphDatabase


class Neo4jConnector:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def clear_database(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def push_graph(self, G):
        with self.driver.session() as session:

            # ---------------------------
            # CREATE NODES
            # ---------------------------
            for node_id, attrs in G.nodes(data=True):

                label = attrs.get("label", "Node")
                clean_props = {}

                # all safe properties
                for k, v in attrs.items():
                    if isinstance(v, (str, int, float, bool)) or v is None:
                        clean_props[k] = v
                    else:
                        print(f"[WARNING] Ignoring complex property on {node_id}: {k}={v}")

                # guarantee ID is a simple string
                clean_props["neo_id"] = node_id

                session.run(
                    f"""
                            MERGE (n:{label} {{neo_id: $neo_id}})
                            SET n += $props
                            """,
                    neo_id=node_id,
                    props=clean_props
                )

            # ---------------------------
            # CREATE RELATIONSHIPS
            # ---------------------------
            for u, v, attrs in G.edges(data=True):
                rel_type = attrs.get("rel_type") or "RELATED_TO"
                rel_type = rel_type.replace(" ", "_").upper()

                session.run(
                    f"""
                            MATCH (a {{neo_id: $u}})
                            MATCH (b {{neo_id: $v}})
                            MERGE (a)-[r:`{rel_type}`]->(b)
                            """,
                    u=u,
                    v=v
                )

    def close(self):
        self.driver.close()
