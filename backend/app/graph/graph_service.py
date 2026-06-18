from app.graph.neo4j_client import driver

def get_graph():
    query = """
    MATCH (a)-[r]->(b)
    RETURN
    a.name AS source,
    type(r) AS relation,
    b.name AS target
    """

    with driver.session() as session:
        records = session.run(query)

        return [
            {
                "source": row["source"],
                "relation": row["relation"],
                "target": row["target"]
            }
            for row in records
        ]
