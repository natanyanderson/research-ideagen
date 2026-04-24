# Preliminary Results & Discussion (Draft)

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

## 4.2 Discussion

The preliminary results suggest that LLM-based research ideation pipelines can produce ideas that are both grounded in existing literature and meaningfully novel. Across our test generations, the system consistently surfaced ideas that human reviewers would likely classify as non-trivial extensions of existing work, rather than mere recombinations.

The dual novelty scoring mechanism proved to be the most consequential design decision. By decoupling semantic similarity from application novelty, we avoid the failure mode where a genuinely creative application of an established method is dismissed simply because the underlying technique is common in the corpus. The agricultural RL example illustrates this clearly: a similarity-only filter would have penalized the idea for its proximity to existing RL literature, missing the point that the domain application is what makes it interesting.

However, the results also highlight a tension in automated idea evaluation: higher novelty does not necessarily mean higher quality. Some of the ideas scoring well on both novelty dimensions were underspecified or lacked clear evaluation pathways. This suggests that novelty scoring should be treated as a necessary but not sufficient signal, and that feasibility and clarity criteria carry more weight in determining whether an idea is actionable.

The three examples also suggest a potential relationship between similarity score and overall idea quality: ideas at intermediate similarity scores (0.48–0.52) tend to score best overall, while very high similarity (>0.65) correlates with incremental ideas and very low similarity may indicate hallucinated or out-of-scope concepts. We treat this as a hypothesis for future investigation rather than a finding—three examples are insufficient to establish a pattern—but it motivates a more systematic analysis of similarity score distributions across a larger test set.

Finally, the ~45 second generation cycle time is promising for practical use. A researcher could plausibly run the pipeline over a lunch break and return to a ranked shortlist of ideas, which aligns with our goal of augmenting rather than replacing human ideation.

## 4.3 Limitations & Future Work

**Corpus Coverage:** Our current corpus of ~1000 arXiv papers provides reasonable coverage of recent CS trends but lacks depth in specialized subfields. Scaling to 50K+ papers from multiple sources (arXiv, Semantic Scholar, conference proceedings) would improve both gap identification and novelty assessment.

**Evaluation Reliability:** The application novelty component relies on GPT-4's judgment, which introduces potential biases. Temperature settings (0.3 for application novelty, 0.7 for other criteria) introduce score variance across repeated runs; the magnitude of this variance has not been systematically measured and should be characterized in future work. Future work should explore ensemble approaches or fine-tuned models for more stable assessments.

**Domain Specificity:** We focused exclusively on computer science. Extending to other domains (biology, physics, social sciences) would require domain-specific corpora and potentially adjusted evaluation criteria.

**Validation Gap:** While our rubric provides systematic evaluation, we have not yet validated whether high-scoring ideas lead to successful research outcomes. Longitudinal studies tracking which generated ideas result in publications or funding would provide crucial ground truth.

**Human Study Status:** The planned comparative study (n=20 participants) awaits IRB approval. Initial pilot results should be available within 3 months. Key metrics will include: ideation time, idea count, expert ratings, and participant satisfaction.

Future iterations should explore: (1) citation network analysis to better identify emerging gaps, (2) multi-turn refinement where the system iteratively improves ideas based on evaluation feedback, and (3) personalization based on researcher expertise and interests.

Addressing the validation gap is the most pressing priority. Without ground truth data linking generated ideas to real research outcomes, our evaluation remains inherently proxy-based. Partnering with research groups willing to track whether pipeline-suggested directions lead to publications or funded proposals would substantially strengthen the empirical foundation of this work.
