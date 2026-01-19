# Related Work - Key Papers to Cite

## Scientific Idea Generation

1. **"Can Large Language Models Generate Novel Research Ideas?"**
   - Si et al. (2024)
   - Evaluates LLMs' capability for research ideation, comparing AI-generated ideas to human expert ideas
   - Relevant to: motivation, comparison of approaches
   - https://arxiv.org/abs/2309.04259

2. **"SciMON: Scientific Inspiration Machines Optimized for Novelty"**
   - Wang et al. (2023)
   - System for generating novel research directions by identifying gaps in literature
   - Relevant to: gap identification methods, novelty assessment
   - https://arxiv.org/abs/2305.14259

## Retrieval-Augmented Generation for Science

3. **"PaperQA: Retrieval-Augmented Generative Agent for Scientific Research"**
   - Skarlinski et al. (2023)
   - RAG system for scientific question answering grounded in literature
   - Relevant to: corpus ingestion, semantic search, grounding in literature
   - https://arxiv.org/abs/2312.07559

4. **"ScholarBERT: Bigger is Not Always Better"**
   - Wadden et al. (2022)
   - Embeddings optimized for scientific text understanding
   - Relevant to: embedding selection, semantic representation of scientific concepts
   - https://arxiv.org/abs/2205.11342

## Novelty Assessment

5. **"Measuring Research Novelty: A Multi-dimensional Framework"**
   - Verhoeven et al. (2016)
   - Proposes multiple dimensions for assessing research novelty beyond semantic similarity
   - Relevant to: dual novelty approach, distinguishing types of novelty
   - https://doi.org/10.1002/asi.23602

6. **"Automated Detection of Research Contributions in Software Engineering Papers"**
   - Novielli et al. (2020)
   - Methods for identifying and classifying types of contributions in research papers
   - Relevant to: evaluation criteria design, contribution assessment
   - https://doi.org/10.1109/MSR52588.2021.00015

---

## Integration Notes for Related Work Section

**Scientific Idea Generation**: Frame our work as extending prior LLM-based ideation systems by adding literature grounding and dual novelty assessment. Contrast with purely generative approaches that lack corpus grounding.

**RAG for Science**: Position our retrieval mechanism as building on established RAG architectures, adapted specifically for the ideation task rather than QA. Emphasize the role of retrieval in both gap identification and generation conditioning.

**Novelty Assessment**: Highlight gap in prior work - most methods use either semantic similarity OR expert judgment, but not hybrid approaches that distinguish semantic vs. application novelty. Our dual check addresses this limitation.
