---
description: "Plan, write, and edit professional financial reports from analysis signals"
---

# AlphaEar Reporter

## Skill Reference

Read and follow the skill at `.cursor/skills/alphaear-reporter/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

- If `$ARGUMENTS` contains "today" or "daily", use daily-stock-check output as input signals
- If `$ARGUMENTS` contains specific signals or themes, use those as input
- If `$ARGUMENTS` mentions "slack", post the final report to Slack
- If `$ARGUMENTS` is empty, gather available signals from recent analysis and ask user to confirm scope

### Step 2: Execute

Follow the workflow in the skill:

1. **Cluster**: Group input signals into 3-5 themes using Cluster Signals prompt
2. **Write**: Generate deep analysis for each cluster using Write Section prompt
3. **Assemble**: Compile into final report with Executive Summary, Risk Factors, References
4. **Post** (optional): Send to Slack via `slack_send_message` MCP

### Step 3: Report

Present the assembled report in markdown with:
- Executive Summary
- Analysis sections per theme
- Risk Factors
- References
