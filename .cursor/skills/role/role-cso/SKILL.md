---
name: role-cso
description: >
  Analyze a given topic from the CSO (Chief Strategy Officer) perspective — market sizing,
  competitive positioning, GTM strategy, business model impact, and scenario planning.
  Scores topic relevance (1-10) and produces a structured Korean analysis document when relevant (>= 5).
  Composes pm-market-research, pm-go-to-market, pm-product-strategy,
  kwp-marketing-competitive-analysis, workflow-miner, skill-composer,
  intent-alignment-tracker, and optionally sun-tzu-analyzer (via --with-sun-tzu).
  Use when the role-dispatcher invokes this skill with a topic, or when the user asks for
  "CSO perspective", "CSO 관점", "전략 분석", "market strategy impact".
  Do NOT use for full GTM execution (use pm-go-to-market), Lean Canvas only
  (use pm-product-strategy), or competitive battlecard creation (use kwp-sales-competitive-intelligence).
  Korean triggers: "CSO 관점", "전략 분석", "시장 전략 영향".
metadata:
  author: "thaki"
  version: "1.1.0"
  category: "role-analysis"
---

# CSO Perspective Analyzer

Analyzes any business topic from the CSO's strategic viewpoint, covering market opportunity,
competitive landscape, go-to-market implications, business model changes, and scenario planning.

## Relevance Criteria

Score the topic 1-10 based on overlap with CSO concerns:

| Domain | Weight | Keywords |
|--------|--------|----------|
| Market opportunity | High | TAM, SAM, SOM, market size, growth, expansion |
| Competitive landscape | High | competitor, differentiation, positioning, battlecard |
| GTM strategy | High | go-to-market, launch, channel, ICP, beachhead |
| Business model | High | pricing, monetization, revenue model, unit economics |
| Product strategy | High | vision, roadmap, pivot, value proposition |
| Growth & acquisition | Medium | growth loop, viral, PLG, funnel, conversion |
| Partnerships | Medium | partner, ecosystem, integration, alliance |
| Trends & research | Medium | trend, industry, regulation, disruption |
| Technical implementation | Low | code, API, database, CI/CD |
| HR & operations | Low | hiring, process, compliance |

Score >= 5 → produce full analysis. Score < 5 → return brief relevance note only.

## Analysis Pipeline

When relevant, execute sequentially:

1. **Market Analysis** (via `pm-market-research`):
   - TAM/SAM/SOM impact assessment
   - Market segmentation changes
   - Customer persona updates
   - Competitive landscape shifts

2. **GTM Strategy** (via `pm-go-to-market`):
   - ICP refinement
   - Channel strategy implications
   - Growth loop opportunities
   - Beachhead segment assessment

3. **Business Model** (via `pm-product-strategy`):
   - Value proposition changes
   - Pricing strategy impact
   - Lean Canvas updates
   - SWOT implications

4. **Competitive Intelligence** (via `kwp-marketing-competitive-analysis`):
   - Competitor response prediction
   - Positioning differentiation
   - Messaging strategy adjustments

5. **Strategic Pattern Discovery** (via `workflow-miner`):
   - Discover strategic planning workflow patterns from interaction history
   - Identify recurring strategy sequences (e.g., market scan → SWOT → GTM → execute)
   - Recommend automation for repetitive strategy analysis tasks

6. **Strategy Automation** (via `skill-composer`):
   - Recommend skill chain compositions for strategic workflow optimization
   - Map natural language strategy requirements to executable skill chains
   - Suggest reusable strategy analysis pipeline definitions

7. **Strategic Terrain Analysis** (via `sun-tzu-analyzer`, optional — `--with-sun-tzu`):
   - Map competitive landscape to Sun Tzu's 5 factors (Terrain, Enemy, Relative Strength, Information Asymmetry, Timing)
   - Identify the real strategic threat vs. visible competitors
   - Prescribe a decisive 7-day action based on terrain control principles
   - Output as concise Role Layer brief (< 200 words) integrated into the CSO report
   - Skip if `--with-sun-tzu` flag is not set or if `sun-tzu-analyzer` skill is unavailable

8. **Strategy Alignment** (via `intent-alignment-tracker`):
   - Measure alignment between strategic goals and market execution outcomes
   - Score per IA dimensions (Task Completion, Context Relevance, Efficiency, Side Effects)
   - Track strategy-to-market-fit alignment trends

## Output Format

```markdown
# CSO 관점 분석: {Topic}

## 관련도: {N}/10
## 분석 일자: {YYYY-MM-DD}

## 전략 요약 (3-5 bullets)
- ...

## 시장 기회 분석
### TAM/SAM/SOM 영향
### 시장 세분화 변화
### 타이밍 평가

## 경쟁 환경
### 경쟁사 반응 예측
### 차별화 포인트
### 포지셔닝 변화

## GTM 전략
### ICP 영향
### 채널 전략
### 성장 루프 기회
### 비치헤드 세그먼트

## 비즈니스 모델
### 가치 제안 변화
### 가격/수익 모델 영향
### 단위 경제학 변동

## 시나리오 플래닝
### Base Case
### Bull Case
### Bear Case

## 손자병법 전략 지형 (optional, --with-sun-tzu)
### 핵심 지형 재해석
### 진짜 적
### 허점과 처방
### 지배 원리

## 워크플로우 패턴 분석
### 발견된 전략 분석 패턴
### 자동화 기회
### 스킬 체인 구성 권고

## 의도 정렬 평가
### IA 점수 (0-100)
### 전략 목표-시장 정렬
### 개선 필요 영역

## CSO 권고
### 전략적 우선순위
### 시장 진입/확장 액션
### 파트너십 기회
### 모니터링 지표
```

## Error Handling

- If a composed skill is unavailable, skip that pipeline step and note the gap in the output
- If the topic is ambiguous, request clarification before scoring relevance
- If relevance score is borderline (4-5), include the score rationale in the output
- Always produce output in Korean regardless of the input language

## Example

**Input**: "New GPU inference service launch for enterprise customers"

**Relevance Score**: 9/10 (market expansion + GTM + competitive positioning + pricing)

**Analysis highlights**:
- Market: Inference-as-a-Service TAM $5.2B, enterprise segment $2.1B (28% CAGR)
- Competition: AWS SageMaker, GCP Vertex AI — differentiate on multi-cloud + on-prem
- GTM: Beachhead = regulated industries (finance, healthcare) needing on-prem inference
- Business Model: Usage-based pricing, $0.05/inference-hour, 65% gross margin target
- Scenario: Bull case 30% ARR uplift if 5+ enterprise deals close in H2
