---
name: msp-runbook-executor-with-approval
description: >-
  MSP Tier 2 skill that executes a recommended runbook ONLY after mandatory
  human approval. Validates parameters, enforces environment-specific approval
  policies (single approver dev/staging, dual approver production with 1h TTL
  and ticket requirement), assumes least-privilege cloud execution roles, runs
  SSM Automation or GCP Workflows/Cloud Run jobs, captures execution logs,
  verifies outcomes, and produces immutable audit records. Consumes Skill #3
  (runbook-recommender) output as primary input. Use when the user asks to
  execute runbook, run runbook with approval, approved runbook execution, MSP
  runbook execute, start automation with approval, execute recommended
  procedure, or needs to run a specific recommended runbook through the
  approval gate. Do NOT use for recommending runbooks without execution (use
  runbook-recommender), incident triage (use incident-triage-summarizer), root
  cause analysis (use root-cause-hypothesis-builder), executing arbitrary
  commands without runbook context, bypassing approval for any environment, or
  direct terraform apply/destroy (prohibited). Korean triggers: 런북 실행, 승인 후
  실행, 자동화 실행, 런북 승인 실행, MSP 런북 실행.
---

# MSP Runbook Executor with Approval

Tier 2 MSP skill that executes a recommended runbook **only after mandatory human approval**. This is the sole Tier 2 skill in Phase 2: the only skill that performs cloud mutations and therefore enforces the approval boundary end-to-end with immutable audit trails.

## Usage

```
/msp-runbook-executor-with-approval --tenant acme-corp --env prod --ticket CHG-2026-12345 --correlation-id <uuid> --runbook-id ssm/RestartDrainedService --params '{"service":"api","namespace":"prod"}'
/msp-runbook-executor-with-approval --tenant acme-corp --env dev --correlation-id <uuid> --recommendation <skill3-output.json>
```

## Prerequisites

- **Skill #3 output**: Valid `runbook-recommender` JSON with `runbook_id` and resolved parameters.
- **Approval service**: Backend that tracks attributed, time-bound, revocable approvals with environment-specific policies.
- **Cloud credentials**: Execution roles (separated from approval/audit roles) via `AssumeRole` (AWS) or Workload Identity (GCP).
- **Ticket system**: Required for production (`ticket_id`); recommended for staging.

## Governance

| Environment | Approvers | TTL | Ticket |
|-------------|-----------|-----|--------|
| **Dev** | Single approver | 24h | Recommended |
| **Staging** | Single approver | 4h | Strongly recommended |
| **Production** | Dual approver (distinct identities) | 1h | **Required** |

**Critical rules:**
- Approval is verified at **execution time**, not only at request time.
- Approvals are attributed, time-bound, and revocable before execution starts.
- Self-approval is prohibited for production dual-approver policy.
- All Tier 2 actions produce immutable audit log entries.

## Pipeline Overview

```
Skill #3 Output (runbook_id + params)
        ↓
1. Validate inputs (tenant, correlation, params, environment)
        ↓
2. Check approval validity (single/dual, TTL, ticket, not revoked)
        ↓
3. Acquire execution role (AssumeRole / Workload Identity)
        ↓
4. Execute automation (SSM / Workflows / Cloud Run job)
        ↓
5. Capture logs (CloudWatch, Workflow logs, Audit Logs)
        ↓
6. Post-execution verification (health, SLO, canary checks)
        ↓
7. Write immutable audit record
        ↓
8. Return structured result + human summary
```

## Detailed Workflow

1. **Receive selection** — Ingest Skill #3 output envelope, `environment`, `ticket_id` (if required), `correlation_id`, `tenant_id`. Reject if `runbook_id` is not from a documented Skill #3 recommendation or formal override ticket.

2. **Validate parameters** — Schema validation, allowlist check, tenant policy conformance, cloud target match (e.g., `cloud` in triage vs runbook). Reject parameter injection attempts.

3. **Check approval validity** — At execution time: verify single (dev/staging) or dual (prod) approvers, TTL not expired, ticket present for prod, approval not revoked, approvers distinct from actor if policy requires. Re-fetch approval state immediately before execution start.

4. **Acquire execution role** — `AssumeRole` (AWS) into execution-specific role separated from approval/audit read roles. GCP: Workload Identity binding for execution principal only. No long-lived static keys.

5. **Execute automation** — Start SSM Automation execution (AWS) or Workflows execution / Cloud Run job (GCP). Pass validated parameters. No interactive shell unless explicitly defined in runbook and approved.

6. **Capture logs** — Persist log pointers: CloudWatch log groups/streams, SSM Automation execution URL, GCP Workflow execution logs, Cloud Audit Logs query links. Correlate with `correlation_id`.

7. **Post-execution verification** — Run automated checks defined by runbook or default platform policy: health endpoints, SLO metric thresholds, canary status, K8s pod status.

8. **Write audit record** — Immutable JSON entry with `correlation_id`, `skill_name`, `skill_version`, `tier: 2`, `action`, `actor`, `approver(s)`, `tenant_id`, `timestamp`, `input_hash`, `result`, `cloud_api_calls[]`.

9. **Return result** — Structured JSON result + markdown human summary for Slack/Notion with outcome, approval chain, log links, and verification status.

## Output Schema

```json
{
  "schema_version": "1.0.0",
  "skill": "runbook-executor-with-approval",
  "generated_at": "ISO-8601",
  "correlation_id": "uuid",
  "tenant_id": "string",
  "environment": "dev|staging|prod",
  "runbook_id": "string",
  "execution_result": {
    "status": "success|failure|partial",
    "per_step_status": [
      { "step": "string", "status": "success|failure|skipped", "duration_ms": 0 }
    ]
  },
  "log_links": {
    "automation_execution": "url",
    "cloudwatch_logs": "url",
    "audit_logs_query": "url"
  },
  "duration": {
    "total_ms": 0,
    "wall_clock": "string"
  },
  "post_exec_verification": {
    "checks_run": ["string"],
    "all_passed": true,
    "details": [
      { "check": "string", "result": "pass|fail|skip", "note": "string" }
    ]
  },
  "approval_chain": {
    "approvers": ["string"],
    "approved_at": ["ISO-8601"],
    "ttl_remaining_at_exec": "string",
    "ticket_id": "string|null"
  },
  "audit": {
    "action": "runbook.execute",
    "actor": "string",
    "tier": 2,
    "input_hash": "sha256",
    "cloud_api_calls": ["string"]
  }
}
```

## Cloud-Specific Implementation

### AWS

| Concern | Service | Notes |
|---------|---------|-------|
| Execution | SSM Automation (`StartAutomationExecution`) | Separated execution role via `AssumeRole` |
| Logs | CloudWatch Logs | stdout/stderr + automation step logs |
| Audit | CloudTrail + custom audit log | Immutable; includes `correlation_id` |
| Role separation | STS `AssumeRole` | Approval principal ≠ execution principal |

### GCP

| Concern | Service | Notes |
|---------|---------|-------|
| Execution | Workflows (`executions.create`) or Cloud Run jobs | Identity separation between approval and execution |
| Logs | Cloud Logging + Workflow execution logs | Correlated with `correlation_id` |
| Audit | Cloud Audit Logs + custom audit log | Immutable; all executions logged |

## Composed Skills

| Skill | Role |
|-------|------|
| **runbook-recommender** (Skill #3) | Primary upstream: `runbook_id`, `parameters`, `correlation_id`, `tenant_id` alignment. Executor refuses if the request is not from a documented Skill #3 selection. |
| **incident-lifecycle-manager** | Approval and lifecycle patterns (attribution, war-room context, post-execution handoff). Notification and customer-facing boundaries alignment. |

## Safety Measures

- **Role separation**: Approval principal never executes cloud APIs; execution role is time-scoped and least-privilege.
- **Optimistic locking**: Re-read approval state with version field immediately before `StartAutomationExecution` or run start to prevent race conditions.
- **Parameter injection guard**: Allowlisted parameters per `runbook_id`; reject unknown keys.
- **Timeouts**: Per-step and global timeouts; automatic fail + audit + operator alert on timeout; no silent hang.
- **Idempotency**: Prefer idempotent automation steps; document `partial` result with compensating actions when idempotency is not possible.
- **Immutable audit**: Every execution (success or failure) produces a complete JSON audit line with traceable `correlation_id`.

## Error Handling

- **Approval expired/revoked** — Reject with clear error; require re-approval.
- **Approval mismatch** — Wrong tenant, wrong environment, same approver as actor in prod → reject.
- **Execution failure** — Record `failure` or `partial` status; persist all logs captured so far; alert operator; audit record includes failure details.
- **Verification failure** — Execution succeeded but post-checks fail → report `partial` with verification details; operator decides next steps.
- **Timeout** — Automatic fail with audit; operator alert; no silent hang.

## Governance

- **Tier 2 — MANDATORY approval** per `metadata.approval_spec`. No execution without valid approval verified at execution time.
- **Zero approval bypass** is a severity-1 defect. Fuzz/negative tests: expired approval, wrong tenant, wrong env, revoked token, second approver same as first in prod.
- All executions produce immutable audit trails with full `cloud_api_calls[]` and `input_hash`.
- **English triggers**: `execute runbook`, `run runbook with approval`, `approved execution`, `start automation`.
- **Korean triggers**: `런북 실행`, `승인 후 실행`, `자동화 실행`, `런북 승인 실행`, `MSP 런북 실행`.
