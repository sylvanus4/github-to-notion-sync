---
description: "Cross-validate native TA signals against TradingView MCP TA (atilaahmettaner) for top screened stocks — expanded with Bollinger Band rating, stock decision verdicts, and candlestick pattern cross-validation. Use when validating TA signals, 'TV TA validation', 'TradingView 기술분석 검증', 'tab-tradingview-ta', 'BB rating', 'stock decision', 'candlestick cross-check'. Do NOT use for native TA computation only (use tab-technical-analysis), screener cross-check (use tab-tradingview-screener), Pine Script generation (use pine-script-generator), or multi-timeframe analysis (use tv-multi-timeframe)."
---

# tab-tradingview-ta

## Purpose

Cross-validates the project's native technical analysis signals against TradingView MCP TA data (atilaahmettaner/tradingview-mcp) for top-screened stocks. Produces per-symbol confidence scores (HIGH/MEDIUM/LOW) based on signal agreement ratios across RSI, MACD, trend direction, Bollinger Band signals, BB rating, stock decision verdicts, and candlestick pattern confirmation.

## When to Use

- validate TA signals against TradingView
- TV TA cross-validation
- TradingView 기술분석 검증
- tab-tradingview-ta
- TA signal confidence check
- BB rating cross-check
- stock decision verdict
- candlestick pattern confirmation

## When NOT to Use

- Native TA computation only — use tab-technical-analysis
- Screener cross-check — use tab-tradingview-screener
- Pine Script generation — use pine-script-generator
- Turtle indicators — use tab-turtle-refresh
- Multi-timeframe analysis — use tv-multi-timeframe
- Backtest strategy comparison — use tv-backtest

## Workflow

1. Ensure the `tradingview-mcp` Python MCP server is available
2. Load analysis output from `outputs/analysis-{date}.json`
3. Extract top 15 symbols
4. **Phase A — Core TA** (existing):
   - Call `ta_service.batch_analysis()` via the MCP adapter
   - Run `cross_validate_signals()` comparing native vs TV signals per symbol
5. **Phase B — BB Rating** (new):
   - Call `ta_service.get_bb_rating(symbol)` for each validated symbol
   - Compare TV Bollinger Band rating against native BB method signals
   - Flag conflicts where BB rating disagrees with native position assessment
6. **Phase C — Stock Decision** (new):
   - Call `ta_service.get_stock_decision(symbol)` for top-confidence symbols
   - Get composite BUY/SELL/HOLD verdict from TV covering fundamentals + technicals
   - Cross-check against the pipeline's own screening score
7. **Phase D — Candlestick Patterns** (new):
   - Call `ta_service.get_candlestick_patterns(symbol, exchange, timeframe)` for daily
   - Confirm or contradict directional bias from Phase A
   - Bullish patterns on BUY-rated stocks boost confidence; bearish patterns flag warnings
8. Merge all phases into unified validation report
9. Write enhanced results to `outputs/tv-ta-validation-{date}.json`

## Pipeline Integration

Registered as **tv_ta_validation** in `pipeline_orchestrator.py`:
- **Depends on:** `export_analysis_json`
- **Retry:** 1
- **Timeout:** 180s
- Gracefully degrades if TradingView MCP is unavailable (returns without output)

## Service

`backend/app/services/tradingview_mcp_adapter.py` → `TradingViewTAService` singleton: `ta_service`

### Key Methods

| Method | MCP Tool | Purpose |
|---|---|---|
| `batch_analysis()` | `get_analysis` | Core TA indicators per symbol |
| `get_bb_rating()` | `rating_filter` | Bollinger Band rating filter |
| `get_stock_decision()` | `stock_decision` | Composite BUY/SELL/HOLD verdict |
| `get_candlestick_patterns()` | `advanced_candle_pattern` | Pattern detection with reliability |

## Signal Cross-Validation Logic

### Phase A — Core Indicators

| Indicator | Native Field | TV Field | Agreement Check |
|---|---|---|---|
| RSI | `rsi_14` | `rsi` | Both oversold (<30) or overbought (>70) |
| MACD | `macd_signal` | `macd.signal` | Same sign (bullish/bearish) |
| Trend | `sma_trend` | `moving_averages.summary` | Directionally aligned |
| Bollinger | `bb_position` | `bollinger.position` | Same zone (upper/middle/lower) |

### Phase B — BB Rating

| Check | Logic |
|---|---|
| BB rating vs native BB method | TV `rating_filter` rating aligns with native signal direction |
| Rating strength | Strong/Neutral/Weak mapped to confidence modifier |

### Phase C — Stock Decision

| Check | Logic |
|---|---|
| TV verdict vs pipeline score | BUY aligns with screening BUY signal; SELL aligns with screening SELL |
| Conflict flag | Raised when TV says SELL but pipeline says BUY (or vice versa) |

### Phase D — Candlestick Confirmation

| Check | Logic |
|---|---|
| Pattern direction | Bullish pattern on BUY-rated stock → confidence boost |
| Contradiction | Bearish pattern on BUY-rated stock → warning flag |
| Reliability | Only patterns with reliability > 0.6 considered |

### Overall Confidence

- ≥5 agreements across all phases → HIGH
- 3-4 agreements → MEDIUM
- ≤2 agreements → LOW
- Any Phase C conflict (TV SELL vs pipeline BUY) → capped at MEDIUM regardless

## Output

```json
{
  "date": "2026-04-05",
  "symbols_validated": 12,
  "high_confidence": ["AAPL", "NVDA"],
  "low_confidence": ["XYZ"],
  "validations": [
    {
      "symbol": "AAPL",
      "phase_a": {
        "agreements": ["rsi_zone", "macd_direction", "trend_alignment"],
        "conflicts": ["bb_position"]
      },
      "phase_b": {
        "bb_rating": "STRONG_BUY",
        "native_bb_signal": "BUY",
        "aligned": true
      },
      "phase_c": {
        "tv_verdict": "BUY",
        "pipeline_score": "BUY",
        "aligned": true
      },
      "phase_d": {
        "patterns": ["bullish_engulfing"],
        "confirms_direction": true
      },
      "total_agreements": 6,
      "total_checks": 8,
      "agreement_ratio": 0.75,
      "overall_confidence": "HIGH"
    }
  ]
}
```

## Dependencies

- `tradingview_mcp` Python package (>=0.7.0)
- Native analysis output file (`analysis-{date}.json`)
