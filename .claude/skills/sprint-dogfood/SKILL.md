---
name: sprint-dogfood
description: >-
  Sprint에 Dogfooding 문화를 내장하는 4단계 파이프라인 오케스트레이터. Plan(가설 수립) → Execute(4관점 병렬
  QA) → Analyze(RICE 스코어링+이슈화) → Integrate(회고 통합+아카이브). 14개 기존 스킬을 조합하여 "내가 만든
  제품을 직접 사용해보는" 습관을 스프린트 프로세스에 정착시킴. GitHub Issue #3831 (제품 Dogfooding 문화 정착
  방안 수립)에서 도출. Use when the user asks to "sprint dogfood", "sprint
  dogfooding", "도그푸딩 스프린트", "제품 써보기", "내가 만든 제품 테스트", "sprint dogfood plan",
  "run dogfood", "dogfood execution", "dogfood analysis", "dogfood retro",
  "스프린트 도그푸드", "제품 직접 사용", "dogfood full pipeline", "dogfood 전체 파이프라인", or
  wants to embed product dogfooding into the sprint cycle. When user says just
  "dogfooding" or "도그푸딩" without sprint context, prefer qa-dogfood for one-off
  exploratory QA. Do NOT use for one-off exploratory QA without sprint context
  (use qa-dogfood). Do NOT use for Playwright E2E test suites (use
  e2e-testing). Do NOT use for code review without dogfooding intent (use
  deep-review). Do NOT use for general sprint retrospectives without dogfood
  data (use sprint-retro-facilitator). Do NOT use for customer feedback
  analysis without internal dogfood context (use customer-feedback-processor).
---

# Sprint Dogfood — 스프린트 Dogfooding 문화 파이프라인

내가 만든 제품을 직접 사용해보는 Dogfooding 문화를 스프린트에 내장하는
4단계 오케스트레이터. AI 플랫폼의 핵심 기능(워크로드 관리, 모델 서빙 등)을
팀원들이 실제 업무에 활용하면서 UX 개선점과 버그를 조기 발견합니다.

## 배경

> "계반묵기를 좀 해보자. 내가 만든 제품은 내가 좀 써보면서 제 업무에 잘 활용할 수 있는 수준인지"
> — 26주차 04 Sprint3 회고 (GitHub Issue #3831)

## 사용법

```
/sprint-dogfood plan                     # Phase 1: 가설 수립 (스프린트 시작)
/sprint-dogfood execute <APP_URL>        # Phase 2: 4관점 QA (스프린트 중, 반복 가능)
/sprint-dogfood analyze                  # Phase 3: 피드백 분석+이슈화 (스프린트 말)
/sprint-dogfood retro <NOTION_URL>       # Phase 4: 회고 통합 (회고 시)
/sprint-dogfood full <APP_URL>           # Phase 1-4 전체 실행 (데모/POC용)
```

## 필수 입력

| 파라미터 | 필수 | 설명 |
|----------|------|------|
| `mode` | Yes | `plan`, `execute`, `analyze`, `retro`, `full` 중 하나 |
| `APP_URL` | execute/full | 대상 앱 URL (예: `https://dev.thakicloud.io`) |
| `NOTION_URL` | retro | 스프린트 회고 Notion 페이지 URL |
| `--figma` | No | Figma URL 제공 시 design-review 활성화 |
| `--repo` | No | GitHub 리포지토리 (기본값: 현재 repo) |
| `--slack-channel` | No | 결과 포스팅 채널 (기본값: `#release-control`) |

## 출력 디렉토리

모든 산출물은 `outputs/sprint-dogfood/{YYYY-MM-DD}/` 에 저장됩니다.

```
outputs/sprint-dogfood/2026-04-21/
├── phase1-plan/
│   ├── dogfood-plan.md
│   └── hypotheses.md
├── phase2-execute/
│   ├── qa-dogfood-report.md
│   ├── expect-qa-results.md
│   ├── ux-audit.md
│   ├── design-review.md          # --figma 옵션 시
│   └── dogfood-findings.jsonl
├── phase3-analyze/
│   ├── classified.jsonl
│   ├── rice-scores.tsv
│   ├── themes.md
│   ├── dogfood-report.docx
│   ├── dogfood-dashboard.html
│   └── manifest.json
├── phase4-integrate/
│   ├── retro-summary.md
│   ├── github-issues.md
│   └── slack-thread.md
└── manifest.json
```

---

## Phase 1: Dogfood Planning (스프린트 시작)

**목적**: 이번 스프린트에서 어떤 기능을 dogfood 할지 결정하고 검증 가설 수립

### 실행 순서

1. **sprint-orchestrator로 대상 식별**
   - 현재 스프린트의 이슈/PR을 스캔하여 사용자 대면 기능 변경사항 식별
   - `dogfood:target` 라벨 후보 목록 생성
   - 신규 기능, UI 변경, 워크플로우 변경에 우선 순위 부여

2. **hypothesis-pm으로 가설 수립**
   - 각 대상 기능에 대해 Dogfood 가설 작성:
     - "우리 제품의 [기능X]가 [업무Y]에 활용 가능한 수준인가?"
     - "팀원이 [기능X]를 사용할 때 [문제Z] 없이 목표를 달성할 수 있는가?"
   - 최소 3개 가설, 각 가설에 검증 기준(성공/실패 조건) 명시
   - `outputs/sprint-dogfood/{date}/phase1-plan/hypotheses.md`에 기록

3. **Dogfood 계획서 생성**
   - 대상 기능 목록, 가설, 담당자, 검증 기준을 `dogfood-plan.md`로 통합
   - GitHub 이슈에 `dogfood:target` 라벨 자동 부여 (`gh issue edit --add-label`)

### Phase 1 산출물

```markdown
<!-- dogfood-plan.md 템플릿 -->
# 🐕 Sprint Dogfood Plan — {Sprint 이름}

## 대상 기능

| # | 기능 | 이슈/PR | 담당자 | 가설 |
|---|------|---------|--------|------|
| 1 | {기능명} | #{이슈번호} | {이름} | {가설} |

## 검증 기준

### 가설 1: {가설 제목}
- **성공 조건**: {조건}
- **실패 조건**: {조건}
- **검증 방법**: {qa-dogfood / expect-qa / ux-expert}

## 스케줄
- Plan 완료: {날짜}
- Execute 시작: {날짜}
- Analyze 예정: {날짜}
```

---

## Phase 2: Dogfood Execution (스프린트 중)

**목적**: 4가지 관점에서 병렬로 제품을 직접 사용해보며 피드백 수집

### 실행 순서

4개 QA 관점을 **workflow-parallel 패턴**으로 동시 실행합니다.
Task tool을 사용하여 독립적인 subagent로 각 QA를 병렬 실행합니다.

#### Agent A: qa-dogfood (탐색형 QA)
- 실제 사용자처럼 앱을 자유롭게 탐색
- `--tier standard` (약 8분) 또는 `--tier exhaustive` (약 15분) 사용
- Phase 1에서 식별된 대상 기능 페이지에 집중
- Health Score (0-100) 산출

#### Agent B: expect-qa (AI 적대적 QA)
- git diff 기반으로 변경된 코드에 대한 adversarial 테스트 생성
- `--scope branch` 또는 `--scope unstaged` 사용
- rrweb 세션 리플레이 캡처
- Pass/Fail 결과 + 재현 가능한 테스트 시나리오

#### Agent C: ux-expert (UX 감사)
- Nielsen 10가지 휴리스틱 평가
- WCAG 2.1 AA 접근성 감사
- 디자인 시스템(TDS) 일관성 검증
- 사용자 플로우 분석

#### Agent D: design-review (디자인 일치도 — 선택적)
- `--figma` 옵션으로 Figma URL 제공 시에만 실행
- 구현 코드 vs Figma 디자인 시각적 일치도 검증
- 기능 커버리지 + 품질 표준 점검

### 결과 통합

모든 Agent의 결과를 `dogfood-findings.jsonl`로 통합합니다:

```jsonl
{"source":"qa-dogfood","severity":"high","category":"bug","title":"...","description":"...","page":"/dashboard","timestamp":"..."}
{"source":"expect-qa","severity":"medium","category":"regression","title":"...","description":"...","page":"/workloads","timestamp":"..."}
{"source":"ux-expert","severity":"low","category":"accessibility","title":"...","description":"...","page":"/models","timestamp":"..."}
{"source":"design-review","severity":"medium","category":"visual-mismatch","title":"...","description":"...","page":"/settings","timestamp":"..."}
```

### Phase 2 산출물
- `phase2-execute/dogfood-findings.jsonl` — 통합 발견 사항
- `phase2-execute/qa-dogfood-report.md` — Health Score + 버그 목록
- `phase2-execute/expect-qa-results.md` — Pass/Fail + 세션 리플레이
- `phase2-execute/ux-audit.md` — 휴리스틱 + WCAG 결과
- `phase2-execute/design-review.md` — 디자인 일치도 (선택적)

---

## Phase 3: Feedback Analysis (스프린트 말)

**목적**: 수집된 피드백을 구조화하고 우선순위를 매기며 이슈화

### 실행 순서 (순차 — 각 단계의 출력이 다음 단계의 입력)

1. **feedback-miner로 토픽 클러스터링**
   - `dogfood-findings.jsonl`을 입력으로 사용
   - 토픽별 클러스터링 (버그, UX, 접근성, 디자인, 성능 등)
   - RICE 프레임워크 스코어링 (Reach × Impact × Confidence / Effort)
   - 산출: `classified.jsonl`, `rice-scores.tsv`, `themes.md`

2. **customer-feedback-processor로 리포트 생성**
   - feedback-miner 결과를 경영진용 보고서로 변환
   - `.docx` 리포트: 주요 발견사항, 테마별 분석, 우선순위 표
   - HTML 대시보드: 인터랙티브 시각화
   - 산출: `dogfood-report.docx`

3. **qa-with-blockers로 이슈 구조화**
   - RICE 상위 항목을 GitHub Issue로 변환 (최대 30개)
   - 블로커 DAG(의존성 그래프) 구축
   - 각 이슈에 `dogfood` 라벨 + 심각도 라벨 부여
   - Mermaid 다이어그램으로 블로커 관계 시각화

4. **visual-explainer로 대시보드 생성**
   - 스프린트 Dogfood 종합 대시보드 HTML 생성
   - 포함 항목:
     - Health Score 추이 (Phase 2 qa-dogfood 결과)
     - 카테고리별 발견 사항 분포
     - RICE 스코어 상위 10개 항목
     - 가설 검증 결과 (Phase 1 대비)
     - 블로커 DAG 시각화
   - 산출: `dogfood-dashboard.html`

### Phase 3 산출물
- `phase3-analyze/classified.jsonl` — 분류된 피드백
- `phase3-analyze/rice-scores.tsv` — RICE 우선순위
- `phase3-analyze/themes.md` — 테마 요약
- `phase3-analyze/dogfood-report.docx` — 경영진 리포트
- `phase3-analyze/dogfood-dashboard.html` — 팀 대시보드
- `phase3-analyze/manifest.json` — 파일 메타데이터

---

## Phase 4: Sprint Integration (회고 시)

**목적**: Dogfood 결과를 스프린트 회고에 통합하고 다음 스프린트에 반영

### 실행 순서

1. **sprint-retro-facilitator로 회고 퍼실리테이션**
   - Notion 회고 페이지 URL을 입력으로 제공
   - Dogfood 메트릭을 회고 데이터에 통합:
     - Health Score 추이
     - 가설 검증 결과 (성공/실패/미검증)
     - 주요 발견 사항 Top 5
   - 구조화된 토론 프롬프트 생성

2. **sprint-retro-to-issues로 액션 아이템 이슈화**
   - 회고에서 도출된 dogfood 관련 액션 아이템을 GitHub Issue로 생성
   - `dogfood` 라벨 + Project #5 연동
   - PM 다관점 분석 + 적대적 품질 비평 적용

3. **md-to-notion으로 결과 아카이빙**
   - 전체 Dogfood 결과를 Notion 서브페이지로 발행
   - 대시보드 HTML 링크 포함
   - 스프린트별 히스토리 추적 가능하도록 구조화

4. **Slack으로 팀 알림**
   - Slack MCP를 사용하여 지정 채널에 3-message thread 포스팅:
     - 메시지 1: 🐕 스프린트 Dogfood 요약 (Health Score, 가설 결과)
     - 메시지 2: 📊 대시보드 링크 + 주요 발견 사항 Top 5
     - 메시지 3: ✅ 액션 아이템 목록 (GitHub Issue 링크)

### Phase 4 산출물
- GitHub Issues — `dogfood` 라벨, Project #5 필드 설정
- Notion 아카이브 — 스프린트별 Dogfood 결과 페이지
- Slack thread — 3-message 요약 (지정 채널)

---

## 전체 실행 모드 (full)

`/sprint-dogfood full <APP_URL>` 실행 시 Phase 1-4를 순차적으로 실행합니다.

```
Phase 1 (plan)     → dogfood-plan.md 생성
    ↓
Phase 2 (execute)  → 4관점 병렬 QA 실행
    ↓
Phase 3 (analyze)  → 피드백 분석 + 이슈화
    ↓
Phase 4 (retro)    → 회고 통합 + 배포
```

full 모드에서는:
- Phase 4의 NOTION_URL이 없으면, 결과를 새 Notion 페이지로 자동 생성
- Slack 포스팅은 항상 수행
- 총 소요 시간: 약 30-45분

---

## 언어 규칙

- **모든 리포트**: 한국어로 작성
- **Slack 메시지**: 한국어로 작성
- **GitHub Issue**: 한국어 제목 + 영어 기술 세부사항
- **JSONL/TSV 데이터**: 영어 (기계 처리용)
- **Notion 페이지**: 한국어로 작성

---

## 스킬 조합 매트릭스

| Phase | 스킬 | 실행 방식 | 역할 |
|-------|-------|----------|------|
| 1 | `hypothesis-pm` | 순차 | Dogfood 가설 수립 |
| 1 | `sprint-orchestrator` | 순차 | 대상 기능 자동 식별 |
| 2 | `qa-dogfood` | 병렬 | 탐색형 QA (사용자 시점) |
| 2 | `expect-qa` | 병렬 | AI 적대적 QA (코드 변경) |
| 2 | `ux-expert` | 병렬 | UX 휴리스틱 + 접근성 |
| 2 | `design-review` | 병렬 (선택적) | Figma 일치도 검증 |
| 3 | `feedback-miner` | 순차 (1/4) | 토픽 클러스터링 + RICE |
| 3 | `customer-feedback-processor` | 순차 (2/4) | 경영진 리포트 |
| 3 | `qa-with-blockers` | 순차 (3/4) | 블로커 DAG 이슈화 |
| 3 | `visual-explainer` | 순차 (4/4) | 대시보드 HTML |
| 4 | `sprint-retro-facilitator` | 순차 | 회고 퍼실리테이션 |
| 4 | `sprint-retro-to-issues` | 순차 | 이슈 자동 생성 |
| 4 | `md-to-notion` | 순차 | Notion 아카이빙 |
| 4 | Slack MCP | 순차 | 팀 알림 |

---

## 참조

- **Origin**: [GitHub Issue #3831](https://github.com/ThakiCloud/ai-platform-webui/issues/3831) — 제품 Dogfooding 문화 정착 방안 수립
- **Sprint**: 26주차 04 Sprint3 회고에서 도출
- **Related Skills**:
  - `qa-dogfood` — 탐색형 브라우저 QA (이 스킬이 Phase 2에서 조합)
  - `expect-qa` — AI 적대적 QA (이 스킬이 Phase 2에서 조합)
  - `sprint-retro-to-issues` — 회고 → 이슈 파이프라인 (이 스킬이 Phase 4에서 조합)
