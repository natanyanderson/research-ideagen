"""
Semantic search script for querying the paper corpus.
"""

import sqlite3
import pickle
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def search_papers(query, db_path="papers.db", top_k=10):
    """
    Search for papers semantically similar to the query.
    
    Args:
        query: Search query string
        db_path: Path to SQLite database
        top_k: Number of top results to return
    
    Returns:
        List of (paper_id, title, abstract, similarity_score) tuples
    """
    client = OpenAI()
    
    # Generate embedding for query
    print(f"Searching for: {query}")
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    query_embedding = np.array(response.data[0].embedding)
    
    # Load all paper embeddings
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.paper_id, p.title, p.abstract, e.embedding
        FROM papers p
        JOIN embeddings e ON p.paper_id = e.paper_id
    """)
    
    # Calculate similarities
    results = []
    for paper_id, title, abstract, embedding_bytes in cursor.fetchall():
        paper_embedding = np.array(pickle.loads(embedding_bytes))
        similarity = cosine_similarity(query_embedding, paper_embedding)
        results.append((paper_id, title, abstract, similarity))
    
    conn.close()
    
    # Sort by similarity and return top k
    results.sort(key=lambda x: x[3], reverse=True)
    return results[:top_k]


def main():
    """Run interactive search."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python src/search_papers.py <query>")
        print("\nExample: python src/search_papers.py 'large language models for code generation'")
        return
    
    query = " ".join(sys.argv[1:])
    results = search_papers(query)
    
    print(f"\nTop {len(results)} results:\n")
    for i, (paper_id, title, abstract, score) in enumerate(results, 1):
        print(f"{i}. [Score: {score:.4f}]")
        print(f"   Title: {title}")
        print(f"   Abstract: {abstract[:200]}...")
        print()


if __name__ == "__main__":
    main()
