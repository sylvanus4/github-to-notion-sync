---
description: "Track AI model leaderboard rankings (Open LLM, Chatbot Arena, Video Gen) and detect rank changes"
---

# HF Leaderboard — AI Model Rankings Tracker

## Skill Reference

Read and follow the skill at `.cursor/skills/hf-leaderboard-tracker/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

Determine scope from user input:

- **All leaderboards** (default): Scan Open LLM Leaderboard, Chatbot Arena, and Video Gen benchmarks
- **Specific leaderboard** (e.g., "arena", "llm", "video"): Scan only that leaderboard
- **Category filter** (e.g., "chat models", "reasoning"): Filter results by category

### Step 2: Execute Pipeline

Run the full 7-phase pipeline as specified in the skill:

1. Fetch Open LLM Leaderboard (from HF dataset)
2. Fetch Chatbot Arena Rankings (from lmarena.ai)
3. Fetch Video Generation Leaderboard (from VBench/HF datasets)
4. Delta Detection (compare against previous snapshots)
5. Save Snapshots (for future comparisons)
6. Report Generation → `output/hf-leaderboard/{DATE}-leaderboard-report.md`
7. Distribute to Slack `#deep-research` (only if changes detected)

### Step 3: Report Results

Summarize:
- Leaderboards checked
- New entries count
- Biggest rank movers (up and down)
- Report file location
- Whether Slack was posted (or skipped due to no changes)

## Constraints

- Always verify `hf` CLI auth before running
- If delta detection shows no significant changes, skip Slack posting
- Save snapshots even if Slack is skipped
- Report in Korean with English technical terms
