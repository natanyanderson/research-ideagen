# Approach Section Draft

## 3. Approach

We present a literature-grounded pipeline for research idea generation with dual novelty assessment. Our system combines semantic search over a scientific corpus, gap identification, LLM-based idea generation, and a hybrid evaluation approach that distinguishes between semantic novelty and application novelty.

### 3.1 Corpus Ingestion & Semantic Search

We built a semantic search system over approximately 1,000 recent CS papers from arXiv, using OpenAI's `text-embedding-3-small` model to generate dense vector embeddings stored in a SQLite database. Retrieval uses cosine similarity between a query embedding and all corpus embeddings, serving two purposes: identifying existing work related to a potential idea, and providing literature context for generation.

### 3.2 Gap Identification

We define a set of predefined topics spanning common CS research areas and compute average cosine similarity between each topic embedding and the top-k most similar papers in the corpus. Topics with lower average similarity indicate underrepresented areas. We categorize topics as "HIGH GAP" (avg similarity < 0.60), "MODERATE GAP" (0.60–0.70), or "WELL COVERED" (> 0.70), with thresholds determined empirically from the corpus similarity distribution.

### 3.3 Idea Generation

Given a target topic, we use GPT-4 to generate research ideas conditioned on the top-5 most semantically similar papers from our corpus. The prompt provides paper titles and abstracts alongside the target topic, and instructs the model to generate 3 distinct, grounded research ideas. Conditioning on retrieved papers reduces duplication of existing work and increases feasibility grounding.

### 3.4 Dual Novelty Evaluation

A central contribution of our work is a dual approach to novelty assessment. We evaluate each generated idea across five criteria (Novelty, Feasibility, Impact, Clarity, Grounding), each scored 1–5, with particular focus on our novelty mechanism.

**Similarity-based Novelty**: The idea description is embedded and compared against all corpus papers via cosine similarity. The novelty score is inversely related to the maximum similarity score:

- Score 5: max similarity < 0.50 (highly novel)
- Score 4: 0.50–0.60 (novel with clear differentiation)
- Score 3: 0.60–0.70 (meaningful extension)
- Score 2: 0.70–0.80 (minor variation)
- Score 1: > 0.80 (well-established)

**Application-based Novelty**: Similarity scores alone miss an important class of novel ideas—those that apply established methods to new domains. We prompt GPT-4 to explicitly assess whether an idea constitutes a novel application, scoring 1–5 on application originality.

**Combined Score**: `novelty = max(similarity_novelty, application_novelty)`. The max operation ensures that ideas novel on either dimension are recognized as such.

### 3.5 Evaluation Framework

To validate AI-generated ideas against human-generated baselines, we designed a controlled experiment comparing two conditions: (1) control (unaided ideation) and (2) AI-assisted (using our pipeline). We developed a standardized rubric with five criteria, each scored 1–5:

| Criterion | Description |
|-----------|-------------|
| Novelty | Originality relative to existing work |
| Feasibility | Practicality with current methods |
| Impact | Potential significance if successful |
| Clarity | Specificity and testability |
| Grounding | Connection to existing literature |

Three expert evaluators (CS PhD students/postdocs) will independently score each idea, with majority voting for final classifications (expected κ > 0.5). **Hypothesis:** AI-assisted ideation will increase quantity and feasibility scores but potentially decrease novelty due to anchoring effects.

### 3.6 Iterative Refinement

To improve output quality, we implement a generate-evaluate-refine loop. The system generates a batch of 5 ideas, evaluates each using dual novelty and the additional criteria, and filters on quality thresholds (overall score ≥ 3.5, novelty ≥ 2). If fewer than 3 ideas pass, the system regenerates and repeats, outputting a ranked list of 3 ideas with full evaluation scores.
