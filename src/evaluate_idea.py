"""
Research Idea Evaluator
Scores ideas on novelty, feasibility, and impact using dual novelty scoring.

Dual novelty scoring:
  1. Corpus-based: semantic distance from existing papers (lower sim = more novel)
  2. Application-based: LLM check for whether the method is novel vs just domain transfer

Final novelty = max(corpus_novelty, application_novelty)

Usage:
    python src/evaluate_idea.py "idea description"
"""
import sys
import json
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
    """Score novelty based on semantic distance from existing corpus."""
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
    
    # Convert similarity to novelty score (1-5)
    # Lower similarity = higher novelty
    if max_sim < 0.3:
        return 5.0
    elif max_sim < 0.4:
        return 4.0
    elif max_sim < 0.5:
        return 3.0
    elif max_sim < 0.6:
        return 2.0
    else:
        return 1.0


def assess_application_novelty(idea_text):
    """LLM-based check: is the METHOD novel or just the APPLICATION domain?
    
    This catches cases like 'apply transformers to protein folding' where
    the corpus-based scorer would rate it as novel (because there are few
    protein folding papers in CS) but the method itself is well-established.
    """
    prompt = f"""Evaluate this research idea for methodological novelty:

"{idea_text}"

Question: Is this idea proposing a genuinely novel METHOD or approach, 
or is it primarily applying an established/well-known method to a new domain?

Score 1-5:
1 = purely applying established method to new domain (e.g., "use BERT for legal docs")
2 = mostly domain transfer with minor methodological tweaks
3 = meaningful methodological extension, not just domain transfer
4 = novel combination of methods or fresh approach
5 = fundamentally new method or paradigm

Respond with just the score (number only)."""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=10
    )
    
    try:
        score = float(response.choices[0].message.content.strip())
        return min(max(score, 1.0), 5.0)
    except ValueError:
        return 3.0


def evaluate_feasibility(idea_text):
    """Score feasibility using LLM."""
    prompt = f"""Rate the feasibility of this research idea (1-5):
"{idea_text}"
1=infeasible, 5=straightforward. Respond with just the number."""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=10
    )
    try:
        return float(response.choices[0].message.content.strip())
    except ValueError:
        return 3.0


def evaluate_impact(idea_text):
    """Score potential impact using LLM."""
    prompt = f"""Rate the potential impact of this research idea (1-5):
"{idea_text}"
1=minimal, 5=transformative. Respond with just the number."""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=10
    )
    try:
        return float(response.choices[0].message.content.strip())
    except ValueError:
        return 3.0


def evaluate(idea_text):
    """Full evaluation with dual novelty scoring."""
    print(f"Evaluating: \"{idea_text[:80]}...\"\n")
    
    corpus_novelty = assess_corpus_novelty(idea_text)
    app_novelty = assess_application_novelty(idea_text)
    final_novelty = max(corpus_novelty, app_novelty)
    
    feasibility = evaluate_feasibility(idea_text)
    impact = evaluate_impact(idea_text)
    
    overall = (final_novelty + feasibility + impact) / 3
    passed = final_novelty >= NOVELTY_THRESHOLD
    
    print(f"Corpus novelty:      {corpus_novelty}/5")
    print(f"Application novelty: {app_novelty}/5")
    print(f"Final novelty:       {final_novelty}/5 (max of both)")
    print(f"Feasibility:         {feasibility}/5")
    print(f"Impact:              {impact}/5")
    print(f"Overall:             {overall:.1f}/5")
    print(f"Status:              {'PASS' if passed else 'FAIL'} (threshold: {NOVELTY_THRESHOLD})")
    
    return {
        "corpus_novelty": corpus_novelty,
        "application_novelty": app_novelty,
        "final_novelty": final_novelty,
        "feasibility": feasibility,
        "impact": impact,
        "overall": overall,
        "passed": passed
    }


if __name__ == "__main__":
    idea = sys.argv[1] if len(sys.argv) > 1 else "Apply RL to agricultural yield optimization"
    evaluate(idea)
