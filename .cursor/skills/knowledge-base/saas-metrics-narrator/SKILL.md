---
name: saas-metrics-narrator
description: >-
  Generate SaaS financial narratives from KB wiki data: MRR waterfall decomposition,
  Rule of 40 analysis, cohort retention tables, unit economics breakdown, and
  board-ready metric summaries. Reads finance-policies, product-strategy, and
  sales-playbook wikis to extract revenue signals, cost data, and growth metrics,
  then produces structured Korean narrative reports suitable for board decks,
  investor updates, and internal reviews.
  Includes mandatory "opposite-direction" risk section (Karpathy Protocol) that
  argues the bear case for each metric before presenting conclusions.
  Use when the user asks to "generate SaaS metrics narrative", "MRR waterfall",
  "Rule of 40", "cohort analysis from KB", "board metrics report",
  "SaaS 지표 서사", "MRR 워터폴", "40의 법칙", "코호트 리텐션", "보드 리포트",
  "SaaS 재무 서사", "saas-metrics-narrator", "unit economics narrative",
  "investor metrics update", "재무 서사 생성", "SaaS 성장 분석",
  or wants financial storytelling derived from KB knowledge base data.
  Do NOT use for general financial statement generation (use kwp-finance-financial-statements).
  Do NOT use for variance analysis without SaaS narrative (use kwp-finance-variance-analysis).
  Do NOT use for stock market financial analysis (use trading-us-stock-analysis).
  Do NOT use for general KB querying without financial narrative (use kb-query).
user_invocable: true
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "knowledge-base"
  tags: ["saas", "metrics", "finance", "mrr", "cohort", "board", "narrative", "kb-domain"]
---

# SaaS Metrics Narrator

Generate board-ready SaaS financial narratives from KB wiki data with
evidence-backed metrics, risk analysis, and visual storytelling.

## When to Use

- Generating MRR waterfall decomposition from KB finance/sales data
- Rule of 40 analysis combining growth rate and margin signals
- Cohort retention table generation from product-strategy KB
- Board-ready SaaS metric narratives with Korean prose
- Investor update metric summaries with opposite-direction risk sections
- User says "SaaS metrics", "MRR waterfall", "보드 리포트", "재무 서사"

## Do NOT Use

- General financial statements → `kwp-finance-financial-statements`
- Budget variance analysis → `kwp-finance-variance-analysis`
- Stock/equity financial analysis → `trading-us-stock-analysis`
- KB querying without financial narrative → `kb-query`

## Architecture

```
SaaS Metrics Narrator
├── Scan KB wikis (finance-policies, product-strategy, sales-playbook)
├── Extract metric signals
│   ├── Revenue (MRR, ARR, expansion, churn, new)
│   ├── Cost (CAC, hosting, R&D headcount, G&A)
│   ├── Efficiency (LTV:CAC, payback period, magic number)
│   └── Growth (month-over-month, net dollar retention)
├── Build metric frameworks
│   ├── MRR Waterfall (New + Expansion - Contraction - Churn)
│   ├── Rule of 40 (Growth Rate + Profit Margin)
│   ├── Cohort Retention Table (monthly cohorts × time periods)
│   ├── Unit Economics (LTV, CAC, Payback, LTV:CAC)
│   └── SaaS Quick Ratio (New+Expansion / Contraction+Churn)
├── Generate opposite-direction risk section (Karpathy Protocol)
│   ├── For each positive metric → argue the bear case
│   ├── For each negative metric → argue potential recovery
│   └── Surface metric that "sounds good but might not be"
├── Compose narrative in Korean
│   ├── Executive summary with traffic-light indicators
│   ├── Per-framework narrative with evidence citations
│   ├── Risk/bear-case section
│   └── Recommendations with confidence levels
└── Output markdown report + optional DOCX via anthropic-docx
```

## Metric Frameworks

### 1. MRR Waterfall

```
Beginning MRR
  + New MRR (new customers)
  + Expansion MRR (upgrades, seat adds)
  - Contraction MRR (downgrades)
  - Churned MRR (lost customers)
  = Ending MRR

Net New MRR = New + Expansion - Contraction - Churn
```

### 2. Rule of 40

```
Revenue Growth Rate (%) + EBITDA Margin (%) ≥ 40

Interpretation:
  ≥ 40: Healthy balance of growth and profitability
  30-39: Acceptable, monitor trend direction
  < 30: Needs strategic intervention
```

### 3. Cohort Retention Table

```
         M0    M1    M2    M3    M4    M5    M6
2024-Q1  100%  85%   78%   72%   70%   68%   67%
2024-Q2  100%  88%   82%   76%   73%   71%   --
2024-Q3  100%  90%   84%   79%   --    --    --
2024-Q4  100%  87%   80%   --    --    --    --
```

### 4. Unit Economics

| Metric | Formula | Healthy Target |
|---|---|---|
| LTV | ARPU × Gross Margin × (1 / Monthly Churn Rate) | > 3× CAC |
| CAC | Total S&M Spend / New Customers Acquired | Declining trend |
| Payback Period | CAC / (ARPU × Gross Margin) | < 18 months |
| LTV:CAC | LTV / CAC | > 3:1 |
| Magic Number | Net New ARR / Prior Period S&M Spend | > 0.75 |

### 5. SaaS Quick Ratio

```
SaaS Quick Ratio = (New MRR + Expansion MRR) / (Contraction MRR + Churned MRR)

  > 4: Excellent — growth far outpacing losses
  2-4: Healthy — sustainable growth
  1-2: Concerning — growth barely offsetting losses
  < 1: Critical — shrinking
```

## Execution Flow

### Step 1: Scan KB for Metric Signals

Read relevant wiki articles:
- `finance-policies/wiki/concepts/saas-metrics-*.md`
- `finance-policies/wiki/concepts/revenue-*.md`
- `finance-policies/wiki/concepts/pricing-*.md`
- `product-strategy/wiki/concepts/growth-*.md`
- `product-strategy/wiki/concepts/retention-*.md`
- `sales-playbook/wiki/concepts/pipeline-*.md`
- `sales-playbook/wiki/concepts/conversion-*.md`

Use `kb-search` to discover additional metric-bearing articles.

### Step 2: Extract and Normalize Metrics

For each metric signal found:
1. Extract numeric value or range
2. Record source article path and date
3. Flag confidence level: **Reported** (explicit number), **Inferred** (calculated from KB data), **Estimated** (derived from partial data with assumptions)
4. Normalize to common time periods (monthly for MRR, annual for ARR)

### Step 3: Build Framework Outputs

For each applicable framework:
1. Populate the framework template with extracted metrics
2. Calculate derived metrics (ratios, rates, trends)
3. Apply traffic-light assessment:
   - 🟢 At or above healthy target
   - 🟡 Within 20% of target
   - 🔴 Below 20% of target or declining trend

### Step 4: Opposite-Direction Risk Analysis (Karpathy Protocol)

For EACH metric conclusion in Step 3:

```markdown
### Bear Case Analysis

**Metric: {metric name} — currently {value} ({assessment})**

**The opposite argument:**
{Strongest case for why this metric might be misleading, unsustainable,
or hiding a problem. Cite specific KB evidence or market conditions.}

**Risk probability:** {Low/Medium/High}
**If materialized:** {Impact description}
```

This section is NOT optional. Skipping it violates the Karpathy Protocol and
produces sycophantic financial analysis.

### Step 5: Compose Korean Narrative

Structure the report:

```markdown
# SaaS 지표 분석 리포트 — {DATE}

## 요약 (Executive Summary)

| 지표 | 현재 값 | 전기 대비 | 상태 | 신뢰도 |
|---|---|---|---|---|
| MRR | {value} | {change} | {🟢/🟡/🔴} | {Reported/Inferred/Estimated} |
| ARR | {value} | {change} | {🟢/🟡/🔴} | ... |
| Rule of 40 | {value} | {change} | {🟢/🟡/🔴} | ... |
| Net Dollar Retention | {value} | {change} | {🟢/🟡/🔴} | ... |
| LTV:CAC | {value} | {change} | {🟢/🟡/🔴} | ... |
| SaaS Quick Ratio | {value} | {change} | {🟢/🟡/🔴} | ... |

**핵심 메시지:** {1-2 sentence narrative of the company's SaaS health}

## MRR 워터폴 분석
{Narrative description of MRR movement with evidence citations}

## 40의 법칙 분석
{Growth vs. profitability balance analysis}

## 코호트 리텐션
{Cohort table + narrative on retention trends}

## 유닛 이코노믹스
{LTV, CAC, payback analysis with trend}

## SaaS Quick Ratio
{Growth-to-loss ratio analysis}

## 리스크 분석 (반대 방향 테스트)
{Bear case for each major metric — from Step 4}

## 권장 사항
{Prioritized recommendations with confidence levels}

## 데이터 출처
{Numbered list of KB articles cited with confidence tags}
```

### Step 6: Output

1. Save markdown to `knowledge-bases/finance-policies/outputs/saas-narrative-{date}.md`
2. Optionally generate DOCX via `anthropic-docx` if `--docx` flag
3. Optionally generate visual dashboard HTML via `visual-explainer` if `--html` flag

## Composability

- **kb-query / kb-search**: Reads finance-policies, product-strategy, sales-playbook topics
- **anthropic-docx**: Generates board-ready DOCX reports
- **visual-explainer**: Renders dashboard HTML with metric charts
- **weighted-rubric-engine**: Can score SaaS health using a custom SaaS rubric
- **kb-daily-report**: SaaS narrative findings can feed into daily intelligence reports

## Constraints

- Every metric MUST cite its KB source article and confidence level
- Never fabricate financial data — clearly mark "Estimated" when derived from assumptions
- The opposite-direction risk section is MANDATORY — skip it and the report fails review
- Reports are additive — prior narrative snapshots are preserved for trend analysis
- Output file naming: `saas-narrative-{YYYY-MM-DD}.md`
- All narrative prose is in Korean; metric labels and framework names remain in English

## Examples

### Example 1: Full SaaS narrative

- **Trigger:** User says: "Generate SaaS financial narrative from the finance-policies KB"
- **Actions:** Query wiki for MRR, churn, CAC, LTV; compute MRR waterfall, Rule of 40, SaaS Quick Ratio; draft narrative; apply Karpathy Protocol bear case per major positive finding; save to `finance-policies/outputs/`.
- **Result:** Dated `saas-narrative-{YYYY-MM-DD}.md` with mandatory risk section.

### Example 2: Quick metrics check

- **Trigger:** User says: "What's our Rule of 40 status?"
- **Actions:** Extract revenue growth and profit margin from KB; compute Rule of 40; respond with one paragraph plus opposite-direction risk.
- **Result:** Point-in-time score with bear-case caveat tied to cited evidence.

## Error Handling

| Error | Action |
|-------|--------|
| Finance KB missing MRR data | Report "MRR data unavailable" and list metrics still computable |
| Computed metric impossible (e.g., invalid churn) | Flag data quality; omit that metric |
| No historical data for trends | Snapshot-only narrative; no trend claims |
| Conflicting values across articles | List all values with sources; flag conflict explicitly |

## Gotchas

- **Symptom:** Generic bear cases that could apply to any SaaS. **Root cause:** Karpathy Protocol executed as filler. **Correct approach:** Each bear case needs plausible triggers and KB-grounded mechanisms, not boilerplate.
- **Symptom:** Nonsensical waterfall or ratios. **Root cause:** Mixed monthly vs. annual figures in sources. **Correct approach:** Normalize to one period definition before any calculation; cite the chosen basis.
- **Symptom:** "Excellent" Quick Ratio hides churn pain. **Root cause:** Headline ratio without decomposition. **Correct approach:** Always show new, expansion, contraction, and churn components alongside the ratio.

## Output Discipline

- Every numeric metric must show formula and inputs (or cite KB lines that imply them).
- Use the latest complete reporting period; do not cherry-pick favorable windows.
- Match narrative strength to evidence density: tentative language when data is thin.

## Honest Reporting

- The bear-case section is mandatory; omitting it fails the Karpathy Protocol for this skill.
- Give unfavorable metrics the same prominence as favorable ones.
- Lead with data-quality caveats when extraction confidence is low or sources conflict.
