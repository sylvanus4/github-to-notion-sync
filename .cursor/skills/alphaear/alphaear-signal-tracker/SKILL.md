---
name: alphaear-signal-tracker
description: >-
  Tracks finance investment signal evolution — determines if signals are
  Strengthened, Weakened, or Falsified based on new market info. Use when
  monitoring finance signals, re-evaluating theses after news/price moves, or
  updating signal confidence and intensity. Do NOT use for one-time stock price
  checks (use daily-stock-check). Do NOT use for generating reports (use
  alphaear-reporter). Do NOT use for sentiment scoring (use alphaear-sentiment).
  Korean triggers: "시그널 추적", "시그널 진화", "강화 약화", "투자 시그널".
metadata:
  version: "1.1.0"
  last_updated: "2026-03-27"
  category: "analysis"
  author: "alphaear"
---
# AlphaEar Signal Tracker

## Overview

Agentic workflow to track how investment signals evolve over time. The agent performs: (1) Research — gather facts using FinResearcher prompt; (2) Analyze — produce `InvestmentSignal` JSON via FinAnalyst prompt; (3) Track — assess evolution (Strengthened/Weakened/Falsified) using Signal Tracking prompt. All prompts live in `references/PROMPTS.md`. Data sources: `alphaear-news`, `alphaear-stock`. Store signals in SQLite (`data/signal_flux.db`).

## Prerequisites

- Python 3.10+
- `agno` (agent framework), `sqlite3` (built-in)
- Access to `alphaear-search`, `alphaear-stock` skills for data gathering
- `scripts/fin_agent.py` — `FinUtils.sanitize_signal_output` for JSON cleanup
- `DatabaseManager` initialized (SQLite — `data/signal_flux.db`)

## Workflow

1. **Research**: Use **FinResearcher** prompt from `references/PROMPTS.md` — gather facts, prices, and industry context for the raw signal. Use `alphaear-search` and `alphaear-stock` for data.
2. **Analyze**: Use **FinAnalyst** prompt — transform research into `InvestmentSignal` JSON (`title`, `impact_tickers`, `transmission_chain`, `summary`, etc.).
3. **Sanitize**: Call `FinUtils.sanitize_signal_output(json_data, research_data, raw_signal)` from `scripts/fin_agent.py` to clean ticker bindings.
4. **Track** (for existing signals): Use **Signal Tracking** prompt — compare baseline signal with new news/price; output evolution assessment + updated `InvestmentSignal` JSON.
5. **Persist**: Store signals in SQLite (`data/signal_flux.db`).

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
- **SQLite schema**: Align stored fields with `signal_flux.db` signal table schema.

## AlphaEar Quality Standards (auto-improved)

### Intent → sub-skill routing

| User query pattern | This skill vs other |
|--------------------|---------------------|
| Signal evolution / validity / Strengthened·Weakened·Falsified | **This skill** |
| One-off RSI/MACD check | `daily-stock-check` |
| Final report assembly | `alphaear-reporter` |
| Sentiment only | `alphaear-sentiment` |

Use `alphaear-search` + `alphaear-stock` inside the research step; do not substitute unrelated skills.

### Data source attribution (required)

Tag facts feeding the signal: `(출처: alphaear-search / 엔진명)`, `(출처: alphaear-stock / yfinance|akshare)`, `(출처: FinResearcher 산출 요약)`. Evolution verdict must reference what changed (뉴스/가격) and from which source.

### Korean output

Korean users: verdicts and rationale in natural Korean (강화/약화/반증, 신뢰도, 근거).

### Fallback protocol

If research sparse: `조사 데이터 부족 — 추가 뉴스/가격 수집 필요` and avoid strong verdicts. If JSON/sanitize fails: `신호 JSON 정제 실패 — 재시도` per Error Handling table.
