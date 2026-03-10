---
description: "Evaluate agent session performance — define criteria, score outputs, and track quality trends"
---

# ECC Eval — Agent Performance Evaluation

## Skill Reference

Read and follow the skill at `.cursor/skills/ecc-eval-harness/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Determine Mode

- **No arguments / score**: Evaluate the current session against default criteria
- **define <criteria>**: Define custom evaluation criteria for a specific task type
- **compare <a> <b>**: Compare two approaches/configurations
- **trend**: Show quality trends across recent sessions

### Step 2: Execute

For **score** mode:
1. Collect session artifacts (code changes, test results, lint output)
2. Score against criteria:
   - **Correctness** (0-10): Does the code work? Tests pass?
   - **Quality** (0-10): Clean code, proper error handling, no dead code?
   - **Efficiency** (0-10): Minimal changes? No unnecessary files?
   - **Completeness** (0-10): All requirements met? Edge cases handled?
   - **Safety** (0-10): No secrets exposed? No destructive operations?
3. Compute weighted average (Correctness 3x, Safety 2x, others 1x)

For **define** mode:
1. Create a custom rubric with dimensions and weights
2. Save to `tasks/eval-criteria/`

For **compare** mode:
1. Score both approaches against the same criteria
2. Present a side-by-side comparison matrix

### Step 3: Report

Present scores with justifications and improvement suggestions.

## Constraints

- Always include evidence (file paths, test output) for each score
- Flag any score below 6 as needing attention
- Store evaluation results for trend tracking
