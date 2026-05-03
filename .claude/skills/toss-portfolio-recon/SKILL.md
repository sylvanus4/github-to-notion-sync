---
name: toss-portfolio-recon
description: >-
  Compare the project's analysis pipeline signals (screener/analysis outputs)
  against actual Toss Securities holdings to detect drift: unknown positions,
  missed opportunities, signal mismatches, and allocation drift. Use when the
  user asks to "reconcile portfolio", "check drift", "portfolio recon", "포트폴리오
  대조", "보유 종목 비교", "toss recon", "signal vs holdings", or when invoked by
  /tossinvest-recon command. Do NOT use for risk scoring (use
  toss-risk-monitor). Do NOT use for trade journal (use toss-trade-journal).
  Do NOT use for live trading (use tossinvest-trading).
---

# toss-portfolio-recon

Compare analysis pipeline signals against actual Toss Securities holdings to detect portfolio drift.

## When to Use

- After daily pipeline run to validate alignment
- Periodic portfolio health check
- Before major rebalancing decisions
- When user suspects pipeline signals diverge from actual holdings

## When NOT to Use

- For risk scoring → use `toss-risk-monitor`
- For trade execution → use `tossinvest-trading`
- For archival snapshots → use `toss-daily-snapshot`

## Prerequisites

- `tossctl` installed and in PATH
- Active authenticated session
- Today's pipeline outputs exist (`outputs/screener-*.json`, `outputs/analysis-*.json`)

## Workflow

### Step 1: Gather Actual Holdings

```bash
tossctl portfolio positions --output json
```

Parse into a set of held symbols with quantities and current values.

### Step 2: Load Pipeline Signals

Load the latest files:
- `outputs/screener-{date}.json` — screener results with composite signals

Extract symbol + signal for each. The screener uses three signal values:
- **NEUTRAL** (composite_score ≥ 40): favorable technical setup
- **CAUTION** (score 15–39): mixed or weak technicals
- **AVOID** (score < 15): unfavorable setup, consider exiting

### Step 3: Reconciliation Analysis

Compare the two datasets to produce four categories:

#### A. In Toss but NOT in Pipeline
Positions held in the Toss account that the pipeline does not track or analyze. These are "unknown" to the analysis system.

#### B. In Pipeline (NEUTRAL signal) but NOT in Toss
Stocks the pipeline rates NEUTRAL (favorable) that the user does not hold. These are potential opportunities or intentionally skipped.

#### C. Signal Mismatch
Stocks held in Toss where the pipeline's current signal conflicts:
- Holding a stock with **AVOID** signal (unfavorable setup — review needed)
- Holding a stock with **CAUTION** signal but position size is disproportionately large

#### D. Allocation Drift
For stocks present in both, compare actual portfolio weight vs the equal-weight or pipeline-implied target weight. Flag positions where actual weight deviates by > 50% from target.

### Step 4: Output Report

Save to `outputs/toss/recon-{date}.json`:

```json
{
  "date": "2026-03-24",
  "toss_positions": 15,
  "pipeline_tracked": 42,
  "overlap": 10,
  "unknown_in_toss": ["XYZ", "ABC"],
  "neutral_not_held": ["NVDA", "005930"],
  "signal_mismatches": [
    {"symbol": "TSLA", "held": true, "signal": "AVOID", "pnl_pct": -8.2}
  ],
  "allocation_drift": [
    {"symbol": "AAPL", "actual_weight": 12.3, "target_weight": 5.0, "drift_pct": 146}
  ]
}
```

### Step 5: Present in Korean

```
🔍 Toss ↔ Pipeline 포트폴리오 대조 (2026-03-24)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
토스 보유: 15종목 | 파이프라인 추적: 42종목 | 겹침: 10종목

🔴 시그널 충돌 (즉시 검토 필요):
- TSLA: 보유 중 but 파이프라인 AVOID (손익 -8.2%)

🟡 미추적 보유 종목:
- XYZ, ABC (파이프라인에서 분석하지 않는 종목)

🟡 미보유 NEUTRAL 시그널:
- NVDA (NEUTRAL, score 48), 005930 (NEUTRAL, score 44)

🟡 비중 드리프트:
- AAPL: 실제 12.3% vs 목표 5.0% (2.5배 초과)
```

### Step 6: Decision Routing

If any **signal mismatches** exist (holding AVOID-signal stocks), optionally invoke `decision-router` to post to `#효정-의사결정`.

## Examples

```
User: 포트폴리오 리콘 돌려줘
Agent: toss-portfolio-recon 실행 →
  A. Toss에만 있는 종목: MSFT (파이프라인 미추적)
  B. NEUTRAL 시그널이지만 미보유: PLTR, SOFI
  C. 시그널 불일치: TSLA 보유 중 → 파이프라인 AVOID ⚠️

User: /tossinvest-recon
Agent: (runs full reconciliation pipeline with Slack posting)

User: pipeline vs toss
Agent: (runs the recon, presents drift analysis)
```

## Error Handling

| Error | Action |
|-------|--------|
| `No active session` | Prompt `tossctl auth login` |
| No pipeline outputs for today | Try yesterday's files; warn about stale data |
| No positions in Toss | Report as "empty portfolio — nothing to reconcile" |
