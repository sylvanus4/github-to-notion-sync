---
description: Review text for grammar, logic, and flow errors — specific corrections without rewriting. Preserve author's voice.
argument-hint: "<text to review> | [objective e.g. persuade, inform]"
---

# PM Proofread

Review text for grammar, logic, and flow errors — specific corrections without rewriting. References pm-toolkit skill, grammar-check sub-skill. Categorize issues as grammar, logic, or flow. Preserve author's voice.

## Usage

```
/pm-proofread Proofread this investor pitch deck intro for clarity
/pm-proofread 이 글 맞춤법, 논리, 흐름 검토해줘
```

## Workflow

### Step 1: Load skill and reference

Read the `pm-toolkit` skill (`.cursor/skills/pm-toolkit/SKILL.md`) and `references/grammar-check.md`.

### Step 2: Obtain text and objective

Request or use provided:

- Text to review (pasted or file path)
- Objective (e.g., persuade investors, inform stakeholders, clarity)
- Any style preferences (formal, casual, technical)

### Step 3: Categorize and fix issues

Scan the text and categorize issues:

- **Grammar** — Spelling, punctuation, tense, subject-verb agreement, articles
- **Logic** — Contradictions, missing steps, unclear causation, unsupported claims
- **Flow** — Awkward transitions, repetition, sentence rhythm, paragraph structure

For each issue:

- Quote the problematic passage
- Explain the issue
- Suggest a targeted fix (minimal change)
- Do NOT rewrite the entire passage unless necessary

### Step 4: Preserve voice

- Keep the author’s tone and style
- Avoid over-formalizing or changing intent
- Flag stylistic preferences (e.g., “consider X” vs “you must X”) as optional

### Step 5: Output

Deliver:

1. Error summary (count by category)
2. Fixes by category (grammar, logic, flow)
3. Priority fixes (high-impact corrections first)
4. Tone/alignment note vs stated objective
5. Corrected text (or diff-style edits) if practical

## Notes

- Do not rewrite; provide specific, minimal corrections.
- Logic issues often need author input (e.g., missing assumptions).
- For long documents, sample key sections or ask user to specify focus.
