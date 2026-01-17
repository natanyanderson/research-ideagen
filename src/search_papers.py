"""
Semantic Search
Search the paper corpus using embedding similarity.

Usage:
    python src/search_papers.py "your query here"
"""
import sys
import sqlite3
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DB_PATH = "papers.db"
EMBEDDING_MODEL = "text-embedding-3-small"


def get_embedding(text):
    """Get OpenAI embedding for text."""
    response = client.embeddings.create(
        input=text[:8000],
        model=EMBEDDING_MODEL
    )
    return np.array(response.data[0].embedding, dtype=np.float32)


def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def search(query, top_k=5):
    """Search papers by semantic similarity to query."""
    query_emb = get_embedding(query)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, abstract, embedding FROM papers")
    
    results = []
    for row in c.fetchall():
        paper_emb = np.frombuffer(row[3], dtype=np.float32)
        sim = cosine_similarity(query_emb, paper_emb)
        results.append({
            "id": row[0],
            "title": row[1],
            "abstract": row[2][:200],
            "similarity": float(sim)
        })
    
    conn.close()
    
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:top_k]


if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "large language models"
    print(f"Searching for: \"{query}\"\n")
    
    results = search(query)
    for i, r in enumerate(results, 1):
        print(f"{i}. [{r['similarity']:.3f}] {r['title']}")
        print(f"   {r['abstract']}...")
        print()
