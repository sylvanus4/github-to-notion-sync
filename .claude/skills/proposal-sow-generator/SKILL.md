---
name: proposal-sow-generator
description: >-
  Meeting-to-proposal pipeline that ingests meeting transcripts or notes,
  extracts client requirements and project scope, generates a professional
  proposal and Statement of Work (SOW) as .docx with pricing tables,
  timelines, deliverables, and terms. Composes meeting-digest for transcript
  analysis and anthropic-docx for document generation. Use when the user asks
  to "generate proposal from meeting", "create SOW", "proposal-sow-generator",
  "meeting to proposal", "write proposal", "generate statement of work", "제안서
  생성", "SOW 작성", "회의록에서 제안서", "미팅 기반 제안서", "작업 명세서", "프로포절 생성", or wants to
  convert meeting context into a professional proposal and SOW document
  package. Do NOT use for meeting summary without proposal intent (use
  meeting-digest). Do NOT use for NDA drafting (use pm-toolkit). Do NOT use
  for pricing strategy design (use marketing-sales-playbook). Do NOT use for
  contract review (use kwp-legal-contract-review).
---

# Proposal/SOW Generator

Transform meeting notes into professional proposals and Statements of Work with pricing, timelines, and deliverables.

## When to Use

- A client meeting just ended and a proposal or SOW needs to be sent within 24-48 hours
- Sales team needs to convert discovery call notes into a structured proposal
- Consulting engagement requires a formal SOW with deliverables and payment milestones
- Freelancers need to quickly generate professional proposals from informal meeting notes

## Output Artifacts

| Phase | Stage Name         | Output File                                                   |
| ----- | ------------------ | ------------------------------------------------------------- |
| 1     | Ingest             | `outputs/proposal-sow-generator/{date}/meeting-extract.md`    |
| 2     | Scope              | `outputs/proposal-sow-generator/{date}/scope-definition.md`   |
| 3     | Proposal           | `outputs/proposal-sow-generator/{date}/proposal.docx`         |
| 4     | SOW                | `outputs/proposal-sow-generator/{date}/sow.docx`              |
| 5     | Manifest           | `outputs/proposal-sow-generator/{date}/manifest.json`         |

## Workflow

### Phase 1: Ingest Meeting Content

Accept meeting input in any form:
- **Transcript file**: Read `.txt`, `.md`, `.docx` directly
- **Notion meeting page**: Fetch via Notion MCP
- **Pasted text**: Accept inline notes or transcript
- **Meeting recording URL**: Extract via `defuddle`
- **Structured brief**: Accept user-provided scope brief directly (skip to Phase 2)

Delegate transcript analysis to `meeting-digest` Phase 1-2 to extract:

| Element | Description |
|---------|-------------|
| Client name & contacts | Company name, attendees with titles |
| Problem statement | What the client needs solved |
| Requirements | Explicit asks and implicit needs |
| Constraints | Budget range, timeline, technical limitations |
| Success criteria | How the client will measure success |
| Competitive context | Competing vendors or internal alternatives mentioned |
| Urgency indicators | Timeline pressure, contractual deadlines |
| Decision process | Who approves, what steps remain |

Save to `meeting-extract.md`.

### Phase 2: Scope Definition

Structure extracted requirements into a formal project scope:

**Project Overview:**

| Field | Description |
|-------|-------------|
| Project name | Clear, client-facing project title |
| Objective | 1-2 sentence statement of what will be achieved |
| Background | Client context and why this project matters |

**Deliverables Table:**

| # | Deliverable | Description | Acceptance Criteria | Priority |
|---|-------------|-------------|---------------------|----------|
| 1 | | | | Must-have / Nice-to-have |

**Phase Breakdown:**

| Phase | Duration | Deliverables | Dependencies |
|-------|----------|-------------|--------------|
| Discovery | | | |
| Design | | | |
| Development | | | |
| Testing | | | |
| Launch | | | |

**Assumptions & Exclusions:**
- What is assumed to be provided by the client
- What is explicitly excluded from scope

Save to `scope-definition.md`. Present to user for review before proceeding.

### Phase 3: Generate Proposal

Generate professional proposal via `anthropic-docx`:

| Section | Content |
|---------|---------|
| Cover page | Project name, client name, date, version |
| Executive summary | Problem + solution + value proposition (1 page via `long-form-compressor`) |
| Understanding | Restated client needs showing comprehension |
| Proposed solution | Approach, methodology, technology choices |
| Deliverables | Detailed deliverables table from Phase 2 |
| Timeline | Gantt-style phase table with milestones |
| Team | Key personnel with relevant experience |
| Investment | Pricing table with options (if applicable) |
| Why us | Differentiators, relevant case studies |
| Next steps | Clear call to action with timeline |
| Terms | Payment schedule, validity period |

**Pricing Options (if budget range available):**

| Package | Scope | Price | Timeline |
|---------|-------|-------|----------|
| Essential | Core deliverables | $ | X weeks |
| Professional | Core + enhancements | $ | X weeks |
| Enterprise | Full scope + support | $ | X weeks |

If no pricing information is available, insert "[PRICING TO BE CONFIRMED]" placeholders.

Polish Korean text via `sentence-polisher`.

Save to `proposal.docx`.

### Phase 4: Generate SOW

Generate Statement of Work via `anthropic-docx`:

| Section | Content |
|---------|---------|
| 1. Purpose | Project objective and scope reference |
| 2. Scope of Work | Detailed work description per phase |
| 3. Deliverables | Complete deliverables table with acceptance criteria |
| 4. Timeline & Milestones | Phase schedule with start/end dates |
| 5. Roles & Responsibilities | Client vs. provider responsibilities matrix |
| 6. Assumptions | Technical, resource, and access assumptions |
| 7. Out of Scope | Explicit exclusions |
| 8. Change Management | Process for scope changes and approvals |
| 9. Acceptance Process | How deliverables are reviewed and accepted |
| 10. Payment Terms | Milestone-based payment schedule |
| 11. Term & Termination | Contract duration, termination clauses |

**Roles & Responsibilities Matrix:**

| Responsibility | Client | Provider |
|---------------|--------|----------|
| Provide access to systems | R | S |
| Design review and approval | A | R |
| Development and testing | I | R |
| User acceptance testing | R | S |
| Production deployment | C | R |

(R = Responsible, A = Approver, S = Support, I = Informed, C = Consulted)

Save to `sow.docx`.

### Phase 5: Deliver

1. Write `manifest.json` with:
   - Client name and project title
   - Meeting date and source type
   - Deliverables count and phases
   - Pricing status (confirmed / placeholder)
   - File paths and timestamps

2. Upload to Google Drive via `gws-drive` (if accessible):
   - Create folder: `{Client Name} - {Project Name}`
   - Upload proposal.docx and sow.docx

3. Push scope summary to Notion via `md-to-notion`

4. Post notification to Slack (if available):
   - "Proposal and SOW generated for {Client Name} - {Project Name}"
   - Thread: file locations and next steps

## Customization

Users can provide:
- **Company branding**: Logo path and brand colors for document formatting
- **Template override**: Existing proposal/SOW template to follow
- **Pricing model**: Hourly, fixed-price, retainer, or milestone-based
- **Industry-specific terms**: Compliance clauses, SLAs, insurance requirements

## Examples

### Example 1: Meeting-to-proposal pipeline

User says: "Generate a proposal from yesterday's client meeting about their data platform migration"

Actions:
1. Retrieve meeting transcript, extract requirements and scope via meeting-digest
2. Research client's industry and competitors
3. Generate proposal sections: executive summary, scope, deliverables, timeline, pricing
4. Produce SOW appendix with milestones and acceptance criteria
5. Apply brand template and export as .docx

Result: Branded proposal .docx, SOW appendix, Notion page, Slack notification

### Example 2: Korean proposal from raw notes

User says: "이 미팅 메모로 제안서 만들어줘"

Actions:
1. Parse Korean meeting notes, extract scope items
2. Generate Korean proposal with proper business honorifics
3. Include pricing table and timeline in Korean format

Result: Korean proposal .docx, SOW in Korean, Slack summary

## Error Handling

If meeting transcript quality is poor (no clear requirements), Phase 2 produces a scope definition with "[CLARIFICATION NEEDED]" markers. The user reviews and fills gaps before Phase 3-4 generate documents. Documents are not generated with fabricated requirements.

## Gotchas

- Never fabricate pricing; if no budget was discussed, use placeholder markers
- Client names and contact details from transcripts may be approximate; flag for user verification
- SOW Section 11 (Term & Termination) should include standard cancellation terms but should note "subject to legal review"
- Change management section is critical; scope creep without it costs both sides
- Payment milestones should align with deliverable acceptance, not calendar dates
- Multi-currency engagements need explicit currency specification in pricing tables
