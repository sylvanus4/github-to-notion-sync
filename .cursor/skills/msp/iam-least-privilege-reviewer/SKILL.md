---
name: msp-iam-least-privilege-reviewer
description: >-
  MSP read-only skill that audits IAM policies, roles, and service accounts
  to identify over-privileged identities, unused permissions, and policy
  violations, then produces a prioritized remediation plan with least-privilege
  policy suggestions — without making any IAM changes. IAM mutations are
  explicitly PROHIBITED by this skill. Uses AWS IAM Access Analyzer/CloudTrail
  and GCP IAM Policy Analyzer/Recommender/Audit Logs. Composes
  compliance-governance, security-expert, and policy-guardrail-checker
  (MSP #7). Use when the user asks to audit IAM permissions, review
  least-privilege, find over-privileged roles, IAM security audit, permission
  review, or needs to identify excessive cloud permissions. Do NOT use for
  applying IAM changes (handle via Terraform with approval), general security
  incident investigation (use security-expert), policy compliance checking
  without IAM focus (use policy-guardrail-checker), or cost analysis (use
  cost-anomaly-explainer). Korean triggers: IAM 권한 감사, 최소 권한 검토,
  과잉 권한 분석, 권한 리뷰, IAM 보안 감사.
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "msp/security"
  approval_tier: "tier-1"
  approval_spec: "docs/msp-skills/APPROVAL_BOUNDARY_SPEC.md"
  mutations: []
  clouds:
    - "aws"
    - "gcp"
  composes:
    - "compliance-governance"
    - "security-expert"
    - "msp-policy-guardrail-checker"
---

# MSP IAM Least-Privilege Reviewer

Read-only MSP skill that audits IAM configurations across MSP-managed cloud accounts, identifies over-privileged identities and unused permissions, and produces a prioritized remediation plan with specific least-privilege policy suggestions—without making any IAM changes.

**IAM changes are explicitly PROHIBITED by this skill.**

## Usage

```
/msp-iam-least-privilege-reviewer --tenant acme-corp --cloud aws --scope account
/msp-iam-least-privilege-reviewer --tenant acme-corp --cloud gcp --project prod-project
/msp-iam-least-privilege-reviewer --tenant acme-corp --cloud aws --role-name AdminRole "audit this role"
/msp-iam-least-privilege-reviewer --tenant acme-corp --lookback 90 "90-day unused permission analysis"
```

## Prerequisites

- **Identity**: `tenant_id`, cloud account/project scope, optional identity filter (role name, user, service account).
- **AWS credentials (read-only)**:
  - IAM: `iam:ListRoles`, `iam:ListPolicies`, `iam:GetPolicy`, `iam:GetPolicyVersion`, `iam:ListAttachedRolePolicies`, `iam:ListRolePolicies`, `iam:GetRolePolicy`, `iam:GenerateServiceLastAccessedDetails`, `iam:GetServiceLastAccessedDetails`.
  - IAM Access Analyzer: `access-analyzer:ListFindings`, `access-analyzer:GetFinding`.
  - CloudTrail: `cloudtrail:LookupEvents` for actual API usage history.
  - STS: `sts:GetCallerIdentity` for session context.
- **GCP credentials (read-only)**:
  - IAM: `iam.roles.list`, `iam.serviceAccounts.list`, `resourcemanager.projects.getIamPolicy`.
  - Policy Analyzer: `policyanalyzer.*.query`.
  - Recommender API: `recommender.iamPolicyRecommendations.list`.
  - Audit Logs: read access to Admin Activity logs.
  - Asset Inventory: `cloudasset.assets.searchAllIamPolicies`.

## Pipeline Overview

```
Sequential Pipeline (read-only)

  1. IAM inventory collection      → List all principals (users, roles, SAs, groups)
  2. Policy analysis               → Parse inline + attached policies for risky permissions
  3. Usage analysis                → Last-accessed data and CloudTrail/Audit Log correlation
  4. Violation detection           → Compare against baseline rules and compliance-governance
  5. Remediation generation        → Least-privilege policy suggestions per identity
  6. Prioritization                → Rank by risk × blast radius × ease of remediation

  Output: JSON audit report + Markdown remediation plan
```

## Detailed Workflow

1. **IAM inventory** — Enumerate all IAM principals in scope:
   - **AWS**: IAM users, roles, groups, and their attached/inline policies. Include trust policies for cross-account access.
   - **GCP**: Service accounts, IAM bindings at project/folder/org level. Include Workload Identity bindings.

2. **Policy analysis** — For each principal, analyze effective permissions:
   - **Wildcard detection**: Flag `*` actions and `*` resources.
   - **Admin/power-user detection**: Flag `AdministratorAccess`, `PowerUserAccess`, `roles/owner`, `roles/editor`.
   - **Privilege escalation paths**: Detect `iam:CreateRole`, `iam:AttachRolePolicy`, `iam:PassRole`, `sts:AssumeRole` chains; GCP `setIamPolicy`, `actAs`.
   - **Cross-account/external access**: IAM Access Analyzer findings (AWS), external member bindings (GCP).
   - **Data exfiltration risk**: S3/GCS full access combined with broad EC2/GCE or Lambda/Cloud Functions permissions.

3. **Usage analysis** — Determine actual permission utilization:
   - **AWS**: `GenerateServiceLastAccessedDetails` for service-level usage. CloudTrail for action-level usage over lookback period (default 90 days).
   - **GCP**: Policy Analyzer query for actual usage. Recommender API for unused role recommendations.
   - Classify permissions as: **Active** (used in lookback), **Stale** (not used in lookback), **Never used** (created but never invoked).

4. **Violation detection** — Apply rules from `compliance-governance` and `security-expert`:
   - No root/owner account usage for daily operations.
   - Service accounts should not have user-interactive roles.
   - Cross-account trust should be narrowly scoped.
   - MFA should be required for human users with console access.
   - Long-lived access keys should be rotated or replaced with temporary credentials.

5. **Generate remediation suggestions** — For each finding:
   - Specific least-privilege policy replacement (JSON/YAML).
   - Unused permissions to remove.
   - Role splitting suggestions (single overprivileged role → multiple scoped roles).
   - Trust policy tightening suggestions.

6. **Prioritize** — Score each finding: `risk_score = severity × blast_radius × exploitability`. Rank by risk score descending.

## Output Schema

```json
{
  "schema_version": "1.0.0",
  "skill": "iam-least-privilege-reviewer",
  "generated_at": "ISO-8601",
  "tenant_id": "string",
  "cloud": "aws|gcp",
  "scope": { "accounts": ["string"], "lookback_days": 90 },
  "summary": {
    "total_principals_analyzed": 0,
    "findings_count": 0,
    "severity_distribution": {
      "CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0
    },
    "unused_permissions_count": 0,
    "admin_principals_count": 0,
    "external_access_findings": 0
  },
  "findings": [
    {
      "id": "string",
      "principal": {
        "type": "user|role|service_account|group",
        "arn_or_email": "string",
        "name": "string"
      },
      "finding_type": "wildcard_permission|admin_access|unused_permission|privilege_escalation|external_access|stale_credentials|missing_mfa",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW|INFO",
      "description": "string",
      "evidence": {
        "policy_name": "string",
        "statement": {},
        "last_used": "ISO-8601|never",
        "access_analyzer_finding_id": "string|null"
      },
      "remediation": {
        "action": "remove_permission|replace_policy|split_role|tighten_trust|rotate_key|enable_mfa",
        "suggested_policy": {},
        "effort": "low|medium|high",
        "read_only": true
      },
      "risk_score": 0.0
    }
  ],
  "data_completeness": {
    "access_analyzer_enabled": true,
    "cloudtrail_available": true,
    "policy_analyzer_available": true,
    "missing_inputs": ["string"],
    "degraded_mode": false
  }
}
```

## Error Handling

- **Access Analyzer not enabled** — Proceed without external access findings; note in `data_completeness`.
- **CloudTrail/Audit Log gaps** — Use available data; mark usage analysis as reduced confidence.
- **Paginated results** — Handle pagination for large accounts with 1000+ policies.
- **Cross-account roles** — Report trust relationship findings but do not attempt to access external accounts.

## Governance

- **Tier 1 — read-only** per `metadata.approval_spec`. **Absolutely no IAM mutations**: no `iam:CreatePolicy`, `iam:AttachRolePolicy`, `iam:DeleteRole`, `iam:PutRolePolicy`, `setIamPolicy`, or any write operation.
- All remediation suggestions are advisory. Implementation requires human review, Terraform codification, and standard change management approval.
