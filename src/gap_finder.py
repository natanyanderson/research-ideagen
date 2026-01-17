"""
Gap Identification Script
Identifies underrepresented topics in the corpus by measuring average similarity.

Usage:
    python src/gap_finder.py
"""
import sqlite3
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DB_PATH = "papers.db"
EMBEDDING_MODEL = "text-embedding-3-small"

TOPICS = [
    "retrieval augmented generation",
    "automated scientific discovery",
    "AI safety and alignment",
    "code generation",
    "research idea evaluation",
    "knowledge graph construction",
    "multi-agent coordination",
    "AI experiment design",
    "prompt engineering",
    "model interpretability",
    "federated learning",
    "neural architecture search",
    "continual learning",
    "causal inference with ML",
    "AI for drug discovery",
    "robotics control",
    "natural language reasoning",
    "computer vision foundation models",
    "large language models",
    "reinforcement learning from human feedback"
]


def get_embedding(text):
    response = client.embeddings.create(
        input=text[:8000],
        model=EMBEDDING_MODEL
    )
    return np.array(response.data[0].embedding, dtype=np.float32)


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def analyze_gaps():
    """Compute avg similarity for each topic against the full corpus."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT embedding FROM papers")
    
    corpus_embeddings = []
    for row in c.fetchall():
        emb = np.frombuffer(row[0], dtype=np.float32)
        corpus_embeddings.append(emb)
    
    conn.close()
    
    print(f"Corpus size: {len(corpus_embeddings)} papers\n")
    print(f"{'Topic':<45} {'Avg Sim':>8} {'Gap Level':>12}")
    print("-" * 70)
    
    results = []
    for topic in TOPICS:
        topic_emb = get_embedding(topic)
        sims = [cosine_similarity(topic_emb, emb) for emb in corpus_embeddings]
        avg_sim = np.mean(sims)
        
        if avg_sim < 0.35:
            level = "HIGH GAP"
        elif avg_sim < 0.45:
            level = "MEDIUM GAP"
        else:
            level = "LOW GAP"
        
        results.append((topic, avg_sim, level))
    
    results.sort(key=lambda x: x[1])
    
    for topic, avg_sim, level in results:
        print(f"{topic:<45} {avg_sim:>8.3f} {level:>12}")
    
    print(f"\nBiggest gap: {results[0][0]} (avg sim: {results[0][1]:.3f})")


if __name__ == "__main__":
    analyze_gaps()
