---
name: pr-review-captain
description: >-
  Summarize pull request changes, assess risks, generate review checklists,
  produce release notes, detect stale documentation, and enforce CHANGELOG and
  VERSION conventions. Use when the user asks for a PR summary, change risk
  assessment, review checklist, or release note generation. Do NOT use for
  committing local changes (use domain-commit) or writing ADR/operational
  documentation (use technical-writer). Korean triggers: "리뷰", "생성", "체크", "커밋".
metadata:
  version: "1.1.0"
  category: "review"
  author: "thaki"
---
# PR Review Captain

Coordinate code reviews and release documentation for pull requests. Works alongside the existing PR commands (`pr-review.md`, `pr-create.md`).

## Change Summary

When reviewing a PR, produce a concise summary:

1. **Read the diff** using `gh pr diff <number>` or `git diff <base>...HEAD`
2. **Categorize changes** by type:
   - Feature (new functionality)
   - Enhancement (improvement to existing)
   - Bug fix
   - Refactor (no behavior change)
   - Infrastructure / config
   - Documentation
3. **Identify affected services** from file paths (`services/<name>/`)
4. **Note migration/schema changes** if any files in `db/migrations/` are modified

## Risk Assessment

### Risk Matrix

| Factor | Low | Medium | High |
|--------|-----|--------|------|
| Scope | Single file/function | Multiple files in one service | Multiple services |
| Data | No schema changes | Additive migration | Destructive migration |
| Security | No auth/PII changes | Auth logic modified | New auth flow / PII handling |
| Dependencies | No dep changes | Patch/minor updates | Major version bump |
| Reversibility | Easily reverted | Needs coordination | Requires data migration to revert |

### Assessment Process

1. Score each factor (1=Low, 2=Medium, 3=High)
2. Overall risk = max(individual scores)
3. If overall >= High, recommend phased rollout or feature flag

## Review Checklist

Generate a checklist tailored to the PR content:

### Always Check

- [ ] PR title follows format: `#<ISSUE> [<TYPE>] <Summary>`
- [ ] PR description explains **why**, not just **what**
- [ ] No secrets, credentials, or PII in the diff
- [ ] No `TODO` or `FIXME` without linked issue
- [ ] Tests added/updated for changed behavior

### If Backend Changes

- [ ] Pydantic models validate inputs
- [ ] Error responses use standard error model
- [ ] Async patterns correct (no blocking calls)
- [ ] Health check still works

### If Frontend Changes

- [ ] Components accessible (keyboard, screen reader)
- [ ] No console errors/warnings
- [ ] Responsive on mobile viewports
- [ ] i18n keys added for new strings

### If DB Migration

- [ ] Migration reversible (downgrade works)
- [ ] No table locks on large tables
- [ ] Indexes added for new FK columns
- [ ] Data migration tested with production-like volume

### If Infrastructure

- [ ] Docker image builds successfully
- [ ] Health probes configured
- [ ] Resource limits set
- [ ] Rollback tested

## Documentation Staleness Detection

When reviewing a PR, automatically check for stale documentation:

### Diff-Based Doc Scan

1. Parse the diff for modified source files
2. For each modified file, check if a corresponding doc exists:
   - `src/api/<module>.ts` → look for `docs/api/<module>.md`
   - `src/services/<name>/` → look for `docs/services/<name>.md`
   - `README.md` references to changed files
3. If the doc exists but was NOT updated in the same PR, flag as potentially stale:

```
⚠️ Documentation may be stale:
  - docs/api/auth.md — auth service modified but docs not updated
  - README.md mentions auth flow but no README changes in diff
```

### CHANGELOG Edit-Only Rule

If the PR includes code changes, verify CHANGELOG presence:

1. Check if `CHANGELOG.md` (or equivalent) is in the diff
2. If present: verify it's an **additive edit** (new entry added, existing entries untouched)
3. If absent: warn that CHANGELOG should be updated for user-facing changes
4. **Never modify existing CHANGELOG entries** — only add new ones at the top

```
CHANGELOG Check:
  [✓] CHANGELOG.md updated with new entry
  [✓] Existing entries unchanged
  OR
  [⚠] CHANGELOG.md not updated — add entry for user-facing changes
```

### VERSION Bump Gate

If the PR modifies API contracts, public interfaces, or contains breaking changes:

1. Check if `VERSION`, `package.json version`, or `pyproject.toml version` is updated
2. Apply semver rules:
   - Breaking changes → major bump required
   - New features → minor bump required
   - Bug fixes → patch bump required
3. If version not bumped but should be:

```
⚠️ VERSION BUMP NEEDED
  Change type: [breaking / feature / fix]
  Expected bump: [major / minor / patch]
  Current version: [X.Y.Z]
  Suggested version: [X.Y.Z+1]
```

## Release Notes

### Format

```markdown
## [vX.Y.Z] - YYYY-MM-DD

### Highlights
[1-2 sentence summary of the most impactful change]

### Added
- [Feature] — [brief description] (#PR)

### Changed
- [Enhancement] — [brief description] (#PR)

### Fixed
- [Bug] — [brief description] (#PR)

### Security
- [Fix] — [brief description] (#PR)

### Breaking Changes
- [Change] — [migration guide if applicable] (#PR)

### Contributors
@[username1], @[username2]
```

### Generation Process

1. Collect merged PRs since last release tag
2. Categorize by commit type prefix (`[feat]`, `[fix]`, `[enhance]`, etc.)
3. Group by category (Added, Changed, Fixed, etc.)
4. Write human-readable descriptions (not raw commit messages)
5. Highlight breaking changes prominently

## Examples

### Example 1: PR review summary
User says: "Review PR #42"
Actions:
1. Run `gh pr diff 42` to read the changes
2. Categorize changes by type and identify affected services
3. Score risk factors and generate tailored review checklist
Result: PR Review Summary with risk assessment and actionable checklist

### Example 2: Generate release notes
User says: "Generate release notes for v1.5.0"
Actions:
1. Collect merged PRs since last release tag
2. Categorize by commit type prefix
3. Write human-readable release notes in Keep a Changelog format
Result: Release notes document ready for publishing

## Troubleshooting

### gh CLI not authenticated
Cause: GitHub CLI not logged in or token expired
Solution: Run `gh auth login` to authenticate

### Large PR with too many files
Cause: PR contains multiple unrelated changes
Solution: Suggest splitting into smaller, focused PRs for easier review

## Comment Labels

When leaving review comments, use severity labels:

| Label | Meaning | Action required |
|-------|---------|----------------|
| `critical.must` | Blocking issue, must fix | Cannot merge |
| `high.imo` | Strong recommendation | Should fix |
| `medium.imo` | Suggestion for improvement | Consider fixing |
| `low.nits` | Minor style/preference | Optional |
| `info.q` | Question for understanding | Response needed |

## Output Format

```
PR Review Summary
=================
PR: #[number] [title]
Author: @[username]
Base: [branch] ← [head branch]

1. Change Summary
   Type: [Feature / Fix / Enhancement / Refactor]
   Services affected: [list]
   Files changed: [N] (+[additions] -[deletions])
   Description: [2-3 sentences]

2. Risk Assessment
   Overall: [Low / Medium / High]
   | Factor | Score | Note |
   |--------|-------|------|
   | Scope | [1-3] | [detail] |
   | Data | [1-3] | [detail] |
   | Security | [1-3] | [detail] |
   | Dependencies | [1-3] | [detail] |
   | Reversibility | [1-3] | [detail] |

3. Review Checklist
   [Generated checklist based on PR content]

4. Concerns / Questions
   - [Concern or question]

5. Recommendation
   [Approve / Request changes / Needs discussion]
```

## Additional Resources

For detailed review patterns and release note examples, see [references/reference.md](references/reference.md).
