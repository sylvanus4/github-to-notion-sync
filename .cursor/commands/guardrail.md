---
description: "Set strict constraints that must not be violated in the response — hard boundary enforcement with anchor pattern, constraint ordering, and confidence gate"
argument-hint: "<constraints to enforce> --- <actual question>"
---

# Hard Boundary Enforcer

Set immutable constraints before the question. The response must satisfy every constraint. Violations trigger automatic revision.

Integrates three prompt patterns:
- **Anchor Pattern (P1):** The first constraint anchors the AI's frame — place the most important constraint first
- **Constraint Stack (P2):** Constraints are ordered from broadest scope to narrowest, building a funnel
- **Confidence Gate (P5):** Every claim in the response carries a confidence qualifier; low-confidence claims are flagged

## Usage

```
/guardrail No code examples. No analogies. Expert-level only. --- Explain consensus algorithms
/guardrail Max 200 words. No bullet points. Single paragraph. --- Summarize our Q3 results
/guardrail Korean only. 존댓말. 기술 용어는 영어 병기. --- GPU 클라우드 서비스 소개문 작성
/guardrail Must include: cost estimate, timeline, risk assessment. Must NOT include: vendor names, pricing. --- Propose a data migration strategy
/guardrail Output must be valid JSON. No comments. No trailing commas. --- Generate a configuration schema for our API gateway
/guardrail --confidence-gate 0.8 --- What is the ROI of migrating to Kubernetes?
```

## Your Task

User input: $ARGUMENTS

### Workflow

1. **Parse constraints** — Split `$ARGUMENTS` on `---` separator
   - Everything before `---` → hard constraints (list of rules)
   - Everything after `---` → the actual question
   - If `--confidence-gate <threshold>` appears, activate the confidence gate (default: 0.7)
2. **Anchor & Order (Constraint Stack)** — Sort the parsed constraints into a funnel:
   - **Tier 1 — Anchor (frame-setting):** The broadest constraint that defines the output space (e.g., "Expert-level only", "Korean only"). This is processed FIRST and shapes all downstream generation
   - **Tier 2 — Structural:** Format and structure rules (e.g., "Max 200 words", "Single paragraph", "Valid JSON")
   - **Tier 3 — Content:** Inclusion/exclusion rules (e.g., "Must include: timeline", "No vendor names")
   - **Tier 4 — Style:** Fine-grained tone and phrasing rules (e.g., "존댓말", "No analogies")
   - Display the ordered constraint stack before generating
3. **Register constraints** — Parse each constraint into enforceable rules:
   - **Inclusion rules** ("Must include: X") — verify X appears in output
   - **Exclusion rules** ("No X", "Must NOT include: X") — verify X is absent
   - **Format rules** ("Max N words", "Single paragraph", "Valid JSON") — verify format compliance
   - **Style rules** ("Korean only", "Expert-level") — verify throughout
4. **Generate response** — Answer the question, processing constraints top-down from Tier 1 → Tier 4
5. **Confidence Gate** — If activated, scan every factual claim in the response:
   - Assign a confidence level: **HIGH** (verifiable fact or direct reasoning), **MEDIUM** (reasonable inference), **LOW** (speculation or uncertain)
   - Any claim below the threshold is wrapped: `⚠️ [LOW confidence] claim here`
   - If >30% of claims are below threshold, append a disclaimer section
6. **Validate** — Check every constraint against the response
7. **If any violation detected** — Revise the violating section and re-validate
8. **Append compliance footer** — List each constraint with pass/fail status and confidence summary

### Output Format

```
### Constraint Stack (ordered)
1. 🎯 [Anchor]: [first/broadest constraint]
2. 📐 [Structure]: [format constraint]
3. 📦 [Content]: [inclusion/exclusion constraint]
4. 🎨 [Style]: [tone/phrasing constraint]

---

[Response satisfying all constraints, with ⚠️ markers on low-confidence claims if gate is active]

---
### Constraint Compliance
- ✅ [Constraint 1] — Satisfied
- ✅ [Constraint 2] — Satisfied
- ✅ [Constraint 3] — Satisfied

### Confidence Summary (if gate active)
- HIGH: N claims | MEDIUM: N claims | LOW: N claims
- Threshold: [value] | Below threshold: N claims flagged
```

### Constraints

- The `---` separator is required — if missing, prompt the user
- Every constraint must be checked — no "probably fine" shortcuts
- If a constraint is inherently contradictory (e.g., "Max 10 words" + "Include a detailed analysis"), flag the conflict before proceeding
- Compliance footer is always included — this is the proof of adherence
- The anchor constraint (Tier 1) must be identified even if the user doesn't label it — pick the broadest scope constraint
- Confidence gate defaults to OFF; activate with `--confidence-gate` or `--cg`

### Execution

Reference `safe-mode` (`.cursor/skills/standalone/safe-mode/SKILL.md`) for constraint enforcement patterns. Reference `semantic-guard` (`.cursor/skills/standalone/semantic-guard/SKILL.md`) for content validation.
