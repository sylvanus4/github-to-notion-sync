---
description: "Force the AI to surface hidden assumptions before analysis — assumption audit pattern"
argument-hint: "<question or analysis request>"
---

# Assumption Audit

Before answering ANY question, explicitly list every assumption being made. Hidden assumptions are the #1 source of confident-but-wrong AI output. This command forces them into the open where they can be challenged.

## Usage

```
/assumption-audit Should we migrate from PostgreSQL to DynamoDB?
/assumption-audit Is our pricing too low for enterprise customers?
/assumption-audit Will adding a free tier increase conversion?
/assumption-audit 우리 팀에 시니어 엔지니어를 더 뽑아야 할까?
/assumption-audit Should we build this feature in-house or buy?
/assumption-audit Is Kubernetes overkill for our current scale?
```

## Your Task

User input: $ARGUMENTS

### Workflow

1. **Freeze** — Do NOT begin answering the question yet
2. **Surface assumptions** — List every assumption embedded in the question and in your likely analysis:
   - **Domain assumptions:** What industry norms or "best practices" am I assuming apply here?
   - **Scale assumptions:** What user count, data volume, or team size am I assuming?
   - **Constraint assumptions:** What budget, timeline, or resource limits am I assuming?
   - **Goal assumptions:** What does "success" mean here? Am I assuming the right metric?
   - **Technical assumptions:** What tech stack, architecture, or environment am I assuming?
   - **Audience assumptions:** Who am I assuming will read or use this output?
   - **Temporal assumptions:** What timeframe am I assuming? 3 months? 3 years?
   - **Causal assumptions:** What cause-effect relationships am I assuming are true?
3. **Classify each assumption** by risk:
   - 🟢 **Safe:** Almost certainly true regardless of context
   - 🟡 **Plausible:** True in most contexts but could be wrong
   - 🔴 **Dangerous:** Likely wrong or heavily context-dependent
4. **Challenge the reds** — For each 🔴 assumption, state what changes if it's wrong
5. **Answer with caveats** — Now answer the original question, with explicit assumption markers on any claim that depends on a 🟡 or 🔴 assumption

### Output Format

```
## Assumption Audit

### Assumptions Detected

| # | Assumption | Category | Risk | If Wrong… |
|---|-----------|----------|------|-----------|
| 1 | [assumption] | [domain/scale/goal/...] | 🟢/🟡/🔴 | [consequence] |
| 2 | [assumption] | [category] | 🟢/🟡/🔴 | [consequence] |

### Dangerous Assumptions (🔴)

**[Assumption N]:** [Detailed explanation of why this is risky and what flips if it's wrong]

---

## Answer (Assumption-Aware)

[The actual analysis, with inline markers like ⚠️[A3] where the answer depends on a non-safe assumption]

### Sensitivity Map

- If assumption [N] is wrong → [how the answer changes]
- If assumption [M] is wrong → [how the answer changes]
```

### Constraints

- Minimum 5 assumptions surfaced, even for seemingly simple questions
- At least 1 must be classified 🔴 — if everything looks safe, you're not looking hard enough
- The answer section must reference specific assumption IDs with ⚠️ markers
- Never present assumption-dependent conclusions as unconditional facts
- Korean input → Korean output with assumption category labels in English
