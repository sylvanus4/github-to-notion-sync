---
name: msp-runbook-recommender
description: >-
  MSP read-only skill that matches incident context (triage + optional
  hypothesis) against a tenant-scoped runbook catalog to recommend the top-3
  best-fit runbooks with prerequisites, parameters, estimated effects, and side
  effects—without executing any automation. Consumes Skill #1
  (incident-triage-summarizer) JSON as primary input and optionally Skill #2
  (root-cause-hypothesis-builder) JSON for tighter matching. Uses
  infra-runbook-generator conventions for catalog parsing. Use when the user
  asks to recommend runbook, match runbook, suggest remediation procedure,
  runbook recommendation, find runbook for incident, MSP runbook match, which
  runbook should I run, or needs ranked operational procedure suggestions from
  triage/hypothesis context without executing anything. Do NOT use for executing
  runbooks (use runbook-executor-with-approval), generating new runbook
  documents from IaC (use infra-runbook-generator), incident triage without
  runbook matching (use incident-triage-summarizer), root cause analysis without
  runbook context (use root-cause-hypothesis-builder), or general infrastructure
  review without incident context. Korean triggers: 런북 추천, 런북 매칭, 조치
  절차 추천, 런북 찾기, 인시던트 런북.
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "msp/automation"
  approval_tier: "tier-1"
  approval_spec: "docs/msp-skills/APPROVAL_BOUNDARY_SPEC.md"
  mutations: []
  clouds:
    - "aws"
    - "gcp"
  composes:
    - "incident-triage-summarizer"
    - "root-cause-hypothesis-builder"
    - "infra-runbook-generator"
---

# MSP Runbook Recommender

Read-only MSP skill that selects and ranks the best-fit operational runbooks from a tenant-scoped catalog for a given incident context. Answers "which procedures should an engineer consider next?" without executing any automation, mutation, or customer-facing communication.

## Usage

```
/msp-runbook-recommender --tenant acme-corp --correlation-id <uuid> --triage <path-to-skill1-json>
/msp-runbook-recommender --tenant acme-corp --correlation-id <uuid> --triage <skill1.json> --hypothesis <skill2.json>
/msp-runbook-recommender "recommend runbook for EKS crashloop in namespace payments" --tenant acme-corp
```

## Prerequisites

- **Skill #1 output**: Valid `incident-triage-summarizer` JSON envelope with `tenant_id`, `correlation_id`, `cloud`, `severity`, `blast_radius`, `top_causes`, and `evidence`.
- **Runbook catalog**: At least one configured source per tenant (markdown repo, SSM document index, GCP Workflow manifests, or a combined catalog index).
- **Identity**: `tenant_id` and `correlation_id` on every invocation (tenant isolation mandatory).
- **Cloud credentials**: Read-only roles for catalog metadata discovery (e.g., `ssm:ListDocuments`, `ssm:GetDocument`, `workflows.list`, `run.jobs.list`).

## Pipeline Overview

```
Inputs
  ├─ Skill #1 triage JSON (required)
  └─ Skill #2 hypothesis JSON (optional)

        ↓ Build incident signature

Catalog Resolution
  ├─ Tenant-scoped catalog load (markdown, SSM index, Workflow/Job metadata)
  └─ Customer overrides / allowlists

        ↓ Match + Score + Rank

Recommendation Generation
  ├─ Top-3 runbooks with match_score, effects, prerequisites, side_effects, parameters_needed
  └─ Summary with rationale and audit references

        ↓ Output

  JSON recommendation report + Markdown human summary
```

## Detailed Workflow

1. **Ingest incident context** — Validate `tenant_id`, `correlation_id`, triage JSON schema version. If Skill #2 JSON is provided, validate `correlation_id` alignment. Build an **incident signature**: normalized `cloud`, severity, affected scopes, top symptoms/causes, keywords, evidence types.

2. **Load runbook catalog** — Resolve tenant catalog source(s) with optional overrides. For each adapter (markdown files, SSM document index, GCP Workflow manifests, Cloud Run job metadata), load metadata and content into a bounded context. Enforce tenant isolation: never mix another tenant's catalog paths or allowlists.

3. **Match incident signature to runbook preconditions** — Apply rule-based filters first (cloud provider, service type, cluster/namespace, alert name patterns). Then apply semantic matching on runbook Overview, Diagnosis, Symptoms sections and SSM/Workflow descriptions.

4. **Score relevance and rank** — Compute composite score: keyword overlap, embedding similarity if available, and optional LLM grader with strict "cite catalog span" instruction. Produce **top-3** with `match_score` in [0, 1].

5. **Estimate side effects** — Derive from runbook Resolution, Rollback, and automation step descriptions: restarts, replacements, data movement, brief outages. If evidence is missing, use conservative language and lower confidence. Never invent cloud APIs not present in catalog text.

6. **Generate recommendation report** — Emit JSON envelope + markdown summary. Attach `limits` if catalog is partial or context was truncated. Include explicit statement that recommendations are for human review and not executed by this skill.

## Output Schema

```json
{
  "schema_version": "1.0.0",
  "skill": "runbook-recommender",
  "generated_at": "ISO-8601",
  "correlation_id": "uuid",
  "tenant_id": "string",
  "inputs": {
    "triage_schema_version": "1.0.0",
    "hypothesis_schema_version": "1.0.0 | null"
  },
  "recommendations": [
    {
      "runbook_id": "string",
      "title": "string",
      "match_score": 0.0,
      "expected_effects": ["string"],
      "prerequisites": ["string"],
      "estimated_duration": "string",
      "side_effects": ["string"],
      "parameters_needed": [
        { "name": "string", "type": "string", "required": true, "source_hint": "string" }
      ],
      "rationale": "string"
    }
  ],
  "summary": "string",
  "limits": {
    "catalog_partial": false,
    "input_truncation": false,
    "notes": "string"
  }
}
```

## Cloud Adapters

### AWS (read-only)

| Source | Discovery | Notes |
|--------|-----------|-------|
| SSM Automation documents | `ListDocuments` / pre-synced catalog index | Read-only; no `StartAutomationExecution` |
| SSM OpsCenter | `GetOpsItem` suggested runbook links | Read metadata only |
| Markdown repo | Git-synced files following `infra-runbook-generator` format | Sections: Overview, Prerequisites, Diagnosis, Resolution, Rollback, Escalation |

### GCP (read-only)

| Source | Discovery | Notes |
|--------|-----------|-------|
| Cloud Workflows | `workflows.list` / exported YAML from Git | Parse step definitions for prerequisite/effect extraction |
| Cloud Run jobs | `run.jobs.list` / describe metadata | Job env expectations as catalog entries |
| Markdown repo | Same pattern as AWS | Scripts treated as catalog entries with declared parameters |

## Composed Skills

| Skill | Role |
|-------|------|
| **incident-triage-summarizer** (Skill #1) | Primary structured incident input (severity, blast radius, causes, evidence) |
| **root-cause-hypothesis-builder** (Skill #2) | Optional boost: hypothesis titles, evidence types, gaps to tighten matching |
| **infra-runbook-generator** | Conventions for markdown runbook shape (sections, prerequisites, resolution steps) enabling consistent parsing |

The recommender does not run the generator in the request path; it consumes **pre-built** runbook artifacts.

## Error Handling

- **Missing triage input** — Reject with clear error; triage JSON is the minimum required context.
- **Catalog unavailable or empty** — Return zero recommendations with `limits.catalog_partial: true` and suggest manual catalog check.
- **Degraded incident data** — If `data_completeness.degraded_mode` is true in triage input, widen uncertainty in `match_score`, expand `parameters_needed`, and note degraded mode in output.
- **Cloud mismatch** — If triage `cloud` does not match top runbook's target cloud, downrank and flag explicitly in summary.
- **LLM hallucination guard** — RAG/retrieval over grounded catalog text; require citations to catalog spans; refuse to assert steps not present in catalog text.

## Governance

- **Tier 1 — read-only** per `metadata.approval_spec`. No `execute`, `apply`, `start`, `run`, or any mutation in the skill's graph.
- Every output artifact states that recommendations are **for human review** and not executed by this skill.
- **English triggers**: `recommend runbook`, `match runbook`, `suggest procedure`, `which runbook`, `runbook for incident`.
- **Korean triggers**: `런북 추천`, `런북 매칭`, `조치 절차 추천`, `런북 찾기`, `인시던트 런북`.
