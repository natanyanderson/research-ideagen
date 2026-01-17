import sqlite3
import openai
import os
import json
import numpy as np
from dotenv import load_dotenv
import sys
import re

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def evaluate_idea(idea, conn):
    """Evaluate a single idea and return scores"""
    # Get idea embedding
    response = openai.embeddings.create(
        input=idea,
        model="text-embedding-3-small"
    )
    idea_embedding = response.data[0].embedding
    
    # Calculate novelty via corpus similarity
    cursor = conn.cursor()
    cursor.execute("SELECT embedding FROM embeddings")
    similarities = []
    for row in cursor.fetchall():
        emb = json.loads(row[0].decode())
        sim = cosine_similarity(idea_embedding, emb)
        similarities.append(sim)
    
    max_similarity = np.max(similarities)
    
    # Determine novelty score
    if max_similarity < 0.40:
        novelty_score = 5
    elif max_similarity < 0.50:
        novelty_score = 4
    elif max_similarity < 0.60:
        novelty_score = 3
    elif max_similarity < 0.70:
        novelty_score = 2
    else:
        novelty_score = 1
    
    # Use LLM to evaluate other criteria
    eval_prompt = f"""Rate this research idea on four criteria (1-5 scale):

Research Idea: {idea}

Respond in this exact format:
Feasibility: [1-5]
Impact: [1-5]
Clarity: [1-5]
Grounding: [1-5]
"""
    
    eval_response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": eval_prompt}],
        temperature=0.3
    )
    
    llm_eval = eval_response.choices[0].message.content
    
    feasibility = int(re.search(r'Feasibility:\s*(\d)', llm_eval).group(1))
    impact = int(re.search(r'Impact:\s*(\d)', llm_eval).group(1))
    clarity = int(re.search(r'Clarity:\s*(\d)', llm_eval).group(1))
    grounding = int(re.search(r'Grounding:\s*(\d)', llm_eval).group(1))
    
    overall = (novelty_score + feasibility + impact + clarity + grounding) / 5.0
    
    return {
        'idea': idea,
        'novelty': novelty_score,
        'feasibility': feasibility,
        'impact': impact,
        'clarity': clarity,
        'grounding': grounding,
        'overall': overall,
        'max_similarity': max_similarity
    }

def generate_ideas(topic, conn, num_ideas=5, excluded_ideas=None):
    """Generate research ideas for a topic"""
    # Get top 5 related papers
    response = openai.embeddings.create(
        input=topic,
        model="text-embedding-3-small"
    )
    topic_embedding = response.data[0].embedding
    
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
    
    results.sort(reverse=True, key=lambda x: x[0])
    top_papers = results[:5]
    
    # Build context
    context = f"Topic: {topic}\n\nTop related papers:\n"
    for i, (score, title, abstract) in enumerate(top_papers, 1):
        context += f"\n{i}. {title} (similarity: {score:.3f})\n"
        context += f"   Abstract: {abstract[:200]}...\n"
    
    # Add exclusion clause if needed
    exclusion = ""
    if excluded_ideas:
        exclusion = f"\n\nAvoid these ideas (already generated):\n"
        for idx, idea in enumerate(excluded_ideas, 1):
            exclusion += f"{idx}. {idea}\n"
    
    # Generate ideas
    prompt = f"""Generate {num_ideas} novel research ideas based on the topic and related work.

{context}{exclusion}

Requirements:
- Address real gaps, not just "apply X to Y"
- Be specific and actionable
- Build meaningfully on existing work
- Avoid simple domain transfer

Format each as:
[Idea number]. [Title]: [One sentence description]
"""
    
    chat_response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )
    
    # Parse ideas
    ideas_text = chat_response.choices[0].message.content
    ideas = []
    for line in ideas_text.split('\n'):
        if re.match(r'^\d+\.', line.strip()):
            idea = re.sub(r'^\d+\.\s*', '', line.strip())
            ideas.append(idea)
    
    return ideas

if len(sys.argv) < 2:
    print("Usage: python generate_and_refine.py 'your research topic'")
    sys.exit(1)

topic = " ".join(sys.argv[1:])

print(f"Generating and refining research ideas for: {topic}")
print("=" * 70)
print()

conn = sqlite3.connect("papers.db")

good_ideas = []
all_generated = []
iteration = 0
max_iterations = 5

while len(good_ideas) < 3 and iteration < max_iterations:
    iteration += 1
    print(f"Iteration {iteration}:")
    print("-" * 70)
    
    # Generate ideas
    ideas = generate_ideas(topic, conn, num_ideas=5, excluded_ideas=all_generated)
    all_generated.extend(ideas)
    
    # Evaluate each idea
    for i, idea in enumerate(ideas, 1):
        print(f"\nEvaluating idea {i}: {idea[:60]}...")
        scores = evaluate_idea(idea, conn)
        
        print(f"  Novelty: {scores['novelty']}/5 (max_sim: {scores['max_similarity']:.3f})")
        print(f"  Overall: {scores['overall']:.1f}/5")
        
        # Check if it passes threshold
        if scores['overall'] >= 3.5 and scores['novelty'] >= 2:
            print(f"  ✓ ACCEPTED")
            good_ideas.append(scores)
        else:
            print(f"  ✗ REJECTED (overall: {scores['overall']:.1f}, novelty: {scores['novelty']})")
    
    print(f"\nGood ideas so far: {len(good_ideas)}/3")
    print()

conn.close()

print("=" * 70)
print("FINAL RESULTS")
print("=" * 70)
print()

for i, idea_scores in enumerate(good_ideas[:3], 1):
    print(f"{i}. {idea_scores['idea']}")
    print(f"   Overall: {idea_scores['overall']:.1f}/5")
    print(f"   Novelty: {idea_scores['novelty']}/5, Feasibility: {idea_scores['feasibility']}/5")
    print(f"   Impact: {idea_scores['impact']}/5, Clarity: {idea_scores['clarity']}/5, Grounding: {idea_scores['grounding']}/5")
    print()
