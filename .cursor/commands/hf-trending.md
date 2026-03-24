---
description: "Run enhanced HF trending intelligence — papers, models, spaces, leaderboards with optional topic filter"
---

# HF Trending — Enhanced AI Research Radar

## Skill Reference

Read and follow the skill at `.cursor/skills/hf-trending-intelligence/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

Determine mode from user input:

- **Default (no args)**: Run the full pipeline without topic filter (v1 behavior)
- **With topics** (e.g., "LLM, video generation"): Enable Phase 1.5 (topic radar) and Phase 2.5 (leaderboard cross-reference)
- **"focused"**: Run with default topics from `hf-topic-radar/references/topic-config.md`
- **Date override** (e.g., "yesterday"): Use specified date instead of today

### Step 2: Execute Pipeline

Run the full pipeline as specified in the skill:

1. Paper Scan (30 trending papers)
1.5. Topic-Focused Model & Space Trending (if topics specified)
2. Cross-Reference (parallel: models, datasets, discussions)
2.5. Leaderboard Cross-Reference (if topics specified)
3. Web Enrichment (top 5 papers)
4. Trend Scoring (composite score with optional leaderboard bonus)
5. Intelligence Report Generation
6. Curate (add HOT items to monthly HF collection)
7. Distribute to Slack `#deep-research-trending` + Notion

### Step 3: Report Results

Summarize:
- Papers scanned
- HOT / WARM / COOL counts
- Top 3 trends with scores
- Topic-specific highlights (if topics were used)
- Leaderboard-validated items (if any)
- Report file, Slack thread, Notion page URLs

## Constraints

- Always verify `hf` CLI auth before running
- Max 4 concurrent subagents during cross-reference phase
- Respect rate limits on all external APIs
- Report in Korean with English technical terms
