---
name: lead-research-agent
version: 1.0.0
description: >
  Autonomous lead research agent that takes an ICP description or target account list,
  discovers prospects via Apollo and Common Room enrichment, runs deep web research on
  each lead, scores fit against ICP criteria, generates personalized outreach drafts,
  and delivers a prioritized lead package with contact details, company intel, and
  ready-to-send emails. Use when the user asks to "research leads", "find prospects",
  "lead research", "lead-research-agent", "autonomous lead gen", "ICP to leads",
  "prospect research and outreach", "리드 리서치", "잠재 고객 조사", "리드 리서치 에이전트",
  "ICP 기반 리드 발굴", "아웃리치 초안 생성", "자동 잠재 고객 발굴", or wants an end-to-end
  pipeline from ICP definition to outreach-ready lead packages. Do NOT use for enriching
  a single known contact (use kwp-apollo-enrich-lead). Do NOT use for competitive
  intelligence without lead gen (use kwp-sales-competitive-intelligence). Do NOT use for
  composing Slack messages (use kwp-slack-slack-messaging). Do NOT use for CRM pipeline
  management (use deal-stage-guardian).
tags: [leads, research, prospecting, outreach, Apollo, enrichment, monetizable]
triggers:
  - "lead research"
  - "lead research agent"
  - "lead-research-agent"
  - "find prospects"
  - "autonomous lead gen"
  - "ICP to leads"
  - "prospect research and outreach"
  - "prospect pipeline"
  - "리드 리서치"
  - "잠재 고객 조사"
  - "리드 리서치 에이전트"
  - "ICP 기반 리드 발굴"
  - "아웃리치 초안 생성"
  - "자동 잠재 고객 발굴"
do_not_use:
  - "For enriching a single known contact (use kwp-apollo-enrich-lead)"
  - "For drafting outreach to a known person without research (use kwp-sales-draft-outreach)"
  - "For competitive intelligence without lead gen intent (use kwp-sales-competitive-intelligence)"
  - "For CRM deal pipeline management (use deal-stage-guardian)"
  - "For call preparation for known prospects (use kwp-sales-call-prep)"
composes:
  - kwp-apollo-prospect
  - kwp-apollo-enrich-lead
  - kwp-common-room-prospect
  - kwp-common-room-contact-research
  - kwp-common-room-account-research
  - kwp-sales-account-research
  - kwp-sales-draft-outreach
  - evaluation-engine
  - batch-agent-runner
  - sentence-polisher
  - visual-explainer
  - anthropic-docx
metadata:
  author: "thaki"
  category: "monetizable"
  mrr_target: "$2K-$5K"
---

# Lead Research Agent

Discover, research, score, and draft outreach for qualified leads — from ICP to inbox-ready emails.

## When to Use

- Sales team has an ICP description and needs a pipeline of qualified leads with contact info
- Outbound campaign needs enriched prospects with personalized first-touch emails
- Account-based marketing requires deep research on target company lists
- Founder-led sales needs efficient prospect research without manual LinkedIn browsing

## Output Artifacts

| Phase | Stage Name         | Output File                                               |
| ----- | ------------------ | --------------------------------------------------------- |
| 1     | ICP Definition     | `outputs/lead-research-agent/{date}/icp-profile.md`       |
| 2     | Discovery          | `outputs/lead-research-agent/{date}/raw-leads.jsonl`      |
| 3     | Enrichment         | `outputs/lead-research-agent/{date}/enriched-leads.jsonl`  |
| 4     | Scoring            | `outputs/lead-research-agent/{date}/scored-leads.tsv`      |
| 5     | Outreach           | `outputs/lead-research-agent/{date}/outreach-drafts.md`    |
| 6     | Package            | `outputs/lead-research-agent/{date}/lead-package.docx`     |
| 6     | Dashboard          | `outputs/lead-research-agent/{date}/dashboard.html`        |
| 6     | Manifest           | `outputs/lead-research-agent/{date}/manifest.json`         |

## Workflow

### Phase 1: ICP Definition

Accept ICP input in any form:
- **Natural language**: "Series A B2B SaaS companies, 50-200 employees, in fintech"
- **Structured criteria**: Industry, headcount, funding stage, geography, tech stack
- **Existing ICP document**: Read from file or Notion page

Formalize into an ICP profile with weighted criteria:

| Criterion | Weight | Example |
|-----------|--------|---------|
| Industry | 0.25 | Fintech, SaaS, AI |
| Company size | 0.20 | 50-200 employees |
| Funding stage | 0.15 | Series A-B |
| Geography | 0.10 | US, UK, EU |
| Tech stack signals | 0.15 | Uses Kubernetes, Python, React |
| Intent signals | 0.15 | Hiring for X role, recent funding announcement |

Save to `icp-profile.md`.

### Phase 2: Discover

Run prospect discovery in parallel where MCPs are available:

| Source | Method | Data Returned |
|--------|--------|---------------|
| Apollo | `kwp-apollo-prospect` with ICP criteria | Company + contact list |
| Common Room | `kwp-common-room-prospect` for community signals | Active accounts, signal events |
| Web search | `kwp-sales-account-research` for target companies | Company intel, news, job postings |

Merge and deduplicate results by company domain. Save to `raw-leads.jsonl` with schema:

```json
{
  "company": { "name": "", "domain": "", "industry": "", "size": "", "funding": "" },
  "contacts": [{ "name": "", "title": "", "email": "", "linkedin": "" }],
  "source": "apollo|common-room|web",
  "discovery_date": "ISO-8601"
}
```

### Phase 3: Enrich

For each lead (top 20 by initial relevance), run enrichment in parallel via `batch-agent-runner`:

| Source | Method | Data Added |
|--------|--------|------------|
| Apollo enrichment | `kwp-apollo-enrich-lead` per contact | Email, phone, title, company intel |
| Common Room signals | `kwp-common-room-contact-research` | Activity signals, community engagement |
| Common Room account | `kwp-common-room-account-research` | Account-level signals, intent data |
| Web research | `kwp-sales-account-research` | Recent news, job postings, tech stack |

Merge enrichment data into each lead record. Save to `enriched-leads.jsonl`.

### Phase 4: Score

Score each enriched lead against ICP criteria using `evaluation-engine` with custom rubric:

| Dimension | Scale | What It Measures |
|-----------|-------|------------------|
| ICP fit | 1-10 | How closely the company matches ICP criteria (weighted) |
| Contact quality | 1-10 | Decision-maker title match, email availability, LinkedIn presence |
| Intent signals | 1-10 | Job postings, funding news, tech stack changes, community activity |
| Reachability | 1-10 | Email verified, phone available, LinkedIn active |
| Timing | 1-10 | Recency of intent signals, funding announcement proximity |

Composite score = weighted average. Assign grade: A (8+), B (6-7.9), C (4-5.9), D (<4).

Rank by composite score descending. Save to `scored-leads.tsv` with columns: rank, company, contact_name, title, email, icp_fit, contact_quality, intent, reachability, timing, composite, grade.

### Phase 5: Outreach Drafts

For the top 10 leads (grade A and B), generate personalized outreach using `kwp-sales-draft-outreach` patterns:

| Element | Description |
|---------|-------------|
| Subject line | 2-3 options, personalized with company/role reference |
| Opening hook | Specific reference to company news, funding, or tech stack |
| Value prop | Mapped to prospect's likely pain points based on ICP segment |
| Social proof | Relevant case study or metric |
| CTA | Low-friction next step (not "book a demo") |

Each draft includes:
- Email version (150-200 words)
- LinkedIn InMail version (300 chars)
- Follow-up sequence outline (3-touch: email → LinkedIn → email)

Save all drafts to `outreach-drafts.md`.

### Phase 6: Package & Deliver

1. Generate `lead-package.docx` via `anthropic-docx`:
   - Executive summary: ICP profile, total leads found, quality distribution
   - Top 10 lead profiles: company overview, key contacts, scoring rationale
   - Outreach drafts: ready-to-send emails with personalization notes
   - Full lead list: all discovered leads with scores

2. Generate `dashboard.html` via `visual-explainer`:
   - Lead funnel visualization (discovered → enriched → qualified → outreach-ready)
   - Score distribution chart
   - ICP fit heatmap
   - Source breakdown (Apollo vs Common Room vs web)

3. Write `manifest.json` with:
   - ICP criteria used
   - Total leads discovered, enriched, qualified
   - Score distribution
   - File paths and timestamps

4. Optionally push top leads summary to Notion via `md-to-notion`

## Examples

### Example 1: ICP-to-outreach pipeline

User says: "Find 20 leads matching our ICP: Series A-B SaaS companies in Southeast Asia with 50-200 employees"

Actions:
1. Define ICP criteria and generate search queries
2. Discover prospects via Apollo/Common Room/web search
3. Enrich with company intel, tech stack, funding data
4. Score and rank leads by fit (0-100)
5. Generate personalized outreach drafts for top 10

Result: Ranked lead list .xlsx, 10 outreach drafts, Notion pipeline entries

### Example 2: Single-company deep dive

User says: "Deep research Acme Corp as a potential lead"

Actions:
1. Gather company overview, recent news, leadership team
2. Assess technology needs and potential pain points
3. Map to our product value propositions
4. Draft personalized email and LinkedIn message

Result: Company research brief, 2 outreach variants, Slack summary

## Error Handling

If enrichment fails for a specific lead, the remaining leads continue. Failed enrichments are logged in `manifest.json` with `status: "enrichment_failed"`. Scoring (Phase 4) uses available data and notes missing enrichment dimensions. Outreach drafts skip leads without verified email addresses.

## Gotchas

- Apollo API rate limits apply; batch discovery into groups of 25 contacts
- Common Room requires MCP access; gracefully skip if unavailable and note reduced signal quality
- Email verification status should be checked before including in outreach; unverified emails are flagged
- Never fabricate contact details; if email is not found, mark as "email_not_found" rather than guessing
- LinkedIn InMail versions must stay under 300 chars including spaces
- Outreach personalization requires at least 1 specific company detail; generic "I noticed your company" is not acceptable
