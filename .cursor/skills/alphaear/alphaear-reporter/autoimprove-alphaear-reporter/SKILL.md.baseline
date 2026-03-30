---
name: alphaear-reporter
description: >-
  Plan, write, and edit professional financial reports; generate finance chart
  configurations. Use when condensing finance analysis into a structured output,
  assembling signals into reports, or producing Executive Summary + Risk Factors
  + References. Do NOT use for daily trading signals (use daily-stock-check). Do
  NOT use for ADRs or technical documentation (use technical-writer). Do NOT use
  for logic chain diagrams (use alphaear-logic-visualizer). Korean triggers:
  "생성", "체크", "계획", "리포트".
metadata:
  version: "1.0.0"
  category: "generation"
  author: "alphaear"
---
# AlphaEar Reporter

## Overview

Professional financial report generation via a Plan → Write → Edit → Chart workflow. The agent clusters scattered signals, writes deep-analysis sections, assembles a structured report, and generates chart configurations.

## Prerequisites

- Python 3.10+
- `sqlite3` (built-in)
- Project stock data and analysis results (e.g. from daily-stock-check) as input signals

## Workflow

1. **Cluster Signals**: Read input signals and use the **Cluster Signals Prompt** in `references/PROMPTS.md` to group them into 3–5 themes.
2. **Write Sections**: For each cluster, use the **Write Section Prompt** in `references/PROMPTS.md` to generate deep analysis; follow the section structure in [assets/templates/report-structure.md](assets/templates/report-structure.md); include `json-chart` blocks where appropriate.
3. **Final Assembly**: Use the **Final Assembly Prompt** in `references/PROMPTS.md` to compile sections into a report following the output structure in [assets/templates/report-structure.md](assets/templates/report-structure.md) — verify section order, quality criteria, and chart configurations match the template.
4. **Visualization**: Use `scripts/visualizer.py` for chart configs when needed; chart configuration templates are documented in [assets/templates/report-structure.md](assets/templates/report-structure.md).

## Examples

| Trigger | Action | Result |
|---------|--------|--------|
| "Write a report from today's stock signals" | Cluster → Write → Assemble | Structured markdown report with Executive Summary |
| "Generate chart config for 002371.SZ" | `scripts/visualizer.py` | Chart configuration for forecast/visualization |
| "Summarize these 10 signals into a report" | Cluster Signals prompt | 3–5 themes; then Write Section per theme |
| "Post report to Slack" | After Assembly → slack_send_message MCP | Report distributed to Slack channel |

## Error Handling

| Error | Behavior | Recovery |
|-------|----------|----------|
| Empty signals input | Cluster returns empty clusters | Ensure signals from daily-stock-check or other sources |
| Missing chart data | `json-chart` block placeholder | Use `scripts/visualizer.py` for explicit chart generation |
| Assemble fails | Inconsistent H2/H3 hierarchy | Re-run Final Assembly prompt with corrected sections |

## Troubleshooting

- **Stale input**: Use project stock data and daily-stock-check outputs for fresh signals.
- **Chart configs**: If Writer prompt omits charts, call `scripts/visualizer.py` directly.
- **Slack posting**: Integrate via `slack_send_message` MCP after report assembly.
