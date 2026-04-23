---
name: sales-security-qa
version: 1.0.0
description: >
  Answer customer security, sovereignty, and on-premise deployment questions
  using a versioned ThakiCloud policy knowledge base. Generates segment-specific
  answer drafts (public sector, financial, general enterprise) with evidence
  links and confidence scores. Auto-escalates unresolved items to legal/security/PM.
  NEVER auto-sends answers to customers — always requires human approval.
  Use when the user asks to "answer security question", "security Q&A",
  "sovereignty question", "on-prem FAQ", "보안 질의 답변", "주권 질문",
  "온프레미스 FAQ", "sales-security-qa", "보안 Q&A", "규제 질문 답변",
  or receives a customer question about security/compliance/data sovereignty.
  Do NOT use for general customer support (use kwp-customer-support-response-drafting).
  Do NOT use for internal security audit (use security-expert).
  Do NOT use for RFP parsing (use sales-rfp-interpreter).
  Do NOT use for proposal generation (use sales-proposal-architect).
tags: [sales, security, sovereignty, on-premise, compliance, qa, policy, thakicloud]
triggers:
  - "answer security question"
  - "security Q&A"
  - "sovereignty question"
  - "on-prem FAQ"
  - "compliance question answer"
  - "sales-security-qa"
  - "보안 질의 답변"
  - "보안 Q&A"
  - "주권 질문"
  - "온프레미스 FAQ"
  - "규제 질문 답변"
  - "보안 답변 초안"
  - "고객 보안 질문"
do_not_use:
  - "General customer support without security focus (use kwp-customer-support-response-drafting)"
  - "Internal security audit or threat modeling (use security-expert)"
  - "RFP parsing without Q&A intent (use sales-rfp-interpreter)"
  - "Proposal generation (use sales-proposal-architect)"
  - "Knowledge base CRUD operations (use kb-orchestrator)"
composes:
  - kb-query
  - kwp-customer-support-customer-research
  - sentence-polisher
  - gws-email-reply
metadata:
  author: "thaki"
  category: "sales-agents/security"
  autonomy: "L2"
  kb_topic: "security-sovereignty"
---

# Sales Security / Sovereignty / On-Premise Q&A Agent

Generate policy-grounded, segment-specific answer drafts for customer security, data sovereignty, and on-premise deployment questions — with mandatory human approval before any external delivery.

## When to Use

- Customer asks about ThakiCloud's security posture, certifications, or compliance
- Customer questions about data sovereignty, residency, or cross-border transfer
- On-premise or air-gapped deployment capability questions
- Repeated security questionnaire completion (e.g., vendor security assessment forms)
- Risk flags from `sales-rfp-interpreter` that need security-focused answers

## Critical Safety Rule

```
┌─────────────────────────────────────────────────────┐
│  ⚠ NEVER AUTO-SEND ANSWERS TO CUSTOMERS             │
│                                                       │
│  Wrong security/compliance answers can create          │
│  contractual liability and deal risk.                  │
│                                                       │
│  EVERY answer MUST be reviewed by a human before       │
│  delivery. No exceptions. No "auto-reply" mode.        │
└─────────────────────────────────────────────────────┘
```

## Pipeline

```
Customer Question (text / email / RFP security section)
       │
       ▼
┌─────────────────────────────┐
│  Phase 1: Question           │
│  Classification              │
│  Topic + customer segment    │
│  identification              │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Phase 2: Policy Lookup      │
│  kb-query on                 │
│  security-sovereignty KB     │
│  + product-strategy KB       │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Phase 3: Answer Generation  │
│  Segment-specific drafting   │
│  Evidence link attachment    │
│  Confidence scoring          │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Phase 4: Escalation Check   │
│  Flag items needing          │
│  legal / security / PM       │
│  confirmation                │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Phase 5: Draft Delivery     │
│  sentence-polisher for       │
│  quality, then present to    │
│  human for approval          │
└─────────────────────────────┘
```

## Customer Segments

Answers MUST be adapted based on the customer segment:

| Segment | Key Concerns | Answer Tone |
|---------|-------------|-------------|
| **Public Sector (공공)** | CSAP certification, data residency within Korea, government audit requirements, closed network deployment | Formal, compliance-focused, reference specific Korean regulations |
| **Financial (금융)** | Financial supervisory compliance, data encryption standards, audit trail requirements, disaster recovery SLA | Precise, quantitative, reference financial industry standards |
| **General Enterprise** | SOC2/ISO27001, SSO integration, RBAC, multi-tenant isolation, SLA guarantees | Balanced technical + business, focus on operational assurance |

## Question Classification Taxonomy

| Category | Sub-topics |
|----------|-----------|
| **Authentication & Access** | SSO/SAML, RBAC, MFA, API key management, service accounts |
| **Data Protection** | Encryption at rest/transit, key management, data classification, DLP |
| **Data Sovereignty** | Residency, cross-border, data processing location, deletion guarantees |
| **Network Security** | VPN, private link, firewall, ingress/egress, DDoS protection |
| **Compliance & Certification** | SOC2, ISO27001, CSAP, ISMS, GDPR, industry-specific |
| **Audit & Logging** | Audit trail, log retention, tamper-proof logging, SIEM integration |
| **Deployment Model** | On-premise, air-gapped, hybrid, multi-cloud, edge |
| **Tenant Isolation** | Namespace isolation, network policy, resource quota, data separation |
| **Incident Response** | SLA, escalation, notification timeline, post-mortem process |
| **Backup & DR** | RPO/RTO, backup frequency, geo-redundancy, failover |

## Answer Output Schema

```json
{
  "question_id": "SQ-001",
  "original_question": "customer's question text",
  "classification": {
    "category": "taxonomy category",
    "sub_topic": "specific sub-topic",
    "customer_segment": "public | financial | enterprise",
    "complexity": "standard | requires-confirmation | novel"
  },
  "answer_draft": {
    "text": "full answer text adapted for the customer segment",
    "evidence_links": [
      {"source": "document name", "section": "specific section", "url": "internal or public URL"}
    ],
    "confidence_score": 0.85,
    "confidence_rationale": "why this score"
  },
  "escalation": {
    "needed": true,
    "team": "legal | security | pm | engineering",
    "reason": "why escalation is needed",
    "items_to_confirm": ["specific items needing confirmation"]
  },
  "metadata": {
    "kb_version": "date of last KB update",
    "generated_at": "ISO-8601",
    "policy_docs_referenced": ["list of policy documents used"]
  }
}
```

## Execution Instructions

### Step 0 — Input Validation

1. Verify the question is non-empty and contains at least one identifiable security/compliance topic keyword. If no security relevance is detected, respond with "This question does not appear to be security/compliance related — please route to the appropriate team or rephrase."
2. For batch inputs (multiple questions in one message or RFP security section): split into individual questions, assign sequential IDs (SQ-001, SQ-002, ...), and process each independently. Combine into a single response document at the end.
3. Check `security-sovereignty` KB freshness: if the latest article's `updated_at` is older than 30 days, prepend a warning to the output: "⚠️ Security KB last updated {date} — answers may not reflect the latest policy changes. Recommend running kb-compile on security-sovereignty topic."

### Step 1 — Classify the Question

1. Detect question language. For Korean questions, extract the security topic using Korean security terminology (e.g., "개인정보", "망분리", "접근통제"). For bilingual questions, process both languages and unify into a single classification.
2. Parse the customer question to identify the security/compliance category and sub-topic from the Question Classification Taxonomy.
3. Determine the customer segment (public/financial/enterprise) from context clues:
   - Public sector signals: mentions of "공공", government agency names, CSAP, "행정안전부", "조달청"
   - Financial signals: mentions of "금융", FSS/FSC, "금감원", ISMS-P, specific financial regulations
   - Enterprise signals: mentions of SOC2, ISO27001, general compliance without sector-specific regulations
   - If ambiguous: ask the user rather than guessing — segment misidentification leads to wrong answer tone
4. Classify complexity: `standard` (covered by existing policy docs), `requires-confirmation` (partially covered, needs team input), `novel` (not covered by any existing docs).

### Step 2 — Policy Knowledge Lookup

1. Query `kb-query` against the `security-sovereignty` KB topic first. If the topic is empty or returns no results, note this as a KB gap and proceed to step 2 — do not fail the entire pipeline.
2. If insufficient coverage, extend to `product-strategy` and `engineering-standards` topics.
3. Use `kwp-customer-support-customer-research` for multi-source enrichment if KB results are thin.
4. If all KB lookups return empty: set confidence score to 0.5 maximum, classify as `requires-confirmation`, and note "No policy documentation found — answer is based on general ThakiCloud knowledge and MUST be verified by the security team before delivery."
5. Record all source documents referenced for evidence links.

### Step 3 — Generate Segment-Specific Answer

1. Draft the answer using the segment-appropriate tone (see Customer Segments table).
2. For public sector: reference Korean regulations and CSAP explicitly.
3. For financial: include quantitative metrics (encryption bit-strength, SLA percentages, RPO/RTO numbers).
4. For enterprise: balance technical detail with business assurance language.
5. Attach evidence links to every factual claim.
6. Calculate confidence score: 0.9+ if all claims backed by current KB docs; 0.7-0.9 if some inference needed; <0.7 triggers mandatory escalation.

### Step 4 — Escalation Check

1. Auto-escalate to `legal` if the question involves contractual commitments, liability, or regulatory interpretation.
2. Auto-escalate to `security` if the question involves specific vulnerability details, penetration test results, or incident history.
3. Auto-escalate to `pm` if the question involves unreleased features or roadmap commitments.
4. Auto-escalate to `engineering` if the question requires specific architecture details not in the KB.
5. For `novel` questions (no KB coverage): always escalate and note the gap for KB enrichment.

### Step 5 — Polish and Present

1. Run `sentence-polisher` on the answer draft for grammar and tone consistency.
2. Present the full output (answer + evidence + escalation flags) to the human reviewer.
3. If approved, optionally use `gws-email-reply` to prepare the customer-facing response.
4. Log the Q&A pair for future KB enrichment.

## Constraints

- Answer length must match question complexity: `standard` ≤ 300 words, `requires-confirmation` ≤ 500 words, `novel` ≤ 200 words (since most content will be "we need to verify")
- Never claim a certification ThakiCloud does not currently hold; use "in progress, target date: YYYY-QN" for roadmap items
- Confidence scores below 0.7 MUST trigger escalation — no exceptions
- Evidence links must point to specific document sections, not entire documents — generic "see our security whitepaper" is NOT acceptable
- Do not mix customer segments in a single answer — if segment is unknown, ask before drafting
- Batch responses must not exceed 20 questions per run; for larger batches, split into chunks and process sequentially
- Every factual claim about ThakiCloud's security posture MUST include a verbatim quote or specific reference from a KB document as evidence

## Gotchas

- Compliance certification status changes frequently — always verify against the latest `compliance-roadmap.md` in the security-sovereignty KB before answering
- Public sector (공공) customers require CSAP-specific language; referencing only SOC2/ISO27001 is insufficient and signals lack of Korean market understanding
- "Data sovereignty" means different things to different segments: for public sector it means physical data residency within Korea; for financial it means regulatory audit access; for enterprise it may just mean data ownership
- Questions about penetration test results or specific vulnerability details MUST be escalated to security — never draft answers for these even if KB has partial data
- Air-gap deployment answers must distinguish between "supported" (production-ready) vs "possible with customization" (requires engineering engagement)

## Verification

Before presenting answers to the human reviewer:
1. Every factual claim has at least one evidence link to a KB document
2. Confidence score calculation follows the documented formula (0.9+ / 0.7-0.9 / <0.7)
3. Escalation flags are set for all `novel` and `requires-confirmation` questions
4. Answer tone matches the identified customer segment
5. No certification claims exceed what's documented in `compliance-roadmap.md`

## Autonomy Level: L2

- **Auto**: Question classification, KB lookup, answer draft generation, escalation flagging
- **Human Review Required**: Every answer before customer delivery (NO exceptions)
- **Never Auto**: Sending answers to customers, making compliance commitments, sharing security architecture details

## Integration Points

- **Upstream**: Customer questions directly, or risk flags from `sales-rfp-interpreter`
- **Downstream**: Answers feed into `sales-proposal-architect` for proposal security sections
- **KB Dependency**: Requires `knowledge-bases/security-sovereignty/` topic (bootstrap via `kb-orchestrator`)
- **Harness**: Invoked as Phase 2 of `sales-agent-harness` in `rfp-flow` mode
