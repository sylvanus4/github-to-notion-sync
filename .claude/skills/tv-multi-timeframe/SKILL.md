---
name: tv-multi-timeframe
description: >-
  Multi-timeframe technical analysis and candlestick pattern recognition via
  TradingView MCP (`get_multi_timeframe_analysis`, `advanced_candle_pattern`,
  `consecutive_candles_scan`).
---

# TV Multi-Timeframe

Multi-timeframe technical analysis and candlestick pattern recognition via TradingView MCP (`get_multi_timeframe_analysis`, `advanced_candle_pattern`, `consecutive_candles_scan`).

## Triggers

Use when the user asks to "multi-timeframe analysis via TV", "TV MTF", "TradingView candlestick patterns", "multi-timeframe TA", "TV 멀티타임프레임", "TV 캔들스틱 패턴", "다중 시간대 분석", "tv-multi-timeframe", or wants MCP-powered cross-timeframe analysis with candlestick pattern detection.

Do NOT use for native TA computation (use `tab-technical-analysis`). Do NOT use for single-timeframe TA cross-validation (use `tab-tradingview-ta`). Do NOT use for Pine Script generation (use `pine-script-generator`).

## Adapter

`backend/app/services/tradingview_mcp_adapter.py` — `TradingViewTAService` singleton: `ta_service`

## Workflow

### Mode 1: Multi-Timeframe Analysis

1. Call `ta_service.get_multi_timeframe(symbol, exchange)`
2. Analyzes across 5m, 15m, 1h, 4h, 1d, 1W timeframes simultaneously
3. Identifies timeframe alignment (all bullish, mixed, all bearish)
4. Reports trend strength and key levels per timeframe

### Mode 2: Candlestick Pattern Scan

1. Call `ta_service.get_candlestick_patterns(symbol, exchange, timeframe)`
2. Detects advanced patterns: doji, hammer, engulfing, morning/evening star, three soldiers/crows, etc.
3. Reports pattern name, type (bullish/bearish/neutral), reliability score

### Mode 3: Consecutive Candles Scan

1. Call the `consecutive_candles_scan` MCP tool via `_call_mcp_tool`
2. Finds stocks with N consecutive up/down candles for momentum detection
3. Useful for breakout and breakdown screening

### Mode 4: Fibonacci Levels

1. Call `ta_service.get_fibonacci(symbol, exchange, timeframe, period)`
2. Auto-calculated retracement and extension levels
3. Key support/resistance zones based on Fibonacci ratios

## Output Format

Report results in Korean with:
- Timeframe alignment summary (e.g., "3/5 timeframes bullish")
- Candlestick patterns with reliability rating
- Fibonacci levels as a reference table
- Trade setup suggestion based on multi-timeframe confluence
