# Paper Outline: Literature-Grounded Research Idea Generation with Dual Novelty Assessment

**Target:** 4-page workshop paper

---

## 1. Introduction (~0.75 pages)
- **Motivation**: Why automated research ideation matters
  - Growing volume of scientific literature
  - Need for systems that can identify gaps and generate novel ideas
  - Challenge: balancing novelty with feasibility and grounding
- **Problem Statement**: Existing approaches struggle to distinguish between semantic novelty and application novelty
  - Pure similarity-based methods miss ideas that apply known techniques to new domains
  - Need for hybrid evaluation approaches
- **Contribution**: Literature-grounded pipeline with dual novelty scoring
  - Semantic search over arXiv corpus
  - Gap identification through topic coverage analysis
  - Dual novelty check: semantic similarity + LLM-based application assessment
  - Preliminary human evaluation framework

---

## 2. Related Work (~0.5 pages)
- **Scientific idea generation**
  - Prior work on automated hypothesis generation
  - LLM-based research assistants
- **Retrieval-augmented generation for science**
  - Literature search and summarization systems
  - Citation-grounded text generation
- **Novelty assessment**
  - Semantic similarity approaches
  - Expert evaluation of research contributions
  - Gap: limited work on distinguishing method novelty vs. application novelty

---

## 3. Approach (~1.5 pages)

### 3.1 Corpus Ingestion & Semantic Search
- ArXiv paper collection (CS domain, ~1000 papers)
- Embedding generation (OpenAI text-embedding-3-small)
- SQLite storage for efficient retrieval
- Cosine similarity for semantic search

### 3.2 Gap Identification
- Predefined topic list for coverage analysis
- Average similarity scores to measure representation
- Identifying underrepresented areas

### 3.3 Idea Generation
- LLM-based generation (GPT-4) conditioned on:
  - Target topic/gap
  - Top-5 most relevant papers from corpus
- Output: 3 research ideas with one-sentence descriptions

### 3.4 Dual Novelty Evaluation
- **Similarity-based novelty**: Cosine distance to nearest papers in corpus
  - Score 1-5 based on distance thresholds
- **Application-based novelty**: LLM assessment
  - Explicitly checks if idea applies established methods to novel problems
  - Score 1-5 based on application originality
- **Final novelty score**: max(similarity_novelty, application_novelty)
- **Additional criteria**: Feasibility, Impact, Clarity, Grounding (all 1-5)

### 3.5 Iterative Refinement
- Generate → Evaluate → Filter → Regenerate loop
- Rejection thresholds: overall score < 3.5 or novelty < 2
- Outputs top 3 ideas meeting quality criteria

---

## 4. Preliminary Results & Discussion (~0.75 pages)

### 4.1 System Performance
- Examples of generated ideas across different topics
- Comparison of similarity-based vs. application-based novelty scores
- Cases where dual check catches novel applications of known methods

### 4.2 Evaluation Framework
- Expert rubric design (5 criteria, 1-5 scale)
- Planned human study: control vs AI-assisted ideation
- Hypothesis: AI increases quantity but may decrease novelty due to anchoring

### 4.3 Limitations & Future Work
- Corpus size and domain coverage
- Scalability to larger literature bases (Semantic Scholar, conference papers)
- Validation through human expert evaluation
- Long-term impact: do generated ideas lead to actual research?

---

## 5. Conclusion (~0.25 pages)
- Summary of contributions:
  - End-to-end literature-grounded ideation pipeline
  - Dual novelty assessment addresses key limitation of pure similarity approaches
  - Framework for systematic evaluation of AI-generated research ideas
- Next steps: Human validation study, corpus expansion, integration with research workflows

---

## Figures/Tables (if space permits)
- **Figure 1**: Pipeline architecture diagram
- **Table 1**: Example ideas with dual novelty scores
- **Table 2**: Evaluation rubric summary
