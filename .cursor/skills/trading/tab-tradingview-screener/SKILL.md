---
description: "Cross-check native screener results against TradingView MCP screener (fiale-plus) with 100+ fields and 14 pre-built strategies. Use when cross-checking screener, 'TV screener', 'TradingView 스크리너', 'tab-tradingview-screener'. Do NOT use for native screening only (use tab-screening), TA cross-validation (use tab-tradingview-ta), or Pine Script generation (use pine-script-generator)."
---

# tab-tradingview-screener

## Purpose

Cross-checks the project's native multi-factor screener results against the TradingView MCP screener (fiale-plus/tradingview-mcp-server) to identify stocks that appear in both systems (high agreement) and stocks flagged only by TradingView (potential blind spots).

## When to Use

- cross-check screener results
- TV screener validation
- TradingView 스크리너 비교
- tab-tradingview-screener
- tradingview screener cross-check

## When NOT to Use

- Native screening only — use tab-screening
- TA signal validation — use tab-tradingview-ta
- Pine Script generation — use pine-script-generator
- Stock price sync — use tab-stock-sync

## Workflow

1. Ensure the `tradingview-mcp-server` MCP is available (`npx -y tradingview-mcp-server`)
2. Load the native screener output from `outputs/screener-{date}.json`
3. Call `TradingViewScreenerService.scan()` via the MCP adapter
4. Compare ticker overlap between native and TV results
5. Write cross-check output to `outputs/tv-screener-crosscheck-{date}.json`

## Pipeline Integration

Registered as **tv_screener_crosscheck** in `pipeline_orchestrator.py`:
- **Depends on:** `screening`
- **Retry:** 1
- **Timeout:** 120s
- Gracefully degrades if TradingView MCP is unavailable (returns empty results)

## Service

`backend/app/services/tradingview_mcp_adapter.py` → `TradingViewScreenerService`

## Output

```json
{
  "date": "2026-04-05",
  "native_count": 25,
  "tv_count": 50,
  "overlap": ["AAPL", "NVDA"],
  "tv_only_highlights": ["SMCI", "PLTR"]
}
```

## Dependencies

- `tradingview-mcp-server` npm package (installed via npx)
- Native screener output file
