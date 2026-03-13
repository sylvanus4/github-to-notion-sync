---
description: Define North Star metric and supporting input metrics with business game classification and validation.
argument-hint: "<product/business type> | <current metrics if any>"
---

# PM North Star

Define North Star metric and supporting input metrics with business game classification and 7-criteria validation. References pm-marketing-growth skill, north-star-metric sub-skill. Classify business game (Attention/Transaction/Productivity), validate against 7 criteria, define input and counter-metrics.

## Usage

```
/pm-north-star Define North Star metric for our marketplace platform
/pm-north-star 우리 B2B SaaS의 노스스타 메트릭 정의해줘
```

## Workflow

### Step 1: Load skill and reference

Read the `pm-marketing-growth` skill (`.cursor/skills/pm-marketing-growth/SKILL.md`) and `references/north-star-metric.md`.

### Step 2: Classify business game

Determine the primary business game:

- **Attention** — Ad-supported, engagement-driven (e.g., social, media)
- **Transaction** — Revenue from transactions (e.g., marketplace, e-commerce)
- **Productivity** — Value from output or efficiency (e.g., SaaS, tools)

Document rationale and any hybrid aspects.

### Step 3: Validate North Star candidate

Apply the 7 validation criteria to the proposed North Star:

1. Captures value delivered to customer
2. Reflects product usage, not vanity
3. Actionable by teams
4. Measurable and reportable
5. Leads to revenue or retention
6. Resonates with stakeholders
7. Drives strategic decisions

Score each criterion; flag gaps.

### Step 4: Define input and counter-metrics

- **Input metrics** — 3–5 leading indicators that drive the North Star (e.g., activation rate, feature adoption)
- **Counter-metrics** — Guardrail metrics to avoid gaming (e.g., quality, churn, NPS)
- Map relationships: input → North Star → counter

### Step 5: Output

Deliver structured markdown:

1. Business game classification
2. North Star metric with definition and rationale
3. Validation summary (7 criteria)
4. Input metrics constellation
5. Counter-metrics
6. Measurement and reporting notes

## Notes

- North Star should be a single metric; avoid composite indices.
- Align with company stage: early-stage vs scale may use different metrics.
- Revisit when business model or strategy shifts.
