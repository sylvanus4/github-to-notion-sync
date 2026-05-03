---
name: msp-change-risk-summarizer
description: >-
  MSP read-only skill that analyzes pending infrastructure changes (PRs,
  Terraform plans, Helm diffs, K8s manifest updates) and produces a structured
  risk summary with blast radius estimation, affected services, rollback
  complexity, and an approval recommendation. Fan-out dispatches
  cloud-specific analyzers in parallel, fan-in merges into a unified risk
  verdict. Composes pr-review-captain, terraform-reviewer, helm-validator, and
  terraform-plan-reviewer (MSP #6). Use when the user asks to assess change
  risk, review infrastructure change, estimate blast radius, pre-approve
  change, change advisory board prep, or needs a risk summary before deploying
  infrastructure changes. Do NOT use for applying changes or executing
  deployments (use sre-devops-expert), code-only PR review without infra
  context (use deep-review), incident investigation (use
  k8s-incident-investigator or incident-triage-summarizer), or policy
  compliance checking only (use policy-guardrail-checker). Korean triggers: 변경
  리스크, 블래스트 반경, 변경 위험 분석, 배포 전 리스크, 인프라 변경 평가.
disable-model-invocation: true
---

# MSP Change-Risk Summarizer

Read-only MSP skill that evaluates pending infrastructure changes across multiple change types and produces a unified risk assessment with blast radius, rollback complexity, and an approval recommendation—without executing any changes.

## Usage

```
/msp-change-risk-summarizer --tenant acme-corp --pr https://github.com/org/infra/pull/123
/msp-change-risk-summarizer --tenant acme-corp --plan-file tfplan.json "assess Terraform plan risk"
/msp-change-risk-summarizer --tenant acme-corp --helm-diff release-name --namespace prod
/msp-change-risk-summarizer --change-ticket CHG-2024-0456 "CAB prep risk summary"
```

## Prerequisites

- **Identity**: `tenant_id`, environment context, optional `change_ticket_id` for audit trail linkage.
- **Change artifacts** (at least one): PR URL, Terraform plan JSON, Helm diff output, K8s manifest diff, or CloudFormation changeset.
- **Cloud credentials**: read-only roles for resource metadata lookup (service dependencies, tag-based ownership).
- **Git access**: read-only for PR diff retrieval.

## Pipeline Overview

```
Fan-out (parallel, read-only)
  ├─ Terraform change analyzer   → terraform-plan-reviewer (MSP #6) for plan risk grading
  ├─ Helm/K8s change analyzer    → helm-validator lint + manifest diff review
  ├─ PR context analyzer         → pr-review-captain for code change summary
  └─ Blast radius estimator      → service dependency graph lookup, tag-based impact mapping

        ↓ Fan-in: merge risk scores, unify blast radius, resolve conflicts

  ├─ Risk scoring engine         → composite risk score (0–100) from weighted dimensions
  └─ Rollback complexity scorer  → estimate rollback difficulty and data-loss risk

        ↓ Classify + report

  Output: JSON risk report + Markdown approval recommendation
```

## Detailed Workflow

1. **Intake and classify change type** — Parse inputs to determine change types present: Terraform plan, Helm release, K8s manifests, CloudFormation changeset, application code. A single change may span multiple types.

2. **Fan-out** — Dispatch parallel analyzers based on detected change types:
   - **Terraform**: Invoke `msp-terraform-plan-reviewer` (MSP #6) for plan parsing, destructive change detection, and MSP risk grading.
   - **Helm/K8s**: Invoke `helm-validator` for chart lint; parse `helm diff` output for value changes, new/removed resources.
   - **PR context**: Invoke `pr-review-captain` for change summary, file-level risk assessment, and reviewer checklist.
   - **Blast radius**: Query cloud resource tags and service dependency metadata to map affected downstream services.

3. **Fan-in** — Merge results into unified risk dimensions:
   - **Destructive changes**: Resources being replaced, deleted, or recreated.
   - **Security changes**: IAM, RBAC, NetworkPolicy, SecurityGroup, firewall rules.
   - **Data-plane changes**: Database migrations, storage modifications, encryption changes.
   - **Availability changes**: Replica counts, scaling policies, load balancer modifications.
   - **Blast radius**: Total affected services, regions, namespaces.

4. **Score risk** — Compute composite risk score (0–100) from weighted dimensions:
   | Dimension | Weight | Scoring |
   |-----------|--------|---------|
   | Destructive scope | 30% | Count of replace/delete resources × severity multiplier |
   | Security impact | 25% | IAM/RBAC/firewall change count × privilege escalation check |
   | Blast radius | 20% | Number of affected services/namespaces/regions |
   | Rollback complexity | 15% | Stateful resource count, migration irreversibility |
   | Change volume | 10% | Total lines changed, resources modified |

5. **Classify risk level**:
   - **CRITICAL** (80–100): Requires senior approval, maintenance window, rollback plan mandatory.
   - **HIGH** (60–79): Requires team lead approval, rollback plan recommended.
   - **MEDIUM** (30–59): Standard approval, monitor after deploy.
   - **LOW** (0–29): Fast-track eligible, minimal monitoring.

6. **Generate rollback assessment** — Estimate rollback difficulty: instant (K8s rollout undo), easy (Terraform state revert), hard (data migration reversal), impossible (destructive deletion).

7. **Emit JSON report and Markdown recommendation**.

## Output Schema

```json
{
  "schema_version": "1.0.0",
  "skill": "change-risk-summarizer",
  "generated_at": "ISO-8601",
  "tenant_id": "string",
  "change_reference": {
    "pr_url": "string|null",
    "plan_file": "string|null",
    "change_ticket": "string|null"
  },
  "risk_score": {
    "composite": 0,
    "level": "CRITICAL|HIGH|MEDIUM|LOW",
    "dimensions": {
      "destructive_scope": 0,
      "security_impact": 0,
      "blast_radius": 0,
      "rollback_complexity": 0,
      "change_volume": 0
    }
  },
  "blast_radius": {
    "affected_services": ["string"],
    "affected_regions": ["string"],
    "affected_namespaces": ["string"],
    "estimated_user_impact": "string"
  },
  "destructive_changes": [
    {
      "resource_type": "string",
      "resource_id": "string",
      "action": "replace|delete|recreate",
      "severity": "CRITICAL|HIGH|MEDIUM",
      "data_loss_risk": true
    }
  ],
  "security_changes": [
    {
      "change_type": "IAM|RBAC|NetworkPolicy|SecurityGroup|firewall",
      "description": "string",
      "privilege_escalation": false
    }
  ],
  "rollback_assessment": {
    "difficulty": "instant|easy|hard|impossible",
    "method": "string",
    "estimated_duration": "string",
    "data_loss_risk": false
  },
  "approval_recommendation": {
    "level": "fast-track|standard|senior|executive",
    "rationale": "string",
    "required_reviewers": ["string"],
    "maintenance_window_required": false,
    "rollback_plan_required": false
  },
  "sub_reports": {
    "terraform": {},
    "helm_k8s": {},
    "pr_context": {}
  }
}
```

## Error Handling

- **Partial change artifacts** — Analyze available artifacts; flag missing types in report. Score only on available dimensions.
- **Dependency graph unavailable** — Use tag-based and namespace-based heuristics for blast radius. Note reduced confidence.
- **Large PR / plan** — Truncate to critical sections; focus on destructive and security changes. Note truncation.
- **Conflicting risk assessments** — When sub-analyzers disagree, take the higher severity and note the conflict.

## Governance

- **Tier 1 — read-only** per `metadata.approval_spec`. No deployment execution, no PR approval actions, no resource modifications.
- Approval recommendations are advisory; actual approval authority rests with designated human approvers per the customer's change management process.
