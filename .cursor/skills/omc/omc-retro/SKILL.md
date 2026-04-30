---
name: omc-retro
description: >-
  Dual self-evolution for the OneManCompany framework. Micro level: 1-on-1
  feedback per agent producing working principle updates (memory). Macro level:
  cross-project retrospective producing SOP and skill improvements.
  Implements the self-evolution mechanism from arXiv:2604.22446.
  Use after completing a complex multi-agent task, or when the user asks
  to reflect on agent performance. Triggers: "회고", "레트로", "retro",
  "자기 진화", "성과 평가", "에이전트 피드백", "omc retro", "1-on-1 피드백",
  "SOP 생성", "조직 회고".
  Do NOT use mid-task (finish first, then retro).
  Do NOT use for individual code review (use simplify or deep-review).
arguments: [mode]
---

# OMC Retro: Dual Self-Evolution

Implements the self-evolution mechanism from the OMC framework.
No model retraining needed -- evolution happens through memory and skill updates.

## Two Levels of Evolution

```
Micro (1-on-1)                    Macro (Retrospective)
  |                                 |
  v                                 v
CEO feedback                     COO-led session
  |                                 |
  v                                 v
Working Principles               SOP (Standard Operating Procedure)
update per agent                  generation/update for the org
  |                                 |
  v                                 v
Memory: feedback type             Skill file: update or create
```

## Mode Selection

`$mode` determines which level to run:

| Mode | When | Output |
|------|------|--------|
| `micro` | After a single task with issues | Feedback memories |
| `macro` | After 3+ tasks or a complex project | SOP + skill updates |
| `full` (default) | After any significant work | Both micro + macro |
| `hr` | Periodic evaluation | Performance report + recommendations |

## Micro Evolution: 1-on-1 Feedback

For each agent that participated in the completed task:

### Step 1: Performance Assessment

Evaluate on 4 dimensions:

| Dimension | Score 1-5 | Evidence |
|-----------|-----------|----------|
| **Quality** | Did the output meet acceptance criteria? | Review results |
| **Efficiency** | Was the model tier appropriate? Could haiku have done it? | Token usage |
| **Reliability** | How many review iterations needed? | Retry count |
| **Scope** | Did the agent stay within its task boundary? | Output vs. spec |

### Step 2: Root Cause for Low Scores

For any dimension scoring <= 2:
- Was the prompt unclear? -> Improve prompt template
- Was the wrong agent type selected? -> Update talent-market heuristics
- Was the model too weak? -> Escalate tier for this task type
- Was the task too broad? -> Decompose further next time

### Step 3: Write Feedback Memory

For actionable insights, write to memory:

```markdown
---
name: omc-feedback-[date]-[topic]
description: [one-line summary of the lesson]
type: feedback
---

[Rule: what to do differently]
**Why:** [what happened and why it was suboptimal]
**How to apply:** [when this guidance kicks in]
```

Only write memories for non-obvious lessons. Don't memorize:
- "Tests should pass" (obvious)
- "Use the right model" (too vague)
- Session-specific details that won't recur

## Macro Evolution: Organizational Retrospective

Run after completing 3+ tasks or one complex multi-agent project.

### Step 1: Pattern Extraction

Review the recent work and identify:

1. **Recurring successes**: What org patterns consistently worked?
   - Which agent compositions delivered on first try?
   - Which model tier assignments were consistently right?
   - Which skill combinations were effective?

2. **Recurring failures**: What org patterns consistently failed?
   - Which agent types struggled with which tasks?
   - Where did the DAG structure cause bottlenecks?
   - Which review cycles burned the most iterations?

3. **Gaps**: What capabilities were missing?
   - Tasks where no existing skill fit
   - Tasks where manual intervention was needed
   - Integration points that broke

### Step 2: SOP Generation

For each recurring pattern, generate a Standard Operating Procedure:

```
## SOP: [Pattern Name]

### When to Use
[Trigger conditions]

### Org Structure
[Which agents, which models, which skills]

### Execution Order
[DAG structure]

### Quality Criteria
[How to verify success]

### Known Pitfalls
[What to watch for]
```

SOPs are stored as skill files if they encode a reusable workflow,
or as memory entries if they encode a heuristic.

### Step 3: Skill Improvement Recommendations

For skills that were used, assess:
- Should the skill be updated with new patterns?
- Should new skills be created for gap areas?
- Should underperforming skills be deprecated?

Output recommendations to CEO:
```
## Skill Recommendations

### Update
- [skill-name]: Add [what] because [why]

### Create
- [new-skill-name]: For [use case] because [gap identified]

### Deprecate
- [skill-name]: Because [reason, e.g., superseded by better approach]
```

## HR Mode: Performance Evaluation

Based on the OMC paper's HR mechanism:

### Performance Tracking

Track per-skill/agent-type performance across sessions using memory:

```markdown
---
name: omc-hr-[agent-type]
description: Performance record for [agent-type] agents
type: project
---

Last 3 evaluations:
1. [date]: [score] - [task summary]
2. [date]: [score] - [task summary]
3. [date]: [score] - [task summary]

Trend: [improving|stable|declining]
```

### Evaluation Criteria

| Grade | Score | Action |
|-------|-------|--------|
| A | 4.5-5.0 | Keep, prefer for similar tasks |
| B | 3.5-4.4 | Keep, monitor |
| C | 2.5-3.4 | PIP: add specific guidance to prompts |
| D | 1.0-2.4 | Offboard: stop using for this task type |

### PIP (Performance Improvement Plan)

When an agent type scores C:
1. Identify the specific failure mode
2. Add targeted instructions to the agent's prompt template
3. Re-evaluate on next 2 tasks
4. If still C or below -> downgrade to D (offboard)

### Offboarding

When an agent type scores D:
1. Write a memory noting this agent type is not suitable for [task type]
2. Update talent-market heuristics to avoid this match
3. Suggest alternative agent type or skill to CEO

## Output Format

```
## OMC Retrospective - [date]

### Micro Feedback
| Agent | Type | Quality | Efficiency | Reliability | Scope | Action |
|-------|------|---------|-----------|-------------|-------|--------|
| ...   | ...  | ...     | ...       | ...         | ...   | ...    |

### Macro Patterns
**Successes:** [list]
**Failures:** [list]
**Gaps:** [list]

### SOPs Generated
[list with links]

### Skill Recommendations
[update/create/deprecate]

### HR Status
[summary of performance trends]

### Memories Written
[list of new feedback memories]
```
