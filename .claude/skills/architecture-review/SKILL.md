---
name: architecture-review
description: >-
  Review AI platform architecture documents and implementation plans for IaaS,
  PaaS, SaaS, Kubernetes, GPU/NPU infrastructure, MLOps, LLMOps, and marketplace
  readiness. Use when reviewing architecture docs, system designs, or infra plans.
disable-model-invocation: true
arguments: [target]
---

# Architecture Review

Review the target architecture or document passed in `$target`.

## Usage

```
/architecture-review docs/ai-platform-architecture.md
/architecture-review docs/multi-cluster-centralization/
/architecture-review $ARGUMENTS
```

## Scope Identification

Identify which areas the document covers:

- IaaS / PaaS / SaaS layers
- Marketplace and billing
- Kubernetes orchestration
- GPU/NPU scheduling (Kueue, kai-scheduler)
- MLOps / LLMOps pipelines
- Model serving and inference
- Security / tenancy / billing / observability

## Architectural Consistency Checks

- [ ] Control plane vs data plane separation
- [ ] Tenant isolation model (namespace, network, storage)
- [ ] GPU/NPU scheduling assumptions and fairness
- [ ] Network topology and storage dependencies
- [ ] Observability and auditability (metrics, logs, traces)
- [ ] Operational failure modes and blast radius
- [ ] Multi-cluster coordination patterns
- [ ] ArgoCD GitOps deployment flow
- [ ] RBAC and Keycloak integration

## Gap Identification

- [ ] Missing functional or non-functional requirements
- [ ] Unclear ownership boundaries between teams/services
- [ ] Hidden operational assumptions
- [ ] Missing cost or capacity model
- [ ] Missing security controls or compliance gaps
- [ ] Missing SLO definitions

## Output Format

```markdown
## Architecture Review: [Document Title]

### Executive Summary
[2-3 sentence assessment]

### Strong Points
- [strength 1]
- [strength 2]

### Risks
- [risk]: [impact] -> [mitigation]

### Missing Decisions
- [decision needed]: [context and options]

### Recommended Next Actions
1. [action] -- [priority]

### Questions for Stakeholders
- [question]: [why it matters]
```

## Review Principles

- Do not modify files unless explicitly requested
- Flag assumptions that need validation
- Compare against existing patterns in `docs/` directory
- Reference relevant ADRs if they exist
- All output in Korean unless targeting global engineers

## Test Invocation

```
/architecture-review docs/planned/queue-management/
/architecture-review docs/multi-cluster-centralization/
```
