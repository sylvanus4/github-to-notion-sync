---
name: workflow-sequential
description: >-
  Execute a list of tasks in dependency order with checkpoints, error
  recovery, and conditional skipping. Use when the user asks to "run tasks in
  order", "sequential pipeline", "chain these steps", "execute in sequence",
  "sequential workflow", "순차 실행", "파이프라인 실행", or needs to orchestrate
  dependent tasks where step B requires step A's output. Do NOT use for
  independent tasks that can run simultaneously (use workflow-parallel). Do
  NOT use for iterative quality refinement (use workflow-eval-opt). Do NOT use
  for single-task execution.
disable-model-invocation: true
---

# Workflow Sequential — Dependency-Ordered Task Execution

Execute tasks in dependency order with checkpoints between stages. Each task receives the output of its predecessor and passes its output to the next. Handles error recovery, conditional skipping, and staged commits.

Based on the Sequential workflow pattern from Anthropic's agent workflow patterns. Trade latency for accuracy by letting each agent focus on a specific subtask instead of handling everything at once.

## Inputs

The user provides (or the orchestrating skill defines):

| Input | Required | Description |
|-------|----------|-------------|
| Task list | Yes | Ordered list of tasks with names and instructions |
| Dependencies | No | Explicit dependency graph (default: linear chain A->B->C) |
| Skip conditions | No | Per-task conditions to skip (flags, data absence) |
| Error policy | No | Per-task: `retry`, `skip-warn`, or `halt` (default: `halt`) |
| Checkpoint | No | Whether to commit/verify after each task (default: verify only) |

## Workflow

### Step 1: Validate Task Graph

Parse the task list and dependency declarations.

1. Build a directed acyclic graph (DAG) of dependencies
2. Detect cycles — if found, report the cycle and halt
3. Topologically sort into execution order
4. If no explicit dependencies, assume linear chain: Task 1 -> Task 2 -> ... -> Task N

### Step 2: Execute Tasks in Order

For each task in topological order:

**2a. Check skip condition:**
- If a skip flag is set for this task, log "Skipped: [task name] (reason)" and continue
- If required input data is missing and the task is marked optional, skip with warning

**2b. Execute the task:**
- Pass the accumulated context (prior task outputs) to the current task
- If the task references a skill, read the skill's SKILL.md and follow its instructions
- If the task is a shell command, execute via the Shell tool
- If the task is a subagent delegation, use the Task tool with appropriate config

**2c. Checkpoint:**
- Verify the task produced expected output (non-empty, correct format)
- If checkpoint config includes `commit`: create a staged commit with `[chore] Pipeline: {task name}`
- If verification fails, apply the error policy (see Step 3)

**2d. Pass output forward:**
- Store the task's output in the pipeline context
- Make it available to subsequent tasks as input

### Step 3: Error Handling

When a task fails, apply its configured error policy:

| Policy | Behavior |
|--------|----------|
| `halt` (default) | Stop the pipeline. Report which task failed, its error, and which tasks remain unexecuted. |
| `retry` | Re-execute the task once with the same inputs. If it fails again, escalate to `halt`. |
| `skip-warn` | Log a warning, mark the task as failed, and continue to the next task. Downstream tasks that depend on this task's output also get skipped. |

### Step 4: Report

Present the pipeline execution report:

```
Sequential Pipeline Report
===========================
Tasks: [N] total | [N] completed | [N] skipped | [N] failed

Execution Log:
  1. [task name] — COMPLETED (output: [summary])
  2. [task name] — COMPLETED (output: [summary])
  3. [task name] — SKIPPED (reason: [skip condition])
  4. [task name] — FAILED (error: [message], policy: halt)

Pipeline Status: [COMPLETED | PARTIAL | FAILED]
```

## Examples

### Example 1: Data Pipeline

User says: "Run the daily data sync pipeline: check freshness, import CSVs, fetch from Yahoo, then verify."

Actions:
1. Parse 4 tasks with linear dependencies: check -> import -> fetch -> verify
2. Execute check: DB status shows 3 stale tickers
3. Execute import: CSV import completes, 150 rows upserted
4. Execute fetch: Yahoo Finance returns 3-day data for stale tickers
5. Execute verify: All tickers now current
6. Report: 4/4 completed

### Example 2: Pipeline with Skip Conditions

User says: "Build and deploy: lint, test, build, deploy. Skip deploy if tests fail."

Actions:
1. Parse 4 tasks: lint -> test -> build -> deploy (deploy skip-condition: test must pass)
2. Execute lint: PASS
3. Execute test: 2 failures
4. Execute build: PASS
5. Skip deploy: test failures present
6. Report: 3/4 completed, 1 skipped

### Example 3: Pipeline with Error Recovery

User says: "Process files in order with retry: parse, validate, transform, load."

Actions:
1. Parse 4 tasks with retry policy on transform
2. Execute parse: PASS
3. Execute validate: PASS
4. Execute transform: FAIL (timeout)
5. Retry transform: PASS
6. Execute load: PASS
7. Report: 4/4 completed (1 retry)

## Error Handling

| Scenario | Action |
|----------|--------|
| Circular dependency detected | Report the cycle and halt before execution |
| Task produces empty output | Apply error policy; if `halt`, stop pipeline |
| Task timeout | Treat as failure; apply error policy |
| Missing skill reference | Log warning; attempt inline execution or skip |
| All tasks skipped | Report "Pipeline completed with no executed tasks" |

## Integration

- Referenced by `mission-control` Step 2.5 for sequential sub-task groups
- Follows `workflow-patterns.mdc` Sequential pattern definition
- Follows `observability.mdc` for checkpoint protocol and staged commits
- Compatible with `workflow-parallel` (a sequential pipeline can contain parallel stages)

## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
