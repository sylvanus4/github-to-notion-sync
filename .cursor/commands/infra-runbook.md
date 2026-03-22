---
description: "Generate structured infrastructure runbooks from IaC context — Helm charts, K8s manifests, monitoring configs"
---

## Infra Runbook

Generate operational runbooks from infrastructure code and configuration.

### Usage

```
/infra-runbook <service-name>               # generate runbook for a specific service
/infra-runbook --all                        # generate runbooks for all services
/infra-runbook --format docx                # output as .docx (default: markdown)
/infra-runbook --upload-notion              # also create Notion page
```

### Execution

Read and follow the skill at `.cursor/skills/infra-runbook-generator/SKILL.md`.

User input: $ARGUMENTS

1. Discover IaC context for the target service (Helm values, K8s manifests, monitoring config)
2. Analyze resource definitions, health checks, scaling policies
3. Generate structured runbook with: Overview, Architecture, Operations, Troubleshooting, Escalation
4. Output as markdown and optionally .docx / Notion page
