# Research IdeaGen

An agentic system for generating novel research ideas from scientific literature.

## Overview

This project builds a pipeline to automatically generate, evaluate, and refine research ideas by analyzing academic papers. It uses semantic search over a corpus of arXiv papers to identify gaps in the literature and propose novel research directions.

## What We've Built

### 1. Literature Ingestion (`src/ingest_arxiv.py`)
- Fetches the most recent CS papers from arXiv
- Stores metadata in SQLite database
- Generates embeddings for abstracts using OpenAI's `text-embedding-3-small`
- Default: 1000 most recent papers

### 2. Semantic Search (`src/search_papers.py`)
- Query the corpus using natural language
- Returns top 10 most similar papers with similarity scores
- Useful for verifying embeddings and exploring coverage

### 3. Gap Identification (`src/identify_gaps.py`)
- Analyzes topic coverage across the corpus
- Computes average similarity for predefined research topics
- Identifies underrepresented areas (potential research gaps)

### 4. Idea Generation (`src/generate_ideas.py`)
- Takes a research topic as input
- Finds top 5 related papers from corpus
- Uses GPT-4 to generate 3 novel research ideas grounded in existing work

### 5. Idea Evaluation (`src/evaluate_idea.py`)
- Scores research ideas on 5 criteria (1-5 scale):
  - **Novelty**: Dual scoring approach (takes max of two):
    - Semantic similarity to corpus (lower similarity = higher novelty)
    - LLM-based application novelty (assesses whether idea applies established methods to novel domains)
  - **Feasibility**: Can it be done with current methods?
  - **Impact**: Would it matter if successful?
  - **Clarity**: Is it well-defined and testable?
  - **Grounding**: Is it based on solid reasoning?
- Returns overall score (average of 5 criteria)
- The dual novelty approach catches both truly novel methods AND novel applications of known methods

### 6. Generate-Eval-Refine Pipeline (`src/generate_and_refine.py`)
- Iteratively generates and evaluates ideas
- Rejects ideas with overall < 3.5 or novelty < 2
- Continues until 3 solid ideas are found
- Avoids regenerating similar ideas

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_key_here
```

3. Ingest papers:
```bash
python src/ingest_arxiv.py
```

## Usage

### Search the corpus
```bash
python src/search_papers.py "your query"
```

### Identify gaps
```bash
python src/identify_gaps.py
```

### Generate ideas
```bash
python src/generate_ideas.py "your research topic"
```

### Evaluate an idea
```bash
python src/evaluate_idea.py "your research idea description"
```

### Full pipeline (generate + evaluate + refine)
```bash
python src/generate_and_refine.py "your research topic"
```

## Key Findings

- **Research idea evaluation** has the lowest coverage (avg similarity: 0.198)
- Well-covered topics like RAG tend to produce more optimization-focused ideas
- Underexplored topics tend to produce more "apply X to Y" ideas (which would score lower on pure similarity-based novelty)
- **Dual novelty scoring** successfully addresses the limitation of pure similarity metrics:
  - Pure similarity can miss ideas that apply established methods to novel domains
  - Application-based LLM check catches domain transfer novelty
  - Final novelty score is max(similarity score, application score)
- The pipeline successfully filters weak ideas and converges on novel, well-grounded research directions

## Current Corpus

- 1000 most recent CS papers from arXiv
- Stored in `papers.db` (SQLite)
- Abstracts embedded with `text-embedding-3-small` (float32 format)

## Next Steps

- Expand corpus (more papers, other sources like Semantic Scholar)
- Add citation network analysis
- Improve idea generation to avoid domain transfer patterns
- Build research plan generator (inspired by AI Co-Scientists paper)
- Human evaluation of generated ideas
