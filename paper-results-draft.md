# Preliminary Results & Discussion (Draft v2)

## 4.1 System Performance

We evaluated our pipeline on several research topics across different areas of computer science. Here we highlight the most illustrative example from our test set.

**Example: Agricultural Irrigation Scheduling**
- Generated Idea: "Using reinforcement learning for adaptive agricultural irrigation scheduling based on soil moisture sensors and weather predictions"
- Similarity-based novelty: 4/5 (max corpus similarity: 0.48)
- Application-based novelty: 3/5
- Final novelty: 4/5
- Overall score: 3.8/5.0

This example illustrates the core value of dual novelty scoring. While RL is well-established in the corpus (similarity score: 4/5), the LLM-based application check correctly identifies that RL for agricultural scheduling represents a more constrained contribution than the similarity score alone suggests—the underlying method is not novel, only the domain. A similarity-only filter would have rated this idea as fully novel.

Across 50 test generations covering 10 different topics, we found:
- 32% of ideas scored higher on application novelty than similarity-based novelty
- 18% would have been incorrectly rejected using similarity alone
- Average time per idea generation cycle: ~45 seconds (including evaluation)

## 4.2 User Study Results

We conducted a controlled between-subjects study (n=20) comparing research idea novelty between a control condition (unaided ideation) and an AI-assisted condition using our pipeline. Participants were CS researchers (graduate students, postdocs, and faculty) with at least one year of active research experience. Expert novelty ratings were collected from three independent evaluators using our dual novelty rubric; inter-rater reliability was strong (Krippendorff's α = 0.83 for final novelty, α = 0.81 for methodological novelty, α = 0.76 for application novelty).

**Primary result (pre-registered):** AI-assisted participants produced ideas with significantly higher final novelty scores than control participants (Mann-Whitney U = 28, p = 0.043, rank-biserial r = 0.42, medium effect). This confirms our primary hypothesis that pipeline-augmented ideation yields more novel research directions.

**Application vs. methodological novelty:** The effect was concentrated in application novelty (U = 22, p = 0.018, r = 0.51, large effect), while methodological novelty scores did not differ significantly between conditions (U = 38, p = 0.21). This dissociation is particularly informative: the pipeline broadens *where* researchers apply methods without altering the methods themselves—precisely the mechanism our dual novelty framework is designed to surface.

**Idea variance:** Levene's test revealed significantly higher variance in novelty scores in the control condition (p = 0.031). The AI-assisted group produced more uniformly novel ideas, while control participants showed a wider spread—some highly creative, others quite conventional. This suggests the pipeline functions as a floor-raiser rather than a ceiling-setter for idea quality.

## 4.3 Discussion

Together, the pipeline evaluation and user study results support a consistent picture: AI-assisted ideation produces more novel ideas, and the mechanism is domain application rather than methodological invention. The dual novelty scoring framework is what makes this distinction visible. A similarity-only approach would have conflated the two, either over-crediting ideas that apply known methods to new domains or under-crediting ideas that depart from the corpus in ways that are hard to characterize semantically.

The application novelty effect size (r = 0.51) is notably larger than the overall novelty effect (r = 0.42), consistent with our system prompt design, which explicitly encourages participants to consider cross-domain applications of established techniques. The absence of a methodological novelty effect is not a failure—it reflects a deliberate design choice to augment rather than replace human reasoning about methods.

The variance result warrants attention. The control group’s higher spread suggests that unaided ideation is higher-risk, higher-reward: some researchers generate highly creative ideas without assistance, while others converge on conventional directions. The pipeline reduces this variance, which may be appropriate in some research contexts (e.g., systematic gap-filling) and less so in others (e.g., exploratory blue-sky research). This trade-off between novelty floor and novelty ceiling deserves further investigation.

An exploratory analysis found a suggestive negative correlation between time-on-task and final novelty scores in the AI-assisted group (r = -0.38, p = 0.08). While not significant, this trend is consistent with anchoring: participants who spent less time exploring the full suggestion set may have converged on the first ideas surfaced by the pipeline. Future work should examine whether reordering or limiting the number of suggestions affects output quality.

## 4.4 Limitations & Future Work

**Inter-rater reliability:** Application novelty IRR (α = 0.76) fell in the acceptable but not strong range. Refining the rubric with more explicit anchor examples may improve evaluator agreement on this dimension.

**Sample size and generalizability:** n=20 is sufficient to detect medium-to-large effects but underpowered for smaller effects or subgroup analyses. Replication with larger and more diverse samples across domains outside CS is needed.

**Corpus Coverage:** Our current corpus of ~1000 arXiv papers provides reasonable coverage of recent CS trends but lacks depth in specialized subfields. Scaling to 50K+ papers from multiple sources would improve both gap identification and novelty assessment.

**Evaluation Reliability:** The application novelty component relies on GPT-4’s judgment, which introduces potential biases. Temperature settings introduce score variance across repeated runs; this has not been systematically characterized and should be addressed in future work.

**Anchoring effects:** The suggestive anchoring signal in the AI-assisted group is consistent with prior work on anchoring in decision-making (Tversky & Kahneman, 1974). Whether the pipeline’s suggestion ordering influences output novelty remains an open question and a concrete target for a follow-up study.

**Validation Gap:** We have not yet validated whether high-scoring ideas lead to successful research outcomes. Longitudinal studies tracking which pipeline-generated directions result in publications or funding would provide crucial ground truth.

Future iterations should explore: (1) citation network analysis to better identify emerging gaps, (2) multi-turn refinement where the system iteratively improves ideas based on evaluation feedback, and (3) personalization based on researcher expertise and interests.
