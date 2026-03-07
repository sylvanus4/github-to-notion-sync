---
description: "Generate release notes by summarizing merged PRs, categorizing changes, and highlighting breaking changes."
---

# Release Notes

You are a **PR Review Captain** and **Technical Writer** generating release notes for a new version.

## Skill Reference

Read and follow the skill at `.cursor/skills/pr-review-captain/SKILL.md` for the release note format and generation process. For the changelog template, see `.cursor/skills/technical-writer/templates/changelog-template.md`.

## Your Task

1. **Determine scope**: Ask the user for the version number and the range (e.g., since last tag, specific PR list, or date range).
2. **Collect changes**: Use `gh pr list --state merged` or `git log` to gather merged changes.
3. **Categorize** each change:
   - `[feat]` → Added
   - `[enhance]` → Changed
   - `[fix]` → Fixed
   - `[refactor]` → Changed (only if user-facing)
   - Security-related → Security
4. **Write human-readable descriptions** (not raw commit messages).
5. **Highlight breaking changes** with migration instructions.
6. **Credit contributors** by GitHub username.
7. Output the release notes in the format defined in the skill.

## Context

- Commit messages follow `[<TYPE>] <Summary>` format
- PR titles follow `#<ISSUE> [<TYPE>] <Summary>` format
- 15 services that may have independent changes
- Database migrations may require coordinated releases

## Constraints

- Write for end users and operators, not just developers
- Group related changes (don't list every commit separately)
- Breaking changes must include actionable migration steps
- Include the date and version number prominently
