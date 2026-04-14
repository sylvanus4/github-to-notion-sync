---
name: trading-agent-desk
description: >-
  Run a multi-agent debate-based trading analysis inspired by TradingAgents
  (arXiv 2412.20138). Replicates a Wall Street trading desk with 4 analyst
  agents, bull/bear dialectical debate, research manager synthesis, and risk
  evaluation gate — all integrated with our existing pipeline data.
  Use when the user asks to "run agent desk", "agent desk", "trading desk",
  "에이전트 데스크", "트레이딩 데스크", "에이전트 데스크 실행",
  "bull bear debate", "불/베어 토론", "multi-agent trade decision",
  "멀티 에이전트 매매 결정", "trading-agent-desk", or "/agent-desk".
  Do NOT use for daily stock signals without debate (use daily-stock-check).
  Do NOT use for AlphaEar sentiment-only analysis (use alphaear-sentiment).
  Do NOT use for weekly price updates (use weekly-stock-update).
  Do NOT use for MiroFish swarm simulations (use mirofish).
  Do NOT use for simple portfolio rebalancing (use trading-position-sizer).
triggers:
  - agent desk
  - trading desk
  - 에이전트 데스크
  - 트레이딩 데스크
  - bull bear debate
  - 불/베어 토론
  - multi-agent trade decision
  - 멀티 에이전트 매매 결정
  - trading-agent-desk
tags: [trading, multi-agent, debate, analysis, risk]
metadata:
  author: "thaki"
  version: "1.1.0"
  category: "trading"
---

# Trading Agent Desk

## Architecture

```
┌──────────────────────────────────────────────────┐
│                  Agent Trading Desk               │
├──────────────────────────────────────────────────┤
│ Phase 1: Analysts (parallel, quick_model)         │
│  ┌─────────┐ ┌────────────┐ ┌──────────┐ ┌────┐ │
│  │Technical│ │Fundamental │ │Sentiment │ │News│ │
│  └────┬────┘ └─────┬──────┘ └────┬─────┘ └─┬──┘ │
│       └────────────┼────────────┼──────────┘    │
│                    ▼                             │
│ Phase 2: Bull/Bear Debate (N rounds, deep_model) │
│  ┌──────────────────────────────────────────┐    │
│  │ Round 1: Bull argues → Bear counters     │    │
│  │ Round 2: Bull rebuts → Bear rebuts       │    │
│  │ + BM25 Memory injection of past lessons  │    │
│  └──────────────────┬───────────────────────┘    │
│                     ▼                            │
│ Phase 3: Research Manager (deep_model)           │
│  ┌──────────────────────────────────────────┐    │
│  │ Synthesize debate → BUY/SELL/HOLD        │    │
│  │ + confidence score + rationale           │    │
│  └──────────────────┬───────────────────────┘    │
│                     ▼                            │
│ Phase 4: Risk Evaluator (quick_model)            │
│  ┌──────────────────────────────────────────┐    │
│  │ Position sizing + risk-adjusted decision │    │
│  └──────────────────┬───────────────────────┘    │
│                     ▼                            │
│ Output: DeskDecision per symbol                  │
│ Memory: Store decision + situation for learning  │
└──────────────────────────────────────────────────┘
```

## Examples

```
User: "NVDA에 대해 트레이딩 데스크 분석 돌려줘"
→ 4 analysts fan-out (Bull, Bear, Macro, Sentiment) → Risk Manager → Debate → DeskDecision

User: "trading-agent-desk AAPL TSLA --skip-sentiment"
→ Multi-symbol desk analysis, Sentiment Analyst skipped, remaining 3 analysts + synthesis

User: "agent desk debate on semiconductor sector"
→ Sector-level analysis across multiple tickers, debate-driven consensus
```

## Temporal Context

All agent prompts MUST receive a system suffix with the current timestamp:

```
Current date/time: {ISO 8601 timestamp, e.g. 2026-04-14T09:30:00+09:00}
Market session: {pre-market | regular | after-hours | closed}
```

This prevents stale-date hallucinations and enables agents to factor in time-sensitive conditions (earnings date proximity, options expiry, economic calendar events).

## Pipeline Phases

### Phase 1: Analyst Reports (Parallel)

4 analyst agents run concurrently using the quick model. Each analyst MUST follow a structured methodology checklist in its prompt:

- **Technical Analyst**: Consumes `analysis-{date}.json` (MA, RSI, MACD, ADX, Bollinger). Methodology checklist: (1) identify primary trend via SMA 20/55/200 alignment, (2) assess momentum via RSI/MACD divergence, (3) evaluate volatility regime via Bollinger width and ADX, (4) check volume confirmation, (5) identify nearest support/resistance levels.
- **Fundamental Analyst**: Consumes screener data (P/E, PBR, FCF yield). Methodology checklist: (1) relative valuation vs sector median, (2) earnings quality (FCF/net income ratio), (3) balance sheet health (debt/equity, current ratio), (4) growth trajectory (revenue/earnings YoY), (5) capital allocation efficiency (ROIC, buybacks).
- **Sentiment Analyst**: Consumes alphaear-sentiment outputs. Methodology checklist: (1) aggregate sentiment polarity and confidence, (2) sentiment trend direction (improving/deteriorating over 7d), (3) volume of sentiment data points (sample size), (4) source diversity (news, social, analyst), (5) contrarian signal detection (extreme readings).
- **News Analyst**: Consumes alphaear-news outputs. Methodology checklist: (1) recency-weight events (last 24h vs 7d), (2) classify catalyst type (earnings, regulatory, macro, sector), (3) assess market reaction vs news magnitude, (4) identify upcoming catalysts within 14d, (5) cross-reference with sector peers.

Each produces a structured `AnalystReport` with a bullish score (0-100), key points, and methodology compliance flags.

### Phase 2: Bull/Bear Debate

A configurable number of debate rounds (default: 2) between:
- **Bull Researcher**: Argues for investing, citing growth potential and positive indicators
- **Bear Researcher**: Argues against, highlighting risks and overvaluation

Both receive all 4 analyst reports, the full debate history, and BM25 memory retrieval of similar past situations.

**Consensus Fast-Track**: If all 4 analyst bullish scores agree directionally (all ≥ 70 or all ≤ 30), the debate phase is shortened to 1 round and the Research Manager receives a `consensus_flag: true` annotation. This saves ~40% of deep-model token cost on clear-cut situations while preserving the full debate for genuinely ambiguous signals.

### Phase 3: Research Manager Synthesis

A senior manager agent reads the complete debate transcript and makes a definitive BUY/SELL/HOLD decision with:
- Confidence score (0-100)
- Detailed rationale in Korean
- Key factors driving the decision
- Strategic action suggestions

### Phase 4: Risk Evaluator

A risk management gate that:
- Assesses the research decision's risk/reward profile
- Determines position size (0-N% of portfolio)
- Applies confidence-weighted risk scoring
- Produces the final `DeskDecision`

The risk evaluator prompt MUST include the following quantitative dimensions (inspired by AutoHedge's structured risk depth):

1. **Value at Risk (VaR)**: Estimate 1-day and 5-day VaR at 95% confidence using recent 60-day returns
2. **Stress scenarios**: Evaluate impact under 3 scenarios — sector correction (-10%), broad market crash (-20%), liquidity crisis (2x spread widening)
3. **Correlation risk**: Flag if the position is highly correlated (ρ > 0.7) with existing portfolio holdings
4. **Maximum drawdown context**: Reference the stock's historical max drawdown and current distance from ATH
5. **Greeks exposure** (options-relevant positions only): Delta, Gamma, Vega sensitivity estimates

Each dimension produces a sub-score (GREEN/YELLOW/RED). If any dimension scores RED, position size is automatically capped at 50% of the base calculation.

### Phase 4.5: Execution Compliance Gate

Before the final `DeskDecision` is emitted, a lightweight compliance check validates:

1. **Regulatory**: No wash-sale violations (check 30-day trade history for same symbol), no insider-window conflicts
2. **Slippage estimate**: Flag if average daily volume < 10x proposed position size (illiquidity risk)
3. **Timing**: Warn if execution falls within 15 minutes of market open/close (high-volatility windows)
4. **Concentration**: Reject if resulting single-position weight would exceed 15% of portfolio

Compliance failures downgrade the decision confidence by 20 points and append a `compliance_warnings` array to the output. CRITICAL failures (wash-sale, concentration breach) convert the decision to HOLD regardless of signal strength.

### Memory & Reflection

Decisions are stored in a BM25-indexed memory store (`outputs/agent-desk/memory/trade_memory.json`). After market close, the `reflect_and_remember` function compares decisions against actual returns and generates lessons learned.

## Execution Steps

1. **Verify prerequisites**: Ensure `analysis-{date}.json` and `screener-{date}.json` exist in `outputs/`
2. **Initialize desk**: Create `AgentDesk` with deep and quick LLM clients
3. **Configure run**: Set symbols, date, debate rounds, model names
4. **Execute**: Call `desk.run(config)` — this runs the full 4-phase pipeline
5. **Save results**: Output stored at `outputs/agent-desk/{date}/desk-decisions.json`
6. **Optional reflection**: After market data is available, run reflection for learning

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `debate_rounds` | 2 | Number of bull/bear debate rounds |
| `deep_model` | gpt-4o | Model for debate and synthesis (high quality) |
| `quick_model` | gpt-4o-mini | Model for analysts and risk eval (cost efficient) |
| `memory_matches` | 2 | Number of past situations to retrieve from BM25 memory |
| `max_symbols` | 5 | Maximum symbols to process per run |

## Cost Estimation

Per symbol: ~4 analyst calls (quick) + 4 debate calls (deep) + 1 synthesis (deep) + 1 risk eval (quick) ≈ 5 quick + 5 deep calls.
- Quick model (~$0.001/call): $0.005/symbol
- Deep model (~$0.03/call): $0.15/symbol
- **Total**: ~$0.16/symbol, ~$0.80 for 5 symbols

## Source Files

- `backend/app/services/agent_desk/desk.py` — Main orchestrator
- `backend/app/services/agent_desk/analysts.py` — 4 analyst agents
- `backend/app/services/agent_desk/debate.py` — Bull/bear debate + research manager
- `backend/app/services/agent_desk/risk.py` — Risk evaluator gate
- `backend/app/services/agent_desk/memory.py` — BM25 trade memory store
- `backend/app/services/agent_desk/reflection.py` — Post-decision reflection
- `backend/app/services/agent_desk/schemas.py` — Pydantic schemas
- `backend/app/services/agent_desk/prompts.py` — Prompt templates
- `docs/tradingagents-analysis/README.md` — Design document

## Reference

- Paper: [TradingAgents: Multi-Agents LLM Financial Trading Framework](https://arxiv.org/abs/2412.20138)
- Repository: [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents)
