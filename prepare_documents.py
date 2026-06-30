import json

# Load graph_output.json
with open("graph_output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract text chunks
chunks = data["text_chunks"]

documents = []

for i, chunk in enumerate(chunks):
    documents.append({
        "id": f"doc{i+1}",
        "text": chunk
    })

# Save documents
with open("documents.json", "w", encoding="utf-8") as f:
    json.dump(documents, f, indent=4)

print("documents.json created successfully")