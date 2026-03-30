---
name: toss-fx-monitor
version: 1.0.0
description: >-
  Derive the USD/KRW exchange rate from Toss Securities account summary
  (implied rate from USD cash/positions and KRW equivalents) for cross-market
  position sizing and FX-aware order cost estimation. Logs daily rates to
  outputs/toss/fx-{date}.json and alerts on significant daily moves (> 1%).
  Use when the user asks to "check fx rate", "exchange rate", "환율 확인",
  "달러 환율", "toss fx", "원달러", "usd krw rate", or needs FX data
  for US stock position sizing in KRW.
  Do NOT use for general currency conversion unrelated to trading.
  Do NOT use for stock quotes (use tossinvest-cli).
  Do NOT use for live trading (use tossinvest-trading).
triggers:
  - fx rate
  - exchange rate
  - 환율 확인
  - 달러 환율
  - toss fx
  - 원달러
  - usd krw
  - usd to krw
  - 환율 조회
  - 환율 알림
tags: [trading, fx, exchange-rate, toss-securities, cross-market]
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "trading"
---

# toss-fx-monitor

Derive the USD/KRW exchange rate from Toss Securities account summary (implied rate from USD cash/position KRW equivalents) for cross-market position sizing and FX-aware cost estimation. No dedicated FX API exists — the rate is inferred.

## When to Use

- Checking current USD/KRW rate before US stock orders
- Sizing US positions in KRW equivalent
- Monitoring FX rate trends across days
- FX-aware P&L calculation for US holdings

## When NOT to Use

- For general currency conversion → use WebSearch
- For stock quotes → use `tossinvest-cli`
- For placing orders → use `tossinvest-trading`

## Prerequisites

- `tossctl` installed and in PATH
- Active authenticated session

## Workflow

### Step 1: Extract FX Rate

Primary method — extract from account summary (US positions report KRW equivalent):

```bash
tossctl account summary --output json
```

Parse the response for FX conversion data. The account summary includes USD cash/position values with KRW equivalents, from which the implied FX rate can be derived.

### Step 2: Log Daily Rate

Save to `outputs/toss/fx-{date}.json`:

```json
{
  "date": "2026-03-24",
  "usd_krw": 1385.50,
  "source": "toss-account-derived",
  "timestamp": "2026-03-24T09:30:00+09:00"
}
```

### Step 3: Trend Detection

Load previous day's FX log. Calculate daily change:

```
daily_change_pct = (today_rate - yesterday_rate) / yesterday_rate * 100
```

Alert thresholds:
- `> 0.5%` daily move → **INFO**: Notable FX movement
- `> 1.0%` daily move → **WARNING**: Significant FX volatility
- `> 2.0%` daily move → **ALERT**: Extreme FX movement, review US position sizing

### Step 4: Position Sizing Helper

When user asks to size a US stock position in KRW terms:

```
KRW_cost = USD_price × quantity × usd_krw_rate
```

Present:
```
AAPL @ $178.50 × 10주 = $1,785.00
환율 적용 (₩1,385.50/USD): ₩2,473,217
```

### Step 5: Report

Present in Korean:

```
💱 USD/KRW 환율 (2026-03-24)
━━━━━━━━━━━━━━━━━━━━━━
현재 환율: ₩1,385.50/USD
전일 대비: +₩3.20 (+0.23%)
상태: 정상 범위
```

## Output Files

| File | Content |
|------|---------|
| `outputs/toss/fx-{date}.json` | Daily FX rate log |

## Examples

```
User: 환율 확인해줘
Agent: toss-fx-monitor 실행 → USD/KRW ₩1,385.50 (전일 대비 +0.23%)

User: AAPL 10주 원화로 얼마야?
Agent: AAPL @ $178.50 × 10주 = $1,785.00 → ₩2,473,217 (환율 ₩1,385.50/USD)

User: toss fx rate
Agent: (runs the workflow, presents rate with trend)
```

## Error Handling

| Error | Action |
|-------|--------|
| No USD positions in account | FX rate cannot be derived; inform user |
| `No active session` | Prompt `tossctl auth login` |
| Yesterday's FX data missing | Skip trend detection, show current rate only |
