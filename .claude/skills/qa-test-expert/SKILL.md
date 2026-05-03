---
name: qa-test-expert
description: Design test strategies, generate test code (pytest, Playwright, Vitest), analyze coverage, and plan regression testing. Use for test planning, test generation, coverage improvement, or QA strategy.
---

# QA / Test Expert

Test strategy and code generation for the full stack.

## Test Pyramid

```
        /  E2E  \          — Playwright (frontend flows)
       / Integration \      — pytest + httpx (API contracts)
      /    Unit Tests   \   — pytest / Vitest (functions, models)
```

| Layer | What | Tools | Location |
|-------|------|-------|----------|
| Unit | Pure functions, models, utils | pytest, Vitest | `services/*/tests/`, `frontend/src/**/*.test.ts` |
| Integration | API endpoints, DB queries | pytest + httpx | `tests/integration/` |
| E2E | Critical user flows | Playwright | `frontend/e2e/` |

## Test Code Generation

### pytest Template
```python
@pytest.mark.asyncio
async def test_create_resource(app, db_session):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/resources", json={...})
        assert response.status_code == 201
```

### Vitest Template
```typescript
describe('ComponentName', () => {
  it('should render correctly', () => {
    render(<Component />);
    expect(screen.getByText('Expected')).toBeInTheDocument();
  });
});
```

## Coverage Analysis

- Run `pytest --cov` for Python coverage
- Run `vitest --coverage` for frontend coverage
- Target: 80% line coverage for critical paths
- Focus on branch coverage for complex logic

## Output Format

1. Current coverage assessment
2. Gap analysis (untested paths)
3. Generated test code
4. Regression test plan
5. Priority ranking for new tests

Do NOT use for: running E2E tests directly (use e2e-testing), CI pipeline (use ci-quality-gate).
