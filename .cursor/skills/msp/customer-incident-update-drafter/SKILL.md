---
name: msp-customer-incident-update-drafter
description: >-
  MSP customer communication drafter: ingest internal incident data (from
  Skill #1 triage report or manual input), classify update type (initial,
  progress, resolution, post-incident), separate customer-safe from internal-only
  details, generate professional empathetic drafts in 3 formats (markdown, HTML,
  plain text) with tone scoring, and optionally route to an approval gate for
  sending — composing kwp-customer-support-response-drafting for empathy
  patterns and sentence-polisher for grammar. Draft generation is Tier 1 (auto);
  sending is Tier 2 (requires explicit human approval per message). Automatic
  sending is Tier 3 PROHIBITED. Use when the user asks to draft customer
  incident update, write customer notification, incident communication draft,
  customer update for incident, or needs professional incident communications
  for MSP customers. Do NOT use for internal incident triage without customer
  communication (use msp-incident-triage-summarizer), full incident lifecycle
  management (use incident-lifecycle-manager), general marketing or sales
  communications (use kwp-marketing-content-creation), sending emails without
  incident context (use gws-email-reply), or automated customer notifications
  without approval (PROHIBITED). Korean triggers: 고객 인시던트 업데이트,
  장애 알림 초안, 고객 커뮤니케이션, 인시던트 통보문.
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "msp/communication"
  approval_tier: "tier-1-draft, tier-2-send"
  approval_spec: "docs/msp-skills/APPROVAL_BOUNDARY_SPEC.md"
  mutations:
    - "email_sent (only if mode=send AND approved by human)"
  clouds:
    - "aws"
    - "gcp"
  composes:
    - "kwp-customer-support-response-drafting"
    - "sentence-polisher"
    - "msp-incident-triage-summarizer"
    - "msp-root-cause-hypothesis-builder"
---

# Customer Incident Update Drafter

## Usage

- An MSP-managed customer needs to be notified of an ongoing incident
- Progress updates are due during an active incident
- An incident has been resolved and the customer needs closure communication
- A post-incident summary report needs to be drafted for the customer
- `/msp-customer-update` with incident context

## Prerequisites

- Incident context (Skill #1 triage report, manual description, or incident ID)
- `tenant_id` and `customer_name` for proper scoping
- `update_type` specification (initial / progress / resolution / post-incident)

## Critical Rules

1. **Auto-send is PROHIBITED (Tier 3)** — every customer message requires fresh human review
2. **No internal details in customer comms** — infrastructure IPs, account IDs, internal hostnames, team names must be redacted
3. **No cross-tenant contamination** — strict tenant_id scoping; prompt isolation per tenant
4. **Speculative root causes require human confirmation** — label as "preliminary" and flag for review
5. **Thread continuity** — reference previous updates when available

## Workflow

### Step 1 — Context Ingestion

```
Read incident_context:
  - Primary: Skill #1 msp-incident-triage-summarizer output (JSON)
  - Secondary: Manual incident description
If update_type is resolution/post-incident:
  Read Skill #2 msp-root-cause-hypothesis-builder output
Load previous_updates for thread continuity (if any)
Validate tenant_id matches customer_name scope
```

### Step 2 — Content Classification

```
Separate all information into two buckets:

CUSTOMER-SAFE:
  - Service impact description (in customer terms)
  - Current status (investigating/identified/monitoring/resolved)
  - Timeline of customer-visible events
  - Actions being taken (at high level)
  - ETA estimates (if available)
  - Confirmed root cause (only if human-approved)

INTERNAL-ONLY (redacted from customer comm):
  - Infrastructure details (IPs, hostnames, instance IDs)
  - Cloud account/project identifiers
  - Internal team names and escalation paths
  - Speculative root causes not yet confirmed
  - Detailed technical diagnostics
  - Cost impact data

Flag items requiring human judgment to classify
```

### Step 3 — Draft Generation

```
Select template based on update_type:
  initial    → "Service Disruption Detected" template
  progress   → "Investigation in Progress" template
  resolution → "Service Restored" template
  post-incident → "Post-Incident Summary" template

Populate template with CUSTOMER-SAFE content only
Apply kwp-customer-support-response-drafting patterns:
  - Empathetic opening acknowledging impact
  - Clear status and next steps
  - Professional closing with contact information

Adjust detail level for audience:
  technical  → Include more specific technical context
  executive  → Focus on business impact and timeline
  general    → Balance clarity with appropriate detail

Generate three format variants:
  - body_markdown (for Slack/internal review)
  - body_html (for email)
  - body_plain (for SMS/basic channels)
```

### Step 4 — Quality Assurance

```
Run sentence-polisher for grammar and flow
Score draft on 4 dimensions (0.0–1.0):
  empathy              — acknowledges customer impact, avoids blame
  clarity              — status and next steps are unambiguous
  professionalism      — appropriate tone, no casual language
  technical_accuracy   — facts match incident context, no fabrication

Verify ZERO internal-only details leaked into customer draft:
  Pattern scan for: IP addresses, AWS account IDs, GCP project IDs,
  internal hostnames, team Slack channels, employee names

Check thread continuity with previous_updates:
  Consistent incident reference, no contradictions with prior comms
```

### Step 5 — Internal Notes Assembly

```
Compile internal_notes:
  redacted_details    — list of details excluded with reason
  escalation_flags    — items needing human judgment
  suggested_follow_up — recommended next update timing and content
```

### Step 6 — Output or Approval Gate

```
If mode = draft-only (default, Tier 1):
  Return complete draft package with send_status = "draft"
  Include internal_notes for reviewer context

If mode = send (Tier 2):
  Present to approver:
    - Full draft text
    - Redacted details list
    - Escalation flags
    - Tone scores
    - Send channel specification
  
  Approval gate:
    TTL: 2 hours (customer comms are time-sensitive)
    On approval: Send via specified channel, log attributed audit entry
    On rejection: Return draft with rejection_reason, allow re-edit
    On timeout: Save draft, alert approver of expired comm
    
  Escalation: Alert at 75% TTL (90 minutes)
```

## Output Schema

```json
{
  "schema_version": "1.0.0",
  "skill": "customer-incident-update-drafter",
  "update_type": "initial|progress|resolution|post-incident",
  "draft": {
    "subject": "",
    "body_markdown": "",
    "body_html": "",
    "body_plain": "",
    "tone_score": {"empathy": 0.0, "clarity": 0.0, "professionalism": 0.0, "technical_accuracy": 0.0}
  },
  "internal_notes": {
    "redacted_details": [],
    "escalation_flags": [],
    "suggested_follow_up": ""
  },
  "send_status": "draft|pending_approval|approved|sent|rejected",
  "approval": {"required": true, "approver": null, "approved_at": null},
  "audit_entry": {"skill_version": "1.0.0", "tier": "1 or 2", "mutations": []}
}
```

## Governance

| Mode | Tier | Actions |
|------|------|---------|
| `draft-only` | Tier 1 | Generate draft — no external communication |
| `send` | Tier 2 | Send with mandatory per-message human approval |
| Automatic send | Tier 3 | **PROHIBITED** — even with standing approval |

## Error Handling

| Error | Recovery |
|-------|----------|
| Missing incident_context | Return error; require at minimum a service impact description |
| Skill #1 output not found | Fall back to manual incident description; note reduced context |
| Internal detail detected in draft | Block draft generation; report specific leak for correction |
| Approval timeout (2h) | Save draft; alert incident commander; do not auto-send |
| Customer name mismatch with tenant | Block operation; report scope violation |

## Subagent Contract

When invoked via `Task`:
- Caller provides: `incident_context`, `tenant_id`, `customer_name`, `update_type`, `affected_services`, `current_status`
- Optional: `mode`, `send_channel`, `audience`, `previous_updates`, `root_cause_summary`
- Returns: Full JSON output with draft and approval status
