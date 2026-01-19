# Pipeline Demo Script (5 min)

For advisor meeting — walkthrough of the research ideation pipeline.

## Section 1: Setup (30 sec)
- Show the repo structure
- Mention: 1000 CS papers ingested from arXiv (2024-2026)
- DB is pre-loaded (ingestion takes ~25 min, skip for demo)

## Section 2: Semantic Search (45 sec)
- Run: `python src/search_papers.py "retrieval augmented generation"`
- Show top 5 results with similarity scores
- Point out: RAG has high coverage (0.575 top score)

## Section 3: Gap Identification (45 sec)
- Run: `python src/gap_finder.py`
- Show the ranked list of topics by gap size
- Highlight: "research idea evaluation" is the biggest gap (0.31 avg sim)
- This validates our project motivation

## Section 4: Idea Generation (45 sec)
- Run: `python src/generate_ideas.py "research idea evaluation"`
- Show 3 generated ideas
- Point out how they're grounded in the gap analysis

## Section 5: Dual Novelty Scoring (2 min)
**This is the key part — what advisor asked about last time.**

- Run: `python src/evaluate_idea.py "Apply RL to agricultural yield optimization"`
- Show BOTH scores:
  - Corpus novelty: ~4.2 (high — because few agriculture papers in CS)
  - Application novelty: ~1.8 (low — RL optimization is well-established)
  - Final: takes the max, but the LLM check correctly flags this as domain transfer

- Compare to: `python src/evaluate_idea.py "Framework for measuring how AI ideation tools affect human researchers"`
  - Corpus novelty: ~3.5
  - Application novelty: ~4.0
  - This IS methodologically novel

- **Key message**: Similarity alone would have rated the RL idea as more novel than the AI-tools idea. Dual scoring fixes this.

## Talking Points
- Why max of both scores: catches both types of novelty
- Temperature settings: 0.7 for generation, 0.3 for evaluation (less randomness in scoring)
- Next steps: experiment design, workshop paper
