## Release Ship

Lightweight shipping pipeline: domain-split commits, git push, issue creation with GitHub Project linking. For non-webui repos, also creates PRs and auto-merges.

### Repository-Specific Behavior

- **ai-platform-webui**: `commit → push → issue → report` (tmp-only mode, no PR/merge)
- **Other repos**: `commit → push → issue → PR → merge` (full pipeline)

### Usage

```
/release-ship                    # full pipeline (webui: commit→push→issue→report)
/release-ship --no-pr            # commit → push → issue (skip PR and merge)
/release-ship --no-issue         # commit → push only (skip issue creation)
/release-ship --no-merge         # commit → push → issue → PR (skip merge)
/release-ship --base dev         # specify PR base branch (non-webui only)
/release-ship --update           # force-update existing PR body (non-webui only)
```

### Workflow

1. **Pre-flight** — Check for changes, detect branch, detect repo
2. **Domain-commit** — Pre-commit hooks + domain-split commits
3. **Push** — `git push origin HEAD:tmp`
4. **Issue** — Create GitHub issues from commits, link to Project #5
5. **PR** — Create/update PR (**skipped for ai-platform-webui**)
6. **Merge** — Squash-merge PR (**skipped for ai-platform-webui**)
7. **Report** — Commit list, issue URLs, PR URL (if applicable)

### Execution

Read and follow the `release-ship` skill (`.cursor/skills/release-ship/SKILL.md`) for pipeline steps, PR template, and error handling.

### Examples

Ship changes in ai-platform-webui (tmp-only):
```
/release-ship
```

Ship changes in other repos (full pipeline):
```
/release-ship
```

Commit and push without creating issues:
```
/release-ship --no-issue
```

Stop after PR creation in non-webui repo:
```
/release-ship --no-merge
```
