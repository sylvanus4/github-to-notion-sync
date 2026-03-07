---
name: alphaear-signal-tracker
description: Tracks finance investment signal evolution — determines if signals are Strengthened, Weakened, or Falsified based on new market info. Use when monitoring finance signals, re-evaluating theses after news/price moves, or updating signal confidence and intensity. Do NOT use for one-time stock price checks (use daily-stock-check). Do NOT use for generating reports (use alphaear-reporter). Do NOT use for sentiment scoring (use alphaear-sentiment).
metadata:
  version: "1.0.0"
  category: analysis
  author: alphaear
---

# AlphaEar Signal Tracker

## Overview

Agentic workflow to track how investment signals evolve over time. The agent performs: (1) Research — gather facts using FinResearcher prompt; (2) Analyze — produce `InvestmentSignal` JSON via FinAnalyst prompt; (3) Track — assess evolution (Strengthened/Weakened/Falsified) using Signal Tracking prompt. All prompts live in `references/PROMPTS.md`. Data sources: `alphaear-news`, `alphaear-stock`. Store signals in project PostgreSQL.

## Prerequisites

- Python 3.10+
- `agno` (agent framework), `sqlite3` (built-in)
- Access to `alphaear-search`, `alphaear-stock` skills for data gathering
- `scripts/fin_agent.py` — `FinUtils.sanitize_signal_output` for JSON cleanup
- `DatabaseManager` initialized (PostgreSQL for project signals)

## Workflow

1. **Research**: Use **FinResearcher** prompt from `references/PROMPTS.md` — gather facts, prices, and industry context for the raw signal. Use `alphaear-search` and `alphaear-stock` for data.
2. **Analyze**: Use **FinAnalyst** prompt — transform research into `InvestmentSignal` JSON (`title`, `impact_tickers`, `transmission_chain`, `summary`, etc.).
3. **Sanitize**: Call `FinUtils.sanitize_signal_output(json_data, research_data, raw_signal)` from `scripts/fin_agent.py` to clean ticker bindings.
4. **Track** (for existing signals): Use **Signal Tracking** prompt — compare baseline signal with new news/price; output evolution assessment + updated `InvestmentSignal` JSON.
5. **Persist**: Store signals in project PostgreSQL (per project schema).

## Examples

| Trigger | Action | Result |
|---------|--------|--------|
| "Track signal for 600519 thesis" | Research → Analyze → output | `InvestmentSignal` JSON |
| "Has this signal strengthened?" | Baseline + new research → Signal Tracking prompt | Evolution (Strengthened/Weakened/Falsified) + updated JSON |
| "Re-evaluate after news" | Load old signal, fetch news, run Track prompt | Updated signal with rationale |

## Error Handling

| Error | Behavior | Recovery |
|-------|----------|----------|
| Invalid JSON from LLM | `sanitize_signal_output` handles partial data | Retry with stricter schema hint in prompt |
| Ticker not in DB | Sanitizer skips unknown codes | Cross-check with `alphaear-stock.search_ticker` |
| Missing research context | Analyst prompt fails | Ensure FinResearcher output is passed into FinAnalyst |
| Evolution ambiguous | LLM may output Unchanged | Provide more specific new data in Tracking prompt |

## Troubleshooting

- **Spurious ticker binding**: Always run `sanitize_signal_output` on LLM output.
- **Weak evolution detection**: Supply structured `new_research_str` (news + price deltas) to Signal Tracking prompt.
- **PostgreSQL schema**: Align stored fields with project's signal table schema.
