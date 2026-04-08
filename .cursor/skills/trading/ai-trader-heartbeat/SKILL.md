# AI-Trader Heartbeat

Poll the AI-Trader platform heartbeat endpoint for notifications, pending tasks, copy-trade alerts, and platform announcements. Uses a pull-based polling mechanism. Korean triggers: "AI-Trader 알림 확인", "AI-Trader 하트비트", "AI-Trader 대기 작업", "ai4trade 알림", "AI-Trader 폴링".

## When to Use

Use when the user asks to "check AI-Trader notifications", "poll AI-Trader heartbeat", "AI-Trader alerts", "AI-Trader pending tasks", "AI-Trader 알림 확인", "AI-Trader 하트비트", "AI-Trader 대기 작업", "ai4trade 알림", "AI-Trader 폴링", "ai-trader-heartbeat", "check AI-Trader tasks", or needs to retrieve pending notifications from the ai4trade.ai platform.

Do NOT use for fetching market data (use ai-trader-market-intel). Do NOT use for browsing signals (use ai-trader-signal-feed). Do NOT use for publishing (use ai-trader-strategy-publisher). Do NOT use for setup (use ai-trader-setup). Do NOT use for general webhook listening (this is pull-based, not push).

## Prerequisites

- Authenticated with AI-Trader (run ai-trader-setup first)
- `AI_TRADER_HEARTBEAT_INTERVAL` env var (default: 60 seconds)

## Polling Intervals

| Context | Interval | Notes |
|---------|----------|-------|
| Market hours (9:30-16:00 ET) | 60s | Real-time signal awareness |
| Off-hours | 300s | Reduced load |
| Pipeline phase (one-shot) | Single poll | Used by `ai_trader_pipeline_runner.py` |
| Background daemon (optional) | Configurable | For continuous monitoring |

## Workflow

### 1. Single Poll

```python
import asyncio
from app.services.ai_trader.client import AITraderClient

async def poll_once():
    client = AITraderClient()
    try:
        await client.login()
        hb = await client.heartbeat()

        print(f"Status: {hb.status}")
        print(f"Notifications: {len(hb.notifications)}")
        print(f"Tasks: {len(hb.tasks)}")
        print(f"Server time: {hb.server_time}")

        for n in hb.notifications:
            print(f"  [{n.get('type')}] {n.get('message')}")
        for t in hb.tasks:
            print(f"  Task: {t.get('action')} - {t.get('description')}")
    finally:
        await client.close()

asyncio.run(poll_once())
```

### 2. Continuous Polling (Daemon Mode)

```python
import asyncio
from app.services.ai_trader.client import AITraderClient
from app.services.ai_trader.config import ai_trader_config

async def heartbeat_loop():
    client = AITraderClient()
    try:
        await client.login()
        while True:
            hb = await client.heartbeat()
            if hb.notifications:
                for n in hb.notifications:
                    print(f"[ALERT] {n.get('message')}")
            await asyncio.sleep(ai_trader_config.heartbeat_interval)
    finally:
        await client.close()
```

### 3. Process Tasks

When the heartbeat returns tasks, route them to appropriate handlers:

```python
for task in hb.tasks:
    action = task.get("action", "")
    if action == "copy_trade_fill":
        print(f"Copy trade filled: {task.get('symbol')} {task.get('side')}")
    elif action == "signal_alert":
        print(f"Signal from leader: {task.get('leaderName')}")
    elif action == "platform_announcement":
        print(f"Announcement: {task.get('message')}")
```

## Pipeline Integration

This phase runs as `4-heartbeat` in `scripts/ai_trader_pipeline_runner.py`. Output is saved to `outputs/ai-trader/{date}/phase-4-heartbeat.json`.

## Output Schema

```json
{
  "status": "ok",
  "server_time": "2026-04-08T12:00:00Z",
  "notification_count": 3,
  "notifications": [
    { "type": "copy_trade", "message": "AlphaBot bought AAPL" }
  ],
  "task_count": 1,
  "tasks": [
    { "action": "signal_alert", "symbol": "MSFT", "description": "..." }
  ]
}
```

## Error Handling

| Scenario | Failure | Recovery |
|----------|---------|----------|
| Single poll | 401 Unauthorized | Re-login, retry once |
| Single poll | 503 Service Unavailable | Log warning, skip heartbeat phase |
| Single poll | Network timeout (>10s) | Retry once after 5s |
| Daemon mode | 3 consecutive failures | Exponential backoff (60s → 120s → 300s), alert via log |
| Daemon mode | Token expired mid-loop | Catch 401, re-login, resume polling |
| Task processing | Unknown action type | Log as `unhandled_action`, skip task |
