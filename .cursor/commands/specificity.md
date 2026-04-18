---
description: "Force every claim to become 3x more specific — the specificity ladder pattern"
argument-hint: "<text or claim to sharpen>"
---

# Specificity Ladder

Take any claim, statement, or draft and climb the specificity ladder: replace every vague word with a concrete, measurable, falsifiable alternative. Each rung makes the output harder to fake and easier to act on.

## Usage

```
/specificity "Our platform is fast and scalable"
/specificity "The market is growing rapidly"
/specificity "We have a strong team with relevant experience"
/specificity 우리 제품은 성능이 좋고 사용하기 쉽습니다
/specificity "This will save costs and improve efficiency"
/specificity "The architecture handles high load well"
```

## Your Task

User input: $ARGUMENTS

### Workflow

1. **Identify vague language** — Scan the input for:
   - Unmeasured adjectives: "fast," "scalable," "good," "strong," "easy"
   - Directionless comparatives: "better," "more efficient," "improved"
   - Weasel quantities: "many," "some," "significant," "rapidly"
   - Unfalsifiable claims: anything that cannot be proven wrong with data
   - Hidden subjects: "it is known that," "people say," "generally"
2. **Climb 3 rungs** — For each vague element, produce 3 increasingly specific versions:
   - **Rung 1 (Directional):** Add direction and category → "Response time is under 200ms"
   - **Rung 2 (Quantified):** Add numbers and conditions → "p95 response time is 180ms under 1000 concurrent users"
   - **Rung 3 (Falsifiable):** Add measurement method and threshold → "p95 response time measured by Datadog APM stays under 200ms at 1000 RPS on 3x c5.2xlarge instances"
3. **Rewrite** — Produce the final version using Rung 2 or Rung 3 language throughout
4. **Vagueness scorecard** — Rate the before/after on a 1-10 specificity scale

### Output Format

```
## Vague → Specific Breakdown

| Original Phrase | Problem | Rung 1 | Rung 2 | Rung 3 |
|-----------------|---------|--------|--------|--------|
| "fast" | unmeasured | < 200ms | p95 180ms at 1K users | p95 180ms at 1K RPS, Datadog APM, c5.2xlarge |
| "scalable" | unfalsifiable | handles 10x growth | auto-scales to 50K RPM | K8s HPA scales 3→30 pods at 70% CPU in <90s |

## Rewritten Version

[Full text with all vague language replaced at Rung 2+ level]

## Specificity Score

- **Before:** [X]/10 — [brief reason]
- **After:** [Y]/10 — [brief reason]
```

### Constraints

- Every adjective and adverb must survive the "compared to what?" test
- Numbers must include units and conditions
- If the user's domain lacks real data, use plausible placeholder ranges with `[TBD: actual measurement]` markers rather than inventing numbers
- Do not strip rhetorical force — specific language should be MORE compelling, not more boring
- Korean input → Korean output with technical terms in English parenthetical notation
