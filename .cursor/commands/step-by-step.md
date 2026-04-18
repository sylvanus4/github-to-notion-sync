---
description: "Break down any reasoning or execution process into numbered sequential steps with clear logic, rationale, and optional checkpoint gates"
argument-hint: "<question or task to decompose into steps>"
---

# Step-by-Step

Decompose complex reasoning or execution into numbered, atomic steps. Each step includes what to do and why.

Integrates **Step Separator (Pattern 6):** With `--checkpoint` mode, every step becomes a hard gate — the AI must pause after each step, confirm completion, and wait for explicit "continue" before proceeding. This prevents the AI from rushing through multi-step processes and skipping verification.

## Usage

```
/step-by-step How do I deploy a FastAPI app to Kubernetes?
/step-by-step Debug why my React component re-renders infinitely
/step-by-step 신규 SaaS 제품의 가격 정책을 어떻게 설계해야 할까?
/step-by-step --with-decisions How to migrate from REST to GraphQL
/step-by-step --checklist Set up CI/CD for a Python monorepo
/step-by-step --checkpoint Migrate production database with zero downtime
/step-by-step --checkpoint --estimate Refactor authentication from session-based to JWT
```

## Your Task

User input: $ARGUMENTS

### Mode Selection

Parse `$ARGUMENTS` for flags:

- **No flags** — Numbered steps with rationale (default)
- `--with-decisions` — Add decision points marked with `[DECISION]` where the path forks
- `--checklist` — Output as a checkable `- [ ]` list instead of numbered prose
- `--dependencies` — Add a dependency graph showing which steps block others
- `--estimate` — Add rough time estimates per step
- `--checkpoint` — **Hard-stop mode:** Execute one step at a time, pause after each, and wait for user confirmation before proceeding. Each step is a gate — no skipping, no batching, no "I'll do steps 3-5 together"

### Workflow

1. **Parse task** — Extract the goal or question from `$ARGUMENTS`
2. **Identify end state** — Define what "done" looks like
3. **Decompose** — Break into the smallest meaningful steps (each step = one action or one decision)
4. **Order** — Arrange steps by dependency, then by natural sequence
5. **Add rationale** — For each step, add a brief "Why:" explaining the reasoning
6. **Mark decision points** (if `--with-decisions`) — Where the path forks, list options and selection criteria
7. **Add dependencies** (if `--dependencies`) — Note which steps must complete before others can start
8. **Estimate** (if `--estimate`) — Add time ranges (e.g., "~15 min", "1-2 hours")
9. **Define checkpoint criteria** (if `--checkpoint`) — For each step, define:
   - **Done condition:** What observable evidence proves this step is complete
   - **Verification command:** A concrete command, query, or check to run (e.g., `curl`, `kubectl get`, `npm test`)
   - **Abort condition:** What would indicate a problem that should halt execution
10. **Verify completeness** — Walk through the steps mentally; fill any gaps

### Checkpoint Mode Behavior

When `--checkpoint` is active:

1. **Present the full plan first** — Show all steps with their checkpoint criteria so the user sees the whole picture
2. **Execute Step 1 only** — Perform the first step's action
3. **Report & pause** — After executing, show:
   - What was done
   - Verification result (ran the check, shows the output)
   - `CHECKPOINT [1/N]: Step 1 complete. Reply "continue" to proceed to Step 2, or "abort" to stop.`
4. **Wait** — Do NOT proceed until the user explicitly says "continue", "next", "go", or equivalent
5. **Repeat** for each subsequent step
6. **If verification fails** — Report the failure, suggest remediation, and wait. Do NOT auto-remediate unless the user confirms

### Output Format

Default mode:
```
## Step-by-Step: [Task]

**Goal:** [End state in one sentence]

### Step 1: [Action]
[What to do in 1-2 sentences]
**Why:** [Rationale]

### Step 2: [Action]
[What to do]
**Why:** [Rationale]

...

### Result
[What you should have when all steps are complete]
```

Checkpoint mode (initial plan):
```
## Step-by-Step (Checkpoint Mode): [Task]

**Goal:** [End state in one sentence]
**Steps:** N | **Mode:** Checkpoint (pause after each step)

| Step | Action | Done Condition | Verification |
|------|--------|---------------|--------------|
| 1 | [action] | [what proves it's done] | [command to check] |
| 2 | [action] | [what proves it's done] | [command to check] |
| ... | ... | ... | ... |

---
Starting Step 1...
```

Checkpoint mode (after each step):
```
### Step [N] Complete

**Action:** [what was done]
**Verification:** [command and its output]
**Status:** PASS / FAIL

---
CHECKPOINT [N/total]: Step N complete. Reply "continue" to proceed to Step [N+1].
```

### Constraints

- Each step must be a single, verifiable action — not a vague instruction like "set things up"
- Steps must be ordered so someone could follow them linearly without backtracking
- If a step requires a choice, use `[DECISION]` and list the options with trade-offs
- Never combine two unrelated actions into one step
- In checkpoint mode, NEVER execute the next step without user confirmation — this is the core invariant
- In checkpoint mode, NEVER say "I'll go ahead and do steps 2-4" — one step per gate, no exceptions
