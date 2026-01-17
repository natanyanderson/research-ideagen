import sqlite3
import openai
import os
import json
import numpy as np
from dotenv import load_dotenv
import sys

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

if len(sys.argv) < 2:
    print("Usage: python evaluate_idea.py 'your research idea description'")
    sys.exit(1)

idea = " ".join(sys.argv[1:])

print(f"Evaluating idea: {idea}\n")

# Get idea embedding for novelty check
response = openai.embeddings.create(
    input=idea,
    model="text-embedding-3-small"
)
idea_embedding = response.data[0].embedding

# Calculate novelty via corpus similarity
conn = sqlite3.connect("papers.db")
cursor = conn.cursor()

cursor.execute("SELECT embedding FROM embeddings")
similarities = []
for row in cursor.fetchall():
    emb = json.loads(row[0].decode())
    sim = cosine_similarity(idea_embedding, emb)
    similarities.append(sim)

conn.close()

avg_similarity = np.mean(similarities)
max_similarity = np.max(similarities)

# Determine novelty score based on similarity
if max_similarity < 0.40:
    novelty_score = 5  # Very novel
elif max_similarity < 0.50:
    novelty_score = 4  # Novel
elif max_similarity < 0.60:
    novelty_score = 3  # Moderately novel
elif max_similarity < 0.70:
    novelty_score = 2  # Somewhat similar
else:
    novelty_score = 1  # Not novel

# Use LLM to evaluate other criteria
eval_prompt = f"""You are evaluating a research idea on four criteria. Rate each on a 1-5 scale.

Research Idea: {idea}

Rate the following (1=poor, 5=excellent):

1. FEASIBILITY: Can this be done with current methods and resources?
2. IMPACT: Would this matter if successful?
3. CLARITY: Is the idea well-defined and testable?
4. GROUNDING: Is it based on solid reasoning and existing work?

Respond in this exact format:
Feasibility: [1-5]
Impact: [1-5]
Clarity: [1-5]
Grounding: [1-5]
Brief justification: [2-3 sentences explaining your ratings]
"""

eval_response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": eval_prompt}],
    temperature=0.3
)

# Parse LLM response
llm_eval = eval_response.choices[0].message.content

print("=" * 70)
print("IDEA EVALUATION")
print("=" * 70)
print()
print(f"NOVELTY: {novelty_score}/5")
print(f"  Max similarity to corpus: {max_similarity:.3f}")
print(f"  Avg similarity to corpus: {avg_similarity:.3f}")
print()
print(llm_eval)
print()

# Extract scores for overall rating
import re
feasibility = int(re.search(r'Feasibility:\s*(\d)', llm_eval).group(1))
impact = int(re.search(r'Impact:\s*(\d)', llm_eval).group(1))
clarity = int(re.search(r'Clarity:\s*(\d)', llm_eval).group(1))
grounding = int(re.search(r'Grounding:\s*(\d)', llm_eval).group(1))

overall = (novelty_score + feasibility + impact + clarity + grounding) / 5.0

print("=" * 70)
print(f"OVERALL SCORE: {overall:.1f}/5.0")
print("=" * 70)
