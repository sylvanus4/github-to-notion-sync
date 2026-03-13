---
name: role-finance
description: >
  Analyze a given topic from the Finance perspective — financial impact, budget variance,
  ROI analysis, cash flow implications, and audit/compliance requirements.
  Scores topic relevance (1-10) and produces a structured Korean analysis document when relevant (>= 5).
  Composes kwp-finance-variance-analysis, kwp-finance-financial-statements,
  agency-finance-tracker, and kwp-finance-audit-support.
  Use when the role-dispatcher invokes this skill with a topic, or when the user asks for
  "finance perspective", "재무 관점", "재무 분석", "financial impact analysis".
  Do NOT use for financial statement generation (use kwp-finance-financial-statements),
  month-end close management (use kwp-finance-close-management), or
  reconciliation (use kwp-finance-reconciliation).
  Korean triggers: "재무 관점", "재무 분석", "재무 영향".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "role-analysis"
---

# Finance Perspective Analyzer

Analyzes any business topic from the Finance team's viewpoint, covering financial impact,
budget implications, ROI projection, cash flow effects, and audit compliance.

## Relevance Criteria

Score the topic 1-10 based on overlap with finance concerns:

| Domain | Weight | Keywords |
|--------|--------|----------|
| Revenue & cost | High | revenue, cost, margin, pricing, unit economics |
| Budget & forecast | High | budget, forecast, variance, capex, opex |
| Investment & ROI | High | ROI, payback, NPV, IRR, investment, funding |
| Cash flow | High | cash flow, runway, burn rate, working capital |
| Audit & compliance | Medium | audit, SOX, tax, regulatory, disclosure |
| Vendor & procurement | Medium | vendor, contract, SLA, procurement, licensing |
| Risk management | Medium | financial risk, hedging, insurance, contingency |
| Financial reporting | Medium | P&L, balance sheet, KPI, dashboard |
| Technical implementation | Low | code, API, database, deployment |
| HR & operations | Low | hiring, process, culture |

Score >= 5 → produce full analysis. Score < 5 → return brief relevance note only.

## Analysis Pipeline

When relevant, execute sequentially:

1. **Financial Impact** (via `kwp-finance-variance-analysis`):
   - Budget variance analysis (volume/mix/price decomposition)
   - Revenue impact projection
   - Cost structure changes
   - Margin impact

2. **Cash Flow & Investment** (via `agency-finance-tracker`):
   - Cash flow implications
   - Capex vs Opex classification
   - Runway impact
   - Investment requirements

3. **Financial Statements** (via `kwp-finance-financial-statements`):
   - P&L impact projection
   - Balance sheet changes
   - Cash flow statement effects

4. **Audit & Compliance** (via `kwp-finance-audit-support`):
   - SOX control implications
   - Revenue recognition treatment
   - Disclosure requirements

## Output Format

```markdown
# 재무 관점 분석: {Topic}

## 관련도: {N}/10
## 분석 일자: {YYYY-MM-DD}

## 재무 요약 (3-5 bullets)
- ...

## 매출/비용 영향
### 매출 영향 (상세)
### 비용 구조 변화
### 마진 영향
### 단위 경제학

## 예산 영향
### 기존 예산 대비 차이
### 추가 예산 필요
### Volume/Mix/Price 분석

## 투자 분석
### 초기 투자 비용
### ROI 전망
### 회수 기간 (Payback Period)
### NPV/IRR 추정

## 현금 흐름
### 단기 현금 흐름 영향
### 런웨이 변동
### 자본/운영비 분류

## 감사 & 컴플라이언스
### 회계 처리 방식
### SOX 통제 영향
### 매출 인식 처리
### 공시 요구사항

## 벤더 & 계약
### 신규 계약 필요
### 라이선스 비용
### SLA 재무 영향

## 재무 권고
### 즉시 예산 조정 필요
### 분기 재무 영향 (Q별)
### 재무 모니터링 KPI
### 리스크 헷지 방안
```

## Error Handling

- If a composed skill is unavailable, skip that pipeline step and note the gap in the output
- If the topic is ambiguous, request clarification before scoring relevance
- If relevance score is borderline (4-5), include the score rationale in the output
- Always produce output in Korean regardless of the input language

## Example

**Input**: "New GPU inference service launch for enterprise customers"

**Relevance Score**: 8/10 (new revenue stream + GPU infra capex + pricing model + margin)

**Analysis highlights**:
- Revenue: New ARR stream estimated $500K-$1.2M in Year 1
- Cost: GPU infra capex $200K (4x H100), monthly opex $15K
- ROI: 18-month payback at 40% gross margin
- Budget: Q2 capex increase $200K, opex +$45K/quarter
- Cash Flow: Negative cash impact Q2-Q3, positive from Q4
- Recommendation: Approve capex, set pricing at $0.05/inference-hour, review at Q3 close
