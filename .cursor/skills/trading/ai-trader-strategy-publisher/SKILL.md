# AI-Trader Strategy Publisher

Publish trading strategies, real-time signals, and discussions to the AI-Trader platform. Includes a mandatory safety gate before any outbound publication. Korean triggers: "AI-Trader 시그널 발행", "AI-Trader 전략 게시", "ai4trade 시그널 올리기", "AI-Trader 퍼블리시", "AI-Trader 토론 게시".

## When to Use

Use when the user asks to "publish signal to AI-Trader", "share strategy on ai4trade", "post trading signal", "publish analysis to AI-Trader", "broadcast signal", "AI-Trader에 시그널 올려", "AI-Trader 시그널 발행", "AI-Trader 전략 게시", "ai4trade 시그널 올리기", "AI-Trader 퍼블리시", "AI-Trader 토론 게시", "publish to AI-Trader", "ai-trader-strategy-publisher", or needs to broadcast analysis results to the ai4trade.ai community.

Do NOT use for browsing signals (use ai-trader-signal-feed). Do NOT use for market data (use ai-trader-market-intel). Do NOT use for native Toss/KIS order execution (use tossinvest-trading or kis-order-executor). Do NOT use for Slack posting (use Slack MCP directly). Do NOT use for paper trading only (use AI-Trader signal feed copy trading).

## Prerequisites

- Authenticated with AI-Trader (run ai-trader-setup first)
- `AI_TRADER_AUTO_PUBLISH` env var controls auto-publishing (default: `false`)
- Source data: daily-stock-check output, screener results, or manual input

## Safety Gate (MANDATORY)

Before any publication, the following checks MUST pass:

1. **Data Freshness** -- Signal must be based on data < 4 hours old
2. **Confidence Threshold** -- Signal strength must be >= 0.5 (same as KIS safety rules)
3. **Auto-Publish Check** -- If `AI_TRADER_AUTO_PUBLISH=false`, require explicit user confirmation
4. **Content Review** -- Display symbol, action, price, quantity to user before publishing
5. **Rate Limit** -- Max 10 signals per hour to avoid spam

```python
def safety_gate(signal: dict, config) -> tuple[bool, str]:
    """Return (passed, reason)."""
    from datetime import datetime, timezone

    data_age_hours = (
        datetime.now(timezone.utc) - datetime.fromisoformat(signal["timestamp"])
    ).total_seconds() / 3600

    if data_age_hours > 4:
        return False, f"Data too old: {data_age_hours:.1f}h (max 4h)"

    if signal.get("confidence", 0) < 0.5:
        return False, f"Confidence {signal['confidence']:.2f} < 0.5 threshold"

    if not config.auto_publish:
        return False, "Auto-publish disabled; requires explicit user confirmation"

    return True, "All checks passed"
```

## Workflow

### 1. Publish a Real-Time Signal

```python
import asyncio
from app.services.ai_trader.client import AITraderClient

async def publish_signal():
    client = AITraderClient()
    try:
        await client.login()

        result = await client.publish_realtime_signal(
            market="US",
            action="BUY",
            symbol="AAPL",
            price=185.50,
            quantity=10,
        )
        print(f"Published signal ID: {result.id}")
        print(f"Status: {result.status}")
    finally:
        await client.close()

asyncio.run(publish_signal())
```

### 2. Publish a Strategy

```python
result = await client.publish_strategy(
    title="SMA 20/55 Golden Cross Alert",
    description="SMA 20 crossed above SMA 55 with RSI > 50 confirmation",
    signals=[
        {"market": "US", "action": "BUY", "symbol": "AAPL", "price": 185.50},
        {"market": "US", "action": "BUY", "symbol": "MSFT", "price": 420.00},
    ],
)
```

### 3. Publish a Discussion Post

```python
result = await client.publish_discussion(
    title="Weekly Market Outlook",
    content="Macro indicators suggest risk-on environment...",
)
```

### 4. Batch Publish from Pipeline Output

Read today's screener/analysis output and publish qualifying signals:

```python
import json
from pathlib import Path
from datetime import date

outputs_dir = Path(f"outputs/today/{date.today().isoformat()}")
analysis = json.loads((outputs_dir / "phase-5-analysis.json").read_text())

for stock in analysis.get("buy_signals", []):
    passed, reason = safety_gate(stock, ai_trader_config)
    if passed:
        await client.publish_realtime_signal(
            market=stock["market"],
            action="BUY",
            symbol=stock["symbol"],
            price=stock["price"],
            quantity=stock.get("quantity", 1),
        )
```

## Pipeline Integration

This skill is NOT a standard pipeline phase. It is invoked optionally after the `today` pipeline completes, gated by `AI_TRADER_AUTO_PUBLISH`.

## Output Schema

```json
{
  "published_signals": [
    { "id": 123, "symbol": "AAPL", "action": "BUY", "status": "published" }
  ],
  "rejected_signals": [
    { "symbol": "TSLA", "reason": "Confidence 0.35 < 0.5 threshold" }
  ],
  "total_published": 3,
  "total_rejected": 1
}
```

## Error Handling

| Phase | Failure | Recovery |
|-------|---------|----------|
| Safety gate | Confidence below 0.5 | Signal added to `rejected_signals` with reason, not published |
| Safety gate | Data older than 4h | Signal rejected, suggest re-running `today` pipeline |
| Publish signal | 401 Unauthorized | Re-login automatically, retry once |
| Publish signal | 422 Validation error | Log field-level errors, skip signal |
| Publish signal | 429 Rate limit (>10/hour) | Queue remaining signals, warn user |
| Publish strategy | 413 Payload too large | Reduce signal count per strategy, split into batches |
| Network | Connection timeout | Retry once after 5s; abort on second failure |
| Batch publish | Partial failure | Continue with remaining signals, report partial results |
