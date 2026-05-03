---
name: agent-behavioral-principles
description: >-
  Inject behavioral rules into agent prompts and score outputs against them
  with pass/fail gates. Register project-specific principles, compile guidance
  from corrections and learnings, and track principle effectiveness over time.
  Use when the user asks to "add a principle", "register behavioral rule",
  "score against principles", "principle gate", "check output compliance",
  "behavioral principles", "agent principles", "원칙 등록", "행동 원칙", "원칙 점수", "원칙
  게이트", "에이전트 원칙", "agent-behavioral-principles", or wants to enforce and
  track behavioral quality rules on agent outputs. Do NOT use for code linting
  or formatting rules (use linters directly). Do NOT use for prompt
  optimization (use prompt-architect). Do NOT use for general code review (use
  deep-review or simplify). Do NOT use for skill quality auditing (use
  skill-optimizer). Do NOT use for compliance governance (use
  compliance-governance). Korean triggers: "원칙", "행동 규칙", "에이전트 규칙", "원칙 점수",
  "게이트".
---

# Agent Behavioral Principles — Principle-Scored Agent Replies

Define behavioral rules that agents must follow, inject them into task prompts,
score every output against them, and use pass/fail gates to catch violations
before they ship.

Adapted from [ReinaMacCredy/maestro](https://github.com/ReinaMacCredy/maestro)'s
principles system.

---

## Why Principles

Skills tell agents WHAT to do. Principles tell agents HOW to behave while doing
it. Without principles, agents produce technically correct but behaviorally wrong
output — e.g., making changes without tests, skipping error handling, or
over-engineering simple tasks.

---

## Principle Structure

```yaml
# .cursor/principles/think-before-coding.yaml
id: think-before-coding
name: Think Before Coding
mode: gate          # "gate" = blocks output on failure; "advisory" = warns only
profile: all        # or: "backend", "frontend", "devops", etc.
rules:
  - "Read existing code before modifying it"
  - "State your approach in 1-2 sentences before writing code"
  - "Identify affected files before making changes"
scoring:
  weight: 1.0       # relative importance (0.0 – 1.0)
  threshold: 0.7    # minimum score to pass (gate mode only)
```

### Modes

| Mode | Behavior |
|------|----------|
| `gate` | Output is BLOCKED if principle score falls below threshold |
| `advisory` | Violation is logged and reported but does not block |

### Profiles

Principles can target specific contexts:
- `all` — applies everywhere
- `backend` — only when modifying backend code
- `frontend` — only when modifying frontend code
- `devops` — only for infrastructure changes
- `planning` — only for spec/PRD work

---

## Principle Directory

```
.cursor/principles/
├── think-before-coding.yaml
├── test-every-change.yaml
├── minimal-blast-radius.yaml
├── no-silent-failures.yaml
├── respect-existing-patterns.yaml
└── _compiled.md              # Auto-generated guidance digest
```

---

## Workflow

### 1. Register Principles

Create YAML files in `.cursor/principles/`. Each file defines one principle
with its rules, mode, profile, and scoring parameters.

Default principles (created on first use if directory is empty):

| Principle | Mode | Key Rules |
|-----------|------|-----------|
| Think Before Coding | gate | Read first, state approach, identify files |
| Test Every Change | gate | Write or update tests for every behavioral change |
| Minimal Blast Radius | advisory | Change the fewest files possible |
| No Silent Failures | gate | Every error path must log or return an error |
| Respect Existing Patterns | advisory | Match project conventions, don't introduce new ones |

### 2. Inject into Prompts

Before delegating work to a subagent or executing a task:

1. Load principles matching the current profile
2. Format as a concise behavioral contract
3. Append to the task prompt

Injection format:
```markdown
## Behavioral Principles (MUST follow)

1. **Think Before Coding** [GATE — blocks on failure]
   - Read existing code before modifying it
   - State your approach in 1-2 sentences before writing code

2. **Test Every Change** [GATE — blocks on failure]
   - Write or update tests for every behavioral change
```

### 3. Score Output

After receiving output from a task or subagent:

1. For each applicable principle, evaluate the output against each rule
2. Score as: `passed` (all rules met), `partial` (some rules met), `failed` (critical rules violated)
3. Calculate weighted composite score

```json
{
  "principle_scores": [
    {
      "id": "think-before-coding",
      "mode": "gate",
      "score": 0.85,
      "passed": true,
      "details": "Stated approach before coding, read 3 files first"
    },
    {
      "id": "test-every-change",
      "mode": "gate",
      "score": 0.3,
      "passed": false,
      "details": "Modified 2 functions but added no tests"
    }
  ],
  "composite_score": 0.58,
  "gate_passed": false,
  "blocking_principle": "test-every-change"
}
```

### 4. Gate Enforcement

If any `gate` principle fails:
- **Do NOT** proceed with the output
- Report which principle failed and why
- Request the agent to fix the violation and resubmit
- Maximum 2 retry attempts before escalating to user

### 5. Track Effectiveness

After each scoring cycle, record the outcome:

```yaml
# .cursor/principles/_effectiveness.yaml
think-before-coding:
  total: 42
  helpful: 38    # caught real issues
  unhelpful: 3   # false positives
  pending: 1
  effectiveness: 0.93
```

Periodically review effectiveness. Principles with effectiveness < 0.5 should be
revised or demoted from `gate` to `advisory`.

---

## Compiled Guidance

The `_compiled.md` file is auto-generated from:
- All registered principles
- Accumulated corrections (mistakes an agent made and learned from)
- Learnings (discovered patterns that should be followed)

This compiled guidance is injected alongside principles for richer context.

### Corrections

```markdown
## Corrections (mistakes to avoid)
- 2026-04-20: Changed API response schema without updating the OpenAPI spec.
  Always update `docs/openapi.yaml` when modifying response types.
- 2026-04-18: Used `fmt.Println` for error logging instead of structured logger.
  Always use `logger.Error()` with context fields.
```

### Learnings

```markdown
## Learnings (patterns to follow)
- This project uses repository pattern — never access DB directly from handlers
- Error codes follow `DOMAIN_ACTION_REASON` format (e.g., `ENDPOINT_CREATE_INVALID_GPU`)
- All new endpoints need entries in both handler_test.go AND integration test
```

---

## Integration with Other Skills

| Skill | Integration |
|---|---|
| `maestro-conductor` | Principles are injected into handoff briefs |
| `mission-control` | Principles are injected before subagent dispatch |
| `ship` / `deep-review` | Principle scoring runs as part of review |
| `icarus-memory-fabric` | Corrections and learnings stored in fabric |
| `ecc-continuous-learning` | Principle violations feed the learning loop |

---

## Commands

| Command | Action |
|---------|--------|
| `principles list` | Show all registered principles |
| `principles add` | Create a new principle interactively |
| `principles score` | Score the last agent output against principles |
| `principles compile` | Regenerate `_compiled.md` |
| `principles effectiveness` | Show effectiveness stats |
| `principles edit {id}` | Modify an existing principle |
