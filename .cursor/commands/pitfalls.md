---
description: "List 5-10 things that could go wrong with a plan, decision, or implementation — with severity, likelihood, and mitigation"
argument-hint: "<plan, decision, or implementation to stress-test>"
---

# Pitfall Detector

Proactively identify what could go wrong with any plan, decision, or implementation. For each pitfall, assess severity, likelihood, and provide a mitigation strategy.

## Usage

```
/pitfalls Migrating our primary database from PostgreSQL to CockroachDB
/pitfalls Launching a self-serve GPU rental platform
/pitfalls --pre-mortem We're planning to rewrite the frontend in Svelte
/pitfalls --murphy Adding real-time collaboration to our editor
/pitfalls 토스증권 API 기반 자동매매 시스템 구축 시 리스크
```

## Your Task

User input: $ARGUMENTS

### Mode Selection

Parse `$ARGUMENTS` for flags:

- **No flags** — Standard pitfall analysis (5-10 items, default)
- `--pre-mortem` — Frame as "It's 6 months from now and this failed. Why?" (prospective hindsight)
- `--murphy` — Apply Murphy's Law aggressively — what's the worst that can happen?
- `--with-examples` — Include real-world examples of each pitfall occurring
- `--top-3` — Output only the 3 most critical risks with deeper analysis

### Workflow

1. **Parse subject** — Extract the plan, decision, or implementation from `$ARGUMENTS`
2. **Identify failure modes** — Brainstorm 10-15 potential problems across dimensions:
   - Technical (architecture, performance, data integrity, security)
   - Organizational (team capacity, communication, dependencies)
   - Business (market timing, cost overruns, competitive response)
   - Operational (deployment, rollback, monitoring)
   - Human (user adoption, training, change resistance)
3. **Rank by risk** — Score each on severity (1-5) and likelihood (1-5); compute risk = severity × likelihood
4. **Select top items** — Present the 5-10 highest-risk pitfalls (or top 3 for `--top-3`)
5. **Add mitigations** — For each pitfall, suggest a concrete prevention or contingency action
6. **Pre-mortem narrative** (if `--pre-mortem`) — Write a 2-3 paragraph story of the failure scenario

### Output Format

```
## Pitfalls: [Subject]

| # | Pitfall | Severity | Likelihood | Risk | Mitigation |
|---|---------|----------|------------|------|------------|
| 1 | [Description] | 🔴 5/5 | 🟡 3/5 | 15 | [Action] |
| 2 | [Description] | 🟡 3/5 | 🔴 4/5 | 12 | [Action] |
| ... | ... | ... | ... | ... | ... |

### Top Risk Deep-Dive
**[Highest risk item]**: [2-3 sentences explaining why this is the biggest threat and the recommended preventive action]

### Overall Risk Assessment
[One paragraph: Is this plan fundamentally sound with manageable risks, or are there showstopper risks that need resolution first?]
```

### Constraints

- Every pitfall must be specific and actionable, not vague ("something might go wrong")
- Mitigations must be concrete actions, not "be careful"
- At least one pitfall must be non-obvious (not the first thing anyone would think of)
- If the plan is fundamentally flawed, say so directly in the overall assessment

### Execution

Reference `pm-execution` (`.cursor/skills/pm/pm-execution/SKILL.md`) pre-mortem sub-skill for prospective hindsight methodology. Apply `critical-thinking` rule (`.cursor/rules/critical-thinking.mdc`) for anti-sycophancy and failure-first elimination.
