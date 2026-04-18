## Changelog

Generate human-readable changelogs from recent git commits, grouped by type and with release note formatting.

### Usage

```
/changelog                             # changelog since last tag
/changelog --since "2025-01-01"        # changelog since a date
/changelog --format developer          # developer-focused detail
/changelog --format user               # user-facing release notes
```

### Workflow

1. **Collect commits** — Read git log since the specified range
2. **Classify** — Group by type: features, fixes, breaking changes, refactors
3. **Summarize** — Generate human-readable descriptions for each change
4. **Format** — Output as markdown changelog with version header
5. **Report** — Formatted changelog ready for README, GitHub release, or Slack

### Execution

Read and follow the `pr-review-captain` skill (`.cursor/skills/review/pr-review-captain/SKILL.md`) for changelog generation, release note formatting, and CHANGELOG/VERSION conventions.

### Examples

Generate changelog since last release:
```
/changelog
```

User-facing release notes:
```
/changelog --format user --since v2.3.0
```
