# Paper Outline: Dual Novelty Scoring for Automated Research Ideation

Workshop paper, 4 pages.

## 1. Introduction
- Motivation: growing interest in AI-assisted research
- Problem: existing automated ideation lacks good novelty evaluation
- Gap: semantic similarity alone doesn't capture methodological novelty
- Contribution: dual novelty scoring + anchoring experiment

## 2. Related Work
- AI Co-Scientists / Rubric Rewards (closest to our work)
- Automated hypothesis generation
- Creativity support tools
- Human evaluation of research ideas
- LLM-based evaluation methods
- Anchoring effects in cognitive science

## 3. Approach
- 3.1 Paper ingestion and embedding
- 3.2 Gap identification
- 3.3 Idea generation from gaps
- 3.4 Dual novelty scoring (KEY CONTRIBUTION)
  - Corpus-based novelty
  - Application novelty (LLM check)
  - Why max of both works
- 3.5 Generate-eval-refine pipeline

## 4. Preliminary Results
- Test cases across 3 topics (9 ideas total)
- Comparison: single vs dual scoring
- Failure cases the fix catches (RL/agriculture, BERT/legal, transformer/protein)

## 5. Experiment Design
- Anchoring study setup
- Rubric with 5 criteria
- Expected analysis

## 6. Discussion & Future Work
- Limitations (corpus scope, LLM judge reliability)
- Follow-up: pipeline vs ChatGPT comparison
- Scaling the experiment
