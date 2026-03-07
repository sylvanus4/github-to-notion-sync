## Domain Commit

Runs pre-commit hooks, fixes lint errors, and creates domain-split git commits from all uncommitted changes in the working directory.

### Usage

```bash
/domain-commit
```

### What it does

1. Fetches the Notion commit guide (mandatory project rule)
2. Analyzes all uncommitted changes (`git status`)
3. Categorizes files by domain (db, frontend, services, shared, docs, infra, etc.)
4. For each domain:
   - Stages files → runs `git commit` (triggers pre-commit hooks)
   - If hooks fail: fixes lint errors (ruff, black, eslint, golangci-lint) and retries
5. Verifies clean working directory

### Skill Reference

This command uses the **domain-commit** skill at `.cursor/skills/domain-commit/SKILL.md`.
Read and follow the skill instructions before proceeding.

### Examples

```bash
# Commit all local changes split by domain
/domain-commit

# After running, verify with:
git log --oneline -10
git status
```

### Notes

- Does NOT push to upstream (per project rule)
- All commits pass pre-commit hooks (ruff, black, eslint, golangci-lint, gitleaks)
- Commit messages follow CONTRIBUTING.md format: `[TYPE] Summary`
