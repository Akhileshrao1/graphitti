from neo4j import GraphDatabase
import re


class GraphRetriever:

    def __init__(
        self,
        uri="bolt://localhost:7687",
        username="neo4j",
        password="password"
    ):

        print("--> [Graph] Connecting to Neo4j...")

        self.driver = GraphDatabase.driver(
            uri,
            auth=(username, password)
        )

    # -------------------------------------------------

    def extract_keyword(self, query):

        stop_words = {
            "what", "does", "is", "the", "a", "an",
            "use", "uses", "used", "who", "how",
            "when", "where", "why", "which", "tell",
            "me", "about", "of", "to", "for",
            "created", "creator", "relationship",
            "connected", "provide", "provides"
        }

        words = re.findall(r"\w+", query.lower())

        filtered = [
            word
            for word in words
            if word not in stop_words
        ]

        return filtered[-1] if filtered else query

    # -------------------------------------------------

    @staticmethod
    def _search_graph(tx, keyword, relation_filter=None):

        if relation_filter:

            cypher_query = """
            MATCH (s)-[r]->(o)
            WHERE (toLower(s.name) = toLower($keyword)
               OR toLower(o.name) = toLower($keyword))
              AND type(r) = $relation_filter

            RETURN
                s.name AS subject,
                type(r) AS relation,
                o.name AS object

            LIMIT 5
            """

            result = tx.run(
                cypher_query,
                keyword=keyword,
                relation_filter=relation_filter
            )

        else:

            cypher_query = """
            MATCH (s)-[r]->(o)
            WHERE toLower(s.name) = toLower($keyword)
               OR toLower(o.name) = toLower($keyword)

            RETURN
                s.name AS subject,
                type(r) AS relation,
                o.name AS object

            LIMIT 5
            """

            result = tx.run(
                cypher_query,
                keyword=keyword
            )

        return [record.data() for record in result]

    # -------------------------------------------------

    def graph_search(self, question):

        keyword = self.extract_keyword(question)

        relation_filter = None

        q = question.lower()

        if "created" in q or "creator" in q:
            relation_filter = "CREATED_BY"

        elif "provide" in q or "provides" in q:
            relation_filter = "PROVIDES"

        elif "support" in q or "supports" in q:
            relation_filter = "SUPPORTS"

        with self.driver.session() as session:

            results = session.execute_read(
                self._search_graph,
                keyword,
                relation_filter
            )

        formatted_results = []

        for r in results:

            formatted_results.append(
                {
                    "text": f"{r['subject']} {r['relation']} {r['object']}",
                    "score": 1.0
                }
            )

        return formatted_results

    # -------------------------------------------------

    def close(self):

        self.driver.close()


# -----------------------------------------------------
# Local Testing
# -----------------------------------------------------

if __name__ == "__main__":

    retriever = GraphRetriever()

    while True:

        question = input("\nAsk a question (type 'exit' to stop): ")

        if question.lower() == "exit":
            break

        results = retriever.graph_search(question)

        if not results:
            print("\nNo related information found.\n")
            continue

        print()

        for i, item in enumerate(results, 1):

            print(f"Result {i}")
            print("-" * 40)
            print(item["text"])
            print()

    retriever.close()