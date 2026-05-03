---
name: automation-strategist
description: >-
  Strategic automation planning for the stock analytics pipeline — decide what
  to automate vs keep manual, design human-in-the-loop checkpoints, calculate
  automation ROI, and manage automation risk. Provides decision frameworks for
  "should we automate this?" questions. Use when the user asks to "plan
  automation", "should I automate this", "automation strategy", "human in the
  loop", "automation risk", "what to automate", "자동화 전략", "자동화 판단", "휴먼 인 더
  루프", "자동화 ROI", or wants to make strategic decisions about what to automate
  in the trading pipeline. Do NOT use for building specific pipelines (use
  pipeline-builder). Do NOT use for designing system architecture (use
  system-thinker). Do NOT use for running automated workflows (use
  ai-workflow-integrator). Do NOT use for operational risk assessment (use
  compliance-governance).
---

# Automation Strategist

Strategic automation planning for the stock analytics pipeline. Knowing what to automate is valuable. Knowing what NOT to automate is more valuable.

## Meta-Orchestration

### Prompt router (representative user phrases)

| # | Example prompt | This skill? | Delegation order (numbered) | Output merge strategy | User overrides |
|---|----------------|-------------|------------------------------|------------------------|----------------|
| 1 | AI 리포트 품질을 자동 평가해줘 | No (downstream) | 1) Finish ARIA recommendation → 2) if publishing auto: `ai-quality-evaluator` before Slack | Decision doc + optional quality gate appendix | `GATE_THRESHOLD` |
| 2 | 데일리 파이프라인을 설계해줘 | Partial | 1) ARIA on each stage → 2) `ai-workflow-integrator` or `today` for blueprint | Strategy table + referenced workflow template | Template choice |
| 3 | 이 프로세스를 자동화할지 결정해줘 | Yes | 1) Inventory → 2) Score ARIA → 3) Risk matrix → 4) HITL pattern → 5) ROI → 6) If build: delegate `pipeline-builder` / `ai-workflow-integrator` with ordered handoff | **Single** decision brief: scores + risks + checkpoints + implementation order | Weight overrides for ARIA factors; `REQUIRE_HITL=1` |
| 4 | 시스템 데이터 흐름을 분석해줘 | No | 1) `system-thinker` → 2) feed bottlenecks back into ARIA | Link bottleneck section into risk mitigations | — |
| 5 | 프로젝트 컨텍스트를 업데이트해줘 | No | 1) `context-engineer` | MEMORY / glossary | — |

### Error recovery

| Failure mode | Retry | Fallback | Abort |
|--------------|-------|----------|-------|
| Ambiguous process scope | — | Ask 1–2 clarifying questions | User cannot define process |
| ROI data missing | — | Use ranges + assumptions section | — |
| User rejects automation | — | Document manual path + audit plan | — |

### Output aggregation

Deliver one merged **Automation Strategy** doc: ARIA scores, risk table, HITL diagram choice, ROI, phased plan, explicit **next skill** to invoke for implementation.

## Decision Framework: ARIA (Assess-Risk-Implement-Audit)

### Phase 1: Assess Automation Candidates

For any process the user considers automating, evaluate 5 factors:

| Factor | Question | Score (1-5) |
|--------|----------|-------------|
| **Frequency** | How often does this run? | 1=yearly, 5=hourly |
| **Volume** | How much data/work per run? | 1=single item, 5=hundreds |
| **Consistency** | How rule-based is the logic? | 1=pure judgment, 5=pure rules |
| **Error cost** | What happens if automation is wrong? | 1=catastrophic, 5=trivial |
| **Time saved** | How much human time per run? | 1=seconds, 5=hours |

**Automation Score** = (Frequency + Volume + Consistency + Error_cost + Time_saved) / 5

| Score | Recommendation |
|-------|---------------|
| 4.0 - 5.0 | Automate immediately |
| 3.0 - 3.9 | Automate with monitoring |
| 2.0 - 2.9 | Automate with human-in-the-loop |
| 1.0 - 1.9 | Keep manual |

### Phase 2: Risk Assessment

For candidates scoring 2.0+, evaluate automation risk:

#### Risk Matrix

| | Low Probability | High Probability |
|---|---|---|
| **High Impact** | Monitor closely | Human-in-the-loop required |
| **Low Impact** | Automate freely | Automate with alerts |

#### Risk Categories for This Project

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Data quality** | Yahoo Finance returns bad data | Validate: price within 50% of previous close |
| **Signal false positive** | BUY signal on a crashing stock | Cross-validate with multiple indicators |
| **Report hallucination** | AI invents price targets or news | Quality gate via ai-quality-evaluator |
| **Stale data** | Analysis runs on outdated prices | Freshness check before analysis |
| **API failure** | Yahoo/Slack API down | Retry with backoff, graceful degradation |
| **Cascading error** | Bad data propagates through pipeline | Stage validation, circuit breakers |

### Phase 3: Human-in-the-Loop Design

For processes requiring human oversight, design checkpoints:

#### Checkpoint Patterns

**Pattern A: Review-Before-Publish**
```
AI generates report → Human reviews → Approved? → Publish to Slack
                                     → Rejected? → Fix and regenerate
```

Best for: Daily reports, signal summaries, any public-facing output.

**Pattern B: Alert-on-Anomaly**
```
Automated pipeline runs → Anomaly detected? → Alert human
                        → Normal?           → Continue silently
```

Best for: Data sync, routine analysis, background pipelines.

Anomaly triggers for this project:
- Price change > 15% in one day
- Signal flip (BUY to SELL in 1 day)
- More than 30% of stocks showing same signal
- Data gap > 3 trading days
- Report quality score < 6.0

**Pattern C: Escalation Ladder**
```
Level 1: Fully automated (data sync, CSV import)
Level 2: Auto with alert (analysis, signal generation)
Level 3: Auto draft + human approval (report, Slack posting)
Level 4: Human only (strategy changes, ticker list updates)
```

**Pattern D: Confidence-Gated**
```
AI generates with confidence score → High confidence? → Auto-publish
                                   → Medium?         → Flag for review
                                   → Low?            → Require approval
```

### Phase 4: Automation Audit

Periodically review automated processes:

#### Audit Checklist

| Check | Frequency | Method |
|-------|-----------|--------|
| Accuracy of automated signals | Weekly | Compare signals vs actual price moves |
| False positive rate | Weekly | Count wrong BUY/SELL signals |
| Pipeline reliability | Daily | Check GitHub Actions run history |
| Data freshness | Daily | Run `weekly_stock_update.py --status` |
| Report quality trend | Weekly | Run ai-quality-evaluator on last 5 reports |
| Cost efficiency | Monthly | Compute time saved vs maintenance time |

#### ROI Calculation

```
Monthly ROI = (Time saved per run × Runs per month) - Maintenance hours
```

| Process | Manual Time | Automated Time | Monthly Runs | Monthly Savings |
|---------|-------------|----------------|--------------|-----------------|
| Data sync | 30 min | 2 min | 22 | 10.3 hours |
| Analysis | 45 min | 5 min | 22 | 14.7 hours |
| Report generation | 60 min | 10 min | 22 | 18.3 hours |
| Hot stock discovery | 20 min | 3 min | 22 | 6.2 hours |
| **Total** | | | | **49.5 hours/month** |

Maintenance cost estimate: 2-4 hours/month for pipeline fixes and updates.

## Workflow

### Step 1: Inventory Current Processes

List all processes in the stock analytics pipeline with their current automation status:

| Process | Current State | Trigger | Human Time |
|---------|--------------|---------|------------|
| Data sync | Semi-auto (cron + manual) | Daily cron | 5 min monitoring |
| CSV import | Manual | On download | 10 min |
| Technical analysis | Automated | Pipeline | 0 min |
| Hot stock discovery | Automated | Pipeline | 0 min |
| News fetch | Semi-auto | Pipeline | 5 min review |
| Sentiment scoring | Automated | Pipeline | 0 min |
| Report generation | Semi-auto | Pipeline | 15 min review |
| Slack posting | Manual trigger | Human | 2 min |
| Ticker list updates | Manual | Ad hoc | 30 min research |

### Step 2: Score Each Process

Apply the ARIA assessment to each process. Present results in a priority matrix.

### Step 3: Design Automation Plan

For each process to automate or improve:

1. **Current state**: How it works today
2. **Target state**: How it should work
3. **Gap**: What needs to change
4. **Implementation**: Specific changes (script, cron, checkpoint)
5. **Risk mitigation**: Safeguards to add
6. **Rollback plan**: How to revert if automation fails

### Step 4: Recommend Implementation Order

Order by: highest ROI first, lowest risk first, dependencies respected.

```
Phase 1 (Week 1): Automate data sync end-to-end with anomaly alerts
Phase 2 (Week 2): Add quality gate to report pipeline
Phase 3 (Week 3): Automate Slack posting with confidence gate
Phase 4 (Week 4): Add signal accuracy feedback loop
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| ARIA score is ambiguous (2.5-3.0) | Edge case between manual and auto | Default to human-in-the-loop; re-evaluate after 1 month |
| Automated pipeline keeps failing | Insufficient error handling | Add retry logic and anomaly alerts before re-enabling |
| Human checkpoint becomes bottleneck | Too many items require approval | Raise confidence threshold or batch approvals |
| ROI negative after automation | Maintenance cost exceeds time saved | Simplify the automation or revert to manual |
| Cascading failures | No circuit breakers | Add stage validation and independent failure handling |

## Anti-Patterns

Things that should NOT be automated:

| Anti-Pattern | Why |
|-------------|-----|
| Changing the tracked ticker list | Requires strategic judgment about portfolio composition |
| Overriding signals manually | Creates inconsistency between analysis and action |
| Publishing without any review | Financial content requires human accountability |
| Ignoring failed pipeline runs | Failures signal data quality issues |
| Automating one-off tasks | Setup cost exceeds benefit |

## Examples

### Example 1: Should we automate Slack posting?

User says: "Should I automate posting reports to Slack?"

Actions:
1. Score: Frequency=5, Volume=3, Consistency=4, Error_cost=3, Time_saved=2 → 3.4
2. Recommendation: Automate with monitoring
3. Design: Review-Before-Publish pattern with quality gate
4. Implementation: Auto-generate → ai-quality-evaluator → score > 8.0 → auto-post; else → human review

### Example 2: Full automation audit

User says: "Audit our current automation and suggest improvements"

Actions:
1. Inventory all processes
2. Score each with ARIA
3. Identify under-automated (manual but should be auto) and over-automated (auto but risky)
4. Generate improvement plan with ROI estimates

### Example 3: Design human-in-the-loop for new feature

User says: "We want to add automatic position sizing -- how should we design it?"

Actions:
1. Score: Frequency=5, Volume=3, Consistency=2, Error_cost=1, Time_saved=3 → 2.8
2. Recommendation: Automate with human-in-the-loop (error cost is high)
3. Design: Confidence-Gated pattern
4. Checkpoints: AI suggests size → Human confirms → Execute
5. Escalation: Flag if position > 10% of portfolio

## Integration

- **Quality gate**: `ai-quality-evaluator` (validates AI outputs before publish)
- **Pipeline building**: `pipeline-builder` (implements automation decisions)
- **System design**: `system-thinker` (designs the systems to automate)
- **Risk assessment**: `compliance-governance`, `security-expert`
- **Monitoring**: `sre-devops-expert` (operational monitoring)
- **GitHub Actions**: `.github/workflows/` (automation runtime)
