import sqlite3
import openai
import os
from dotenv import load_dotenv
import numpy as np
import sys

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")

client = openai.OpenAI(api_key=OPENAI_API_KEY)
DATABASE_NAME = "papers.db"

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

def get_top_n_papers(query_embedding, top_n=5):
    """Retrieves the top N most semantically similar papers from the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT p.paper_id, p.title, p.abstract, e.embedding FROM papers p JOIN embeddings e ON p.paper_id = e.paper_id")
    papers_data = cursor.fetchall()
    conn.close()

    similarities = []
    for paper_id, title, abstract, embedding_blob in papers_data:
        paper_embedding = np.frombuffer(embedding_blob, dtype=np.float32)
        similarity = cosine_similarity(query_embedding, paper_embedding)
        similarities.append((similarity, paper_id, title, abstract))

    similarities.sort(key=lambda x: x[0], reverse=True)
    return similarities[:top_n]

def generate_ideas(topic):
    """
    Generates research ideas based on a topic, using top related papers as context.
    """
    # Check if database exists
    if not os.path.exists(DATABASE_NAME):
        print(f"❌ Database not found: {DATABASE_NAME}")
        print("Please run 'python src/ingest_arxiv.py' first to populate the database.")
        return
    
    print(f"Generating research ideas for: {topic}")
    print("=" * 70)

    topic_embedding = get_embedding(topic)
    if topic_embedding is None:
        print("❌ Could not generate embedding for the topic.")
        return

    top_papers = get_top_n_papers(topic_embedding, top_n=5)
    
    if not top_papers:
        print("❌ No papers found in database.")
        return
    
    context_papers = ""
    for i, (sim, paper_id, title, abstract) in enumerate(top_papers):
        context_papers += f"Paper {i+1} (Similarity: {sim:.3f}):\n"
        context_papers += f"Title: {title}\n"
        context_papers += f"Abstract: {abstract[:300]}...\n\n"

    prompt = f"""You are an expert research assistant. Your task is to generate novel and feasible research ideas based on the provided topic and relevant scientific papers.

Topic: "{topic}"

Relevant Papers (for context and inspiration):
{context_papers}

Based on the topic and the context from these papers, generate 3 distinct research ideas. Each idea should be a single sentence, clearly stating the core concept. Focus on identifying gaps, extending existing work, or combining concepts in novel ways.

Format your response as:
1. [Idea Title]: [One sentence description]
2. [Idea Title]: [One sentence description]
3. [Idea Title]: [One sentence description]
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful research assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
        )
        ideas_raw = response.choices[0].message.content.strip()

        print("\nGENERATED RESEARCH IDEAS")
        print("=" * 70)
        print(ideas_raw)
        print("=" * 70)

    except openai.APIError as e:
        print(f"❌ OpenAI API Error: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/generate_ideas.py \"your research topic\"")
        sys.exit(1)
    
    topic_text = " ".join(sys.argv[1:])
    try:
        generate_ideas(topic_text)
    except Exception as e:
        print(f"❌ Error: {e}")
