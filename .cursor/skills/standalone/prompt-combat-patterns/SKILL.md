---
name: prompt-combat-patterns
description: >-
  Tactical prompt pattern selector and composer. Diagnoses prompt weaknesses,
  prescribes the right combat pattern (Anchor, Constraint Stack, Persona
  Boundary, Failure Injection, Confidence Gate, Step Separator, Compression
  Command, Assumption Audit, Reframe Test, Specificity Ladder), and composes
  multi-pattern stacks for complex tasks. Complements prompt-architect
  (framework selection) and prompt-transformer (polishing) with pattern-level
  tactical composition. Use when the user asks to "diagnose this prompt",
  "which pattern should I use", "compose patterns", "stack patterns", "prompt
  combat", "prompt patterns", "tactical prompt", "fix my prompt with patterns",
  "프롬프트 패턴", "패턴 진단", "패턴 조합", "전술적 프롬프트", or wants to select and
  layer specific prompt engineering patterns onto existing prompts. Do NOT use
  for framework-level prompt restructuring (use prompt-architect). Do NOT use
  for general prompt polishing without pattern selection (use
  prompt-transformer). Do NOT use for creating new skills (use create-skill).
  Do NOT use for writing documentation (use technical-writer).
metadata:
  author: "thaki"
  version: "1.0.0"
  source: "10 Prompt Patterns — @thisguyknowsai thread"
  category: "execution"
---

# Prompt Combat Patterns — Tactical Pattern Composition

Select, diagnose, and compose the 10 prompt combat patterns to eliminate specific weaknesses in AI prompts. Each pattern targets a precise failure mode.

## Pattern Arsenal

| # | Pattern | Targets | Command |
|---|---------|---------|---------|
| P1 | **Anchor** | Frame drift, buried intent | `/guardrail` (Tier 1) |
| P2 | **Constraint Stack** | Constraint disorder, missed rules | `/guardrail` (Tier 1-4) |
| P3 | **Persona Boundary** | Role drift, competence bleed | `/act-as` |
| P4 | **Failure Injection** | Generic output, vague responses | `/anti-example` |
| P5 | **Confidence Gate** | Hallucination, false certainty | `/guardrail --confidence-gate` |
| P6 | **Step Separator** | Skipped steps, rushed execution | `/step-by-step --checkpoint` |
| P7 | **Compression Command** | Verbose, bloated output | `/tldr`, `/compress` |
| P8 | **Assumption Audit** | Hidden assumptions, false premises | `/assumption-audit` |
| P9 | **Reframe Test** | Confirmation bias, one-sided analysis | `/reframe` |
| P10 | **Specificity Ladder** | Vague claims, unmeasurable statements | `/specificity` |

## Modes

### Mode 1: `diagnose`

Analyze a prompt (or AI output) and identify which patterns would fix its weaknesses.

**Trigger:** "diagnose this prompt", "what's wrong with this prompt", "why is my output bad"

**Workflow:**

1. **Read the prompt or output** — Accept user's prompt text or a sample of unsatisfying AI output
2. **Scan for 10 failure signatures:**

| Failure Signature | Detected By | Prescribed Pattern |
|---|---|---|
| No framing constraint at the top | First line is the question, not a constraint | P1 Anchor |
| Constraints are unordered or scattered | Rules appear randomly, not funnel-ordered | P2 Constraint Stack |
| Role adopted but drifts into other domains | Advice outside the persona's competence | P3 Persona Boundary |
| Output is generic / could be anyone's answer | No distinctive style, no concrete details | P4 Failure Injection |
| Claims presented without qualification | "X is true" without evidence level | P5 Confidence Gate |
| Multi-step process executed without verification | Steps skipped or batched together | P6 Step Separator |
| Output is 3x longer than necessary | Padding, repetition, throat-clearing | P7 Compression Command |
| Answer relies on unstated assumptions | "Assuming you mean..." never said | P8 Assumption Audit |
| Analysis is one-sided, no counter-argument | Only pros listed, no cons explored | P9 Reframe Test |
| Claims use vague language | "significant", "fast", "many", "good" | P10 Specificity Ladder |

3. **Score severity** — Rate each detected failure as HIGH / MEDIUM / LOW
4. **Prescribe** — Recommend the top 1-3 patterns to apply, ordered by impact
5. **Show the fix** — Demonstrate how the prompt would look after applying each prescribed pattern

**Output Format:**

```
## Prompt Diagnosis

### Failures Detected
1. 🔴 [HIGH] [Failure description] → **Rx: P[N] [Pattern Name]**
2. 🟡 [MEDIUM] [Failure description] → **Rx: P[N] [Pattern Name]**
3. 🟢 [LOW] [Failure description] → **Rx: P[N] [Pattern Name]**

### Prescription
Apply in this order:
1. **P[N] [Pattern]** — [one-line explanation of what it fixes]
2. **P[N] [Pattern]** — [one-line explanation]

### Before / After
**Before:**
> [original prompt]

**After (with P[N] + P[N] applied):**
> [improved prompt]
```

### Mode 2: `apply`

Apply a specific pattern (or patterns) to a given prompt.

**Trigger:** "apply failure injection to this", "add confidence gate", "use pattern 4"

**Workflow:**

1. **Parse request** — Extract which pattern(s) to apply and the target prompt
2. **Apply each pattern** according to its rules:
   - **P1 Anchor:** Move the most important constraint to the very first line
   - **P2 Constraint Stack:** Reorder all constraints from broadest (Tier 1) to narrowest (Tier 4)
   - **P3 Persona Boundary:** Add an explicit "Hard Boundary" section defining what the persona will NOT do
   - **P4 Failure Injection:** Insert a negative example block: "Do NOT produce output like: [bad example]"
   - **P5 Confidence Gate:** Append: "For every factual claim, indicate confidence: HIGH / MEDIUM / LOW"
   - **P6 Step Separator:** Add: "After completing each step, pause and report status. Do not proceed to the next step until confirmed."
   - **P7 Compression Command:** Prepend: "Respond in ≤N sentences. Every sentence must contain information not in the previous one."
   - **P8 Assumption Audit:** Insert before the question: "Before answering, list every assumption you're making about this question."
   - **P9 Reframe Test:** Append: "After answering, argue the opposite position with equal conviction. Then state which position is stronger and why."
   - **P10 Specificity Ladder:** Append: "Replace every vague adjective with a concrete number, comparison, or falsifiable claim."
3. **Show the result** — Display the modified prompt with pattern annotations

**Output Format:**

```
## Pattern Applied: P[N] [Name]

**Original:**
> [original prompt]

**Modified:** (changes marked with 🏷️)
> 🏷️ [P1] [Anchor constraint moved to first line]
> [rest of prompt]
> 🏷️ [P5] For every factual claim, indicate confidence: HIGH / MEDIUM / LOW
```

### Mode 3: `compose`

Stack multiple patterns for a complex task. Resolves conflicts between patterns and produces a single, coherent prompt.

**Trigger:** "compose patterns for a complex analysis", "stack P1 + P4 + P5 + P9", "build a prompt with multiple patterns"

**Workflow:**

1. **Accept the task description** — What is the user trying to accomplish?
2. **Auto-select patterns** — Based on the task type, recommend a pattern stack:

| Task Type | Recommended Stack |
|---|---|
| **Research / Analysis** | P1 + P5 + P8 + P9 + P10 |
| **Code Generation** | P1 + P2 + P4 + P6 |
| **Decision Making** | P8 + P9 + P5 + P10 |
| **Content Creation** | P3 + P4 + P7 + P10 |
| **System Design** | P1 + P2 + P6 + P8 |
| **Debugging** | P6 + P8 + P5 |
| **Review / Audit** | P2 + P5 + P9 + P10 |

3. **Resolve conflicts** — Some patterns tension against each other:
   - P7 (Compression) vs P6 (Step Separator): compression wants brevity, steps want thoroughness → apply compression within each step, not globally
   - P4 (Failure Injection) vs P9 (Reframe Test): both challenge the default → apply failure injection to the initial answer, reframe test to the conclusion
   - P3 (Persona Boundary) vs P8 (Assumption Audit): persona limits scope, assumption audit wants breadth → audit only within the persona's domain
4. **Assemble the composed prompt** — Layer patterns in this canonical order:
   1. P1 Anchor (first line, always)
   2. P3 Persona Boundary (if role-based)
   3. P2 Constraint Stack (ordered constraints)
   4. P8 Assumption Audit (before the question)
   5. [The actual question/task]
   6. P4 Failure Injection (negative examples)
   7. P6 Step Separator (execution mode)
   8. P5 Confidence Gate (qualifier requirement)
   9. P10 Specificity Ladder (precision requirement)
   10. P9 Reframe Test (counter-argument requirement)
   11. P7 Compression Command (output length limit)
5. **Output the composed prompt** with pattern labels

**Output Format:**

```
## Composed Prompt (N patterns)

**Task type:** [detected type]
**Pattern stack:** P[N] + P[N] + P[N]
**Conflict resolutions:** [any tensions and how they were resolved]

---

🏷️ P1 — [Anchor constraint]
🏷️ P3 — You are [role]. Hard boundary: [what you will NOT do].
🏷️ P2 — Constraints (ordered):
  1. [Tier 1 — broadest]
  2. [Tier 2 — structural]
  3. [Tier 3 — content]
  4. [Tier 4 — style]
🏷️ P8 — Before answering, list every assumption you're making.

[The actual question]

🏷️ P4 — Do NOT produce output like this: [negative example]
🏷️ P5 — Mark every factual claim with confidence: HIGH / MEDIUM / LOW
🏷️ P10 — Replace every vague word with a concrete, measurable alternative.
🏷️ P9 — After answering, argue the opposite position with equal conviction.
🏷️ P7 — Total output ≤ [N] sentences.
```

## Relationship to Other Skills

| Skill | Scope | When to Use |
|---|---|---|
| `prompt-architect` | **Framework selection** (CO-STAR, RISEN, etc.) | Restructuring a prompt from scratch using a research framework |
| `prompt-transformer` | **General polishing** | Making any prompt more professional without specific pattern intent |
| `prompt-combat-patterns` | **Pattern-level tactics** | Fixing specific failure modes with targeted patterns |

These three skills compose well: `prompt-architect` for structure → `prompt-combat-patterns` for tactical pattern injection → `prompt-transformer` for final polish.

## Constraints

- Never apply more than 5 patterns to a single prompt — diminishing returns and conflicting instructions
- Always show before/after when applying patterns
- Pattern labels (🏷️) must be included so the user can trace which pattern added which element
- If the user's prompt is already strong, say so — do not force patterns where none are needed
- Respect the canonical ordering when composing — anchor always first, compression always last
