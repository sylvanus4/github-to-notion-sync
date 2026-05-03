---
name: git-guardrails
description: >-
  Set up hooks to block dangerous git commands (push, reset --hard, clean,
  branch -D, etc.) before they execute. Use when user wants to "add git
  safety", "block force push", "git guardrails", or protect against
  destructive git operations.
---

# Git Guardrails

Set up a `beforeShellExecution` hook that intercepts and blocks dangerous git commands before they execute.

## What Gets Blocked

- `git push` (any push — require explicit user action)
- `git push --force` / `push --force`
- `git reset --hard` / `reset --hard`
- `git clean -f` / `git clean -fd`
- `git branch -D`
- `git checkout .`
- `git restore .`

## Setup

### 1. Create the hook script

Create `scripts/block-dangerous-git.sh`:

```bash
#!/bin/bash

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

DANGEROUS_PATTERNS=(
  "git push"
  "git reset --hard"
  "git clean -fd"
  "git clean -f"
  "git branch -D"
  "git checkout \\."
  "git restore \\."
  "push --force"
  "reset --hard"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qE "$pattern"; then
    echo "BLOCKED: '$COMMAND' matches dangerous pattern '$pattern'. The user has prevented you from doing this." >&2
    exit 2
  fi
done

exit 0
```

Make it executable:

```bash
chmod +x scripts/block-dangerous-git.sh
```

### 2. Register the hook

Add to `.cursor/hooks.json` (or equivalent hooks configuration):

```json
{
  "hooks": [
    {
      "event": "beforeShellExecution",
      "script": "scripts/block-dangerous-git.sh",
      "description": "Block dangerous git commands"
    }
  ]
}
```

### 3. Verify

Try a blocked command and confirm it's intercepted.

## Notes

- The script reads the command from stdin as JSON (`tool_input.command`)
- Exit code 2 = block the command
- Exit code 0 = allow the command
- The blocked message is sent to stderr so the agent sees it
