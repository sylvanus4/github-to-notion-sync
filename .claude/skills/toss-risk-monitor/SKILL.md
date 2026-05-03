---
name: toss-risk-monitor
description: >-
  Real-time risk assessment of the Toss Securities portfolio — concentration
  risk, sector exposure, drawdown alerts, and buying power utilization.
  Generates a GREEN/YELLOW/RED risk scorecard and auto-routes RED alerts to
  #효정-의사결정 via decision-router. Use when the user asks to "check risk",
  "portfolio risk", "concentration check", "토스 리스크", "포트폴리오 위험 점검", "risk
  scorecard", or when invoked by the today pipeline (Phase 5.5) or
  toss-morning-briefing. Do NOT use for live trading (use tossinvest-trading).
  Do NOT use for portfolio reconciliation (use toss-portfolio-recon). Do NOT
  use for trade journaling (use toss-trade-journal).
---

# toss-risk-monitor

Real-time risk assessment of the Toss Securities portfolio with multi-dimensional scorecard and automated alert routing.

## When to Use

- After position changes to assess new risk profile
- As part of the daily pipeline (Phase 5.5)
- When toss-morning-briefing needs a risk snapshot
- Ad-hoc portfolio risk check

## When NOT to Use

- For reconciliation vs pipeline signals → use `toss-portfolio-recon`
- For trade logging → use `toss-trade-journal`
- For placing orders → use `tossinvest-trading`

## Prerequisites

- `tossctl` installed and in PATH
- Active authenticated session

## Risk Dimensions and Thresholds

| Dimension | GREEN | YELLOW | RED |
|-----------|-------|--------|-----|
| Single position weight | < 5% of equity | 5–10% | > 10% |
| Top-3 position concentration | < 30% | 30–50% | > 50% |
| Sector concentration | < 20% per sector | 20–35% | > 35% |
| Daily unrealized loss | < 1% | 1–3% | > 3% |
| Buying power utilization | < 60% | 60–85% | > 85% |
| Total position count | 5–20 | 3–4 or 21–30 | < 3 or > 30 |

## Workflow

### Step 1: Gather Data

```bash
tossctl portfolio positions --output json
tossctl account summary --output json
```

### Step 2: Calculate Metrics

For each position from the positions JSON:
1. **Position weight**: `position_market_value / total_assets * 100`
2. **Sector assignment**: classify by ticker (manual mapping or Toss-provided sector)
3. **Unrealized P&L %**: from positions data
4. **Daily drawdown**: sum of negative P&L positions / total_assets

From account summary:
1. **Buying power utilization**: `(total_assets - buying_power) / total_assets * 100`
2. **Position count**: number of holdings

### Step 3: Score Each Dimension

Apply thresholds from the table above. Each dimension gets GREEN/YELLOW/RED.

### Step 4: Composite Score

- All GREEN → **HEALTHY** (overall GREEN)
- Any YELLOW, no RED → **CAUTION** (overall YELLOW)
- Any RED → **AT RISK** (overall RED)

### Step 5: Report

Present in Korean:

```
🛡️ Toss 포트폴리오 리스크 스코어카드
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
종합 상태: 🟡 주의 (CAUTION)

개별 종목 비중:    🟢 최대 4.2% (AAPL)
상위 3종목 집중:   🟡 38.5%
섹터 집중도:       🟢 최대 18.3% (Tech)
일일 미실현 손실:   🟢 -0.4%
매수 여력 사용률:   🟡 72.3%
보유 종목 수:       🟢 15개

⚠️ 주의 항목:
- 상위 3종목(AAPL, MSFT, NVDA) 비중 38.5% — 분산 권장
- 매수 여력 72.3% 사용 — 추가 매수 신중
```

### Step 6: Auto-Alert on RED

If any dimension is RED, invoke `decision-router` to post to `#효정-의사결정`:

```
🚨 [토스 포트폴리오 리스크 경보]
{RED dimension}: {value} (임계값 초과)
즉시 포지션 조정 필요
```

## Integration

- Called by `toss-morning-briefing` for the risk section
- Called by `today` pipeline Phase 5.5 for the Slack thread
- Standalone via user trigger

## Examples

```
User: 리스크 체크해줘
Agent: toss-risk-monitor 실행 → 종합 등급: YELLOW
  - 집중도: RED (NVDA 42% — 최대 25% 초과)
  - 섹터: GREEN (3개 섹터 분산)
  - 드로다운: YELLOW (포트폴리오 -6.2%, 임계치 -5%)
  - 실현손익: GREEN (+12.4%)
  - 현금비중: GREEN (28%)
  - 베타: YELLOW (가중평균 β=1.35)

User: toss risk
Agent: (runs the full 6-dimension risk scan, presents scorecard)
```

## Error Handling

| Error | Action |
|-------|--------|
| `No active session` | Prompt `tossctl auth login` |
| No positions found | Report as "empty portfolio — no risk" |
| Sector mapping unavailable | Report per-position weights without sector grouping |
