## Git Guardrails

Block dangerous git commands (force push, hard reset, clean) before they execute. Set up safety hooks for production repos.

### Usage

```
/git-guardrails                        # check current guardrail status
/git-guardrails --setup                # install safety hooks
/git-guardrails --audit                # audit recent dangerous operations
```

### Workflow

1. **Inventory** — List current git hooks and safety configurations
2. **Assess risk** — Identify unprotected branches and missing safeguards
3. **Configure** — Set up hooks to intercept destructive commands
4. **Verify** — Test that guardrails trigger correctly on simulated operations
5. **Report** — Safety posture summary with any remaining gaps

### Execution

Read and follow the `safe-mode` skill (`.cursor/skills/standalone/safe-mode/SKILL.md`) for intercepting destructive shell commands, locking file edits, and combined guard mode.

### Examples

Install guardrails:
```
/git-guardrails --setup
```

Audit safety status:
```
/git-guardrails --audit
```
