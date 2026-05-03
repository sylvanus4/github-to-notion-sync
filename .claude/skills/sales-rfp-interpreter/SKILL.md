---
name: sales-rfp-interpreter
description: >-
  Parse RFP documents, customer emails, and meeting transcripts to extract
  structured requirements with ThakiCloud-specific taxonomy (on-prem
  deployment, data sovereignty, audit logging, multi-tenant isolation, model
  serving, GPU allocation). Produces a requirements table, missing-question
  list, security/sovereignty risk flags, and internal confirmation checklist.
  Use when the user asks to "parse RFP", "interpret customer requirements",
  "extract requirements from RFP", "structure customer document", "RFP 해석",
  "고객 요구사항 추출", "RFP 분석", "요구사항 구조화", "고객 문서 파싱", "sales-rfp-interpreter", or
  receives a customer RFP/email/meeting note that needs structured requirement
  extraction. Do NOT use for general document summarization without
  requirement extraction (use long-form-compressor). Do NOT use for technical
  feasibility analysis only (use cloud-requirements-analyst). Do NOT use for
  proposal generation (use sales-proposal-architect). Do NOT use for security
  Q&A without RFP context (use sales-security-qa).
---

# Sales RFP / Customer Requirements Interpreter

Extract, classify, and structure customer requirements from unstructured documents into an actionable ThakiCloud-specific format — requirements table, missing questions, risk flags, and confirmation checklist.

## When to Use

- Customer sends an RFP (PDF/DOCX) that needs structured requirement extraction
- Sales receives an email or meeting transcript containing implicit requirements
- Pre-proposal requirement analysis before engaging #2 (security Q&A) and #3 (proposal architect)
- Internal confirmation checklist generation for cross-team review (PM, security, legal)

## Pipeline

```
Input Document (RFP / Email / Meeting Note)
       │
       ▼
┌─────────────────────────────┐
│  Phase 1: Document Ingestion │
│  opendataloader (PDF/DOCX)   │
│  OR plain text extraction    │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Phase 2: Requirement        │
│  Extraction & Classification │
│  structured-extractor with   │
│  ThakiCloud taxonomy schema  │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Phase 3: Gap Analysis       │
│  Detect missing items via    │
│  ThakiCloud checklist        │
│  kb-query for policy lookup  │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Phase 4: Risk Tagging       │
│  Security/sovereignty flags  │
│  Feasibility pre-check via   │
│  cloud-requirements-analyst  │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Phase 5: Output Assembly    │
│  Requirements table (JSON+MD)│
│  Missing questions list      │
│  Risk flags                  │
│  Internal checklist          │
└─────────────────────────────┘
```

## ThakiCloud Requirement Taxonomy

Every extracted requirement MUST be classified into one or more of these categories:

| Category | Examples |
|----------|----------|
| **Deployment Model** | On-premise, hybrid, cloud-only, air-gapped |
| **Data Sovereignty** | Data residency, cross-border transfer restrictions, data classification |
| **Security & Compliance** | Audit logging, encryption at rest/transit, RBAC, SSO/SAML, certifications (ISO27001, SOC2, CSAP) |
| **Multi-Tenant Isolation** | Namespace isolation, network policies, resource quotas, tenant data separation |
| **Model Serving** | vLLM, TGI, custom runtime, model registry, A/B serving, canary deployment |
| **GPU / Compute** | GPU type requirements (A100/H100/B200), MIG partitioning, scheduling, quota management |
| **Networking** | VPN, private link, ingress/egress controls, firewall rules |
| **Operations** | Monitoring, alerting, backup/DR, SLA requirements, support tiers |
| **Integration** | API compatibility, SSO providers, storage backends, CI/CD integration |
| **Licensing & Commercial** | Pricing model, SLA terms, support scope, contract duration |

## Output Schema

### Requirements Table (JSON)

```json
{
  "metadata": {
    "source_type": "rfp | email | meeting_note",
    "source_name": "filename or subject",
    "customer_name": "string",
    "extracted_at": "ISO-8601",
    "total_requirements": 0,
    "confidence_score": 0.0
  },
  "requirements": [
    {
      "id": "REQ-001",
      "category": "taxonomy category",
      "requirement": "description",
      "priority": "must | should | nice-to-have | unclear",
      "source_reference": "page/section/line",
      "thakicloud_capability": "supported | partial | roadmap | not-supported",
      "notes": "clarification needed or implementation notes"
    }
  ],
  "missing_questions": [
    {
      "id": "MQ-001",
      "category": "taxonomy category",
      "question": "what is missing",
      "why_needed": "impact on proposal/implementation",
      "suggested_default": "ThakiCloud standard approach if not specified"
    }
  ],
  "risk_flags": [
    {
      "id": "RF-001",
      "severity": "high | medium | low",
      "category": "taxonomy category",
      "description": "risk description",
      "mitigation": "suggested approach",
      "escalation_to": "security | legal | pm | engineering"
    }
  ],
  "confirmation_checklist": [
    {
      "team": "security | pm | legal | engineering",
      "items": ["item requiring confirmation"]
    }
  ]
}
```

## Execution Instructions

### Step 0 — Input Validation

1. Verify the input is non-empty. If empty or placeholder text only, abort with a clear error message.
2. For PDF/DOCX: confirm the file is not corrupted (opendataloader returns valid markdown). If extraction yields < 50 characters, flag as "possibly corrupted or image-only PDF" and request an alternative format.
3. For meeting transcripts: verify at least 3 distinct speaker turns or 200+ words exist — shorter fragments rarely contain extractable requirements.

### Step 1 — Ingest Document

1. If input is PDF/DOCX: use `opendataloader` (preferred) for high-fidelity markdown extraction. Fallback to `anthropic-pdf` if opendataloader is unavailable.
2. If input is email: extract body text directly.
3. If input is meeting transcript: use the raw text, preserving speaker labels if available.

### Step 2 — Extract Requirements

1. Read the extracted text line-by-line.
2. Detect the document's primary language. For bilingual (Korean + English) documents, extract requirements from both languages and unify duplicates, preferring the more specific phrasing.
3. For each requirement-like statement, classify using the ThakiCloud Requirement Taxonomy.
4. Assign priority based on language signals:
   - **Must**: "must", "shall", "required", "mandatory" / Korean: "필수", "반드시", "의무"
   - **Should**: "should", "prefer", "recommend" / Korean: "권장", "바람직", "우선"
   - **Nice-to-have**: "nice to have", "optional", "desirable" / Korean: "선택", "가능하면", "희망"
   - **Unclear**: ambiguous phrasing or Korean honorific hedging ("~했으면 합니다", "~부탁드립니다") — default to unclear rather than guessing
5. Deduplicate requirements: if the same capability is mentioned in multiple sections (common in multi-department RFPs), merge into a single requirement, combine source references, and keep the stricter priority.
6. Cross-reference each requirement against ThakiCloud capabilities using `kb-query` on the `product-strategy` and `engineering-standards` KB topics. If KB topics return empty results or are unavailable, mark `thakicloud_capability` as `"unclear"` with a note: "KB lookup returned no results — manual verification required."
7. Mark `thakicloud_capability` as supported/partial/roadmap/not-supported/unclear.

### Step 3 — Gap Analysis

1. Compare extracted requirements against the ThakiCloud standard checklist (all 10 taxonomy categories).
2. For each category with zero requirements, generate a missing question.
3. Generate at minimum 5 missing questions, maximum 15.
4. For each missing question, provide a suggested ThakiCloud default approach.

### Step 4 — Risk Tagging

1. Flag any requirement touching data sovereignty, air-gap deployment, or regulatory compliance as HIGH risk.
2. Flag custom integration or non-standard GPU requirements as MEDIUM risk.
3. Use `cloud-requirements-analyst` to pre-check technical feasibility for flagged items.
4. Assign escalation targets (security, legal, PM, engineering).

### Step 5 — Assemble Output

1. Generate the JSON output following the schema above.
2. Generate a parallel markdown summary table for human review.
3. Persist outputs to `outputs/sales-rfp/{date}/{customer-slug}/`.

## Constraints

- Output the simplest actionable requirements table — do not pad with speculative requirements not grounded in the source document
- Maximum 30 requirements per RFP; if more exist, prioritize by must > should > nice-to-have and note truncation
- Never infer ThakiCloud capability status without KB evidence; mark as "unclear" if no match found
- Risk flags must cite the specific source text that triggered the flag
- Do not generate the proposal or security answers — hand off to downstream skills
- JSON output must be < 50KB total; if larger, split into core requirements + appendix
- Every risk flag MUST include a verbatim quote from the source document as evidence

## Gotchas

- PDF tables with merged cells often break `opendataloader` extraction — verify table outputs manually when source has complex layouts
- Korean-language RFPs may use honorific business language that obscures whether a requirement is mandatory or optional; default to "unclear" priority rather than guessing
- Customer emails often mix requirements with pleasantries/context — only extract statements with actionable technical or commercial implications
- The `structured-extractor` JSON schema must exactly match the Output Schema above; mismatched field names cause silent downstream failures in `sales-proposal-architect`
- Air-gap deployment requirements are frequently implicit (e.g., "no external network access") rather than explicitly stated as "air-gap" — scan for synonyms

## Verification

Before marking output as complete:
1. Confirm every requirement has a valid taxonomy category — reject "uncategorized" entries
2. Verify missing questions cover at least 5 of the 10 taxonomy categories
3. Check that HIGH-risk flags all have an assigned escalation target
4. Validate JSON output parses without error

## Autonomy Level: L2

- **Auto**: Document ingestion, requirement extraction, gap analysis, risk tagging
- **Human Review Required**: All outputs before sharing externally or feeding into sales-proposal-architect
- **Never Auto**: Customer-facing communications, commitment to capability claims

## Integration Points

- **Upstream**: Customer sends RFP/email/meeting transcript
- **Downstream**: Feeds into `sales-security-qa` (risk flags trigger security Q&A) and `sales-proposal-architect` (requirements table feeds proposal drafting)
- **Harness**: Invoked as Phase 1 of `sales-agent-harness` in `rfp-flow` mode
