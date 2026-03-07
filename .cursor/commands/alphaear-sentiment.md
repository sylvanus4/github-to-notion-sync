---
description: "Analyze financial text sentiment using LLM (default) or FinBERT (optional)"
---

# AlphaEar Sentiment

## Skill Reference

Read and follow the skill at `.cursor/skills/alphaear-sentiment/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

- If `$ARGUMENTS` contains text in quotes, analyze that text
- If `$ARGUMENTS` mentions "batch" and a source name, run batch sentiment update
- If `$ARGUMENTS` mentions "bert" or "finbert", use FinBERT mode (requires torch)
- If `$ARGUMENTS` is empty, ask user for the text to analyze

### Step 2: Execute

Follow the workflow in the skill:

1. Default: use the LLM prompt from the skill to analyze sentiment
2. Parse JSON response: `{score, label, reason}`
3. Optionally persist via `update_single_news_sentiment`

### Step 3: Report

Present results with:
- Sentiment score (-1.0 to 1.0)
- Label (positive / negative / neutral)
- Reasoning
