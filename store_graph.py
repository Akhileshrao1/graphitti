import json
import re
from neo4j import GraphDatabase

# Neo4j connection
URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "password"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

# Load graph_output.json
with open("graph_output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

triples = data["triples"]


# Clean predicate into valid Neo4j relationship type
def clean_predicate(predicate):
    predicate = re.sub(r'[^A-Za-z0-9]', '_', predicate)
    predicate = re.sub(r'_+', '_', predicate)
    predicate = predicate.strip('_')

    if not predicate:
        predicate = "DEFAULT_REL"

    if predicate[0].isdigit():
        predicate = "REL_" + predicate

    return predicate.upper()


# Store one triple
def store_triple(tx, subject, predicate, obj, source_url):
    query = f"""
    MERGE (s:Entity {{name: $subject}})
    MERGE (o:Entity {{name: $obj}})
    MERGE (s)-[r:{predicate}]->(o)
    SET r.source_url = $source_url
    """

    tx.run(
        query,
        subject=subject,
        obj=obj,
        source_url=source_url
    )


# Store all triples with counter
total = len(triples)

with driver.session() as session:
    for count, triple in enumerate(triples, start=1):
        subject = triple["subject"]
        predicate = clean_predicate(
            triple["predicate"]
        )
        obj = triple["object"]
        source_url = triple.get(
            "source_url",
            ""
        )

        session.execute_write(
            store_triple,
            subject,
            predicate,
            obj,
            source_url
        )

        print(f"Stored {count}/{total}")

print("Graph stored successfully")

driver.close()