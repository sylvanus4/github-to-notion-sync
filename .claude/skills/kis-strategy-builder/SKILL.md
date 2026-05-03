---
name: kis-strategy-builder
description: >-
  Design KIS trading strategies using 10 presets and 83 technical indicators,
  and export them as .kis.yaml files. Covers strategy_builder visual builder,
  indicator selection (RSI/MACD/BB/EMA/ADX etc.), entry/exit condition design
  with DSL operators, risk management configuration, and YAML generation with
  strict numeric-literal-only value constraints. Completed YAML feeds directly
  into backtesting (kis-backtester) or live signal execution
  (kis-order-executor). Use when the user asks to 'create a KIS strategy',
  'design a strategy', 'build a YAML strategy', 'RSI strategy',
  'MACD+Bollinger strategy', 'golden cross strategy', 'strategy builder', 'KIS
  전략 만들어줘', '전략 설계', 'YAML 전략', '지표 조합', '매매 조건 짜줘', '전략 파일'. Do NOT use for
  backtesting (use kis-backtester). Do NOT use for order execution (use
  kis-order-executor). Do NOT use for full pipeline orchestration (use
  kis-team). Do NOT use for Toss Securities strategies (use
  tossinvest-trading). Do NOT use for general stock screening without KIS
  context (use daily-stock-check).
---

# [Step 1] KIS Strategy Design

## Purpose

Design technical-indicator-based trading strategies using the strategy_builder visual builder and export them as `.kis.yaml` files. Completed YAML can be used directly for backtesting (Step 2) or real-time signal generation (Step 3).

## Server Startup (if needed)

```bash
# Backend
cd $CLAUDE_PROJECT_DIR/strategy_builder && uv run uvicorn backend.main:app --reload --port 8000

# Frontend
cd $CLAUDE_PROJECT_DIR/strategy_builder/frontend && pnpm dev
# → http://localhost:3000/builder
```

## Workflow

### 1. Identify Strategy Type

- Choose from 10 presets vs. custom design
- Categories: `trend` / `momentum` / `mean_reversion` / `volatility` / `oscillator`

### 2. Select Indicators

83 technical indicators available:

| Family | Indicators |
|--------|------------|
| Moving Average | SMA, EMA, VWAP |
| Momentum | RSI, MACD, ROC, Returns |
| Volatility | BB, ATR, STD, Volatility, ZScore |
| Oscillator | Stoch, CCI, Williams%R, MFI, IBS |
| Trend | ADX, Disparity |
| Volume | OBV |
| Other | Consecutive, Change, CustomCandle |

### 3. Design Entry/Exit Conditions

**Operators**: `greater_than` / `less_than` / `cross_above` / `cross_below` / `equals` / `not_equal` / `breaks`

> `greater_than_or_equal` / `gte` / `lte` are **NOT supported**.
> Express `>= 50` as `greater_than: 50` (functionally identical for integer RSI).

**Logic**: `AND` / `OR`

**Candlestick patterns** (66 types — see `candlestick.py` `PATTERN_DETECTORS` for full list):
`hammer`, `inverted_hammer`, `doji`, `engulfing`, `harami`,
`morning_star`, `evening_star`, `three_white_soldiers`, `three_black_crows`,
`shooting_star`, `hanging_man`, `piercing`

### 4. Risk Management

`risk` is a top-level key (outside `strategy` block). Both `enabled: true` and `percent` are required.

```yaml
risk:
  stop_loss:
    enabled: true
    percent: 3.0
  take_profit:
    enabled: true
    percent: 8.0
  trailing_stop:
    enabled: true
    percent: 2.0
```

> Placing `risk: {}` or nesting `risk:` inside `strategy` causes backtester runtime errors.

### 5. Confirm Parameters

Before generating YAML, show the user a parameter summary table and get confirmation:

```
| Parameter  | Default | Description        |
|------------|---------|-------------------|
| period     | 14      | RSI period         |
| oversold   | 30      | Buy entry level    |
| overbought | 70      | Sell exit level    |
| stop_loss  | 3.0     | Stop loss %        |

이 값으로 전략을 생성할까요? 변경할 항목이 있으면 말씀해주세요.
```

### 6. Generate YAML

**Critical rule**: The `value` field in conditions must contain **numeric literals only**.
`$param_name` variable references cause backtester validation errors.
Substitute the `params` default values directly into conditions.

```yaml
# ❌ WRONG — backtester validation error
entry:
  conditions:
    - indicator: rsi
      operator: less_than
      value: $rsi_oversold     # ← string fails

# ✅ CORRECT — numeric literal
entry:
  conditions:
    - indicator: rsi
      operator: less_than
      value: 30                # ← actual value
```

Full `.kis.yaml` example:

```yaml
version: "1.0"
metadata:
  name: RSI Oversold Strategy
  description: Enter below RSI 30, exit above RSI 70
  category: momentum
  author: user

strategy:
  id: rsi_oversold
  indicators:
    - id: rsi
      alias: rsi
      params:
        period: 14

  entry:
    conditions:
      - indicator: rsi
        operator: less_than
        value: 30
    logic: AND

  exit:
    conditions:
      - indicator: rsi
        operator: greater_than
        value: 70
    logic: AND

risk:
  stop_loss:
    enabled: true
    percent: 3.0
  take_profit:
    enabled: true
    percent: 8.0
```

### 7. Multi-Output Indicators (MACD Golden Cross)

MACD has three outputs: `value` (MACD line), `signal` (signal line), `histogram`.
Golden/dead cross uses a **single alias** with `output` and `compare_output`.

```yaml
strategy:
  id: macd_rsi_composite
  indicators:
    - id: macd
      alias: macd
      params:
        fast: 12
        slow: 26
        signal: 9
    - id: rsi
      alias: rsi
      params:
        period: 14

  entry:
    logic: AND
    conditions:
      - indicator: macd
        output: value
        operator: cross_above
        compare_to: macd
        compare_output: signal
      - indicator: rsi
        operator: greater_than
        value: 50

  exit:
    logic: OR
    conditions:
      - indicator: macd
        output: value
        operator: cross_below
        compare_to: macd
        compare_output: signal

risk:
  stop_loss:
    enabled: true
    percent: 3.0
  take_profit:
    enabled: true
    percent: 8.0
```

> **Important**: Splitting `macd` into two aliases and comparing via `compare_to` creates two independent Lean MACD instances where crossovers do not work. Always use **single alias + compare_to: same alias + compare_output: signal**.

### 8. Code Preview (optional)

```bash
POST /api/strategies/preview
Body: { "yaml": "<yaml content>" }
```

## 10 Preset Strategies

| ID | Name | Category | Key Indicators |
|----|------|----------|---------------|
| `golden_cross` | Golden Cross | trend | SMA(50), SMA(200) |
| `adx_trend` | ADX Strong Trend | trend | ADX(14) |
| `obv_divergence` | OBV Divergence | volume | OBV |
| `mfi_oversold` | MFI Oversold | oscillator | MFI(14) |
| `vwap_bounce` | VWAP Bounce | trend | VWAP |
| `cci_reversal` | CCI Reversal | oscillator | CCI(20) |
| `williams_reversal` | Williams %R Reversal | oscillator | Williams%R(14) |
| `atr_breakout` | ATR Volatility Breakout | volatility | ATR(14) |
| `disparity_mean_revert` | Disparity Mean Reversion | mean_reversion | Disparity(20) |
| `consecutive_candle` | Consecutive Candle Pattern | momentum | Consecutive(3) |

## Troubleshooting

- Indicator shows NaN → Insufficient data. Need at least `min_period` bars (SMA20 → 20+ days)
- YAML parse error → Check 2-space indentation, verify `$param_name` is not used in `value`
- Preview error → Verify indicator ID matches the `indicator` field in conditions

## Next Steps

- **[Step 2]** `kis-backtester` — Validate the completed YAML with historical data
- **[Step 3]** `kis-order-executor` — Execute signals directly without backtesting
