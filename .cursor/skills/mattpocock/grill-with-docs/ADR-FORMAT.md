# ADR Format

Architecture Decision Records live in `docs/adr/` and capture decisions that are hard to reverse, surprising without context, or result from a real trade-off.

## Template

```markdown
# ADR-NNN: [Decision Title]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-NNN]

## Context

What is the issue that we're seeing that is motivating this decision?

## Decision

What is the change that we're proposing/doing?

## Consequences

What becomes easier or harder because of this change?
```

## Rules

1. **One decision per ADR.** Don't bundle.
2. **Immutable once accepted.** To change a decision, create a new ADR that supersedes the old one.
3. **Sequential numbering.** ADR-001, ADR-002, etc.
4. **Short.** If the ADR exceeds one page, you're explaining too much context. Link to other docs instead.

## When to Offer an ADR

Offer to create an ADR when:

- A decision is **hard to reverse** (database schema, API contract, major dependency)
- The decision would be **surprising without context** ("why did we use X instead of Y?")
- There was a **real trade-off** (two valid options, chose one for specific reasons)

Don't create ADRs for:

- Obvious choices with no real alternatives
- Implementation details that can change easily
- Style/formatting preferences (use linter rules instead)
