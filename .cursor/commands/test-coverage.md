# Test Coverage Analysis

Analyze test coverage for the current project and identify untested areas that need attention.

## Usage

```bash
# Full coverage analysis
/test-coverage

# Specific directory
/test-coverage backend/app/services/

# With threshold enforcement
/test-coverage --threshold 80
```

## Instructions

1. **Detect test framework**: Scan for `pytest`, `vitest`, `jest`, or `go test` configuration
2. **Run coverage**: Execute the appropriate coverage command:
   - Python: `pytest --cov=backend/app --cov-report=term-missing --cov-report=json -q`
   - Node.js: `npx vitest run --coverage` or `npx jest --coverage`
   - Go: `go test -coverprofile=coverage.out ./... && go tool cover -func=coverage.out`
3. **Parse results**: Extract per-file and per-function coverage percentages
4. **Identify gaps**: List files with coverage below the threshold (default 70%)
5. **Prioritize**: Rank uncovered areas by risk (critical paths first, utilities last)
6. **Suggest tests**: For the top 5 uncovered areas, draft test stubs with meaningful test cases
7. **Report**: Output a structured summary with actionable recommendations

Use the `qa-test-expert` skill for detailed test strategy design and the `test-suite` skill for generating the actual test files.
