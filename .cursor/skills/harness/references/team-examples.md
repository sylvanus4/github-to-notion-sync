# Harness 구성 예시 (Cursor 환경)

## 예시 1: 코드 리뷰 에이전트 팀

### 도메인 분석 결과
- **목적:** 풀스택 코드 리뷰 (보안, 성능, 코드 품질, 테스트 커버리지)
- **패턴:** 팬아웃/팬인 + 취합
- **에이전트 수:** 4명 리뷰어 + 1명 취합자

### 팀 구성

| 에이전트 | subagent_type | model | 역할 |
|---|---|---|---|
| security-reviewer | generalPurpose | default | OWASP Top 10, 시크릿 탐지, 인젝션 |
| performance-reviewer | generalPurpose | fast | N+1, 메모리, 캐싱, 복잡도 |
| quality-reviewer | generalPurpose | fast | DRY, 네이밍, 에러 핸들링, 타입 |
| test-reviewer | generalPurpose | fast | 커버리지 갭, 엣지 케이스, 모킹 |
| review-synthesizer | generalPurpose | default | 4개 리뷰 취합, 우선순위 정렬 |

### 오케스트레이터 워크플로우

```
Phase 1: 준비
  - git diff 수집 → _workspace/00_diff.md
  - 변경 파일 목록 → _workspace/00_files.md

Phase 2: 병렬 리뷰 (4개 Task 동시 호출)
  ├── Task(security-reviewer, prompt="00_diff.md 보안 리뷰 → _workspace/01_security.md")
  ├── Task(performance-reviewer, prompt="00_diff.md 성능 리뷰 → _workspace/01_performance.md")
  ├── Task(quality-reviewer, prompt="00_diff.md 품질 리뷰 → _workspace/01_quality.md")
  └── Task(test-reviewer, prompt="00_diff.md 테스트 리뷰 → _workspace/01_test.md")

Phase 3: 취합
  Task(review-synthesizer, prompt="01_*.md 4개 파일 취합 → _workspace/02_review-summary.md")

Phase 4: 산출물
  - 02_review-summary.md를 최종 경로로 복사
  - (선택) Slack 포스팅
```

### 에이전트 스킬 예시 (security-reviewer)

```markdown
---
name: security-reviewer
description: "코드 변경 사항의 보안 취약점 리뷰. OWASP Top 10, 시크릿 노출, SQL 인젝션,
XSS, 인증/인가 우회를 점검한다. Use when the code-review orchestrator invokes this agent.
Do NOT use standalone — 오케스트레이터가 호출한다."
---

# Security Reviewer

## 역할
코드 diff에서 보안 취약점을 식별하고 severity 등급(Critical/High/Medium/Low)으로 분류한다.

## 입력
- `_workspace/00_diff.md`: git diff 내용

## 출력
- `_workspace/01_security.md`: 보안 이슈 목록 (severity 순)

## 프로토콜
1. diff를 파일 단위로 분석
2. 각 이슈에 파일:라인, 설명, 권장 수정 포함
3. False positive 가능성 명시
4. 이슈 없으면 "보안 이슈 없음" 명시 (빈 파일 금지)
```

---

## 예시 2: 문서 생성 파이프라인

### 도메인 분석 결과
- **목적:** 기술 문서 자동 생성 (아키텍처 분석 → 다이어그램 → 문서 → 검수)
- **패턴:** 순차 파이프라인 + 생성-검증 루프
- **에이전트 수:** 4명

### 팀 구성

| 에이전트 | subagent_type | model | 역할 |
|---|---|---|---|
| code-analyst | explore | fast | 코드베이스 구조 분석, 의존성 그래프 |
| diagram-generator | generalPurpose | default | Mermaid 다이어그램 생성 |
| doc-writer | generalPurpose | default | 마크다운 문서 작성 |
| doc-reviewer | generalPurpose | fast | 정확성, 완결성, 가독성 검수 |

### 오케스트레이터 워크플로우

```
Phase 1: 분석
  Task(code-analyst, subagent_type="explore",
       prompt="src/ 디렉토리 구조, 의존성, API 엔드포인트 분석 → _workspace/01_analysis.md")

Phase 2: 다이어그램
  Task(diagram-generator,
       prompt="01_analysis.md 기반 아키텍처 다이어그램 생성 → _workspace/02_diagrams.md")

Phase 3: 문서 작성 (생성-검증 루프, max 2회)
  Loop:
    Task(doc-writer,
         prompt="01_analysis.md + 02_diagrams.md 기반 문서 작성 → _workspace/03_doc.md")
    Task(doc-reviewer,
         prompt="03_doc.md 검수 → _workspace/03_review.md")
    if review.passed → break
    else → doc-writer에게 review 피드백 전달하여 재작성

Phase 4: 산출물
  - docs/ 경로에 최종 문서 저장
```

---

## 예시 3: 리서치 에이전트 팀 (복합 패턴)

### 도메인 분석 결과
- **목적:** 기술 주제 종합 리서치 (웹 검색 + 논문 + 코드 분석 → 보고서)
- **패턴:** 팬아웃(정보 수집) → 파이프라인(분석 → 보고서) + 검증
- **에이전트 수:** 5명

### 팀 구성

| 에이전트 | subagent_type | model | 역할 |
|---|---|---|---|
| web-researcher | generalPurpose | fast | 웹 검색, 블로그/문서 수집 |
| paper-scanner | generalPurpose | fast | 논문/학술 자료 탐색 |
| code-explorer | explore | fast | GitHub 코드, 오픈소스 구현 탐색 |
| analyst | generalPurpose | default | 3개 소스 종합 분석 |
| report-writer | generalPurpose | default | 최종 보고서 작성 |

### 오케스트레이터 워크플로우

```
Phase 1: 정보 수집 (병렬 3개)
  ├── Task(web-researcher, prompt="주제 웹 리서치 → _workspace/01_web.md")
  ├── Task(paper-scanner, prompt="관련 논문 탐색 → _workspace/01_papers.md")
  └── Task(code-explorer, prompt="관련 코드/구현 탐색 → _workspace/01_code.md")

Phase 2: 종합 분석 (순차)
  Task(analyst, prompt="01_web + 01_papers + 01_code 종합 분석 → _workspace/02_analysis.md")

Phase 3: 보고서 (순차)
  Task(report-writer, prompt="02_analysis.md 기반 보고서 작성 → _workspace/03_report.md")

Phase 4: 산출물
  - 03_report.md → output/{topic}-research-{date}.md
  - (선택) .docx 변환, Notion 업로드, Slack 포스팅
```

---

## 예시에서 추출한 패턴

### 파일명 컨벤션

```
_workspace/
├── 00_input/              # 원본 입력
├── 01_{agent}_{artifact}.md  # Phase 1 산출물
├── 02_{agent}_{artifact}.md  # Phase 2 산출물
├── 03_{agent}_{artifact}.md  # Phase 3 산출물
└── final/                 # 최종 산출물
```

### 공통 에러 핸들링

| 상황 | 전략 |
|---|---|
| 에이전트 1개 실패 | 1회 재시도 → 재실패 시 해당 결과 "N/A" 표기하고 진행 |
| 과반 실패 | 사용자에게 보고 (Slack/터미널) |
| 데이터 충돌 | 출처 병기, 삭제하지 않음 |
| 생성-검증 루프 교착 | max iteration 도달 시 마지막 결과 사용, 미통과 항목 명시 |

### Task 호출 프롬프트 템플릿

```
"당신은 {역할}입니다. {스킬 SKILL.md 내용을 참조하세요: .cursor/skills/{name}/SKILL.md}.

## 입력
{입력 파일 경로와 내용 설명}

## 작업
{구체적 지시}

## 출력
결과를 `{출력 경로}`에 Write 도구로 저장하세요.
{출력 형식 명세}

## 제약
- {금지 사항}
- {품질 기준}"
```
