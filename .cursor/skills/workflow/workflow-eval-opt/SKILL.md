---
name: workflow-eval-opt
description: >-
  Wrap any generation task in an evaluator-optimizer loop with defined quality
  criteria, iteration limits, and stopping conditions. Separates generation
  from evaluation for higher output quality. Use when the user asks to "refine
  this", "iterate until quality", "evaluator optimizer", "eval-opt loop",
  "quality loop", "re-evaluate", "refine output", "improve quality iteratively",
  "품질 반복", "평가 최적화", or when first-draft quality consistently falls short.
  Do NOT use when first-draft quality already meets needs. Do NOT use for
  real-time tasks requiring immediate responses. Do NOT use when evaluation
  criteria are too subjective for consistent application. Do NOT use when
  deterministic tools (linters, type checkers, test runners) can check quality
  directly — use those instead.
metadata:
  author: thaki
  version: 1.0.0
  category: orchestration
---

# Workflow Eval-Opt — Evaluator-Optimizer Loop

Wrap any generation task in an iterative refinement cycle: one agent generates, another evaluates against measurable criteria, and the generator refines based on feedback. Continues until quality threshold is met or max iterations reached.

Based on the Evaluator-Optimizer workflow pattern from Anthropic's agent workflow patterns. The key insight: generation and evaluation are different cognitive tasks. Separating them lets each agent specialize. Trades token usage and iteration time for higher output quality.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Generator task | Yes | What to generate (code, report, communication, etc.) |
| Evaluation criteria | Yes | Measurable dimensions with scoring rubric |
| Quality threshold | Yes | Minimum score to pass (e.g., 8.0/10, no Critical findings) |
| Max iterations | No | Maximum refinement cycles (default: 2) |
| Evaluator type | No | Which evaluator to use (see Evaluator Configuration) |
| Scope | No | What to re-evaluate on refinement (default: modified content only) |

## Workflow

### Step 0: Pre-flight — Define Criteria Before Generating

**CRITICAL: Define evaluation criteria BEFORE the first generation pass.**

Without upfront criteria, you risk expensive loops where the evaluator keeps finding minor issues and the generator keeps tweaking, but quality plateaus.

Criteria format:
```
Dimension 1: [name] — [what it measures] — weight: [1-10]
Dimension 2: [name] — [what it measures] — weight: [1-10]
...
Pass threshold: [minimum weighted score]
Hard fails: [conditions that auto-fail regardless of score]
```

### Step 1: Generate (First Pass)

Run the generator task. This can be:
- A direct generation in the main agent
- A subagent via the Task tool (`subagent_type: generalPurpose`)
- A skill invocation (e.g., `alphaear-reporter` for reports)

Store the output as `version_1`.

### Step 2: Evaluate

Run the evaluator on the generated output. The evaluator MUST be a separate agent or tool from the generator.

- `subagent_type`: `generalPurpose`
- `model`: `fast`
- `readonly`: `true`

The evaluator receives:
- The generated output
- The evaluation criteria and rubric
- The original task description (for context)

**Evaluator Anti-Sycophancy Guards:**
- Score the output BEFORE reading the generator's self-assessment or rationale
- Apply the "hostile reviewer" lens: "What would a senior engineer reject about this?"
- If all dimensions score >= 8, re-examine at least 2 dimensions with deliberate skepticism
- Document what the output gets WRONG before what it gets RIGHT

Evaluator output format:
```
EVALUATION:
  overall_score: [0.0-10.0]
  dimensions:
    - name: [dimension]
      score: [0.0-10.0]
      feedback: [specific, actionable feedback for improvement]
  hard_fails: [list of hard-fail conditions triggered, if any]
  pass: [true|false]
  actionable_feedback: [prioritized list of concrete improvements]
```

### Step 3: Decision Gate

| Condition | Action |
|-----------|--------|
| `pass == true` (score >= threshold, no hard fails) | **PASS** — output the result |
| `pass == false` AND `iteration < max_iterations` | **REFINE** — feed feedback to generator, go to Step 4 |
| `pass == false` AND `iteration >= max_iterations` | **BEST EFFORT** — output the highest-scoring version with quality warning |

### Step 4: Refine (Optimizer Pass)

Feed the evaluator's actionable feedback to the generator:

1. Provide the previous version and the specific feedback
2. Instruct the generator to address ONLY the feedback items (do not rewrite from scratch)
3. Apply **scope reduction**: if the output is code, only re-generate modified files. If a report, only rewrite flagged sections.
4. Store the new output as `version_{N+1}`
5. Increment iteration counter
6. Return to Step 2

### Step 5: Stopping Criteria

The loop stops when ANY of these conditions is met:

1. **Threshold met** — overall score >= quality threshold AND no hard fails
2. **Max iterations reached** — iteration counter >= max_iterations
3. **No improvement** — score delta between iterations < 0.5 (plateau detection)
4. **No actionable feedback** — evaluator returns empty feedback list
5. **Regression** — new version scores lower than previous version (keep the better one)

### Step 6: Report

```
Eval-Opt Report
===============
Task: [generation task description]
Iterations: [N] / [max]
Final Score: [X.X] / 10.0
Status: [PASS | BEST EFFORT | FAILED]

Iteration History:
  v1: [score] — [summary of feedback]
  v2: [score] — [summary of improvements]
  v3: [score] — [final state]

Quality Dimensions:
  [dimension 1]: [score] / 10
  [dimension 2]: [score] / 10
  ...

Remaining Issues: [list, if any]
Output: [version with highest score]
```

## Evaluator Configuration

Pre-built evaluator configurations for common use cases:

### For Code

- Re-run 1-2 domain review agents on modified files only
- Criteria: no Critical/High findings remain, lint passes, type checks pass
- Threshold: 0 Critical findings, <= 2 High findings
- Max iterations: 2
- Scope reduction: evaluate only modified files

### For Financial Reports

- Use `ai-quality-evaluator` skill (5-dimension scoring)
- Criteria: accuracy, hallucination detection, data consistency, coverage, actionability
- Threshold: overall score >= 8.0
- Max iterations: 2
- Hard fails: hallucination detected, data inconsistency

### For General Content

- Define custom rubric (1-10 per dimension)
- Common dimensions: clarity, completeness, accuracy, tone, structure
- Threshold: average >= 7.0 and no dimension below 5.0
- Max iterations: 3

## Examples

### Example 1: Report Quality Loop

User says: "Generate a stock analysis report and refine until quality is high."

Actions:
1. Criteria: accuracy (w:3), hallucination (w:3), consistency (w:2), coverage (w:1), actionability (w:1). Threshold: 8.0
2. Generate v1 via `alphaear-reporter`
3. Evaluate v1: score 6.8 (coverage: 5.0, hallucination: 8.0)
4. Refine: rewrite coverage-weak sections with evaluator feedback
5. Evaluate v2: score 8.4 (coverage: 7.5, hallucination: 9.0)
6. PASS — output v2
7. Report: 2 iterations, final score 8.4

### Example 2: Code Generation with Standards

User says: "Write an API endpoint that meets our security standards."

Actions:
1. Criteria: no SQL injection, input validation present, auth check present, error handling. Threshold: 0 Critical
2. Generate v1: endpoint code
3. Evaluate v1: 1 Critical (missing input validation), 1 High (no rate limiting)
4. Refine: add input validation and rate limiting
5. Evaluate v2: 0 Critical, 0 High
6. PASS — output v2
7. Report: 2 iterations, all security criteria met

### Example 3: Max Iterations Reached

User says: "Draft a customer email and iterate until perfect."

Actions:
1. Criteria: tone (w:3), accuracy (w:3), brevity (w:2), empathy (w:2). Threshold: 9.0
2. Generate v1: score 7.2
3. Refine v2: score 8.1
4. Refine v3 (max): score 8.5
5. BEST EFFORT — output v3 with warning "Quality threshold 9.0 not reached (8.5). Best version returned."
6. Report: 3 iterations, remaining gap in brevity dimension

## Error Handling

| Scenario | Action |
|----------|--------|
| Evaluator returns invalid format | Re-run evaluator once; if still invalid, use the last valid score |
| Generator fails during refinement | Keep the previous best version; report partial refinement |
| Evaluator and generator disagree fundamentally | Flag for human review; output both versions |
| Score oscillates between iterations | Stop and output the highest-scoring version |
| Evaluator criteria too vague | Halt and ask user to define measurable criteria |

## Integration

- Referenced by `mission-control` Step 2.5 for quality-critical sub-task groups
- Used by `simplify --refine`, `deep-review --refine` for post-fix re-evaluation
- Used by `today` pipeline Step 5b½ for report quality gate
- Used by `ship` Step 4.5 for quick re-evaluation of Critical/High findings
- Follows `workflow-patterns.mdc` Evaluator-Optimizer pattern definition and guardrails
- Can be nested inside `workflow-sequential` or after `workflow-parallel` aggregation

## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
