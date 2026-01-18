# Human-AI Ideation Study: One-Pager

## Research Question
Does AI-assisted ideation increase quantity but decrease novelty of human-generated research ideas?

## Hypothesis
Researchers using AI tools (ChatGPT) will generate more ideas but with lower novelty scores compared to unassisted brainstorming, due to cognitive anchoring effects.

## Design
**Between-subjects pilot study**
- N = 20 participants (grad students/postdocs in CS or related fields)
- 2 conditions: Control (n=10) vs AI-Assisted (n=10)

## Procedure
Participants are given a research topic and 30 minutes to generate 5 research ideas.

**Control group**: Brainstorm independently using whatever methods they normally use (paper, notes, web search, etc.)

**AI-Assisted group**: Given access to ChatGPT with a starter prompt template ("Generate 5 research ideas about [topic]"). Can iterate and refine with the tool during the session.

## Measurements
1. **Novelty**: Semantic similarity to existing literature corpus (using our embeddings pipeline)
2. **Diversity**: Semantic distance between participant's own ideas
3. **Feasibility**: Expert panel ratings (1-5 scale)
4. **Quantity**: Total number of distinct ideas generated
5. **Time to first idea**: Cognitive load indicator

## Expected Outcomes
- AI-assisted group: higher quantity, lower novelty, lower diversity
- Control group: fewer ideas but more original/diverse

## Resources Needed
- ChatGPT Plus accounts for AI-assisted group (or free tier)
- ~$20 gift cards per participant for compensation
- Expert panel (2-3 researchers) for feasibility ratings
- Topic selection (should be relevant but not too niche)

## Timeline
- Recruitment: 2 weeks
- Data collection: 1 week
- Analysis: 1 week
- Writeup: 1-2 weeks

## Follow-up Opportunities
- Add AI-collaborative condition (real-time iteration)
- Compare ChatGPT vs our literature-grounded pipeline
- Scale to N=60+ for publication
- Measure long-term retention/implementation of ideas
