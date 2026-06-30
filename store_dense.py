import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load documents
with open("documents.json", "r", encoding="utf-8") as f:
    documents = json.load(f)

texts = [doc["text"] for doc in documents]

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings
embeddings = model.encode(texts)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings))

# Save FAISS index
faiss.write_index(index, "dense_index.faiss")

print("Dense index stored successfully")