"""
ArXiv paper ingestion script.

Pulls CS papers from arXiv (2024-2025), stores them in SQLite,
and generates embeddings for abstracts.
"""

import arxiv
import sqlite3
import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Database setup
def init_db(db_path="papers.db"):
    """Initialize SQLite database with papers table."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS papers (
            paper_id INTEGER PRIMARY KEY AUTOINCREMENT,
            arxiv_id TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            abstract TEXT NOT NULL,
            authors TEXT,
            published_date TEXT,
            categories TEXT,
            pdf_url TEXT,
            ingested_at TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            paper_id INTEGER PRIMARY KEY,
            embedding BLOB NOT NULL,
            FOREIGN KEY (paper_id) REFERENCES papers (paper_id)
        )
    """)
    
    conn.commit()
    return conn


def fetch_arxiv_papers(category="cs", start_year=2024, max_results=1000):
    """
    Fetch papers from arXiv.
    
    Args:
        category: arXiv category (default: cs for Computer Science)
        start_year: Start year for papers
        max_results: Maximum number of papers to fetch
    
    Returns:
        List of arxiv.Result objects
    """
    # Query for CS papers from 2024 onwards
    query = f"cat:{category}.* AND submittedDate:[{start_year}0101 TO 20251231]"
    
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )
    
    papers = []
    print(f"Fetching up to {max_results} papers from arXiv...")
    
    for result in search.results():
        papers.append(result)
        if len(papers) % 100 == 0:
            print(f"  Fetched {len(papers)} papers...")
    
    print(f"Fetched {len(papers)} papers total.")
    return papers


def store_paper(conn, paper):
    """Store a single paper in the database."""
    cursor = conn.cursor()
    
    # Prepare data
    arxiv_id = paper.entry_id.split('/')[-1]
    title = paper.title
    abstract = paper.summary
    authors = ", ".join([author.name for author in paper.authors])
    published_date = paper.published.isoformat() if paper.published else None
    categories = ", ".join(paper.categories)
    pdf_url = paper.pdf_url
    ingested_at = datetime.now().isoformat()
    
    try:
        cursor.execute("""
            INSERT INTO papers (arxiv_id, title, abstract, authors, published_date, 
                              categories, pdf_url, ingested_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (arxiv_id, title, abstract, authors, published_date, categories, pdf_url, ingested_at))
        
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        # Paper already exists
        return None


def generate_embedding(text, client):
    """Generate embedding for text using OpenAI API."""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def store_embedding(conn, paper_id, embedding):
    """Store embedding for a paper."""
    cursor = conn.cursor()
    
    # Convert embedding list to bytes
    import pickle
    embedding_bytes = pickle.dumps(embedding)
    
    cursor.execute("""
        INSERT OR REPLACE INTO embeddings (paper_id, embedding)
        VALUES (?, ?)
    """, (paper_id, embedding_bytes))
    
    conn.commit()


def main():
    """Main ingestion pipeline."""
    print("Starting arXiv ingestion pipeline...")
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your API key.")
        return
    
    client = OpenAI()
    
    # Initialize database
    conn = init_db()
    
    # Fetch papers
    papers = fetch_arxiv_papers(max_results=1000)
    
    # Store papers and generate embeddings
    print("\nStoring papers and generating embeddings...")
    stored_count = 0
    skipped_count = 0
    
    for i, paper in enumerate(papers):
        paper_id = store_paper(conn, paper)
        
        if paper_id:
            # Generate and store embedding for abstract
            try:
                embedding = generate_embedding(paper.summary, client)
                store_embedding(conn, paper_id, embedding)
                stored_count += 1
                
                if stored_count % 50 == 0:
                    print(f"  Processed {stored_count} papers (skipped {skipped_count} duplicates)...")
            except Exception as e:
                print(f"  Error generating embedding for paper {paper_id}: {e}")
        else:
            skipped_count += 1
    
    conn.close()
    
    print(f"\nIngestion complete!")
    print(f"  Stored: {stored_count} papers")
    print(f"  Skipped: {skipped_count} duplicates")
    print(f"  Database: papers.db")


if __name__ == "__main__":
    main()
