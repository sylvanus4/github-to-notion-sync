## Diagnose

Run 3 parallel analysis agents (Root Cause, Error Context, Impact) to diagnose bugs and errors, synthesize a root cause, and auto-fix.

### Usage

```
/diagnose                              # analyze current error in context
/diagnose "TypeError in auth module"   # diagnose specific error message
/diagnose src/api/auth.ts              # diagnose specific file
/diagnose --no-fix                     # analysis only, no auto-fix
```

### Workflow

1. **Gather context** — Collect error message, lint errors, recent git changes, related files
2. **Parallel analysis** — 3 agents (Root Cause, Error Context, Impact) analyze simultaneously
3. **Synthesize** — Compare hypotheses, identify consensus root cause
4. **Fix** — Apply highest-confidence fix (skip with `--no-fix`)
5. **Verify** — Lint check, ensure no regressions
6. **Report** — Diagnosis with evidence, fix details, and follow-up recommendations

### Execution

Read and follow the `diagnose` skill (`.cursor/skills/diagnose/SKILL.md`) for agent prompts, output format, and error handling.

### Examples

Debug a runtime error:
```
/diagnose "TypeError: Cannot read property 'id' of undefined"
```

Investigate a slow endpoint:
```
/diagnose src/api/search.ts
```

Analysis only (no auto-fix):
```
/diagnose --no-fix "Intermittent 500 on /api/users"
```
