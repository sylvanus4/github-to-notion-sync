---
description: "Scan HuggingFace for trending models, spaces, and papers by topic (LLM, multi-LLM, video generation)"
---

# HF Topic Radar — Topic-Focused Trending Scan

## Skill Reference

Read and follow the skill at `.cursor/skills/hf-topic-radar/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

Determine topic scope from user input:

- **Specific topics provided** (e.g., "LLM", "video generation"): Use those topics
- **No topics specified**: Use all default topics from `references/topic-config.md`
- **"add topic X"**: Temporarily add to default list for this run

### Step 2: Load Topic Config

Read `.cursor/skills/hf-topic-radar/references/topic-config.md` to get HF tags and keywords for each requested topic.

### Step 3: Execute Pipeline

Run the full 7-phase pipeline as specified in the skill:

1. Model Scan (per topic)
2. Space Scan (per topic)
3. Paper Scan (filtered by topic keywords)
4. Deduplication and Cross-Linking
5. Scoring
6. Report Generation → `outputs/hf-trending/{DATE}-topic-radar.md`
7. Distribute to Slack `#deep-research-trending`

### Step 4: Report Results

Summarize:
- Topics scanned
- HOT / WARM / COOL counts per topic
- Top 3 items across all topics
- Report file location
- Slack thread link

## Constraints

- Always verify `hf` CLI auth before running
- Respect rate limits: max 10 API calls per topic
- Keep Slack thread replies under 3000 characters each
- Report in Korean with English technical terms
