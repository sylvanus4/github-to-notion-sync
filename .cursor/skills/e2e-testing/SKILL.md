---
name: e2e-testing
description: >-
  Write, run, and debug Playwright E2E tests for the frontend application. Use
  when the user asks to create E2E tests, run E2E tests, debug test failures, or
  automate browser-based testing scenarios. Do NOT use for test strategy
  planning, coverage analysis, or unit test generation (use qa-test-expert).
  Korean triggers: "테스트", "생성", "계획", "디버깅".
metadata:
  version: "1.0.0"
  category: "execution"
  author: "thaki"
---
# E2E Testing Skill

Playwright 기반 E2E 테스트 작성, 실행, 디버깅 가이드.

## Project Context

- **Test dir**: `frontend/e2e/`
- **Config**: `frontend/playwright.config.ts`
- **Base URL**: `http://localhost:5173`
- **Framework**: Playwright `^1.58.2`
- **Browser**: Chromium only
- **Runner**: `pnpm test:e2e` (또는 `make test-e2e`)

## Prerequisites

E2E 테스트 실행 전 필수 환경:

```bash
# 1. 인프라 시작 (postgres, redis, pgbouncer, qdrant, minio)
make dev-infra   # 또는 docker compose up -d

# 2. DB 마이그레이션 + 시드 데이터
make db-migrate && make db-seed

# 3. 백엔드 서비스 시작 (최소: admin:8018, call-manager:8010)
docker compose -f docker-compose.yml -f docker-compose.services.yml up -d

# 4. 프론트엔드 (자동 시작됨 — playwright.config의 webServer)
cd frontend && pnpm dev
```

**Redis 참고**: `global-setup.ts`가 `autopilot-dev-redis` 또는 `aa-redis` 컨테이너의 rate-limit 키를 플러시함.

## Test File Structure

```
frontend/e2e/
├── {feature}.spec.ts      # 테스트 파일
├── global-setup.ts        # Rate-limit flush
└── helpers/
    ├── auth.ts            # loginAs() 헬퍼
    └── setup.ts           # 커스텀 fixture 확장점
```

## Writing Tests

### 1. 기본 구조

```typescript
import { test, expect } from "@playwright/test";
import { loginAs } from "./helpers/auth";

test.describe("Feature Name", () => {
  test.beforeEach(async ({ page }) => {
    await loginAs(page);  // 인증 필요 시
  });

  test("should do something", async ({ page }) => {
    await page.goto("/route");
    await expect(page.getByRole("button", { name: /action/i })).toBeVisible();
  });
});
```

### 2. 인증 패턴

```typescript
// 로그인 (기본: minjun@demo.example / changeme123)
await loginAs(page);
await loginAs(page, "admin@demo.example", "adminpass");

// 로그아웃 상태 보장
async function ensureLoggedOut(page: Page) {
  await page.goto("/login", { waitUntil: "networkidle" });
  await page.evaluate(() => localStorage.clear());
  await page.reload({ waitUntil: "networkidle" });
}
```

### 3. Selector 우선순위

1. **`data-testid`**: `page.getByTestId("chatbot-fab")` — 가장 안정적
2. **Role + name**: `page.getByRole("button", { name: /start call/i })` — 시맨틱
3. **Text**: `page.getByText("Adoption Rate")` — 간단한 경우
4. **CSS selector**: `page.locator('input[type="email"]')` — 최후 수단

새 컴포넌트에 `data-testid` 속성 추가를 권장.

### 4. API Mocking

백엔드 의존성 없이 테스트할 때:

```typescript
await page.route("**/api/v1/calls/*/summary", async (route) => {
  if (route.request().method() === "GET") {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ data: mockData, error: null, meta: {} }),
    });
  } else {
    await route.continue();
  }
});
```

### 5. 파일 업로드

```typescript
const fileInput = page.getByTestId("audio-file-input");
await fileInput.setInputFiles({
  name: "test.wav",
  mimeType: "audio/wav",
  buffer: Buffer.from("fake-audio-data"),
});
```

## Running Tests

```bash
# 전체 실행
cd frontend && pnpm test:e2e

# UI 모드 (디버깅에 유용)
pnpm test:e2e:ui

# 특정 파일만
npx playwright test e2e/auth.spec.ts

# 특정 테스트만
npx playwright test -g "login with valid credentials"

# headed 모드 (브라우저 표시)
npx playwright test --headed

# 디버그 모드 (step-by-step)
npx playwright test --debug
```

## Debugging Failures

### 실패 원인별 대응

| 증상 | 원인 | 해결 |
|------|------|------|
| `toHaveURL` 타임아웃 | 로그인 실패 / rate-limit | Redis rate-limit 키 확인, `make db-seed` 재실행 |
| `toBeVisible` 타임아웃 | 컴포넌트 렌더링 지연 | `timeout` 옵션 증가, `waitUntil: "networkidle"` 추가 |
| `ERR_CONNECTION_REFUSED` | 백엔드 미실행 | `docker compose ps`로 서비스 상태 확인 |
| 인증 관련 실패 | 시드 데이터 없음 | `make db-seed` 실행 |
| opacity 체크 필요 | CSS 애니메이션 hide | `toHaveCSS("opacity", "0")` 사용 |

### Trace & Screenshot

- **Trace**: 첫 번째 재시도에서 자동 기록 (`trace: "on-first-retry"`)
- **Screenshot**: 실패 시 자동 캡처 (`screenshot: "only-on-failure"`)
- **HTML 리포트**: `npx playwright show-report`

### 디버깅 명령어

```bash
# trace 파일 보기
npx playwright show-trace trace.zip

# codegen으로 selector 찾기
npx playwright codegen http://localhost:5173
```

## Routes & Features

테스트 대상 라우트 참조:

| Route | Feature | Auth |
|-------|---------|------|
| `/login` | 로그인 | Public |
| `/call` | 통화 화면 | Protected |
| `/call/:id/summary` | 통화 요약 | Protected |
| `/dashboard` | 대시보드 | Protected |
| `/knowledge` | 지식 관리 | Protected |
| `/admin/*` | 관리자 페이지 | Admin only |

## Naming Convention

- 파일명: `{feature}.spec.ts` (예: `auth.spec.ts`, `call-flow.spec.ts`)
- describe: feature 이름 (예: `"Authentication"`, `"Call Flow"`)
- test: `"should ..."` 또는 동작 설명 (예: `"login with valid credentials redirects to /call"`)

## Checklist for New Tests

새 E2E 테스트 작성 시 확인:

- [ ] `@playwright/test`에서 `test`, `expect` import
- [ ] 인증 필요 시 `loginAs()` 헬퍼 사용
- [ ] 외부 API 의존 시 `page.route()` mock 적용
- [ ] timeout은 적절한 값으로 설정 (기본 5000~10000ms)
- [ ] `data-testid` 기반 selector 우선 사용
- [ ] 테스트 간 상태 격리 (localStorage clear 등)

## Additional Resources

- 기존 테스트 파일별 상세 패턴: [references/reference.md](references/reference.md)
- Playwright 공식 문서: https://playwright.dev/docs/intro

## Examples

### Example 1: Standard usage
**User says:** "e2e testing" or request matching the skill triggers
**Actions:** Execute the skill workflow as specified. Verify output quality.
**Result:** Task completed with expected output format.

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Unexpected input format | Validate input before processing; ask user for clarification |
| External service unavailable | Retry with exponential backoff; report failure if persistent |
| Output quality below threshold | Review inputs, adjust parameters, and re-run the workflow |
