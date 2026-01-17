import arxiv
import sqlite3
import openai
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Database setup
conn = sqlite3.connect("papers.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS papers (
    arxiv_id TEXT PRIMARY KEY,
    title TEXT,
    authors TEXT,
    abstract TEXT,
    published TEXT,
    categories TEXT,
    pdf_url TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS embeddings (
    arxiv_id TEXT PRIMARY KEY,
    embedding BLOB,
    FOREIGN KEY (arxiv_id) REFERENCES papers (arxiv_id)
)
""")

conn.commit()

# Fetch CS papers from 2024-2025
client = arxiv.Client()
search = arxiv.Search(
    query="cat:cs.* AND submittedDate:[20240101 TO 20251231]",
    max_results=1000,
    sort_by=arxiv.SortCriterion.SubmittedDate
)

print("Fetching papers from arXiv...")
for i, paper in enumerate(client.results(search)):
    # Store paper metadata
    cursor.execute("""
        INSERT OR IGNORE INTO papers (arxiv_id, title, authors, abstract, published, categories, pdf_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        paper.entry_id.split('/')[-1],
        paper.title,
        ", ".join([author.name for author in paper.authors]),
        paper.summary,
        paper.published.isoformat(),
        ", ".join(paper.categories),
        paper.pdf_url
    ))
    
    # Generate embedding for abstract
    response = openai.embeddings.create(
        input=paper.summary,
        model="text-embedding-3-small"
    )
    embedding = response.data[0].embedding
    
    # Store embedding as bytes
    import json
    embedding_bytes = json.dumps(embedding).encode()
    cursor.execute("""
        INSERT OR IGNORE INTO embeddings (arxiv_id, embedding)
        VALUES (?, ?)
    """, (paper.entry_id.split('/')[-1], embedding_bytes))
    
    if (i + 1) % 50 == 0:
        print(f"Processed {i + 1} papers...")
        conn.commit()

conn.commit()
conn.close()
print("Ingestion complete!")
