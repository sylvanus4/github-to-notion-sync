---
name: role-hr
description: >-
  Analyze a given topic from the HR perspective — organizational impact,
  hiring needs, change management, training requirements, and people analytics
  implications. Scores topic relevance (1-10) and produces a structured Korean
  analysis document when relevant (>= 5). Composes
  kwp-human-resources-org-planning, kwp-human-resources-people-analytics,
  kwp-operations-change-management, kwp-human-resources-interview-prep,
  workflow-miner, semantic-guard, and intent-alignment-tracker. Use when the
  role-dispatcher invokes this skill with a topic, or when the user asks for
  "HR perspective", "HR 관점", "인사 분석", "organizational impact". Do NOT use for
  compensation benchmarking (use
  kwp-human-resources-compensation-benchmarking), employee handbook creation
  (use kwp-human-resources-employee-handbook), or recruiting pipeline
  management (use kwp-human-resources-recruiting-pipeline). Korean triggers:
  "HR 관점", "인사 분석", "조직 영향".
disable-model-invocation: true
---

# HR Perspective Analyzer

Analyzes any business topic from the HR team's viewpoint, covering organizational impact,
workforce planning, change management, training needs, and employee experience implications.

## Relevance Criteria

Score the topic 1-10 based on overlap with HR concerns:

| Domain | Weight | Keywords |
|--------|--------|----------|
| Organizational change | High | reorg, restructure, new team, expansion, merger |
| Workforce planning | High | headcount, hiring, skill gap, capacity, staffing |
| Change management | High | rollout, transition, adoption, communication, training |
| Employee experience | Medium | onboarding, retention, engagement, culture, morale |
| Compensation & benefits | Medium | salary, equity, benefits, benchmark, comp review |
| Learning & development | Medium | training, upskilling, certification, workshop |
| Compliance & policy | Medium | labor law, policy, handbook, GDPR (employee data) |
| Product & technology | Low | feature, API, code, deployment |
| Finance & strategy | Low | revenue, market, investment, pricing |

Score >= 5 → produce full analysis. Score < 5 → return brief relevance note only.

## Analysis Pipeline

When relevant, execute sequentially:

1. **Organizational Impact** (via `kwp-human-resources-org-planning`):
   - Team structure changes
   - Headcount requirements
   - Span of control impact
   - Reporting line adjustments

2. **People Analytics** (via `kwp-human-resources-people-analytics`):
   - Workforce capacity assessment
   - Skill gap analysis
   - Attrition risk for affected teams
   - Productivity impact estimation

3. **Change Management** (via `kwp-operations-change-management`):
   - Communication plan
   - Stakeholder mapping
   - Adoption timeline
   - Resistance assessment

4. **Talent Acquisition** (via `kwp-human-resources-interview-prep`):
   - New role definitions (if hiring needed)
   - Competency requirements
   - Interview guide for new positions

5. **HR Process Pattern Discovery** (via `workflow-miner`):
   - Discover HR workflow patterns from interaction history
   - Identify recurring HR sequences (e.g., hiring → onboarding → review → retention)
   - Recommend automation for repetitive people management tasks

6. **PII Protection** (via `semantic-guard`):
   - Scan HR documents and communications for employee PII exposure
   - Validate data flow for sensitive employee information
   - Check outputs for GDPR/labor law compliance in data handling

7. **Organizational Alignment** (via `intent-alignment-tracker`):
   - Measure alignment between organizational goals and workforce outcomes
   - Score per IA dimensions (Task Completion, Context Relevance, Efficiency, Side Effects)
   - Track employee engagement and organizational health alignment trends

## Output Format

```markdown
# HR 관점 분석: {Topic}

## 관련도: {N}/10
## 분석 일자: {YYYY-MM-DD}

## HR 요약 (3-5 bullets)
- ...

## 조직 영향
### 팀 구조 변화
### 인력 필요
### 보고 체계 변경

## 인력 분석
### 역량 갭 분석
### 용량 평가
### 이직 리스크

## 변화 관리
### 커뮤니케이션 계획
### 이해관계자 매핑
### 채택 타임라인
### 저항 요인

## 교육 & 역량 개발
### 필요 교육 프로그램
### 대상 인원
### 일정 & 형태

## 채용 필요
### 신규 직무 정의
### 역량 요구사항
### 채용 우선순위

## 정책 & 컴플라이언스
### 규정 변경 필요
### 근로계약 영향
### 개인정보 (직원 데이터)

## 워크플로우 패턴 분석
### 발견된 HR 프로세스 패턴
### 자동화 기회

## 개인정보 보호 검증
### PII 노출 점검
### GDPR/노동법 데이터 컴플라이언스

## 의도 정렬 평가
### IA 점수 (0-100)
### 조직 목표-인력 성과 정렬
### 개선 필요 영역

## HR 권고
### 즉시 조치 (사내 공지 등)
### 중기 계획 (채용/교육)
### 모니터링 지표 (eNPS, 이직률)
```

## Error Handling

- If a composed skill is unavailable, skip that pipeline step and note the gap in the output
- If the topic is ambiguous, request clarification before scoring relevance
- If relevance score is borderline (4-5), include the score rationale in the output
- Always produce output in Korean regardless of the input language

## Example

**Input**: "New GPU inference service launch for enterprise customers"

**Relevance Score**: 5/10 (new team capacity needed + skill gaps + onboarding)

**Analysis highlights**:
- Org Impact: Need 2 ML inference engineers — new sub-team under Platform
- Skill Gap: GPU optimization and model serving expertise not in current team
- Change: Engineering team communication about new service ownership
- Training: CUDA optimization workshop for existing ML engineers (2 days)
- Recommendation: Start recruiting immediately, target 4-week onboarding
