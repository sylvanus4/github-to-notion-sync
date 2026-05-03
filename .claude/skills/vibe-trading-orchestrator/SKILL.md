---
name: vibe-trading-orchestrator
description: >-
  Master orchestrator for Vibe-Trading integration -- composes
  vibe-trading-data, vibe-trading-backtest, vibe-trading-swarm, and
  vibe-trading-quant into 4 workflow modes: Discovery, Research,
  Cross-Validation, and Strategy. Use when the user asks to "vibe-trading
  analysis", "full vibe pipeline", "vibe-trading orchestrator", "vibe research
  workflow", "vibe strategy pipeline", "바이브 오케스트레이터", "바이브 종합 분석", "바이브
  파이프라인", or wants an end-to-end finance analysis through Vibe-Trading. Do NOT
  use for individual Vibe-Trading operations (invoke the specific skill). Do
  NOT use for the project's daily pipeline (use today). Do NOT use for setup
  (use vibe-trading-setup).
---

# Vibe-Trading Orchestrator

## Overview

Composes 4 Vibe-Trading skills into end-to-end workflows for finance analysis.
Each mode defines a specific pipeline with ordered steps, data handoffs, and
output expectations.

## Prerequisites

- Vibe-Trading MCP server registered and healthy (see vibe-trading-setup)
- At minimum, `OPENAI_API_KEY` configured in `~/thaki/Vibe-Trading/agent/.env`

---

## Mode 1: Discovery

**Purpose**: Explore what Vibe-Trading can do for a specific asset or market.

```
Step 1. list_skills → browse 67+ finance skills
Step 2. load_skill(name) → read methodology for relevant skills
Step 3. list_swarm_presets → find suitable multi-agent teams
Step 4. get_market_data(codes, dates) → verify data availability
```

**When to use**: First time analyzing a new asset class, exploring Vibe-Trading
capabilities, or checking data source availability for a specific market.

---

## Mode 2: Research

**Purpose**: Deep multi-agent research on a specific stock, sector, or theme.

```
Step 1. get_market_data → fetch OHLCV for context
Step 2. factor_analysis → screen for quality factors (if multi-stock universe)
Step 3. run_swarm("investment_committee", {target, market}) → team analysis
Step 4. (conditional) pattern_recognition → requires a run_dir with OHLCV artifacts.
        If no prior backtest exists, run a lightweight backtest first (Mode 4 Steps 2-4)
        to create the run_dir, then call pattern_recognition on it.
        Skip this step if chart patterns are not needed.
Step 5. Synthesize: combine factor scores, swarm report, and patterns (if available)
```

**When to use**: Before making investment decisions, for weekly deep-dives, or
when the project's daily pipeline signals something worth investigating.

**Output**: Structured research report with:
- Factor quality assessment
- Multi-agent consensus/disagreement
- Chart pattern context
- Actionable recommendation with confidence level

---

## Mode 3: Cross-Validation

**Purpose**: Validate the project's daily pipeline signals against Vibe-Trading's
independent analysis.

```
Step 1. Read today's pipeline outputs (outputs/today/{date}/)
Step 2. For each BUY/SELL signal from the pipeline:
   a. get_market_data → fetch same asset via Vibe-Trading
   b. run_swarm("quant_strategy_desk", {target}) → independent quant view
   c. analyze_options → pricing context if options-relevant
Step 3. Compare: project signal vs swarm consensus
Step 4. Flag agreements (high confidence) and disagreements (investigate further)
```

**When to use**: End-of-day validation of high-conviction signals, weekly
cross-check routine, or when signals seem suspicious.

**Integration point**: Feeds into `ai-quality-evaluator` for combined scoring.

---

## Mode 4: Strategy

**Purpose**: End-to-end strategy development from hypothesis to backtested results.

```
Step 1. load_skill("strategy-generate") → read strategy design methodology
Step 2. Write signal_engine.py based on hypothesis
Step 3. Write config.json with target asset and date range
Step 4. backtest(run_dir) → execute vectorized backtest
Step 5. pattern_recognition(run_dir) → overlay patterns on backtest data
Step 6. Evaluate metrics: Sharpe > 1.0, MDD < 20%, win_rate > 50%
Step 7. If metrics pass → run_swarm("investment_committee") for sanity check
Step 8. If swarm validates → strategy ready for paper trading
```

**When to use**: New strategy ideas, optimizing existing strategies, or
developing cross-market strategies not covered by the project's 7 native
strategies.

---

## Mode Selection Guide

| User Intent | Mode | Example Trigger |
|-------------|------|-----------------|
| "What can Vibe-Trading do for crypto?" | Discovery | Explore capabilities |
| "Deep-dive on AAPL" | Research | Multi-agent analysis |
| "Verify today's BUY signal on MSFT" | Cross-Validation | Pipeline check |
| "Build a momentum strategy for A-shares" | Strategy | Hypothesis → backtest |
| "Compare my Turtle signals with AI agents" | Cross-Validation | Signal comparison |
| "Factor screen the KOSPI 200" | Research | Factor analysis focus |

## Execution Pattern

When the orchestrator determines the appropriate mode, it invokes the
relevant vibe-trading-* skills in sequence using subagents:

1. **Sequential dependencies**: Each step waits for the previous step's output
2. **Parallel where possible**: In Research mode, factor_analysis and
   run_swarm can run in parallel since they don't depend on each other
3. **Fail-fast**: If data fetch fails, stop before burning swarm tokens
4. **Cost gate**: Estimate token usage before launching swarms; warn if
   expected cost > $0.50

## Integration with Project Ecosystem

| Project Skill | Orchestrator Integration |
|---------------|-------------------------|
| `today` | Cross-Validation mode reads its outputs |
| `daily-strategy-engine` | Strategy mode complements the 7 native strategies |
| `alphaear-orchestrator` | Research mode runs in parallel for comparison |
| `trading-intel-orchestrator` | Research mode provides independent second opinion |
| `ai-quality-evaluator` | Cross-Validation output feeds quality scoring |
| `role-dispatcher` | Research mode's swarm = Vibe's version of multi-role analysis |

## Error Handling

| Scenario | Action |
|----------|--------|
| MCP server not responding | Remind user to run vibe-trading-setup |
| Data unavailable for symbol | Suggest alternative symbol format or source |
| Swarm timeout (> 30 min) | Reduce scope or skip swarm step |
| Backtest returns poor metrics | Report findings honestly; do not force validation |
| LLM API rate limited | Wait and retry with exponential backoff |
