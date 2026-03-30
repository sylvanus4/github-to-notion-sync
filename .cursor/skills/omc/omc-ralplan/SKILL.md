---
name: omc-ralplan
description: >-
  3-agent consensus planning with RALPLAN-DR structured deliberation. Runs a
  Planner → Architect → Critic loop (max 5 iterations) until consensus is
  reached. Produces plans with ADR (Architecture Decision Record), principles,
  decision drivers, and viable options with bounded pros/cons. Supports short
  mode (default) and deliberate mode for high-risk work (adds pre-mortem and
  expanded test planning). Use when the user asks to "consensus plan", "ralplan",
  "multi-agent plan", "architect review plan", "critic review plan", "3-agent
  planning", "structured planning", "RALPLAN", "plan with consensus",
  "plan with review", "합의 기반 계획", "3에이전트 계획", "구조화된 계획",
  "합의 계획", "아키텍트 리뷰 계획", or needs a quality-gated planning process
  with architectural review and critical evaluation before execution. Do NOT use
  for simple single-step tasks (execute directly). Do NOT use for plan execution
  (use sp-executing-plans). Do NOT use for brainstorming without planning intent
  (use sp-brainstorming). Do NOT use for code review (use deep-review or simplify).
metadata:
  author: "oh-my-claudecode"
  version: "1.0.0"
  category: "planning"
---

# Ralplan: 3-Agent Consensus Planning

Adapted from [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) ralplan skill. Implements iterative planning with Planner, Architect, and Critic agents until consensus is reached.

## Instructions

### Overview

Ralplan chains three quality gates via subagents:

```
Planner creates plan → Architect reviews → Critic evaluates → Loop until APPROVE (max 5)
```

### Step 1: Planner Draft

Spawn a `Task` subagent (`subagent_type="generalPurpose"`) as the Planner role:

**Planner responsibilities:**
- Explore the codebase to understand the current state (never ask the user for codebase facts)
- Create a 3-6 step actionable plan with clear acceptance criteria per step
- Include a **RALPLAN-DR summary**:
  - **Principles** (3-5): Core design principles guiding the plan
  - **Decision Drivers** (top 3): Key factors influencing the approach
  - **Viable Options** (≥2): Each with bounded pros/cons
  - If only one viable option remains, provide explicit invalidation rationale for alternatives
- Write the plan to `outputs/plans/ralplan-{slug}.md`

**Deliberate mode** (for high-risk work: auth/security, migrations, destructive changes, production incidents, compliance/PII, public API changes):
- Add **pre-mortem**: 3 specific failure scenarios assuming the plan was executed exactly as written and failed
- Add **expanded test plan**: unit, integration, e2e, and observability coverage

### Step 2: Present Draft (Optional Interactive)

If the task warrants user input, use `AskQuestion` to present the draft plan with the Principles/Drivers/Options summary:

- Proceed to Architect review
- Request changes
- Skip review (not recommended)

For straightforward tasks, proceed automatically to Architect review.

### Step 3: Architect Review

Spawn a `Task` subagent as the Architect role (read-only analysis):

**Architect must provide:**
- Every finding cites a specific file:line reference
- Root cause identification (not just symptoms)
- Concrete, implementable recommendations with trade-offs
- **Strongest steelman antithesis** against the favored direction
- At least one **real tradeoff tension** that cannot be ignored
- **Synthesis** if feasible — how to preserve strengths from competing options
- In deliberate mode: explicit **principle-violation flags**

**CRITICAL: Await Architect completion before starting Critic. Never run them in parallel.**

### Step 4: Critic Evaluation

Spawn a `Task` subagent as the Critic role (read-only analysis):

**Critic evaluation protocol:**
1. **Pre-commitment predictions**: Before reading, predict 3-5 likely problem areas
2. **Verification**: Extract and verify ALL file references, function names, technical claims
3. **Plan-specific investigation**:
   - Key Assumptions Extraction (VERIFIED / REASONABLE / FRAGILE)
   - Pre-Mortem (5-7 failure scenarios — does the plan address each?)
   - Dependency Audit (circular deps, missing handoffs, resource conflicts)
   - Ambiguity Scan ("Could two developers interpret this differently?")
   - Feasibility Check ("Does the executor have everything needed?")
4. **Multi-perspective review**: Executor, Stakeholder, Skeptic perspectives
5. **Gap analysis**: What's MISSING, not just what's wrong
6. **Self-audit**: Move low-confidence findings to Open Questions

**Critic verdict:** `APPROVE` / `ITERATE` / `REJECT`

**Critic must enforce:**
- Principle-option consistency
- Fair alternatives exploration
- Risk mitigation clarity
- Testable acceptance criteria
- Concrete verification steps
- In deliberate mode: reject missing/weak pre-mortem or expanded test plan

### Step 5: Re-Review Loop (Max 5 Iterations)

Any non-`APPROVE` verdict triggers the full loop:
1. Collect Architect + Critic feedback
2. Revise plan with Planner subagent
3. Return to Architect review (Step 3)
4. Return to Critic evaluation (Step 4)
5. Repeat until `APPROVE` or 5 iterations reached

If 5 iterations reached without `APPROVE`, present the best version to the user with noted reservations.

### Step 6: Final Output

On Critic approval, the final plan must include:

- **ADR** (Architecture Decision Record):
  - Decision
  - Drivers
  - Alternatives considered
  - Why chosen
  - Consequences
  - Follow-ups
- **RALPLAN-DR Summary**: Principles, Decision Drivers, Options
- **Acceptance criteria** for each step
- **Implementation steps** with file references

Present execution options:
1. **Execute with parallel agents** (recommended for large scope)
2. **Execute sequentially** (safer for complex dependencies)
3. **Request changes** — return to interview
4. **Reject** — discard and start fresh

### Pre-Execution Gate

The ralplan gate intercepts underspecified requests for execution modes. When a request lacks concrete anchors (file paths, function names, issue numbers, test targets, numbered steps):

**Passes the gate** (specific enough):
- "Fix the null check in `src/hooks/bridge.ts:326`"
- "Implement issue #42"
- "Add validation to `processKeywordDetector`"

**Gated — needs planning first:**
- "Fix this"
- "Improve performance"
- "Add authentication"

## Error Handling

- **Planner subagent fails to explore codebase**: Include whatever context is available; note gaps in the plan for Architect to flag.
- **Architect or Critic subagent times out**: Retry once; on second failure, present the current plan version to the user with a note that review was incomplete.
- **5 iterations reached without APPROVE**: Present the best version to the user with all unresolved Critic findings listed, and ask for user decision.
- **Conflicting Architect and Critic feedback**: Planner should address both concerns explicitly in the next revision; if fundamentally contradictory, surface the conflict to the user.
- **Plan file write fails**: Output the plan in the response text as a fallback.

## When to Use

- Task needs multi-perspective planning before execution
- Work involves architectural decisions with trade-offs
- High-risk changes (auth, migrations, production, APIs)
- User wants consensus between planning, architecture, and quality perspectives
- Execution request is underspecified (no file paths, function names, or test targets)

## When NOT to Use

- Simple single-step tasks with clear targets — execute directly
- User already has a detailed plan — use sp-executing-plans
- Brainstorming without intent to produce a plan — use sp-brainstorming
- Code review without planning — use deep-review or simplify

## Examples

<example>
User: "Add user authentication to the app"

[Planner subagent explores codebase, finds no existing auth]

**RALPLAN-DR Summary:**
- Principles: (1) Minimal session state, (2) Standard protocols only, (3) Progressive security
- Decision Drivers: (1) Time-to-ship, (2) Future SSO compatibility, (3) Security posture
- Option A: JWT + passport.js — Pros: stateless, scalable / Cons: token revocation complexity
- Option B: Session-based with Redis — Pros: simple revocation / Cons: Redis dependency, state management

[Architect reviews: steelman antithesis against JWT, tradeoff tension on token revocation]
[Critic evaluates: ITERATE — missing rate-limiting, no password policy defined]
[Planner revises with feedback]
[Architect re-reviews]
[Critic: APPROVE — all criteria met]

Final plan with ADR written to outputs/plans/ralplan-user-auth.md
</example>

<example>
Deliberate mode trigger:

User: "Migrate the database schema from PostgreSQL to a new structure"

[Auto-detects high-risk: migration → deliberate mode enabled]
[Planner includes pre-mortem: (1) data loss during migration, (2) downtime exceeds SLA, (3) rollback fails]
[Planner includes expanded test plan: unit tests for data transformers, integration tests for migration scripts, e2e for user flows post-migration, observability for migration progress metrics]
</example>
