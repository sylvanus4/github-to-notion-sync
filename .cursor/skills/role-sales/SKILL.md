---
name: role-sales
description: >
  Analyze a given topic from the Sales perspective — sales enablement impact, competitive
  battlecard needs, customer outreach implications, pipeline effects, and demo/asset requirements.
  Scores topic relevance (1-10) and produces a structured Korean analysis document when relevant (>= 5).
  Composes kwp-sales-account-research, kwp-sales-competitive-intelligence,
  kwp-sales-create-an-asset, demo-forge, workflow-miner, and intent-alignment-tracker.
  Use when the role-dispatcher invokes this skill with a topic, or when the user asks for
  "sales perspective", "영업 관점", "영업 분석", "sales enablement impact".
  Do NOT use for drafting outreach emails (use kwp-sales-draft-outreach), call preparation
  (use kwp-sales-call-prep), or lead prospecting (use kwp-apollo-prospect).
  Korean triggers: "영업 관점", "영업 분석", "세일즈 영향".
metadata:
  author: "thaki"
  version: "1.1.0"
  category: "role-analysis"
---

# Sales Perspective Analyzer

Analyzes any business topic from the Sales team's viewpoint, covering sales enablement,
competitive positioning, customer impact, pipeline effects, and demo/asset requirements.

## Relevance Criteria

Score the topic 1-10 based on overlap with sales concerns:

| Domain | Weight | Keywords |
|--------|--------|----------|
| Customer impact | High | customer, enterprise, deal, contract, renewal, churn |
| Competitive positioning | High | competitor, differentiation, win/loss, battlecard |
| Sales enablement | High | pitch, demo, deck, one-pager, case study, ROI |
| Pipeline & revenue | High | pipeline, ARR, deal size, conversion, quota |
| Product launch | Medium | launch, new feature, GA, beta, pricing change |
| Market & ICP | Medium | market, segment, ICP, vertical, territory |
| Partner & channel | Medium | partner, reseller, channel, referral |
| Technical details | Low | API, code, architecture, deployment |
| HR & operations | Low | hiring, process, compliance, finance |

Score >= 5 → produce full analysis. Score < 5 → return brief relevance note only.

## Analysis Pipeline

When relevant, execute sequentially:

1. **Customer Impact** (via `kwp-sales-account-research`):
   - Impact on existing customer accounts
   - Upsell/cross-sell opportunities
   - Churn risk assessment
   - Customer communication needs

2. **Competitive Positioning** (via `kwp-sales-competitive-intelligence`):
   - Updated battlecard requirements
   - Win/loss implications
   - Differentiation messaging

3. **Sales Assets** (via `kwp-sales-create-an-asset`):
   - Required new sales materials
   - Pitch deck updates
   - ROI calculator needs
   - Case study opportunities

4. **Demo Strategy** (via `demo-forge`):
   - Demo scenario requirements
   - Before/after showcase opportunities
   - Customer-facing demonstration plan

5. **Sales Workflow Pattern Discovery** (via `workflow-miner`):
   - Discover sales workflow patterns from interaction history
   - Identify recurring sales sequences (e.g., research → outreach → demo → close)
   - Recommend automation for repetitive sales enablement tasks

6. **Customer Alignment** (via `intent-alignment-tracker`):
   - Measure alignment between customer needs and sales/product offerings
   - Score per IA dimensions (Task Completion, Context Relevance, Efficiency, Side Effects)
   - Track customer satisfaction and deal alignment trends

## Output Format

```markdown
# 영업 관점 분석: {Topic}

## 관련도: {N}/10
## 분석 일자: {YYYY-MM-DD}

## 영업 요약 (3-5 bullets)
- ...

## 고객 영향
### 기존 고객 영향
### 업셀/크로스셀 기회
### 이탈 리스크

## 경쟁 포지셔닝
### 배틀카드 업데이트 필요
### 차별화 메시징
### Win/Loss 영향

## 세일즈 에셋 필요사항
### 피치 덱 변경
### 원페이저/케이스 스터디
### ROI 계산기
### 데모 시나리오

## 파이프라인 영향
### 예상 딜 사이즈 변화
### 세일즈 사이클 영향
### 분기 목표 영향

## 가격 & 패키징
### 가격 변동 여부
### 패키징 변경
### 할인/프로모션 기회

## 워크플로우 패턴 분석
### 발견된 영업 워크플로우 패턴
### 자동화 기회

## 의도 정렬 평가
### IA 점수 (0-100)
### 고객 요구-제안 정렬
### 개선 필요 영역

## 영업 권고
### 즉시 고객 커뮤니케이션
### 세일즈 트레이닝 필요
### 신규 에셋 제작 우선순위
### 파이프라인 목표 조정
```

## Error Handling

- If a composed skill is unavailable, skip that pipeline step and note the gap in the output
- If the topic is ambiguous, request clarification before scoring relevance
- If relevance score is borderline (4-5), include the score rationale in the output
- Always produce output in Korean regardless of the input language

## Example

**Input**: "New GPU inference service launch for enterprise customers"

**Relevance Score**: 9/10 (new product for enterprise + upsell + competitive + pricing)

**Analysis highlights**:
- Customer: 12 existing enterprise accounts eligible for upsell, avg deal size +$25K/yr
- Competition: Need battlecard update vs AWS SageMaker inference pricing
- Assets: New pitch deck, inference ROI calculator, 2 pilot case studies
- Pipeline: Q3 pipeline boost estimated $300K from inference add-on deals
- Recommendation: Prioritize top 5 accounts for early access, create demo video
