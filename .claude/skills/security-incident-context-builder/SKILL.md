---
name: msp-security-incident-context-builder
description: >-
  MSP security context assembly: ingest a security finding (GuardDuty,
  Security Hub, SCC), fan out three parallel investigators (identity activity,
  network flows, resource configuration), merge into a correlated timeline,
  score risk dimensions (data exposure, lateral movement, persistence), and
  emit a structured JSON context report with recommended investigation steps —
  all read-only, zero remediation. Composes security-expert (STRIDE/OWASP
  classification, read-only mode only) and compliance-governance (policy
  violation check). Use when the user asks to build security context, security
  investigation context, assemble security incident data, security finding
  analysis, security context builder, or needs a consolidated security context
  package from cloud security signals without taking remediation action. Do
  NOT use for executing remediation (blocking IPs, revoking credentials,
  quarantining resources), operational incident triage without security focus
  (use msp-incident-triage-summarizer), full incident lifecycle management
  (use incident-lifecycle-manager), vulnerability scanning or pen testing (use
  security-expert directly), or compliance-only audits without a security
  finding (use compliance-governance). Korean triggers: 보안 인시던트 컨텍스트, 보안 조사
  컨텍스트, GuardDuty 분석, SCC 분석, 보안 컨텍스트 빌더.
disable-model-invocation: true
---

# Security Incident Context Builder

## Usage

- A GuardDuty, Security Hub, or SCC finding needs investigation context
- A suspicious IAM activity event requires surrounding evidence assembly
- Credential exposure alert needs identity/network/resource correlation
- Security team requests a structured context package before remediation
- `/msp-security-context` with a finding ID or finding JSON

## Prerequisites

- AWS: GuardDuty, Security Hub, CloudTrail, VPC Flow Logs, AWS Config enabled
- GCP: Security Command Center, Audit Logs, VPC Flow Logs, Asset Inventory enabled
- `tenant_id`, `account_id`/`project_id` in MSP scope
- Security finding object or finding ID

## Workflow

### Step 1 — Finding Ingestion

```
Read security finding JSON or fetch by finding ID
Validate tenant_id and account_id scope
Classify finding source:
  - AWS: GuardDuty GetFindings | Security Hub GetFindings
  - GCP: Security Command Center ListFindings
Extract affected resources, principal, severity
Determine investigation time_window (default: 24 hours before finding)
```

### Step 2 — Parallel Investigation (Fan-out)

Launch three investigation agents in parallel:

#### Agent 1 — Identity Investigation
```
AWS path:
  CloudTrail LookupEvents filtered by principal within time_window
  IAM GetPolicy + SimulatePrincipalPolicy for effective permissions
  IAM GetAccessKeyLastUsed for credential age
  Detect anomalous API calls outside normal baseline

GCP path:
  Cloud Audit Logs query for principal within time_window
  Policy Analyzer for effective permissions
  IAM ListServiceAccountKeys for key age
  Detect anomalous API calls outside normal baseline

Output: identity_context block with recent_api_calls, permission_scope,
        anomalous_actions, credential_status
```

#### Agent 2 — Network Investigation
```
AWS path:
  VPC Flow Logs via CloudWatch Logs Insights for suspicious IPs
  Security Group analysis for exposure
  Geo-locate external IPs via WebSearch

GCP path:
  VPC Flow Logs query for suspicious traffic
  Firewall Rules analysis for exposure
  Geo-locate external IPs via WebSearch

Output: network_context block with suspicious_ips, geo_locations,
        vpc_flow_summary, security_group_exposure
```

#### Agent 3 — Resource Investigation
```
AWS path:
  AWS Config GetResourceConfigHistory for affected resources
  Check for public access (S3 bucket policies, Security Group 0.0.0.0/0)
  Review encryption status

GCP path:
  Cloud Asset Inventory for resource state and history
  Check for public access (IAM allUsers/allAuthenticatedUsers bindings)
  Review encryption status

Output: resource_context block with configuration_snapshot,
        recent_changes, unauthorized_modifications
```

### Step 3 — Timeline Construction

```
Merge events from all three agents by timestamp
Sources: CloudTrail/AuditLogs + VPC Flow Logs + GuardDuty/SCC + Config changes
Order chronologically
Identify attack progression phases (initial access → persistence → lateral movement)
Flag gaps in logging coverage (missing log types, disabled services)
```

### Step 4 — Risk Assessment

```
Score four risk dimensions (HIGH/MEDIUM/LOW/NONE):
  - data_exposure_risk: public access, unencrypted data, exfiltration indicators
  - lateral_movement_risk: cross-resource API calls, role chaining
  - persistence_indicators: new IAM keys, modified policies, backdoor users
  - blast_radius: number of affected resources, cross-service impact

All assessments must cite specific evidence from the timeline
Speculation is labeled explicitly as "hypothesis — requires verification"
```

### Step 5 — Threat Classification

```
Pass finding + identity_context to security-expert in read-only mode
Get STRIDE classification and OWASP mapping
Pass resource_context to compliance-governance for policy violation check
If finding correlates with an operational incident, query Skill #1 output
```

### Step 6 — Report Assembly

```
Merge all parallel outputs into final JSON structure
Include:
  - finding_summary
  - identity_context
  - network_context
  - resource_context
  - timeline (chronological event list)
  - risk_assessment (scored dimensions)
  - recommended_investigation_steps (ordered for human analyst)
  - audit_entry (tier-1, zero mutations)
Generate markdown summary for quick human consumption
```

## Output Schema

```json
{
  "schema_version": "1.0.0",
  "skill": "security-incident-context-builder",
  "finding_summary": {"source": "", "severity": "", "finding_type": "", "affected_resources": []},
  "identity_context": {"principal": "", "recent_api_calls": [], "anomalous_actions": []},
  "network_context": {"suspicious_ips": [], "geo_locations": [], "security_group_exposure": []},
  "resource_context": {"affected_resources": []},
  "timeline": [{"timestamp": "", "event_type": "", "source": "", "description": ""}],
  "risk_assessment": {"data_exposure_risk": "", "lateral_movement_risk": "", "persistence_indicators": [], "blast_radius": ""},
  "recommended_investigation_steps": [],
  "audit_entry": {"skill_version": "1.0.0", "tier": 1, "mutations": []}
}
```

## Governance

**Tier 1 — Read-only.** No remediation actions permitted.

Prohibited:
- Blocking IPs, modifying security groups or firewall rules
- Revoking credentials, rotating keys, disabling users
- Quarantining or isolating resources
- Modifying IAM policies or role bindings
- Sending external notifications or customer communications
- Executing any remediation runbooks

## Error Handling

| Error | Recovery |
|-------|----------|
| Finding ID not found | Return error with finding_id; suggest checking finding source |
| CloudTrail/Audit Logs not enabled | Report as logging gap; proceed with available data |
| VPC Flow Logs not enabled | Report as coverage gap; skip network investigation agent |
| API rate limiting | Exponential backoff with 3 retries; report partial results if exhausted |
| Cross-account finding | Scope to authorized account only; flag cross-account activity for human follow-up |

## Subagent Contract

When invoked by `Task` subagent, the caller must provide:
- `security_finding` (JSON object or finding ID + source)
- `tenant_id` and `account_id`/`project_id`
- `correlation_id`

The skill returns the full JSON output to the caller for downstream processing.
