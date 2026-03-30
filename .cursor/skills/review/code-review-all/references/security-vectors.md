# Hacker-Perspective Security Review — Agent 3 Reference

Goal: find attack vectors that can **crash the app** or **corrupt/steal data**. This is NOT a compliance audit — focus on practical exploitability.

Review ONLY the sections matching the detected stack flags. Skip sections where the flag is inactive.

---

## Common (Always Check)

### Data Integrity

- Can a user corrupt stored data by modifying config/data files on disk?
- If the app reads a config file, what happens when the file contains malformed data?
- Are critical data files written atomically (temp file → rename) or directly (corruption on crash)?
- Is there checksum/hash validation on important data files?

### Denial of Service (DoS)

- Can user input trigger an infinite loop? (e.g., regex backtracking, recursive parsing)
- Can user input cause memory exhaustion? (e.g., unbounded list, large file load into memory)
- Are there rate limits on expensive operations?
- Can a single malformed request crash the entire process (not just the request handler)?

### Information Disclosure

- Do error messages expose file paths, stack traces, or internal architecture?
- Are debug logs enabled in production configuration?
- Do API responses include internal IDs, database schema details, or server versions?
- Are `.env`, `.git/`, or config files accessible via web server?

---

## FLAG_FRONTEND = true

### XSS (Cross-Site Scripting)

Enumerate ALL instances of:
- `innerHTML` assignment
- `dangerouslySetInnerHTML` (React)
- `v-html` (Vue)
- `{@html ...}` (Svelte)
- Dynamic `<script>` tag creation
- `document.write()`

For each instance, verify whether the content is user-controlled. If yes → Critical.

### Code Injection

- `eval()` usage with any dynamic input
- `new Function()` with dynamic strings
- Dynamic `import()` with user-controlled path
- `setTimeout` / `setInterval` with string argument (acts as eval)
- Template literal injection in SQL/shell commands

### Client-Side Security

- Sensitive data stored in localStorage/sessionStorage without encryption
- Authentication tokens accessible via JavaScript (not httpOnly cookies)
- Client-side authorization checks without server-side enforcement
- Sensitive operations performed without CSRF protection

---

## FLAG_TAURI = true

### IPC Security

- `tauri.conf.json` → `allowlist`: check for overly permissive entries
  - `fs: { all: true }` → Critical (full filesystem access)
  - `shell: { all: true }` or `open: true` → Critical (arbitrary command execution)
  - `http: { all: true }` → High (unrestricted network access)
  - `dialog`, `notification` → generally safe
- Are all `#[tauri::command]` parameters validated on the Rust side?
- Can the frontend invoke commands with unexpected types?

### CSP (Content Security Policy)

- Check `tauri.conf.json` → `security` → `csp`
- Flag if CSP is missing entirely → High
- Flag if CSP contains `unsafe-inline` → Medium
- Flag if CSP contains `unsafe-eval` → High
- Flag if CSP allows `*` as script-src → Critical

### Path Traversal

- File save/read paths: can `../` be injected to escape the intended directory?
- Check if `app_data_dir()`, `app_config_dir()` paths are validated
- Symbolic link following: does the app follow symlinks that could point outside the sandbox?
- File picker results: are selected paths validated against an allowed directory?

---

## FLAG_RUST = true

### Input Validation

- `#[tauri::command]` or API handler parameters: are they validated before use?
- String inputs used directly in file paths without sanitization
- Numeric inputs used without range checks (buffer allocation size, array index)
- Deserialized data trusted without schema validation

### Unsafe Code

- Any `unsafe` blocks: enumerate and justify each one
- Raw pointer arithmetic
- Transmute operations
- FFI calls without proper null checks

### Panic Vectors

- Can external input trigger `unwrap()` failure?
- Can external input trigger index out of bounds?
- Can external input trigger integer overflow in release mode?

---

## FLAG_PYTHON = true

### Command Injection

- `subprocess.run()`, `subprocess.Popen()`, `os.system()`, `os.popen()` with user input
- `shlex.split()` missing before passing to subprocess
- f-string or `.format()` used to build shell commands

### SQL Injection

- Raw SQL queries with string concatenation or f-strings
- ORM queries with `.raw()`, `.execute()` using unparameterized input
- Dynamic table/column names from user input

### Path Traversal

- `open()`, `pathlib.Path()` with user-controlled path components
- Missing `os.path.abspath()` + prefix check
- Serving static files with user-controlled path (`send_file`, `FileResponse`)

### Deserialization Attacks

- `pickle.loads()` on untrusted data → Critical (arbitrary code execution)
- `yaml.load()` without `Loader=SafeLoader` → Critical
- `eval()`, `exec()` with any external input → Critical

---

## FLAG_GO = true

### Input Validation

- HTTP handler parameters used without validation
- `strconv.Atoi()` / `strconv.ParseInt()` error ignored
- Path construction with `filepath.Join()` not validated against traversal

### Concurrency Vulnerabilities

- Shared map access without sync.Mutex or sync.RWMutex (race condition → crash)
- Goroutine leak: goroutines started without cancellation context
- Channel operations without select/timeout (potential deadlock)

---

## FLAG_NODE = true

### Prototype Pollution

- `Object.assign()`, spread operator, or deep merge with user-controlled keys
- Libraries known for prototype pollution vulnerabilities (lodash < 4.17.21, etc.)

### ReDoS (Regular Expression DoS)

- User input matched against complex regex with nested quantifiers
- No timeout on regex execution

### Dependency Supply Chain

- Dependencies imported from CDN without integrity hash (`<script src="...">` without `integrity`)
- `node_modules` containing known vulnerable packages (check `npm audit` / `yarn audit`)
