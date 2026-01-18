import sqlite3
import openai
import os
from dotenv import load_dotenv
import numpy as np
import sys
import re

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

def calculate_novelty_score(idea_embedding):
    """
    Calculates a novelty score based on semantic similarity to the corpus.
    1 (not novel) to 5 (highly novel).
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT embedding FROM embeddings")
    corpus_embeddings_blob = cursor.fetchall()
    conn.close()

    if not corpus_embeddings_blob:
        return 0, 0.0, 0.0

    corpus_embeddings = [np.frombuffer(b[0], dtype=np.float32) for b in corpus_embeddings_blob]
    
    similarities = [cosine_similarity(idea_embedding, ce) for ce in corpus_embeddings]
    max_similarity = np.max(similarities) if similarities else 0.0
    avg_similarity = np.mean(similarities) if similarities else 0.0

    # Map similarity to novelty score (inverse relationship)
    if max_similarity > 0.75:
        novelty_score = 1
    elif max_similarity > 0.65:
        novelty_score = 2
    elif max_similarity > 0.55:
        novelty_score = 3
    elif max_similarity > 0.45:
        novelty_score = 4
    else:
        novelty_score = 5
    
    return novelty_score, max_similarity, avg_similarity

def evaluate_idea(idea_description):
    """
    Evaluates a research idea based on predefined criteria using an LLM and corpus similarity.
    """
    # Check if database exists
    if not os.path.exists(DATABASE_NAME):
        print(f"❌ Database not found: {DATABASE_NAME}")
        print("Please run 'python src/ingest_arxiv.py' first to populate the database.")
        return None
    
    print(f"Evaluating idea: {idea_description}")
    print("=" * 70)

    idea_embedding = get_embedding(idea_description)
    if idea_embedding is None:
        print("❌ Could not generate embedding for the idea.")
        return None

    novelty_score, max_sim, avg_sim = calculate_novelty_score(idea_embedding)

    prompt = f"""You are an expert research evaluator. Rate the following research idea on a scale of 1 to 5 for Feasibility, Impact, Clarity, and Grounding.

Research Idea: "{idea_description}"

Criteria:
- **Feasibility (1-5)**: Can this research realistically be done with current methods and resources? (1=impossible, 5=highly feasible)
- **Impact (1-5)**: Would this research matter if successful? (1=low impact, 5=high impact)
- **Clarity (1-5)**: Is the idea well-defined and testable? (1=vague, 5=very clear)
- **Grounding (1-5)**: Is it supported by existing literature or established concepts? (1=ungrounded, 5=strongly grounded)

Provide your response in the following format:
Feasibility: [score]
Impact: [score]
Clarity: [score]
Grounding: [score]
Brief justification: [Your justification]
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful research evaluator."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
        )
        eval_text = response.choices[0].message.content.strip()
        
        # Parse LLM scores
        llm_scores = {}
        justification = ""
        for line in eval_text.split('\n'):
            if "Feasibility:" in line:
                match = re.search(r'\d+', line)
                if match:
                    llm_scores["Feasibility"] = int(match.group())
            elif "Impact:" in line:
                match = re.search(r'\d+', line)
                if match:
                    llm_scores["Impact"] = int(match.group())
            elif "Clarity:" in line:
                match = re.search(r'\d+', line)
                if match:
                    llm_scores["Clarity"] = int(match.group())
            elif "Grounding:" in line:
                match = re.search(r'\d+', line)
                if match:
                    llm_scores["Grounding"] = int(match.group())
            elif "Brief justification:" in line or "Justification:" in line:
                justification = line.split(":", 1)[1].strip() if ":" in line else ""

        # Calculate overall score
        total_score = (novelty_score + llm_scores.get("Feasibility", 0) + 
                       llm_scores.get("Impact", 0) + llm_scores.get("Clarity", 0) + 
                       llm_scores.get("Grounding", 0))
        overall_score = total_score / 5.0

        print("\nIDEA EVALUATION")
        print("=" * 70)
        print(f"NOVELTY: {novelty_score}/5")
        print(f"  Max similarity to corpus: {max_sim:.3f}")
        print(f"  Avg similarity to corpus: {avg_sim:.3f}")
        print(f"\nFeasibility: {llm_scores.get('Feasibility', 'N/A')}/5")
        print(f"Impact: {llm_scores.get('Impact', 'N/A')}/5")
        print(f"Clarity: {llm_scores.get('Clarity', 'N/A')}/5")
        print(f"Grounding: {llm_scores.get('Grounding', 'N/A')}/5")
        if justification:
            print(f"\nJustification: {justification}")
        print("\n" + "=" * 70)
        print(f"OVERALL SCORE: {overall_score:.1f}/5.0")
        print("=" * 70)
        
        return {
            "novelty": novelty_score,
            "feasibility": llm_scores.get("Feasibility"),
            "impact": llm_scores.get("Impact"),
            "clarity": llm_scores.get("Clarity"),
            "grounding": llm_scores.get("Grounding"),
            "overall_score": overall_score,
            "justification": justification,
            "max_similarity": max_sim,
            "avg_similarity": avg_sim
        }

    except openai.APIError as e:
        print(f"❌ OpenAI API Error: {e}")
        return None
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/evaluate_idea.py \"Your research idea description\"")
        sys.exit(1)
    
    idea_text = " ".join(sys.argv[1:])
    try:
        evaluate_idea(idea_text)
    except Exception as e:
        print(f"❌ Error: {e}")
