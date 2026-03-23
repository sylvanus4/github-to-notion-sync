# Money Machine

## Description

Master orchestrator that runs the full autonomous money-making pipeline end-to-end: data sync → stock screening → signal generation → content creation → content quality gate → content distribution → paper trading → P&L reporting → feedback loop. Composes `today`, `content-auto-gate`, `stock-content-printer`, `paper-trading-validator`, `daily-pnl-report`, and `affiliate-manager` into a single sequential workflow.

## Triggers

Use when the user asks to:
- "run money machine", "make money", "autonomous pipeline"
- "money-machine", "full pipeline", "daily autonomous run"
- "머니 머신", "돈 벌어", "자동 수익 파이프라인", "전체 파이프라인"
- "run everything", "daily money pipeline"

Do NOT use for:
- Running only the stock analysis pipeline (use `today`)
- Running only content generation (use `stock-content-printer`)
- Running only paper trading (use `paper-trading-validator`)
- Running only P&L reporting (use `daily-pnl-report`)
- Individual skill execution

## Pipeline Stages

The pipeline runs sequentially. Each stage depends on the previous stage's output.

### Stage 1: Data Sync & Analysis (`today` pipeline)

Runs the full `today` skill:
- Stock price sync from Yahoo Finance
- Hot stock discovery (NASDAQ/KOSPI/KOSDAQ 100)
- Multi-factor screening (P/E, RSI, volume, MA crossovers, FCF yield)
- Turtle/Bollinger/DualMA/Oscillator analysis
- News fetch and sentiment analysis
- Daily .docx report generation
- Slack posting to #h-report

**Output**: `outputs/screener-{date}.json`, `outputs/analysis-{date}.json`, `outputs/reports/daily-{date}.docx`

### Stage 2: Content Generation (`stock-content-printer`)

Generates multi-channel content drafts from screener data:
- Twitter thread drafts (market summary + top picks)
- YouTube Shorts script (60s AI signal explainer)
- Newsletter copy (weekly digest if Friday)
- Affiliate content (themed product recommendations)

**Output**: `outputs/content/drafts/drafts-{date}.json`

### Stage 3: Content Quality Gate (`content-auto-gate`)

Scores each draft on 5 dimensions using LLM + rule-based checks:
- Accuracy, Compliance, Tone, Completeness, Originality
- Auto-approves drafts scoring ≥ 7.0/10
- Blocks drafts with credential leaks or guarantee language

**Output**: `outputs/content/approved/*.json`, `outputs/content/gate-report-{date}.json`

### Stage 4: Content Distribution

Posts approved content to channels:

```bash
# Twitter
cd backend && python scripts/twitter_poster.py --date $(date +%Y-%m-%d)

# Affiliate tweets
cd backend && python scripts/affiliate_poster.py --date $(date +%Y-%m-%d)

# YouTube Shorts (if approved)
cd backend && python scripts/youtube_uploader.py --date $(date +%Y-%m-%d)
```

### Stage 5: Paper Trading (`paper-trading-validator`)

Executes BUY/SELL signals via Alpaca paper trading account:

```bash
cd backend
python -c "
from app.services.broker import AlpacaBroker
from app.services.broker.signal_bridge import load_screener_signals, execute_signals, RiskLimits
from datetime import datetime

broker = AlpacaBroker(paper=True)
signals = load_screener_signals(datetime.now().strftime('%Y-%m-%d'))
limits = RiskLimits(max_position_pct=0.05, max_daily_loss_pct=0.02)
results = execute_signals(broker, signals, limits, dry_run=False)
print(f'Executed {len(results)} signals')
"
```

### Stage 6: P&L Reporting (`daily-pnl-report`)

Generates portfolio snapshot and posts to Slack:

```bash
cd backend
python -c "
from app.services.broker import AlpacaBroker
from app.services.portfolio_tracker import generate_pnl_report

broker = AlpacaBroker(paper=True)
report = generate_pnl_report(broker, days=7)
snap = report['current_snapshot']
print(f'Equity: \${snap[\"equity\"]:,.2f}')
print(f'P&L: \${snap[\"unrealized_pnl\"]:+,.2f} ({snap[\"unrealized_pnl_pct\"]:+.1f}%)')
"
```

### Stage 7: Feedback Loop

Evaluates past signals against actual outcomes:

```bash
cd backend
python -c "
from app.services.feedback_loop import rolling_accuracy
result = rolling_accuracy(days=14)
print(f'Rolling accuracy: {result[\"overall_accuracy_pct\"]}%')
print(f'Evaluated: {result[\"total_evaluated\"]} signals')
"
```

## Safety Rails

- **Kill switch**: If drawdown exceeds 5%, halt all new entries
- **Daily loss limit**: Max 2% account loss per day
- **Position sizing**: Max 5% per position, 20% per sector
- **Content compliance**: All content passes quality gate before distribution
- **Paper-first**: All strategies start in paper mode; live only after graduation criteria met

## Monitoring

After the pipeline completes, check:
1. Slack #h-report for daily analysis
2. Portfolio page at `/portfolio` for positions and P&L
3. `outputs/content/gate-report-{date}.json` for content quality
4. `outputs/feedback/` for signal accuracy trends

## Schedule

Designed to run once daily:
- **Weekdays**: Full pipeline (markets open)
- **Weekends/Holidays**: Skip trading stages (Stages 5-6), run content + analysis only
