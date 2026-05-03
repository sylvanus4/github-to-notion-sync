---
name: maestro-conductor
description: >-
  Long-running mission orchestrator with plan-approve-execute lifecycle,
  durable cross-session state, milestone-gated phases, handoff brief
  generation, and checkpoint save/restore. Extends mission-control with
  persistent multi-session mission state that survives context window resets.
  Use when the user asks to "create a mission", "long-running task",
  "multi-session project", "plan-approve-execute", "mission orchestrator",
  "handoff brief", "checkpoint save", "restore mission", "미션 생성", "장기 미션",
  "멀티세션 프로젝트", "핸드오프 브리프", "체크포인트", "미션 복원", "계획-승인-실행", "maestro-conductor",
  or wants durable cross-session orchestration with approval gates. Do NOT use
  for single-session task orchestration (use mission-control). Do NOT use for
  simple todo tracking (use TodoWrite). Do NOT use for code review pipelines
  (use deep-review or ship). Do NOT use for agent memory (use
  icarus-memory-fabric or memkraft). Korean triggers: "미션", "장기 프로젝트", "핸드오프",
  "체크포인트", "마에스트로".
---

# Maestro Conductor — Long-Running Mission Orchestrator

Durable mission orchestration for work that spans multiple agent sessions. While
`mission-control` handles single-session multi-skill dispatch, Maestro Conductor
persists mission state on disk so a fresh agent can pick up exactly where the
previous one left off.

Adapted from [ReinaMacCredy/maestro](https://github.com/ReinaMacCredy/maestro)'s
plan-approve-execute lifecycle.

---

## Core Concepts

### Mission Hierarchy

```
Mission (the overall goal)
 └─ Milestone (phase gate — must pass assertions before proceeding)
     └─ Feature (a concrete deliverable)
         └─ Assertion (a verifiable claim about the feature)
```

### Lifecycle State Machine

```
Mission:    draft → approved → executing → paused → completed
                                             ↘ failed
Milestone:  pending → active → passed → failed
Feature:    planned → in_progress → done → blocked
Assertion:  pending → passed → failed → skipped
```

Transitions are one-way (no backward jumps) except `paused ↔ executing`.

---

## Mission State Directory

All state lives under `.cursor/missions/{mission-id}/`:

```
.cursor/missions/{mission-id}/
├── mission.json          # Mission metadata + current status
├── milestones/
│   ├── 01-setup.json     # Milestone with embedded features + assertions
│   └── 02-core.json
├── checkpoints/
│   ├── cp-2026-04-22T09.json   # Full state snapshot
│   └── cp-2026-04-22T14.json
├── handoffs/
│   └── handoff-02.md     # Handoff brief for milestone 02
└── learnings.md          # Corrections and discoveries
```

---

## Workflow

### Phase 1: Mission Creation (Draft)

When the user describes a long-running goal:

1. **Decompose** into milestones (3-7 per mission)
2. For each milestone, define features and assertions
3. Write `mission.json` with status `draft`
4. Present the plan to the user for review

```json
{
  "id": "mission-abc123",
  "title": "Implement RBAC for AI Platform",
  "status": "draft",
  "created": "2026-04-22T09:00:00Z",
  "milestones": ["01-schema", "02-api", "03-ui", "04-e2e"],
  "current_milestone": null,
  "metadata": {
    "estimated_sessions": 4,
    "priority": "high"
  }
}
```

### Phase 2: Approval Gate

The mission MUST be explicitly approved before execution begins:

- User says "approve", "승인", "go ahead" → status becomes `approved`
- User says "reject", "거절" → mission stays `draft` for revision
- User says "modify" → update milestones and re-present

### Phase 3: Execution

For each milestone in order:

1. **Check prerequisites**: Previous milestone must be `passed`
2. **Activate milestone**: Set status to `active`
3. **Execute features**: Delegate to appropriate skills via Task tool
4. **Run assertions**: Verify each assertion (test passes, file exists, etc.)
5. **Gate check**: ALL assertions must pass to mark milestone `passed`
6. **Save checkpoint**: Auto-checkpoint after each milestone completion

If an assertion fails:
- Log the failure with details
- Offer: retry, skip (with justification), or pause mission

### Phase 4: Handoff Brief Generation

When a session is ending or context is running low:

1. Capture current state (active milestone, completed features, pending work)
2. Summarize key decisions made in this session
3. List blockers and open questions
4. Generate a structured handoff brief as markdown

```markdown
# Handoff Brief — Mission: {title}
## Session: {n} | Date: {date}

### Progress
- Milestone 01-schema: PASSED (3/3 assertions)
- Milestone 02-api: ACTIVE (2/5 features done)

### Current Context
- Working on: POST /roles endpoint
- Decision: Using Casbin for policy engine (ADR-042)
- Blocker: Need Redis for policy cache — not in local dev stack

### Next Session Should
1. Resolve Redis dependency (ask user or add to docker-compose)
2. Complete remaining 3 features in milestone 02-api
3. Run assertion: "All RBAC endpoints return 403 for unauthorized users"

### Files Modified This Session
- backend/internal/rbac/policy.go (new)
- backend/internal/rbac/handler.go (new)
- docker-compose.yaml (modified — added Redis)
```

### Phase 5: Checkpoint Save/Restore

**Auto-save** after each milestone completion.
**Manual save** when user says "checkpoint", "save state", "체크포인트 저장".
**Restore** when user says "restore mission", "load checkpoint", "미션 복원".

Checkpoint includes:
- Full `mission.json` with all milestone/feature/assertion states
- Git diff summary since mission start
- Last handoff brief
- Learnings accumulated so far

---

## Assertions

Assertions are the quality gate for milestones. Types:

| Type | Verification Method |
|------|-------------------|
| `test_passes` | Run specified test command, check exit code 0 |
| `file_exists` | Verify file path exists |
| `grep_match` | Search file for pattern match |
| `build_succeeds` | Run build command, check exit code 0 |
| `lint_clean` | Run linter, check zero errors |
| `manual` | Present to user for confirmation |
| `custom` | Run arbitrary shell command |

```json
{
  "id": "assert-rbac-403",
  "type": "test_passes",
  "description": "All RBAC endpoints return 403 for unauthorized users",
  "command": "go test ./internal/rbac/... -run TestUnauthorized",
  "status": "pending"
}
```

---

## Learnings and Corrections

During execution, capture discoveries that future sessions need:

- **Corrections**: "Don't use X because Y" — mistakes to avoid repeating
- **Learnings**: "The codebase uses pattern Z for..." — context for future agents

Stored in `learnings.md` within the mission directory and injected into
handoff briefs.

---

## Integration with Existing Skills

| Existing Skill | How Maestro Conductor Uses It |
|---|---|
| `mission-control` | Delegates single-milestone execution to mission-control's orchestration |
| `domain-commit` | Creates domain-split commits after each feature completion |
| `deep-review` | Runs code review as a milestone assertion |
| `recall` | Loads prior session context when restoring a mission |
| `icarus-memory-fabric` | Stores high-value decisions for cross-mission memory |
| `agent-behavioral-principles` | Injects principles into handoff briefs |

---

## Commands

| Command | Action |
|---------|--------|
| `maestro create` | Start a new mission from a goal description |
| `maestro approve` | Approve a draft mission for execution |
| `maestro status` | Show current mission state |
| `maestro checkpoint` | Save current state |
| `maestro restore` | Load a checkpoint |
| `maestro handoff` | Generate handoff brief for next session |
| `maestro pause` | Pause active mission |
| `maestro resume` | Resume paused mission |
| `maestro list` | List all missions |

---

## Example: Full Lifecycle

```
User: "I need to add multi-tenant support to the AI Platform backend.
       This will take several sessions."

Agent: [Creates mission with 5 milestones]
       1. Schema migration (add tenant_id columns)
       2. API middleware (tenant context extraction)
       3. Service layer (tenant-scoped queries)
       4. Admin API (tenant CRUD)
       5. E2E tests (cross-tenant isolation)

User: "Approve"

Agent: [Executes milestone 1, runs assertions, checkpoints]
       [Context getting low — generates handoff brief]
       "Mission paused. Handoff brief saved. Next session should
        start with 'maestro resume mission-abc123'"

--- New session ---

User: "maestro resume"

Agent: [Loads checkpoint, reads handoff brief, continues from milestone 2]
```
