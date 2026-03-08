---
name: workflow-parallel
description: >-
  Fan out independent tasks to parallel subagents, aggregate results with a
  defined strategy (merge, vote, defer, union), and handle conflicts. Use when
  the user asks to "run in parallel", "fan out", "parallel workflow", "multiple
  perspectives", "concurrent agents", "parallel review", "병렬 실행", "동시 실행",
  or needs multiple independent analyses on the same input.
  Do NOT use for dependent tasks where order matters (use workflow-sequential).
  Do NOT use for iterative quality refinement (use workflow-eval-opt).
  Do NOT use when only 1 task exists.
metadata:
  author: thaki
  version: 1.0.0
  category: orchestration
---

# Workflow Parallel — Fan-Out/Fan-In Task Execution

Distribute independent tasks across parallel subagents, aggregate results using a defined strategy, and handle contradictions. Implements the fan-out/fan-in pattern from distributed systems.

Based on the Parallel workflow pattern from Anthropic's agent workflow patterns. Trades cost (multiple concurrent calls) for speed and separation of concerns.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Task list | Yes | List of independent tasks (2+) with names and instructions |
| Aggregation strategy | Yes | One of: `merge`, `vote`, `defer`, `union` |
| Conflict resolution | No | Policy for contradictory results (default: `flag`) |
| Agent config | No | Per-agent model and readonly settings (default: `fast`, `readonly: true`) |
| Shared context | No | Files or data provided to all agents |

## Workflow

### Step 1: Validate Independence

Before launching agents:

1. Verify no task depends on another task's output
2. If dependencies detected, suggest `workflow-sequential` instead and halt
3. Count tasks; if only 1, suggest direct execution and halt

### Step 2: Define Aggregation Strategy

**CRITICAL: Define this BEFORE launching agents.** Changing strategy after results arrive leads to data loss or contradictions.

| Strategy | Behavior | Best For |
|----------|----------|----------|
| `merge` | Combine all results into one list, deduplicate by key fields | Code review findings, analysis results |
| `vote` | Majority agreement wins; ties broken by confidence score | Classification, yes/no decisions |
| `defer` | Accept the most specialized agent's result for its domain | Multi-domain review where each agent owns a domain |
| `union` | Take all unique results without deduplication | Brainstorming, idea generation, exhaustive search |

### Step 3: Launch Parallel Agents

Use the Task tool to spawn subagents. Configuration:

- `subagent_type`: `generalPurpose`
- `model`: `fast` (default; override with agent config)
- `readonly`: `true` for analysis tasks; `false` for execution tasks
- Maximum: **4 concurrent subagents**

If more than 4 tasks: batch into rounds of 4. Wait for each round to complete before launching the next.

```
Round 1: Agent 1, Agent 2, Agent 3, Agent 4
  ↓ (wait for all to complete)
Round 2: Agent 5, Agent 6
  ↓ (wait for all to complete)
Aggregate all results
```

Each agent receives:
- Its specific task description
- Shared context (files, data)
- Required output format (structured, consistent across agents)

### Step 4: Aggregate Results

Apply the chosen aggregation strategy:

**Merge:**
1. Collect all agent outputs
2. Combine into a single list
3. Deduplicate: same file + same line + similar issue = keep the more detailed one
4. Sort by severity or priority

**Vote:**
1. Collect all agent decisions
2. Count votes per option
3. Majority wins; if tied, use confidence scores
4. Report vote distribution

**Defer:**
1. For each result, identify the originating agent's domain
2. Accept the domain-specialist agent's result for that domain
3. Flag cross-domain findings for manual review

**Union:**
1. Collect all agent outputs
2. Remove exact duplicates only
3. Preserve all unique contributions

### Step 5: Handle Conflicts

When agents produce contradictory results:

| Policy | Behavior |
|--------|----------|
| `flag` (default) | Include both results, mark as "CONFLICT — needs human review" |
| `specialist-wins` | Accept the result from the agent specialized in that domain |
| `majority-wins` | Accept the majority opinion (requires 3+ agents) |
| `conservative` | Accept the more cautious / safer result |

### Step 6: Report

```
Parallel Workflow Report
========================
Agents: [N] launched | [N] completed | [N] failed
Strategy: [merge|vote|defer|union]

Per-Agent Summary:
  Agent 1 ([name]): [N] findings / [decision]
  Agent 2 ([name]): [N] findings / [decision]
  Agent 3 ([name]): [N] findings / [decision]

Aggregated Results: [N] total ([N] after dedup)
Conflicts: [N] (resolution: [policy])

[Aggregated result details]
```

## Examples

### Example 1: Code Review (merge strategy)

User says: "Review this code from frontend, backend, security, and test perspectives."

Actions:
1. Validate: 4 independent review tasks
2. Strategy: merge (combine all findings)
3. Launch 4 agents in parallel (Frontend, Backend, Security, Test)
4. Aggregate: 3 + 5 + 2 + 4 = 14 findings, 2 duplicates removed = 12 unique
5. Sort by severity: 1 Critical, 3 High, 5 Medium, 3 Low
6. Report with domain breakdown

### Example 2: Classification (vote strategy)

User says: "Should we refactor this module? Get 3 independent opinions."

Actions:
1. Validate: 3 independent classification tasks
2. Strategy: vote
3. Launch 3 agents with the same question and code context
4. Votes: Yes (2), No (1) → Majority: Yes
5. Report: "2/3 agents recommend refactoring. Dissenting opinion: [reason]."

### Example 3: Batched Execution (6 tasks)

User says: "Analyze 6 documents for key themes."

Actions:
1. Validate: 6 independent analysis tasks
2. Strategy: union
3. Round 1: Launch agents 1-4
4. Round 1 complete: collect 4 results
5. Round 2: Launch agents 5-6
6. Round 2 complete: collect 2 results
7. Union: 38 unique themes identified
8. Report with per-document breakdown

## Error Handling

| Scenario | Action |
|----------|--------|
| Agent timeout | Re-launch once with same config; if still fails, report partial results |
| Agent returns empty | Note as "no findings" for that agent; continue aggregation |
| All agents fail | Report failure; suggest running tasks sequentially as fallback |
| Contradictory Critical findings | Always flag for human review regardless of conflict policy |
| Too many tasks (>20) | Warn user; suggest narrowing scope or batching manually |

## Integration

- Referenced by `mission-control` Step 2.5 for parallel sub-task groups
- Used by `deep-review` (4 domain agents), `simplify` (4 review agents), `diagnose` (3 analysis agents)
- Follows `workflow-patterns.mdc` Parallel pattern definition
- Follows `parallel-orchestration.mdc` for scaling and sync point rules
- Can be nested inside `workflow-sequential` as a parallel stage within a sequential pipeline
