---
name: git-guardrails-claude-code
description: Pre-push safety rails that prevent dangerous git operations (force-push, branch deletion, main commits) via a beforeShellExecution hook. Use when user wants to set up git safety, prevent force-push, protect main branch, or add git guardrails.
---

# Git Guardrails for Claude Code

Safety rails that prevent common destructive git operations:

- Force-pushing to shared branches
- Deleting remote branches
- Committing directly to main/master
- Using `--no-verify` to bypass pre-commit hooks

## Installation

### Option 1: Hook Script (Recommended)

Add this to your project's `.cursor/hooks.json`:

```json
{
  "hooks": [
    {
      "event": "beforeShellExecution",
      "script": "scripts/block-dangerous-git.sh \"$command\"",
      "description": "Block dangerous git operations"
    }
  ]
}
```

Then copy the script from [scripts/block-dangerous-git.sh](./scripts/block-dangerous-git.sh) into your project.

### Option 2: Cursor Rule

If you prefer a rule-based approach (which relies on the model obeying instructions rather than hard-blocking at the shell level), add the contents of `SKILL.md` as a Cursor rule.

## What it blocks

| Pattern | Why it's dangerous |
|---------|-------------------|
| `git push --force` / `git push -f` | Rewrites remote history, can destroy teammates' work |
| `git push --force-with-lease` | Slightly safer but still destructive |
| `git push origin --delete` | Permanently removes remote branches |
| `git branch -D` | Force-deletes local branches without merge check |
| `git commit` on main/master | Direct commits bypass PR review workflow |
| `--no-verify` flag | Bypasses pre-commit hooks that enforce code quality |

## What it allows

- Normal pushes, pulls, fetches
- Creating and switching branches
- Regular commits on feature branches
- Interactive rebase on feature branches (but not force-push after)
- Merging via PR workflow

## Overriding

The hook script is intentionally hard to override from within a Claude Code session. If you genuinely need to force-push (rare), do it manually in your terminal outside of Claude Code.

If you need to customize the blocked patterns, edit the hook script directly.

## Safety Rules for Claude Code

Even without the hook installed, follow these rules:

1. **Never force-push** — `git push --force` and `git push --force-with-lease` are prohibited
2. **Never delete remote branches** — `git push origin --delete` is prohibited
3. **Never commit to main/master directly** — always use feature branches
4. **Never skip hooks** — `--no-verify` is prohibited
5. **Never force-delete branches** — use `git branch -d` (lowercase) which checks if the branch is merged

If a user asks you to perform any of these operations, explain why it's dangerous and suggest the safe alternative.
