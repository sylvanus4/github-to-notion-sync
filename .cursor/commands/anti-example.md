---
description: "Provide a negative example to steer AI away from generic or unwanted outputs — failure injection pattern"
argument-hint: "<task description> --- <example of what you do NOT want>"
---

# Failure Injection

Provide an example of the *wrong* answer before asking for the right one. Negative examples outperform positive examples for steering LLM output away from generic, vague, or structurally flawed responses.

## Usage

```
/anti-example Write a product launch email --- "We're excited to announce our new product! It has many great features that we think you'll love."
/anti-example Summarize our Q3 performance --- "Q3 was good. Revenue went up and costs went down. We're optimistic about Q4."
/anti-example 기술 블로그 글 작성 --- "오늘은 AI에 대해 알아보겠습니다. AI는 매우 중요한 기술입니다."
/anti-example Write a code review comment --- "This code looks wrong. Please fix it."
/anti-example Draft a sales outreach email --- "Dear Sir/Madam, I hope this email finds you well. I wanted to reach out because..."
```

## Your Task

User input: $ARGUMENTS

### Workflow

1. **Parse input** — Split `$ARGUMENTS` on `---` separator
   - Everything before `---` → the task to perform
   - Everything after `---` → the anti-example (what NOT to produce)
2. **Dissect the anti-example** — Identify exactly what makes it bad:
   - Vague claims without evidence?
   - Generic phrasing that could apply to anything?
   - Missing structure or specificity?
   - Wrong tone, register, or audience fit?
   - Clichés or filler language?
3. **Extract rejection criteria** — Convert each flaw into a concrete constraint:
   - "No unsupported superlatives" (from "many great features")
   - "No vague directional claims without numbers" (from "revenue went up")
   - "No generic openings" (from "I hope this email finds you well")
4. **Generate the response** — Produce the requested output while actively avoiding every identified flaw
5. **Contrast report** — Show a brief before/after comparison highlighting what was avoided and why

### Output Format

```
## Anti-Example Analysis

**What makes it bad:**
- [Flaw 1]: [Why it weakens the output]
- [Flaw 2]: [Why it weakens the output]
- [Flaw 3]: [Why it weakens the output]

**Rejection criteria derived:**
- ❌ [Constraint 1]
- ❌ [Constraint 2]
- ❌ [Constraint 3]

---

## Generated Output

[The actual response, free of all identified flaws]

---

## Contrast

| Anti-Example Pattern | What Was Done Instead |
|---------------------|----------------------|
| [Bad pattern 1] | [Specific replacement approach] |
| [Bad pattern 2] | [Specific replacement approach] |
```

### Constraints

- The `---` separator is required — if missing, prompt the user to provide an anti-example
- Every flaw identified in the anti-example must produce a corresponding constraint
- The generated output must violate zero of the derived constraints
- Do not mock or belittle the anti-example — treat it as useful calibration data
- If the anti-example is actually good, say so and ask for a genuinely bad example instead
