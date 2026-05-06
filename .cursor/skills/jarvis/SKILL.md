---
name: jarvis
description: >-
  Meta-orchestrator that decomposes user goals into agent execution plans and
  (optionally) pursues them across turns via Goal Mode. Maintains a persistent
  wiki-style TODO backlog under state/todos/. Searches available skills,
  classifies task complexity, selects optimal agent composition (Hermes, role-*,
  orchestrators), produces a numbered dispatch plan with model routing and
  dependency ordering, and persists multi-turn objectives with
  pursuing/paused/achieved/unmet/budget-limited lifecycle states.
  Use when the user asks to "plan how to do X", "jarvis", "decompose this goal",
  "자비스", "goal mode", "pursue this until done", "jarvis goal", "jarvis plan",
  "자비스 계획", "자비스 목표", "long-running objective", "multi-turn goal",
  "자비스 TODO", "jarvis todo", or wants intelligent skill composition planning
  with optional persistent goal pursuit.
  Do NOT use for executing a single known skill (invoke it directly).
  Do NOT use for simple file edits or one-shot tasks.
  Do NOT use for the daily pipeline (use today).
  Korean triggers: "자비스", "목표 모드", "계획 세워줘", "장기 목표", "멀티턴 목표",
  "자비스 계획", "자비스 TODO"
---

# Jarvis — Meta-Orchestrator for Cursor

Decompose → Search → Classify → Plan → (optionally) Pursue.

---

## Layer 1: 직무 정의 (Job Definition)

| Dimension | Answer |
|-----------|--------|
| **Problem** | 복잡한 목표를 받았을 때, 어떤 스킬을 어떤 순서로 조합해야 하는지 결정하는 것 |
| **User** | 1인 AI 엔지니어가 1000+ 스킬 생태계를 효과적으로 활용해야 하는 상황 |
| **Success** | (1) 계획의 스킬 매칭 정확도 ≥ 80%, (2) Goal Mode 달성률 ≥ 70%, (3) 사용자가 계획 수정 없이 승인하는 비율 ≥ 60% |
| **Non-Goal** | 단일 스킬로 해결 가능한 작업 실행, 코드 직접 작성, 일상 파이프라인 운영 |

---

## Layer 3: 모델 선택 전략 (Model Selection & Fallback)

### Routing Table

| Task Type | Primary Model | Rationale |
|-----------|--------------|-----------|
| Exploration / file reading | `fast` (Haiku-tier) | 낮은 비용, 높은 처리량 |
| Implementation / code gen | `default` (Sonnet-tier) | 균형 잡힌 품질-비용 비율 |
| Architecture / multi-step reasoning | `opus` (Opus-tier) | 복잡한 의존성 분석에 필요 |
| Subagent quick lookup | `fast` | Task tool readonly 작업 |
| Goal Mode iteration | `default` | 비용-품질 밸런스 |
| Consolidation | `fast` → `default` escalation | 단순 패턴 추출 → 복잡 분석 |

### Fallback Chain

```
Primary Model (selected by task)
  ↓ timeout/rate-limit/error
Fallback 1: same-tier alternative (retry with backoff)
  ↓ 3 consecutive failures
Fallback 2: downgrade one tier (opus → default → fast)
  ↓ all tiers unavailable
Circuit Break: pause + notify user "모델 접근 불가 — 수동 개입 필요"
```

### Context Management

| Strategy | When Applied |
|----------|-------------|
| Window Packing | 계획 단계에서 관련 스킬 설명을 1-line 요약으로 압축 |
| Observation Masking | 이전 iteration 도구 출력은 요약만 유지 |
| Progressive Disclosure | Phase 2 검색 결과 중 top-3만 context에 포함 |

### Token Tracking

- 계획 생성: target ≤ 3,000 tokens
- Goal iteration: target ≤ 10,000 tokens per step
- Budget 80% 도달 시 경고 + 토큰 절약 모드 활성화

---

## Layer 4: 런타임 루프 — PTAO Cycle (Runtime Loop)

모든 Jarvis 실행은 Perceive-Think-Act-Observe 루프를 따른다.

```
    ┌─────────────────────────────────────────┐
    │              PTAO Cycle                   │
    │                                          │
    │   ┌──────────┐    ┌──────────┐          │
    │   │ Perceive │───→│  Think   │          │
    │   └──────────┘    └──────────┘          │
    │        ↑               │                 │
    │        │               ↓                 │
    │   ┌──────────┐    ┌──────────┐          │
    │   │ Observe  │←───│   Act    │          │
    │   └──────────┘    └──────────┘          │
    │                                          │
    │   Stops when Exit Condition fires        │
    └─────────────────────────────────────────┘
```

### Phase Definitions

| Phase | Jarvis Mapping | Inputs | Outputs |
|-------|---------------|--------|---------|
| **Perceive** | 사용자 입력 + 메모리 로드 + 도구 결과 수집 | user query, goal state, MemKraft recall, plan archive | 정제된 context package |
| **Think** | LLM reasoning + plan generation | context package + agent registry | 실행 계획 또는 다음 action 결정 |
| **Act** | 도구 호출 또는 subagent dispatch | plan step + selected skill | tool/skill 실행 결과 |
| **Observe** | 결과 검증 + exit condition 체크 | action output + evaluation criteria | continue/stop/escalate 판정 |

### Exit Conditions (루프 종료 조건)

| Condition | Trigger | Action |
|-----------|---------|--------|
| Success | 모든 evaluation criteria `check_cmd` 통과 | status → `achieved`, 결과 보고 |
| Budget Exhausted | consumed > budget (iters/tokens/cost) | status → `budget-limited`, 진행 상황 보고 |
| Deadline Passed | current_time > deadline | status → `budget-limited` |
| Circuit Break | 동일 action 3회 반복 (progress stall) | pause + 사용자에게 방향 전환 요청 |
| User Interrupt | 사용자가 "stop" / "pause" 명시 | status → `paused` |
| Unrecoverable Error | 모든 fallback 소진 | status → `unmet`, 에러 상세 보고 |

### Plan Mode vs Goal Mode 루프 차이

| Aspect | Plan Mode | Goal Mode |
|--------|-----------|-----------|
| PTAO 반복 횟수 | 1회 (single-shot) | multi-turn (budget 범위 내) |
| Act 범위 | 계획 생성만 (실행 없음) | 실제 skill dispatch |
| Observe | 사용자 승인 대기 | 자동 criteria 체크 + 사용자 확인 |
| State 지속 | 없음 (plan file로 저장) | JSON state file 갱신 |

---

## Layer 5: 메모리 전략 (Memory Architecture)

### Short-Term (세션 내)

| Source | Purpose | Access |
|--------|---------|--------|
| Goal state JSON | 현재 진행 중인 목표의 반복 기록 | `state/goals/<id>.json` |
| TODO backlog | 미완료 작업 대기열 | `state/todos/*.md` |
| Current plan | 이번 세션에서 승인된 실행 계획 | context window 내 보유 |

### Long-Term (세션 간)

| Source | Purpose | Access |
|--------|---------|--------|
| MemKraft | 과거 계획 패턴, 사용자 선호, 반복 교정 | `memkraft-ingest` / `ai-recall` |
| Plan archive | 모든 계획 이력 (승인/거부/완료) | `outputs/jarvis-plans/` |
| Consolidation log | 야간 자기 개선 결과 | `state/kb-intel-compile.log` |
| Skill performance | 스킬별 성공/실패 이력 | `intent-alignment-tracker` via recall |

### Memory Update Rules

- Goal 완료 시: 성공 패턴을 MemKraft HOT tier에 기록
- Goal 실패 시: 실패 원인 + 대안을 `tasks/lessons.md`에 추가
- 사용자 계획 수정 시: 수정 이유를 MemKraft에 기록 (선호 학습)
- Consolidation 실행 시: 최근 7일 패턴 → skill-autoimprove 후보 추출

---

## Layer 7: 인터페이스 전략 (Interface Strategy)

| Interface | Channel | Use Case |
|-----------|---------|----------|
| **Cursor Chat** (primary) | 직접 대화 | 계획 수립, 목표 추적, TODO 관리 |
| **Slack #효정-할일** | 결과 알림 | Goal 달성/실패 알림, 일일 진행 요약 |
| **Plan Files** | `outputs/jarvis-plans/` | 비동기 계획 공유, 이력 검색 |
| **Goal State** | `state/goals/*.json` | 세션 간 상태 복원, 외부 스크립트 연동 |
| **Cursor Automation** | scheduled trigger | Consolidation Mode 야간 실행 (향후) |

---

## Layer 8: 테스트 + 개선 루프 (Eval & Iteration)

### 품질 지표

| Metric | Measurement | Target |
|--------|-------------|--------|
| Plan Accuracy | 사용자가 수정 없이 승인한 비율 | ≥ 60% |
| Skill Match | 계획에서 선택한 스킬이 실제 적합했는지 (post-hoc 검증) | ≥ 80% |
| Goal Completion | Goal Mode에서 achieved 상태로 종료한 비율 | ≥ 70% |
| Token Efficiency | 계획 생성에 소비한 평균 토큰 수 | ≤ 3,000 |
| Iteration Waste | budget-limited로 끝난 Goal 비율 (과소 예산) | ≤ 20% |

### 개선 메커니즘

| Trigger | Action |
|---------|--------|
| 사용자가 계획을 3회 연속 수정 | 수정 패턴을 autoskill-extractor로 분석, Jarvis 자체 프롬프트 개선 |
| Goal 3회 연속 budget-limited | 기본 budget 상향 또는 분해 전략 재검토 |
| Skill mismatch 발생 | skill-guide 인덱스와 SRA retrieve 결과 비교 → 인덱스 갱신 |
| Consolidation 실행 | 주간 intent-alignment-tracker 스코어 리뷰, 하위 20% 패턴 개선 |
| 월말 리뷰 | Plan archive 전체 분석 → complexity 분류 정확도 + 소요 시간 트렌드 |

### Feedback Loop

```
Plan → Execute → User Feedback → MemKraft 기록 → Consolidation 분석 → Jarvis 개선
                      ↑                                              ↓
                      └──────── 다음 Plan에 학습 반영 ←──────────────┘
```

---

## Layer 9: 관측 가능성 (Observability)

모든 실행 단계를 측정하여 무엇이 작동하고 고장 나는지 파악한다.

### Trace 구조

| Layer | What to Log | Where |
|-------|-------------|-------|
| **Plan** | goal text, decomposition count, skill candidates, selected skills, classification result | Plan archive frontmatter |
| **Dispatch** | agent name, subagent type, model tier, input size (chars), start timestamp | Goal state `iterations[]` |
| **Execution** | skills_used[], data_sources[], pipeline pattern, tool calls count, tokens consumed, elapsed_ms, exit status | Goal state `iterations[]` |
| **Result** | output artifact paths, verification pass/fail, user approval/rejection | Goal state + MemKraft |

### 핵심 지표 (Metrics)

| Metric | Formula | Alert Threshold |
|--------|---------|-----------------|
| **Plan Latency** | plan_end_ts - request_ts | > 30s (warn) |
| **Skill Hit Rate** | approved_skills / total_planned_skills | < 70% (trigger reindex) |
| **Token Cost per Goal** | sum(iteration.tokens) * model_rate | > $3.00 (budget warning) |
| **Error Rate** | failed_iterations / total_iterations | > 30% (pause + notify) |
| **Goal Velocity** | achieved_goals / calendar_days | Trend 하락 시 consolidation |
| **Iteration Efficiency** | useful_actions / total_iterations | < 50% (decomposition 재검토) |

### Audit Trail

모든 Goal Mode 실행은 불변 감사 로그를 유지:

```json
// state/goals/<id>.json → iterations[] entry
{
  "iter": 3,
  "ts": "2026-05-04T10:23:00+09:00",
  "agent": "rr-solopreneur-researcher",
  "action": "dispatch role-researcher",
  "skills_used": ["parallel-web-search", "kb-ingest", "defuddle"],
  "data_sources": ["web:google", "KB:competitive-intel"],
  "pipeline": "Sequential(collect -> analyze -> persist)",
  "model": "default",
  "tokens_in": 1200,
  "tokens_out": 3400,
  "elapsed_ms": 8500,
  "result": "success",
  "artifacts": ["outputs/founder-pipeline/researcher-report.md"],
  "check_results": {"C1": true, "C2": false}
}
```

### Circuit Breaker

| Condition | Action |
|-----------|--------|
| 3 consecutive iteration failures | Goal 자동 pause + Slack 알림 |
| Token cost 80% budget 도달 | 경고 메시지 + 남은 예산으로 달성 가능 여부 재평가 |
| Same skill 2회 연속 실패 | 대체 스킬 탐색 (SRA fallback) |
| Deadline 24h 이내 + < 50% criteria met | 사용자에게 scope 축소 제안 |

### 대시보드 출력

`jarvis goal status` 실행 시 observability 요약 포함:

```
Goal: goal-2026-05-04-lead-magnet | Status: pursuing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Progress: 2/3 criteria met | Iter: 4/10 | Budget: $2.10/$5.00
Token: 180K/500K | Elapsed: 2h 15m | Error rate: 0%
Last action: role-copywriter (success, 45s, 12K tokens)
  Agent: rr-solopreneur-content
  Skills: content-graph-produce, hook-generator, edit-article
  Data: KB:content-library, web:competitor-blogs
  Pipeline: Sequential(plan -> draft -> edit-loop -> distribute)
Next suggested: role-builder
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Plan** | `jarvis plan <goal>` | Single response: numbered plan with skill assignments. No execution. |
| **Goal** | `jarvis goal <objective>` | Multi-turn pursuit. Persists state, evaluates criteria each iteration. |
| **TODO** | `jarvis todo [add\|list\|done\|drop]` | Wiki-style task backlog in `state/todos/`. |
| **Consolidation** | `jarvis consolidate` | Specialized Goal Mode for overnight pattern review and skill/memory updates. |

Default (no sub-command): Plan Mode.

---

## Agent Registry

### Tier 1 — Hermes (Self-Improvement & Safety)

| Agent | Skill Path | Purpose |
|-------|-----------|---------|
| Checkpoint | `hermes-checkpoint-rollback` | Shadow git snapshots before destructive ops |
| Skill Guard | `hermes-skills-guard` | Security scan for externally-sourced skills |
| Skill Evolver | `hermes-skill-evolver` | Population-based SKILL.md optimization |
| MoA | `hermes-mixture-of-agents` | Multi-model consensus for high-stakes decisions |

### Tier 2A — Executive Perspectives

| Agent | Skill | Perspective |
|-------|-------|-------------|
| CEO | `role-ceo` | Strategic impact, market positioning |
| CTO | `role-cto` | Architecture, tech debt, SLO |
| CSO | `role-cso` | Market sizing, GTM, scenario planning |
| PM | `role-pm` | PRD, sprint impact, OKR alignment |
| Sales | `role-sales` | Sales enablement, battlecards |
| Security | `role-security-engineer` | STRIDE, OWASP, compliance |
| UX | `role-ux-designer` | UX impact, accessibility |
| Developer | `role-developer` | Implementation complexity, test coverage |
| Finance | `role-finance` | Financial impact, ROI |
| HR | `role-hr` | Org impact, hiring needs |
| Data Sci | `role-data-scientist` | ML impact, data quality |
| Trading | `role-trading-expert` | Market impact, strategy validation |

Dispatch via: `role-dispatcher --mode=executive`

### Tier 2B — Founder Pipeline (Sequential)

| Step | Agent | Skill | Gate |
|------|-------|-------|------|
| 1 | Researcher | `role-researcher` | P1 severity ≥ 28/35 |
| 2 | Strategist | `role-strategist` | Winner AVG ≥ 7.0/10 |
| 3 | Copywriter | `role-copywriter` | F-K ≤ 7 + exact-3 bullets |
| 4 | Builder | `role-builder` | P0 3개 (이메일/CTA/모바일 fold) |
| 5 | Marketer | `role-marketer` | 30/60/90 plan + Day 0 스냅샷 |

Dispatch via: `role-dispatcher --mode=founder`

### Tier 3 — Orchestrators

| Agent | Skill | Pattern |
|-------|-------|---------|
| Mission Control | `mission-control` | Multi-skill decomposition |
| Engineering | `engineering-harness` | Fan-out/fan-in code review |
| Content | `content-production/coordinator` | Pipeline + editor gate |
| Research | `research-report/coordinator` | Pipeline + review loop |
| Incident | `incident-response/coordinator` | Severity routing |
| Strategic Intel | `strategic-intel/coordinator` | Fan-out + synthesis |
| Sales Deal | `sales-deal/coordinator` | Parallel research + proposal |
| Meeting Intel | `meeting-intel/coordinator` | Parallel extraction |
| Knowledge | `knowledge-builder/coordinator` | Pipeline + gap-fill |

### Tier 4 — Specialists (select by domain)

Categories: Frontend, Backend, Infra, Trading, Research, Content, Automation, Knowledge Base, Patent, MSP, Marketing, Sales, Legal, HR, Finance, Ops, Design.

Use `skill-recommender` or `skill-guide` to find the right specialist.

---

## Workflow (5 Phases)

### Phase 1: Decompose

Break the goal into 2-7 sub-goals. Each sub-goal has:
- Clear success criterion (measurable, external if possible)
- Estimated complexity: S/M/L/XL
- Dependencies on other sub-goals

### Phase 2: Search

For each sub-goal, find the best-fit skill:
1. Check Agent Registry above (Tier match)
2. Run `python3 scripts/sra/retrieve.py --top-k 5 "<keywords>"` for BM25 search
3. If no match → recommend `generalPurpose` subagent with explicit instructions

### Phase 3: Classify

| Dimension | Assessment |
|-----------|-----------|
| Complexity | S (1 skill) / M (2-3 skills) / L (orchestrator) / XL (multi-orchestrator) |
| Risk | Low (read-only) / Med (writes files) / High (external APIs, money) |
| Model Tier | fast (exploration) / default (implementation) / opus (architecture) |
| Parallelism | Sequential / Parallel / Mixed |

### Phase 4: Plan

Output a numbered dispatch plan:

```
## Execution Plan: <Goal Title>

### Phase 1: <Name> [parallel|sequential]
1. **<Skill>** — <task description>
   - Model: default | Input: <what> | Output: <what>
2. **<Skill>** — <task description>
   - Model: fast | Depends: #1

### Phase 2: <Name>
3. **<Skill>** — <task description>
   - Model: opus | Input: outputs of #1, #2

### Verification
- [ ] <criterion 1>
- [ ] <criterion 2>

### Risk Assessment
- <risk 1>: <mitigation>
```

### Phase 5: Validate

- Present plan to user for approval before execution
- If Goal Mode: proceed to goal lifecycle after approval
- If Plan Mode: stop here (user executes manually or says "go")

---

## Goal Mode

### Lifecycle States

```
[created] → [pursuing] → [achieved]
                ↓              ↑
           [paused]      (criteria met)
                ↓
         [budget-limited]
                ↓
            [unmet]
            [cleared]
```

### State File

Persisted at: `.cursor/skills/jarvis/state/goals/<goal-id>.json`

```json
{
  "id": "goal-YYYY-MM-DD-<slug>",
  "objective": "...",
  "status": "pursuing",
  "mode": "live",
  "created_at": "ISO8601",
  "updated_at": "ISO8601",
  "budget": {
    "max_iters": 10,
    "max_tokens": 500000,
    "max_cost_usd": 5.0,
    "deadline": "2026-05-04T00:00:00+09:00"
  },
  "consumed": {
    "iters": 0,
    "tokens": 0,
    "cost_usd": 0.0
  },
  "evaluation_criteria": [
    {"id": "C1", "desc": "...", "check_cmd": "test -f outputs/report.md"},
    {"id": "C2", "desc": "...", "check_cmd": null}
  ],
  "iterations": [],
  "plan": "..."
}
```

### Iteration Loop (Cursor Adaptation)

Cursor lacks Claude Code's `/loop` and `ScheduleWakeup`. Goal Mode works via:

1. **Manual continuation**: After each iteration, Jarvis reports progress and suggests next step. User approves continuation.
2. **Evaluation script**: Run `python3 .cursor/skills/jarvis/hooks/goal-continuation.py [goal-id]` to check criteria and budget.
3. **State persistence**: Each iteration updates the JSON state file.

Per-iteration workflow:
1. Run `goal-continuation.py` to get status
2. If `status == "pursuing"`: execute the smallest useful action
3. Update state JSON (iterations array, consumed counters)
4. Report to user with progress summary
5. If `status == "achieved"` or `status == "budget-limited"`: report final status and stop

### Budget Defaults

| Parameter | Default | Override |
|-----------|---------|---------|
| `max_iters` | 10 | `--iters N` |
| `max_tokens` | 500,000 | `--tokens N` |
| `max_cost_usd` | 5.00 | `--cost N` |
| `deadline` | none | `--deadline ISO` |

### Evaluation Criteria Rules

- Every goal MUST have ≥1 criterion with `check_cmd` (external verification)
- `check_cmd` runs in repo root, must exit 0 for pass
- LLM self-assessment alone is insufficient (overconfidence risk)
- Example check_cmds: `test -f <path>`, `grep -q <pattern> <file>`, `python3 -c "..."`, `make test`

---

## TODO Mode

Lightweight task backlog at `.cursor/skills/jarvis/state/todos/`.

### Commands

| Command | Action |
|---------|--------|
| `jarvis todo add <task>` | Create `{date}-{slug}.md` |
| `jarvis todo list` | Show all open items |
| `jarvis todo done <id>` | Mark complete |
| `jarvis todo drop <id>` | Archive without completing |
| `jarvis todo promote <id>` | Convert to Goal Mode objective |

### TODO File Format

```markdown
---
id: todo-2026-05-03-fix-auth
status: open
priority: high
created: 2026-05-03T10:00:00+09:00
source: session
---
# Fix auth token refresh

Token refresh fails after 30min idle. Reproduce: login → wait 35min → API call.
```

---

## Consolidation Mode

`jarvis consolidate` — overnight self-improvement cycle:

1. Scan recent agent transcripts (last 24h)
2. Extract recurring patterns → candidate skills
3. Update MEMORY.md with new learnings
4. Run `autoskill-evolve` on high-frequency patterns
5. Update `skill-guide` documentation
6. Report what changed

Budget: max_iters=5, max_cost_usd=3.0

---

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

## Safety Gates (Guardrails Layer)

### Input Filter (요청 사전 정제)
- 사용자 입력에서 prompt injection 패턴 탐지 (semantic-guard 연동)
- 비정상적으로 긴 입력 (>10,000 chars) 경고 + 요약 요청
- 금지된 작업 키워드 감지: secrets export, credential dump → 즉시 차단 + 안내

### Output Check (결과 사후 검증)
- 계획 내 skill 이름이 실제 존재하는지 검증 (registry miss → 경고)
- Goal Mode 결과에 placeholder/stub 출력 감지 → 재실행 요청
- 비용 추정 > budget의 120% → 실행 전 사용자 확인 강제
- 외부 API 호출 결과의 에러 코드(4xx/5xx) → 자동 retry 또는 fallback 경로

### Human Gate (고위험 작업 승인)
- NEVER auto-execute without user approval in Plan Mode
- Hermes checkpoint before destructive operations
- Skill security scan on externally-sourced skills
- Cost warning when plan exceeds $2.00 estimated
- 외부 서비스 호출 (Slack 포스팅, email 전송, git push) → 명시적 승인 필요

### Circuit Breaker (반복 실패 차단)
- 동일 skill 3회 연속 실패 → 해당 skill 비활성화 + 대안 제시
- 동일 Goal iteration에서 progress 0% 연속 2회 → 자동 pause + 사용자에게 방향 전환 요청
- Model fallback chain 전부 소진 → 전체 실행 중단 + 알림

### Goal Mode Specific
- `max_iters` hard limit (no override without explicit user approval)
- Budget overrun notification at 80% threshold
- Destructive commands (rm, DROP, force-push) require per-command approval
- Stale goal cleanup: goals untouched >7 days → auto-pause with notification
- Mandatory `check_cmd` for at least 1 evaluation criterion
- Checkpoint every 3 iterations

---

## Sub-Commands

```
jarvis plan <goal>           # Plan Mode (default)
jarvis goal <objective>      # Start Goal Mode
jarvis goal status           # Show active goal status
jarvis goal pause            # Pause active goal
jarvis goal resume           # Resume paused goal
jarvis goal clear            # Clear achieved/unmet goals
jarvis todo add <task>       # Add to backlog
jarvis todo list             # List open items
jarvis todo done <id>        # Complete item
jarvis todo promote <id>     # Promote to goal
jarvis consolidate           # Overnight self-improvement
```

---

## Integration Points

| Skill | How Jarvis Uses It |
|-------|-------------------|
| `skill-recommender` | Phase 2: find domain-fit skills |
| `skill-guide` | Phase 2: interactive discovery fallback |
| `sra-retriever` | Phase 2: BM25 skill search |
| `ralplan-execute-bridge` | Bridge plan → sp-executing-plans |
| `hermes-checkpoint-rollback` | Safety: snapshot before destructive ops |
| `role-dispatcher` | Dispatch Tier 2A (executive) or 2B (founder) |
| `omc-ralplan` | Alternative: 3-agent consensus planning |
| `mission-control` | Tier 3: multi-skill orchestration |

---

## Examples

### Example 1: Plan Mode

```
User: jarvis plan "ThakiCloud 블로그 시리즈 5편 기획 + 1편 작성"

Jarvis:
## Execution Plan: ThakiCloud 블로그 시리즈

### Phase 1: Research [parallel]
1. **pm-market-research** — TAM/competitor content analysis
   - Model: default | Output: market-context.md
2. **kb-query** — Query existing product-strategy wiki
   - Model: fast | Output: internal-context.md

### Phase 2: Strategy [sequential]
3. **content-graph-produce** — Generate 5-post series outline
   - Model: default | Input: #1, #2 | Output: series-outline.md

### Phase 3: Write [sequential]
4. **content-production/coordinator** — Write post #1
   - Model: default | Input: #3 | Output: blog-post-1.md

### Verification
- [ ] series-outline.md has 5 distinct topics with hooks
- [ ] blog-post-1.md passes content-graph quality score ≥ 80
```

### Example 2: Goal Mode

```
User: jarvis goal "Founder Pipeline으로 AI 코딩 교육 리드 매그넷 런칭"

Jarvis:
Goal created: goal-2026-05-03-founder-pipeline-lead-magnet
Budget: 10 iters, $5.00, 500K tokens
Evaluation criteria:
  C1: role-researcher 리포트 존재 (check_cmd: test -f outputs/founder-pipeline/researcher-report.md)
  C2: 랜딩 페이지 배포 (check_cmd: curl -s -o /dev/null -w "%{http_code}" https://...)
  C3: 이메일 시퀀스 5개 작성 완료 (check_cmd: test -f outputs/founder-pipeline/email-sequence.md)

Starting iteration 1...
→ Dispatching role-dispatcher --mode=founder (Step 1: Researcher)
```
