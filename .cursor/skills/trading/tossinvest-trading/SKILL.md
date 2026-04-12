---
name: tossinvest-trading
version: 1.1.0
description: >-
  Execute trading operations (buy, sell, cancel, amend) on Toss Securities
  via tossctl with mandatory enforcement of the 7-layer Safety Model.
  Every live mutation requires all layers to pass (Layer 0 is Paperclip governance).
  Use when the user asks to "buy stock on toss", "toss sell", "toss order",
  "토스 매수", "토스 매도", "토스 주문", "토스 거래", or needs to place,
  cancel, or amend orders on Toss Securities.
  Do NOT use for read-only queries like portfolio or quotes (use tossinvest-cli).
  Do NOT use for setup, installation, or authentication (use tossinvest-setup).
  Do NOT use for non-Toss brokerage trading (use tab-kiwoom for Kiwoom Securities).
triggers:
  - toss buy
  - toss sell
  - toss place order
  - toss cancel order
  - toss amend order
  - toss trade
  - toss order place
  - toss order cancel
  - toss order amend
  - toss permissions
  - tossinvest trade
  - 토스 매수
  - 토스 매도
  - 토스 주문
  - 토스 주문 취소
  - 토스 주문 정정
  - 토스 거래
tags: [trading, brokerage, live-orders, toss-securities, korean-market, safety-critical]
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "trading"
---

# tossinvest-trading

Execute live trading operations on Toss Securities via tossctl. **Every mutation is gated by the 7-layer Safety Model — no layer may be skipped.**

## When to Use

Use when the user asks to buy stock, sell stock, cancel a pending order, amend an order, or manage trading permissions on Toss Securities.

## When NOT to Use

- For installing or authenticating tossctl → use `tossinvest-setup`
- For read-only queries (account, portfolio, quotes) → use `tossinvest-cli`
- For Kiwoom Securities trading → use `tab-kiwoom`
- For paper trading or backtesting → use `trading-backtest-expert`

## CRITICAL: 7-Layer Safety Model

**ALL 7 LAYERS ARE MANDATORY for every live trading operation. There are no shortcuts.**

```
Layer 0: Paperclip approval gate  → Governance approval for orders above threshold
Layer 1: config.json trading flags → Must explicitly allow the operation type
Layer 2: permissions grant (TTL)  → Time-limited execution window must be active
Layer 3: preview (dry run)        → Always preview first, never skip to execute
Layer 4: --execute flag           → Explicit flag to attempt live mutation
Layer 5: --dangerously-skip-permissions → Explicit risk acknowledgement
Layer 6: --confirm <token>        → Cryptographic confirmation from preview output
```

### Layer 0: Paperclip Governance Gate (Optional but Recommended)

Before proceeding with any live trading operation, check if Paperclip governance is available. If available, create an approval request for orders exceeding the cost threshold.

**Threshold**: Orders with estimated total cost >= KRW 500,000 (or USD equivalent) require Paperclip board approval.

**Step 0a — Check Paperclip availability:**

```
Tool: paperclip_dashboard
Input: { "companyId": "b573bdbe-785a-4f39-b1e9-f2b623e40a92" }
```

If Paperclip is unavailable (connection refused), log "Paperclip unavailable — proceeding with standard 6-layer safety" and skip to Layer 1.

**Step 0b — Create approval request (if above threshold):**

```
Tool: paperclip_create_issue
Input: {
  "companyId": "b573bdbe-785a-4f39-b1e9-f2b623e40a92",
  "title": "Trading approval: {BUY/SELL} {symbol} x {qty} @ {price}",
  "body": "Estimated cost: {total}\nStrategy: {source}\nMarket: {KR/US}\nRisk assessment: {risk_level}",
  "priority": "critical",
  "labels": ["trading-approval", "live-order", "governance-required"]
}
```

**Step 0c — Wait for approval:**

Poll `paperclip_list_approvals` or direct the user to approve via Paperclip UI at `http://127.0.0.1:3100`. Do NOT proceed to Layer 1 until the approval is granted or the user explicitly overrides with "skip-paperclip-approval".

**Step 0d — Log the approval decision:**

```
Tool: paperclip_log_cost
Input: {
  "agentId": "<trading-agent-id>",
  "amountCents": 0,
  "description": "Trading approval {approved/overridden}: {symbol} x {qty}",
  "metadata": { "approval_status": "approved", "override": false }
}
```

**Graceful degradation**: If Paperclip is unavailable, the existing 6-layer safety model remains fully enforced. Layer 0 adds governance tracking, not a replacement for user confirmation.

### Layer 1: Configuration Gate

Before ANY trading command, verify the operation is allowed in `config.json`:

```bash
tossctl config show
```

Required flags per operation:

| Operation | Required Config Fields |
|-----------|----------------------|
| Buy (US) | `trading.place=true`, `allow_live_order_actions=true` |
| Buy (KR) | `trading.place=true`, `trading.kr=true`, `allow_live_order_actions=true` |
| Buy (US fractional) | `trading.place=true`, `trading.fractional=true`, `allow_live_order_actions=true` |
| Sell | `trading.sell=true`, `trading.place=true`, `allow_live_order_actions=true` |
| Cancel | `trading.cancel=true`, `allow_live_order_actions=true` |
| Amend | `trading.amend=true`, `allow_live_order_actions=true` |

**If any required flag is `false`, STOP. Inform the user which flag to enable and do NOT proceed.**

### Layer 2: Permissions Grant

Grant a time-limited execution window:

```bash
tossctl order permissions grant --ttl 5m
```

The `--ttl` (time-to-live) sets how long the execution window stays open. Recommended: `5m` (5 minutes). Maximum: `30m`.

Check current permission status:

```bash
tossctl order permissions status
```

**If permissions have expired or were never granted, STOP. Re-grant before proceeding.**

### Layer 3: Preview (Dry Run)

**ALWAYS preview before executing.** This is the most important safety step.

```bash
# Buy preview
tossctl order place buy AAPL --qty 10 --limit 150.00

# Sell preview
tossctl order place sell AAPL --qty 5 --limit 160.00

# Cancel preview
tossctl order cancel <order-id>

# Amend preview
tossctl order amend <order-id> --qty 8 --limit 155.00
```

Without `--execute`, the command runs in preview mode and outputs:
- Estimated order details (symbol, quantity, price, total cost)
- Fee estimates
- A **confirmation token** for Layer 6

**Present the preview output to the user. Ask for explicit confirmation before proceeding to Layer 4.**

### Layer 4: Execute Flag

Add `--execute` to attempt the live mutation:

```bash
tossctl order place buy AAPL --qty 10 --limit 150.00 --execute
```

This will still be blocked by Layers 5 and 6.

### Layer 5: Risk Acknowledgement

Add `--dangerously-skip-permissions` to acknowledge this is a live trade:

```bash
tossctl order place buy AAPL --qty 10 --limit 150.00 \
  --execute \
  --dangerously-skip-permissions
```

### Layer 6: Confirmation Token

Add `--confirm <token>` using the token from the Layer 3 preview output:

```bash
tossctl order place buy AAPL --qty 10 --limit 150.00 \
  --execute \
  --dangerously-skip-permissions \
  --confirm abc123def456
```

**Only use the exact token from the preview. Never fabricate or reuse tokens.**

## Complete Trading Workflows

### Buy Stock (Full Workflow)

```bash
# 1. Check config
tossctl config show

# 2. Grant permissions
tossctl order permissions grant --ttl 5m

# 3. Preview the order
tossctl order place buy AAPL --qty 10 --limit 150.00

# --- USER CONFIRMS PREVIEW ---

# 4-6. Execute with all safety flags
tossctl order place buy AAPL --qty 10 --limit 150.00 \
  --execute \
  --dangerously-skip-permissions \
  --confirm <TOKEN_FROM_PREVIEW>
```

### Sell Stock (Full Workflow)

```bash
# 1. Check config (trading.sell must be true)
tossctl config show

# 2. Grant permissions
tossctl order permissions grant --ttl 5m

# 3. Preview
tossctl order place sell AAPL --qty 5 --limit 160.00

# --- USER CONFIRMS PREVIEW ---

# 4-6. Execute
tossctl order place sell AAPL --qty 5 --limit 160.00 \
  --execute \
  --dangerously-skip-permissions \
  --confirm <TOKEN_FROM_PREVIEW>
```

### Cancel Order (Full Workflow)

```bash
# 1. List pending orders to find order ID
tossctl orders list --output json

# 2. Check config (trading.cancel must be true)
tossctl config show

# 3. Grant permissions
tossctl order permissions grant --ttl 5m

# 4. Preview cancellation
tossctl order cancel <ORDER_ID>

# --- USER CONFIRMS ---

# 5-6. Execute
tossctl order cancel <ORDER_ID> \
  --execute \
  --dangerously-skip-permissions \
  --confirm <TOKEN_FROM_PREVIEW>
```

### Amend Order (Full Workflow)

```bash
# 1. List pending orders to find order ID
tossctl orders list --output json

# 2. Check config (trading.amend must be true)
tossctl config show

# 3. Grant permissions
tossctl order permissions grant --ttl 5m

# 4. Preview amendment
tossctl order amend <ORDER_ID> --qty 8 --limit 155.00

# --- USER CONFIRMS ---

# 5-6. Execute
tossctl order amend <ORDER_ID> --qty 8 --limit 155.00 \
  --execute \
  --dangerously-skip-permissions \
  --confirm <TOKEN_FROM_PREVIEW>
```

## Order Parameters

### Place (Buy/Sell)

| Flag | Required | Description |
|------|----------|-------------|
| `buy` / `sell` | yes | Order side |
| `<SYMBOL>` | yes | Ticker (US) or KRX code (KR) |
| `--qty <N>` | yes | Number of shares |
| `--limit <PRICE>` | yes (limit orders) | Limit price |
| `--market` | no | Market order (US only, requires `trading.fractional=true`) |

### Cancel

| Flag | Required | Description |
|------|----------|-------------|
| `<ORDER_ID>` | yes | Order ID from `tossctl orders list` |

### Amend

| Flag | Required | Description |
|------|----------|-------------|
| `<ORDER_ID>` | yes | Order ID to amend |
| `--qty <N>` | no | New quantity |
| `--limit <PRICE>` | no | New limit price |

### Permissions

| Flag | Required | Description |
|------|----------|-------------|
| `grant` | — | Sub-command to grant permissions |
| `status` | — | Sub-command to check permission status |
| `--ttl <DURATION>` | yes (grant) | Time-to-live: `5m`, `10m`, `30m` |

## Agent Safety Rules

1. **NEVER skip the preview step.** Always run without `--execute` first.
2. **NEVER fabricate a confirmation token.** Only use the exact token from preview output.
3. **NEVER proceed without explicit user confirmation** after presenting the preview.
4. **NEVER execute if config flags are insufficient** — guide the user to enable them first.
5. **NEVER cache or reuse confirmation tokens** across different orders or sessions.
6. **ALWAYS check permission TTL** before executing — expired permissions must be re-granted.
7. **ALWAYS present the full preview** including estimated cost, fees, and market conditions before asking for user confirmation.
8. **REAL MONEY is at stake.** Treat every trading command as irreversible.

## Examples

### Example 1: Buy stock

User: "토스에서 삼성전자 10주 매수해줘"

Actions:
1. Layer 1 — `tossctl config show` → verify `trading.place = true`
2. Layer 2 — `tossctl order permissions grant --ttl 5m`
3. Layer 3 — `tossctl order place buy --symbol 005930 --qty 10 --order-type market --output json` (preview, no `--execute`)
4. Present preview (종목, 수량, 예상금액, 수수료) + confirmation token to user
5. Ask user: "확인 — 주문 실행" vs "취소 — 주문 중단"
6. If confirmed → Layer 4+5+6 — execute with `--execute --dangerously-skip-permissions --confirm <TOKEN>`
7. Report order ID and status

### Example 2: Cancel order

User: "토스 주문 ORD-12345 취소해줘"

Actions:
1. Layer 1 — `tossctl config show` → verify `trading.cancel = true`
2. Layer 2 — `tossctl order permissions grant --ttl 5m`
3. Layer 3 — `tossctl order cancel ORD-12345 --output json` (preview)
4. Present cancellation preview + confirmation token
5. Ask user for confirmation
6. If confirmed → execute with `--execute --dangerously-skip-permissions --confirm <TOKEN>`

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| `config: trading.place is false` | Config gate blocked | Guide user to enable in config.json |
| `permissions: no active grant` | Layer 2 not satisfied | Run `tossctl order permissions grant --ttl 5m` |
| `permissions: grant expired` | TTL elapsed | Re-grant permissions |
| `confirm: invalid token` | Wrong or expired token | Re-run preview to get a fresh token |
| `insufficient buying power` | Account lacks funds | Inform user, suggest smaller order |
| `market closed` | Trading outside hours | Inform user of market hours |
| `invalid symbol` | Unrecognized ticker | Verify symbol format |
