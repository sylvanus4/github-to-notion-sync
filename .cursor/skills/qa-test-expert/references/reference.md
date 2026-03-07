# QA / Test Expert — Reference

## pytest Fixtures (conftest.py patterns)

### Database Fixture (Integration Tests)

```python
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

@pytest_asyncio.fixture
async def db_engine():
    engine = create_async_engine(
        "postgresql+asyncpg://test:test@localhost:5433/test_db",
        echo=False,
    )
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture
async def db_session(db_engine):
    async_session = sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.rollback()
```

### FastAPI App Fixture

```python
import pytest_asyncio
from app.main import create_app

@pytest_asyncio.fixture
async def app(db_session):
    app = create_app()
    app.dependency_overrides[get_db] = lambda: db_session
    yield app
```

### Auth Token Fixture

```python
@pytest.fixture
def auth_headers():
    token = create_test_token(user_id="test-user", tenant_id="test-tenant", role="admin")
    return {"Authorization": f"Bearer {token}"}
```

## Testcontainers Pattern

For tests that need real PostgreSQL/Redis:

```python
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

@pytest.fixture(scope="session")
def postgres():
    with PostgresContainer("postgres:16-alpine") as pg:
        yield pg.get_connection_url()

@pytest.fixture(scope="session")
def redis():
    with RedisContainer("redis:7-alpine") as r:
        yield r.get_connection_url()
```

## Playwright Best Practices

### Page Object Model

```typescript
// e2e/pages/dashboard.page.ts
export class DashboardPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/dashboard');
  }

  async getMetricsCount() {
    return this.page.getByTestId('metrics-panel').count();
  }

  async waitForLoad() {
    await this.page.waitForSelector('[data-testid="dashboard-loaded"]');
  }
}
```

### Test Data Isolation

```typescript
test.beforeEach(async ({ page }) => {
  // Seed test data via API
  await page.request.post('/api/v1/test/seed', {
    data: { scenario: 'dashboard-with-metrics' },
  });
});

test.afterEach(async ({ page }) => {
  await page.request.post('/api/v1/test/cleanup');
});
```

### Screenshot on Failure

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    screenshot: 'only-on-failure',
    trace: 'on-first-retry',
  },
});
```

## Coverage Configuration

### pytest-cov (pyproject.toml)

```toml
[tool.pytest.ini_options]
addopts = "--cov=app --cov-report=html --cov-report=term-missing"

[tool.coverage.run]
omit = ["tests/*", "*/migrations/*"]

[tool.coverage.report]
fail_under = 80
```

### Vitest (vitest.config.ts)

```typescript
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      exclude: ['node_modules/', 'e2e/', '**/*.d.ts'],
      thresholds: {
        lines: 70,
        branches: 60,
      },
    },
  },
});
```

## Common Test Anti-Patterns

| Anti-pattern | Problem | Fix |
|-------------|---------|-----|
| Shared mutable state | Tests depend on execution order | Use fixtures with setup/teardown |
| Testing implementation | Tests break on refactor | Test behavior (inputs → outputs) |
| Sleeping in tests | Slow and flaky | Use `waitFor`, polling, or event-driven waits |
| Giant test functions | Hard to diagnose failures | One assertion focus per test |
| No assertions | Test always passes | Every test must assert something |
