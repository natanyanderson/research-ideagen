# Research IdeaGen

Agentic system for generating and evaluating research ideas from scientific literature.

## Scripts

| Script | Description |
|--------|-------------|
| `src/ingest_arxiv.py` | Fetches CS papers from arXiv, stores with embeddings |
| `src/search_papers.py` | Semantic search over paper corpus |
| `src/gap_finder.py` | Identifies underrepresented research topics |
| `src/generate_ideas.py` | Generates research ideas from literature gaps |
| `src/evaluate_idea.py` | Scores idea novelty via corpus similarity |
| `src/pipeline.py` | Generate-eval-refine loop |

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your OpenAI API key
python src/ingest_arxiv.py
python src/pipeline.py "your topic"
```

## Key Finding
Biggest gap: "research idea evaluation" (avg similarity: 0.31)
