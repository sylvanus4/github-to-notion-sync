---
name: qa-test-expert
description: Design test strategies, generate test code (pytest, Playwright, Vitest), analyze coverage, and plan regression testing. Use when the user asks about test planning, test generation, coverage improvement, or QA strategy. Do NOT use for writing or running Playwright E2E tests directly (use e2e-testing) or running the full CI pipeline (use ci-quality-gate).
metadata:
  version: "1.0.0"
  category: review
---

# QA / Test Expert

Specialist for testing the FastAPI microservices (pytest + httpx) and React frontend (Vitest + Playwright). Tests at `tests/` (integration), per-service `tests/` dirs, and `frontend/` for E2E.

## Test Strategy

### Test Pyramid

```
        /  E2E  \          — Playwright (frontend flows, 10-20 scenarios)
       / Integration \      — pytest + httpx (API contracts, 50-100 tests)
      /    Unit Tests   \   — pytest / Vitest (functions, models, 200+ tests)
```

### When to Write Which

| Layer | What to test | Tools | Location |
|-------|-------------|-------|----------|
| Unit | Pure functions, Pydantic models, utils | pytest, Vitest | `services/*/tests/`, `frontend/src/**/*.test.ts` |
| Integration | API endpoints, DB queries, service interactions | pytest + httpx + testcontainers | `tests/integration/` |
| E2E | Critical user flows end-to-end | Playwright | `frontend/e2e/` |

## Test Code Generation

### pytest Template (FastAPI endpoint)

```python
import pytest
from httpx import AsyncClient, ASGITransport

@pytest.mark.asyncio
async def test_create_resource(app, db_session):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/resources",
            json={"name": "test", "tenant_id": "t1"},
            headers={"Authorization": "Bearer <test-token>"},
        )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "test"
```

### Playwright Template (E2E)

```typescript
import { test, expect } from '@playwright/test';

test.describe('Dashboard', () => {
  test('loads dashboard with metrics', async ({ page }) => {
    await page.goto('/dashboard');
    await expect(page.getByRole('heading', { name: /dashboard/i })).toBeVisible();
    await expect(page.getByTestId('metrics-panel')).toBeVisible();
  });
});
```

### Vitest Template (React hook)

```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { useAuth } from '@/hooks/useAuth';

describe('useAuth', () => {
  it('returns authenticated state after login', async () => {
    const { result } = renderHook(() => useAuth());
    await waitFor(() => {
      expect(result.current.isAuthenticated).toBe(true);
    });
  });
});
```

## Coverage Analysis

### Targets

| Layer | Target | Measurement |
|-------|--------|-------------|
| Unit (Python) | >= 80% line coverage | `pytest --cov` |
| Unit (Frontend) | >= 70% line coverage | `vitest --coverage` |
| Integration | All public API endpoints covered | Manual checklist |
| E2E | Critical flows (login, CRUD, error states) | Scenario count |

### Coverage Commands

```bash
# Python services
pytest --cov=app --cov-report=html tests/

# Frontend
cd frontend && pnpm test -- --coverage

# Playwright
cd frontend && pnpm test:e2e
```

## Regression Testing

### Scope Determination

When a change is made, determine regression scope by:

1. **Direct impact**: Files changed → tests in same module
2. **Dependency impact**: Imports of changed module → tests of dependents
3. **API contract impact**: Changed endpoint → integration tests + downstream consumers
4. **DB schema impact**: Migration → all services using affected tables

### Regression Checklist

- [ ] All existing tests pass
- [ ] New code has corresponding tests
- [ ] Edge cases covered (empty input, max values, concurrent access)
- [ ] Error paths tested (network failure, timeout, invalid input)
- [ ] No flaky tests introduced (run 3x to verify stability)

## Examples

### Example 1: Test strategy for new feature
User says: "Plan tests for the new email channel feature"
Actions:
1. Analyze the feature scope and affected services
2. Design test pyramid: unit tests for handlers, integration tests for API, E2E for flow
3. Generate pytest and Playwright test templates
Result: Test Plan Report with prioritized test cases and code templates

### Example 2: Coverage improvement
User says: "How can I improve test coverage for the admin service?"
Actions:
1. Run `pytest --cov=app` to measure current coverage
2. Identify uncovered paths and edge cases
3. Generate test code for the highest-impact gaps
Result: Coverage analysis with generated test code for priority gaps

## Troubleshooting

### pytest fixtures not found
Cause: conftest.py missing or not in the correct directory
Solution: Ensure conftest.py exists at the test root and contains shared fixtures

### Flaky tests
Cause: Test depends on timing, network, or shared state
Solution: Add retries, use mocks for external dependencies, ensure test isolation

## Output Format

```
Test Plan Report
================
Scope: [Feature / Service / Full regression]
Date: [YYYY-MM-DD]

1. Test Strategy
   Approach: [Unit-heavy / Integration-heavy / E2E-heavy]
   Rationale: [Why this balance]

2. Test Cases
   New tests needed: [N]
   | # | Type | Description | Priority |
   |---|------|-------------|----------|
   | 1 | Unit | [description] | High |
   | 2 | Integration | [description] | High |
   | 3 | E2E | [description] | Medium |

3. Coverage Impact
   Current: [XX%] → Expected: [XX%]
   Gaps closed:
   - [Module]: [uncovered scenario]

4. Regression Scope
   Affected services: [list]
   Tests to run: [list or "full suite"]
   Estimated runtime: [X minutes]

5. Risks
   - [Risk]: [Mitigation]
```

## Additional Resources

For pytest fixtures, conftest patterns, and Playwright best practices, see [references/reference.md](references/reference.md).
