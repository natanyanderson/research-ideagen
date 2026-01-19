# Approach Section Draft

## 3. Approach

We present a literature-grounded pipeline for research idea generation with dual novelty assessment. Our system combines semantic search over a scientific corpus, gap identification, LLM-based idea generation, and a hybrid evaluation approach that distinguishes between semantic novelty and application novelty.

### 3.1 Corpus Ingestion & Semantic Search

We built a semantic search system over recent computer science literature from arXiv. Our corpus consists of approximately 1,000 recent CS papers, selected to provide broad coverage of contemporary research topics. For each paper, we extract metadata (title, authors, abstract, publication date) and generate dense vector embeddings using OpenAI's `text-embedding-3-small` model, which produces 1536-dimensional representations optimized for semantic similarity tasks.

Embeddings are stored in a SQLite database alongside paper metadata, enabling efficient retrieval. To find papers relevant to a given query or topic, we embed the query using the same model and compute cosine similarity between the query embedding and all paper embeddings in the corpus. Papers are ranked by similarity score, with higher scores indicating stronger semantic relevance.

This retrieval mechanism serves two purposes: (1) identifying existing work related to a potential research idea, and (2) providing literature context to ground the idea generation process.

### 3.2 Gap Identification

To systematically identify underrepresented research areas, we implement a topic coverage analysis. We define a set of predefined topics spanning common CS research areas (e.g., "retrieval augmented generation," "automated scientific discovery," "research idea evaluation"). For each topic, we:

1. Generate an embedding for the topic description
2. Compute cosine similarity between the topic embedding and all papers in the corpus
3. Calculate the average similarity score across the top-k most similar papers

Topics with lower average similarity scores indicate areas with less existing coverage in our corpus, suggesting potential gaps where novel contributions may be more feasible. This automated gap identification helps prioritize topics for idea generation.

We categorize topics as "HIGH GAP" (avg similarity < 0.60), "MODERATE GAP" (0.60-0.70), or "WELL COVERED" (> 0.70). These thresholds were determined empirically based on the distribution of similarity scores in our corpus.

### 3.3 Idea Generation

Given a target topic (often identified through gap analysis), we use GPT-4 to generate research ideas grounded in the existing literature. The generation process is conditioned on:

1. **Target topic or gap**: The research area to explore
2. **Related papers**: The top-5 most semantically similar papers from our corpus, including titles and abstracts

We construct a prompt that provides this context and instructs the model to generate 3 distinct research ideas. Each idea includes a concise one-sentence description. The prompt explicitly encourages ideas that build on or extend the provided papers, ensuring grounding in existing work.

This retrieval-augmented approach addresses a key limitation of purely generative systems: without literature context, LLMs may propose ideas that duplicate existing work or lack grounding in established methods. By conditioning generation on retrieved papers, we increase the likelihood that generated ideas are both novel and feasible.

### 3.4 Dual Novelty Evaluation

A central contribution of our work is a dual approach to novelty assessment that addresses limitations of purely similarity-based methods. We evaluate each generated idea across five criteria (Novelty, Feasibility, Impact, Clarity, Grounding), each scored on a 1-5 scale. Here we focus on our novelty scoring mechanism.

**Similarity-based Novelty**: We first compute semantic novelty using the same embedding-based approach as our retrieval system. The idea description is embedded, and we compute its cosine similarity to all papers in the corpus. The novelty score is inversely related to the maximum similarity:

- Score 5: max similarity < 0.50 (highly novel, distant from existing work)
- Score 4: 0.50-0.60 (novel with clear differentiation)
- Score 3: 0.60-0.70 (meaningful extension of existing work)
- Score 2: 0.70-0.80 (minor variation)
- Score 1: > 0.80 (well-established, minimal novelty)

**Application-based Novelty**: Similarity scores alone can miss an important class of novel ideas: those that apply established methods to new domains or problems. For example, applying transformers (a well-known architecture) to research idea evaluation (a less-explored application) would score low on semantic novelty despite representing a novel contribution.

To address this, we introduce an LLM-based assessment that explicitly evaluates whether an idea constitutes a novel application. We prompt GPT-4 to analyze the idea and determine if it applies known techniques to a new problem domain, scoring from 1-5:

- Score 5: Highly novel application to an unexplored domain
- Score 4: Novel application with clear differentiation from existing work
- Score 3: Adaptation of method to related domain
- Score 2: Minor variation in application
- Score 1: Standard application of established method

**Combined Score**: The final novelty score is the maximum of the similarity-based and application-based scores: `novelty = max(similarity_novelty, application_novelty)`. This ensures that ideas scoring high on either dimension are recognized as novel. The max operation reflects that novelty can arise from either semantic distance from existing work or from novel application of known methods.

**Additional Evaluation Criteria**: Beyond novelty, we score each idea on four additional dimensions:

- **Feasibility** (1-5): Can the idea be executed with available methods and resources?
- **Impact** (1-5): Would success meaningfully advance the field?
- **Clarity** (1-5): Is the idea well-defined and testable?
- **Grounding** (1-5): Does it connect to and build on existing literature?

These scores provide a multidimensional assessment of research idea quality, balancing novelty with practical considerations.

### 3.5 Iterative Refinement

To improve the quality of generated ideas, we implement an iterative generate-evaluate-refine loop. The system:

1. Generates a batch of 5 ideas for a given topic
2. Evaluates each idea using the dual novelty approach and additional criteria
3. Filters ideas based on quality thresholds: overall score ≥ 3.5 and novelty ≥ 2
4. If fewer than 3 ideas pass the thresholds, regenerates ideas and repeats

This process continues until at least 3 high-quality ideas are produced. The rejection and regeneration mechanism encourages the system to explore the idea space more thoroughly rather than accepting the first generated candidates.

The final output is a ranked list of 3 research ideas with their evaluation scores across all five criteria, providing both the ideas themselves and a detailed quality assessment to support human decision-making.
