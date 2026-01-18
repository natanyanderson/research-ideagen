import sqlite3
import openai
import os
import numpy as np
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")

client = openai.OpenAI(api_key=OPENAI_API_KEY)
DATABASE_NAME = "papers.db"

def get_embedding(text):
    """Generates an embedding for the given text using OpenAI's API."""
    text = text.replace("\n", " ")
    try:
        response = client.embeddings.create(input=[text], model="text-embedding-3-small")
        return response.data[0].embedding
    except openai.APIError as e:
        print(f"OpenAI API Error: {e}")
        return None

def cosine_similarity(vec1, vec2):
    """Computes the cosine similarity between two vectors."""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def search_papers(query, top_n=10):
    """
    Searches the paper corpus for the most semantically similar papers to the query.
    """
    # Check if database exists
    if not os.path.exists(DATABASE_NAME):
        print(f"❌ Database not found: {DATABASE_NAME}")
        print("Please run 'python src/ingest_arxiv.py' first to populate the database.")
        return
    
    query_embedding = get_embedding(query)
    if query_embedding is None:
        print("❌ Could not generate embedding for the query.")
        return

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT p.paper_id, p.title, p.authors, e.embedding FROM papers p JOIN embeddings e ON p.paper_id = e.paper_id")
        papers_data = cursor.fetchall()
    except sqlite3.OperationalError as e:
        print(f"❌ Database error: {e}")
        print("The database may be corrupted or empty. Try running ingestion again.")
        conn.close()
        return
    
    conn.close()

    if not papers_data:
        print("❌ No papers found in database. Please run ingestion first.")
        return

    similarities = []
    for paper_id, title, authors, embedding_blob in papers_data:
        paper_embedding = np.frombuffer(embedding_blob, dtype=np.float32)
        similarity = cosine_similarity(query_embedding, paper_embedding)
        similarities.append((similarity, paper_id, title, authors))

    similarities.sort(key=lambda x: x[0], reverse=True)

    print(f"\nSearching for: {query}")
    print("=" * 70)
    print(f"Top {top_n} results:\n")
    
    for i, (similarity, paper_id, title, authors) in enumerate(similarities[:top_n]):
        print(f"{i+1}. [{similarity:.3f}] {title}")
        print(f"   Authors: {authors}")
        print(f"   arXiv ID: {paper_id}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/search_papers.py \"your search query\"")
        sys.exit(1)
    
    query_text = " ".join(sys.argv[1:])
    search_papers(query_text)
