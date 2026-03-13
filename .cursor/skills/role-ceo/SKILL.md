---
name: role-ceo
description: >
  Analyze a given topic from the CEO/executive perspective — strategic impact, market positioning,
  stakeholder communication, and investment implications. Scores topic relevance (1-10) and produces
  a structured Korean analysis document when relevant (>= 5). Composes pm-product-strategy,
  presentation-strategist, agency-executive-summary-generator, and pm-market-research.
  Use when the role-dispatcher invokes this skill with a topic, or when the user asks for
  "CEO perspective", "CEO 관점", "경영진 분석", "strategic impact analysis".
  Do NOT use for daily morning briefings (use morning-ship), investor deck creation only
  (use presentation-strategist), or routine stakeholder updates (use kwp-product-management-stakeholder-comms).
  Korean triggers: "CEO 관점", "경영진 분석", "전략 영향".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "role-analysis"
---

# CEO Perspective Analyzer

Analyzes any business topic from the CEO's strategic viewpoint, covering market positioning,
financial implications, stakeholder communication needs, and decision-making priorities.

## Relevance Criteria

Score the topic 1-10 based on overlap with CEO concerns:

| Domain | Weight | Keywords |
|--------|--------|----------|
| Strategic direction | High | vision, strategy, roadmap, pivot, expansion, market entry |
| Financial impact | High | revenue, cost, ROI, investment, funding, runway, valuation |
| Market & competitive | High | market share, competition, TAM, positioning, differentiation |
| Stakeholder relations | Medium | investors, board, partners, customers, reputation |
| Organization & culture | Medium | hiring, team structure, leadership, culture, growth |
| Product decisions | Medium | product launch, feature priority, pricing, go-to-market |
| Operations & risk | Low | compliance, security incident, process change |
| Technical implementation | Low | code, API, database, CI/CD, testing |

Score >= 5 → produce full analysis. Score < 5 → return brief relevance note only.

## Analysis Pipeline

When relevant, execute sequentially:

1. **Strategic Assessment** (via `pm-product-strategy`):
   - SWOT analysis of the topic's strategic implications
   - Impact on company vision and product roadmap
   - Competitive positioning changes

2. **Market Impact** (via `pm-market-research`):
   - TAM/SAM/SOM implications
   - Customer segment impact
   - Market timing assessment

3. **Executive Summary** (via `agency-executive-summary-generator`):
   - SCQA-structured executive brief
   - Key findings with quantitative backing
   - Prioritized recommendations with timeline and owners

4. **Communication Plan** (via `kwp-product-management-stakeholder-comms`):
   - Board/investor messaging
   - Internal team communication
   - Customer-facing narrative

## Output Format

```markdown
# CEO 관점 분석: {Topic}

## 관련도: {N}/10
## 분석 일자: {YYYY-MM-DD}

## 경영진 요약 (3-5 bullets)
- ...

## 전략적 영향 분석
### SWOT
### 시장 포지셔닝 변화
### 로드맵 영향

## 재무적 시사점
### 매출/비용 영향
### 투자 필요성
### ROI 전망

## 리스크 & 기회
### 핵심 리스크 (확률 x 영향)
### 기회 요인

## 이해관계자 커뮤니케이션 계획
### 투자자/이사회
### 내부 팀
### 고객

## 의사결정 권고
### 즉시 조치 필요 사항
### 단기 (1-3개월) 액션
### 중장기 고려 사항
```

## Error Handling

- If a composed skill is unavailable, skip that pipeline step and note the gap in the output
- If the topic is ambiguous, request clarification before scoring relevance
- If relevance score is borderline (4-5), include the score rationale in the output
- Always produce output in Korean regardless of the input language

## Example

**Input**: "New GPU inference service launch for enterprise customers"

**Relevance Score**: 9/10 (product launch + market entry + revenue impact)

**Analysis highlights**:
- SWOT: Strength in existing GPU orchestration → natural extension
- Market: Enterprise AI inference TAM $5.2B, 32% CAGR
- Financial: Projected ARR uplift 15-20% within 6 months
- Risk: Competitive response from hyperscalers within 3 months
- Recommendation: Fast-follow GTM with 3 pilot customers in Q2
