---
name: role-developer
description: >-
  Analyze a given topic from the Developer perspective — implementation
  complexity, code impact, testing requirements, documentation needs, and
  CI/CD implications. Scores topic relevance (1-10) and produces a structured
  Korean analysis document when relevant (>= 5). Composes deep-review,
  test-suite, diagnose, technical-writer, refactor-simulator, workflow-miner,
  skill-composer, semantic-guard, and intent-alignment-tracker. Use when the
  role-dispatcher invokes this skill with a topic, or when the user asks for
  "developer perspective", "개발자 관점", "구현 영향 분석", "implementation impact". Do
  NOT use for hands-on code review (use deep-review), bug diagnosis (use
  diagnose), or test generation (use test-suite). Korean triggers: "개발자 관점",
  "구현 영향", "코드 영향 분석".
disable-model-invocation: true
---

# Developer Perspective Analyzer

Analyzes any business topic from the Developer's viewpoint, covering implementation complexity,
codebase impact, testing strategy, documentation requirements, and CI/CD pipeline changes.

## Relevance Criteria

Score the topic 1-10 based on overlap with developer concerns:

| Domain | Weight | Keywords |
|--------|--------|----------|
| Implementation | High | code, implement, build, develop, API endpoint, module |
| Code impact | High | refactor, migration, breaking change, dependency, import |
| Testing | High | test, coverage, regression, E2E, unit test, edge case |
| CI/CD & tooling | High | pipeline, build, deploy, lint, pre-commit, GitHub Actions |
| Documentation | Medium | docs, README, ADR, API docs, changelog |
| Performance | Medium | latency, memory, optimization, profiling, bundle size |
| Security | Medium | vulnerability, auth, input validation, secret |
| Product & UX | Low | user flow, design, wireframe, persona |
| Strategy & finance | Low | market, revenue, investment, competition |

Score >= 5 → produce full analysis. Score < 5 → return brief relevance note only.

## Analysis Pipeline

When relevant, execute sequentially:

1. **Code Impact Analysis** (via `refactor-simulator`):
   - Affected files, modules, and services
   - Call site and import chain analysis
   - Type dependency mapping
   - Risk score

2. **Implementation Assessment** (via `deep-review`):
   - Architecture fit (frontend/backend/DB)
   - Code quality implications
   - Pattern consistency with existing codebase

3. **Testing Strategy** (via `test-suite` + `qa-test-expert`):
   - Test coverage gaps
   - Required new test cases (unit, integration, E2E)
   - Edge cases and failure modes

4. **Documentation Plan** (via `technical-writer`):
   - API documentation updates
   - ADR if architectural decision involved
   - Changelog entries

5. **Dev Workflow Pattern Discovery** (via `workflow-miner`):
   - Discover development workflow patterns from interaction history
   - Identify recurring dev sequences (e.g., branch → implement → test → review → merge)
   - Recommend automation for repetitive development tasks

6. **Dev Automation Assessment** (via `skill-composer`):
   - Recommend skill chain compositions for development workflow optimization
   - Map natural language implementation requirements to executable skill chains
   - Suggest reusable dev pipeline definitions (test → lint → deploy)

7. **Code Security Validation** (via `semantic-guard`):
   - Scan code changes for hardcoded secrets and credentials
   - Validate input handling for injection vulnerabilities
   - Check API responses for PII exposure risks

8. **Implementation Alignment** (via `intent-alignment-tracker`):
   - Measure alignment between implementation goals and delivered outcomes
   - Score per IA dimensions (Task Completion, Context Relevance, Efficiency, Side Effects)
   - Track code quality and velocity alignment trends

## Output Format

```markdown
# 개발자 관점 분석: {Topic}

## 관련도: {N}/10
## 분석 일자: {YYYY-MM-DD}

## 구현 요약 (3-5 bullets)
- ...

## 코드 영향 분석
### 영향 파일 수 & 범위
### 의존성 변경
### Breaking Changes

## 구현 복잡도
### 예상 난이도 (Low/Medium/High)
### 필요 기술 스택
### 기존 패턴 활용 가능성

## 테스트 전략
### 필요 테스트 유형
### 커버리지 목표
### 핵심 엣지 케이스

## CI/CD 영향
### 파이프라인 변경 필요
### 빌드 시간 영향
### 배포 전략

## 문서화 필요사항
### API 문서 변경
### ADR 작성 필요 여부
### Changelog 항목

## 리스크 & 의존성
### 기술적 리스크
### 외부 의존성
### 블로커

## 워크플로우 패턴 분석
### 발견된 개발 워크플로우 패턴
### 자동화 기회
### 스킬 체인 구성 권고

## 코드 보안 검증
### 시크릿/크리덴셜 점검
### 입력 검증 취약점
### PII 노출 리스크

## 의도 정렬 평가
### IA 점수 (0-100)
### 구현 목표-결과 정렬
### 개선 필요 영역

## 개발자 권고
### 구현 접근법
### 예상 소요 시간
### 단계별 작업 분해
```

## Error Handling

- If a composed skill is unavailable, skip that pipeline step and note the gap in the output
- If the topic is ambiguous, request clarification before scoring relevance
- If relevance score is borderline (4-5), include the score rationale in the output
- Always produce output in Korean regardless of the input language

## Example

**Input**: "New GPU inference service launch for enterprise customers"

**Relevance Score**: 9/10 (new service implementation + API + testing + deployment)

**Analysis highlights**:
- Impact: New service module, 3 existing services need client updates
- Complexity: High — gRPC server, model loading, GPU memory management
- Testing: Unit tests for inference logic, integration tests for API, E2E for deployment flow
- CI/CD: New Docker image, Helm chart, GPU-enabled test runner needed
- Documentation: API docs, deployment runbook, model format spec
- Recommendation: 3-sprint implementation, start with API contract and stub service
