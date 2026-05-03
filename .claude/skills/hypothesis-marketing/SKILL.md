---
name: hypothesis-marketing
description: >-
  Scientific-method investigation loop adapted for Marketing: Observe campaign
  and channel performance metrics → Hypothesize why advertising or content
  metrics deviate → Experiment with minimal creative or targeting adjustments
  → Conclude with evidence-backed campaign optimization decisions. Persists
  reasoning to INVESTIGATION.md. Use when campaign CTR/ROAS/CAC deviates from
  benchmarks, when A/B tests yield surprising results, when an ad channel
  stops performing, when paid acquisition cost increases without explanation,
  or when the user asks to "diagnose campaign", "hypothesis marketing",
  "marketing experiment design", "why did ad CTR drop", "campaign hypothesis",
  "마케팅 가설 실험", "캠페인 진단", "채널 성과 조사", "CAC 증가 원인". Do NOT use for campaign
  planning without a diagnostic question (use
  kwp-marketing-campaign-planning). Do NOT use for content creation without
  investigation intent (use kwp-marketing-content-creation). Do NOT use for
  brand voice work (use kwp-marketing-brand-voice). Do NOT use for product
  feature adoption diagnosis (use hypothesis-pm). Do NOT use for general SEO
  without a performance hypothesis (use marketing-seo-ops).
---

# Hypothesis-Driven Marketing Investigation

Adapted from the core `hypothesis-investigation` methodology for marketing experiment design and performance diagnosis.

## Iron Laws (Marketing Context)

1. **No creative/targeting changes before hypotheses are listed** — write ≥3 competing explanations
2. **Each experiment tests 1 variable** — headline OR audience OR placement, never multiple at once
3. **All evidence persists to file** — `outputs/investigation/{date}/INVESTIGATION.md` survives context compaction
4. **Two same-direction failures → forced pivot** — if the same creative direction fails twice, switch
5. **Explicit predictions with metric thresholds** — "If H1 is correct, CTR should exceed [X%]"

## Phase 1: Observe (Performance Signals)

1. **Identify the trigger** — which metric dropped? Which channel underperforms? What surprised you?
2. **Collect performance data** — CTR, conversion rate, CAC, ROAS, engagement metrics by channel
3. **Map the funnel** — where exactly do users drop off? Which segments convert?
4. **Working boundary** — which campaigns/channels ARE performing? What audiences DO convert?
5. **Create investigation file** — initialize from `hypothesis-investigation/references/investigation-template.md`

Compose with: `kwp-marketing-performance-analytics`, `kwp-data-data-visualization`, `marketing-growth-engine`

## Phase 2: Hypothesize (Competing Explanations)

Generate **minimum 3** competing explanations:
- "CTR dropped because [creative fatigue / audience saturation / seasonal shift / competitor bid increase]"
- "CAC increased because [channel mix / targeting drift / landing page friction]"
- "Conversion dropped because [messaging mismatch / pricing perception / trust signals]"

Compose with: `kwp-marketing-competitive-analysis`, `marketing-conversion-ops` (CRO audit)

## Phase 3: Experiment (Single-Variable Test)

Test one hypothesis at a time:
1. Change one variable — headline, CTA, audience segment, placement, or landing page element
2. Set a metric threshold — "success means CTR ≥ X% within Y impressions"
3. Run with minimum viable sample size
4. Record actual vs predicted result

Compose with: `marketing-growth-engine` (experiment lifecycle), `kwp-data-statistical-analysis` (significance testing)

### Experiment Guardrails

- Maximum 7 single-variable tests before stepping back to re-observe with fresh data
- If all hypotheses are rejected, return to Phase 1 — the performance model may be wrong
- Always log pivot decisions in INVESTIGATION.md Pivot Log section
- Never test multiple variables in one experiment — isolation is non-negotiable

## Phase 4: Conclude (Optimization Decision)

1. **State the validated finding** — one sentence
2. **Map to action** — creative refresh, audience refinement, channel reallocation, landing page update
3. **Scale the winner** — apply confirmed insight across campaigns
4. **Track compounding effect** — measure next-period impact

Compose with: `kwp-marketing-campaign-planning` (apply insights), `marketing-content-ops` (content scoring)

## Quality Gates

### Observation Quality Gate
Before proceeding to Phase 2, verify:
- [ ] Performance trigger clearly documented (which metric, which channel)
- [ ] Funnel data collected with drop-off points identified
- [ ] Working boundary identified (which campaigns/channels ARE performing)
- [ ] Investigation file created at `outputs/investigation/{date}/`

### Hypothesis Quality Gate
Before proceeding to Phase 3, verify:
- [ ] ≥ 3 hypotheses written in INVESTIGATION.md
- [ ] Each hypothesis tests a single variable
- [ ] Metric threshold defined for each experiment (success = CTR ≥ X%)
- [ ] Predictions written before running experiments

### Conclusion Quality Gate
Before declaring done:
- [ ] Validated finding documented in one sentence
- [ ] Action mapped to specific campaign change (creative, targeting, channel, landing page)
- [ ] Winner scaled across campaigns
- [ ] INVESTIGATION.md fully completed and archived

## Anti-Patterns

| Anti-Pattern | Why It Fails | What To Do Instead |
|---|---|---|
| "Ad fatigue" as default explanation | Lazy diagnosis, often wrong | Check audience overlap, bid changes, and competitive activity first |
| Changing headline + CTA + image together | Can't attribute improvement to any single change | Test one variable per experiment |
| Declaring winner after 100 impressions | Insufficient sample size, noise mistaken for signal | Set minimum sample sizes before running |
| Blaming "the algorithm" without data | Stops investigation at platform black box | Check bid strategy, targeting settings, quality scores |

## Harness Integration

Integrates into `marketing-harness` as a diagnostic mode when campaign metrics deviate from benchmarks.
