## Superpowers TDD

Strict Test-Driven Development using the Superpowers Red-Green-Refactor cycle. Write the test first. Watch it fail. Write minimal code to pass. No exceptions.

### Usage

```
/sp-tdd [feature or bugfix to implement]
```

### The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Wrote code before the test? Delete it. Start over. No keeping it as "reference".

### Workflow

Read and follow the Superpowers `test-driven-development` skill throughout.

**For each behavior to implement, repeat this cycle:**

**RED — Write Failing Test**

- Write ONE minimal test showing what should happen
- Clear, descriptive name (no `test1`, no "and" in name)
- Test real code, not mocks (mocks only if unavoidable)

**Verify RED — Watch It Fail**

```bash
# Run the specific test
pytest tests/path/test.py::test_name -v       # Python
cd frontend && npx vitest run path/test.ts     # Frontend
go test ./path/... -run TestName -v            # Go
```

Confirm: fails because the feature is missing (not because of typos or syntax errors).

**GREEN — Write Minimal Code**

- Simplest code to pass the test — nothing more
- No future-proofing, no "while I'm here" improvements
- YAGNI: if the test doesn't require it, don't add it

**Verify GREEN — Watch It Pass**

```bash
# Same test command — must pass now
# Also run full suite to check for regressions
```

Confirm: test passes AND no other tests broken.

**REFACTOR — Clean Up**

- Remove duplication, improve names, extract helpers
- Keep tests green — don't add new behavior
- If tests break during refactor, undo and try again

**Repeat** for the next behavior.

### Verification

Read and follow the Superpowers `verification-before-completion` skill.

- Run full test suite and confirm output
- Confirm no warnings or errors in output
- Every new function/method has a test
- Each test was watched failing before implementation

### When to Use

- New features (always)
- Bug fixes (write failing test reproducing the bug first)
- Refactoring (ensure tests exist before changing code)
- Behavior changes (update tests to reflect new behavior)

### Common Rationalizations (all wrong)

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "TDD will slow me down" | TDD is faster than debugging. |
| "Need to explore first" | Fine. Throw away exploration, start with TDD. |

### Output

- Tests written before implementation (verified by watching each fail)
- Minimal implementation code
- All tests passing with clean output
- No dead code or over-engineering
