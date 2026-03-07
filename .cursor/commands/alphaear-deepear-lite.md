---
description: "Comprehensive financial analysis orchestrating all AlphaEar skills"
---

# AlphaEar DeepEar Lite

## Skill Reference

Read and follow the skill at `.cursor/skills/alphaear-deepear-lite/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

- If `$ARGUMENTS` contains a broad question (e.g., "Analyze how X affects the market"), run full orchestration
- If `$ARGUMENTS` mentions specific domains (news, sentiment, prediction), run only those sub-skills
- If `$ARGUMENTS` mentions "latest signals", run `fetch_latest_signals()` from `scripts/deepear_lite.py`
- If `$ARGUMENTS` is empty, ask user for a finance analysis question

### Step 2: Execute

Follow the orchestration workflow in the skill:

1. Parse intent to identify needed domains
2. Delegate to alphaear sub-skills in sequence:
   - alphaear-search + alphaear-news (data gathering)
   - alphaear-sentiment (sentiment scoring)
   - alphaear-signal-tracker (signal analysis)
   - alphaear-predictor (time-series forecast)
   - alphaear-logic-visualizer (transmission chain)
   - alphaear-reporter (final report)
3. Synthesize into comprehensive response

### Step 3: Report

Present a comprehensive analysis with:
- Data sources and news summary
- Sentiment scores
- Signal assessments
- Predictions (if applicable)
- Logic chain diagram (if applicable)
- Structured report (if full orchestration)
