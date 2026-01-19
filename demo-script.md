# Pipeline Demo Script (5 minutes)

## Overview
This demo walks through the literature-grounded research idea generation pipeline, showing corpus ingestion, semantic search, gap identification, idea generation, and evaluation with dual novelty scoring.

---

## Demo Flow

### 1. Introduction (30 seconds)
**Say:** "I've built a pipeline that generates research ideas grounded in existing literature. It uses ~1000 CS papers from arXiv, embeddings for semantic search, and LLM-based evaluation with a dual novelty check."

**Show:** Pull up the README briefly to show the 6 tools we built.

---

### 2. Semantic Search Demo (1 minute)
**Say:** "First, let me show how the semantic search works. We can query our corpus to find relevant papers."

**Run:**
```bash
python3 src/search_papers.py "automated scientific discovery"
```

**Expected:** Top 5 papers with similarity scores around 0.65-0.75. Point out that it's finding semantically related work, not just keyword matches.

---

### 3. Gap Identification (1 minute)
**Say:** "Next, we identify research gaps by measuring how well-covered different topics are in the corpus."

**Run:**
```bash
python3 src/identify_gaps.py
```

**Expected:** List of topics with average similarity scores. Point out that "research idea evaluation" has the lowest coverage (~0.55), which aligns with our project goals.

**Say:** "This tells us where there's less existing work, suggesting potential areas for novel contributions."

---

### 4. Idea Generation (30 seconds)
**Say:** "Given a gap, we can generate research ideas that build on related papers in the corpus."

**Run:**
```bash
python3 src/generate_ideas.py "research idea evaluation"
```

**Expected:** 3 research ideas with one-sentence descriptions. Note that these are grounded in the top 5 related papers from the corpus.

---

### 5. Idea Evaluation with Dual Novelty Check (2 minutes)
**Say:** "Here's where it gets interesting. We evaluate ideas on 5 criteria, and after your feedback, I improved the novelty scoring to catch ideas that apply established methods to new domains."

**Run:**
```bash
python3 src/evaluate_idea.py "Using transformer attention patterns to automatically detect research idea novelty in scientific papers"
```

**Expected output structure:**
- Similarity-based novelty: ~2-3 (if transformers are well-covered)
- Application-based novelty: ~4 (novel application to idea evaluation)
- Final novelty score: 4 (max of the two)
- Other scores: Feasibility, Impact, Clarity, Grounding

**Say:** "Notice how the dual check catches that while transformers are well-known, applying them to research idea evaluation is novel. The old system would have missed this."

**Show:** Briefly open `src/evaluate_idea.py` and point to the `assess_application_novelty()` function and the line where we take `max(similarity_novelty, application_novelty)`.

---

### 6. Full Pipeline (30 seconds)
**Say:** "Finally, we can run the full generate-and-refine loop that generates 5 ideas, evaluates them, rejects low-scoring ones, and regenerates until we get 3 solid ideas."

**Optional (if time):** Run `python3 src/generate_and_refine.py "automated literature review"` but note this takes 30-60 seconds.

**Say:** "This runs the entire loop automatically and outputs the top 3 ideas with their scores."

---

## Key Points to Emphasize
1. **Literature grounding**: All ideas are generated from actual papers in the corpus
2. **Dual novelty check**: Catches both semantic novelty and application novelty
3. **Iterative refinement**: The system can reject and regenerate ideas until quality thresholds are met
4. **Evaluation criteria**: 5 dimensions (novelty, feasibility, impact, clarity, grounding) align with what makes good research

---

## Anticipated Questions

**Q: How big is your corpus?**
A: Currently ~1000 CS papers from arXiv (most recent). Can scale easily.

**Q: Why both semantic and LLM-based novelty checks?**
A: Semantic similarity misses cases where the application is novel but uses known methods. The LLM check explicitly evaluates whether the idea applies something established to a new problem.

**Q: How do you validate the quality of generated ideas?**
A: That's what the human-AI ideation experiment is for. We'll compare AI-assisted vs control conditions with expert evaluators using the rubric we designed.

**Q: What's next?**
A: Run the human study, validate the scoring system, and potentially expand the corpus to include Semantic Scholar or conference papers.
