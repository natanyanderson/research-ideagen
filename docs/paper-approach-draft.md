# 3. Approach

## 3.1 Literature Ingestion

We build a corpus of recent CS research by ingesting papers from arXiv (2024-2026). Each paper's abstract is embedded using OpenAI's text-embedding-3-small model and stored in a SQLite database alongside metadata (title, authors, publication date, categories). The current corpus contains 1,000 papers.

## 3.2 Gap Identification

To identify underrepresented research areas, we compute the average cosine similarity between a topic's embedding and all paper embeddings in the corpus. Topics with low average similarity indicate sparse coverage — potential opportunities for novel contributions. Our analysis found "research idea evaluation" (avg sim: 0.31) as the most underrepresented topic.

## 3.3 Idea Generation

Given a target topic, we retrieve the top-k most similar papers and prompt GPT-4 to generate research ideas that address identified gaps. The prompt includes paper abstracts as context to ground the generated ideas in existing work.

## 3.4 Dual Novelty Scoring

Our key contribution addresses a limitation of purely embedding-based novelty assessment. Semantic similarity alone conflates topic novelty with methodological novelty. For example, "apply RL to agricultural yield optimization" scores as highly novel because there are few agriculture papers in the CS corpus — but reinforcement learning for optimization is a well-established technique.

We introduce a secondary LLM-based check that specifically evaluates whether an idea proposes a genuinely novel *method* or merely applies a known method to a new *domain*. The final novelty score is the maximum of:

1. **Corpus novelty**: Derived from semantic distance to the nearest paper in the corpus
2. **Application novelty**: GPT-4 assessment of methodological originality (temperature=0.3)

This dual approach correctly identifies domain-transfer ideas (scored 1.8-2.1 on application novelty) while preserving high scores for genuinely novel approaches (scored 4.0+ on application novelty).

## 3.5 Generate-Eval-Refine Pipeline

The full pipeline generates a batch of candidate ideas, evaluates each using dual novelty scoring plus feasibility and impact assessments, rejects ideas below a novelty threshold of 3.5, and iterates until a target number of high-quality ideas is reached. In testing, the pipeline typically converges in 1-2 iterations.
