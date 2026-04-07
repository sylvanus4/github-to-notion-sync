---
description: "Answer with numbers, data, KPIs, and measurable evidence — minimize qualitative statements"
argument-hint: "<topic to analyze quantitatively>"
---

# Quantitative Metrics Mode

Numbers-first mode. Every claim must be backed by a metric, a benchmark, or a quantified estimate. Minimize adjectives, maximize data.

## Usage

```
/metrics-mode How effective is our CI/CD pipeline?
/metrics-mode Compare the cost of self-hosted vs managed Kubernetes
/metrics-mode What's the ROI of investing in developer experience?
/metrics-mode 자동매매 시스템의 성과를 정량적으로 평가
/metrics-mode How healthy is our codebase?
```

## Your Task

User input: $ARGUMENTS

### Workflow

1. **Identify measurable dimensions** — What can be counted, timed, sized, or rated?
2. **Research/estimate concrete numbers** — Use known benchmarks, industry data, or reasoned estimates
3. **Present as metrics table** with:
   - Metric name
   - Unit of measurement
   - Current value (or estimate)
   - Industry baseline / benchmark
   - Target / recommended value
4. **Include data sources** — Where each number comes from
5. **Flag confidence levels:**
   - ✅ Verified — from authoritative sources or measured data
   - 🔶 Estimated — reasoned estimate with stated assumptions
   - ❓ Unknown — data not available; suggest how to measure

### Output Format

```
## Quantitative Analysis: [Topic]

| Metric | Value | Unit | Baseline | Target | Confidence |
|--------|-------|------|----------|--------|------------|
| [Metric 1] | [X] | [unit] | [Y] | [Z] | ✅/🔶/❓ |
| [Metric 2] | ... | ... | ... | ... | ... |

### Key Findings
- [Finding backed by specific numbers]
- [Finding backed by specific numbers]

### Data Gaps
- [What we can't measure yet and how to fix it]
```

### Constraints

- Every claim must include a number — "performance improved" → "p95 latency dropped from 450ms to 120ms"
- No superlatives without data — "significantly better" is banned; "3.2x faster" is required
- Estimates must state their assumptions explicitly
- If no data exists, say so and suggest a measurement approach — don't fabricate numbers

### Execution

Reference `kwp-data-statistical-analysis` (`.cursor/skills/kwp/kwp-data-statistical-analysis/SKILL.md`) for statistical methods. Reference `pm-data-analytics` (`.cursor/skills/pm/pm-data-analytics/SKILL.md`) for KPI and metrics frameworks.
