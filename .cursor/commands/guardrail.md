---
description: "Set strict constraints that must not be violated in the response — hard boundary enforcement"
argument-hint: "<constraints to enforce> --- <actual question>"
---

# Hard Boundary Enforcer

Set immutable constraints before the question. The response must satisfy every constraint. Violations trigger automatic revision.

## Usage

```
/guardrail No code examples. No analogies. Expert-level only. --- Explain consensus algorithms
/guardrail Max 200 words. No bullet points. Single paragraph. --- Summarize our Q3 results
/guardrail Korean only. 존댓말. 기술 용어는 영어 병기. --- GPU 클라우드 서비스 소개문 작성
/guardrail Must include: cost estimate, timeline, risk assessment. Must NOT include: vendor names, pricing. --- Propose a data migration strategy
/guardrail Output must be valid JSON. No comments. No trailing commas. --- Generate a configuration schema for our API gateway
```

## Your Task

User input: $ARGUMENTS

### Workflow

1. **Parse constraints** — Split `$ARGUMENTS` on `---` separator
   - Everything before `---` → hard constraints (list of rules)
   - Everything after `---` → the actual question
2. **Register constraints** — Parse each constraint into enforceable rules:
   - **Inclusion rules** ("Must include: X") — verify X appears in output
   - **Exclusion rules** ("No X", "Must NOT include: X") — verify X is absent
   - **Format rules** ("Max N words", "Single paragraph", "Valid JSON") — verify format compliance
   - **Style rules** ("Korean only", "Expert-level") — verify throughout
3. **Generate response** — Answer the question
4. **Validate** — Check every constraint against the response
5. **If any violation detected** — Revise the violating section and re-validate
6. **Append compliance footer** — List each constraint with pass/fail status

### Output Format

```
[Response satisfying all constraints]

---
### Constraint Compliance
- ✅ [Constraint 1] — Satisfied
- ✅ [Constraint 2] — Satisfied
- ✅ [Constraint 3] — Satisfied
```

### Constraints

- The `---` separator is required — if missing, prompt the user
- Every constraint must be checked — no "probably fine" shortcuts
- If a constraint is inherently contradictory (e.g., "Max 10 words" + "Include a detailed analysis"), flag the conflict before proceeding
- Compliance footer is always included — this is the proof of adherence

### Execution

Reference `safe-mode` (`.cursor/skills/standalone/safe-mode/SKILL.md`) for constraint enforcement patterns. Reference `semantic-guard` (`.cursor/skills/standalone/semantic-guard/SKILL.md`) for content validation.
