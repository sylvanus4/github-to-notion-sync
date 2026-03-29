## AI Slop Cleaner

Regression-safe, smell-classified, pass-by-pass cleanup of AI-generated code. Preserves behavior while removing duplication, dead code, needless abstractions, and boundary violations.

### Usage

```
[file paths...] [--review]
```

### Actions

| Flag | Description |
|------|-------------|
| _(none)_ | Full cleanup workflow: protect → plan → classify → fix → verify |
| `--review` | Reviewer-only mode — analyzes without editing files |

### Execution

Read and follow the `omc-ai-slop-cleaner` skill (`.cursor/skills/omc-ai-slop-cleaner/SKILL.md`) for the full workflow.

### Examples

```bash
# Clean up a specific directory
/omc-ai-slop-cleaner src/services/auth/

# Clean specific files
/omc-ai-slop-cleaner src/auth/login.ts src/auth/register.ts

# Review-only mode (no edits)
/omc-ai-slop-cleaner src/services/ --review

# Clean up recent AI-generated code
/omc-ai-slop-cleaner
```
