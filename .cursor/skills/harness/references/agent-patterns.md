# Agent Team Design Patterns (Cursor Adaptation)

## 실행 모드: Cursor의 Task 도구

Cursor에서 에이전트 팀은 `Task` 도구의 병렬/순차 호출로 구현한다.

### 병렬 팬아웃 (Agent Team 등가)

한 메시지에서 여러 Task를 동시 호출하면 병렬 실행된다:

```
[오케스트레이터] → 단일 메시지에서:
├── Task(subagent_type="generalPurpose", prompt="분석A → _workspace/01_a.md")
├── Task(subagent_type="generalPurpose", prompt="분석B → _workspace/01_b.md")
└── Task(subagent_type="generalPurpose", prompt="분석C → _workspace/01_c.md")
→ 모든 결과 파일 읽기 → 취합
```

**특징:**
- 병렬 실행으로 시간 절약
- 각 서브에이전트는 독립 컨텍스트
- 결과는 파일로 전달 (서브에이전트 간 직접 통신 불가)
- 최대 4개 동시 권장

### 순차 파이프라인 (Sub-agent 등가)

Task 호출 결과를 다음 Task의 입력으로 사용:

```
Phase 1: Task(analyst) → _workspace/01_analysis.md
    ↓ 결과 읽기
Phase 2: Task(builder, prompt="01_analysis.md 기반 구현") → _workspace/02_build.md
    ↓ 결과 읽기
Phase 3: Task(qa, prompt="02_build.md 검증") → _workspace/03_qa.md
```

### 모드 선택 의사결정 트리

```
1. 단일 에이전트로 충분한가?
   → YES: 단일 Task 호출.
   → NO: 계속.

2. 서브태스크 간 순차 의존이 있는가? (B가 A 결과 필요)
   → YES: 순차 Task 호출.

3. 독립 서브태스크가 있는가?
   → YES: 병렬 Task 호출 (한 메시지에 여러 Task).

4. 첫 결과 품질이 일관되게 부족한가?
   → YES: 순차 생성→검증 루프 추가.
```

---

## 아키텍처 유형별 Cursor 구현

### 1. 파이프라인 (Pipeline)

```
Task(분석, prompt="...") → 결과 읽기
Task(설계, prompt="분석 결과 기반...") → 결과 읽기
Task(구현, prompt="설계 결과 기반...") → 결과 읽기
Task(검증, prompt="구현 결과 기반...")
```

**Cursor 구현:** 순차 Task 호출. 각 Task는 이전 Task의 출력 파일을 읽도록 prompt에 경로 명시.

### 2. 팬아웃/팬인 (Fan-out/Fan-in)

```
단일 메시지에서 병렬 Task:
├── Task(전문가A, prompt="관점A 분석 → _workspace/01_a.md")
├── Task(전문가B, prompt="관점B 분석 → _workspace/01_b.md")
└── Task(전문가C, prompt="관점C 분석 → _workspace/01_c.md")
→ 오케스트레이터가 3개 파일 읽고 통합
```

**Cursor 구현:** 단일 메시지에 여러 Task 호출. 결과 파일 경로를 명시하여 오케스트레이터가 취합.

### 3. 전문가 풀 (Expert Pool)

```
오케스트레이터가 입력 분류 후 조건부 Task 호출:
if 보안_이슈 → Task(security-expert, ...)
if 성능_이슈 → Task(performance-expert, ...)
if 아키텍처_이슈 → Task(architecture-expert, ...)
```

**Cursor 구현:** 오케스트레이터가 입력 분석 후 해당 전문가의 Task만 호출.

### 4. 생성-검증 (Producer-Reviewer)

```
Loop (max 3회):
  Task(generator, prompt="생성 → _workspace/draft.md")
  → 결과 읽기
  Task(reviewer, prompt="draft.md 검증 → _workspace/review.md")
  → 결과 읽기
  if review.passed → break
  else → generator에게 review 피드백 포함하여 재생성
```

**Cursor 구현:** 순차 Task 루프. 최대 반복 횟수 설정 필수.

### 5. 감독자 (Supervisor)

```
오케스트레이터가 작업 목록 관리:
1. 전체 작업 분석 → TodoWrite로 작업 등록
2. 병렬 Task 호출 (batch 1)
3. 결과 수집 → 실패 작업 재할당
4. 병렬 Task 호출 (batch 2)
5. 반복
```

**Cursor 구현:** 오케스트레이터가 TodoWrite로 작업 추적, 배치별 병렬 Task 호출.

### 6. 계층적 위임 (Hierarchical Delegation)

```
Task(총괄, prompt="...")
  └→ 총괄 내부에서:
     Task(팀장A, prompt="...")
       └→ 팀장A 내부에서:
          Task(실무자A1, prompt="...")
          Task(실무자A2, prompt="...")
     Task(팀장B, prompt="...")
```

**Cursor 구현:** Task 내에서 추가 Task 호출 (중첩). 2단계 이내 권장 (깊이 증가 시 컨텍스트 손실).

---

## 복합 패턴

| 복합 패턴 | Cursor 구현 |
|---|---|
| 팬아웃 + 생성-검증 | 병렬 Task(생성) → 각 결과에 순차 Task(검증) |
| 파이프라인 + 팬아웃 | 순차 Task(분석) → 병렬 Task(구현) → 순차 Task(통합) |
| 감독자 + 전문가 풀 | 오케스트레이터가 분류 → 조건부 병렬 Task 호출 |

---

## subagent_type 선택

| Cursor subagent_type | 용도 | 비고 |
|---|---|---|
| `generalPurpose` | 범용 (웹 검색, 파일 읽기/쓰기) | 기본 선택 |
| `explore` | 코드베이스 탐색 (읽기 전용) | 빠르고 저렴 |
| `shell` | 셸 명령 실행 | Git, npm, Docker 등 |
| `best-of-n-runner` | 격리된 실험 | 별도 worktree에서 실행 |

### model 라우팅

| 에이전트 역할 | Cursor model | 이유 |
|---|---|---|
| 탐색/검색/간단 분류 | `model: "fast"` | 비용 절감 |
| 구현/분석/코드 생성 | 기본 모델 | 균형 |
| 아키텍처/복잡한 추론 | 더 높은 모델 | 복잡한 판단 |

---

## 에이전트 스킬 vs 오케스트레이터

| 구분 | 에이전트 스킬 | 오케스트레이터 스킬 |
|---|---|---|
| 역할 | 단일 전문 작업 수행 | 여러 에이전트를 조율 |
| 위치 | `.cursor/skills/{agent}/SKILL.md` | `.cursor/skills/{domain}-orchestrator/SKILL.md` |
| 호출 | Task 도구로 호출됨 | 사용자가 직접 트리거 |
| 크기 | 작은~중간 | 큰 (워크플로우 전체) |

---

## 오케스트레이터 템플릿

```markdown
---
name: {domain}-orchestrator
description: "{도메인} 에이전트를 조율하는 오케스트레이터. {트리거 키워드}."
---

# {Domain} Orchestrator

## 에이전트 구성

| 에이전트 | subagent_type | model | 역할 | 출력 경로 |
|---|---|---|---|---|
| {agent-1} | generalPurpose | fast | {역할} | `_workspace/01_{agent-1}_{artifact}.md` |
| {agent-2} | generalPurpose | default | {역할} | `_workspace/01_{agent-2}_{artifact}.md` |

## 워크플로우

### Phase 1: 준비
1. 사용자 입력 분석
2. `_workspace/` 폴더 생성
3. 입력 데이터를 `_workspace/00_input/`에 저장

### Phase 2: {주요 작업}

**실행 방식:** {병렬 | 순차 | 조건부}

{병렬인 경우}
단일 메시지에서 N개 Task를 동시 호출:

| 에이전트 | 입력 | 출력 |
|---|---|---|
| {agent-1} | {입력 소스} | `_workspace/01_{artifact}.md` |
| {agent-2} | {입력 소스} | `_workspace/01_{artifact}.md` |

### Phase 3: 통합
1. 모든 결과 파일 Read
2. 통합/검증
3. 최종 산출물 생성

## 데이터 흐름

```
입력 → [agent-1] → artifact-1 ─┐
                                ├→ [통합] → 최종 산출물
입력 → [agent-2] → artifact-2 ─┘
```

## 에러 핸들링

| 상황 | 전략 |
|---|---|
| 에이전트 1개 실패 | 1회 재시도 → 재실패 시 해당 결과 없이 진행 |
| 과반 실패 | 사용자에게 보고, 진행 여부 확인 |
| 데이터 충돌 | 출처 병기, 삭제하지 않음 |
```
