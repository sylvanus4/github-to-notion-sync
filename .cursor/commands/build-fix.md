# Build Fix

Resolve build and compile errors across the project's multi-language stack.

## Usage

```bash
# Auto-detect stack and fix all build errors
/build-fix

# Fix specific language stack
/build-fix --lang python
/build-fix --lang node
/build-fix --lang go

# Use a custom build command
/build-fix --cmd "make build"
```

## Instructions

Use the `build-error-resolver` skill to execute this command. Read the skill at `.cursor/skills/review/build-error-resolver/SKILL.md` and follow its workflow.

Key points:
- Auto-detects Python (ruff + mypy), Node.js (tsc), Go (go build) stacks
- Fixes errors in priority order: syntax → imports → types → undefined refs → config → deprecation
- Max 5 fix-verify cycles to prevent infinite loops
- Never modifies test files to fix build errors
- Reports a structured summary of fixed and remaining errors
