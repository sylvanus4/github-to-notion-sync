---
name: daily-strategy-engine
version: 1.1.0
description: >-
  Generate 10 backtested daily trading strategy cards from 7 strategies
  (Turtle, DualMA, Bollinger I–IV, OvernightDipBuy) across 16 blue-chip
  stocks (KR + US), with commission-aware simulations and risk-adjusted ranking.
  OvernightDipBuy buys afternoon dips and sells next-morning opens, requiring
  net returns above bank interest after fees.
  Use when the user asks to "generate daily strategies", "today's strategy cards",
  "backtested trade recommendations", "daily trading plan", "매매 전략 카드",
  "일일 전략", "백테스트 전략 추천", "daily-strategy-engine", "overnight dip buy",
  "오버나이트 전략", or wants commission-aware backtested trading recommendations.
  Do NOT use for daily stock checks without strategy cards (use daily-stock-check).
  Do NOT use for manual backtesting of a single strategy (use trading-backtest-expert).
  Do NOT use for Toss order execution (use tossinvest-trading).
  Do NOT use for weekly price sync (use weekly-stock-update).
triggers:
  - daily strategy
  - strategy cards
  - backtested strategies
  - trading plan
  - daily trading
  - 매매 전략 카드
  - 일일 전략
  - 백테스트 전략
  - 전략 엔진
  - generate strategies
  - overnight dip buy
  - 오버나이트 전략
  - dip buy strategy
tags: [trading, backtest, strategy, signals, pipeline, daily, overnight]
metadata:
  author: "thaki"
  category: "trading"
---

# daily-strategy-engine

Generate 10 backtested daily strategy cards ranked by risk-adjusted return, with precise entry/stop/target prices and commission-aware P&L. Includes the OvernightDipBuy strategy for short-term dip-buying with emotion-free paired limit orders.

## Stock Universe (16 tickers)

### Required (6)

| Symbol | Name |
|--------|------|
| 005930 | Samsung Electronics |
| 032830 | Samsung Life Insurance |
| 000660 | SK Hynix |
| NVDA | NVIDIA |
| GOOGL | Alphabet |
| 071050 | Korea Investment Holdings |

### Additional Blue-Chips (10)

| Symbol | Name |
|--------|------|
| 035420 | NAVER |
| 005380 | Hyundai Motor |
| 207940 | Samsung Biologics |
| 012450 | Hanwha Aerospace |
| 068270 | Celltrion |
| AVGO | Broadcom |
| TSM | TSMC |
| AMD | AMD |
| META | Meta Platforms |
| MSFT | Microsoft |

## Strategies (7)

1. **Turtle Trading** — Donchian channel breakout (20-day entry / 10-day exit)
2. **DualMA Crossover** — SMA 20/55 golden/death cross
3. **Bollinger Method I** — %B breakout with volume confirmation
4. **Bollinger Method II** — Mean reversion squeeze
5. **Bollinger Method III** — Bandwidth expansion breakout
6. **Bollinger Method IV** — Walking-the-bands trend following
7. **OvernightDipBuy** — Buy afternoon dips (Day T close), sell next morning (Day T+1 open)

### OvernightDipBuy Details

Targets stocks that dropped significantly during the day, buying at close and selling at next open. Entry criteria:

- **Dip Score ≥ 0.4** — composite of close-to-close drop, lower-Bollinger-Band penetration, and RSI-oversold proximity (weighted 0.4 / 0.3 / 0.3)
- **Not near resistance** — filters out stocks within 3% of 52-week high, pivot R1/R2, or 20-day high
- **Net return > bank interest** — backtested average overnight return must exceed daily bank interest rate after full commission deduction
- **Minimum daily drop ≥ 1.5%** — close-to-close drop threshold

Output includes `sell_limit_price` so the Toss bridge can immediately place a paired sell order after buy execution. Emotion-free: once bought, the sell limit order is placed and left untouched.

## Commission Model

| Market | Buy Fee | Sell Fee | Sell Tax | Slippage |
|--------|---------|----------|----------|----------|
| Korea (KRX) | 0.015% | 0.015% | 0.18% | 2 bps |
| US (NYSE/NASDAQ) | $0 | $0 | $0 | 2 bps |

## Output Format

`outputs/strategy-cards-{date}.json`:

```json
{
  "strategy_cards": [
    {
      "symbol": "005930",
      "name": "Samsung Electronics",
      "strategy": "Turtle",
      "signal": "BUY",
      "entry_price": 78500,
      "stop_loss": 75200,
      "target_price": 85100,
      "position_size_pct": 0.05,
      "sharpe": 1.42,
      "win_rate": 0.58,
      "total_return": 0.124,
      "max_drawdown": -0.082,
      "score": 7.85,
      "tv_consensus": "agree",
      "risk_assessment": {
        "var_1d_95": -0.023,
        "stress_scenario": "If sector drops 5%: estimated loss -3.8%",
        "correlation_with_portfolio": 0.72,
        "concentration_warning": false
      },
      "execution_guidance": {
        "optimal_window": "09:00-09:30 KST",
        "avoid_period": "14:50-15:30 (closing auction)",
        "min_volume_threshold": 50000,
        "expected_slippage_bps": 3
      }
    },
    {
      "symbol": "000660",
      "name": "SK Hynix",
      "strategy": "OvernightDipBuy",
      "signal": "BUY",
      "entry_price": 185000,
      "stop_loss": 181000,
      "target_price": 188500,
      "sell_limit_price": 188500,
      "position_size_pct": 0.03,
      "sharpe": 0.95,
      "win_rate": 0.62,
      "total_return": 0.034,
      "max_drawdown": -0.028,
      "score": 6.80,
      "dip_score": 0.72,
      "avg_overnight_return": 0.0045,
      "bank_interest_daily": 0.000096,
      "min_profitable_return": 0.0038,
      "timing": {
          "buy_window": "14:30-15:30 KST",
          "sell_window": "09:00-10:00 KST+1",
          "hold_hours": 18
        },
        "risk_assessment": {
          "var_1d_95": -0.018,
          "stress_scenario": "If overnight gap-down 3%: estimated loss -2.1%",
          "correlation_with_portfolio": 0.55,
          "concentration_warning": false
        },
        "execution_guidance": {
          "optimal_window": "14:30-15:20 KST",
          "avoid_period": "15:20-15:30 (closing auction)",
          "min_volume_threshold": 100000,
          "expected_slippage_bps": 5
        }
      }
    ],
  "meta": {
    "date": "2026-04-05",
    "total_evaluated": 112,
    "top_k": 10,
    "backtest_period": "1Y",
    "fee_model": {
      "kr_buy_bps": 1.5,
      "kr_sell_bps": 1.5,
      "kr_sell_tax_bps": 18,
      "us_commission": 0,
      "us_slippage_bps": 2
    }
  }
}
```

## Risk Assessment Fields (AutoHedge P4)

Each strategy card includes a `risk_assessment` object with forward-looking risk metrics:

| Field | Type | Description |
|-------|------|-------------|
| `var_1d_95` | float | 1-day Value-at-Risk at 95% confidence (negative = loss) |
| `stress_scenario` | string | Worst-case narrative for a sector-level shock |
| `correlation_with_portfolio` | float | Correlation with current portfolio holdings (0–1) |
| `concentration_warning` | bool | True if adding this position would exceed 20% sector concentration |

## Execution Guidance Fields (AutoHedge P5)

Each strategy card includes an `execution_guidance` object with timing and liquidity parameters:

| Field | Type | Description |
|-------|------|-------------|
| `optimal_window` | string | Best execution window based on historical volume profile |
| `avoid_period` | string | Time periods with elevated slippage or volatility risk |
| `min_volume_threshold` | int | Minimum daily volume required for clean execution |
| `expected_slippage_bps` | int | Expected slippage in basis points based on historical fills |

## TradingView Cross-Validation

When TradingView backtest data is available (produced by default during the `today` pipeline; skip with `--skip-tradingview`), each strategy card is enriched with a `tv_consensus` field:

- **agree** — TV backtest confirms the signal direction (score bonus +0.5)
- **disagree** — TV backtest contradicts the signal (no bonus)
- **no_data** — no TV data available for this symbol/strategy pair (no bonus)

Cards are re-ranked after applying the consensus bonus. The `tv_consensus` field appears in the output JSON alongside each card.

## Scoring Formula

Composite score (0–10 scale) blending backtested performance with forward-looking risk:

### Backtested Metrics (60% weight)

- **Sharpe Ratio** — higher is better
- **Win Rate** — higher is better
- **Total Return** — net of commissions
- **Risk-Reward Ratio** — (target - entry) / (entry - stop)
- **Drawdown Penalty** — reduces score for deep drawdowns

### Forward-Looking Risk Adjustment (30% weight)

- **VaR Penalty** — deduct points when `var_1d_95` exceeds -3% (higher loss = larger penalty)
- **Correlation Discount** — deduct points when `correlation_with_portfolio` > 0.7 (reduces diversification benefit)
- **Concentration Gate** — hard cap: if `concentration_warning` is true, maximum score capped at 5.0 regardless of other metrics

### Consensus & Execution (10% weight)

- **TV Consensus Bonus** — +0.5 when TradingView backtest agrees (applied post-scoring)
- **Execution Feasibility** — deduct points if `min_volume_threshold` is not met by the stock's average daily volume

## Pipeline Integration

Registered as Phase 5b in `today_pipeline_runner.py`, depends on `screening` and `analysis` stages.

```
Phase 4: Analysis → Phase 5b: Strategy Engine → Phase 5.5: Toss Signal Bridge
```

## Downstream Consumers

1. **DOCX Report** (`generate-report.js`) — "일일 매매 전략 카드 — Top 10" section + dedicated "🌙 Overnight Dip-Buy 전략" sub-section
2. **Markdown Fallback** (`generate_daily_report.py`) — strategy cards table + overnight sub-section
3. **Toss Signal Bridge** (`toss-signal-bridge`) — converts cards to tossctl order previews; OvernightDipBuy cards produce paired buy + sell limit orders
4. **Slack** — thread reply with ranked strategy summary

## CLI Usage

```bash
cd /path/to/project
python scripts/daily_strategy_engine.py              # today's date
python scripts/daily_strategy_engine.py --date 2026-04-05
python scripts/daily_strategy_engine.py --out-dir /tmp/cards
```

## Error Handling

| Error | Action |
|-------|--------|
| No price data for a ticker | Skip ticker, log warning |
| Insufficient history (<60 days) | Skip strategy for that ticker |
| DB connection failure | Fail with clear error message |
| All strategies filtered out | Return empty cards with meta explaining why |

## Examples

```
User: 오늘 전략 카드 생성해줘
Agent: daily-strategy-engine 실행 →
  112개 전략 평가 (7 × 16), 수수료 반영 →
  Top 10 전략 카드:
  1. NVDA — Turtle BUY @ $850.20, SL $815, TP $920, Sharpe 1.8
  2. 005930 — Bollinger I BUY @ ₩78,500, SL ₩75,200, TP ₩85,100, Sharpe 1.4
  3. 000660 — OvernightDipBuy BUY @ ₩185,000 → 매도호가 ₩188,500, Dip 0.72
  ...

User: 전략 카드로 토스 주문 미리보기 만들어줘
Agent: toss-signal-bridge가 strategy-cards-2026-04-05.json을 읽어
  BUY 시그널 7개 → tossctl order preview 생성 (실행 없음)
  OvernightDipBuy 카드 → 매수 + 매도 지정가 주문 2건 페어로 생성

User: 오버나이트 전략만 보여줘
Agent: OvernightDipBuy 카드 필터:
  000660 SK Hynix — 진입 ₩185,000, 매도호가 ₩188,500
  Dip Score 0.72, 평균 수익 0.45%, 은행이자 대비 ✅ 초과
```
