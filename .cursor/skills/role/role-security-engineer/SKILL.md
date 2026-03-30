---
name: role-security-engineer
description: >
  Analyze a given topic from the Security Engineer perspective — threat modeling (STRIDE),
  vulnerability assessment (OWASP Top 10), compliance impact, incident readiness, and
  access control implications. Scores topic relevance (1-10) and produces a structured
  Korean analysis document when relevant (>= 5).   Composes security-expert, compliance-governance, dependency-auditor,
  kwp-operations-risk-assessment, workflow-miner, semantic-guard, and intent-alignment-tracker.
  Use when the role-dispatcher invokes this skill with a topic, or when the user asks for
  "security perspective", "보안 관점", "보안 엔지니어 분석", "threat analysis".
  Do NOT use for running a full security audit (use security-expert), dependency CVE scanning
  (use dependency-auditor), or incident response (use incident-to-improvement).
  Korean triggers: "보안 관점", "보안 엔지니어 분석", "위협 분석".
metadata:
  author: "thaki"
  version: "1.1.0"
  category: "role-analysis"
---

# Security Engineer Perspective Analyzer

Analyzes any business topic from the Security Engineer's viewpoint, covering threat modeling,
vulnerability exposure, compliance requirements, data protection, and incident preparedness.

## Relevance Criteria

Score the topic 1-10 based on overlap with security concerns:

| Domain | Weight | Keywords |
|--------|--------|----------|
| Authentication & authorization | High | auth, login, JWT, RBAC, ABAC, session, token |
| Data protection | High | PII, encryption, data classification, GDPR, privacy |
| Vulnerability & threats | High | CVE, OWASP, injection, XSS, CSRF, SSRF |
| API security | High | rate limit, input validation, API key, endpoint exposure |
| Compliance & audit | High | SOC 2, ISO 27001, audit log, regulatory |
| Infrastructure security | Medium | network, firewall, container, K8s, secrets management |
| Dependency security | Medium | supply chain, package, CVE scan, SCA |
| Incident response | Medium | breach, incident, forensics, recovery, postmortem |
| Product & UX | Low | UI, dashboard, onboarding, user flow |
| Finance & strategy | Low | revenue, market, investment |

Score >= 5 → produce full analysis. Score < 5 → return brief relevance note only.

## Analysis Pipeline

When relevant, execute sequentially:

1. **Threat Modeling** (via `security-expert`):
   - STRIDE analysis for the topic
   - OWASP Top 10 exposure assessment
   - LLM/AI-specific security checks (if applicable)
   - PII and sensitive data handling review

2. **Compliance Impact** (via `compliance-governance`):
   - Regulatory requirements (GDPR, SOC 2, ISO 27001)
   - Audit logging requirements
   - Access control policy changes
   - Data classification implications

3. **Dependency & Supply Chain** (via `dependency-auditor`):
   - New dependency CVE assessment
   - Supply chain risk analysis
   - License compliance

4. **Risk Assessment** (via `kwp-operations-risk-assessment`):
   - Severity x likelihood matrix
   - Residual risk after mitigations
   - Incident response readiness

5. **Security Pattern Discovery** (via `workflow-miner`):
   - Discover security review workflow patterns from interaction history
   - Identify recurring security analysis sequences (e.g., threat model → audit → patch → verify)
   - Recommend automation for repetitive security validation tasks

6. **Content Security Validation** (via `semantic-guard`):
   - Runtime semantic validation of generated content and configurations
   - Prompt injection and adversarial input detection
   - Sensitive data flow tracking across system boundaries

7. **Compliance Alignment** (via `intent-alignment-tracker`):
   - Measure alignment between security policies and implementation compliance
   - Score per IA dimensions (Task Completion, Context Relevance, Efficiency, Side Effects)
   - Track compliance posture improvement trends

## Output Format

```markdown
# 보안 엔지니어 관점 분석: {Topic}

## 관련도: {N}/10
## 분석 일자: {YYYY-MM-DD}

## 보안 요약 (3-5 bullets)
- ...

## 위협 모델링 (STRIDE)
### Spoofing
### Tampering
### Repudiation
### Information Disclosure
### Denial of Service
### Elevation of Privilege

## 취약점 평가 (OWASP Top 10)
### 해당 항목
### 노출 수준 (Critical/High/Medium/Low)

## 컴플라이언스 영향
### 규제 요구사항
### 감사 로깅 변경
### 접근 통제 변경

## 데이터 보호
### 데이터 분류 변경
### 암호화 요구사항
### PII 처리 변경

## 의존성 & 공급망
### 신규 의존성 보안 상태
### CVE 노출
### 라이선스 호환성

## 리스크 매트릭스
| 리스크 | 심각도 | 가능성 | 잔여 리스크 |
|--------|--------|--------|-------------|

## 워크플로우 패턴 분석
### 발견된 보안 리뷰 패턴
### 자동화 기회

## 콘텐츠 보안 검증
### 시맨틱 검증 결과
### 프롬프트 인젝션 탐지
### 민감 데이터 흐름 추적

## 의도 정렬 평가
### IA 점수 (0-100)
### 보안 정책-구현 정렬
### 개선 필요 영역

## 보안 엔지니어 권고
### 필수 보안 조치 (배포 전)
### 권장 보안 강화
### 모니터링 & 알럿 설정
### 인시던트 대응 준비
```

## Error Handling

- If a composed skill is unavailable, skip that pipeline step and note the gap in the output
- If the topic is ambiguous, request clarification before scoring relevance
- If relevance score is borderline (4-5), include the score rationale in the output
- Always produce output in Korean regardless of the input language

## Example

**Input**: "New GPU inference service launch for enterprise customers"

**Relevance Score**: 8/10 (new API endpoint + model data + auth + enterprise compliance)

**Analysis highlights**:
- STRIDE: Spoofing HIGH (model API needs strong auth), Info Disclosure MEDIUM (model weights)
- OWASP: A01 Broken Access Control — model endpoint needs RBAC
- Compliance: Enterprise SLA requires SOC 2 Type II audit trail
- Data: Model weights classified as Confidential, inference inputs may contain PII
- Recommendation: Implement API auth + rate limiting before launch, add audit logging
