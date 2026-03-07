## Release Ship

Lightweight shipping pipeline: domain-split commits, git push, issue creation with GitHub Project linking, PR creation/update, and auto-merge — without code review overhead.

### Usage

```
/release-ship                    # full pipeline: commit → push → issue → PR → merge
/release-ship --no-pr            # commit → push → issue (skip PR and merge)
/release-ship --no-issue         # commit → push → PR → merge (skip issue creation)
/release-ship --no-merge         # commit → push → issue → PR (skip merge)
/release-ship --base dev         # specify PR base branch
/release-ship --update           # force-update existing PR body
```

### Workflow

1. **Pre-flight** — Check for changes, detect branch, extract issue number
2. **Domain-commit** — Pre-commit hooks + domain-split commits
3. **Push** — `git push origin HEAD:tmp`
4. **Issue** — Create GitHub issues from commits, link to Project #5
5. **PR** — Create new PR or update existing one with change summary and issue references
6. **Merge** — Squash-merge PR (webui: keep `tmp`; other repos: delete branch)
7. **Report** — Commit list, issue URLs, PR URL, merge status

### Execution

Read and follow the `release-ship` skill (`.cursor/skills/release-ship/SKILL.md`) for pipeline steps, PR template, and error handling.

### Examples

Ship changes from a feature branch:
```
/release-ship
```

Commit and push without creating PR:
```
/release-ship --no-pr
```

Ship without creating issues:
```
/release-ship --no-issue
```

Stop after PR creation (skip merge):
```
/release-ship --no-merge
```

Target a specific base branch:
```
/release-ship --base main
```
