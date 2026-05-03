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

## Safety Gates

### General
- NEVER auto-execute without user approval in Plan Mode
- Hermes checkpoint before destructive operations
- Skill security scan on externally-sourced skills
- Cost warning when plan exceeds $2.00 estimated

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
