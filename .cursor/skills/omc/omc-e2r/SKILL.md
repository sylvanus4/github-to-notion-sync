---
name: omc-e2r
description: >-
  E2R (Explore-Execute-Review) Tree Search engine. MCTS-inspired parallel
  exploration, DAG-based AND-tree execution, and bottom-up quality review.
  The execution core of the OneManCompany framework.
  Use when a task needs structured decomposition with exploration of multiple
  approaches before committing to execution. Triggers: "e2r", "탐색-실행-리뷰",
  "E2R 루프", "트리 탐색", "병렬 탐색 후 실행".
  Do NOT use for simple linear tasks (execute directly).
  Do NOT use for planning without execution (use omc-ralplan).
arguments: [task]
disable-model-invocation: true
---

# E2R Tree Search Engine

Implements the Explore-Execute-Review loop from the OMC framework.
Core insight: combine MCTS exploration with DAG execution and bottom-up review
in a single deadlock-free loop.

## The E2R Loop

```
        +---> Explore (MCTS) ---+
        |                       |
        |                       v
  Review (bottom-up) <--- Execute (AND-tree DAG)
        |
        v
  Accept or Iterate
```

## Phase 1: Explore (MCTS-Inspired)

Goal: Find the best approach before committing to execution.

### Step 1: Generate Candidates

Spawn 2-3 exploration agents (haiku tier) in parallel. Each agent:
- Takes a different approach to the task
- Returns: approach description, estimated effort, risk assessment, key decisions

```
Agent prompt template for explorers:
"You are exploring approach [N] for: [task].
Your approach angle: [specific constraint or perspective].
Return in under 200 words:
1. Approach summary
2. Key files/components involved  
3. Estimated complexity (S/M/L)
4. Top risk
5. Dependencies on other work"
```

### Step 2: Evaluate & Select (UCB1-Inspired)

Score each candidate on:

| Criterion | Weight | How to assess |
|-----------|--------|---------------|
| Feasibility | 0.3 | Can we do this with available tools? |
| Quality ceiling | 0.3 | Best possible outcome if executed well |
| Risk | 0.2 | What can go wrong? (lower = better) |
| Cost | 0.2 | Agent count x model tier |

Select the approach with highest weighted score.
If two approaches score within 10%, present both to CEO for decision.

### Step 3: Decompose Selected Approach

Break the selected approach into an AND-tree (all subtasks must complete):

```
Root Task
  |-- Subtask A (independent)
  |-- Subtask B (independent)
  |-- Subtask C (depends on A)
  |-- Subtask D (depends on A + B)
```

Verify DAG invariant: no cycles. If a cycle is detected, restructure.

## Phase 2: Execute (AND-Tree DAG)

### Scheduling Algorithm

```
1. Create TaskCreate for each node in the AND-tree
2. ready_set = {nodes with no unmet dependencies}
3. while ready_set is not empty:
     a. Dispatch all nodes in ready_set as parallel Agent calls
     b. Mark dispatched nodes as Processing
     c. Collect results
     d. Mark completed nodes as Completed
     e. Update ready_set with newly unblocked nodes
4. If a node fails:
     a. Mark as Failed
     b. Cascade: mark all descendants as Blocked
     c. Attempt recovery (re-dispatch with error context)
     d. If recovery fails after 2 attempts -> escalate
```

### Agent Dispatch Rules

- **Independent subtasks**: Dispatch in parallel (single message, multiple Agent calls)
- **Dependent subtasks**: Wait for all dependencies to complete
- **Model selection**: Match to subtask complexity
  - File reading / grep / simple transform -> haiku
  - Implementation / writing -> sonnet  
  - Architecture decisions / complex reasoning -> opus
- **Isolation**: Use `isolation: "worktree"` for any subtask that writes code

### Execution Invariants

1. A task transitions only forward: Pending -> Processing -> Completed
2. A Processing task has exactly one agent working on it
3. A task enters Processing only when ALL dependencies are Accepted (not just Completed)
4. No two tasks write to the same file simultaneously (worktree isolation prevents this)

## Phase 3: Review (Bottom-Up)

Review from leaf nodes upward to root.

### Review Protocol

For each Completed task:

1. **Automated checks** (when applicable):
   - Code: `rtk go test` / `rtk vitest run` / `rtk tsc` / `rtk lint`
   - Docs: word count, structure check, link validation
   - Analysis: claim-evidence alignment

2. **Agent review** (for quality assessment):
   Spawn a reviewer agent (sonnet) with:
   ```
   "Review this deliverable against the acceptance criteria:
   Task: [description]
   Criteria: [what done looks like]
   Deliverable: [output summary]
   
   Return:
   - ACCEPT or REJECT
   - If REJECT: specific issues (max 3) with suggested fixes
   - Confidence: high/medium/low"
   ```

3. **Decision**:
   - ACCEPT -> Mark Accepted, unblock dependents
   - REJECT -> Re-dispatch original agent with reviewer feedback
   - Max 3 review rounds per task

### Integration Review

After all leaf tasks are Accepted, review the integrated result:
- Do the parts compose correctly?
- Does the whole satisfy the original goal?
- Any gaps between subtask outputs?

## Iteration Control

The E2R loop can iterate (back to Explore from Review) when:
- Integration review reveals a fundamental approach flaw
- More than 50% of tasks were rejected in first review round
- New information invalidates the selected approach

Max E2R iterations: 2 (explore-execute-review, then one retry).
After 2 iterations, deliver best result with issues documented.

## Output Format

Return to caller (omc-company or user):

```
## E2R Result

### Approach Selected
[1-2 sentence summary of chosen approach]

### Execution Summary
| Task | Status | Agent | Model | Review Rounds |
|------|--------|-------|-------|---------------|
| ...  | ...    | ...   | ...   | ...           |

### Deliverables
[List of outputs with locations]

### Issues
[Any unresolved issues or compromises]

### Cost
Agents dispatched: N
Estimated token cost: [breakdown by model tier]
```
