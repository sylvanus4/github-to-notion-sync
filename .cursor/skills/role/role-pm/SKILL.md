---
name: role-pm
description: >
  Analyze a given topic from the Product Manager perspective — PRD implications, sprint impact,
  user story generation, OKR alignment, roadmap changes, and stakeholder communication.
  Scores topic relevance (1-10) and produces a structured Korean analysis document when relevant (>= 5).
  Composes pm-execution, kwp-product-management-feature-spec, pm-product-discovery,
  kwp-product-management-roadmap-management, workflow-miner, skill-composer,
  and intent-alignment-tracker.
  Use when the role-dispatcher invokes this skill with a topic, or when the user asks for
  "PM perspective", "PM 관점", "기획자 분석", "product impact".
  Do NOT use for writing a full PRD (use pm-execution), sprint planning execution
  (use agency-sprint-prioritizer), or A/B test analysis (use pm-data-analytics).
  Korean triggers: "PM 관점", "기획자 분석", "제품 영향".
metadata:
  author: "thaki"
  version: "1.1.1"
  category: "role-analysis"
---

# PM Perspective Analyzer

Analyzes any business topic from the Product Manager's viewpoint, covering product requirements,
user impact, sprint/roadmap changes, OKR alignment, and stakeholder communication needs.

## Relevance Criteria

Score the topic 1-10 based on overlap with PM concerns:

| Domain | Weight | Keywords |
|--------|--------|----------|
| Product requirements | High | feature, PRD, spec, user story, acceptance criteria |
| User experience | High | user flow, journey, persona, usability, onboarding |
| Roadmap & planning | High | roadmap, sprint, milestone, priority, backlog |
| Metrics & OKR | High | KPI, OKR, retention, conversion, engagement |
| Stakeholder comms | Medium | update, report, alignment, decision, trade-off |
| Market & competition | Medium | competitor, positioning, market fit, user research |
| Technical feasibility | Medium | API, integration, migration, performance |
| Financial & strategy | Low | revenue, cost, investment, valuation |
| HR & organization | Low | team, hiring, culture |

Score >= 5 → produce full analysis. Score < 5 → return brief relevance note only.

## Analysis Pipeline

When relevant, execute sequentially:

1. **Product Discovery** (via `pm-product-discovery`):
   - Opportunity Solution Tree for the topic
   - Assumption identification and testing plan
   - User impact hypothesis

2. **Requirements Analysis** (via `pm-execution` + `kwp-product-management-feature-spec`):
   - User stories and job stories (JTBD)
   - Acceptance criteria
   - Success metrics definition

3. **Roadmap Impact** (via `kwp-product-management-roadmap-management`):
   - Now/Next/Later positioning
   - Dependency mapping
   - Sprint capacity impact

4. **Stakeholder Summary** (via `kwp-product-management-stakeholder-comms`):
   - Engineering-facing brief
   - Executive-facing brief
   - Customer-facing narrative

5. **Product Workflow Pattern Discovery** (via `workflow-miner`):
   - Discover product management workflow patterns from interaction history
   - Identify recurring PM sequences (e.g., discovery → spec → sprint → retro)
   - Recommend automation for repetitive product planning tasks

6. **Process Automation** (via `skill-composer`):
   - Recommend skill chain compositions for product workflow optimization
   - Map natural language product requirements to executable skill chains
   - Suggest reusable PM pipeline definitions

7. **Product-User Intent Alignment** (via `intent-alignment-tracker`):
   - Measure alignment between product goals and user outcomes
   - Score per IA dimensions (Task Completion, Context Relevance, Efficiency, Side Effects)
   - Track product-market fit alignment trends

## Output Format

```markdown
# PM 관점 분석: {Topic}

## 관련도: {N}/10
## 분석 일자: {YYYY-MM-DD}

## 제품 요약 (3-5 bullets)
- ...

## 사용자 영향 분석
### 영향받는 페르소나
### 사용자 여정 변화
### JTBD 매핑

## 제품 요구사항
### 사용자 스토리 (상위 5개)
### 수용 기준 (핵심)
### 성공 메트릭

## 로드맵 영향
### Now/Next/Later 배치
### 의존성
### 스프린트 용량 영향

## OKR 정렬
### 관련 Objective
### Key Result 영향
### 메트릭 변동 예측

## 리스크 & 트레이드오프
### 제품 리스크
### 기술적 제약
### 우선순위 트레이드오프

## 이해관계자 브리핑
### 경영진 요약
### 엔지니어링 핸드오프
### 고객 커뮤니케이션

## 워크플로우 패턴 분석
### 발견된 제품 관리 패턴
### 프로세스 자동화 기회
### 스킬 체인 구성 권고

## 의도 정렬 평가
### IA 점수 (0-100)
### 제품-사용자 정렬 추적
### 개선 필요 영역

## PM 권고
### 즉시 착수 항목
### 추가 검증 필요 항목
### 보류/모니터링 항목
```

## Agent Response Contract (Binary Eval Gate)

When relevance score is **≥ 5**, every end-user analysis MUST satisfy:

1. **EVAL 1 — Relevance first:** Before any other analysis sections, output `## 관련도 선행 평가` containing `**점수:** N/10` and `**선행 근거:**` (2–4 Korean sentences explicitly mapping the topic to the **Relevance Criteria** table). If N < 5, output only a short Korean relevance note—do not fill the full template.

2. **EVAL 2 — Composed sub-skills (≥3):** Include `## 위임된 서브스킬` as a markdown table with **at least three rows** chosen from this skill's **Analysis Pipeline** only. Columns: 서브스킬 (backtick name, e.g. `pm-product-discovery`), 위임 범위 (Korean), 기대 산출물 (Korean).

3. **EVAL 3 — Korean narrative structure:** After the sections above, all substantive analysis MUST be **Korean** (proper nouns and skill identifiers may appear in English inside backticks). Use H2/H3 headings, bullet lists, and **at least one** additional markdown table in the body (excluding the delegation table).

4. **EVAL 4 — Actionable recommendations:** End with `## 실행 액션 플랜` containing **at least three** numbered items (`1.`, `2.`, `3.`). Each item MUST explicitly include **담당:** (role or team) and **기한:** (concrete horizon, e.g. 2주 내, 30일 내, 분기 내).

## Error Handling

- If a composed skill is unavailable, skip that pipeline step and note the gap in the output
- If the topic is ambiguous, request clarification before scoring relevance
- If relevance score is borderline (4-5), include the score rationale in the output
- Always produce output in Korean regardless of the input language

## Example

**Input**: "New GPU inference service launch for enterprise customers"

**Relevance Score**: 8/10 (new feature + user impact + roadmap change + metrics)

**Analysis highlights**:
- Persona: MLOps Engineer, Cluster Admin — new inference workflow needed
- User Stories: 6 stories covering model deployment, scaling, monitoring
- Roadmap: Shifts Q2 Now slot, pushes model versioning to Next
- OKR: Directly impacts O1-KR2 (enterprise feature adoption 50%+)
- Risk: Scope creep from enterprise customization requests
- Recommendation: MVP with 3 core stories, pilot with 2 customers in Sprint 25
