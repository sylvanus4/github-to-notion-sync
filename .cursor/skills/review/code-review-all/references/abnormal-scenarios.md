# 30 Abnormal Behavior Scenarios — Agent 2 Reference

Imagine 30 unexpected actions a real user (or abusive user) could perform. For each scenario, determine whether a bug exists by examining the actual source code.

**Rules:**
- **Total scenario count**: Select exactly 30 scenarios from the 40 templates below. Adapt each scenario to the actual code found during review. The templates are a pool — pick the most relevant ones for the detected stack.
- If a category does not apply (stack flag inactive), skip it entirely and redistribute its scenario slots to other applicable categories to maintain exactly 30 total.
- Each scenario MUST be grounded in actual code logic found during review — no hypothetical assessments.
- For scenarios marked as bugs, provide file:line evidence.

## Scenario Report Format

```
| # | 시나리오 | 버그 여부 | 심각도 | 설명 |
|---|---------|----------|--------|------|
| 1 | (구체적 상황) | ✅ 버그 있음 / ✅ 안전 | Critical/High/Medium/Low/없음 | (코드 근거 포함 설명) |
```

---

## Category 1: Timing / Concurrency (5+ scenarios)

Test what happens when operations overlap or are interrupted.

| # | Scenario Template |
|---|-------------------|
| 1 | User force-quits the app while a save/write operation is in progress |
| 2 | User rapidly clicks the same button 10+ times in under 1 second |
| 3 | User navigates to a different screen while an async operation is still running |
| 4 | User opens two windows/tabs and performs the same action simultaneously |
| 5 | User clicks back/cancel during a network request that modifies server state |
| 6 | User triggers a long operation, then triggers it again before the first completes |
| 7 | User submits a form, gets impatient, refreshes the page, and submits again |

**What to look for in code:**
- Missing debounce/throttle on click handlers
- No mutex/lock on concurrent write operations
- Async state updates without cancellation tokens
- Missing `AbortController` on fetch requests during navigation
- No idempotency protection on mutation endpoints

---

## Category 2: File / System (5+ scenarios)

Applies when `FLAG_RUST = true`, `FLAG_TAURI = true`, or any file I/O is present.

| # | Scenario Template |
|---|-------------------|
| 8 | File name contains special characters: emoji (📁), Korean (파일), spaces, `#`, `&` |
| 9 | Disk is full — write operation fails mid-stream |
| 10 | Target save directory has been deleted or moved by another process |
| 11 | User attempts to save to a read-only directory or file |
| 12 | Network drive / USB storage is disconnected during file operation |
| 13 | File is locked by another process when app tries to read/write |
| 14 | File path exceeds OS maximum path length (260 chars on Windows) |

**What to look for in code:**
- `fs::write()` / `fs.writeFile()` without error handling
- Path construction using string concatenation (not `Path::join` or `path.join`)
- Missing existence check before read operations
- No atomic write pattern (write to temp → rename)
- Hardcoded path separators (`/` vs `\`)

---

## Category 3: Input / Data (5+ scenarios)

Test boundary and malicious inputs.

| # | Scenario Template |
|---|-------------------|
| 15 | User submits an empty string where input is required |
| 16 | User pastes 1,000,000+ characters into a text field at once |
| 17 | User pastes rich text (HTML, RTF) via clipboard into a plain text field |
| 18 | User inputs special Unicode: zero-width joiner (ZWJ), RTL override (U+202E), surrogate pairs |
| 19 | User inputs strings that break JSON: unescaped `"`, `\`, null byte (`\x00`) |
| 20 | User inputs negative numbers, `0`, `MAX_INT`, `NaN`, `Infinity` in numeric fields |
| 21 | User submits form with only whitespace characters |

**What to look for in code:**
- No input length limit (`maxLength` on frontend, validation on backend)
- No sanitization of control characters
- Direct string interpolation into JSON/SQL/HTML
- Number parsing without range validation
- Missing `.trim()` before empty check

---

## Category 4: Settings / State (5+ scenarios)

Test configuration corruption and state persistence edge cases.

| # | Scenario Template |
|---|-------------------|
| 22 | User manually edits the config/settings file with a text editor, introducing malformed JSON/TOML |
| 23 | User force-quits during onboarding/tutorial, then restarts the app |
| 24 | User changes the save path to a non-existent directory |
| 25 | User rapidly toggles language/theme/settings back and forth 20+ times |
| 26 | App loads a settings file from a previous version with different schema |
| 27 | User clears app data / localStorage but keeps the app running |

**What to look for in code:**
- Config file parsing without fallback to defaults
- No migration path for settings schema changes
- Settings state not validated after load
- UI not debouncing rapid setting changes
- Missing onboarding completion state persistence

---

## Category 5: Malicious Behavior (5+ scenarios)

Test deliberate abuse and manipulation.

| # | Scenario Template |
|---|-------------------|
| 28 | User opens DevTools and modifies DOM values (hidden fields, disabled buttons) |
| 29 | User directly modifies localStorage / IndexedDB / app data files |
| 30 | User injects `<script>alert(1)</script>` into a contentEditable area or text input |
| 31 | (FLAG_TAURI) User calls IPC/invoke endpoints directly from DevTools console |
| 32 | User modifies license/authentication files or tokens on disk |
| 33 | User intercepts and replays/modifies API requests via proxy (Burp Suite, mitmproxy) |

**What to look for in code:**
- `innerHTML`, `dangerouslySetInnerHTML`, `v-html` with user-controlled content
- Client-side-only validation without server-side mirror
- No integrity check on config/data files
- IPC commands without parameter validation
- API endpoints trusting client-provided user IDs or roles

---

## Category 6: Environment / System (5+ scenarios)

Test OS-level and hardware edge cases.

| # | Scenario Template |
|---|-------------------|
| 34 | Display resolution at extreme values: 800×600, 4K, 8K, ultra-wide |
| 35 | System clock changed to a date in the past or far future |
| 36 | Computer enters sleep/hibernate mode and resumes during active operation |
| 37 | System runs out of available memory during app operation |
| 38 | OS dark/light mode toggles at runtime while app is running |
| 39 | System language or locale changes while app is running |
| 40 | App runs with minimal permissions (no write access to home directory) |

**What to look for in code:**
- Hardcoded dimensions or breakpoints without responsive handling
- `Date.now()` / `SystemTime::now()` used for token expiry without clock skew tolerance
- No reconnection logic after sleep/wake
- No memory pressure handling (unbounded caches, unlimited list rendering)
- No media query listeners for system theme changes
- Locale-dependent string formatting (date, number, currency)
