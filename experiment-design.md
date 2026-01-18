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

## Pre-Survey
All participants will complete a brief survey before the ideation task to measure prior AI tool experience (potential confounding variable). This allows us to control for baseline familiarity in our analysis.

**Survey Questions:**
1. How often do you use AI tools like ChatGPT, Claude, or similar assistants? (Never / Rarely / Monthly / Weekly / Daily)
2. Which AI tools have you used in the past 6 months? (Select all that apply: ChatGPT, Claude, Copilot, Gemini, Other, None)
3. For what purposes do you primarily use AI tools? (Select all that apply: Writing/editing, Coding, Research, Brainstorming ideas, Learning new topics, Other, I don't use AI tools)
4. How comfortable are you using AI tools for creative or research tasks? (1 = Not comfortable at all, 5 = Very comfortable)
5. Have you ever used AI tools specifically for generating research ideas? (Yes / No / Not sure)
6. How many years have you been involved in academic research? (Less than 1 year / 1-2 years / 3-5 years / 5+ years)

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
