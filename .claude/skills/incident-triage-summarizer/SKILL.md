---
name: msp-incident-triage-summarizer
description: >-
  MSP-facing read-only triage: ingest alert/incident signals (logs, metrics,
  deploy context, trace refs), fan out to three parallel evidence agents
  (alarm parser, log correlator, deployment diff checker), fan in, classify
  severity and blast radius using kwp-engineering-incident-response, and emit
  a versioned JSON triage report plus a short markdown summary. Uses
  diagnose-style parallel evidence gathering only (no code fixes, no apply
  paths). Use when the user asks to triage incident, summarize alert, incident
  summary, classify severity, MSP triage, alert orientation, or needs
  SEV/blast-radius/next-actions from observability data without mutating cloud
  resources. Do NOT use for executing remediation, changing IAM or infra,
  sending customer comms, full incident-to- improvement/post-mortem pipelines,
  or code/repo fixes (use incident-to- improvement, diagnose with fix paths,
  or sre-devops-expert as appropriate). Korean triggers: 인시던트 요약, 장애 분류, 알림
  분석, 트리아지.
disable-model-invocation: true
---

# MSP Incident Triage Summarizer

Read-only MSP skill that turns heterogeneous incident signals into one structured triage package: severity, blast radius, ranked hypotheses, and read-only next actions—no mutations and no outbound customer messaging.

## Usage

```
/msp-incident-triage-summarizer --tenant acme-corp --cloud aws --correlation-id <uuid> "<paste alert JSON>"
/msp-incident-triage-summarizer "triage incident: CloudWatch ALARM api-5xx-high, window 15m, ECS service arn:..."
/msp-incident-triage-summarizer --cloud gcp "summarize alert: Error Reporting group + Cloud Logging samples"
/msp-incident-triage-summarizer --degraded "incident summary"   # title-only / thin context → conservative SEV + gaps
```

## Prerequisites

- **Identity**: `tenant_id`, environment (`dev`/`staging`/`prod`), and `correlation_id` on every run (tenant isolation is mandatory).
- **Cloud credentials**: read-only roles for the target cloud (AWS and/or GCP) with observability permissions only.
- **API access (examples)**:
  - **AWS**: CloudWatch (alarms, logs), X-Ray (trace read), SSM OpsCenter (optional `GetOpsItem` / `DescribeOpsItems`), ECS/CloudFormation/CodeDeploy **describe**-style calls for change context.
  - **GCP**: Cloud Monitoring (alerts/incidents), Cloud Logging `entries.list`, Error Reporting, GKE/Cloud Run/Build metadata **read** for change context.
- **Harness**: enforce token/size budgets for pasted payloads; redact secrets before LLM usage.

## Pipeline Overview

```
Fan-out (parallel, read-only)
  ├─ Alarm parser agent          → thresholds, state transitions, composite metrics, flapping
  ├─ Log correlator agent        → overlapping time windows, error clusters, service labels
  └─ Deployment diff checker     → changes in [t−Δ, t], risky touches (data plane, auth, net)

        ↓ Fan-in: merge, dedupe, timestamp alignment, fill evidence.{alarm,log,deployment}

  ├─ kwp-engineering-incident-response  → SEV1–SEV4 vocabulary + triage rubric (no comms execution)
  └─ diagnose (read-only / no-fix)     → parallel evidence pattern only; no fix/apply sub-graph

        ↓ Classify + report

  Output: JSON triage report (canonical) + short Markdown human summary
```

## Detailed Workflow

1. **Intake and validate** — Confirm `tenant_id`, environment, `correlation_id`; reject or flag cross-tenant mixing. Parse alert/incident payload for resource IDs, time window, alarm/condition names, metric/trace handles.
2. **Normalize inputs** — Map cloud-native blobs into the internal model (alarm event, bounded log windows, change records, optional trace IDs). Record truncation in `limits`.
3. **Fan-out** — Run three subagents in parallel (see Subagent Contract). Each returns structured evidence with pointers, not narrative-only guesses.
4. **Fan-in** — Merge timelines; dedupe; note contradictions; populate `evidence.alarm_interpretation`, `evidence.log_correlation`, `evidence.deployment_diff`.
5. **Compose classification** — Use `kwp-engineering-incident-response` for SEV table alignment and scope language; use `diagnose`-style parallel perspectives **without** fix steps (equivalent to `--no-fix` for production signals).
6. **Emit JSON** — Fill `severity`, `blast_radius`, `top_causes`, `next_actions` (all `read_only: true`), `data_completeness`, `limits`.
7. **Emit Markdown** — Headline, SEV/impact bullets, top hypotheses with “why,” next checks (read-only), explicit gaps/unknowns.

## Output Schema

Canonical JSON (fields may be extended in minor versions; `schema_version` tracks compatibility):

```json
{
  "schema_version": "1.0.0",
  "skill": "incident-triage-summarizer",
  "generated_at": "2026-04-23T12:00:00Z",
  "correlation_id": "uuid",
  "tenant_id": "string",
  "cloud": "aws|gcp|multi|unknown",
  "severity": {
    "level": "SEV1|SEV2|SEV3|SEV4|UNKNOWN",
    "rationale": "string",
    "confidence": 0.0
  },
  "blast_radius": {
    "summary": "string",
    "affected_scopes": [
      { "type": "region|service|cluster|namespace|project|...", "id": "string", "evidence": "string" }
    ],
    "confidence": 0.0
  },
  "top_causes": [
    {
      "rank": 1,
      "hypothesis": "string",
      "evidence": ["string"],
      "likelihood": 0.0
    }
  ],
  "next_actions": [
    {
      "priority": "P0|P1|P2",
      "action": "string",
      "owner_hint": "L1|L2|SRE|customer",
      "read_only": true
    }
  ],
  "evidence": {
    "alarm_interpretation": {},
    "log_correlation": {},
    "deployment_diff": {}
  },
  "data_completeness": {
    "missing_inputs": ["string"],
    "degraded_mode": false
  },
  "limits": {
    "input_truncation": false,
    "notes": "string"
  }
}
```

**Markdown companion** (human-facing): one-line headline, severity/impact, top 3–5 hypotheses with rationale, next 3 read-only checks, and missing-data warnings.

## Cloud Adapters

### AWS (read-only)

| Concern | Services | Examples |
|--------|----------|----------|
| Alarms / metrics | CloudWatch Alarms | `DescribeAlarms`, alarm history, metric math context, `StateReason` |
| Logs | CloudWatch Logs | `FilterLogEvents` in tight windows; cap rows |
| Traces | X-Ray | `BatchGetTraces` / summaries; bounded depth |
| Ops workflow (optional) | SSM OpsCenter | `GetOpsItem`, `DescribeOpsItems` when IDs provided |
| Change context | ECS, CodeDeploy, CloudFormation (read) | Service revisions, stack events—evidence only |

### GCP (read-only)

| Concern | Services | Examples |
|--------|----------|----------|
| Alerts | Cloud Monitoring | Incidents/policies; normalize condition, state, resource labels |
| Logs | Cloud Logging | `entries.list` with bounded filters |
| Errors | Error Reporting | Grouped errors as symptom layer; pair with logs |
| Change context | GKE, Cloud Run, Cloud Build (read) | Revisions, build IDs, namespace metadata |

Adapters **normalize** to one internal schema; authentication and query dialects differ, field names do not leak into `top_causes` without evidence pointers.

## Error Handling

- **Insufficient context** — Set `severity.level` to `UNKNOWN` or conservative SEV with low `confidence`; `data_completeness.degraded_mode: true`; `next_actions` only request more read-only artifacts.
- **API throttling / partial data** — Retry with backoff; shrink time windows; record in `limits.notes` and `missing_inputs`.
- **Contradictory evidence** — Keep both; lower confidence; spell out conflict in `evidence` subtrees.
- **PII / secrets in logs** — Redact before LLM; prefer hashed or scoped excerpts.
- **diagnose skill** — Strip fix/apply automation; never emit `read_only: false` in `next_actions` from this skill.

## Subagent Contract (fan-out)

1. **Alarm parser** — Interprets alarm JSON: threshold vs actual, state transitions, composite metrics, flapping, annotation fields (e.g., trace IDs). Output: structured `evidence.alarm_interpretation` suitable for severity and likely cause ordering.
2. **Log correlator** — Aligns log windows to the incident clock; clusters error signatures; maps to service/namespace/region from labels. Output: `evidence.log_correlation` with cluster summaries and representative lines (capped).
3. **Deployment diff checker** — Lists changes in `[t−Δ, t]` from read-only deploy metadata (ECS/CFN/CodeDeploy, GKE/Cloud Run/Build). Output: `evidence.deployment_diff` with candidate root changes and risk notes—**no** automated rollback or deploy.

**Composition notes**

- **`kwp-engineering-incident-response`**: use for SEV vocabulary and triage structure; do **not** run comms, mitigation execution, or postmortem steps inside this skill.
- **`diagnose`**: borrow the parallel “perspectives” pattern for evidence only; disable repository fix paths and any blast-radius warning that implies file edits. This is triage for cloud signals, not local code changes.

## Governance

- **Tier 1 — read-only** per `metadata.approval_spec`. No `apply`, `execute`, `send`, IAM changes, or runbook **execution** in the default graph.
- **English triggers** (illustrative): `triage incident`, `summarize alert`, `incident summary`, `classify severity`.
- **Korean triggers**: `인시던트 요약`, `장애 분류`, `알림 분석`, `트리아지`.
