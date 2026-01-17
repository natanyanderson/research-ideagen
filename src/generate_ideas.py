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
    print("Usage: python generate_ideas.py 'your research topic'")
    sys.exit(1)

topic = " ".join(sys.argv[1:])

print(f"Generating research ideas for: {topic}\n")

# Get topic embedding
response = openai.embeddings.create(
    input=topic,
    model="text-embedding-3-small"
)
topic_embedding = response.data[0].embedding

# Find top 5 related papers
conn = sqlite3.connect("papers.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT p.title, p.abstract, e.embedding
    FROM papers p
    JOIN embeddings e ON p.arxiv_id = e.arxiv_id
""")

results = []
for row in cursor.fetchall():
    title, abstract, embedding_bytes = row
    embedding = json.loads(embedding_bytes.decode())
    similarity = cosine_similarity(topic_embedding, embedding)
    results.append((similarity, title, abstract))

conn.close()

results.sort(reverse=True, key=lambda x: x[0])
top_papers = results[:5]

# Build context
context = f"Topic: {topic}\n\nTop related papers:\n"
for i, (score, title, abstract) in enumerate(top_papers, 1):
    context += f"\n{i}. {title} (similarity: {score:.3f})\n"
    context += f"   Abstract: {abstract[:200]}...\n"

# Generate ideas
prompt = f"""You are a research assistant helping generate novel research ideas.

{context}

Based on the topic and related work above, generate 3 novel research ideas. Each idea should:
- Address a gap or unexplored area
- Build on or extend the existing work
- Be feasible with current methods

Format your response as:
1. [Idea Title]
Description: [One sentence describing the research idea]

2. [Idea Title]
Description: [One sentence describing the research idea]

3. [Idea Title]
Description: [One sentence describing the research idea]
"""

chat_response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.8
)

print("=" * 70)
print("GENERATED RESEARCH IDEAS")
print("=" * 70)
print()
print(chat_response.choices[0].message.content)
