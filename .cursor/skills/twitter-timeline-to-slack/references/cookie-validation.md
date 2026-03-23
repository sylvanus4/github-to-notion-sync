# Cookie Validation (Phase 0)

Before fetching tweets, verify that `TWITTER_COOKIE` is set and functional.

## Step 0a: Check .env

Read the project `.env` file and check if `TWITTER_COOKIE` is present and non-empty.

- If **missing or empty** → jump to Step 0c (Cookie Registration).
- If **present** → proceed to Step 0b.

## Step 0b: Test Cookie Validity

Run the fetch script in test mode to verify the cookie works:

```bash
cd scripts/twitter && node run_pipeline.js --fetch-only --limit 1
```

If the fetch succeeds → proceed to Phase 1.

If the fetch fails with a cookie-related error (e.g. "401", "403", "Could not authenticate", or empty timeline returned) → inform the user the cookie has expired and jump to Step 0c.

## Step 0c: Cookie Registration (Interactive)

When the cookie is missing or expired, guide the user through registration:

1. **Notify** the user:
   ```
   TWITTER_COOKIE가 설정되지 않았거나 만료되었습니다.
   브라우저에서 새 쿠키를 가져와야 합니다.
   ```

2. **Display instructions** — ask the user to provide their cookie value:
   ```
   Twitter 쿠키를 가져오는 방법:
   1. Chrome에서 x.com에 로그인
   2. F12 → Network 탭 열기
   3. 페이지를 새로고침 (F5)
   4. 아무 요청을 클릭 → Headers 탭
   5. "cookie:" 헤더의 전체 값을 복사

   복사한 쿠키 값을 붙여넣어 주세요.
   ```

3. **Receive cookie value** from the user. Once provided:
   - Validate the format: must contain `auth_token=` and `ct0=` substrings (minimum required cookies for Twitter Syndication API)
   - If invalid format → ask the user to re-copy with the full cookie header value

4. **Save to .env**:
   - Read the current `.env` file
   - If a `TWITTER_COOKIE=` line exists, replace its value with the new cookie
   - If no `TWITTER_COOKIE=` line exists, append it after the Twitter comment block
   - Write the updated `.env` file

5. **Verify** by re-running Step 0b. If it succeeds → proceed to Phase 1.
