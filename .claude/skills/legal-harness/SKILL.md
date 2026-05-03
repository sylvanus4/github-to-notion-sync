---
name: legal-harness
description: >-
  Legal domain harness orchestrator — Pipeline + Producer-Reviewer pattern
  with dual-verification for contract review, NDA triage, risk assessment,
  compliance, and patent delegation. Human-in-the-loop gate for RED-classified
  items. Use when the user asks to "run legal pipeline", "legal harness",
  "contract review pipeline", "법률 하네스", "법무 파이프라인", "legal-harness", or wants
  end-to-end legal operations. Do NOT use for individual legal operations
  (invoke kwp-legal-* directly). Do NOT use for patent-only work (use
  patent-orchestrator directly).
---

# Legal Harness Orchestrator

Pipeline + Producer-Reviewer pattern with mandatory dual-verification for high-risk items. Every document passes through both generation and independent review before finalization.

## When to Use

- Processing incoming NDAs through the GREEN/YELLOW/RED classification pipeline
- Full contract review with clause-by-clause analysis and risk assessment
- Compliance review for GDPR, CCPA, or DPA requirements
- Preparing legal briefings for negotiation meetings
- Any "handle this legal matter end-to-end" request

## Architecture

```
Legal Request (mode selection)
       │
       ▼
┌──────────────┐
│ Phase 1      │ ← NDA Triage: GREEN/YELLOW/RED classification
│ NDA TRIAGE   │   kwp-legal-nda-triage
└──────┬───────┘
       │
       ├─── GREEN ──→ Auto-approve with standard terms
       ├─── YELLOW ──→ Continue to Phase 2
       ├─── RED ────→ HUMAN GATE: Senior counsel must review
       │
       ▼
┌──────────────┐
│ Phase 2      │ ← Contract Review: clause-by-clause analysis
│ REVIEW       │   kwp-legal-contract-review  [PRODUCER]
└──────┬───────┘
       ▼
┌──────────────┐
│ Phase 2b     │ ← Independent re-review of flagged clauses
│ VERIFY       │   kwp-legal-contract-review  [REVIEWER]
└──────┬───────┘
       ▼
┌──────────────┐
│ Phase 3      │ ← Risk Assessment: severity × likelihood matrix
│ RISK         │   kwp-legal-legal-risk-assessment
└──────┬───────┘
       ▼
┌──────────────┐
│ Phase 4      │ ← Compliance: GDPR/CCPA/DPA review
│ COMPLIANCE   │   kwp-legal-compliance
└──────┬───────┘
       ▼
┌──────────────┐
│ Phase 5      │ ← Meeting Briefing: negotiation prep
│ BRIEFING     │   kwp-legal-meeting-briefing
└──────┬───────┘
       ▼
┌──────────────┐
│ Phase 6      │ ← Canned Responses: template for routine queries
│ RESPONSES    │   kwp-legal-canned-responses
└──────────────┘
```

## Producer-Reviewer Pattern

Phases 2 and 2b implement the Producer-Reviewer pattern:

1. **Producer (Phase 2)**: First-pass contract review — clause analysis, deviation detection, redline suggestions
2. **Reviewer (Phase 2b)**: Independent re-review focusing on:
   - Clauses flagged as YELLOW or RED by the Producer
   - Consistency of risk classifications
   - Completeness of redline suggestions
   - Any clauses the Producer may have missed

If Reviewer disagrees with Producer on risk classification, the higher risk level takes precedence.

## Modes

| Mode | Phases | Use Case |
|------|--------|----------|
| `nda` | 1 only | Quick NDA GREEN/YELLOW/RED triage |
| `contract` | 1→2→2b→3 | Full contract review with dual verification |
| `compliance` | 4 only | GDPR/CCPA/DPA review |
| `meeting` | 5 only | Legal meeting preparation and briefing |
| `patent` | Delegates to `patent-orchestrator` | Patent-related workflows |
| `full` | 1→2→2b→3→4→5→6 | Complete legal pipeline |

Default mode: `contract`

## Pipeline

### Phase 1: NDA Triage

Screen incoming NDAs and classify by risk level.

**Skill**: `kwp-legal-nda-triage`
**Input**: NDA document
**Output**: `outputs/legal-harness/{date}/phase1-nda-triage.md`

| Classification | Action |
|---------------|--------|
| **GREEN** | Standard terms — auto-approve with template response |
| **YELLOW** | Needs review — continue to Phase 2 |
| **RED** | Significant issues — **HUMAN GATE**: pause pipeline, alert senior counsel |

### Phase 2: Contract Review (Producer)

Review contract against negotiation playbook, flagging deviations.

**Skill**: `kwp-legal-contract-review`
**Input**: Contract document + Phase 1 triage (if NDA)
**Output**: `outputs/legal-harness/{date}/phase2-contract-review.md`

Covers: clause-by-clause analysis, standard position deviations, redline suggestions.

### Phase 2b: Contract Verification (Reviewer)

Independent re-review of the Producer's findings.

**Skill**: `kwp-legal-contract-review` (run as independent reviewer)
**Input**: Phase 2 output + original contract
**Output**: `outputs/legal-harness/{date}/phase2b-verification.md`

Focus: validate risk classifications, check completeness, identify missed clauses.

### Phase 3: Risk Assessment

Assess and classify legal risks using severity × likelihood framework.

**Skill**: `kwp-legal-legal-risk-assessment`
**Input**: Phase 2 + 2b outputs (merged findings)
**Output**: `outputs/legal-harness/{date}/phase3-risk-assessment.md`

Covers: contract risk, deal exposure, issue classification, escalation criteria.

### Phase 4: Compliance Review

Navigate privacy regulations and review data processing requirements.

**Skill**: `kwp-legal-compliance`
**Input**: Contract/agreement + applicable jurisdictions
**Output**: `outputs/legal-harness/{date}/phase4-compliance.md`

Covers: GDPR, CCPA, DPA review, cross-border data transfer, data subject rights.

### Phase 5: Meeting Briefing

Prepare structured briefing for legal meetings and negotiations.

**Skill**: `kwp-legal-meeting-briefing`
**Input**: Phase 2-4 outputs (full legal context)
**Output**: `outputs/legal-harness/{date}/phase5-briefing.md`

Covers: background research, key negotiation points, action item tracking.

### Phase 6: Canned Responses

Generate templated responses for routine legal inquiries.

**Skill**: `kwp-legal-canned-responses`
**Input**: Common inquiry patterns from pipeline history
**Output**: `outputs/legal-harness/{date}/phase6-responses.md`

## Error Handling

| Error | Recovery |
|-------|----------|
| RED NDA detected | Pipeline pauses at Phase 1. Human gate activated. Resume only after senior counsel approval. |
| Producer-Reviewer disagreement | Higher risk classification prevails. Document disagreement in Phase 3 risk report. |
| Missing jurisdiction data for compliance | Flag as incomplete, list required jurisdictions, pause Phase 4 pending input. |
| Phase N fails | Prior phase outputs remain valid. Fix and re-run from Phase N. |

## Output Artifacts

| Phase | Stage Name | Output File | Skip Flag |
|-------|-----------|-------------|-----------|
| 1 | NDA Triage | `outputs/legal-harness/{date}/phase1-nda-triage.md` | `skip-nda` |
| 2 | Contract Review | `outputs/legal-harness/{date}/phase2-contract-review.md` | `skip-review` |
| 2b | Verification | `outputs/legal-harness/{date}/phase2b-verification.md` | `skip-verify` |
| 3 | Risk Assessment | `outputs/legal-harness/{date}/phase3-risk-assessment.md` | `skip-risk` |
| 4 | Compliance | `outputs/legal-harness/{date}/phase4-compliance.md` | `skip-compliance` |
| 5 | Briefing | `outputs/legal-harness/{date}/phase5-briefing.md` | `skip-briefing` |
| 6 | Responses | `outputs/legal-harness/{date}/phase6-responses.md` | `skip-responses` |

## Workspace Convention

- Intermediate files: `_workspace/legal-harness/`
- Final deliverables: `outputs/legal-harness/{date}/`
- Audit log: `outputs/legal-harness/{date}/audit-log.jsonl`

## Constraints

- **Human-in-the-loop**: RED-classified items MUST be reviewed by senior counsel before proceeding
- **Audit trail**: Every phase records input source, timestamp, and reviewer identity in `audit-log.jsonl`
- **Confidentiality**: Contract content must not be logged to Slack or external channels
- **Producer-Reviewer independence**: Phase 2b reviewer must not see Producer's risk classifications until after completing independent review
- **Patent delegation**: Patent-related requests bypass this pipeline and delegate to `patent-orchestrator`
