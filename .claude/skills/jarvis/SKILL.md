---
name: jarvis
description: >-
  Meta-orchestrator that decomposes user goals into agent execution plans
  and (optionally) pursues them across turns via Goal Mode (Codex /goal
  equivalent / Ralph Loop). Also maintains a persistent wiki-style TODO
  backlog under state/todos/ so that follow-up work surfaced during
  execution doesn't get lost. Searches available skills, classifies task
  complexity, selects optimal agent composition (Hermes, role-*,
  orchestrators), produces a numbered dispatch plan with model routing
  and dependency ordering, and persists multi-turn objectives with
  pursuing/paused/achieved/unmet/budget-limited lifecycle states.
---

# Jarvis

사용자의 목표를 받아 스킬 탐색 -> 복잡도 분류 -> 에이전트 실행 계획 수립까지 수행하는 메타 오케스트레이터.
직접 실행하지 않고, **어떤 스킬/에이전트를 어떤 순서로 어떤 모델에서 돌릴지** 계획을 세운다.
4가지 모드 지원:
- **Plan Mode** (기본): 단일 응답 안에서 계획 출력
- **Goal Mode** (Codex `/goal` 등가, Ralph Loop): 다중 턴 자동 추구
- **TODO Mode**: 백로그 항목 wiki-style 관리 (작업 트리거는 사람이)
- **Consolidation Mode**: 세션 학습 지식을 4-agent 검토 → 합의 → 자동 적용 (Goal Mode 특수형, 잠들기 전 한 줄 명령용)

## When to Use

- 목표가 단일 스킬로 해결 불가능할 때
- 어떤 스킬을 써야 할지 모를 때
- 복수 에이전트의 병렬/순차 조합이 필요할 때
- "이거 해줘"라는 모호한 요청을 구조화할 때
- **다중 턴/세션에 걸쳐 자동 추구할 영속 목표가 필요할 때 → Goal Mode**

## Do NOT Use

- 단일 스킬로 충분한 작업 (직접 호출이 빠름)
- 코드 구현 자체 (Jarvis는 계획만, 실행은 별도)
- 스킬 생성/수정 (write-a-skill, hermes-skill-evolver 직접 사용)
- DONE 기준 정의 불가능한 모호한 목표 (Goal Mode -> 무한루프 위험)

## Agent Registry

### Tier 1: Hermes (자기개선/안전)

| Skill | 역할 | 비용 |
|-------|------|------|
| `hermes-checkpoint-rollback` | 파괴적 작업 전 스냅샷 | 무료 |
| `hermes-skills-guard` | 외부 스킬 보안 스캔 | 낮음 |
| `hermes-skill-evolver` | 스킬 품질 최적화 (3라운드 진화) | 중간 |
| `hermes-mixture-of-agents` | 다중 LLM 합의 (고위험 판단) | $0.15-8.00 |
| `skill-curator` | 스킬 lifecycle 관리/통합/정리 | 낮음 |

### Tier 2A: Executive Perspectives (다각도 의사결정 분석)

기성 조직의 *대형 결정*에 대한 다각도 평가용. 입력: 결정/제안. 출력: 관점별 분석.

| Skill | 관점 |
|-------|------|
| `role-ceo` | 전략/시장/투자 |
| `role-cto` | 아키텍처/기술부채/SLO |
| `role-pm` | PRD/스프린트/OKR |
| `role-developer` | 구현 복잡도/테스트 |
| `role-security-engineer` | STRIDE/OWASP/컴플라이언스 |
| `role-finance` | ROI/예산/감사 |
| `role-ux-designer` | UX/접근성/디자인시스템 |
| `role-cso` | GTM/경쟁/시장규모 |
| `role-sales` | 세일즈 이네이블먼트/파이프라인 |
| `role-hr` | 조직/채용/변화관리 |
| `role-data-scientist` | 데이터파이프라인/ML |
| `role-trading-expert` | 시장환경/기술분석/리스크 |
| `role-dispatcher` | Tier 2A 12개 역할 일괄 디스패치 (mode=executive) |

### Tier 2B: Founder Pipeline (제로→MRR 실행 라인)

Mike Koenigs / Greg Isenberg 식 lean-MVP 파이프라인. 검증되지 않은 아이디어를
*검증된 페인 → 리드 매그넷 → 카피 → 라이브 페이지 → MRR* 까지 직선 운반.
Tier 2A와 달리 *분석가가 아니라 실행자* — 각 단계가 다음 단계의 입력을 생성.

| # | Skill | 역할 | 다음 단계 입력 |
|---|-------|------|---------------|
| 1 | `role-researcher` | 페인 검증 (Reddit/Amazon/G2 verbatim) | Pain Validation Report (P1 GO) |
| 2 | `role-strategist` | 페인 → 리드 매그넷 5안 + Winner Spec | Lead Magnet Winner Spec |
| 3 | `role-copywriter` | Sequential Prompt Chain (hook→bullets→landing) | Landing Copy (H1+3 bullets+CTA+body) |
| 4 | `role-builder` | Polish < Proof 라이브 1-pager + 이메일 캡처 | Live URL + Day 0 Snapshot |
| 5 | `role-marketer` | 30/60/90 organic-first 그로스 → MRR | Weekly KPI + 진단 게이트 |

**파이프라인 게이트**:
- 1→2: P1 severity ≥ 28/35 (GO 판정) 아니면 ICP 재검증
- 2→3: Winner AVG ≥ 7.0/10 아니면 페인 재선정
- 3→4: F-K ≤ 7, passive ≤ 1, exact-3 bullets 검증
- 4→5: P0 3개 (이메일 작동/단일 CTA/모바일 fold) 미통과 시 ship 거부
- 5 W4: conversion ≥ 5% 아니면 1로 회귀 (페인 재검증)

**Tier 2B 일괄 실행**: `role-dispatcher --mode=founder` (5개 스킬 순차 실행, 각 게이트 자동 평가)

### Tier 3: Orchestrators (실행 엔진)

| Skill | 용도 |
|-------|------|
| `ralplan-execute-bridge` | 합의 기반 계획 -> 배치 실행 |
| `maestro-conductor` | 장기 미션 (다세션, 마일스톤 게이트) |
| `coordinator` | 전략 인텔리전스 (시장+경쟁 분석) |
| `agency-agents-orchestrator` | 개발 파이프라인 (Dev-QA 루프) |
| `sprint-orchestrator` | 스프린트 단위 작업 관리 |

### Tier 4: Specialists (도메인 전문)

| Category | Examples |
|----------|----------|
| Research | `deep-research-pipeline`, `feynman`, `199-deep-research` |
| Knowledge | `kb-search`, `kb-compile`, `unified-knowledge-search` |
| Analysis | `competitive-analyst`, `strategic-planner`, `risk-assessor` |
| Development | `lead-programmer`, `backend-expert`, `frontend-expert` |
| Quality | `qa`, `code-reviewer-expert`, `security-review` |
| Content | `executive-briefing`, `summary-writer`, `draft-writer` |

## Workflow

```
User Goal (jarvis: ... | jarvis goal: ...)
  │
  ▼
Phase 1: Decompose ─── 목표를 sub-goals로 분해 (+SMART 기준 추출 if Goal Mode)
  │
  ▼
Phase 2: Search ────── 스킬 레지스트리 + skill-recommender 탐색
  │
  ▼
Phase 3: Classify ──── 복잡도/위험도 분류 (+budget 산정 if Goal Mode)
  │
  ▼
Phase 4: Plan ──────── 에이전트 실행 계획 생성 (+state 파일 if Goal Mode)
  │
  ▼
Phase 5: Validate ──── 안전 게이트 + 사용자 승인 (+budget 동의 if Goal Mode)
  │
  ├─ Plan Mode ──────── 사용자 직접 실행 또는 ralplan bridge 위임 (단일 응답 종료)
  │
  └─ Goal Mode ──────── pursuing 상태 진입
                          │
                          ▼
                       Continuation Loop:
                          ├─ Eval criteria 만족? → achieved (terminal)
                          ├─ Budget 소진? → budget-limited (사용자 선택)
                          ├─ 정체 3 iters? → unmet (terminal)
                          └─ 그 외 → next iter (CONTINUATION_PROMPT 주입)
```

### Phase 1: Decompose

사용자 목표를 atomic sub-goals로 분해한다.

1. 목표에서 **동사**를 추출: 분석/구현/배포/리뷰/조사/최적화/...
2. 각 동사를 독립 실행 가능한 단위로 분리
3. 의존관계 파악: A의 출력이 B의 입력이면 순차, 아니면 병렬

출력:
```
Sub-goals:
  G1: [동사] [대상] — 선행 조건 없음
  G2: [동사] [대상] — G1 출력 필요
  G3: [동사] [대상] — 선행 조건 없음
```

### Phase 2: Search

각 sub-goal에 적합한 스킬을 찾는다.

1. Agent Registry (위 테이블)에서 1차 매칭
2. 매칭 실패 시 `skill-recommender` 호출하여 기술 스택 기반 추천
3. 매칭 실패 시 `skill-guide` 호출하여 키워드 검색
4. 최종 매칭 실패 -> "범용 subagent (general-purpose)" 표기

각 sub-goal에 1-3개 후보 스킬 배정.

### Phase 3: Classify

전체 계획의 복잡도와 위험도를 분류한다.

#### Complexity Matrix

| Level | 기준 | 실행 엔진 |
|-------|------|----------|
| **Simple** | sub-goal 1-2개, 단일 도메인 | 직접 스킬 호출 (계획 불필요) |
| **Medium** | sub-goal 3-5개, 병렬 가능 | Jarvis plan -> 수동 실행 |
| **Complex** | sub-goal 6+개, 의존관계 복잡 | ralplan-execute-bridge 위임 |
| **Mission** | 다세션, 마일스톤 필요 | maestro-conductor 위임 |

#### Risk Assessment

| Signal | Risk Level | 자동 조치 |
|--------|-----------|----------|
| 5+ 파일 수정 예상 | MEDIUM | `hermes-checkpoint-rollback` 추가 |
| DB/인프라 변경 포함 | HIGH | 파괴적 작업 스캔, 수동 실행 강제 |
| 외부 스킬 사용 | MEDIUM | `hermes-skills-guard` 스캔 선행 |
| 아키텍처 결정 포함 | HIGH | `hermes-mixture-of-agents` 또는 `role-dispatcher` 추가 |
| 비용 $5+ 예상 | HIGH | 사용자 예산 동의 필수 |

### Phase 4: Plan

구조화된 실행 계획을 생성한다.

#### Plan Format

```markdown
# Jarvis Plan: {목표 요약}

Generated: {timestamp}
Complexity: {Simple|Medium|Complex|Mission}
Risk: {LOW|MEDIUM|HIGH}
Estimated cost: ~${X.XX}

## Pre-flight

| # | Action | Skill | Reason |
|---|--------|-------|--------|
| 0a | 체크포인트 생성 | hermes-checkpoint-rollback | 5+ 파일 변경 예상 |
| 0b | 외부 스킬 보안 스캔 | hermes-skills-guard | community 스킬 사용 |

## Execution Steps

| # | Sub-goal | Skill | Model | Mode | Depends |
|---|----------|-------|-------|------|---------|
| 1 | {G1 설명} | {skill-name} | haiku | parallel | — |
| 2 | {G2 설명} | {skill-name} | sonnet | parallel | — |
| 3 | {G3 설명} | {skill-name} | sonnet | sequential | 1,2 |
| 4 | {G4 설명} | {skill-name} | opus | sequential | 3 |

## Post-flight

| # | Action | Skill | Condition |
|---|--------|-------|-----------|
| P1 | 결과 종합 | executive-briefing | 항상 |
| P2 | Slack 공유 | — | 사용자 요청 시 |
| P3 | 스킬 학습 | hermes-inline-learning | 8+ 도구 호출 시 |
| P4 | 스킬 큐레이션 | skill-curator | 10+ 스킬 사용 또는 마지막 실행 7일+ 경과 |

## Decision Points

- Step 3 이후: {판단 필요 사항} -> 사용자 확인 후 진행
- Step 4 비용 $2+ 예상: MoA 사용 전 동의 필요
```

#### Model Routing Rules

| Task Type | Model | Rationale |
|-----------|-------|-----------|
| 파일 탐색, 목록 조회, 간단 검색 | `haiku` | 비용 최소 |
| 구현, 리뷰, 분석, 테스트 작성 | `sonnet` | 기본 작업 |
| 아키텍처 결정, 복잡 추론, MoA aggregation | `opus` | 고난이도 |

#### Parallelism Rules

- 의존관계 없는 sub-goals -> `parallel` (Agent tool 동시 호출)
- 출력-입력 연결 -> `sequential`
- 병렬 배치 최대 4개 (리소스 제한)
- role-* 스킬 병렬 시 role-dispatcher 사용 (자체 배치 관리)

### Phase 5: Validate

계획을 사용자에게 제시하고 승인을 받는다.

1. Plan Format 출력
2. 위험 요소 명시 (Risk Assessment 결과)
3. 예상 비용 명시
4. 사용자 선택지 제시:
   - **승인**: 계획대로 실행 시작
   - **수정**: 특정 step 변경 후 재계획
   - **위임**: ralplan-execute-bridge로 자동 실행
   - **고정 (Goal Mode)**: 다중 턴 영속 목표로 등록 후 자동 추구
   - **취소**: 중단

## Goal Mode (Persistent Multi-Turn Pursuit)

Codex CLI 0.128.0 `/goal` 등가. 철학: **"턴을 넘어 목표를 유지하라. 달성될 때까지 멈추지 마라."** (Ralph Loop, by Eric Traut)

Plan 모드는 **단일 응답 안에서 끝**난다. Goal 모드는 사용자 한 번 승인 후 **자동 반복 평가/실행**을 통해 목표 달성·예산 소진·사용자 중단까지 지속한다.

### Plan vs Goal 모드 비교

| 측면 | Plan 모드 (기본) | Goal 모드 |
|------|-----------------|----------|
| 실행 | 사용자 수동 | 자동 반복 (until done/limit) |
| 범위 | 단일 응답 | 다중 턴 / 다중 세션 |
| 종료 조건 | 계획 출력 | achieved / unmet / budget-limited / cleared |
| State | 무상태 | 영속 JSON state 파일 |
| 안전 | 사용자 게이트 | + 예산 한도 + max_iters + checkpoint |

### Lifecycle States (Codex와 동일 5상태)

```
   jarvis goal: X
        │
        ▼
    pursuing ◄──────── resume ────────┐
    │  │  │                            │
    │  │  └─► budget-limited (예산 소진) │
    │  │           │                    │
    │  │           └─► extend → pursuing │
    │  │                                │
    │  └────► paused ────────────────── ┘
    │
    ├─► achieved   (자체 평가: 완료 기준 충족)
    ├─► unmet      (자체 평가: 더 이상 진전 불가)
    └─► cleared    (사용자 명시 삭제)
```

| State | 의미 | 다음 액션 |
|-------|------|-----------|
| `pursuing` | 진행 중 | `/loop` ScheduleWakeup으로 다음 iter 자동 페이싱 |
| `paused` | 일시중지 | resume 받기 전까지 대기 (자동 진행 없음) |
| `achieved` | 달성 (terminal) | 종합 보고 후 state 보존 (감사용) |
| `unmet` | 미달성 (terminal) | 실패 회고 + 잔여 작업 목록 |
| `budget-limited` | 예산 소진 | 사용자에게 extend / 종료 / pause 선택 요청 |
| `cleared` | 사용자 삭제 (terminal) | state 파일 archive 이동 |

### Sub-commands

```
jarvis goal: <objective>            # 새 목표 시작 (pursuing 진입)
jarvis goal status [<id>]           # 현재 / 특정 목표 상태 조회
jarvis goal list                    # 모든 목표 일괄 조회 (상태별 그룹)
jarvis goal pause [<id>]            # paused 전이
jarvis goal resume [<id>]           # paused → pursuing
jarvis goal clear [<id>]            # 사용자 삭제 (terminal: cleared)
jarvis goal extend <id> --iters N --cost N  # budget-limited 후 예산 확장
jarvis goal evaluate [<id>]         # 즉시 자체 평가 강제 (achieved 여부)
```

`<id>` 미지정 시 가장 최근 `pursuing` 목표를 대상으로 한다.

### Budget Configuration

기본값:

| Field | Default | 의미 |
|-------|---------|------|
| `max_iters` | 20 | 반복 횟수 한도 (강제값 ≤ 100) |
| `max_tokens` | 100,000 | 누적 토큰 |
| `max_cost_usd` | 5.00 | 누적 비용 |
| `deadline` | created+12h | 절대 시각 |

사용자 지정 예시:
```
jarvis goal: <목표> --max-iters 30 --max-cost 10.00 --deadline 24h
```

예산 90% 도달 시 사용자에게 통지 (silent overrun 금지).

### State Storage

경로: `.claude/skills/jarvis/state/goals/<goal-id>.json` (skill base 하위, 런타임 생성)

스키마:
```json
{
  "id": "goal-2026-05-01-<slug>",
  "objective": "사용자 원문",
  "status": "pursuing",
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601",
  "budget": {
    "max_iters": 20,
    "max_tokens": 100000,
    "max_cost_usd": 5.00,
    "deadline": "ISO-8601"
  },
  "consumed": { "iters": 0, "tokens": 0, "cost_usd": 0.0 },
  "evaluation_criteria": ["기준1", "기준2"],
  "iterations": [
    {
      "n": 1,
      "started_at": "...",
      "skill": "...",
      "outcome": "...",
      "next_step": "...",
      "self_eval": { "progress_pct": 30, "blockers": [] }
    }
  ],
  "exit_reason": null,
  "exit_at": null
}
```

State 무결성: Goal Mode 진입 시 `hermes-checkpoint-rollback`이 자동으로 baseline 스냅샷 생성.

### Continuation Loop (`/loop` + ScheduleWakeup)

Stop hook 대신 `/loop` 자체 페이싱 방식으로 iteration을 구동한다.

#### 시작

사용자가 `/loop jarvis goal: <objective>` 실행 시 Jarvis가 goal state 생성 후
자동으로 첫 iteration을 실행한다.

#### 매 iteration 알고리즘

```
1. goal-continuation.py 실행 (CLI 유틸)
   python3 .claude/skills/jarvis/hooks/goal-continuation.py [goal-id]
   → JSON 출력: {status, criteria_met, criteria_remaining, budget_status, ...}

2. status == "achieved"?  → state 갱신, 보고, 루프 종료 (ScheduleWakeup 미호출)
3. status == "budget-limited"?  → BUDGET_PROMPT 출력, 루프 종료
4. progress 정체 (3 iter 연속 progress_pct 동일)?  → status = unmet, 루프 종료
5. status == "pursuing"?  → 작업 1개 실행 → state 갱신 → ScheduleWakeup 호출
```

#### ScheduleWakeup 페이싱 규칙

| 작업 유형 | delay | 이유 |
|-----------|-------|------|
| 파일 편집/생성 완료 | 60s | 즉시 다음 iter, 캐시 유지 |
| 외부 API/빌드 대기 | 270s | 캐시 5min TTL 직전, 1회 대기 |
| 긴 작업 (빌드/테스트) | 270s | 캐시 유지하면서 결과 대기 |

ScheduleWakeup 호출 시 `prompt`에 `/loop` 입력을 그대로 전달하여 다음 tick 재진입.

#### BUDGET_PROMPT (루프 종료 시 출력)

```
[GOAL HALTED: budget-limited]
원인: <max_iters | max_tokens | max_cost | deadline>
달성도: <progress_pct>% (자체 평가)
잔여 기준: <list>

사용자 선택지:
  1. jarvis goal extend <id> --iters N --cost N
  2. jarvis goal evaluate <id>
  3. jarvis goal pause <id>
  4. jarvis goal clear <id>
```

### Evaluation Criteria

목표 시작 시 SMART 기준 자동 추출 (Specific/Measurable/Achievable/Relevant/Time-bound).
**기준이 정량적이지 않으면 사용자에게 명시 요청** (Ralph Loop의 핵심 위험: DONE 신호 부재 → 무한 반복).

좋은 기준 예시:
- "tests/test_auth.py 100% 통과"
- "PRD v2 verification-report.md 모든 체크 PASS"
- "p95 latency < 200ms (최근 5분 윈도)"

나쁜 기준 예시 (거부):
- "잘 작동하면 됨"  ← 측정 불가
- "최선을 다해서"   ← 종결 신호 없음

#### External Verification Gate (LLM-as-judge over-confidence 방지)

각 criterion은 **외부 검증 명령** (`check_cmd`)을 가질 수 있다. Stop hook이
매 iter 종료 시 명령을 실행하고 종료코드 0이면 자동으로 `criteria_met`에
편입한다. LLM 자체 평가는 보조 신호일 뿐 — 명령이 진실원이다.

스키마 (확장):

```json
"evaluation_criteria": [
  {
    "id": "C1",
    "desc": "model-economics-analysis.md GPU lifecycle 섹션 존재",
    "check_cmd": "grep -q '## GPU Lifecycle' output/serverless-prd/model-economics-analysis.md"
  },
  {
    "id": "C2",
    "desc": "경쟁사 5개 이상 비교표",
    "check_cmd": "grep -cE '^\\| (Modal|Replicate|RunPod|Together|Fireworks)' output/serverless-prd/model-economics-analysis.md | awk '{exit ($1>=5)?0:1}'"
  },
  {
    "id": "C3",
    "desc": "verification-report 모든 체크 PASS",
    "check_cmd": "! grep -q '\\[ \\]' output/serverless-prd/verification-report.md"
  }
]
```

`check_cmd` 안전 가드:
- shell injection 패턴 (`rm -rf /`, `:(){`, `dd if=`, `curl|sh`) 자동 거부
- 길이 1000자 초과 거부
- subprocess timeout 15s
- working directory = repo root (절대경로 강제 안 함, 상대경로 OK)
- 종료코드 0 = PASS, 그 외 = FAIL

`check_cmd` 미지정 criterion은 **LLM 자체평가에 의존** (Ralph Loop의 약점,
정성 기준 불가피한 경우만 사용 권장).

**모든 criterion이 자동 검증 가능 + 모두 PASS** → status `achieved`로 자동 전이.
하나라도 정성 기준이 섞여 있으면 LLM이 명시적으로 `criteria_met` 갱신해야 함.

### CLI 유틸리티

`goal-continuation.py`는 Stop hook이 아닌 CLI 도구로 동작:

```bash
python3 .claude/skills/jarvis/hooks/goal-continuation.py [goal-id]
```

출력: JSON `{status, criteria_met, criteria_remaining, budget_status, continuation_prompt}`
종료코드: 0=pursuing(계속), 1=terminal(종료), 2=목표 없음

매 `/loop` iteration에서 Claude가 직접 호출하여 상태를 확인한다.
위험한 check_cmd (rm -rf /, fork bomb, dd, curl|sh) 자동 거부.

### Goal Mode 전용 Safety Gates

1. **No infinite loop**: `max_iters` ≤ 100 강제, 무한 ∞ 거부
2. **No silent overrun**: 예산 90% 도달 시 사용자 통지
3. **Destructive blocker**: DB drop / `git push --force` / `rm -rf` 감지 → 즉시 paused
4. **Stale cleanup**: 7일+ paused → 자동 cleared (사용자 통지 후)
5. **DONE 기준 필수**: evaluation_criteria 비어 있으면 시작 거부
6. **Checkpoint cadence**: 5 iter마다 자동 스냅샷 (rollback 가능)

### Codex `/goal` ↔ Jarvis Goal Mode 매핑

| Codex CLI 0.128.0 | Jarvis 등가 |
|-------------------|-------------|
| `/goal <objective>` | `jarvis goal: <objective>` |
| `/goal pause` | `jarvis goal pause` |
| `/goal resume` | `jarvis goal resume` |
| `/goal clear` | `jarvis goal clear` |
| 5 states (pursuing/paused/achieved/unmet/budget-limited) | 동일 5상태 + `cleared` (terminal) |
| `goals/continuation.md` 자동 주입 | Stop hook + CONTINUATION_PROMPT |
| `goals/budget_limit.md` 자동 주입 | BUDGET_PROMPT |
| 토큰 예산 소진 종료 | `budget.{max_iters,max_tokens,max_cost_usd,deadline}` |
| (없음) | `extend` / `evaluate` / `list` (확장) |

## Plan Output Persistence

모든 Plan Mode 출력은 자동으로 마크다운 파일로 저장된다.

### 저장 경로

```
outputs/jarvis-plans/{YYYY-MM-DD}/{HH}_{MM}-{slug}.md
```

| Component | Rule |
|-----------|------|
| `YYYY-MM-DD` | 계획 생성 시점의 로컬 날짜 |
| `HH_MM` | 계획 생성 시점의 24시간제 시:분 |
| `slug` | 목표 제목에서 kebab-case 변환, 영문+숫자+하이픈만, 최대 50자 |

### 파일 구조

```markdown
---
jarvis_plan: true
goal: "{원본 목표 텍스트}"
generated: "ISO-8601 timestamp"
complexity: "Simple|Medium|Complex|Mission"
risk: "LOW|MEDIUM|HIGH"
estimated_cost: "$X.XX"
status: "proposed|approved|executing|completed|cancelled"
---

# Jarvis Plan: {목표 요약}

(전체 계획 내용)
```

### 동작 규칙

1. Plan Mode 출력 생성 시 디렉토리를 자동 생성 (`mkdir -p`)
2. 동일 시각 slug 충돌 시 `-2`, `-3` 접미사 추가
3. Goal Mode의 plan 필드도 동일 경로에 저장 (goal state JSON과 별도)
4. 사용자가 계획을 승인/수정하면 `status` 필드를 갱신

---

## Safety Gates

1. **Never auto-execute**: Jarvis는 계획만 세움. 실행은 항상 사용자 승인 후.
2. **Hermes checkpoint**: 5+ 파일 변경 계획이면 Pre-flight에 자동 추가.
3. **Skills guard**: community/agent-created 스킬 포함 시 Pre-flight에 자동 추가.
4. **Cost ceiling**: 총 예상 비용 $10 초과 시 경고 + 대안 제시.
5. **Blast radius**: 15+ 파일 터치 시 배치 분할 권장.

## Examples

### Example 1: 단순 요청

```
User: "인증 모듈 리팩토링해줘"

Jarvis 판단:
  Complexity: Medium (구현 + 테스트 + 리뷰)
  Risk: MEDIUM (5+ 파일)

Plan:
  0a. hermes-checkpoint-rollback (스냅샷)
  1. role-developer (구현 복잡도 분석) — haiku
  2. role-security-engineer (보안 영향 분석) — haiku
  3. lead-programmer (구현) — sonnet, depends: 1,2
  4. qa (테스트 검증) — sonnet, depends: 3
  5. code-reviewer-expert (리뷰) — sonnet, depends: 4
```

### Example 2: 전략적 판단

```
User: "마이크로서비스 전환할지 모놀리스 유지할지 결정해야 해"

Jarvis 판단:
  Complexity: Complex (다각도 분석 + 합의)
  Risk: HIGH (아키텍처 결정)

Plan:
  1. role-dispatcher (12개 역할 전체 분석) — sonnet, parallel batch
  2. hermes-mixture-of-agents (3-model 합의) — opus, depends: 1
  3. executive-briefing (종합 보고) — sonnet, depends: 2
  4. decision-router (의사결정 Slack 라우팅) — haiku, depends: 3
```

### Example 3: 장기 미션

```
User: "AI 플랫폼 v2 전체 설계부터 배포까지"

Jarvis 판단:
  Complexity: Mission (다세션, 마일스톤)
  Risk: HIGH

Plan:
  → maestro-conductor로 위임 권장
  Milestone 1: 요구사항 분석 (role-pm, role-ceo, deep-research-pipeline)
  Milestone 2: 아키텍처 설계 (role-cto, role-developer, hermes-mixture-of-agents)
  Milestone 3: 구현 (agency-agents-orchestrator, Dev-QA 루프)
  Milestone 4: 배포 (sre-devops-expert, k8s-gitops-cicd)
```

### Example 4: Goal Mode (Codex /goal 등가)

```
User: jarvis goal: thakicloud serverless inference 단가 경쟁력 분석을
      GPU lifecycle 비용까지 포함하여 PRD 검증보고서 PASS까지 완성
      --max-iters 15 --max-cost 3.00 --deadline 6h

Jarvis 응답:
  Goal id: goal-2026-05-01-serverless-pricing
  Status: pursuing
  Evaluation criteria:
    - serverless-inference-pricing-unified.md GPU lifecycle 섹션 추가
    - 경쟁사 5+ 비교표 (Modal, Replicate, RunPod, Together, Fireworks)
    - verification-report.md 모든 체크 PASS
  Budget: 15 iters / $3.00 / 6h
  Initial plan (iter 1):
    - deep-research-pipeline (시장 가격 조사)

  ── iter 1 종료 ──
  outcome: 5개 경쟁사 가격 raw data 수집
  next_step: GPU lifecycle 비용 모델 작성
  consumed: 1/15 iters, $0.18, 12min
  → CONTINUATION_PROMPT 자동 주입, iter 2 시작

  ── iter 2 종료 ──
  outcome: lifecycle 비용 모델 v1 (감가상각/전력/냉각)
  next_step: 비교표 작성
  consumed: 2/15 iters, $0.41
  → CONTINUATION_PROMPT 자동 주입, iter 3 시작

  ...

  ── iter 8: achieved ──
  All evaluation criteria met.
  Total: 8/15 iters, $1.42, 3h12min
  보고서: executive-briefing 자동 호출
```

### Example 5: Goal Mode 예산 소진

```
User: jarvis goal status

Jarvis 응답:
  goal-2026-05-01-prd-rewrite [budget-limited]
    progress: 73% (3/4 criteria met)
    consumed: 20/20 iters, $4.85/$5.00
    잔여: verification-report.md 검증 PASS
    선택지:
      1. extend --iters 10 --cost 2.50
      2. evaluate (현재까지로 unmet 분류)
      3. pause (다음 세션에 재개)
      4. clear (포기)

User: jarvis goal extend goal-2026-05-01-prd-rewrite --iters 10 --cost 2.50

Jarvis: budget 확장 완료. status = pursuing. iter 21 시작.
```

## Invocation

### Plan Mode (기본, 단일 턴)

```
jarvis: {목표 설명}
jarvis plan: {목표}              # 계획만 (기본)
jarvis plan --roles: {목표}      # 역할 분석 포함
jarvis plan --deliberate: {목표} # 고위험 모드 (pre-mortem 추가)
jarvis replan: {수정 요청}       # 기존 계획 수정
```

### Goal Mode (다중 턴 영속)

```
jarvis goal: {목표} [--max-iters N] [--max-cost N] [--deadline 6h] [--auto-loop]
jarvis goal status [<id>]
jarvis goal list
jarvis goal pause [<id>]
jarvis goal resume [<id>]
jarvis goal clear [<id>]
jarvis goal extend <id> --iters N --cost N
jarvis goal evaluate [<id>]
```

`--auto-loop` 옵션 시 settings.json에 stop hook 등록 동의 요청 (자동 반복).
미지정 시 사용자가 매번 `jarvis goal resume`으로 다음 iter 진행 (안전 기본값).

### Consolidation Mode (Knowledge → Skills/Rules, 잠들기 전 한 줄용)

세션에서 학습된 비-자명 패턴들을 **밤새 자동 검토 + 적용**하는 Goal Mode 특수형. Codex `/goal`처럼 한 번 명령 → Stop hook 루프가 알아서 진행 → 아침에 결과.

#### Trigger phrases (외우기 쉽게)

다음 중 **무엇으로 호출해도 동일 동작**:

```
/jarvis 밤새 동작                 ← 가장 짧고 권장
/jarvis 밤새
/jarvis overnight
/jarvis consolidate
jarvis goal consolidate: last-session   ← 명시적 풀폼
```

전부 같은 기본값으로 매핑 (사용자 수정 불필요):
- `--max-iters 25`
- `--max-cost 4.00`
- `--deadline 8h` (= 다음날 아침)
- `--scope=skills` (룰은 token-diet 위반 위험으로 기본 제외)
- `--auto-apply` (apply까지 자동, sleep mode 의도 반영)

오버라이드가 필요하면 풀폼:
```
jarvis goal consolidate: <session_summary>
  [--max-iters N] [--max-cost N] [--deadline 6h]
  [--scope=skills|rules|both]
  [--auto-apply | --review-only]
```

#### 표준 워크플로 (각 iter)

```
[iter 1] Inventory     — Explore subagent: 패턴별 기존 커버리지 매핑
[iter 2] Architect     — Plan subagent: 적용 위치 후보 (skill/rule/hook/skip)
[iter 3] Dev review    — general-purpose: 회귀/실패 모드 식별
[iter 4] Curator       — general-purpose: lifecycle/중복/통합 검토
[iter 5] Consensus     — Jarvis 자체: 4개 결과 매트릭스 → 적용 항목 결정
[iter 6+] Apply        — 항목별 1개씩 Edit, syntax check, git diff 검증
[iter N-1] Trainset    — claude-code-trainset-distill (mechanical, 무 LLM):
                          extract_sft.py --since 1d → outputs/training-data/sft/
                          extract_preference.py --since 1d → .../preference/
                          (~1초, 비용 0)
[iter N] Verify        — check_cmd 외부 검증 + executive-briefing 보고
```

#### 표준 evaluation_criteria (자동 추출)

각 적용 항목마다 자동 생성:

```json
{
  "id": "C-pattern-{N}",
  "desc": "Pattern N applied to <target>",
  "check_cmd": "grep -q '<unique signature phrase>' <target file>"
}
```

추가 글로벌 criteria:
- `git diff --stat | wc -l > 0` — 실제 변경 발생
- 모든 수정된 .py syntax check pass (`python3 -m py_compile`)
- 모든 수정된 .sh syntax check pass (`bash -n`)
- `.claude/skills/*/SKILL.md` 의 frontmatter YAML 유효

#### 안전 게이트 (Goal Mode 기본 + 추가)

- **Pre-flight**: 자동 git checkpoint (commit hash 기록 → 실패 시 rollback)
- **Per-apply**: 한 번에 1 파일만 수정, syntax check 즉시
- **Cycle break**: 같은 패턴 3 iter 연속 적용 시도 실패 → skip + log
- **No new skills without approval**: 새 스킬 생성은 budget-limited 상태로 paused (사용자 명시 승인)
- **Token diet check**: `.claude/rules/`에 추가하기 전 토큰 영향 측정 (>2KB 추가 거부)

#### 운영 예시

```
User (잠들기 전, 23:50):
  jarvis goal consolidate: last-session
    --max-iters 25 --max-cost 4.00 --deadline 8h
    --scope=skills --auto-apply

Jarvis 응답:
  Goal id: goal-2026-05-02-consolidate-last-session
  Status: pursuing
  Patterns extracted: 16 (from this session's transcript + git diff)
  Initial inventory dispatch: Explore subagent (haiku)
  Stop hook 등록 — 매 턴 종료 시 자동 다음 iter 진행
  → CONTINUATION_PROMPT 자동 주입, iter 2 시작

User (다음날 08:00):
  jarvis goal status
  → goal-2026-05-02-consolidate-last-session [achieved]
    consumed: 14/25 iters, $2.31, 6h12min
    files modified: 5 (1 new file, 4 existing)
    patterns applied: 11/16 (5 skipped — already covered or unsafe)
    git: 3 commits on branch consolidate/2026-05-02
    report: output/jarvis-consolidate-2026-05-02/REPORT.md
```

### TODO Mode (백로그 wiki, LLM-friendly)

```
jarvis todo add: <title> [--priority=P1] [--cost=$X] [--time=Xmin] [--tags=...]
jarvis todo list [--status=open|in-progress|blocked|done] [--tag=...]
jarvis todo show <id>
jarvis todo done <id> [--note=...]
jarvis todo block <id>: <reason>
jarvis todo unblock <id>
jarvis todo archive <id>
jarvis todo promote <id>          # TODO → Goal (acceptance criteria → evaluation_criteria)
jarvis todo reindex                # INDEX.md 재생성
```

State 위치: `.claude/skills/jarvis/state/todos/` ([README](state/todos/README.md) 참조)

각 TODO는 frontmatter (id/status/priority/cost/tags/related_*) + 마크다운 본문 (Context / Acceptance criteria / Notes / History) 1파일. INDEX/BACKLOG는 큐레이션 뷰, 진실원은 개별 파일.

Plan/Goal 결과로 surface된 후속 작업은 TODO에 적재하여 잊혀지지 않게 한다 (예: feature flag 정리, monitor triage, doc 갱신).

## Integration Points

| Skill | Jarvis에서의 역할 |
|-------|-------------------|
| `skill-recommender` | Phase 2 스킬 탐색 보조 |
| `skill-guide` | Phase 2 키워드 검색 |
| `ralplan-execute-bridge` | Complex 이상 -> 실행 위임 |
| `maestro-conductor` | Mission급 -> 전체 위임 |
| `role-dispatcher` | 다각도 분석 일괄 디스패치 |
| `hermes-checkpoint-rollback` | Pre-flight 안전망 + Goal Mode 5-iter cadence |
| `hermes-skills-guard` | Pre-flight 보안 스캔 |
| `hermes-mixture-of-agents` | 고위험 판단 합의 |
| `hermes-skill-evolver` | Post-flight 스킬 품질 개선 |
| `skill-curator` | Post-flight 스킬 lifecycle 관리/정리 |
| `executive-briefing` | Post-flight 결과 종합 / Goal achieved 보고 |
| `decision-router` | Post-flight 의사결정 라우팅 |
| `loop` | Goal Mode `--auto-loop` 시 자체 페이싱 반복 |
| `update-config` | Goal Mode stop hook 등록 (settings.json) |

## References

- Codex CLI 0.128.0 Release: `/goal` command (OpenAI, 2026-04-30) — Eric Traut, Pyright 개발자
- Ralph Loop pattern: Geoffrey Huntley, "ignorant, persistent, optimistic"
- Simon Willison, "Codex CLI 0.128.0 adds /goal" (2026-04-30)
- GitHub openai/codex#20536: Goals lifecycle docs
