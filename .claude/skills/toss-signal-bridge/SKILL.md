---
name: toss-signal-bridge
description: >-
  Read today's analysis pipeline signals (screener/analysis outputs) and
  translate them into tossctl order previews. Does NOT execute orders — only
  previews and presents ranked trade candidates. Routes to tossinvest-trading
  for execution if user approves. Applies position sizing via
  trading-position-sizer logic. Use when the user asks to "convert signals to
  orders", "signal to order", "pipeline to toss", "시그널 매매 연계", "분석 결과로 주문",
  "preview trades", "bridge signals", or when invoked by the today pipeline
  (Phase 5.5). Do NOT use for direct order execution (use tossinvest-trading).
  Do NOT use for portfolio reconciliation (use toss-portfolio-recon). Do NOT
  use for risk scoring (use toss-risk-monitor).
---

# toss-signal-bridge

Bridge analysis pipeline signals to tossctl order previews — the critical link between analysis and execution.

## When to Use

- After `today` pipeline generates BUY/SELL signals
- When user wants to act on pipeline recommendations via Toss
- Preview mode before committing to trades
- Part of the daily pipeline Phase 5.5

## When NOT to Use

- For direct order execution → use `tossinvest-trading`
- For portfolio reconciliation → use `toss-portfolio-recon`
- For risk assessment → use `toss-risk-monitor`

## Prerequisites

- `tossctl` installed and in PATH
- Active authenticated session
- Today's pipeline outputs — prefers `outputs/strategy-cards-{date}.json` (Phase 5b strategy engine); falls back to `outputs/screener-*.json` and `outputs/analysis-*.json`

## SAFETY: Preview Only

This skill NEVER executes orders. It operates entirely within Layer 3 (preview/dry-run) of the tossinvest-trading safety model. All output is informational — the user must explicitly invoke `tossinvest-trading` to execute.

## Workflow

### Step 1: Load Pipeline Signals

**Preferred source (v1.1+)**: Load strategy cards from the daily strategy engine (Phase 5b):

```bash
cat outputs/strategy-cards-$(date +%Y-%m-%d).json
```

Each strategy card provides precise `entry_price`, `stop_loss`, `target_price`, `position_size_pct`, composite `score`, and `signal` (BUY/SELL) backed by a full backtest. Use these directly for order previews — no additional screening needed.

**Fallback**: If strategy cards are not available, load the legacy screener and analysis outputs:

```bash
ls -t outputs/screener-*.json | head -1
ls -t outputs/analysis-*.json | head -1
```

Parse for entries with actionable signals (the screener uses three values):
- **NEUTRAL** (composite_score ≥ 40): favorable setup — potential new positions
- **CAUTION** (score 15–39): mixed technicals — watch only
- **AVOID** (score < 15): unfavorable — potential exits if currently held

### Step 1.5: TV Sentiment Pre-Filter

Before generating order previews, check TradingView sentiment data to flag emotionally-charged symbols. Load the TV sentiment output:

```bash
cat backend/outputs/tv-sentiment-$(date +%Y-%m-%d).json
```

For each candidate symbol, look up `sentiments[SYMBOL]`:
- **Bearish sentiment (score < -0.3)** on a BUY signal: Downgrade to WATCH. Add warning: "⚠️ TV 감성 부정적 — 매수 보류 권장"
- **Bullish sentiment (score > 0.3)** on a SELL signal: Add caution note: "ℹ️ TV 감성 긍정적 — 매도 재확인 필요"
- **Neutral or no data**: Proceed normally

This filter is advisory — it downgrades signals but never blocks user-approved execution. TV sentiment data is produced by default during the `today` pipeline. If the TV sentiment file is missing (TradingView MCP unavailable or `--skip-tradingview` was used), skip this step entirely and proceed.

### Step 2: Filter Tradeable Symbols

Filter to symbols tradeable on Toss Securities:
- US tickers (NYSE/NASDAQ): direct match
- KRX codes (6-digit numeric): direct match
- Skip ETFs or instruments not supported by Toss

### Step 3: Get Current Prices

For each candidate symbol:

```bash
tossctl quote get <symbol> --output json
```

### Step 4: Check Existing Exposure

```bash
tossctl portfolio positions --output json
```

Cross-reference:
- For NEUTRAL signals: check if already held (avoid doubling)
- For AVOID signals: check if actually held (can't sell what you don't own)

### Step 5: Position Sizing

**When using strategy cards**: Each card includes `position_size_pct` (default 5% of equity) and precise `entry_price`. Calculate share quantity directly:

```
share_qty = (equity × position_size_pct) / entry_price
```

**Legacy fallback**: For screener-based candidates, apply position sizing logic:

```bash
tossctl account summary --output json
```

Calculate:
- Available buying power
- Target position size (e.g., 3-5% of equity per position)
- Share quantity: `target_allocation / current_price`
- FX consideration for US stocks (use `toss-fx-monitor` rate if available)

### Step 6: Prerequisite — Permissions Check (Layer 2)

Before generating any order preview, verify that `tossinvest-trading` permissions are granted for the session. The `toss-signal-bridge` skill itself NEVER executes trades — but order previews still require an active, authenticated session:

```bash
tossctl auth status
```

If the session is not active, prompt the user to authenticate first.

### Step 7: Order Preview (Layer 3 — Dry Run)

For each candidate, generate a dry-run preview using `tossctl order place` **without the `--execute` flag**. This follows Layer 3 of the `tossinvest-trading` 6-layer safety model:

```bash
tossctl order place <buy|sell> <SYMBOL> --qty <N> --limit <PRICE> --output json
```

Without `--execute`, this returns a preview showing estimated cost, fees, and order details — no real order is submitted. This is the correct command; there is no separate `preview` subcommand.

### Step 8: Ranked Presentation

Present all candidates ranked by signal strength, in Korean. Include TV sentiment status where available:

```
🔗 시그널 → 주문 미리보기 (2026-03-24)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
파이프라인 시그널 8개 → 실행 가능 5개 (TV 감성 필터 적용)

📈 매수 후보:
┌──────┬────────┬────────┬──────┬──────────┬────────────┐
│ 순위 │ 종목   │ 시그널 │ 수량 │ 예상 비용│ TV 감성    │
├──────┼────────┼────────┼──────┼──────────┼────────────┤
│ 1    │ NVDA   │ ★★★★★ │ 5주  │ $4,250   │ 긍정 (+0.6)│
│ 2    │ 005930 │ ★★★★  │ 10주 │ ₩780,000 │ 중립       │
│ 3    │ AMD    │ ★★★   │ 15주 │ $2,100   │ —          │
└──────┴────────┴────────┴──────┴──────────┴────────────┘

⚠️ TV 감성 필터 보류:
- PLTR: BUY 시그널 but TV 감성 부정적 (-0.45) → 매수 보류 권장

📉 매도 후보:
- TSLA: AVOID (보유 중, 손익 -8.2%) ℹ️ TV 감성 긍정적 — 매도 재확인

💡 실행하려면 tossinvest-trading 스킬을 사용하세요.
   (6-layer 안전 모델 적용됨)
```

### Step 9: Slack Posting (Pipeline Mode)

When invoked as part of the `today` pipeline Phase 5.5, include the preview summary in the Slack thread under "Toss 실행 가능 시그널" section.

## Examples

```
User: 오늘 시그널 브릿지 돌려줘
Agent: toss-signal-bridge 실행 →
  NEUTRAL 시그널 종목 2개 → 주문 프리뷰 생성 (실행 없음):
  - PLTR: 매수 15주 @ $78.20 → 예상 비용 $1,173.00
  - SOFI: 매수 30주 @ $14.80 → 예상 비용 $444.00
  AVOID 시그널 보유 종목 1개 → 매도 프리뷰:
  - TSLA: 매도 5주 @ $245.00 → 예상 수익 $1,225.00

User: toss signal bridge --dry-run
Agent: (runs the full pipeline, generates order previews without execution)

User: /today (with skip-toss not set)
Agent: Phase 5.5에서 자동으로 toss-signal-bridge 실행
```

## Error Handling

| Error | Action |
|-------|--------|
| `No active session` | Prompt `tossctl auth login` |
| No pipeline outputs | Inform user to run `today` pipeline first |
| Quote fetch failed | Skip symbol, note in report |
| Insufficient buying power | Flag in report, reduce quantity suggestion |
| Symbol not tradeable on Toss | Skip with note |
