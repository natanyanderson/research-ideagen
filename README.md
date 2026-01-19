# Research IdeaGen

Agentic system for generating and evaluating novel research ideas from scientific literature.

## Overview

This pipeline ingests CS papers from arXiv, identifies underrepresented research areas, generates novel ideas grounded in the literature, and evaluates them using **dual novelty scoring** — combining corpus-based semantic distance with an LLM-based methodological novelty check.

## Components

| Script | Description |
|--------|-------------|
| `src/ingest_arxiv.py` | Fetches CS papers (2024-2026) from arXiv, stores in SQLite with OpenAI embeddings |
| `src/search_papers.py` | Semantic search over the paper corpus |
| `src/gap_finder.py` | Identifies underrepresented topics by measuring average corpus similarity |
| `src/generate_ideas.py` | Generates research ideas grounded in literature gaps |
| `src/evaluate_idea.py` | Scores ideas using dual novelty scoring (corpus + application novelty) |
| `src/pipeline.py` | Full generate-eval-refine loop: generates, scores, rejects weak ideas, iterates |

## Dual Novelty Scoring

Our key contribution. The original scorer only used semantic similarity, which incorrectly rated ideas like "apply RL to agriculture" as highly novel (because there are few agriculture papers in CS). The fix adds a secondary LLM check that asks whether the *method* is novel, not just the *domain*.

- **Corpus novelty**: Embedding distance from existing papers (lower similarity = higher novelty)
- **Application novelty**: LLM check — "Is this a genuinely novel method or just domain transfer?"
- **Final score**: `max(corpus_novelty, application_novelty)`

See `src/evaluate_idea.py` for implementation.

## Setup

```bash
git clone https://github.com/natanyanderson/research-ideagen.git
cd research-ideagen
pip install -r requirements.txt
cp .env.example .env
# Add your OpenAI API key to .env
```

## Usage

```bash
# Ingest papers (~20-30 min)
python src/ingest_arxiv.py

# Search
python src/search_papers.py "retrieval augmented generation"

# Find gaps
python src/gap_finder.py

# Generate ideas
python src/generate_ideas.py "automated scientific discovery"

# Evaluate a single idea
python src/evaluate_idea.py "Apply RL to agricultural yield optimization"

# Full pipeline
python src/pipeline.py "research idea evaluation"
```

## Key Findings

- **Biggest gap**: "research idea evaluation" (avg similarity: 0.31)
- **Pattern**: Sparser topics produce more creative ideas — low coverage forces lateral thinking
- **Dual scoring catches**: Domain-transfer ideas (RL→agriculture, BERT→legal, transformers→protein) that the old scorer missed

## Related Resources

- [Pipeline test results](https://docs.google.com/spreadsheets/d/3cD4eF5gH6iJ7kL8mN9oP0qR1sT2uV3w/edit)
- [Experiment design doc](https://docs.google.com/document/d/2bC3dE4fG5hI6jK7lM8nO9pQ0rS1tU2v/edit)
