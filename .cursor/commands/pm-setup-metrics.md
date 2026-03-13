---
description: Design a product metrics dashboard with North Star, input metrics, health metrics, and alert thresholds
argument-hint: "<product or feature area>"
---

# Product Metrics Dashboard Design

Design a comprehensive metrics framework — from choosing the right North Star metric to defining alert thresholds that catch problems early.

## Usage
```
/pm-setup-metrics SaaS project management tool
/pm-setup-metrics New checkout flow we just launched
/pm-setup-metrics 제품 지표 대시보드 설계
```

## Workflow

### Step 1: Understand What to Measure
Ask about: product/feature area, stage, business goals/OKRs, existing metrics, analytics tools.

### Step 2: Define Metrics Framework
Read and apply pm-product-discovery skill, invoking **metrics-dashboard** sub-skill.

Define: North Star Metric (validates against 7 criteria), Input Metrics (3-5 levers), Health Metrics (3-5 guardrails), Counter-Metrics (1-2 anti-gaming).

### Step 3: Design Alert Thresholds
For each metric: Green (normal), Yellow (investigate), Red (immediate action), check frequency.

### Step 4: Generate Dashboard Spec
Output: metrics tree, implementation notes, review cadence (daily/weekly/monthly/quarterly). Save as markdown.

### Step 5: Suggest Next Steps
- "Shall I **write SQL queries** to calculate these metrics?"
- "Shall I **draft OKRs** based on this metrics framework?"
- "Shall I **build a cohort analysis** to set realistic baselines?"
