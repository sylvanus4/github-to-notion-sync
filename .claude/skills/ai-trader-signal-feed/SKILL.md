---
name: ai-trader-signal-feed
description: >-
  Browse and analyze trading signals from the AI-Trader community agent
  marketplace. Includes signal feed, grouped signals by agent, copy trading
  subscriptions, and position tracking. Korean triggers: "AI-Trader 시그널",
  "AI-Trader 커뮤니티 신호", "ai4trade 시그널 피드", "AI-Trader 카피트레이딩", "AI-Trader 포지션".
---

# AI-Trader Signal Feed

Browse and analyze trading signals from the AI-Trader community agent marketplace. Includes signal feed, grouped signals by agent, copy trading subscriptions, and position tracking. Korean triggers: "AI-Trader 시그널", "AI-Trader 커뮤니티 신호", "ai4trade 시그널 피드", "AI-Trader 카피트레이딩", "AI-Trader 포지션".

## When to Use

Use when the user asks to "check AI-Trader signals", "browse trading signals", "ai4trade signal feed", "AI-Trader community signals", "AI-Trader leaderboard", "AI-Trader 시그널", "AI-Trader 시그널 피드", "AI-Trader 커뮤니티 신호", "AI-Trader 카피트레이딩", "AI-Trader 포지션 확인", "ai-trader-signal-feed", "follow a trader on AI-Trader", "AI-Trader copy trade", or needs to consume external trading signals from the ai4trade.ai marketplace.

Do NOT use for market intelligence snapshots (use ai-trader-market-intel). Do NOT use for publishing own signals (use ai-trader-strategy-publisher). Do NOT use for native stock signals (use daily-stock-check). Do NOT use for KIS signal execution (use kis-order-executor). Do NOT use for Toss Securities operations (use tossinvest-trading).

## Prerequisites

- Authenticated with AI-Trader (run ai-trader-setup first)
- `AI_TRADER_AGENT_EMAIL` + `AI_TRADER_AGENT_PASSWORD` or `AI_TRADER_TOKEN` in `.env`

## Workflow

### 1. Fetch Latest Signals

```python
import asyncio
from app.services.ai_trader.client import AITraderClient

async def browse_signals():
    client = AITraderClient()
    try:
        await client.login()
        signals = await client.get_signal_feed(limit=20, sort="new")
        for s in signals:
            print(f"  [{s.action}] {s.symbol} @ ${s.price} by {s.agent_name}")
    finally:
        await client.close()

asyncio.run(browse_signals())
```

### 2. View Signals Grouped by Agent

```python
groups = await client.get_signals_grouped()
for g in groups:
    print(f"\n{g.agent_name} (PnL: {g.total_pnl})")
    for s in g.signals[:3]:
        print(f"  {s.action} {s.symbol} @ ${s.price}")
```

### 3. Copy Trading

Follow a top-performing agent:

```python
await client.follow_leader(leader_id=42)
```

Check current subscriptions:

```python
following = await client.get_following()
for sub in following:
    print(f"  Following: {sub.leader_name} (since {sub.followed_at})")
```

Unfollow:

```python
await client.unfollow_leader(leader_id=42)
```

### 4. View Positions

```python
positions = await client.get_positions()
for p in positions:
    print(f"  {p.side} {p.quantity}x {p.symbol} @ ${p.entry_price} (PnL: {p.pnl})")
```

## Pipeline Integration

This phase runs as `3-signal-feed` in `scripts/ai_trader_pipeline_runner.py`. Output is saved to `outputs/ai-trader/{date}/phase-3-signal-feed.json`.

## Output Schema

```json
{
  "signal_count": 30,
  "signals": [
    {
      "action": "BUY",
      "symbol": "AAPL",
      "price": 185.50,
      "agentName": "AlphaBot",
      "signalType": "realtime"
    }
  ],
  "group_count": 5,
  "groups": [
    {
      "agentName": "AlphaBot",
      "signals": [...],
      "totalPnl": 1234.56
    }
  ]
}
```

## Error Handling

| Operation | Failure | Recovery |
|-----------|---------|----------|
| Login | 401 Unauthorized | Re-run ai-trader-setup to refresh token |
| Signal feed | Empty response | Log "no signals available", continue pipeline |
| Signal feed | 429 Rate Limit | Back off 30s, retry once |
| Grouped signals | Timeout (>15s) | Log warning, return partial data if available |
| Follow leader | 404 Leader not found | Verify leader_id, suggest `get_signal_feed` to browse |
| Follow leader | 409 Already following | Skip, log as already subscribed |
| Positions | 403 Forbidden | Token may be expired; re-login |

## Safety Notes

- AI-Trader uses simulated trading capital; signals are NOT live order recommendations
- Always cross-validate external signals with native analysis (daily-stock-check, trading-technical-analyst)
- Do NOT auto-execute AI-Trader signals on real brokerages without explicit user approval
