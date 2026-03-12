---
name: kwp-engineering-testing-strategy
description: >-
  Design test strategies and test plans. Trigger with "how should we test",
  "test strategy for", "write tests for", "test plan", "what tests do we need",
  or when the user needs help with testing approaches, coverage, or test
  architecture. Do NOT use for this project's pytest/Vitest/Playwright
  conventions — prefer qa-test-expert or e2e-testing skill. Korean triggers:
  "테스트 전략", "테스트 설계".
metadata:
  author: "anthropic-kwp"
  version: "1.0.0"
  category: "workflow"
---
# Testing Strategy

Design effective testing strategies balancing coverage, speed, and maintenance.

## Testing Pyramid

```
        /  E2E  \         Few, slow, high confidence
       / Integration \     Some, medium speed
      /    Unit Tests  \   Many, fast, focused
```

## Strategy by Component Type

- **API endpoints**: Unit tests for business logic, integration tests for HTTP layer, contract tests for consumers
- **Data pipelines**: Input validation, transformation correctness, idempotency tests
- **Frontend**: Component tests, interaction tests, visual regression, accessibility
- **Infrastructure**: Smoke tests, chaos engineering, load tests

## What to Cover

Focus on: business-critical paths, error handling, edge cases, security boundaries, data integrity.

Skip: trivial getters/setters, framework code, one-off scripts.

## Output

Produce a test plan with: what to test, test type for each area, coverage targets, and example test cases. Identify gaps in existing coverage.

## Examples

### Example 1: Typical request

**User says:** "I need help with engineering testing strategy"

**Actions:**
1. Ask clarifying questions to understand context and constraints
2. Apply the domain methodology step by step
3. Deliver structured output with actionable recommendations

### Example 2: Follow-up refinement

**User says:** "Can you go deeper on the second point?"

**Actions:**
1. Re-read the relevant section of the methodology
2. Provide detailed analysis with supporting rationale
3. Suggest concrete next steps
## Error Handling

| Issue | Resolution |
|-------|-----------|
| Missing required context | Ask user for specific inputs before proceeding |
| Skill output doesn't match expectations | Re-read the workflow section; verify inputs are correct |
| Conflict with another skill's scope | Check the "Do NOT use" clauses and redirect to the appropriate skill |