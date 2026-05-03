---
name: msp-root-cause-hypothesis-builder
description: >-
  Generate ranked root-cause hypotheses from incident evidence with confidence
  scoring and counter-evidence identification. Use when triage output exists
  and you need plausible causes, RCA-style hypothesis lists, cloud
  audit/runtime correlation, or evidence gaps for L2/L3. Do NOT use for
  confirming true root cause, mutating cloud resources, sending customer
  comms, applying fixes, or replacing human RCA sign-off. Korean triggers: 근본
  원인, 가설 생성, 원인 분석, RCA.
---

# MSP Root-Cause Hypothesis Builder

Read-only incident investigation skill. Consumes **Skill #1 — Incident Triage Summarizer** output (triage JSON) plus optional observability and audit evidence, and produces a **ranked list of testable root-cause hypotheses** with confidence, supporting/contradicting evidence, and gaps. **Does not assert ground truth.**

## Summary

- **Tier 1 — read-only:** No cloud mutations, no identity or billing changes, no outbound customer messaging.
- **Primary input:** Triage report JSON from `msp-incident-triage-summarizer` (see registry/plans for field contract).
- **Composition:** Uses the **structured reasoning pattern** from `diagnose` (`.cursor/skills/review/diagnose/SKILL.md`) — evidence → competing explanations → synthesis — **without** auto-fixes, merges of definitive “root cause” language, or closure claims.
- **Output:** One JSON artifact matching **Output Schema** below + short markdown summary for humans.

## Usage Examples

```
/msp-root-cause-hypothesis-builder --triage outputs/msp/triage-report.json
/msp-root-cause-hypothesis-builder "root cause hypothesis for last hour's ALB 5xx" + paste Skill #1 JSON
/msp-root-cause-hypothesis-builder --tenant acme --window 2026-04-23T13:00:00Z/2026-04-23T14:00:00Z
```

**English triggers:** root cause hypothesis, RCA builder, cause analysis, hypothesis generation.

## Prerequisites

- **Triage JSON** from Skill #1 (minimum: `incident_id`, `tenant_id`, `time_window`, `severity`, `summary`, `affected_resources`, `primary_signals`; optional: `blast_radius_hints`).
- **Read-only** cloud access: viewer / read APIs scoped to the tenant (see Cloud Adapters).
- Optional: redacted log excerpts, metric query definitions, deployment/change references from triage.
- Implementations SHOULD validate tenant id and time window before queries.

## CRITICAL LANGUAGE RULE

**The phrase “root cause confirmed” and equivalent definitive claims are PROHIBITED** in this skill’s outputs and in prompts that drive it.

| Use | Do not use |
|-----|------------|
| hypothesis, candidate, leading hypothesis | root cause confirmed, verified RC |
| likely, suggests, consistent with | we know the RC is X, definitively caused by |
| confidence 0.62 (medium), confidence band | proven, certain, closed |

JSON MUST use `hypotheses[]` — **not** a single `root_cause` field. Include the normative `disclaimer` string in the JSON artifact.

## Pipeline Overview

**Sequential pipeline** (single pass; no parallel mutation groups):

```
Collect & validate evidence
        ↓
Generate N competing hypotheses (default 3–7)
        ↓
Score confidence + label supporting / contradicting / missing evidence
        ↓
Rank + counter-evidence + evidence_gaps + next_investigation_steps (read-only)
```

## Detailed Workflow

1. **Ingest Skill #1 triage report**
   Validate JSON (required fields, RFC3339 `time_window`, `tenant_id`). Extract `affected_resources`, `primary_signals`, and blast-radius hints for scoped queries.

2. **Gather additional evidence (read-only)**
   Within the same window and blast radius: CloudTrail / GCP Audit Logs; CloudWatch / Cloud Monitoring metrics and log samples; AWS Config / GCP Asset Inventory where relevant. De-duplicate; attach citations (event id, query id, metric name + timestamp). Redact PII/secrets before LLM; cite pointers to raw stores for humans.

3. **Generate N hypotheses**
   Cover mechanisms and failure modes (e.g. config change, dependency outage, quota, bad deploy, credential expiry, network partition). **N** configurable (default 3–7).

4. **Score each hypothesis**
   For each: tag evidence as supporting, contradicting, or missing. Apply confidence rubric (0.0–1.0); set `confidence_band` (low | medium | high). Require **counter_evidence** and **falsification_criteria**; cap confidence when gaps are large.

5. **Rank and next steps**
   Sort by `confidence` (then by severity of remaining gaps). Emit `evidence_gaps` with **read-only** `suggested_collection` (queries, not mutating runbooks). Order `next_investigation_steps`.

**Optional:** Run **diagnose-inspired** prompts in-process (same session) instead of full multi-agent `diagnose` to limit tool/token scope; still **no fixes** and **no** definitive root-cause wording.

## Output Schema

**Normative JSON** (plus human-readable markdown summary). `skill_version` SHOULD match this skill’s `metadata.version`.

```json
{
  "incident_id": "string",
  "tenant_id": "string",
  "skill_version": "1.0.0",
  "generated_at": "2026-04-23T12:00:00Z",
  "disclaimer": "Hypotheses are not confirmed root causes. Confidence reflects evidence fit, not certainty.",
  "hypotheses": [
    {
      "id": "H1",
      "title": "string",
      "statement": "string",
      "confidence": 0.0,
      "confidence_band": "low | medium | high",
      "evidence": [
        {
          "type": "audit_trail | metric | log | config | inventory | other",
          "source": "e.g. cloudtrail:LookupEvents",
          "citation": "string (event id, query, or pointer)",
          "supports": true,
          "notes": "string"
        }
      ],
      "counter_evidence": [
        {
          "description": "string",
          "citation": "string"
        }
      ],
      "evidence_gaps": [
        {
          "gap": "string",
          "suggested_collection": "string (read-only query or next step)"
        }
      ],
      "falsification_criteria": [
        "string"
      ]
    }
  ],
  "next_investigation_steps": [
    {
      "priority": 1,
      "action": "string",
      "rationale": "string"
    }
  ],
  "cloud_correlation_notes": {
    "aws": "string (optional)",
    "gcp": "string (optional)"
  }
}
```

**Confidence:** `confidence` is 0.0–1.0; `confidence_band` MUST align with numeric rules in the implementation. Factual cloud claims in `evidence` SHOULD be traceable to tool/read API output (avoid hallucinated citations).

## Cloud Adapters (Read-Only)

Invocation MUST use **read-only** IAM / viewer roles scoped to the tenant. **No mutating APIs.**

| Cloud | Sources | Role in this skill |
|-------|---------|--------------------|
| **AWS** | **CloudTrail** (management events), **CloudWatch** (logs, metrics, alarms, Contributor Insights as applicable), **AWS Config** (resource configuration timeline, relationships) | Correlate who changed what and when with metric/log symptoms; test misconfiguration vs. external traffic (e.g. ELB/ECS: Trail near window → Config listener/health check → CloudWatch 5xx/target health). |
| **GCP** | **Cloud Audit Logs** (Admin Activity; Data Access where policy allows), **Cloud Monitoring** (metrics, logs, SLOs), **Asset Inventory** (resource metadata and history) | Align failure windows with admin changes; GKE/SQL/LB: audit → monitoring crash/error signals → asset drift (e.g. firewall, node pool). |

**Query templates** SHOULD be parameterized (`time_window`, account/project, resources from triage). **Rate limits / pagination:** handle gracefully; label partial results in `evidence_gaps`.

## Error Handling

| Scenario | Action |
|----------|--------|
| Missing or invalid Skill #1 JSON | Stop; list required fields and request valid triage output. |
| Triage time window too wide | Narrow or ask for bounds; note query budget in `evidence_gaps`. |
| Read API throttling / partial data | Record partial results; fill `evidence_gaps` with what failed to fetch. |
| No audit/config data in window | Still emit hypotheses with **lower** confidence; expand `evidence_gaps`. |
| Tenant isolation / auth failure | Do not fall back to another tenant; fail closed with clear error. |
| Model output uses forbidden phrasing | Reject or rewrite; enforce **CRITICAL LANGUAGE RULE** and schema without `root_cause`. |
| `diagnose` pattern suggests a single “fix” | Strip fix instructions from deliverable; map only to ranked hypotheses and read-only next steps. |

## Governance

- **Approval Tier:** Tier 1 — fully read-only, no human gate required.
- **Mutations:** None. This skill reads telemetry, logs, and configuration data; it never modifies infrastructure, IAM, or incident state.
- **Prohibited:** Executing fixes, applying patches, modifying resources, or confirming a root cause (see CRITICAL LANGUAGE RULE above).

## Cross-References

- [`docs/msp-skills/APPROVAL_BOUNDARY_SPEC.md`](../../../docs/msp-skills/APPROVAL_BOUNDARY_SPEC.md) — Tier 1 rules
- [`docs/msp-skills/MSP_SKILL_REGISTRY.md`](../../../docs/msp-skills/MSP_SKILL_REGISTRY.md) — suite index
- [`docs/msp-skills/plans/root-cause-hypothesis-builder.md`](../../../docs/msp-skills/plans/root-cause-hypothesis-builder.md) — planning source
- Upstream: Skill #1 plan — `docs/msp-skills/plans/incident-triage-summarizer.md`
- Composed pattern: [`.cursor/skills/review/diagnose/SKILL.md`](../review/diagnose/SKILL.md) (read-only subset; no auto-fix)
