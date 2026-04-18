## PRD to Issues

Break a PRD into independently-grabbable GitHub issues with vertical slices, acceptance criteria, and blocking relationships.

### Usage

```
/prd-to-issues                              # from PRD in current context
/prd-to-issues docs/prd/feature-x.md        # from a specific PRD file
/prd-to-issues --epic "Auth System"          # group under an epic label
/prd-to-issues --dry-run                     # preview issues without creating
```

### Workflow

1. **Parse PRD** — Extract requirements, user stories, and technical constraints
2. **Decompose** — Split into independent vertical-slice issues
3. **Add metadata** — Acceptance criteria, labels, size estimates, and blockers
4. **Create issues** — File as GitHub issues with project field setup
5. **Report** — List of created issues with blocking graph

### Execution

Read and follow the `sprint-retro-to-issues` skill (`.cursor/skills/pipeline/sprint-retro-to-issues/SKILL.md`) for issue creation format and GitHub Project field setup. Use `commit-to-issue` (`.cursor/skills/review/commit-to-issue/SKILL.md`) for the GitHub issue creation mechanics.

### Examples

Create issues from a PRD:
```
/prd-to-issues docs/prd/billing.md
```

Preview without creating:
```
/prd-to-issues --dry-run docs/prd/billing.md
```
