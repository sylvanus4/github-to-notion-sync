---
name: infra-runbook-generator
description: >-
  Generate infrastructure runbooks from Helm charts, K8s manifests, monitoring
  configs, and alert rules. Produces structured runbooks with overview,
  prerequisites, step-by-step procedures, rollback plans, and escalation
  paths. Output as .md + .docx with Cognee indexing. Use when the user asks to
  "generate runbook", "create runbook", "런북 생성", "인프라 런북",
  "infra-runbook-generator", or needs operational runbooks for infrastructure
  components. Do NOT use for incident response (use incident-to-improvement),
  general documentation (use technical-writer), or reviewing existing runbooks
  (use sre-devops-expert).
disable-model-invocation: true
---

# Infrastructure Runbook Generator

Transform infrastructure code into operational runbooks, reducing runbook creation from 3 days to 15 minutes.

## When to Use

- When deploying a new service/component that needs operational documentation
- When infrastructure code changes require runbook updates
- As part of the release pipeline (post-code-review, pre-deployment)
- When onboarding new SRE/ops team members

## Workflow

### Step 1: Analyze Infrastructure Context

Read and analyze the target infrastructure component:

**Helm Charts** (if present):
- `Chart.yaml`: name, version, dependencies
- `values.yaml`: configurable parameters, defaults
- `templates/`: resource types, labels, selectors
- `README.md`: existing documentation

**K8s Manifests** (if present):
- Deployments, StatefulSets, DaemonSets
- Services, Ingresses, NetworkPolicies
- ConfigMaps, Secrets references
- PVCs, StorageClasses

**Monitoring Config** (if present):
- Prometheus rules, Grafana dashboards
- AlertManager routes and receivers
- SLO definitions

**Docker Config** (if present):
- Dockerfile: build process, dependencies, ports
- docker-compose: service dependencies, volumes, networks

### Step 2: Identify Runbook Scope

Determine which runbook types are needed:

| Type | Trigger | Content Focus |
|------|---------|---------------|
| Deployment | New release, config change | Deploy steps, verification, rollback |
| Troubleshooting | Alert fires, incident | Diagnosis, mitigation, resolution |
| Scaling | Load increase, capacity planning | Horizontal/vertical scaling procedures |
| Backup/Recovery | Scheduled, disaster | Backup verification, restore procedure |
| Maintenance | Scheduled update, cert renewal | Pre-checks, execution, post-checks |

### Step 3: Generate Runbook

For each identified scope, generate a structured runbook:

```markdown
# Runbook: <Component> — <Type>

## Overview
- **Service**: <name>
- **Team**: <owning team>
- **Severity**: <P0-P3 scenarios this covers>
- **Last Updated**: <date>
- **Author**: Auto-generated from infrastructure code

## Prerequisites
- [ ] kubectl access to <cluster> with <namespace> permissions
- [ ] Helm v3.x installed
- [ ] Access to monitoring dashboard: <grafana-url>
- [ ] PagerDuty escalation policy: <policy-name>

## Diagnosis
### Symptoms
- <observable symptom 1>
- <observable symptom 2>

### Investigation Steps
1. Check pod status:
   ```bash
   kubectl get pods -n <namespace> -l app=<name>
   ```
2. Check recent events:
   ```bash
   kubectl get events -n <namespace> --sort-by='.lastTimestamp' | head -20
   ```
3. Check logs:
   ```bash
   kubectl logs -n <namespace> -l app=<name> --tail=100
   ```

## Resolution Procedures

### Procedure 1: <scenario>
1. <step with exact command>
2. <verification step>
3. <next step>

### Procedure 2: <scenario>
...

## Rollback Plan
1. Identify the last known good version:
   ```bash
   helm history <release-name> -n <namespace>
   ```
2. Rollback:
   ```bash
   helm rollback <release-name> <revision> -n <namespace>
   ```
3. Verify rollback:
   ```bash
   kubectl rollout status deployment/<name> -n <namespace>
   ```

## Escalation Path
| Level | Contact | When |
|-------|---------|------|
| L1 | On-call engineer | Initial response |
| L2 | Service owner | Resolution not found in 30 min |
| L3 | Platform team | Infrastructure-level issue |

## Related Resources
- Grafana Dashboard: <url>
- Alert Rules: <file-path>
- Architecture Doc: <url>
```

### Step 4: Generate .docx

Use `anthropic-docx` to produce a formatted Word document with:
- Table of contents
- Code blocks with syntax highlighting
- Formatted tables and checklists

### Step 5: Index in Cognee

Ingest the generated runbook into the Cognee knowledge graph for searchable retrieval:
- Entities: service names, commands, tools, team names
- Relationships: service dependencies, escalation chains

### Step 6: Publish

- Save `.md` to `docs/on-call/03-runbooks/`
- Generate `.docx` to `output/runbooks/`
- Optionally publish to Notion via `md-to-notion`

## Output

```
Runbook Generation Report
=========================
Component: api-server (Helm chart)
Runbooks Generated: 3

1. deployment-runbook.md — Deploy, verify, rollback procedures
2. troubleshooting-runbook.md — Common failure scenarios
3. scaling-runbook.md — Horizontal and vertical scaling

Outputs:
- Markdown: docs/on-call/03-runbooks/api-server-*.md
- DOCX: output/runbooks/api-server-runbooks.docx
- Cognee: Indexed (12 entities, 28 relationships)
```

## Error Handling

| Error | Action |
|-------|--------|
| No IaC files found in target path | Report "no infrastructure files found" with suggested paths; exit without generating |
| DOCX generation fails | Fall back to markdown-only output; log error and path to `anthropic-docx` |
| Notion upload fails | Save runbook locally; retry Notion upload once; if still failing, skip and report |
| Helm chart parsing error | Skip the failing chart; continue with other components; include parse error in report |
| Monitoring config not found | Generate runbook with placeholder "Add monitoring config" section; note missing config in output |

## Examples

### Example 1: Generate from Helm chart
User says: "Generate runbook for the API server"
Actions:
1. Read helm/api-server/ chart
2. Analyze deployment, service, ingress resources
3. Generate deployment + troubleshooting + scaling runbooks
4. Output .md + .docx
Result: 3 runbooks covering operational scenarios

### Example 2: Bulk generation
User says: "Generate runbooks for all services"
Actions:
1. Discover all Helm charts and K8s manifests
2. Generate runbooks for each component
3. Create index document linking all runbooks
Result: Complete operational documentation set
