---
description: "Track investment signal evolution — Strengthened, Weakened, or Falsified"
---

# AlphaEar Signal Tracker

## Skill Reference

Read and follow the skill at `.cursor/skills/alphaear-signal-tracker/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

- If `$ARGUMENTS` contains a signal description or thesis, create a new signal via Research → Analyze
- If `$ARGUMENTS` mentions "track" or "update" with a signal ID, run the Tracking workflow
- If `$ARGUMENTS` mentions "re-evaluate", load existing signal and run evolution assessment
- If `$ARGUMENTS` is empty, ask user for a signal description or signal ID to track

### Step 2: Execute

Follow the workflow in the skill:

1. **New signal**: FinResearcher → FinAnalyst → sanitize → persist
2. **Track existing**: Load baseline + fetch new data → Signal Tracking prompt → update

### Step 3: Report

Present results with:
- Signal title and summary
- Evolution status (Strengthened / Weakened / Falsified / Unchanged)
- Updated confidence and intensity scores
- Key reasoning for the assessment
