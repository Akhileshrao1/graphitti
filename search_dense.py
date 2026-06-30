import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class DenseRetriever:

    def __init__(
        self,
        document_file="documents.json",
        index_file="dense_index.faiss",
        model_name="all-MiniLM-L6-v2"
    ):

        print("--> [Dense] Loading documents...")

        with open(document_file, "r", encoding="utf-8") as f:
            self.documents = json.load(f)

        print("--> [Dense] Loading FAISS index...")

        self.index = faiss.read_index(index_file)

        print("--> [Dense] Loading embedding model...")

        self.model = SentenceTransformer(model_name)

    def dense_search(self, query: str, k: int = 3):

        query_embedding = self.model.encode(
            [query]
        ).astype("float32")

        distances, indices = self.index.search(
            np.array(query_embedding),
            k
        )

        results = []

        for rank, idx in enumerate(indices[0]):

            if idx == -1:
                continue

            results.append(
                {
                    "chunk_id": idx,
                    "text": self.documents[idx]["text"],
                    "score": float(distances[0][rank])
                }
            )

        return results


# -----------------------------
# Local Testing
# -----------------------------

if __name__ == "__main__":

    retriever = DenseRetriever()

    while True:

        question = input("\nAsk: ")

        if question.lower() == "exit":
            break

        output = retriever.dense_search(question)

        print()

        for i, result in enumerate(output, 1):

            print(f"Result {i}")
            print("-" * 40)
            print(result["text"])
            print("Score :", result["score"])
            print()