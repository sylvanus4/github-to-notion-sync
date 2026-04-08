# AI-Trader Market Intel

Fetch read-only market intelligence snapshots from the AI-Trader platform: market overview, macro signals, ETF flows, grouped news, and per-symbol stock analysis. Korean triggers: "AI-Trader 시장 정보", "AI-Trader 매크로", "AI-Trader ETF", "ai4trade 시장 분석", "AI-Trader 뉴스".

## When to Use

Use when the user asks to "fetch AI-Trader market data", "AI-Trader market intelligence", "ai4trade market overview", "AI-Trader macro signals", "AI-Trader ETF flows", "AI-Trader stock analysis", "AI-Trader 시장 정보", "AI-Trader 매크로 시그널", "AI-Trader ETF 흐름", "ai4trade 시장 분석", "AI-Trader 뉴스", "ai-trader-market-intel", or needs external market intelligence from the ai4trade.ai community.

Do NOT use for signal feed browsing (use ai-trader-signal-feed). Do NOT use for publishing (use ai-trader-strategy-publisher). Do NOT use for setup/auth (use ai-trader-setup). Do NOT use for AlphaEar news (use alphaear-news). Do NOT use for native market environment analysis (use tab-market-environment). Do NOT use for native market breadth (use tab-market-breadth).

## Prerequisites

- AI-Trader client package installed (`backend/app/services/ai_trader/`)
- Network access to ai4trade.ai
- Some endpoints may require authentication; run ai-trader-setup first if `401` errors occur

## Workflow

### 1. Fetch Overview

```python
import asyncio
from app.services.ai_trader.client import AITraderClient

async def fetch_overview():
    client = AITraderClient()
    try:
        overview = await client.get_market_intel_overview()
        print(f"Available: {overview.available}")
        print(f"Last updated: {overview.last_updated}")
        print(f"Sections: {overview.sections}")
        print(f"Summary: {overview.summary}")
    finally:
        await client.close()

asyncio.run(fetch_overview())
```

### 2. Fetch Macro Signals

```python
macro = await client.get_macro_signals()
for sig in macro.signals:
    print(f"  {sig.get('indicator')}: {sig.get('value')} ({sig.get('trend', 'N/A')})")
print(f"Overall trend: {macro.trend}")
```

### 3. Fetch ETF Flows

```python
etf = await client.get_etf_flows()
print(f"Net flow: ${etf.net_flow:,.0f}" if etf.net_flow else "No flow data")
for flow in etf.flows[:5]:
    print(f"  {flow.get('symbol')}: ${flow.get('flow', 0):,.0f}")
```

### 4. Fetch News

```python
news = await client.get_market_intel_news(category="earnings", limit=10)
for item in news:
    print(f"  [{item.category}] {item.title}")
```

### 5. Per-Symbol Analysis

```python
analysis = await client.get_stock_analysis("AAPL")
print(f"Recommendation: {analysis.recommendation}")
```

## Pipeline Integration

This phase runs as `2-market-intel` in `scripts/ai_trader_pipeline_runner.py`. Output is saved to `outputs/ai-trader/{date}/phase-2-market-intel.json`.

## Output Schema

```json
{
  "overview": { "available": true, "sections": [...], "summary": "..." },
  "macro_signals": { "signals": [...], "trend": "bullish" },
  "etf_flows": { "flows": [...], "netFlow": 1234567 },
  "news_count": 20,
  "news": [{ "title": "...", "category": "...", "summary": "..." }]
}
```

## Error Handling

| Endpoint | Failure | Recovery |
|----------|---------|----------|
| Overview | 503 Service Unavailable | Retry once after 5s; if still down, skip and continue pipeline |
| Macro signals | Empty `signals` array | Log warning, proceed with native `tab-market-environment` data |
| ETF flows | Timeout (>10s) | Log warning, mark as unavailable in output JSON |
| News | 429 Rate Limit | Back off 30s, retry once; cap at 50 items per call |
| Stock analysis | 404 Unknown symbol | Skip symbol, log as `"not_found"` in output |
| Any endpoint | Network error | Log error with endpoint name, continue to next endpoint |

## Cross-Reference with Native Data

AI-Trader market intel supplements (does not replace) the project's native sources:
- Compare macro signals with `tab-market-environment` regime classification
- Cross-reference ETF flows with `trading-sector-analyst` rotation data
- Use AI-Trader news alongside `alphaear-news` for broader coverage
