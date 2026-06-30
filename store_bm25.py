import json
import pickle
from rank_bm25 import BM25Okapi

# Load documents
with open("documents.json", "r", encoding="utf-8") as f:
    documents = json.load(f)

texts = [doc["text"] for doc in documents]

# Simple tokenization
tokenized_docs = [
    text.lower().split() for text in texts
]

# Create BM25 index
bm25 = BM25Okapi(tokenized_docs)

# Save BM25 index
with open("bm25_index.pkl", "wb") as f:
    pickle.dump(bm25, f)

print("BM25 stored successfully")