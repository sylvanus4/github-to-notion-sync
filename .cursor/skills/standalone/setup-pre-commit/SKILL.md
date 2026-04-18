---
name: setup-pre-commit
description: Set up Husky pre-commit hooks with lint-staged, Prettier, ESLint, type checking, and test runners for any JavaScript/TypeScript project. Use when the user asks to "set up pre-commit", "add git hooks", "configure Husky", "lint on commit", "format on commit", "enforce code quality", "setup-pre-commit", "add lint-staged", "커밋 훅 설정", "프리커밋 설정", "Husky 설정", "커밋 시 린트", "코드 품질 자동화", or is bootstrapping a new JS/TS repo without hooks. Do NOT use for Python projects (use pre-commit framework), Go projects (use golangci-lint), projects with working hooks (audit instead), or CI-only linting without local hooks (configure CI directly).
---

# Setup Pre-Commit

Set up Husky pre-commit hooks with lint-staged, Prettier, ESLint, type checking, and test runners — configured once, enforced on every commit.

## When to Use

- Bootstrapping a new JavaScript/TypeScript repository
- Adding pre-commit hooks to an existing project that has none
- Upgrading from deprecated husky v4 to modern husky v9+
- Standardizing code quality enforcement across a team
- Preventing broken code from being committed (lint errors, type errors, failing tests)

## When NOT to Use

- Python projects (use `pre-commit` framework with `.pre-commit-config.yaml` instead)
- Go projects (use `golangci-lint` with git hooks or CI)
- Projects that already have working pre-commit hooks (audit them instead)
- CI-only linting without local hooks (just configure CI)

## Workflow

### Phase 1: Audit Current State

1. Check for existing hook setup:
   - `.husky/` directory
   - `lint-staged` config in `package.json` or `.lintstagedrc`
   - `.prettierrc` / `prettier.config.*`
   - `.eslintrc*` / `eslint.config.*`
   - `tsconfig.json` (for TypeScript projects)
2. Identify the package manager: `npm`, `yarn`, `pnpm`, `bun`
3. Note existing scripts in `package.json` (`lint`, `format`, `typecheck`, `test`)

### Phase 2: Install Dependencies

```bash
# Husky (git hooks manager)
npx husky init

# lint-staged (run linters on staged files only)
npm install --save-dev lint-staged

# Prettier (code formatter) — skip if already installed
npm install --save-dev prettier

# ESLint — skip if already installed
npm install --save-dev eslint
```

### Phase 3: Configure lint-staged

Add to `package.json`:

```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix --max-warnings 0",
      "prettier --write"
    ],
    "*.{json,md,yml,yaml,css,scss}": [
      "prettier --write"
    ]
  }
}
```

Adapt based on project needs:
- **TypeScript projects**: Add `tsc --noEmit` as a separate hook (not in lint-staged, since tsc needs all files)
- **Test runner**: Add `vitest related --run` or `jest --bail --findRelatedTests` for affected test detection
- **Monorepos**: Configure per-package lint-staged or use root-level with workspace-aware paths

### Phase 4: Set Up Husky Hooks

```bash
# Pre-commit hook: lint and format staged files
echo "npx lint-staged" > .husky/pre-commit

# Optional: Pre-push hook for type checking and tests
echo "npm run typecheck && npm run test -- --run" > .husky/pre-push
```

Recommended hook structure:

| Hook | Purpose | Speed Target |
|------|---------|-------------|
| `pre-commit` | lint-staged (ESLint + Prettier on changed files) | < 5 seconds |
| `pre-push` | Type check + test suite | < 30 seconds |
| `commit-msg` | Conventional commit format validation (optional) | < 1 second |

### Phase 5: Add Conventional Commits (Optional)

```bash
npm install --save-dev @commitlint/cli @commitlint/config-conventional

echo "npx --no -- commitlint --edit \$1" > .husky/commit-msg
```

Create `commitlint.config.js`:
```javascript
export default { extends: ['@commitlint/config-conventional'] };
```

### Phase 6: Verify Setup

1. Stage a file with a lint error and attempt to commit — should be blocked
2. Stage a properly formatted file — should commit successfully
3. Verify Prettier formatting is applied automatically on commit
4. If pre-push hook is set, push and verify type check + tests run
5. Document the setup in README:

```markdown
## Development Setup

This project uses Husky + lint-staged for automated code quality:

- **Pre-commit**: ESLint + Prettier run on staged files
- **Pre-push**: TypeScript type check + test suite
- **Commit messages**: Conventional Commits enforced

After cloning, hooks are installed automatically via `prepare` script.
```

## Gotchas

1. **`husky install` is deprecated.** Husky v9+ uses `npx husky init`. Using the old API causes silent failures where hooks simply never run.
2. **`tsc` in lint-staged = false safety.** TypeScript type checking requires the full project context. Running `tsc` on individual staged files misses cross-file type errors. Always run it as a separate pre-push hook.
3. **Monorepo lint-staged paths are tricky.** Root-level lint-staged config may not match workspace package paths. Test with an actual staged file in a nested package before shipping.
4. **`--no-verify` escape hatch.** Developers can bypass hooks with `git commit --no-verify`. Complement local hooks with CI enforcement for critical checks.

## Verification

After completing all phases:
1. Stage a file with a deliberate lint error → commit must be blocked
2. Stage a clean file → commit must succeed with Prettier formatting applied
3. Verify `cat .husky/pre-commit` shows `npx lint-staged`
4. Confirm `prepare` script exists in `package.json` (so hooks auto-install for new clones)
5. If pre-push hook is set, run `git push --dry-run` and verify type check + tests execute

## Anti-Example

```bash
# BAD: Using deprecated Husky API
npx husky install  # This is v4 syntax — hooks won't register in v9+

# BAD: Running tsc inside lint-staged
"lint-staged": {
  "*.ts": ["tsc --noEmit"]  # tsc needs ALL files, not just staged ones
}

# BAD: No prepare script — hooks break for new team members
# package.json is missing:
# "scripts": { "prepare": "husky" }
# → New clone runs npm install → no hooks installed → broken code gets committed
```

## Constraints

- Always use `npx husky init` for modern Husky (v9+), never the deprecated `husky install`
- lint-staged should only run on staged files, never the entire codebase
- Keep pre-commit hooks fast (< 5 seconds) — move slow checks to pre-push or CI
- Do not run `tsc` inside lint-staged (it needs the full project context); run it as a separate pre-push hook
- Ensure the `prepare` script in `package.json` runs `husky` so hooks auto-install on `npm install`
- Test the hooks locally before pushing the configuration
- Do NOT add commit-msg hooks or conventional commits unless the user explicitly requests them — keep the default setup minimal

## Output

1. Updated `package.json` with husky, lint-staged, and formatter dependencies
2. `.husky/pre-commit` hook file
3. `.husky/pre-push` hook file (optional)
4. `.husky/commit-msg` hook file (optional)
5. Prettier and ESLint configs if not already present
6. README section documenting the hook setup
