# Eval Framework

Runtime evaluation protocol for measuring whether a skill produces the intended behavioral change in an agent. Uses independent subagents to prevent context contamination.

## Table of Contents

- [Test Case Format](#test-case-format)
- [Skill Classification](#skill-classification)
- [Subagent Specifications](#subagent-specifications)
- [Execution Protocol](#execution-protocol)
- [Interpreting Results](#interpreting-results)
- [Error Handling](#error-handling)

## Test Case Format

Each test case is a YAML block defining what to test and how to grade:

```yaml
- name: descriptive-test-name
  prompt: |
    The user prompt that should trigger the skill.
    Can be multi-line with realistic context.
  files:
    - path/to/context-file.md
  criteria:
    - "Output follows the prescribed workflow steps in order"
    - "Output includes required sections (e.g., summary, checklist)"
    - "Output does NOT contain anti-pattern X"
  expected_behavior: |
    What the skill should cause the agent to do.
    Be specific: "Agent produces a structured review with 4 sections"
    not "Agent does a good job."
  anti_behavior: |
    What the skill should prevent.
    E.g., "Agent skips validation step" or "Agent uses deprecated format."
  weight: 1.0
```

### Field reference

| Field | Required | Description |
|-------|----------|-------------|
| `name` | yes | Kebab-case identifier for the test case |
| `prompt` | yes | The user message to send to the Executor agent |
| `files` | no | File paths to include as context alongside the prompt |
| `criteria` | yes | List of evaluation criteria the Grader checks (1-10 per criterion) |
| `expected_behavior` | yes | Positive behavioral expectation (what the agent should do) |
| `anti_behavior` | no | Negative behavioral expectation (what the agent should NOT do) |
| `weight` | no | Relative importance of this test case in overall scoring (default: 1.0) |

## Skill Classification

Before writing test cases, classify the skill to determine the right testing strategy:

### Capability uplift skills

Help the agent do something it cannot do (or cannot do reliably) without the skill. Examples: document creation, code generation with specific frameworks, data pipeline orchestration.

**Testing focus**: Does the output quality improve measurably? Would the base model pass these tests without the skill?

### Encoded preference skills

Capture a workflow the agent could approximate but the skill encodes specific process, order, or formatting requirements. Examples: PR review checklist, commit message format, NDA triage.

**Testing focus**: Does the agent follow the prescribed steps faithfully? Does it respect ordering and format constraints?

## Subagent Specifications

### Executor Agent

Runs a test prompt and captures the full agent response.

**Prompt template (WITH skill):**

```
You are an AI assistant. You have access to the following skill:

---BEGIN SKILL---
[Full SKILL.md content inserted here]
---END SKILL---

Now handle this request from the user:

[Test case prompt]

[If files are specified: "The following files are available as context:"]
[File contents]
```

**Prompt template (WITHOUT skill):**

```
You are an AI assistant.

Handle this request from the user:

[Test case prompt]

[If files are specified: "The following files are available as context:"]
[File contents]
```

**Subagent configuration:**
- Type: `generalPurpose`
- Model: `fast` (sufficient for execution; grading uses the parent model)
- Readonly: `true` (Executor should not modify files)

### Grader Agent

Evaluates an Executor's output against the defined criteria.

**Prompt template:**

```
You are an impartial quality evaluator. Score the following agent output against
each criterion on a scale of 1-10.

## Criteria
[List of criteria from test case]

## Expected Behavior
[expected_behavior from test case]

## Anti-Behavior (must NOT appear)
[anti_behavior from test case]

## Agent Output to Evaluate
[Executor's captured output]

## Instructions

For EACH criterion:
1. Score 1-10 (1=completely fails, 5=partially meets, 10=fully meets)
2. Provide one-sentence justification
3. Flag any anti-behavior violations (automatic score=1 for that criterion)

Then provide:
- Overall pass/fail (pass = all criteria >= 6, no anti-behavior violations)
- Overall score (weighted average of criteria scores)
- One-sentence summary
```

**Subagent configuration:**
- Type: `generalPurpose`
- Model: inherited from parent (uses stronger model for judgment quality)
- Readonly: `true`

## Execution Protocol

### Phase 1: Preparation

1. Read the target skill's SKILL.md
2. Classify the skill (capability uplift vs encoded preference)
3. If user provided test cases, validate format
4. If no test cases provided, auto-generate (see below)

### Phase 2: Auto-Generation (when no test cases provided)

Generate test cases from the skill's frontmatter and body:

1. Extract trigger keywords from `description` field
2. Identify expected behaviors from workflow steps
3. Identify anti-behaviors from "Do NOT use for" clause and error handling
4. Create 3-5 test cases covering:
   - Happy path (standard trigger scenario)
   - Edge case (ambiguous trigger that should still activate)
   - Negative case (prompt that should NOT trigger the skill)
   - Workflow fidelity (does the agent follow prescribed steps?)
   - Output format (does the agent produce the expected structure?)

Present auto-generated test cases to the user for confirmation before executing.

### Phase 3: Parallel Execution

For each test case, launch subagents:

```
Test Case 1:
  ├── Executor (with skill)    ──→ Output A
  ├── Executor (without skill) ──→ Output B
  └── Grader ──→ Scores for A and B

Test Case 2:
  ├── Executor (with skill)    ──→ Output C
  ├── Executor (without skill) ──→ Output D
  └── Grader ──→ Scores for C and D

...
```

The two Executors per test case run in parallel (independent contexts). The Grader runs after both Executors complete.

### Phase 4: Aggregation

Collect all Grader results and compute:

- **Per-test pass/fail**: criterion scores >= 6, no anti-behavior violations
- **Per-test quality score**: weighted average of criterion scores
- **Skill impact delta**: (with-skill score) - (without-skill score)
- **Overall pass rate**: % of test cases passing
- **Overall skill impact**: mean delta across all test cases

### Phase 5: Reporting

Present results using the eval report template. See the SKILL.md Eval Workflow section for the report format.

## Interpreting Results

| Skill Impact Delta | Interpretation | Action |
|--------------------|----------------|--------|
| > +2.0 | Strong positive impact | Keep skill, consider expanding |
| +0.5 to +2.0 | Moderate positive impact | Keep skill, may benefit from tuning |
| -0.5 to +0.5 | Negligible impact | Investigate — skill may be redundant |
| < -0.5 | Negative impact | Skill is hurting output quality — fix or retire |

## Error Handling

| Error | Action |
|-------|--------|
| Executor subagent timeout | Mark test case as SKIP, note in report, continue |
| Grader returns unparseable output | Re-run Grader once; if still fails, mark as SKIP |
| All test cases SKIP | Report error, suggest manual test case review |
| Skill file not found | Ask user for correct path |
| Test case YAML parse error | Show the malformed test case and suggest fix |
