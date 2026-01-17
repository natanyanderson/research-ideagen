"""
Research Idea Evaluator (v1)
Scores ideas on novelty (corpus similarity), feasibility, and impact.

Usage:
    python src/evaluate_idea.py "idea description"
"""
import sys
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from search_papers import search, get_embedding, cosine_similarity
import sqlite3
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DB_PATH = "papers.db"
NOVELTY_THRESHOLD = 3.5

def assess_corpus_novelty(idea_text):
    idea_emb = get_embedding(idea_text)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT embedding FROM papers")
    max_sim = 0
    for row in c.fetchall():
        paper_emb = np.frombuffer(row[0], dtype=np.float32)
        sim = cosine_similarity(idea_emb, paper_emb)
        max_sim = max(max_sim, sim)
    conn.close()
    if max_sim < 0.3: return 5.0
    elif max_sim < 0.4: return 4.0
    elif max_sim < 0.5: return 3.0
    elif max_sim < 0.6: return 2.0
    else: return 1.0

def evaluate(idea_text):
    novelty = assess_corpus_novelty(idea_text)
    print(f"Novelty: {novelty}/5")
    print(f"Status: {'PASS' if novelty >= NOVELTY_THRESHOLD else 'FAIL'}")
    return {"novelty": novelty, "passed": novelty >= NOVELTY_THRESHOLD}

if __name__ == "__main__":
    idea = sys.argv[1] if len(sys.argv) > 1 else "Apply RL to agricultural yield optimization"
    evaluate(idea)
