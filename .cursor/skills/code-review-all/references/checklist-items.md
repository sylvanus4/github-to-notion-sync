# 7-Item Checklist — Agent 1 Reference

Review each item against the detected stack flags. Mark each item as `[발견됨]`, `[없음]`, or `[해당없음]`.

**Rule**: `[해당없음]` is ONLY permitted when the corresponding stack flag is inactive. If the flag is active, the item MUST be checked and marked `[발견됨]` or `[없음]`.

## Finding Report Format

For every finding, use this exact format:

```
### [Severity: Critical/High/Medium/Low] 문제 제목
- **위치**: `파일명:라인번호`
- **해당 항목**: #N (항목명)
- **문제**: 무엇이 잘못되었는지 + 왜 위험한지
- **재현 시나리오**: 어떤 상황에서 터지는지
- **수정 제안**:
\`\`\`diff
- 문제 코드
+ 수정 코드
\`\`\`
```

---

## Item 1: Runtime Panic / Crash Potential

### Common (always check)

- Array/map access without existence check
- null/undefined dereference
- Division by zero
- Integer overflow on arithmetic operations

### FLAG_RUST = true

- `unwrap()`, `expect()` — enumerate ALL usage sites
- Direct index access on `Vec`, `HashMap` (use `.get()` instead)
- `from_str()`, `parse()` results not handled (`.unwrap()` or missing `match`)
- `as` casting without bounds check (e.g., `u64 as u32` overflow)

### FLAG_FRONTEND = true

- Nested object access without optional chaining (`a.b.c` without `a?.b?.c`)
- `JSON.parse()` without try-catch
- `parseInt()` / `parseFloat()` without NaN check
- Accessing `.length` on potentially null/undefined values

### FLAG_PYTHON = true

- Bare `dict[key]` without `.get()` or `in` check
- `list[index]` without bounds check
- `int()`, `float()` conversion without try-except
- `next()` on iterator without default value

### FLAG_GO = true

- Nil pointer dereference (unchecked error returns)
- Index out of range on slices
- Type assertion without comma-ok pattern

---

## Item 2: Async Processing Bugs

### Common (always check)

- Race condition: concurrent calls corrupting shared state
- Fire-and-forget: async operation result silently discarded
- Missing timeout on async operations

### FLAG_FRONTEND = true

- Missing `await` (Promise resolves after next line executes)
- Stale closure: callback captures outdated state value
- `useEffect` missing cleanup function (event listeners, subscriptions, timers)
- `useEffect` dependency array missing or incomplete
- `setState` called on unmounted component

### FLAG_RUST = true

- `Mutex` lock held across `.await` point (deadlock risk)
- `tokio::spawn` error silently dropped (no `.await` or error handler)
- `async` function without proper cancellation handling
- Shared `Arc<Mutex<T>>` contention under load

### FLAG_PYTHON = true

- `asyncio` event loop blocking with synchronous I/O
- Missing `await` on coroutine (coroutine never executed)
- Thread-unsafe shared state in async context

### FLAG_NODE = true

- Unhandled promise rejection (missing `.catch()` or try-catch)
- Callback hell with error propagation gaps
- Event emitter listener leak (no `removeListener`)

---

## Item 3: Memory / Ownership / Resource Leak

### FLAG_RUST = true

- Ownership/lifetime warnings (cargo clippy baseline)
- Excessive `Arc<Mutex<T>>` nesting increasing complexity
- `Clone` on large structs where borrowing suffices
- `Box<dyn Trait>` where generics would avoid allocation

### FLAG_FRONTEND = true

- Event listener not removed on component unmount
- `setInterval` / `setTimeout` without cleanup
- Closure capturing large objects preventing GC
- WebSocket / EventSource not closed on unmount
- Large data held in React state that should be in ref or external store

### FLAG_NODE = true

- Stream not properly closed (file handle leak)
- Database connection not returned to pool
- Temporary files not cleaned up

### FLAG_PYTHON = true

- File handle not closed (missing `with` statement)
- Database cursor not closed
- Large objects held in memory beyond necessity

---

## Item 4: Serialization / Deserialization Failure

### FLAG_TAURI = true

- `#[tauri::command]` parameter types mismatched with frontend `invoke()` arguments
- `serde` serialization failure cases (`Option`, enum variant handling)
- JS `undefined` vs Rust `None` confusion (JS `undefined` is NOT `null` in serde)
- Missing `#[serde(default)]` on optional fields
- Enum variants without `#[serde(rename_all)]` causing case mismatch

### FLAG_FRONTEND = true (API communication)

- Response type assumed without validation (cast to interface without checking)
- `undefined` vs `null` difference causing parse failure
- API response schema changed but frontend types not updated
- Missing error response body parsing

### FLAG_PYTHON = true

- Pydantic validation failure not caught (422 sent as raw error)
- `dict` key access without existence check (`KeyError`)
- JSON serialization of `datetime`, `Decimal`, `UUID` without custom encoder
- `None` values in required fields

### FLAG_GO = true

- `json.Unmarshal` into wrong type silently producing zero values
- Missing `json` struct tags
- Unexported fields not serialized

---

## Item 5: Error Handling / User Feedback Gaps

### Common (always check)

- try-catch / Result processing that silently swallows errors (empty catch block, `_ = result`)
- Error occurs but user sees no feedback (no toast, no message, no state change)
- Error logged to console only — user left staring at loading spinner
- Generic "Something went wrong" without actionable information

### FLAG_TAURI = true

- `invoke()` call without `.catch()` handler
- Rust command returns `Err` but frontend has no error handling
- IPC error messages not translated to user-facing text

### FLAG_FRONTEND = true

- API call without timeout handling (infinite loading state)
- Error during loading leaves loading state stuck (spinner forever)
- Form submission error doesn't re-enable submit button
- Network offline not detected or communicated

### FLAG_PYTHON = true

- Bare `except Exception` with `pass` or `continue`
- HTTP 500 returned with no structured error body
- Background task failure with no notification mechanism

---

## Item 6: Edge Cases

### Common (always check)

- Empty string input handling
- Extreme values: `0`, negative numbers, `MAX_INT`, empty arrays, `null`
- File not found, permission denied, disk full
- Special characters in input: Korean, emoji, `../`, `<script>`, null byte (`\x00`)
- Unicode edge cases: zero-width joiners (ZWJ), right-to-left markers, surrogate pairs

### FLAG_RUST = true

- `app_data_dir()`, `app_config_dir()` returning `None` (path not available)
- File I/O error propagation chain via `?` operator — trace the full path
- UTF-8 validation on external input (non-UTF-8 file names on some OS)

### FLAG_FRONTEND = true

- 1,000,000+ character input causing performance degradation
- RTL text, zero-width characters (ZWJ), surrogate pairs in text fields
- Paste event with rich text / HTML content
- Browser back/forward button during form submission
- Very long single word without spaces (CSS overflow)

### FLAG_PYTHON = true

- Very large file upload exceeding memory
- Concurrent requests with same resource identifier
- Timezone-naive datetime comparison with timezone-aware values

---

## Item 7: State Management Bugs

### FLAG_FRONTEND = true

- Global state pollution: one screen's mutation affects another screen
- Navigation leaves stale state (previous screen data visible on next screen)
- Persist middleware: stored value conflicts with runtime initial value after schema change
- State update ordering dependency (A must update before B, but order not guaranteed)
- Optimistic update not rolled back on server error
- Derived state computed incorrectly when source state changes

### FLAG_TAURI = true

- `State<Mutex<T>>` lock failure causes panic (poisoned mutex)
- Multi-window environment: global state shared incorrectly across windows
- Backend state and frontend state diverge after error

### FLAG_PYTHON = true

- Global mutable state in module scope (shared across requests in ASGI)
- Request-scoped state leaking to other requests
- Cache invalidation inconsistency
