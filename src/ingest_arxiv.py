import arxiv
import sqlite3
import openai
import os
from dotenv import load_dotenv
import time
import numpy as np

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file. Please add it and try again.")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

DATABASE_NAME = "papers.db"
MAX_PAPERS = 1000
BATCH_SIZE = 50
ARXIV_QUERY = "cat:cs.*"
DATE_RANGE = "2024-01-01 TO 2025-12-31"

def get_embedding(text):
    """Generates an embedding for the given text using OpenAI's API."""
    text = text.replace("\n", " ")
    try:
        response = client.embeddings.create(input=[text], model="text-embedding-3-small")
        return response.data[0].embedding
    except openai.APIError as e:
        print(f"  ⚠️  OpenAI API Error: {e}")
        return None
    except Exception as e:
        print(f"  ⚠️  Unexpected error generating embedding: {e}")
        return None

def initialize_db():
    """Initializes the SQLite database and tables."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS papers (
            paper_id TEXT PRIMARY KEY,
            title TEXT,
            abstract TEXT,
            authors TEXT,
            published_date TEXT,
            arxiv_id TEXT UNIQUE,
            categories TEXT,
            url TEXT,
            pdf_url TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            paper_id TEXT PRIMARY KEY,
            embedding BLOB,
            FOREIGN KEY (paper_id) REFERENCES papers (paper_id)
        )
    """)
    conn.commit()
    conn.close()
    print(f"✓ Database initialized: {DATABASE_NAME}")

def fetch_and_store_papers():
    """Fetches papers from arXiv and stores them in the database with embeddings."""
    initialize_db()
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    search = arxiv.Search(
        query=ARXIV_QUERY,
        max_results=MAX_PAPERS,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    print(f"\nFetching up to {MAX_PAPERS} CS papers from arXiv ({DATE_RANGE})...")
    print("=" * 70)
    
    papers_to_process = []
    fetched_count = 0
    
    try:
        for result in search.results():
            published_year = result.published.year
            if not (2024 <= published_year <= 2025):
                if published_year < 2024:
                    break
                continue

            paper_id = result.entry_id.split('/')[-1]
            if 'v' in paper_id:
                paper_id = paper_id.split('v')[0]

            # Check if paper already exists
            cursor.execute("SELECT arxiv_id FROM papers WHERE arxiv_id = ?", (paper_id,))
            if cursor.fetchone():
                continue

            authors = ", ".join([a.name for a in result.authors])
            categories = ", ".join(result.categories)
            
            pdf_url = None
            for link in result.links:
                if link.title == "pdf":
                    pdf_url = link.href
                    break

            papers_to_process.append({
                "paper_id": paper_id,
                "title": result.title,
                "abstract": result.summary,
                "authors": authors,
                "published_date": result.published.isoformat(),
                "arxiv_id": paper_id,
                "categories": categories,
                "url": result.entry_id,
                "pdf_url": pdf_url
            })
            fetched_count += 1
            
            if fetched_count % 100 == 0:
                print(f"  Fetched {fetched_count} papers...")
            
            if fetched_count >= MAX_PAPERS:
                break

    except Exception as e:
        print(f"\n⚠️  Error during arXiv fetch: {e}")
        print("Continuing with papers fetched so far...")

    print(f"\n✓ Found {len(papers_to_process)} new papers to process")
    print("\nGenerating embeddings and storing papers...")
    print("=" * 70)

    stored_count = 0
    failed_count = 0
    
    for i in range(0, len(papers_to_process), BATCH_SIZE):
        batch = papers_to_process[i:i + BATCH_SIZE]
        for paper in batch:
            try:
                cursor.execute("""
                    INSERT INTO papers (paper_id, title, abstract, authors, published_date, arxiv_id, categories, url, pdf_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    paper["paper_id"],
                    paper["title"],
                    paper["abstract"],
                    paper["authors"],
                    paper["published_date"],
                    paper["arxiv_id"],
                    paper["categories"],
                    paper["url"],
                    paper["pdf_url"]
                ))
                
                embedding = get_embedding(paper["abstract"])
                if embedding:
                    cursor.execute("""
                        INSERT INTO embeddings (paper_id, embedding)
                        VALUES (?, ?)
                    """, (paper["paper_id"], np.array(embedding).tobytes()))
                    stored_count += 1
                else:
                    failed_count += 1
                    
            except sqlite3.IntegrityError:
                print(f"  ⚠️  Duplicate paper: {paper['paper_id']}, skipping")
            except Exception as e:
                print(f"  ⚠️  Error processing paper {paper['paper_id']}: {e}")
                failed_count += 1
                
        conn.commit()
        print(f"  Processed {min(stored_count + failed_count, len(papers_to_process))} / {len(papers_to_process)} papers")
        time.sleep(0.5)  # Rate limiting

    conn.close()
    
    print("\n" + "=" * 70)
    print("✓ Ingestion complete!")
    print(f"  Papers successfully stored: {stored_count}")
    if failed_count > 0:
        print(f"  Papers with errors: {failed_count}")
    print("=" * 70)

if __name__ == "__main__":
    try:
        fetch_and_store_papers()
    except KeyboardInterrupt:
        print("\n\n⚠️  Ingestion interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
