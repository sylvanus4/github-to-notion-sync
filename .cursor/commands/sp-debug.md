## Superpowers Systematic Debugging

Evidence-based debugging with the Superpowers 4-phase process — root cause investigation, pattern analysis, hypothesis testing, and verified fix. No guessing allowed.

### Usage

```
/sp-debug [error message, test failure, or symptom description]
```

### The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes. This is not negotiable.

### Workflow

Read and follow the Superpowers `systematic-debugging` skill throughout this entire process.

**Phase 1: Root Cause Investigation**

1. Read error messages and stack traces completely — don't skip past them
2. Reproduce the issue consistently (exact steps, reliable trigger)
3. Check recent changes (`git diff`, recent commits, new dependencies)
4. For multi-component systems: add diagnostic instrumentation at each component boundary, run once, then analyze where it breaks
5. Trace data flow backward from the symptom to find the source

Use project domain skills for component-specific investigation:
- **backend-expert** (`.cursor/skills/backend-expert/SKILL.md`) for FastAPI/async issues
- **frontend-expert** (`.cursor/skills/frontend-expert/SKILL.md`) for React/state issues
- **db-expert** (`.cursor/skills/db-expert/SKILL.md`) for query/connection issues

**Phase 2: Pattern Analysis**

1. Find working examples of similar code in the codebase
2. Compare working vs. broken — list every difference
3. Understand dependencies and assumptions

**Phase 3: Hypothesis and Testing**

1. State a single, specific hypothesis: "X is the root cause because Y"
2. Make the SMALLEST possible change to test it
3. One variable at a time — don't fix multiple things at once
4. If hypothesis fails, form a NEW one (don't stack fixes)
5. If 3+ fixes fail → stop and question the architecture

**Phase 4: Implementation**

Read and follow the Superpowers `test-driven-development` skill.

1. Write a failing test that reproduces the bug
2. Run it — confirm it fails for the right reason
3. Implement a single fix addressing the root cause
4. Run tests — confirm the fix works and nothing else breaks

**Verification**

Read and follow the Superpowers `verification-before-completion` skill.

- Run verification commands and confirm output before claiming success
- Ensure no new issues introduced

### Red Flags (STOP and return to Phase 1)

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- Proposing solutions before tracing data flow

### Difference from `/fix-error`

`/fix-error` focuses on error classification and report formatting. This command enforces Superpowers' iron law: systematic root cause investigation before any fix attempt, with evidence at every phase.

### Output

- Root cause analysis with evidence
- Failing test that reproduces the bug
- Minimal fix addressing the root cause
- All tests passing (verified with actual output)
