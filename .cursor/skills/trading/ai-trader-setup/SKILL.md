# AI-Trader Setup

Register, authenticate, and verify connectivity with the AI-Trader platform (ai4trade.ai). Korean triggers: "AI-Trader 설정", "AI-Trader 연결", "AI-Trader 인증", "ai4trade 로그인", "AI-Trader 등록".

## When to Use

Use when the user asks to "set up AI-Trader", "register on ai4trade", "login to AI-Trader", "check AI-Trader connection", "verify AI-Trader auth", "AI-Trader health check", "AI-Trader 설정", "AI-Trader 연결 확인", "AI-Trader 인증", "ai4trade 로그인", "AI-Trader 등록", "AI-Trader 계정 확인", "ai-trader-setup", or needs to configure credentials and verify the platform is reachable.

Do NOT use for fetching market data (use ai-trader-market-intel). Do NOT use for signal browsing (use ai-trader-signal-feed). Do NOT use for publishing strategies (use ai-trader-strategy-publisher). Do NOT use for the full pipeline (use ai-trader-orchestrator). Do NOT use for native brokerage auth (use tossinvest-setup or kis-team).

## Prerequisites

- `AI_TRADER_AGENT_EMAIL` and `AI_TRADER_AGENT_PASSWORD` set in `.env`
- Optional: `AI_TRADER_BASE_URL` (defaults to `https://ai4trade.ai/api`)
- Optional: `AI_TRADER_TOKEN` (skip login if pre-set)
- Python packages: `httpx`, `pydantic` (already in requirements.txt)

## Workflow

### 1. Verify Environment

Check that required environment variables are configured:

```bash
python -c "
from backend.app.services.ai_trader.config import ai_trader_config
print(f'Configured: {ai_trader_config.is_configured}')
print(f'Base URL: {ai_trader_config.base_url}')
print(f'Agent: {ai_trader_config.agent_name}')
print(f'Email: {ai_trader_config.agent_email[:3]}***')
print(f'Has token: {bool(ai_trader_config.token)}')
"
```

### 2. Register (First Time Only)

```python
import asyncio
from app.services.ai_trader.client import AITraderClient

async def register():
    client = AITraderClient()
    try:
        result = await client.register()
        print(f"Registered: {result}")
        print(f"Token: {client._token[:10]}...")
    finally:
        await client.close()

asyncio.run(register())
```

Save the returned token to `AI_TRADER_TOKEN` in `.env` for future sessions.

### 3. Login & Verify

```python
import asyncio
from app.services.ai_trader.client import AITraderClient

async def verify():
    client = AITraderClient()
    try:
        token = await client.login()
        info = await client.get_agent_info()
        print(f"Agent ID: {info.id}")
        print(f"Name: {info.name}")
        print(f"Cash: ${info.cash_balance:,.2f}")
        print(f"Points: {info.points}")
    finally:
        await client.close()

asyncio.run(verify())
```

### 4. Quick Connectivity Test

```bash
python scripts/ai_trader_pipeline_runner.py --dry-run
```

This validates the pipeline structure without making API calls.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Not authenticated` | Missing email/password in .env | Set `AI_TRADER_AGENT_EMAIL` and `AI_TRADER_AGENT_PASSWORD` |
| `401 Unauthorized` | Expired token | Clear `AI_TRADER_TOKEN`, re-login |
| `Connection refused` | Platform unreachable | Check `AI_TRADER_BASE_URL`, verify network |
| `422 Unprocessable` | Bad registration data | Check email format, password requirements |

## Output Schema

```json
{
  "status": "authenticated",
  "agent_id": "abc-123",
  "agent_name": "ThakiAnalytics",
  "cash_balance": 100000.00,
  "token_cached": true,
  "base_url": "https://ai4trade.ai/api"
}
```

When used for connectivity verification only, the output confirms reachability without persisting files.

## Error Handling

| Phase | Failure | Recovery |
|-------|---------|----------|
| Env check | Missing `AI_TRADER_AGENT_EMAIL` | Print setup instructions, abort |
| Register | 409 Conflict (already registered) | Skip to login |
| Register | 422 Unprocessable | Validate email format, password length >= 8 |
| Login | 401 Unauthorized | Clear cached `AI_TRADER_TOKEN`, retry with password |
| Login | Network timeout | Verify `AI_TRADER_BASE_URL`, check DNS/proxy |
| Agent info | 403 Forbidden | Token expired; re-login automatically |
| Dry run | Script not found | Verify `scripts/ai_trader_pipeline_runner.py` exists |
