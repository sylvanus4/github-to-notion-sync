---
name: role-cto
description: >
  Analyze a given topic from the CTO/technical leadership perspective — architecture impact,
  tech debt implications, performance/SLO concerns, security posture, and engineering capacity.
  Scores topic relevance (1-10) and produces a structured Korean analysis document when relevant (>= 5).
  Composes deep-review, backend-expert, sre-devops-expert, security-expert, and refactor-simulator.
  Use when the role-dispatcher invokes this skill with a topic, or when the user asks for
  "CTO perspective", "CTO 관점", "기술 리더 분석", "architecture impact".
  Do NOT use for hands-on code review (use deep-review), release pipeline execution
  (use release-commander), or incident response (use incident-to-improvement).
  Korean triggers: "CTO 관점", "기술 리더 분석", "아키텍처 영향".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "role-analysis"
---

# CTO Perspective Analyzer

Analyzes any business topic from the CTO's technical leadership viewpoint, covering architecture
impact, engineering capacity, tech debt, performance, security, and infrastructure implications.

## Relevance Criteria

Score the topic 1-10 based on overlap with CTO concerns:

| Domain | Weight | Keywords |
|--------|--------|----------|
| Architecture & design | High | microservice, API, system design, scalability, migration |
| Performance & SLO | High | latency, throughput, SLO, p99, monitoring, observability |
| Security & compliance | High | vulnerability, threat, OWASP, compliance, data protection |
| Tech debt & quality | High | refactor, legacy, code quality, maintainability |
| Infrastructure & DevOps | High | K8s, deployment, CI/CD, cloud, GPU cluster |
| Engineering capacity | Medium | team size, hiring, onboarding, skill gaps |
| Product & feature | Medium | new feature, MVP, technical feasibility |
| Strategic & market | Low | market, revenue, competition, pricing |
| HR & organization | Low | culture, retention, org structure |

Score >= 5 → produce full analysis. Score < 5 → return brief relevance note only.

## Analysis Pipeline

When relevant, execute sequentially:

1. **Architecture Impact** (via `backend-expert`):
   - System design implications
   - API contract changes
   - Data flow and dependency analysis
   - Async patterns and error handling review

2. **Blast Radius Simulation** (via `refactor-simulator`):
   - Affected files, call sites, import chains
   - Type dependency analysis
   - Risk score assessment

3. **Security Assessment** (via `security-expert`):
   - STRIDE threat model for the change
   - OWASP Top 10 exposure
   - Dependency vulnerability check

4. **Infrastructure & SLO** (via `sre-devops-expert`):
   - Deployment impact
   - SLO target compliance
   - Monitoring and alerting requirements
   - Capacity planning needs

## Output Format

```markdown
# CTO 관점 분석: {Topic}

## 관련도: {N}/10
## 분석 일자: {YYYY-MM-DD}

## 기술 요약 (3-5 bullets)
- ...

## 아키텍처 영향
### 시스템 설계 변경
### API/데이터 흐름 변화
### 의존성 분석

## 기술 부채 & 품질
### 영향 범위 (Blast Radius)
### 기존 부채 악화/개선 여부
### 리팩토링 필요성

## 성능 & SLO
### 예상 성능 영향
### SLO 목표 충족 여부
### 모니터링 요구사항

## 보안 평가
### 위협 모델 (STRIDE)
### 취약점 노출 수준
### 컴플라이언스 영향

## 인프라 & 배포
### 인프라 변경 필요
### 배포 전략
### 용량 계획

## 엔지니어링 리소스
### 필요 인력/기간
### 기술 스택 준비도
### 온보딩/교육 필요성

## 기술 의사결정 권고
### 즉시 조치
### 기술 로드맵 반영
### 위험 완화 방안
```

## Error Handling

- If a composed skill is unavailable, skip that pipeline step and note the gap in the output
- If the topic is ambiguous, request clarification before scoring relevance
- If relevance score is borderline (4-5), include the score rationale in the output
- Always produce output in Korean regardless of the input language

## Example

**Input**: "New GPU inference service launch for enterprise customers"

**Relevance Score**: 9/10 (new service architecture + GPU infra + security + SLO)

**Analysis highlights**:
- Architecture: New inference microservice, gRPC + REST dual API
- Blast Radius: 8 existing services need client updates, risk 6.5/10
- Security: Model endpoint requires auth middleware, rate limiting, input validation
- SLO: p99 inference latency target < 500ms requires GPU memory preallocation
- Infrastructure: 4x H100 nodes needed, Kueue queue configuration
- Recommendation: Phased rollout with canary deployment, 2-sprint implementation
