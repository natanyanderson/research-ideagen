# Analysis Plan — AI-Assisted Research Ideation Study

**Status:** Draft — awaiting evaluator scores before execution
**Last updated:** Jordan

---

## 1. Overview

This document outlines the statistical analysis plan for the user study comparing idea novelty between the control condition (no AI assistance) and the AI-assisted condition. Analysis will be conducted once expert evaluator scores are returned.

---

## 2. Data Preparation

- **Merge evaluator scores:** Combine scores from all 3 evaluators into a single dataset keyed by participant ID and idea ID.
- **Score dimensions:** Each idea is scored on:
  - Methodological novelty (1–5)
  - Application novelty (1–5)
  - Final/overall novelty (1–5)
- **Condition mapping:** Apply participant-to-condition assignments (P01–P10 = Control, P11–P20 = AI-assisted). Keep this mapping separate from the evaluator-facing data.

---

## 3. Inter-Rater Reliability (IRR)

**Method:** Krippendorff's alpha

**Rationale:** Three raters, ordinal scale (1–5), unequal distributions expected — Krippendorff's alpha is appropriate and handles missing values gracefully.

**Thresholds:**
- α ≥ 0.80 → strong agreement, proceed with averaged scores
- 0.67 ≤ α < 0.80 → acceptable agreement, flag and proceed with caution
- α < 0.67 → low agreement, review disagreements before averaging; consider adjudication

**Implementation:** Compute per score dimension (methodological, application, final). Report all three in the paper.

---

## 4. Condition Comparison

**Method:** Mann-Whitney U test (two-tailed)

**Rationale:** n=20 total (10 per condition), ordinal scores, cannot assume normality — nonparametric test is appropriate.

**Comparisons to run:**
1. Control vs. AI-assisted: methodological novelty scores
2. Control vs. AI-assisted: application novelty scores
3. Control vs. AI-assisted: final/overall novelty scores

**Effect size:** Compute rank-biserial correlation (r) for each significant comparison.

**Significance threshold:** p < 0.05 (report exact p-values).

---

## 5. Secondary Analyses

- **Score distribution plots:** Box plots per condition for each novelty dimension.
- **Anchoring proxy:** Correlate time-on-task (AI-assisted group) with final novelty score — lower time may indicate anchoring on first suggestions.
- **Variance comparison:** Levene's test for equality of variances between conditions (to quantify the uniformity vs. spread observation from field notes).

---

## 6. Reporting

- All results to be written up in the Results section (paper-results-draft.md).
- IRR scores reported in the Approach/Evaluation Framework section.
- Effect sizes and exact p-values reported for all significant comparisons.
- Non-significant results also reported (don't bury null findings).

---

## 7. Tools

- Python (scipy, krippendorff, pandas, matplotlib/seaborn)
- Scripts to be added to `/src/` once data is in hand

---

## 8. Pre-Registration

**Primary confirmatory analysis** (to be pre-registered on OSF before evaluator scores are received):

> *"We will compare final/overall novelty scores between the control and AI-assisted conditions using a two-tailed Mann-Whitney U test (α = 0.05). We predict that AI-assisted participants will produce ideas with significantly higher novelty scores than control participants."*

All other analyses (methodological novelty, application novelty, anchoring proxy, variance comparison) are **exploratory** and will be labeled as such in the paper.

**Pre-registration platform:** OSF (Open Science Framework)
**Timing:** Must be submitted before evaluator scores are unblinded.

---

*No changes to the primary confirmatory analysis after pre-registration without explicit documentation of the deviation.*
