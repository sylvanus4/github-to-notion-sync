## Superpowers Finish Branch

Structured branch completion — verify all tests pass, clean up commits, then choose how to integrate the work (merge, PR, keep, or discard).

### Usage

```
/sp-finish
```

### Workflow

**Step 1: Verification**

Read and follow the Superpowers `verification-before-completion` skill.

Run all verification commands and confirm actual output before proceeding:

```bash
# Python
ruff check shared/ services/
pytest --tb=short

# Go
cd services/call-manager && go test ./... && go vet ./...

# Frontend
cd frontend && npm run lint && npm run type-check && npm run test -- --run
```

If any check fails → fix first. Do NOT proceed with failing tests.

**Step 2: Commit Cleanup**

Use **domain-commit** (`.cursor/skills/domain-commit/SKILL.md`) to:
- Split uncommitted changes into domain-based commits
- Run pre-commit hooks (ruff, black, eslint, golangci-lint, gitleaks)
- Fix any lint errors and retry
- Follow commit message format from `CONTRIBUTING.md`

**Step 3: Finish Branch**

Read and follow the Superpowers `finishing-a-development-branch` skill.

Present exactly these 4 options:

```
Implementation complete. All tests pass. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work
```

Execute the chosen option:
- **Option 1 (Merge):** Checkout base → pull → merge → verify tests on merged result → delete feature branch
- **Option 2 (PR):** Push branch → create PR via `gh pr create` following CONTRIBUTING.md template
- **Option 3 (Keep):** Report branch name and path, preserve everything
- **Option 4 (Discard):** Require typed "discard" confirmation → delete branch

**Step 4: Update Task Tracking**

Update `tasks/todo.md` with completed items per project convention.

### Important Rules

- Never proceed with failing tests
- Never force-push without explicit request
- Never delete work without typed confirmation
- Always verify tests on the merged result (Option 1)
- Do NOT push to upstream unless the user explicitly asks

### Output

- All tests passing (with actual output shown)
- Clean, domain-split commits
- Branch integrated via chosen method (merge/PR/keep/discard)
- Task tracking updated
