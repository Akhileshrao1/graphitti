import json
import pickle


class BM25Retriever:

    def __init__(
        self,
        document_file="documents.json",
        index_file="bm25_index.pkl"
    ):

        print("--> [BM25] Loading documents...")

        with open(document_file, "r", encoding="utf-8") as f:
            self.documents = json.load(f)

        print("--> [BM25] Loading BM25 index...")

        with open(index_file, "rb") as f:
            self.bm25 = pickle.load(f)

    # -------------------------------------------------

    def bm25_search(
        self,
        query: str,
        k: int = 3
    ):

        tokens = query.lower().split()

        scores = self.bm25.get_scores(tokens)

        ranked = sorted(
            zip(self.documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        results = []

        for doc, score in ranked[:k]:

            results.append(
                {
                    "text": doc["text"],
                    "score": float(score)
                }
            )

        return results


# -----------------------------------------------------
# Local Testing
# -----------------------------------------------------

if __name__ == "__main__":

    retriever = BM25Retriever()

    while True:

        question = input("\nAsk: ")

        if question.lower() == "exit":
            break

        output = retriever.bm25_search(
            question
        )

        print()

        for i, result in enumerate(output, 1):

            print(f"Result {i}")
            print("-" * 40)
            print(result["text"])
            print("Score :", result["score"])
            print()
