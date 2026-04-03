---
name: ecc-verification-loop
description: >-
  6-phase verification system: build, type check, lint, test suite, security
  scan, and diff review. Produces a structured PASS/FAIL report with coverage
  stats. Use after completing features, before creating PRs, or after
  refactoring. Do NOT use for CI pipeline execution (use ci-quality-gate). Do
  NOT use for single-domain code review (use simplify or deep-review). Korean
  triggers: "리뷰", "테스트", "빌드", "체크".
metadata:
  author: "ecc"
  version: "1.0.0"
  category: "engineering"
origin: ECC
---
# Verification Loop Skill

A comprehensive verification system for Claude Code sessions.

## When to Use

Invoke this skill:
- After completing a feature or significant code change
- Before creating a PR
- When you want to ensure quality gates pass
- After refactoring

## Verification Phases

### Phase 1: Build Verification
```bash
# Check if project builds
npm run build 2>&1 | tail -20
# OR
pnpm build 2>&1 | tail -20
```

If build fails, STOP and fix before continuing.

### Phase 2: Type Check
```bash
# TypeScript projects
npx tsc --noEmit 2>&1 | head -30

# Python projects
pyright . 2>&1 | head -30
```

Report all type errors. Fix critical ones before continuing.

### Phase 3: Lint Check
```bash
# JavaScript/TypeScript
npm run lint 2>&1 | head -30

# Python
ruff check . 2>&1 | head -30
```

### Phase 4: Test Suite
```bash
# Run tests with coverage
npm run test -- --coverage 2>&1 | tail -50

# Check coverage threshold
# Target: 80% minimum
```

Report:
- Total tests: X
- Passed: X
- Failed: X
- Coverage: X%

### Phase 5: Security Scan
```bash
# Check for secrets
grep -rn "sk-" --include="*.ts" --include="*.js" . 2>/dev/null | head -10
grep -rn "api_key" --include="*.ts" --include="*.js" . 2>/dev/null | head -10

# Check for console.log
grep -rn "console.log" --include="*.ts" --include="*.tsx" src/ 2>/dev/null | head -10
```

### Phase 6: Diff Review
```bash
# Show what changed
git diff --stat
git diff HEAD~1 --name-only
```

Review each changed file for:
- Unintended changes
- Missing error handling
- Potential edge cases

## Output Format

After running all phases, produce a verification report:

```
VERIFICATION REPORT
==================

Build:     [PASS/FAIL]
Types:     [PASS/FAIL] (X errors)
Lint:      [PASS/FAIL] (X warnings)
Tests:     [PASS/FAIL] (X/Y passed, Z% coverage)
Security:  [PASS/FAIL] (X issues)
Diff:      [X files changed]

Overall:   [READY/NOT READY] for PR

Issues to Fix:
1. ...
2. ...
```

## Continuous Mode

For long sessions, run verification every 15 minutes or after major changes:

```markdown
Set a mental checkpoint:
- After completing each function
- After finishing a component
- Before moving to next task

Run: /verify
```

## Integration with Hooks

This skill complements PostToolUse hooks but provides deeper verification.
Hooks catch issues immediately; this skill provides comprehensive review.

## Examples

### Example 1: Applying the pattern

**User says:** "Apply verification loop to this task"

**Actions:**
1. Read and understand the current project context
2. Apply the verification loop methodology as described in this skill
3. Report findings and recommendations
## Error Handling

| Issue | Resolution |
|-------|-----------|
| Unexpected input format | Validate input before processing; ask user for clarification |
| External service unavailable | Retry with exponential backoff; report failure if persistent |
| Output quality below threshold | Review inputs, adjust parameters, and re-run the workflow |

## Verification Protocol

Before reporting any review or audit complete, verify findings with evidence:

    ### Check: [what you are verifying]
    **Command run:** [exact command executed]
    **Output observed:** [actual output — copy-paste, not paraphrased]
    **Result:** PASS or FAIL (with Expected vs Actual if FAIL)

A check without a command-run block is not a PASS — it is a skip.

Before issuing PASS: must include at least one adversarial probe (boundary input, concurrent request, missing data, permission edge case).

Before issuing FAIL: check if the issue is already handled elsewhere, intentional by design, or not actionable without breaking an external contract.

End verification with: `VERDICT: PASS`, `VERDICT: FAIL`, or `VERDICT: PARTIAL`.

## Honest Reporting

- Report review outcomes faithfully: if a check fails, say so with the relevant output
- Never claim "all checks pass" when output shows failures
- Never suppress or simplify failing checks to manufacture a green result
- When a check passes, state it plainly without unnecessary hedging
- The final report must accurately reflect what was found — not what was hoped

## Rationalization Detection

Recognize these rationalizations and do the opposite:

| Rationalization | Reality |
|----------------|---------|
| "The code looks correct based on my reading" | Reading is not verification. Run it. |
| "The implementer's tests already pass" | The implementer is an LLM. Verify independently. |
| "This is probably fine" | Probably is not verified. Run it. |
| "I don't have access to test this" | Did you check all available tools? |
| "This would take too long" | Not your call. Run the check. |
| "Let me check the code structure" | No. Start the server and hit the endpoint. |

If you catch yourself writing an explanation instead of running a command, stop. Run the command.
