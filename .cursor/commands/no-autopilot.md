---
description: "Avoid generic/predictable answers — force novel, non-obvious insights that a Google search wouldn't surface"
argument-hint: "<topic where you want genuine depth>"
---

# Anti-Autopilot Deep Insight

Disable pattern-matching mode. No generic answers, no "Top 5 Best Practices", no Wikipedia summaries. Force genuine depth and non-obvious insight.

## Usage

```
/no-autopilot Why do most microservice migrations fail?
/no-autopilot What's actually wrong with the current state of AI coding assistants?
/no-autopilot The real reason startups fail at Series B
/no-autopilot 한국 GPU 클라우드 시장에서 진짜 경쟁 우위는 무엇인가
/no-autopilot Why does code review rarely catch the bugs that matter?
```

## Your Task

User input: $ARGUMENTS

### Workflow

1. **Generate the "obvious" answer internally** — What would any AI give? What shows up on page 1 of Google?
2. **Discard it** — That answer is not allowed
3. **Ask: "What would a contrarian expert say?"** — Someone with 20 years of experience who disagrees with the mainstream view
4. **Find the non-obvious angle:**
   - What does everyone assume that might be wrong?
   - What second-order effect does nobody talk about?
   - What's the uncomfortable truth?
5. **Support with specifics** — Concrete evidence, examples, or data. Not hand-waving
6. **Challenge your own take** — Present the strongest counterargument to your novel insight

### Output Format

```
## [Topic]

### The Obvious Answer (Discarded)
[1 sentence: what everyone says]

### The Non-Obvious Insight
[Your actual answer — specific, evidence-backed, potentially uncomfortable]

### Supporting Evidence
[Concrete examples, data, or case studies]

### Counterargument
[The strongest case against your insight]

### Why I Still Stand By This
[Final 2-3 sentences]
```

### Constraints

- If your answer could appear on the first page of a Google search for the topic, it's not deep enough
- No lists of "best practices" — those are autopilot outputs
- The insight must be specific enough to be falsifiable — not vague wisdom
- You must genuinely challenge your own novel take, not strawman it

### Execution

Apply the `critical-thinking` rule (`.cursor/rules/critical-thinking.mdc`), specifically the Karpathy Opposite Direction Test: after completing the analysis, construct the strongest case for the opposite conclusion.
