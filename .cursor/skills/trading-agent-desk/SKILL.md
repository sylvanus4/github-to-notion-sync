# Trading Agent Desk

Run a multi-agent debate-based trading analysis inspired by TradingAgents (arXiv 2412.20138). Replicates a Wall Street trading desk with 4 analyst agents, bull/bear dialectical debate, research manager synthesis, and risk evaluation gate — all integrated with our existing pipeline data.

## Trigger Phrases

- "agent desk", "trading desk", "에이전트 데스크", "트레이딩 데스크"
- "run agent desk", "에이전트 데스크 실행"
- "bull bear debate", "불/베어 토론"
- "multi-agent trade decision", "멀티 에이전트 매매 결정"
- "trading-agent-desk", "/agent-desk"

Do NOT use for:
- Daily stock signals without debate (use `daily-stock-check`)
- AlphaEar sentiment-only analysis (use `alphaear-sentiment`)
- Weekly price updates (use `weekly-stock-update`)
- MiroFish swarm simulations (use `mirofish`)
- Simple portfolio rebalancing (use `trading-position-sizer`)

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

## Pipeline Phases

### Phase 1: Analyst Reports (Parallel)

4 analyst agents run concurrently using the quick model:
- **Technical Analyst**: Consumes `analysis-{date}.json` (MA, RSI, MACD, ADX, Bollinger)
- **Fundamental Analyst**: Consumes screener data (P/E, PBR, FCF yield)
- **Sentiment Analyst**: Consumes alphaear-sentiment outputs
- **News Analyst**: Consumes alphaear-news outputs

Each produces a structured `AnalystReport` with a bullish score (0-100) and key points.

### Phase 2: Bull/Bear Debate

A configurable number of debate rounds (default: 2) between:
- **Bull Researcher**: Argues for investing, citing growth potential and positive indicators
- **Bear Researcher**: Argues against, highlighting risks and overvaluation

Both receive all 4 analyst reports, the full debate history, and BM25 memory retrieval of similar past situations.

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
