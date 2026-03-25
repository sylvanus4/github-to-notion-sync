# Project Overrides for AI Stock Analytics

This directory contains project-specific reference documents that override
cloud-platform assumptions in shared skill definitions.

## Files

| File | Overrides | Policy Source |
|------|-----------|---------------|
| `project-terminology-glossary.md` | Product name, domain terms, forbidden terms | POL-001 |
| `project-design-conventions.md` | Design system, colors, components | POL-002 |
| `project-tone-matrix.md` | Tone by context, signal rules, formatting | POL-003 |
| `project-copy-patterns.md` | UI copy, errors, empty states, Slack | POL-003 |
| `project-document-standards.md` | Quality gate, grading, report standards | POL-004 |
| `project-ssot.md` | Artifact locations, not-used systems | POL-005 |
| `project-tech-stack.md` | Frontend/backend libraries, versions | POL-001 |

## Usage

Skills should reference these files instead of cloud-platform conventions:

```markdown
## Project-Specific Overrides

This skill follows project-specific policies. See:
- `.cursor/skills/references/project-overrides/project-design-conventions.md`
- `.cursor/skills/references/project-overrides/project-terminology-glossary.md`
```

## Maintenance

When policies in `docs/policies/` change, update these override files
and propagate to affected skills per `docs/policies/06-skill-governance.md`.
