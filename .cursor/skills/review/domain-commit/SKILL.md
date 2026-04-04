---
name: domain-commit
description: >-
  Run pre-commit hooks, fix lint errors, and create domain-split git commits
  from uncommitted changes. Use when the user asks to commit local changes, run
  pre-commit, split commits by domain, clean up the working directory, or says
  "commit my changes", "domain commit", "split commits". Do NOT use for
  single-file trivial commits, git push/pull/merge operations, or branch
  management. Korean triggers: "커밋", "생성", "수정".
metadata:
  author: "thaki"
  version: "1.1.0"
  category: "execution"
---
# Domain-Split Commit

Automates the full pre-commit + lint-fix + domain-split commit workflow for this project.

## Prerequisites

- Pre-commit hooks installed (`.pre-commit-config.yaml`)
- Commit message format: Conventional Commits — `TYPE: Summary` (50 char max, English imperative)
- Valid types: `feat`, `fix`, `docs`, `chore`, `refactor`, `style`, `test`, `perf`, `ci`, `build`, `revert`
- **`enhance` is NOT valid** — use `feat` instead (pre-commit hook rejects `enhance`)

## Workflow

### Step 1: Analyze uncommitted changes

```bash
git status --short | wc -l
git status --short | sort
```

If working directory is clean, stop and inform the user.

### Step 2: Categorize files into domains

Group files by directory prefix into commit batches. For the full domain-to-path mapping and commit type assignments, see [references/hooks-and-domains.md](references/hooks-and-domains.md).

**Critical — Untracked file safety**: `git status --short` includes both
modified tracked files (`M`) and untracked files (`??`). Both MUST be
categorized and committed. If a file path does not match any domain in
the mapping table, assign it to the **Catch-all** domain with `chore:`
type. Never silently skip untracked content files (`.md`, `.ts`, `.tsx`,
`.go`, `.py`, `.yaml`, `.json`, `.sql`, `.sh`, image files, etc.).

Only skip files matching `.gitignore` patterns (these won't appear in
`git status` output at all).

Skip empty domains. Combine small domains if fewer than 3 files.

### Step 3: Commit each domain

For each domain batch:

1. **Stage**: `git add <files>`
2. **Commit** with HEREDOC message:

```bash
git commit -m "$(cat <<'EOF'
TYPE: English summary (max 50 chars)

- Korean or English detail bullet 1
- Korean or English detail bullet 2
EOF
)"
```

3. **If pre-commit fails**:
   - `git reset HEAD <files>` to unstage
   - Read the error output and identify the failing hook
   - For hook-specific remediation steps, see [references/hooks-and-domains.md](references/hooks-and-domains.md)
   - Re-stage and commit again (new commit, never amend failed commits)

4. **If pre-commit modifies files** (black/ruff auto-fix): add modified files and create a new commit

### Step 4: Verify

```bash
git status --short   # must be empty
git log --oneline -N  # show N new commits
```

**Post-commit safety check**: If `git status --short` still shows files
after committing all domains, these are files that fell through the
mapping. Stage and commit them with `chore: Add remaining untracked
files`. The working directory MUST be clean after domain-commit
completes.

## Commit message rules (Conventional Commits)

- Format: `TYPE: Summary` (Conventional Commits)
- Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `style`, `test`, `perf`, `ci`, `build`, `revert`
- **`enhance` is NOT valid** — use `feat` instead (pre-commit hook rejects `enhance`)
- Summary: English imperative, max 50 chars, no trailing period
- Body: blank line after summary, bullet details in Korean or English, wrap at 72 chars

## Examples

### Example 1: Multi-domain commit session

User says: "변경사항 커밋해줘"

Actions:
1. `git status --short` → 8 files across `.cursor/`, `services/`, `docs/`
2. Categorize: Project config (3 files), Backend services (3 files), Documentation (2 files)
3. Commit 1: `chore: Update Cursor skill configurations`
4. Commit 2: `feat: Add retry logic to auth service`
5. Commit 3: `docs: Update API documentation`
6. Verify: `git status --short` is empty, `git log --oneline -3` shows 3 commits

Result: 3 domain-split commits with pre-commit hooks passing

## Safety rules

- **Never push to upstream** unless the user explicitly requests it
- **Never force push** to main/master
- **Never amend** commits that failed pre-commit; create new commits instead
- **Never commit** `.env`, credentials, or secret files
- Check `git stash list` and inform the user if stashes exist

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Unexpected input format | Validate input before processing; ask user for clarification |
| External service unavailable | Retry with exponential backoff; report failure if persistent |
| Output quality below threshold | Review inputs, adjust parameters, and re-run the workflow |
