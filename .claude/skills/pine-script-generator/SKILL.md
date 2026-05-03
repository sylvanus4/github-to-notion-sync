---
name: pine-script-generator
description: >-
  Generate Pine Script v5 code for technical indicators from the project's
  native Python implementations. Supports SMA, EMA, RSI, MACD, Bollinger
  Bands, Donchian Channel, ADX, Stochastic, Williams %R, CCI, Ultimate
  Oscillator, ROC, ATR, and composite overlays. Use when generating Pine
  Script, 'Pine Script 생성', 'pine-script-generator', 'create TradingView
  indicator'. Do NOT use for native TA computation (use
  tab-technical-analysis), TA cross-validation (use tab-tradingview-ta), or
  screener cross-check (use tab-tradingview-screener).
---

# pine-script-generator

## Purpose

Translates the project's native Python technical indicator implementations into Pine Script v5 code ready to import into TradingView. Supports individual indicator scripts and composite multi-indicator overlays. Generated scripts include proper Pine Script annotations, input parameters, plot definitions, and signal markers.

## When to Use

- generate Pine Script from native indicators
- create TradingView custom indicator
- Pine Script 생성
- pine-script-generator
- export indicators to TradingView
- convert Python TA to Pine Script

## When NOT to Use

- Native TA computation — use tab-technical-analysis
- TA cross-validation — use tab-tradingview-ta
- Screener cross-check — use tab-tradingview-screener
- KIS strategy YAML generation — use kis-strategy-builder

## Supported Indicators

### Overlay Indicators (on price chart)

| Indicator | Pine Script Function | Parameters |
|-----------|---------------------|------------|
| SMA | `ta.sma()` | periods (default: [20, 55, 200]) |
| EMA | `ta.ema()` | periods (default: [12, 26]) |
| Bollinger Bands | `ta.bb()` | period (20), std_dev (2.0) |
| Donchian Channel | `ta.highest()` / `ta.lowest()` | period (20) |

### Separate-Pane Indicators

| Indicator | Pine Script Function | Parameters |
|-----------|---------------------|------------|
| RSI | `ta.rsi()` | period (14) |
| MACD | `ta.macd()` | fast (12), slow (26), signal (9) |
| Stochastic | `ta.stoch()` | k_period (14), d_period (3), smooth (3) |
| ADX | `ta.dmi()` | period (14), adx_smoothing (14) |
| Williams %R | `ta.wpr()` | period (14) |
| CCI | `ta.cci()` | period (20) |
| ROC | `ta.roc()` | period (12) |
| ATR | `ta.atr()` | period (14) |
| Ultimate Oscillator | Custom formula | p1 (7), p2 (14), p3 (28) |

## Workflow

1. Import indicator templates from `backend/app/services/pine_script_generator.py`
2. Call `generate_pine_script(indicator_name, symbol, **params)` for individual scripts
3. Call `generate_composite_script(indicator_list, symbol, params_map)` for multi-overlay scripts
4. Output files saved to `outputs/pine-scripts/{SYMBOL}-{indicator}-{date}.pine`

## Pipeline Integration

Registered as **pine_script_generation** in `pipeline_orchestrator.py`:
- **Depends on:** `export_analysis_json`
- **Retry:** 1
- **Timeout:** 120s
- Runs locally (no external MCP dependency)
- Generates scripts for top 5 screened symbols

## Service

`backend/app/services/pine_script_generator.py`

Key functions:
- `generate_pine_script(indicator, symbol, **params)` → single indicator script
- `generate_composite_script(indicators, symbol, params_map)` → multi-indicator overlay

## Output Structure

```
outputs/pine-scripts/
├── AAPL-overlay-2026-04-05.pine      # SMA + EMA + BB + Donchian composite
├── AAPL-rsi-2026-04-05.pine          # RSI standalone
├── AAPL-macd-2026-04-05.pine         # MACD standalone
├── AAPL-adx-2026-04-05.pine          # ADX standalone
├── AAPL-stochastic-2026-04-05.pine   # Stochastic standalone
├── NVDA-overlay-2026-04-05.pine
├── ...
└── manifest-2026-04-05.json          # Generation manifest
```

## Dependencies

- No external dependencies (pure Python code generation)
- `backend/app/services/pine_script_generator.py`
