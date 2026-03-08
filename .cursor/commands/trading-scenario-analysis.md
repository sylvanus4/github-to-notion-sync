---
description: "Analyze news headlines to build 18-month scenario projections with sector impacts"
argument-hint: "News headline or topic (e.g., 'Fed rate cut expectations', 'AI chip export controls')"
---

# Trading Scenario Analysis

## Skill Reference

Read and follow `.cursor/skills/trading-scenario-analyzer/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: News Collection

If `$ARGUMENTS` is a specific headline, use it as the primary input.
If `$ARGUMENTS` is a topic, use WebSearch to gather relevant recent headlines.

### Step 2: Scenario Analysis

Run the `trading-scenario-analyzer` skill:
1. Launch scenario-analyst subagent for primary analysis
2. Build 18-month scenario projections (base, bull, bear)
3. Map 1st/2nd/3rd order effects
4. Identify impacted sectors and recommend tickers

### Step 3: Strategy Review

Launch strategy-reviewer subagent for second opinion:
1. Critical review of the primary analysis
2. Identify blind spots and counter-arguments
3. Suggest alternative scenarios

### Step 4: Report

Generate comprehensive scenario report:
- Headline and context
- 3 scenarios with probabilities
- Sector impact matrix
- Recommended tickers (long and short)
- Critical review summary
- Key triggers to watch

Save to `outputs/reports/trading/scenario_analysis_YYYY-MM-DD.md`.

## Constraints

- Dual-agent architecture: analyst + reviewer
- All output in English
- Include probability ranges for each scenario
- Include "This is not financial advice" disclaimer
