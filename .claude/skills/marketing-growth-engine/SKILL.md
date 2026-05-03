---
name: marketing-growth-engine
description: >-
  Autonomous marketing experiment lifecycle — create, run, measure, optimize
  growth experiments using Karpathy-style auto-experimentation with
  statistical scoring, pacing alerts, and weekly scorecards.
disable-model-invocation: true
---

# Marketing Growth Engine

Autonomous marketing experiment lifecycle manager. Creates, tracks, scores, and optimizes growth experiments using statistical significance testing, pacing alerts, and automated weekly scorecards.

## Triggers

Use when the user asks to:
- "growth experiment", "marketing experiment", "A/B test engine", "experiment engine"
- "weekly scorecard", "pacing alert", "experiment scoring"
- "성장 실험", "마케팅 실험", "A/B 테스트 엔진", "주간 스코어카드"
- "create experiment", "score experiment", "suggest next experiment"

## Do NOT Use

- For daily stock trading experiments or backtesting → use `trading-backtest-expert`
- For PM-level growth strategy and North Star metrics → use `pm-marketing-growth`
- For marketing campaign planning without experiment tracking → use `kwp-marketing-campaign-planning`
- For general A/B test statistical analysis → use `pm-data-analytics`
- For agency-level growth hacking ideation → use `agency-growth-hacker`

## Prerequisites

- Python 3.10+
- `pip install numpy scipy` (for statistical scoring)
- Environment variables (optional): `GROWTH_ENGINE_DATA_DIR`, `PIPELINE_API_URL`, `EMAIL_API_URL`

## Execution Steps

### Step 1: Experiment Creation
Run `scripts/experiment-engine.py create` with experiment parameters (name, hypothesis, metric, variants, sample size).

### Step 2: Data Logging
Log results with `scripts/experiment-engine.py log` — records daily metric observations per variant.

### Step 3: Statistical Scoring
Run `scripts/experiment-engine.py score` — applies Bayesian/frequentist scoring with configurable thresholds (`P_WINNER=0.05`, `LIFT_WIN=0.10`).

### Step 4: Playbook Promotion
Winners are promoted to the playbook with `scripts/experiment-engine.py playbook`. Failed experiments are archived with learnings.

### Step 5: Weekly Scorecard
Run `scripts/autogrowth-weekly-scorecard.py` — generates a digest of all active experiments, winners, and pipeline health.

### Step 6: Pacing Alerts
Run `scripts/pacing-alert.py` — monitors campaign spend/volume pacing and alerts on under/over-delivery.

### Step 7: Next Experiment Suggestion
Run `scripts/experiment-engine.py suggest` — uses historical data to recommend the next highest-impact experiment.

## Workflow

```
Create → Log → Score → Promote/Archive → Weekly Scorecard → Suggest Next
                ↑                                              ↓
                └──────────────── Feedback Loop ───────────────┘
```

## Output

- Experiment database (JSON in `GROWTH_ENGINE_DATA_DIR`)
- Weekly scorecard markdown report
- Pacing alert notifications
- Playbook of winning experiments

## Examples

### Example 1: Create and score an experiment

User: "Create an A/B test for our new landing page CTA"

1. Run `scripts/experiment-engine.py create --name "CTA Test" --hypothesis "Green CTA increases clicks by 15%" --metric click_rate --variants "green,blue"`
2. Log daily observations with `scripts/experiment-engine.py log`
3. Run `scripts/experiment-engine.py score` to check statistical significance

Result: Experiment tracked in JSON database with Bayesian scoring and winner determination.

### Example 2: Weekly digest

User: "Generate this week's experiment scorecard"

1. Run `scripts/autogrowth-weekly-scorecard.py`

Result: Markdown digest of active experiments, winners promoted to playbook, and next suggested experiment.

## Error Handling

| Error | Action |
|-------|--------|
| Missing numpy/scipy | Install: `pip install numpy scipy` |
| No experiments found | Run `create` first to initialize the experiment database |
| Insufficient data for scoring | Wait for more observations (minimum 100 per variant recommended) |
| GROWTH_ENGINE_DATA_DIR not set | Defaults to `./data/experiments/`; set env var for custom location |

## Composed Skills

- `kwp-data-statistical-analysis` for deep statistical methodology
- `kwp-marketing-performance-analytics` for marketing metrics context
- `pm-data-analytics` for cohort and retention analysis
