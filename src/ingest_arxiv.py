"""
ArXiv Ingestion Script
Fetches CS papers from 2024-2026, stores in SQLite with OpenAI embeddings on abstracts.

Usage:
    python src/ingest_arxiv.py

Requires OPENAI_API_KEY in .env file.
"""
import os
import json
import sqlite3
import time
import struct
import numpy as np
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

import arxiv
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DB_PATH = "papers.db"
EMBEDDING_MODEL = "text-embedding-3-small"
MAX_PAPERS = 1000


def init_db():
    """Initialize SQLite database with papers table."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS papers (
            id TEXT PRIMARY KEY,
            title TEXT,
            abstract TEXT,
            authors TEXT,
            published TEXT,
            categories TEXT,
            embedding BLOB
        )
    """)
    conn.commit()
    return conn


def get_embedding(text):
    """Get OpenAI embedding for text, returns float32 array."""
    response = client.embeddings.create(
        input=text[:8000],
        model=EMBEDDING_MODEL
    )
    embedding = response.data[0].embedding
    return np.array(embedding, dtype=np.float32)


def fetch_papers():
    """Fetch CS papers from arXiv (2024-2026)."""
    search = arxiv.Search(
        query="cat:cs.*",
        max_results=MAX_PAPERS,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )
    
    papers = []
    for result in search.results():
        pub_year = result.published.year
        if pub_year < 2024:
            continue
        papers.append({
            "id": result.entry_id,
            "title": result.title,
            "abstract": result.summary,
            "authors": ", ".join([a.name for a in result.authors]),
            "published": result.published.isoformat(),
            "categories": ", ".join(result.categories)
        })
    
    return papers


def ingest():
    """Main ingestion pipeline."""
    print("Initializing database...")
    conn = init_db()
    
    print("Fetching papers from arXiv...")
    papers = fetch_papers()
    print(f"Found {len(papers)} papers")
    
    c = conn.cursor()
    for i, paper in enumerate(papers):
        if i % 50 == 0:
            print(f"Processing paper {i+1}/{len(papers)}...")
        
        try:
            embedding = get_embedding(paper["abstract"])
            embedding_blob = embedding.tobytes()
            
            c.execute("""
                INSERT OR REPLACE INTO papers 
                (id, title, abstract, authors, published, categories, embedding)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                paper["id"], paper["title"], paper["abstract"],
                paper["authors"], paper["published"], paper["categories"],
                embedding_blob
            ))
            
            if i % 100 == 0:
                conn.commit()
                
        except Exception as e:
            print(f"Error processing paper {paper['id']}: {e}")
            continue
    
    conn.commit()
    
    # Verify
    c.execute("SELECT COUNT(*) FROM papers")
    count = c.fetchone()[0]
    print(f"\nIngestion complete: {count} papers stored with embeddings")
    
    conn.close()


if __name__ == "__main__":
    ingest()
