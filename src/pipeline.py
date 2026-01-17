"""
Generate-Eval-Refine Pipeline
Generates ideas, evaluates them, rejects weak ones, and iterates until
we have enough high-quality ideas.

Usage:
    python src/pipeline.py "topic"
"""
import sys
import json
from generate_ideas import generate_ideas
from evaluate_idea import evaluate, NOVELTY_THRESHOLD
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TARGET_IDEAS = 3
MAX_ITERATIONS = 5
IDEAS_PER_ROUND = 5


def parse_ideas(raw_text):
    """Parse numbered list of ideas from LLM output."""
    ideas = []
    current = []
    
    for line in raw_text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        if line[0].isdigit() and (line[1] == '.' or (len(line) > 1 and line[1] == ')')):
            if current:
                ideas.append("\n".join(current))
            current = [line]
        else:
            current.append(line)
    
    if current:
        ideas.append("\n".join(current))
    
    return ideas


def run_pipeline(topic):
    """Run the full generate-eval-refine pipeline."""
    print(f"=" * 60)
    print(f"Pipeline: \"{topic}\"")
    print(f"Target: {TARGET_IDEAS} ideas above {NOVELTY_THRESHOLD} threshold")
    print(f"=" * 60)
    
    accepted = []
    rejected = []
    
    for iteration in range(1, MAX_ITERATIONS + 1):
        print(f"\n--- Iteration {iteration} ---")
        
        remaining = TARGET_IDEAS - len(accepted)
        if remaining <= 0:
            break
        
        print(f"Need {remaining} more idea(s)")
        raw = generate_ideas(topic, num_ideas=IDEAS_PER_ROUND)
        ideas = parse_ideas(raw)
        
        for idea in ideas:
            if len(accepted) >= TARGET_IDEAS:
                break
            
            print(f"\nEvaluating: {idea[:80]}...")
            scores = evaluate(idea)
            
            if scores["passed"]:
                accepted.append({"idea": idea, "scores": scores})
                print(f">>> ACCEPTED (novelty: {scores['final_novelty']})")
            else:
                rejected.append({"idea": idea, "scores": scores})
                print(f">>> REJECTED (novelty: {scores['final_novelty']})")
    
    print(f"\n{'=' * 60}")
    print(f"Pipeline complete!")
    print(f"Accepted: {len(accepted)} | Rejected: {len(rejected)}")
    print(f"Iterations: {iteration}")
    print(f"{'=' * 60}")
    
    for i, item in enumerate(accepted, 1):
        print(f"\n{i}. {item['idea'][:100]}")
        s = item['scores']
        print(f"   Novelty: {s['final_novelty']} | Feasibility: {s['feasibility']} | Impact: {s['impact']}")
    
    return accepted


if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "automated research ideation from literature"
    run_pipeline(topic)
