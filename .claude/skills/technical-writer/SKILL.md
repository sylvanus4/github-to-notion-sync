---
name: technical-writer
description: >-
  Author Architecture Decision Records (ADRs), API documentation, operational guides,
  changelogs, and technical documentation. Use when documenting design decisions,
  writing operational guides, or generating changelogs from commit history.
disable-model-invocation: true
arguments: [doc_type, topic]
---

# Technical Writer — Documentation Generation

Generate structured technical documentation for architecture decisions, APIs, operations, and changelogs.

## Usage

```
/technical-writer adr "Switch from REST to gRPC for inter-service communication"
/technical-writer api-doc backend/app/handlers/
/technical-writer ops-guide "Deployment rollback procedure"
/technical-writer changelog v2.5.0..HEAD
/technical-writer runbook "GPU node scaling"
```

## Document Types

### ADR (Architecture Decision Record)

```markdown
# ADR-NNN: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Context
[What is the issue? What forces are at play?]

## Decision
[What is the change we're proposing/deciding?]

## Consequences

### Positive
- [benefit 1]

### Negative
- [trade-off 1]

### Neutral
- [side effect 1]

## Alternatives Considered
[Options evaluated and why they were rejected]
```

### API Documentation

From code analysis, generate:
- Endpoint inventory with methods, paths, request/response schemas
- Authentication/authorization requirements
- Error response catalog
- Rate limiting and pagination patterns
- Example requests and responses

### Operational Guide

- Prerequisites and access requirements
- Step-by-step procedures with verification at each step
- Rollback procedures
- Monitoring and alerting checks
- Escalation paths

### Changelog

From git history, generate grouped changelog:
- Features (feat commits)
- Bug Fixes (fix commits)
- Breaking Changes (BREAKING CHANGE footer)
- Other (refactor, docs, chore)

### Runbook

- Trigger conditions and severity classification
- Diagnostic commands with expected output
- Resolution steps with rollback at each stage
- Post-resolution verification
- Lessons learned section

## Quality Rules

- Every procedure must have a verification step
- Every change must have a rollback step
- Use concrete commands, not abstractions ("Run `kubectl get pods -n ai-platform`" not "Check the pods")
- Include expected output for diagnostic commands
- Flag prerequisites that are frequently missed
- All output in Korean unless targeting global engineers

## Test Invocation

```
/technical-writer adr "Adopt Kueue for GPU workload scheduling"
/technical-writer changelog
/technical-writer runbook "CNPG PostgreSQL failover"
```
