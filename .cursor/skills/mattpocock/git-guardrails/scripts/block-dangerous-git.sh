#!/usr/bin/env bash
# block-dangerous-git.sh — Pre-execution hook for Cursor
# Blocks destructive git operations before they run.
#
# Usage in .cursor/hooks.json:
# {
#   "hooks": [{
#     "event": "beforeShellExecution",
#     "script": "scripts/block-dangerous-git.sh \"$command\"",
#     "description": "Block dangerous git operations"
#   }]
# }

set -euo pipefail

command="$1"

# Only check git commands
if [[ ! "$command" =~ ^git[[:space:]] ]]; then
  exit 0
fi

# Force push (--force or -f, but not -ff which is a merge strategy)
if [[ "$command" =~ push.*--force ]] || [[ "$command" =~ push.*[[:space:]]-f[[:space:]] ]] || [[ "$command" =~ push.*[[:space:]]-f$ ]]; then
  echo "BLOCKED: Force-pushing is not allowed. It rewrites remote history and can destroy teammates' work."
  echo "If you need to update a PR branch, use: git pull --rebase origin <branch> && git push"
  exit 1
fi

# Delete remote branches
if [[ "$command" =~ push.*--delete ]] || [[ "$command" =~ push.*:refs/ ]]; then
  echo "BLOCKED: Deleting remote branches is not allowed. Use the GitHub UI or PR merge cleanup instead."
  exit 1
fi

# Force-delete local branches (-D uppercase)
if [[ "$command" =~ branch[[:space:]]+-D[[:space:]] ]]; then
  echo "BLOCKED: Force-deleting branches is not allowed. Use 'git branch -d' (lowercase) which checks if the branch is merged first."
  exit 1
fi

# Direct commits to main/master
if [[ "$command" =~ ^git[[:space:]]+commit ]]; then
  current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
  if [[ "$current_branch" == "main" || "$current_branch" == "master" ]]; then
    echo "BLOCKED: Direct commits to $current_branch are not allowed. Create a feature branch first:"
    echo "  git checkout -b feature/your-change"
    exit 1
  fi
fi

# --no-verify flag
if [[ "$command" =~ --no-verify ]]; then
  echo "BLOCKED: Skipping pre-commit hooks (--no-verify) is not allowed. Fix the hook errors instead."
  exit 1
fi

# All checks passed
exit 0
