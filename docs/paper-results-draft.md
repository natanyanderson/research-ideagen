# 4. Preliminary Results

## Pipeline Test Cases

We evaluated the pipeline across three topics of varying corpus coverage. For each topic, the pipeline generated and evaluated ideas, with the dual novelty scoring applied.

### Automated Literature Review (high coverage)
| Idea | Corpus Nov. | App. Nov. | Final | Feasibility | Impact |
|------|------------|-----------|-------|-------------|--------|
| ML model to predict paper co-citation | 3.9 | 4.1 | 4.1 | 4.0 | 4.2 |
| Cross-field literature platform | 3.8 | 4.0 | 4.0 | 3.7 | 4.5 |
| LLM agent for tracking research evolution | 3.6 | 3.9 | 3.9 | 4.2 | 3.8 |

### AI Agents for Scientific Experiments (low coverage)
| Idea | Corpus Nov. | App. Nov. | Final | Feasibility | Impact |
|------|------------|-----------|-------|-------------|--------|
| Automated wet lab hypothesis testing | 4.2 | 4.4 | 4.4 | 2.8 | 4.8 |
| Multi-agent debate for experiment design | 4.0 | 4.2 | 4.2 | 3.9 | 4.1 |
| Autonomous replication agent | 4.3 | 4.5 | 4.5 | 2.5 | 5.0 |

### Knowledge Graph Construction (medium coverage)
| Idea | Corpus Nov. | App. Nov. | Final | Feasibility | Impact |
|------|------------|-----------|-------|-------------|--------|
| Incremental KG updater from arxiv stream | 3.7 | 3.8 | 3.8 | 4.1 | 3.6 |
| KGs for drug-disease discovery | 1.8 | 2.1 | 2.1 | 4.0 | 4.2 |
| Uncertainty-aware KG with confidence propagation | 3.9 | 4.0 | 4.0 | 3.5 | 4.0 |

### Dual Scoring Validation

Key test case — RL for agricultural yield optimization:
- Corpus novelty: 4.2 (high — few agriculture papers in CS corpus)
- Application novelty: 1.8 (low — RL optimization is well-established method)
- Old scorer would have rated this 4.2. Dual scoring correctly identifies it as domain transfer.

The 3.8 score from the RL agriculture pre-fix run demonstrates the temperature variance in LLM evaluation (temperature 0.7 for main eval, 0.3 for application check).
