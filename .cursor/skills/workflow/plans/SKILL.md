---
name: plans
description: >-
  Two-phase pipeline: optimize a raw prompt using prompt-architect frameworks,
  then decompose the optimized prompt into a skill-based execution plan with
  task delegation, dependency ordering, and verification criteria. Use when the
  user runs /plans, asks to "plan and optimize", "architect and plan", "optimize
  then plan", "프롬프트 최적화 후 계획", "플랜 작성", or wants both prompt optimization and
  execution planning in one flow. Do NOT use for prompt optimization only (use
  prompt-architect), execution only without optimization (use mission-control),
  or simple implementation planning (use /plan command).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
---
# Plans — Optimize Prompt, Then Plan Execution

A meta-orchestrator that combines prompt-architect (framework-based prompt design) with mission-control-style skill planning. Takes a raw prompt, structures it using the best framework, then decomposes it into a skill-based execution plan.

## Workflow

Execute these 7 steps in order.

### Step 1: Receive Raw Prompt

Accept the user's raw prompt. This may come from:
- `/plans` command `$ARGUMENTS`
- Direct user message
- Selected text in the editor

If the prompt is empty, ask the user to provide one. Store the original text verbatim for the before/after comparison.

### Step 2: Phase 1 — Optimize the Prompt

Read and follow the `prompt-architect` skill at `.cursor/skills/standalone/prompt-architect/SKILL.md`.

Execute its 6-step workflow against the raw prompt:
1. **Score** the original prompt across 5 dimensions (Clarity, Specificity, Context, Completeness, Structure — each 1-10)
2. **Recommend** a framework using the decision tree (or use `--framework` override if provided)
3. **Ask** 3-5 clarifying questions based on framework gaps
4. **Apply** the framework template from `.cursor/skills/standalone/prompt-architect/references/templates.md`
5. **Present** before/after comparison with scores
6. **Iterate** if the user wants changes

If `--framework <name>` was specified, skip the recommendation step and use the requested framework directly.

### Step 3: Phase 1 Checkpoint

Present the optimized prompt and ask for user confirmation before proceeding:

```
Phase 1 complete.

Original score: X.X/10 → Optimized score: Y.Y/10
Framework applied: [framework name]

[Show the optimized prompt]

Proceed to Phase 2 (execution planning)? Or refine the prompt further?
```

MUST wait for explicit user approval. If the user requests changes, return to Step 2.

### Step 4: Phase 2 — Decompose into Sub-Tasks

Break the optimized prompt into 3-8 concrete, actionable sub-tasks:

1. Read the optimized prompt and identify distinct work units
2. Each sub-task must be completable by a single skill or subagent
3. Each sub-task must have a clear deliverable
4. Order sub-tasks by logical dependency

Guidelines:
- If fewer than 3 sub-tasks emerge, the prompt may be too narrow — consider whether Phase 2 adds value, or just present the optimized prompt as the final output
- If more than 8 sub-tasks emerge, group related tasks to reduce to 5-8
- Label each sub-task with a short descriptive name

### Step 5: Phase 2 — Match Skills to Sub-Tasks

For each sub-task, find the best matching skill:

1. Load the domain-to-skill mapping from [references/skill-domains.md](references/skill-domains.md)
2. Classify the sub-task's domain (code quality, testing, security, UI/UX, etc.)
3. Check whether the matched skill exists at `.cursor/skills/{skill-name}/SKILL.md`
4. Classify the match quality:
   - **exact**: Skill directly handles the entire sub-task
   - **partial**: Skill covers part of the sub-task; note what remains
   - **none**: No matching skill; assign to `generalPurpose` subagent

If multiple skills match a sub-task, prefer the more specific one. If the sub-task spans multiple domains, split it further or assign the primary skill and note the secondary.

### Step 6: Phase 2 — Build the Execution Plan

Produce a structured plan with the following sections:

#### 6a. Task Table

| # | Task | Skill | Match | Depends On | Group | Complexity |
|---|------|-------|-------|------------|-------|------------|
| 1 | [name] | [skill] | exact/partial/none | - | A | Low/Med/High |

- **Depends On**: List task numbers that must complete first (or `-` for no dependencies)
- **Group**: Tasks in the same group can run in parallel (A, B, C...)
- **Complexity**: Estimated effort (Low = minutes, Medium = 30min, High = 1hr+)

#### 6b. Dependency Graph

Show the execution order visually:

```
Group A (parallel): Task 1, Task 2
    ↓
Group B (parallel): Task 3, Task 4
    ↓
Group C (sequential): Task 5
```

#### 6c. Verification Criteria

For each task, define how to verify completion:
- What files should change
- What tests should pass
- What output to expect

#### 6d. Recommended Next Steps

1-3 concrete actions the user should take next (e.g., "Run `/plans --execute` to begin", "Review Task 3 scope before starting").

### Step 7: Optional Execute

If the `--execute` flag was provided and the user approves:

1. Read the `mission-control` skill at `.cursor/skills/workflow/mission-control/SKILL.md`
2. Delegate the execution plan to mission-control
3. Pass each task's skill assignment and verification criteria
4. Follow mission-control's orchestration protocol (parallel subagents, progress tracking, result aggregation)

If `--execute` was NOT provided, present the plan and stop. The user can later invoke specific skills manually or run `/plans --execute` to resume.

## Output Format

```
## Plans Report

### Phase 1: Prompt Optimization
- **Framework**: [selected framework]
- **Score**: [before] → [after]

**Optimized Prompt:**
[structured prompt in code block]

### Phase 2: Execution Plan

| # | Task | Skill | Match | Depends On | Group | Complexity |
|---|------|-------|-------|------------|-------|------------|
| 1 | ... | ... | exact | - | A | Low |
| 2 | ... | ... | exact | - | A | Medium |
| 3 | ... | ... | partial | 1, 2 | B | High |

**Execution Order:**
Group A (parallel): Task 1, Task 2
  → Group B: Task 3

### Verification Criteria
- Task 1: [criteria]
- Task 2: [criteria]
- Task 3: [criteria]

### Recommended Next Steps
1. [action]
2. [action]
```

## Error Handling

| Problem | Solution |
|---------|----------|
| Raw prompt is empty | Ask the user to provide a prompt |
| Prompt too vague even after optimization | Ask additional clarifying questions before Phase 2 |
| No skills match a sub-task | Assign to generalPurpose subagent, note in plan |
| Too many sub-tasks (>8) | Group related tasks, reduce to 5-8 |
| Too few sub-tasks (<3) | Consider skipping Phase 2; deliver optimized prompt as final output |
| User rejects optimized prompt | Iterate on Phase 1 (return to Step 2) |
| Matched skill does not exist at expected path | Note as "planned skill", assign to generalPurpose |
| `--execute` fails mid-way | Follow mission-control failure classification and retry protocol |

## Examples

### Example 1: Feature development prompt

**User**: `/plans Build a user authentication system with OAuth and JWT`

**Phase 1** (prompt-architect):
- Original score: 3.2/10
- Framework: RISEN (multi-step process with methodology and constraints)
- Optimized prompt includes Role, Instructions, Steps, End Goal, Narrowing

**Phase 2** (skill planning):
| # | Task | Skill | Group |
|---|------|-------|-------|
| 1 | Design auth architecture | backend-expert | A |
| 2 | Review security requirements | security-expert | A |
| 3 | Implement OAuth + JWT | generalPurpose | B |
| 4 | Write auth tests | test-suite | C |
| 5 | Create API documentation | technical-writer | C |

### Example 2: Code quality audit

**User**: `/plans Review the frontend for performance issues and fix them`

**Phase 1** (prompt-architect):
- Framework: RISEN
- Optimized prompt with clear steps, end goal, and narrowing

**Phase 2** (skill planning):
| # | Task | Skill | Group |
|---|------|-------|-------|
| 1 | Frontend performance review | simplify (focus: performance) | A |
| 2 | Bundle size analysis | performance-profiler | A |
| 3 | Apply performance fixes | generalPurpose | B |
| 4 | Verify fixes pass tests | test-suite | C |

### Example 3: Content creation (Phase 2 skipped)

**User**: `/plans Write a blog post about our new AI features`

**Phase 1** (prompt-architect):
- Framework: CO-STAR
- Score: 2.0 → 8.5

**Phase 2**: Only 1-2 sub-tasks emerge (write + review). Phase 2 adds minimal value. Present the optimized CO-STAR prompt as the final deliverable.

## References

- Phase 1 skill: [prompt-architect](.cursor/skills/standalone/prompt-architect/SKILL.md)
- Phase 1 frameworks: [prompt-architect/references/frameworks.md](.cursor/skills/standalone/prompt-architect/references/frameworks.md)
- Phase 1 templates: [prompt-architect/references/templates.md](.cursor/skills/standalone/prompt-architect/references/templates.md)
- Phase 2 skill matching: [references/skill-domains.md](references/skill-domains.md)
- Phase 2 execution: [mission-control](.cursor/skills/workflow/mission-control/SKILL.md)
- Phase 2 skill registry: [mission-control/references/skill-registry.md](.cursor/skills/workflow/mission-control/references/skill-registry.md)
