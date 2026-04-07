---
description: "Break down any reasoning or execution process into numbered sequential steps with clear logic and rationale"
argument-hint: "<question or task to decompose into steps>"
---

# Step-by-Step

Decompose complex reasoning or execution into numbered, atomic steps. Each step includes what to do and why.

## Usage

```
/step-by-step How do I deploy a FastAPI app to Kubernetes?
/step-by-step Debug why my React component re-renders infinitely
/step-by-step 신규 SaaS 제품의 가격 정책을 어떻게 설계해야 할까?
/step-by-step --with-decisions How to migrate from REST to GraphQL
/step-by-step --checklist Set up CI/CD for a Python monorepo
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

### Workflow

1. **Parse task** — Extract the goal or question from `$ARGUMENTS`
2. **Identify end state** — Define what "done" looks like
3. **Decompose** — Break into the smallest meaningful steps (each step = one action or one decision)
4. **Order** — Arrange steps by dependency, then by natural sequence
5. **Add rationale** — For each step, add a brief "Why:" explaining the reasoning
6. **Mark decision points** (if `--with-decisions`) — Where the path forks, list options and selection criteria
7. **Add dependencies** (if `--dependencies`) — Note which steps must complete before others can start
8. **Estimate** (if `--estimate`) — Add time ranges (e.g., "~15 min", "1-2 hours")
9. **Verify completeness** — Walk through the steps mentally; fill any gaps

### Output Format

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

### Constraints

- Each step must be a single, verifiable action — not a vague instruction like "set things up"
- Steps must be ordered so someone could follow them linearly without backtracking
- If a step requires a choice, use `[DECISION]` and list the options with trade-offs
- Never combine two unrelated actions into one step
