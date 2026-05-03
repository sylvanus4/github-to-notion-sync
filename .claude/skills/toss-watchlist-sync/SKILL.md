---
name: toss-watchlist-sync
description: >-
  Bidirectional comparison between the pipeline's hot stock discoveries and
  the Toss Securities watchlist. Identifies pipeline hot stocks NOT on Toss
  watchlist and Toss watchlist items NOT tracked by the pipeline. Use when the
  user asks to "sync watchlist", "watchlist sync", "관심종목 동기화", "핫 종목 토스 추가",
  "compare watchlist", or wants to align pipeline discoveries with brokerage
  watchlist. Do NOT use for live trading (use tossinvest-trading). Do NOT use
  for portfolio reconciliation (use toss-portfolio-recon). Do NOT use for
  read-only watchlist viewing (use tossinvest-cli).
---

# toss-watchlist-sync

Compare pipeline hot stock discoveries with Toss Securities watchlist to identify sync gaps.

## When to Use

- After daily pipeline discovers new hot stocks
- Reviewing which pipeline picks are on the Toss watchlist
- Cleaning up stale watchlist entries
- Aligning analysis pipeline tracking with brokerage monitoring

## When NOT to Use

- For read-only watchlist viewing → use `tossinvest-cli`
- For portfolio reconciliation → use `toss-portfolio-recon`
- For live trading → use `tossinvest-trading`

## Prerequisites

- `tossctl` installed and in PATH
- Active authenticated session
- Pipeline outputs available (`outputs/discovery-*.json`, `outputs/screener-*.json`)

## Known Limitation

`tossctl` currently provides **read-only** watchlist access. Adding/removing items programmatically is not supported. This skill identifies the gaps and presents recommendations for the user to act on manually in the Toss app.

## Workflow

### Step 1: Load Pipeline Hot Stocks

Gather from today's (or latest) pipeline outputs:

1. `outputs/discovery-{date}.json` — hot stock discovery results
2. `outputs/screener-{date}.json` — screener results with STRONG_BUY/BUY signals

Extract the set of recommended symbols.

### Step 2: Load Toss Watchlist

```bash
tossctl watchlist list --output json
```

Extract the set of watched symbols.

### Step 3: Comparison

| Category | Description |
|----------|-------------|
| **Pipeline → Toss (missing)** | Hot stocks with BUY/STRONG_BUY NOT on Toss watchlist |
| **Toss → Pipeline (untracked)** | Watchlist items NOT tracked by the analysis pipeline |
| **Overlap** | Items present in both — properly synced |

### Step 4: Recommendations

For each category, present actionable recommendations:

- **Pipeline → Toss**: "Consider adding these to your Toss watchlist for real-time alerts"
- **Toss → Pipeline**: "Consider adding these tickers to the pipeline's tracked symbols for analysis"
- **Overlap**: "Properly synced — no action needed"

### Step 5: Report in Korean

```
🔄 관심종목 동기화 리포트 (2026-03-24)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
파이프라인 추천: 8종목 | 토스 관심: 12종목 | 겹침: 5종목

📌 토스에 추가 권장 (파이프라인 추천, 미등록):
- NVDA (STRONG_BUY, RSI 42)
- 005930 (BUY, SMA 상향돌파)
- AMD (BUY, 볼륨 급증)

❓ 파이프라인 미추적 (토스에만 등록):
- XYZ — 파이프라인에 종목 추가 권장
- ABC — 분석 대상 검토 필요

✅ 동기화 완료: AAPL, MSFT, GOOGL, TSLA, 000660
```

## Examples

```
User: 관심종목 싱크해줘
Agent: toss-watchlist-sync 실행 →
  - 파이프라인 추천 but 관심목록 미등록: PLTR, SOFI, ARM
  - 관심목록에만 있고 파이프라인 미추적: COIN
  - 양쪽 모두 존재: NVDA, AAPL, MSFT

User: toss watchlist sync
Agent: (runs the full comparison, presents sync report)
```

## Error Handling

| Error | Action |
|-------|--------|
| `No active session` | Prompt `tossctl auth login` |
| No pipeline outputs found | Try yesterday's files; warn about stale data |
| Empty watchlist | Report pipeline recommendations only |
