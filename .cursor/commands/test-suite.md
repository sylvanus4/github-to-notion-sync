## Test Suite

Run a full test lifecycle pipeline: 2 parallel review agents (Test Coverage, Test Quality) analyze existing tests, then a Test Generator creates missing tests, and a Test Runner executes the suite with retry logic.

### Usage

```
# Scoping modes
/test-suite                            # diff mode — test files from uncommitted changes
/test-suite today                      # today mode — all test files changed today
/test-suite full                       # full mode — entire project test audit
/test-suite project                    # alias for full mode

# Pipeline control
/test-suite --no-gen                   # review only, skip test generation
/test-suite --no-run                   # skip test execution
/test-suite full --no-gen --no-run     # full audit, review only

# Directory scope
/test-suite src/services/              # scan specific directory only
```

### Workflow

1. **Scope files** — Resolve source and test files by mode, build source-to-test mapping
2. **Parallel review** — 2 agents analyze simultaneously (Test Coverage, Test Quality)
3. **Aggregate** — Merge findings, separate into coverage gaps and quality issues
4. **Generate** — Test Generator creates missing tests and fixes quality issues (skip with `--no-gen`)
5. **Execute** — Test Runner runs the suite, fixes failures with retry (skip with `--no-run`)
6. **Report** — Coverage metrics, generated tests, execution results

### Execution

Read and follow the `test-suite` skill (`.cursor/skills/test-suite/SKILL.md`) for agent prompts, output format, and error handling.

### Examples

Post-feature test audit:
```
/test-suite
```

Full project test health check:
```
/test-suite full
```

Review-only mode (no generation or execution):
```
/test-suite full --no-gen --no-run
```
