from app.graph.neo4j_client import driver

def seed_graph():
    query = """
    MERGE (alpha:Project {id:'P1', name:'Project Alpha'})
    MERGE (beta:Project {id:'P2', name:'Project Beta'})
    MERGE (team:Team {id:'T1', name:'Team X'})
    MERGE (risk:Risk {id:'R1', name:'Resource Overload'})

    MERGE (alpha)-[:DEPENDS_ON]->(beta)
    MERGE (beta)-[:OWNED_BY]->(team)
    MERGE (team)-[:HAS_RISK]->(risk)
    """

    with driver.session() as session:
        session.run(query)

    return {"status": "graph seeded"}
