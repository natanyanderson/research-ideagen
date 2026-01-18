import sys
import time
import os
import re
from generate_ideas import get_top_n_papers, get_embedding
from evaluate_idea import evaluate_idea, calculate_novelty_score
import openai
from dotenv import load_dotenv
import numpy as np
import sqlite3

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")

client = openai.OpenAI(api_key=OPENAI_API_KEY)
DATABASE_NAME = "papers.db"

def cosine_similarity(vec1, vec2):
    """Computes the cosine similarity between two vectors."""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def generate_and_refine_ideas(topic, num_desired_ideas=3, max_iterations=5):
    """
    Generates, evaluates, and refines research ideas iteratively.
    """
    # Check if database exists
    if not os.path.exists(DATABASE_NAME):
        print(f"❌ Database not found: {DATABASE_NAME}")
        print("Please run 'python src/ingest_arxiv.py' first to populate the database.")
        return []
    
    print(f"Generating and refining research ideas for: {topic}")
    print("=" * 70)
    print(f"Target: {num_desired_ideas} high-quality ideas")
    print(f"Criteria: Overall score ≥ 3.5/5.0, Novelty ≥ 2/5")
    print("=" * 70)

    accepted_ideas = []
    iteration = 0

    while len(accepted_ideas) < num_desired_ideas and iteration < max_iterations:
        iteration += 1
        print(f"\nIteration {iteration}:")
        print("-" * 70)

        # Generate topic embedding and get related papers
        topic_embedding = get_embedding(topic)
        if topic_embedding is None:
            print("❌ Could not generate embedding for the topic. Exiting.")
            return []

        top_papers = get_top_n_papers(topic_embedding, top_n=5)
        
        context_papers = ""
        for i, (sim, paper_id, title, abstract) in enumerate(top_papers):
            context_papers += f"Paper {i+1} (Similarity: {sim:.3f}):\n"
            context_papers += f"Title: {title}\n"
            context_papers += f"Abstract: {abstract[:300]}...\n\n"

        generation_prompt = f"""You are an expert research assistant. Your task is to generate novel and feasible research ideas based on the provided topic and relevant scientific papers.

Topic: "{topic}"

Relevant Papers (for context and inspiration):
{context_papers}

Generate 5 distinct research ideas. Each idea should be a single sentence, clearly stating the core concept. Focus on identifying gaps, extending existing work, or combining concepts in novel ways. Avoid simple "apply X to Y" ideas.

Format each as:
1. [Idea]
2. [Idea]
3. [Idea]
4. [Idea]
5. [Idea]
"""
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful research assistant."},
                    {"role": "user", "content": generation_prompt}
                ],
                max_tokens=700,
                n=1,
                stop=None,
                temperature=0.8,
            )
            generated_ideas_raw = response.choices[0].message.content.strip()
            generated_ideas = []
            for line in generated_ideas_raw.split('\n'):
                line = line.strip()
                if re.match(r'^\d+\.', line):
                    idea = re.sub(r'^\d+\.\s*', '', line)
                    if idea:
                        generated_ideas.append(idea)

        except openai.APIError as e:
            print(f"❌ OpenAI API Error during idea generation: {e}")
            break
        except Exception as e:
            print(f"❌ An unexpected error occurred during idea generation: {e}")
            break

        if not generated_ideas:
            print("⚠️  No ideas generated in this iteration")
            continue

        for idea_description in generated_ideas:
            if len(accepted_ideas) >= num_desired_ideas:
                break

            print(f"\nEvaluating: \"{idea_description[:70]}...\"")
            eval_results = evaluate_idea(idea_description)

            if eval_results:
                novelty = eval_results["novelty"]
                overall_score = eval_results["overall_score"]

                if overall_score >= 3.5 and novelty >= 2:
                    print(f"  ✓ ACCEPTED (Overall: {overall_score:.1f}/5.0, Novelty: {novelty}/5)")
                    accepted_ideas.append({
                        "idea": idea_description,
                        "overall_score": overall_score,
                        "novelty": novelty,
                        "feasibility": eval_results["feasibility"],
                        "impact": eval_results["impact"],
                        "clarity": eval_results["clarity"],
                        "grounding": eval_results["grounding"]
                    })
                else:
                    print(f"  ✗ REJECTED (Overall: {overall_score:.1f}/5.0, Novelty: {novelty}/5)")
            
            time.sleep(0.5)

        print(f"\nGood ideas so far: {len(accepted_ideas)}/{num_desired_ideas}")
        time.sleep(1)

    print("\n" + "=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)
    
    if not accepted_ideas:
        print("\n⚠️  Could not generate enough high-quality ideas within the given iterations.")
        print("Consider:")
        print("  - Trying a different topic")
        print("  - Adjusting evaluation criteria")
        print("  - Increasing max_iterations")
    else:
        for i, idea_data in enumerate(accepted_ideas, 1):
            print(f"\n{i}. {idea_data['idea']}")
            print(f"   Overall: {idea_data['overall_score']:.1f}/5")
            print(f"   Novelty: {idea_data['novelty']}/5, Feasibility: {idea_data['feasibility']}/5")
            print(f"   Impact: {idea_data['impact']}/5, Clarity: {idea_data['clarity']}/5, Grounding: {idea_data['grounding']}/5")
    
    print("\n" + "=" * 70)
    return accepted_ideas

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/generate_and_refine.py \"your research topic\"")
        sys.exit(1)
    
    topic_text = " ".join(sys.argv[1:])
    try:
        generate_and_refine_ideas(topic_text)
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
