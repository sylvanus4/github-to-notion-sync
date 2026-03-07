---
name: technical-writer
description: Author Architecture Decision Records (ADRs), API documentation, operational guides, and changelogs. Use when the user asks to document a design decision, write an ADR, generate a changelog, or create operational documentation. Do NOT use for PR summaries or release notes (use pr-review-captain) or prompt engineering (use prompt-transformer).
metadata:
  version: "1.0.0"
  category: generation
---

# Technical Writer

Produce clear, structured documentation for the realtime-agent-copilot platform. Documentation lives at `docs/`.

## ADR (Architecture Decision Record)

### When to Write

- New technology adopted or replaced
- Architectural pattern chosen (e.g., event-driven vs request-response)
- Significant trade-off decision made
- Infrastructure change (new service, DB choice, deployment model)

### Process

1. **Create** ADR using the template at [templates/adr-template.md](templates/adr-template.md)
2. **Number** sequentially: `docs/09-decisions-guidelines/adr/NNNN-title-in-kebab-case.md`
3. **Status** lifecycle: `Proposed` → `Accepted` → (`Deprecated` | `Superseded by ADR-NNNN`)
4. **Review** with at least one team member before merging

### Writing Guidelines

- **Context**: State the problem and constraints objectively
- **Decision**: Be specific about what was chosen
- **Consequences**: List both positive and negative outcomes
- **Alternatives**: Document what was considered and why it was rejected
- Keep each section concise (3-5 bullet points)

## API Documentation

### Format

Follow OpenAPI 3.1 conventions. For each endpoint document:

```markdown
### POST /api/v1/resources

Create a new resource.

**Request Body** (application/json):
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Resource name (1-255 chars) |
| tenant_id | string | Yes | Tenant UUID |

**Response** (201 Created):
| Field | Type | Description |
|-------|------|-------------|
| id | string | Generated UUID |
| name | string | Resource name |
| created_at | string | ISO 8601 timestamp |

**Errors**:
| Status | Code | When |
|--------|------|------|
| 400 | VALIDATION_ERROR | Invalid input |
| 409 | CONFLICT | Duplicate name |
```

### Checklist

- [ ] All public endpoints documented
- [ ] Request/response examples provided
- [ ] Error responses listed
- [ ] Authentication requirements noted
- [ ] Rate limits documented

## Operational Guide

### Structure

```markdown
# [Service Name] Operations Guide

## Overview
[What this service does, 2-3 sentences]

## Dependencies
[Database, Redis, upstream/downstream services]

## Configuration
[Key environment variables and their purpose]

## Health Checks
[Liveness and readiness endpoints]

## Common Operations
[Start, stop, restart, scale, log access]

## Troubleshooting
[Common issues and resolutions]
```

## Changelog

### Format (Keep a Changelog)

Use the template at [templates/changelog-template.md](templates/changelog-template.md). Categories:

- **Added** — New features
- **Changed** — Changes to existing functionality
- **Deprecated** — Features to be removed
- **Removed** — Removed features
- **Fixed** — Bug fixes
- **Security** — Vulnerability fixes

### Commit-to-Changelog Mapping

| Commit type | Changelog category |
|------------|-------------------|
| `[feat]` | Added |
| `[enhance]` | Changed |
| `[fix]` | Fixed |
| `[refactor]` | Changed (if user-facing) or omit |
| `[docs]` | Omit (unless user-facing) |
| `[chore]` | Omit |

## Examples

### Example 1: Write an ADR
User says: "Document the decision to use Qdrant for vector search"
Actions:
1. Load the ADR template from templates/adr-template.md
2. Fill in context, decision, consequences, and alternatives
3. Number and save to `docs/09-decisions-guidelines/adr/`
Result: Complete ADR document ready for team review

### Example 2: Generate a changelog
User says: "Generate changelog for the latest release"
Actions:
1. Collect merged PRs and commits since last release tag
2. Map commit types to changelog categories (Added, Changed, Fixed)
3. Write human-readable entries using the changelog template
Result: Changelog entry in Keep a Changelog format

## Troubleshooting

### ADR numbering conflict
Cause: Multiple ADRs created concurrently with the same number
Solution: Check existing ADRs in `docs/09-decisions-guidelines/adr/` and use the next available number

### Commit type not mapping to changelog
Cause: Commit uses `[chore]` or `[docs]` type which is normally omitted
Solution: Include in changelog only if the change is user-facing

## Output Format

When asked to write documentation, produce the complete document in markdown, ready to save to the appropriate location in `docs/`.

## Templates

- ADR template: [templates/adr-template.md](templates/adr-template.md)
- Changelog template: [templates/changelog-template.md](templates/changelog-template.md)
