import sqlite3
import openai
import os
from dotenv import load_dotenv
import numpy as np

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")

client = openai.OpenAI(api_key=OPENAI_API_KEY)
DATABASE_NAME = "papers.db"

# Topics to analyze for gaps
RESEARCH_TOPICS = [
    "retrieval augmented generation",
    "multi-agent research systems",
    "automated scientific discovery",
    "AI for hypothesis generation",
    "research idea evaluation",
    "scientific workflow automation",
    "computational creativity",
    "literature-based discovery",
    "cross-domain synthesis",
    "knowledge graph reasoning"
]

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

def identify_gaps():
    """
    Identifies research gaps by analyzing topic coverage in the corpus.
    """
    # Check if database exists
    if not os.path.exists(DATABASE_NAME):
        print(f"❌ Database not found: {DATABASE_NAME}")
        print("Please run 'python src/ingest_arxiv.py' first to populate the database.")
        return
    
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT embedding FROM embeddings")
        corpus_embeddings_blob = cursor.fetchall()
    except sqlite3.OperationalError as e:
        print(f"❌ Database error: {e}")
        conn.close()
        return
    
    conn.close()

    if not corpus_embeddings_blob:
        print("❌ No embeddings found in the database. Please run ingest_arxiv.py first.")
        return

    corpus_embeddings = [np.frombuffer(b[0], dtype=np.float32) for b in corpus_embeddings_blob]

    print("Analyzing topic coverage in corpus...")
    print("=" * 70)
    
    gap_analysis_results = []

    for topic in RESEARCH_TOPICS:
        topic_embedding = get_embedding(topic)
        if topic_embedding is None:
            print(f"⚠️  Skipping topic '{topic}' due to embedding failure.")
            continue

        similarities = [cosine_similarity(topic_embedding, ce) for ce in corpus_embeddings]
        
        avg_similarity = np.mean(similarities) if similarities else 0
        max_similarity = np.max(similarities) if similarities else 0

        gap_analysis_results.append({
            "topic": topic,
            "avg_similarity": avg_similarity,
            "max_similarity": max_similarity
        })
    
    # Sort by average similarity to find the least covered (biggest gaps)
    gap_analysis_results.sort(key=lambda x: x["avg_similarity"])

    print("\nPOTENTIAL RESEARCH GAPS (lowest coverage first)")
    print("=" * 70)

    for i, result in enumerate(gap_analysis_results):
        if result["avg_similarity"] < 0.30:
            gap_indicator = "🔴 HIGH GAP"
        elif result["avg_similarity"] < 0.35:
            gap_indicator = "🟡 MODERATE GAP"
        else:
            gap_indicator = "🟢 WELL COVERED"
            
        print(f"\n{i+1}. {result['topic']}")
        print(f"   Avg similarity: {result['avg_similarity']:.3f} | Max similarity: {result['max_similarity']:.3f}")
        print(f"   {gap_indicator}")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    try:
        identify_gaps()
    except Exception as e:
        print(f"❌ Error: {e}")
