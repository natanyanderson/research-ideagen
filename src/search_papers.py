import sqlite3
import openai
import os
import json
import numpy as np
from dotenv import load_dotenv
import sys

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Get query from command line
if len(sys.argv) < 2:
    print("Usage: python search_papers.py 'your search query'")
    sys.exit(1)

query = " ".join(sys.argv[1:])

# Generate embedding for query
print(f"Searching for: {query}")
response = openai.embeddings.create(
    input=query,
    model="text-embedding-3-small"
)
query_embedding = response.data[0].embedding

# Connect to database
conn = sqlite3.connect("papers.db")
cursor = conn.cursor()

# Fetch all embeddings
cursor.execute("""
    SELECT p.arxiv_id, p.title, p.authors, e.embedding
    FROM papers p
    JOIN embeddings e ON p.arxiv_id = e.arxiv_id
""")

results = []
for row in cursor.fetchall():
    arxiv_id, title, authors, embedding_bytes = row
    embedding = json.loads(embedding_bytes.decode())
    similarity = cosine_similarity(query_embedding, embedding)
    results.append((similarity, arxiv_id, title, authors))

conn.close()

# Sort by similarity and show top 10
results.sort(reverse=True, key=lambda x: x[0])
print(f"\nTop 10 results:\n")
for i, (score, arxiv_id, title, authors) in enumerate(results[:10], 1):
    print(f"{i}. [{score:.3f}] {title}")
    print(f"   Authors: {authors}")
    print(f"   arXiv ID: {arxiv_id}\n")
