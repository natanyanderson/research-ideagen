import sqlite3
import openai
import os
import json
import numpy as np
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Topics to check for gaps
topics = [
    "retrieval augmented generation",
    "automated scientific discovery",
    "AI for hypothesis generation",
    "multi-agent research systems",
    "computational creativity",
    "literature-based discovery",
    "research idea evaluation",
    "scientific workflow automation",
    "knowledge graph reasoning",
    "cross-domain synthesis"
]

print("Analyzing topic coverage in corpus...\n")

# Connect to database once
conn = sqlite3.connect("papers.db")
cursor = conn.cursor()

# Load all embeddings once
cursor.execute("""
    SELECT e.embedding
    FROM embeddings e
""")
corpus_embeddings = [json.loads(row[0].decode()) for row in cursor.fetchall()]
conn.close()

results = []
for topic in topics:
    # Generate embedding for topic
    response = openai.embeddings.create(
        input=topic,
        model="text-embedding-3-small"
    )
    topic_embedding = response.data[0].embedding
    
    # Calculate similarities
    similarities = [cosine_similarity(topic_embedding, emb) for emb in corpus_embeddings]
    
    avg_sim = np.mean(similarities)
    max_sim = np.max(similarities)
    
    results.append({
        'topic': topic,
        'avg_similarity': avg_sim,
        'max_similarity': max_sim
    })

# Sort by average similarity (ascending) to find gaps
results.sort(key=lambda x: x['avg_similarity'])

print("=" * 70)
print("POTENTIAL RESEARCH GAPS (lowest coverage first)")
print("=" * 70)
print()

for i, r in enumerate(results, 1):
    gap_indicator = "🔴 HIGH GAP" if r['avg_similarity'] < 0.30 else "🟡 MODERATE GAP" if r['avg_similarity'] < 0.35 else "🟢 WELL COVERED"
    print(f"{i}. {r['topic']}")
    print(f"   Avg similarity: {r['avg_similarity']:.3f} | Max similarity: {r['max_similarity']:.3f}")
    print(f"   {gap_indicator}")
    print()
