---
name: goose-retention-playbook-builder
description: >-
  Design a customer retention playbook with lifecycle stages, health scores,
  intervention triggers, and playbook actions for each risk tier. Combines
  product usage patterns, engagement signals, and support interactions into a
  systematic retention framework. Pure reasoning skill.
---

# Goose Retention Playbook Builder

Design a customer retention playbook with lifecycle stages, health scores, intervention triggers, and playbook actions for each risk tier. Combines product usage patterns, engagement signals, and support interactions into a systematic retention framework. Pure reasoning skill.

Adapted from [gooseworks-ai/goose-skills](https://github.com/gooseworks-ai/goose-skills) composites/retention-playbook-builder.

## When to Use

- "Build a retention playbook"
- "Design our customer health scoring system"
- "리텐션 플레이북", "고객 유지 전략"
- "Create intervention triggers for at-risk customers"

## Do NOT Use

- For churn signal detection in current data (use goose-churn-risk-detector)
- For expansion/upsell signals (use goose-expansion-signal-spotter)
- For SaaS metrics narrative (use saas-metrics-narrator)

## Methodology

### Phase 1: Lifecycle Stage Definition
Define customer lifecycle with clear boundaries:
- **Onboarding** (Day 0-30): First value realization
- **Adoption** (Day 30-90): Building habits
- **Growth** (Day 90-180): Expanding usage
- **Mature** (Day 180+): Renewal/expansion decisions

### Phase 2: Health Score Design
Composite score from weighted signals:
| Signal | Weight | Red | Yellow | Green |
|--------|--------|-----|--------|-------|
| Login frequency | 25% | <1x/wk | 1-3x/wk | >3x/wk |
| Core feature usage | 30% | <20% features | 20-60% | >60% |
| Support sentiment | 15% | Negative trend | Neutral | Positive |
| Engagement score | 15% | No response | Passive | Active |
| Expansion signals | 15% | None | Interest | Ready |

### Phase 3: Intervention Triggers
For each risk tier (Red/Yellow/Green), define:
- **Trigger condition** (what combination of signals)
- **Response time** (SLA for intervention)
- **Owner** (CSM, product, executive)
- **Playbook action** (specific steps)

### Phase 4: Playbook Actions
Per lifecycle stage × health tier:
- Red + Onboarding → Executive sponsor call within 48h
- Yellow + Adoption → CSM proactive check-in + training offer
- Green + Growth → Expansion play + case study request
- Red + Mature → Retention save play (discount, migration help)

## Output: Retention Playbook with lifecycle stages, health score model, intervention trigger matrix, and specific actions per stage-tier combination
