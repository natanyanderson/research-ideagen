"""
Research Idea Generator
Generates novel research ideas based on gaps in the literature.

Usage:
    python src/generate_ideas.py "topic"
"""
import sys
import json
from openai import OpenAI
from dotenv import load_dotenv
from search_papers import search
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_ideas(topic, num_ideas=3):
    """Generate research ideas grounded in literature gaps."""
    # Pull related papers
    related = search(topic, top_k=5)
    
    papers_context = "\n".join([
        f"- {r['title']} (similarity: {r['similarity']:.3f}): {r['abstract']}"
        for r in related
    ])
    
    prompt = f"""Based on the following research papers related to "{topic}", 
generate {num_ideas} novel research ideas. Each idea should:
1. Address a gap not covered by existing papers
2. Be specific and actionable
3. Have clear potential for contribution

Related papers:
{papers_context}

For each idea, provide:
- Title (one line)
- Description (one sentence)
- Why it's novel (one sentence)

Format as numbered list."""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )
    
    return response.choices[0].message.content


if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "research idea evaluation"
    print(f"Generating ideas for: \"{topic}\"\n")
    ideas = generate_ideas(topic)
    print(ideas)
