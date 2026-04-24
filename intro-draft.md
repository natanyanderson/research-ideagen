# Introduction

Scientific progress depends on researchers generating novel ideas that extend beyond the current state of the art. However, human researchers are known to be susceptible to **anchoring**—the cognitive bias of relying too heavily on existing paradigms and familiar approaches when forming new hypotheses [CITE: Tversky & Kahneman, 1974]. This tendency can limit the novelty of generated research ideas, particularly in fields where established methods dominate the literature.

Recent work has explored the use of large language models (LLMs) to assist with research ideation [CITE: Si et al., 2024; AI co-scientists work]. While these systems show promise in generating a volume of ideas, evaluating the *novelty* of those ideas remains an open challenge. Existing approaches typically rely on similarity-based methods, measuring how close a generated idea is to existing papers in an embedding space. However, this approach conflates two distinct forms of novelty: **methodological novelty** (is the method itself new?) and **application novelty** (is the method being applied to a new domain?).

Consider an example from our preliminary experiments: applying reinforcement learning to an agricultural domain. A similarity-based novelty score would rate this idea as highly novel, simply because few papers discuss RL in agriculture. However, the underlying method—reinforcement learning—is well-established, and the true novelty lies in the domain transfer. Relying on similarity alone leads to false positives, where ideas appear novel simply because their application domain is underrepresented in the training corpus.

In this paper, we present a research ideation pipeline that combines automated literature ingestion, gap identification, and a **dual novelty scoring** approach that evaluates both methodological and application novelty as independent signals. Our main contributions are:

1. An end-to-end pipeline for generating and evaluating research ideas, grounded in a corpus of 1,000 scientific papers.
2. A dual novelty scoring method that separately quantifies methodological and application novelty, combined through a hybrid aggregation rule.
3. Preliminary results on 50 generated ideas across 10 topics demonstrating that our dual approach correctly identifies domain-transfer-only ideas that similarity-based methods misclassify as fully novel.
4. An experimental design for a planned user study (N=20) comparing AI-assisted ideation against a control condition, with the goal of measuring whether AI assistance helps researchers break out of anchoring patterns.

The remainder of this paper is organized as follows. Section 2 reviews related work on automated research ideation, novelty assessment, and anchoring effects in scientific creativity. Section 3 describes our system architecture and the dual novelty scoring approach. Section 4 presents preliminary results from our test cases. Section 5 outlines the design of our planned user study, and Section 6 discusses limitations and future directions.
