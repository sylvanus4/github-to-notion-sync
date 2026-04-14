# AutoHedge

Install, configure, and operate AutoHedge — a Swarms-based autonomous multi-agent hedge fund system with 5 specialized AI agents (Director, Quant, Sentiment, Risk Management, Execution). Orchestrates end-to-end trading workflows from market analysis through order execution on Solana DEX venues.

## Triggers

Use when the user asks to:
- "run autohedge", "autohedge trading", "autonomous hedge fund"
- "swarms trading", "multi-agent hedge fund", "AutoHedge"
- "오토헤지", "자율 헤지펀드", "스웜즈 트레이딩"
- "autohedge setup", "install autohedge", "autohedge 설치"
- "run autohedge analysis", "autohedge sentiment", "autohedge pipeline"

Do NOT use for:
- Project-native daily stock analysis (use `daily-stock-check` or `today`)
- MiroFish multi-agent simulation (use `mirofish` or `mirofish-financial-sim`)
- Vibe-Trading orchestration (use `vibe-trading-orchestrator`)
- KIS/Toss broker integration (use `kis-team` or `toss-ops-orchestrator`)
- Internal trading agent desk debate analysis (use `trading-agent-desk`)
- General market environment analysis without AutoHedge context (use `trading-market-environment-analysis`)

## Prerequisites

| Prerequisite | Check Command | Install |
|---|---|---|
| Python 3.10+ | `python3 --version` | System package manager |
| `autohedge` package | `pip show autohedge` | `pip install -U autohedge` |
| `OPENAI_API_KEY` env var | `echo $OPENAI_API_KEY` | Set in `.env` or shell |
| Solana wallet (for live trading) | Check `.env` for `SOLANA_PRIVATE_KEY` | Generate via Solana CLI |

## Architecture

AutoHedge uses the [Swarms](https://github.com/kyegomez/swarms) AI agent framework to coordinate 5 specialized agents in a pipeline:

```
┌─────────────────────────────────────────────────────────┐
│                    AutoHedge Pipeline                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  User Task ──► Director Agent                           │
│                    │                                    │
│                    ├──► Quant Agent (technical analysis) │
│                    ├──► Sentiment Agent (market mood)    │
│                    ├──► Risk Management Agent            │
│                    └──► Execution Agent (DEX orders)     │
│                                                         │
│  Tools: search_tokens, get_token_price,                 │
│         execute_trade, get_holdings, get_order           │
│                                                         │
│  Venue: Solana DEX (Jupiter aggregator)                 │
└─────────────────────────────────────────────────────────┘
```

### Agent Roles

| Agent | Role | Key Output |
|---|---|---|
| **Director** | Orchestrator — coordinates other agents, synthesizes final thesis | Trading decision with confidence level |
| **Quant** | Technical/quantitative analysis — price patterns, indicators, risk metrics | Quantitative signals and position recommendations |
| **Sentiment** | Market sentiment from news, social media, on-chain data | Sentiment score (-100 to +100) and narrative |
| **Risk Management** | Position sizing, stop-loss, portfolio exposure limits | Risk-adjusted position size and limits |
| **Execution** | Order placement on Solana DEX via Jupiter | Trade execution status and confirmation |

## Workflow

### Phase 1: Setup & Verification

```bash
pip install -U autohedge
```

Verify installation:

```bash
python3 -c "from autohedge import AutoHedge; print('OK')"
```

Ensure environment variables are set (`.env` file in project root or exported):

```
OPENAI_API_KEY=sk-...
SOLANA_PRIVATE_KEY=...         # only for live execution
SOLANA_RPC_URL=...             # optional, defaults to public endpoint
```

### Phase 2: Run Analysis (Read-Only)

For analysis-only mode (no trade execution):

```python
from autohedge import AutoHedge

system = AutoHedge(
    name="analysis-fund",
    description="Read-only market analysis",
)

result = system.run(
    task="Analyze the sentiment of the AI token market and provide a thesis on emerging trends."
)
print(result)
```

### Phase 3: Interactive REPL

AutoHedge includes a CLI with interactive REPL:

```bash
python3 -m autohedge
```

This launches a prompt where you can submit natural-language trading tasks iteratively.

### Phase 4: Full Pipeline (with Execution)

For live trading (requires Solana wallet credentials):

```python
from autohedge import AutoHedge

system = AutoHedge(
    name="swarms-fund",
    description="Private Hedge Fund for Swarms Corp",
)

result = system.run(
    task="Find undervalued Solana DeFi tokens with strong fundamentals and execute a diversified position."
)
print(result)
```

## Safety Rules

1. **Never execute live trades without explicit user confirmation** — always preview the Director's thesis first
2. **Verify `SOLANA_PRIVATE_KEY` is NOT committed to git** — check `.gitignore`
3. **Start with analysis-only tasks** before enabling execution
4. **Monitor agent outputs** — the Director agent coordinates all others; review its reasoning chain
5. **Position sizing** — Risk Management agent enforces limits, but user should set conservative bounds initially

## Integration with Project Pipeline

AutoHedge operates independently from the project's native pipeline (`today`, `daily-stock-check`). To cross-reference:

1. Run `today` pipeline for native stock screening and signals
2. Feed `today` output themes into AutoHedge as task prompts for Solana DEX perspective
3. Compare thesis alignment between native TA signals and AutoHedge agent consensus

## Tools Available to Agents

| Tool | Description |
|---|---|
| `search_tokens` | Search Solana tokens via Jupiter aggregator |
| `get_token_price` | Fetch real-time token price data |
| `execute_trade` | Place a trade on Solana DEX |
| `get_holdings` | Query current portfolio holdings |
| `get_order` | Check order status |

## Outputs

- Director agent final thesis (markdown-formatted trading decision)
- Individual agent analysis reports (quant, sentiment, risk)
- Execution confirmation (when trades are placed)
- Conversation history (full agent communication log)

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: autohedge` | Package not installed | `pip install -U autohedge` |
| `OPENAI_API_KEY not set` | Missing env var | Set in `.env` or export |
| Agent returns empty response | API rate limit or model error | Check OpenAI API status, retry |
| Trade execution fails | Invalid wallet or insufficient balance | Verify `SOLANA_PRIVATE_KEY` and SOL balance |
| `Connection refused` on RPC | Bad RPC endpoint | Set `SOLANA_RPC_URL` to a reliable endpoint |

## Source

- **Repository**: [The-Swarm-Corporation/AutoHedge](https://github.com/The-Swarm-Corporation/AutoHedge)
- **License**: MIT
- **Framework**: [Swarms](https://github.com/kyegomez/swarms) multi-agent orchestration
- **Venue**: Solana DEX (Jupiter aggregator)
