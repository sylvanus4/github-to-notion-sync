---
name: toss-morning-briefing
version: 1.0.0
description: >-
  Comprehensive morning portfolio briefing combining Toss account data with
  overnight market analysis. Integrates account summary, positions with
  overnight P&L, pending orders, and risk snapshot into a single Korean
  briefing posted to Slack.
  Use when the user asks to "toss morning", "morning portfolio", "아침 포트폴리오",
  "토스 아침 브리핑", "portfolio briefing", "morning toss check",
  or when invoked by the morning-ship pipeline.
  Do NOT use for archival snapshots (use toss-daily-snapshot).
  Do NOT use for risk-only checks (use toss-risk-monitor).
  Do NOT use for live trading (use tossinvest-trading).
triggers:
  - toss morning
  - morning portfolio
  - portfolio briefing
  - morning toss check
  - 아침 포트폴리오
  - 토스 아침 브리핑
  - 토스 모닝
  - 포트폴리오 브리핑
  - 아침 토스 체크
tags: [trading, morning, briefing, toss-securities, portfolio, pipeline]
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "trading"
---

# toss-morning-briefing

Comprehensive morning portfolio briefing combining Toss account state with risk assessment and market context.

## When to Use

- Morning routine — understand portfolio state before market open
- Integrated into `morning-ship` pipeline after Google Workspace phase
- Standalone morning portfolio check

## When NOT to Use

- For archival snapshots → use `toss-daily-snapshot`
- For risk scoring only → use `toss-risk-monitor`
- For read-only queries → use `tossinvest-cli`

## Prerequisites

- `tossctl` installed and in PATH
- Active authenticated session
- Previous day's snapshot for comparison (optional but recommended)

## Workflow

### Step 1: Verify Authentication

```bash
tossctl auth status --output json
```

If session expired, prompt re-authentication and stop.

### Step 2: Gather All Data

Run in sequence:

```bash
tossctl account summary --output json
tossctl portfolio positions --output json
tossctl orders list --output json
```

For top holdings, fetch latest/pre-market prices:

```bash
tossctl quote batch <top-5-symbols> --output json
```

### Step 3: Yesterday Comparison

Load yesterday's snapshot from `outputs/toss/positions-{yesterday}.json` and `outputs/toss/summary-{yesterday}.json`.

Calculate:
- Total asset value change (absolute and %)
- Per-position overnight P&L changes
- New or closed positions

### Step 4: Risk Snapshot

Apply `toss-risk-monitor` logic inline (lightweight version):
- Check single position concentration
- Check buying power utilization
- Flag any RED dimensions

### Step 5: Compose Briefing

Generate a comprehensive Korean morning briefing:

```
☀️ Toss 포트폴리오 모닝 브리핑 (2026-03-24)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 계좌 현황
총 자산: ₩15,234,567 (전일 대비 +₩128,400, +0.85%)
현금 잔고: ₩2,345,678
매수 가능 금액: ₩2,100,000
투자 중: ₩12,888,889

📊 주요 보유 종목 (상위 5)
┌──────────┬────────┬──────────┬──────────┐
│ 종목     │ 수량   │ 현재가   │ 수익률   │
├──────────┼────────┼──────────┼──────────┤
│ AAPL     │ 20주   │ $178.50  │ +12.3%   │
│ NVDA     │ 5주    │ $850.00  │ +25.1%   │
│ 005930   │ 50주   │ ₩78,000  │ -2.1%    │
│ MSFT     │ 8주    │ $420.30  │ +8.7%    │
│ GOOGL    │ 3주    │ $178.20  │ +4.2%    │
└──────────┴────────┴──────────┴──────────┘

📈 어제 대비 주요 변동
- 최대 상승: NVDA +3.2% (+₩128,000)
- 최대 하락: 005930 -1.1% (-₩42,900)

📋 미체결 주문: 2건
- AAPL 매수 5주 @ $175.00 (지정가)
- TSLA 매도 3주 @ $190.00 (지정가)

🛡️ 리스크 상태: 🟢 양호
- 최대 개별 비중: 8.2% (AAPL) — 정상
- 매수 여력: 62% 사용 — 정상
```

### Step 6: Post to Slack

Post the briefing to `#h-daily-stock-check` as a threaded message.

When integrated into `morning-ship`, include as a section of the consolidated morning Slack post in `#효정-할일`.

## Integration Points

- **`morning-ship`**: Called after Google Workspace phase, before stock pipeline
- **`/tossinvest-morning` command**: Standalone execution
- **`toss-daily-snapshot`**: Uses yesterday's snapshot for comparison
- **`toss-risk-monitor`**: Inline risk assessment logic

## Examples

```
User: 토스 모닝 브리핑
Agent: toss-morning-briefing 실행 →
  📊 포트폴리오 현황: $45,230 (전일 대비 +$320, +0.71%)
  ⚠️ 리스크: YELLOW (NVDA 집중도 38%)
  💱 환율: ₩1,385.50/USD (+0.23%)
  📈 전일 체결: SOFI 매수 20주 @ $14.80
  🎯 오늘 주시: PLTR (NEUTRAL 시그널, 미보유)

User: /tossinvest-morning
Agent: (runs the full morning briefing with Slack posting)

User: /morning-ship (with --skip-toss not set)
Agent: Phase 3.3에서 자동으로 toss-morning-briefing 실행
```

## Error Handling

| Error | Action |
|-------|--------|
| `No active session` | Prompt re-auth, skip Toss section in pipeline |
| No previous snapshot | Skip comparison, show current state only |
| Quote fetch failed | Show positions without latest prices |
| Markets closed (weekend) | Show last known state, note "시장 휴장" |
