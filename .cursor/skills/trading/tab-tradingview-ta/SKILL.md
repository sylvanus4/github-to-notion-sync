---
description: "Cross-validate native TA signals against TradingView MCP TA (atilaahmettaner) for top screened stocks. Use when validating TA signals, 'TV TA validation', 'TradingView 기술분석 검증', 'tab-tradingview-ta'. Do NOT use for native TA computation only (use tab-technical-analysis), screener cross-check (use tab-tradingview-screener), or Pine Script generation (use pine-script-generator)."
---

# tab-tradingview-ta

## Purpose

Cross-validates the project's native technical analysis signals against TradingView MCP TA data (atilaahmettaner/tradingview-mcp) for top-screened stocks. Produces per-symbol confidence scores (HIGH/MEDIUM/LOW) based on signal agreement ratios across RSI, MACD, trend direction, and Bollinger Band signals.

## When to Use

- validate TA signals against TradingView
- TV TA cross-validation
- TradingView 기술분석 검증
- tab-tradingview-ta
- TA signal confidence check

## When NOT to Use

- Native TA computation only — use tab-technical-analysis
- Screener cross-check — use tab-tradingview-screener
- Pine Script generation — use pine-script-generator
- Turtle indicators — use tab-turtle-refresh

## Workflow

1. Ensure the `tradingview-mcp` Python MCP server is available (`python -m tradingview_mcp`)
2. Load analysis output from `outputs/analysis-{date}.json`
3. Extract top 15 symbols
4. Call `TradingViewTAService.batch_analysis()` via the MCP adapter
5. Run `cross_validate_signals()` comparing native vs TV signals per symbol
6. Write validation results to `outputs/tv-ta-validation-{date}.json`

## Pipeline Integration

Registered as **tv_ta_validation** in `pipeline_orchestrator.py`:
- **Depends on:** `export_analysis_json`
- **Retry:** 1
- **Timeout:** 180s
- Gracefully degrades if TradingView MCP is unavailable (returns without output)

## Service

`backend/app/services/tradingview_mcp_adapter.py` → `TradingViewTAService`, `cross_validate_signals()`

## Signal Cross-Validation Logic

| Indicator | Native Field | TV Field | Agreement Check |
|-----------|-------------|----------|----------------|
| RSI | `rsi_14` | `rsi` | Both oversold (<30) or overbought (>70) |
| MACD | `macd_signal` | `macd.signal` | Same sign (bullish/bearish) |
| Trend | `sma_trend` | `moving_averages.summary` | Directionally aligned |
| Bollinger | `bb_position` | `bollinger.position` | Same zone (upper/middle/lower) |

Confidence mapping: ≥3 agreements → HIGH, 2 → MEDIUM, ≤1 → LOW

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
      "agreements": ["rsi_zone", "macd_direction", "trend_alignment"],
      "conflicts": ["bb_position"],
      "agreement_ratio": 0.75,
      "overall_confidence": "HIGH"
    }
  ]
}
```

## Dependencies

- `tradingview_mcp` Python package
- Native analysis output file (`analysis-{date}.json`)
