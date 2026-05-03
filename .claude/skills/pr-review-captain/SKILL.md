---
name: pr-review-captain
description: Summarize PR changes, assess risks, generate review checklists, and produce release notes.
---

Summarize and review a pull request for merge readiness.

## Capabilities

1. **PR Summary**: Analyze all commits and produce a structured change summary
2. **Risk Assessment**: Score changes by blast radius, complexity, and reversibility
3. **Review Checklist**: Generate domain-specific review items
4. **Release Notes**: Create user-facing changelog entries
5. **Stale Doc Detection**: Flag documentation that may need updates

## Output Format

```markdown
## PR Summary
- **Scope**: [files changed / lines added / lines removed]
- **Risk**: [LOW / MEDIUM / HIGH]

## Changes
- [Grouped by domain]

## Review Checklist
- [ ] [Domain-specific items]

## Release Notes
- [User-facing changes]

## Risks & Concerns
- [Specific risks with mitigation]
```

## Rules

- Analyze ALL commits, not just the latest
- Flag any secrets, credentials, or PII
- Check for missing tests on new code paths
