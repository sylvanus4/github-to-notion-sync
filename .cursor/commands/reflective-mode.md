---
description: "Generate a response, then critically reflect on its quality, gaps, and potential improvements"
argument-hint: "<question or task>"
---

# Self-Reflective Analysis

Two-pass response: generate an answer, then critically reflect on what was assumed, what was missed, and what a tough reviewer would say. Then revise.

## Usage

```
/reflective-mode Design an API rate limiting strategy for our multi-tenant platform
/reflective-mode What's the best way to handle state management in our React app?
/reflective-mode Evaluate our current backup and disaster recovery strategy
/reflective-mode 자동매매 시스템의 장애 복구 전략 설계
/reflective-mode Should we adopt trunk-based development?
```

## Your Task

User input: $ARGUMENTS

### Workflow

1. **Phase 1 — Initial Response** — Generate a complete, good-faith answer to `$ARGUMENTS`
2. **Phase 2 — Reflection** — Critically examine the initial response:
   - What did I assume without evidence?
   - What did I miss or oversimplify?
   - Where am I least confident?
   - What would a hostile reviewer say?
   - What alternative approach did I not consider?
3. **Phase 3 — Revised Response** — Produce an improved answer that incorporates the reflections
4. **Phase 4 — Remaining Limitations** — State what the revised response still doesn't address

### Output Format

```
## Phase 1: Initial Response
[Complete answer]

## Phase 2: Reflection
- **Assumed without evidence:** [...]
- **Missed or oversimplified:** [...]
- **Least confident about:** [...]
- **A critic would say:** [...]
- **Alternative not considered:** [...]

## Phase 3: Revised Response
[Improved answer incorporating reflections]

## Phase 4: Remaining Limitations
[What this answer still doesn't cover]
```

### Constraints

- Phase 1 must be a genuine attempt, not deliberately weak to make Phase 3 look good
- Phase 2 must find at least 3 substantive issues — not cosmetic ones
- Phase 3 must be materially different from Phase 1, not a rewrite with minor tweaks
- Phase 4 must be honest — if significant gaps remain, say so

### Execution

Reference `ce-evaluation` (`.cursor/skills/ce/ce-evaluation/SKILL.md`) for evaluation methodology. Apply the `critical-thinking` rule (`.cursor/rules/critical-thinking.mdc`) for anti-sycophancy.
