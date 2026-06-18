from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "nexuspassword"

driver = GraphDatabase.driver(
    URI,
    auth=(USER, PASSWORD)
)
