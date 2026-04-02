---
name: mission-control
description: >-
  Orchestrate multi-skill autonomous workflows — decompose high-level goals
  into sub-tasks, delegate to specialist skills via subagents, aggregate
  results, and track progress. Use when the user asks for a full review, release
  prep, quality audit, incident response, or any task spanning multiple domains,
  or invokes workflow commands like /full-quality-audit, /feature-pipeline. Do
  NOT use for single-domain tasks that one specific skill can handle alone.
  Korean triggers: "감사", "리뷰", "파이프라인", "워크플로우".
metadata:
  author: "thaki"
  version: "1.1.0"
  category: "execution"
---
# Mission Control — Agent Orchestrator

The meta-skill that coordinates all other skills. Decomposes high-level goals into sub-tasks, delegates to specialist skills via the Task tool, aggregates results, and tracks progress.

## Core Principles

1. **Decompose first**: Break the goal into concrete sub-tasks before acting
2. **Right-size sub-tasks**: Each sub-task should be completable in one agent turn (3-5 files, 15-30 min). If larger, decompose further. If smaller, combine with related work.
3. **Delegate to specialists**: Each sub-task maps to a specific skill
4. **Parallelize**: Use up to 4 Task subagents concurrently
5. **Observe and verify**: After each sub-task completes, verify output against the expected blueprint before proceeding to the next
6. **Track progress**: Update `tasks/todo.md` with checkable items
7. **Aggregate results**: Combine outputs into a unified report
8. **Handle failures with classification**: When a sub-task fails, classify the failure before retrying (see Failure Classification below)

## Skill Registry

Currently available skills: `cursor-sync`, `deep-review`, `design-architect`, `diagnose`, `domain-commit`, `intent-alignment-tracker`, `semantic-guard`, `ship`, `simplify`, `skill-composer`, `skill-optimizer`, `test-suite`, `transcribee`, `ui-suite`, `video-compress`, `visual-explainer`, `workflow-miner`, `x-to-slack`, `mission-control`.

For the full registry (available + planned skills) and goal-to-skill mapping, see [references/skill-registry.md](references/skill-registry.md).

**IMPORTANT**: Before delegating to any skill, verify it exists by checking `.cursor/skills/{skill-name}/SKILL.md`. If a skill does not exist, handle the task inline via a general-purpose subagent or skip with a note.

## Orchestration Protocol

### Step 1: Analyze Goal

Read the user's request and identify:
- **Primary objective**: What needs to be achieved
- **Scope**: Which parts of the codebase are affected
- **Constraints**: Time, safety, or scope limitations
- **Matching workflow**: Does it match a predefined workflow?

### Step 2: Create Task Plan

Write a plan to `tasks/todo.md`:

```markdown
## [Goal Title]
Date: YYYY-MM-DD

- [ ] Sub-task 1 → skill: [skill-name]
- [ ] Sub-task 2 → skill: [skill-name]
- [ ] Sub-task 3 → skill: [skill-name]
- [ ] Aggregate results and report
```

### Step 2.5: Select Orchestration Pattern

For each sub-task group, classify which workflow pattern applies (per `workflow-patterns.mdc`):

| Sub-task characteristic | Pattern | Example |
|---|---|---|
| Independent review/analysis tasks | **Parallel** | 4 review agents in `/deep-review` |
| Tasks where output B depends on input A | **Sequential** | Data sync → Analysis → Report in `/today` |
| Tasks producing content that must meet a quality bar | **Evaluator-Optimizer** | Report generation with `ai-quality-evaluator` gate |

For the overall workflow, select a combination:

1. **Default:** Sequential pipeline with Parallel stages at bottleneck points
2. **Quality-critical outputs:** Add Evaluator-Optimizer loops at content generation stages (reports, PRDs, communications)
3. **Speed-critical:** Maximize Parallel stages; skip Evaluator-Optimizer loops

Document the pattern choice in the task plan (Step 2). Example:

```markdown
## [Goal Title]
Pattern: Parallel (review) → Evaluator-Optimizer (fix+verify) → Sequential (commit+PR)
```

### Step 3: Delegate via Subagents

Use the Task tool to run skills in parallel. Maximum 4 concurrent subagents.

Before launching, define a **blueprint** for each sub-task: expected output, files that should change, files that must NOT change. This blueprint serves as the verification criteria in Step 4.

For each subagent:
1. Read the target skill's SKILL.md first
2. Include the specific sub-task in the prompt
3. Include relevant context (file paths, error messages, etc.)
4. Include "Must NOT Have" guardrails where applicable
5. Request structured output

```
Task(
  description="Run [skill-name] for [sub-task]",
  prompt="Read the skill at [SKILL.md path] and follow its instructions to [specific task]. Return structured results.",
  subagent_type="generalPurpose"
)
```

**Parallelization strategy:**
- Review skills (read-only) can all run in parallel
- Execution skills must respect dependency order
- CI quality gate should run after code modifications
- domain-commit should be the final execution step

### Step 4: Aggregate Results

Collect outputs from all subagents and:
1. Merge findings by severity/priority
2. De-duplicate overlapping findings
3. Create a unified summary
4. Update `tasks/todo.md` with completed items

### Step 5: Present Results

Deliver a structured report to the user:

```
Mission Control Report
======================
Goal: [original goal]
Date: [YYYY-MM-DD]
Skills invoked: [N]

Summary:
  [2-3 sentence executive summary]

Findings by Priority:
  Critical: [N]
  High: [N]
  Medium: [N]
  Low: [N]

Detailed Results:
  [Skill 1]: [summary of findings]
  [Skill 2]: [summary of findings]
  ...

Actions Taken:
  1. [action]
  2. [action]

Recommended Next Steps:
  1. [recommendation]
  2. [recommendation]
```

### Step 6: Self-Improvement

After task completion, if any errors or unexpected results occurred:
- Document the lesson in `tasks/lessons.md`
- Pattern: `[Date] [Skill] [What went wrong] → [What to do differently]`

## Predefined Workflows

Workflow commands: `/full-quality-audit`, `/feature-pipeline`, `/release-prep`, `/incident-response`, `/dependency-sweep`, `/i18n-check`

For detailed workflow definitions (steps, parallelization strategy, skill assignments), see [references/workflows.md](references/workflows.md).

## Failure Classification

When a sub-task fails, classify the failure before retrying (per `critical-thinking.mdc`):

- **Type 1 — Context Gap**: Subagent lacked necessary information (missing file reference, unknown convention). **Action**: Re-launch with additional context.
- **Type 2 — Direction Error**: Requirements were ambiguous or misunderstood. **Action**: Clarify the sub-task description and re-launch.
- **Type 3 — Structural Conflict**: The task scope or code structure makes the sub-task inherently conflicting. **Action**: Decompose further, add guardrails, or restructure the approach.

**Never re-launch a failed subagent with the same prompt.** Diagnose the failure type, modify the instruction accordingly, then retry.

## Examples

### Example 1: Full quality audit

User says: "/full-quality-audit" or "Run a full review of the codebase"

Actions:
1. Decompose into 4 sub-tasks: code quality, test coverage, security, performance
2. Delegate to `simplify`, `test-suite`, `deep-review` in parallel (3 subagents)
3. Aggregate findings, de-duplicate, sort by severity
4. Present unified report with actions taken and next steps

Result: Single report covering all domains with prioritized findings and auto-applied fixes.

### Example 2: Incident response

User says: "The API is returning 500 errors on /users endpoint"

Actions:
1. Delegate to `diagnose` (root cause analysis on the endpoint)
2. Based on diagnosis, delegate fix to a general-purpose subagent
3. Delegate to `test-suite` (verify fix doesn't break other tests)
4. Update `tasks/todo.md` with incident timeline

Result: Root cause identified, fix applied, tests passing, incident documented.

## Error Handling

- **Subagent timeout**: Re-launch with `model: "fast"` for simpler analysis
- **Skill not found**: Log to `tasks/lessons.md` and continue with available skills
- **Conflicting results**: Present both findings to the user for resolution
- **Partial failure**: Complete remaining tasks and report partial results
- **All failed**: Report the failure pattern and suggest manual investigation

## Troubleshooting

- **Skill not found at expected path**: Check [references/skill-registry.md](references/skill-registry.md) — it may be a planned skill. Handle inline or skip.
- **Subagent returns empty results**: Verify the skill exists and the prompt includes sufficient context (file paths, error messages).
- **Workflow command not recognized**: Supported commands are listed under Predefined Workflows. Check [references/workflows.md](references/workflows.md) for definitions.

## Integration Notes

- This skill is the orchestrator — it reads other skills but is never called by them
- Always read the target skill's SKILL.md before delegating (skills may have been updated)
- Respect the safety rules: never push to upstream, never force delete
- Track all orchestration runs in `tasks/todo.md` for audit trail
- Follow `observability.mdc` for intermediate checkpoints and staged commits
- Follow `parallel-orchestration.mdc` when running multiple subagents simultaneously
- Follow `context-architecture.mdc` for context isolation between parallel subagents

## Coordinator Synthesis

When delegating to subagents:

- **Never use lazy delegation.** Provide specific inputs (file paths, data, context) to every subagent — not "based on your findings, do X."
- **Purpose statement required:** Every subagent prompt must include why the task matters and how its output is used downstream.
- **Continue vs Spawn decision:**
  - Continue (resume) when worker context overlaps with the next task or fixing a previous failure
  - Spawn fresh when verifying another worker's output or when previous approach was fundamentally wrong
- Use `model: "fast"` for exploration/read-only subagents; default model for generation/analysis

## Honest Reporting

- Report phase outcomes faithfully: if a phase fails, say so with the error output
- Never claim "pipeline complete" when phases were skipped or failed
- Never suppress failing phases to manufacture a green summary
- When a phase succeeds, state it plainly without unnecessary hedging
- The Slack summary must accurately reflect what happened — not what was hoped

## Subagent Contract

Subagent prompts must include:
- Always use absolute file paths (subagent cwd may differ)
- Return `{ status, file, summary }` for orchestrator context efficiency
- Include code snippets only when exact text is load-bearing
- Do not recap files merely read — summarize findings
- Final response: concise report of what was done, key findings, files changed
- Do not use emojis
