---
name: client-onboarding-automator
version: 1.0.0
description: >
  End-to-end client onboarding pipeline that generates welcome kits, checklists,
  templated documents, shared Drive folders, Notion project pages, scheduled kick-off
  meetings, and onboarding email sequences from a new client intake form or signed
  contract. Orchestrates Google Workspace, Notion, and Slack integrations to ensure
  nothing falls through the cracks. Use when the user asks to "onboard a new client",
  "client onboarding", "client-onboarding-automator", "new client setup", "welcome
  kit", "onboarding checklist", "신규 고객 온보딩", "클라이언트 온보딩", "고객 온보딩
  자동화", "웰컴 킷 생성", "온보딩 체크리스트", or wants to automate the full new-client
  onboarding workflow. Do NOT use for internal employee onboarding (use
  onboarding-accelerator). Do NOT use for meeting scheduling without onboarding context
  (use smart-meeting-scheduler). Do NOT use for Notion page creation without onboarding
  workflow (use md-to-notion). Do NOT use for email drafting without onboarding sequence
  (use gws-email-reply).
tags: [onboarding, client, automation, checklist, welcome-kit, monetizable]
triggers:
  - "onboard new client"
  - "client onboarding"
  - "client-onboarding-automator"
  - "new client setup"
  - "welcome kit"
  - "onboarding checklist"
  - "client setup automation"
  - "onboarding sequence"
  - "신규 고객 온보딩"
  - "클라이언트 온보딩"
  - "고객 온보딩 자동화"
  - "웰컴 킷 생성"
  - "온보딩 체크리스트"
  - "고객 셋업"
do_not_use:
  - "For internal developer/employee onboarding (use onboarding-accelerator)"
  - "For meeting scheduling without onboarding context (use smart-meeting-scheduler)"
  - "For standalone Notion page creation (use md-to-notion)"
  - "For single email drafting (use gws-email-reply)"
  - "For CRM deal stage management (use deal-stage-guardian)"
composes:
  - anthropic-docx
  - gws-drive
  - gws-gmail
  - gws-calendar
  - gws-docs
  - md-to-notion
  - sentence-polisher
  - long-form-compressor
metadata:
  author: "thaki"
  category: "monetizable"
  mrr_target: "$2K-$5K"
---

# Client Onboarding Automator

Automate new client onboarding from intake to kick-off: checklists, welcome docs, Drive folders, Notion pages, calendar events, and email sequences.

## When to Use

- A new client contract is signed and the onboarding process needs to start
- Agencies or service businesses need a repeatable, nothing-falls-through-the-cracks onboarding
- Teams want to reduce manual setup time for each new engagement
- Management wants visibility into onboarding status across clients

## Output Artifacts

| Phase | Stage Name         | Output File                                                         |
| ----- | ------------------ | ------------------------------------------------------------------- |
| 1     | Intake             | `outputs/client-onboarding-automator/{date}/client-profile.md`      |
| 2     | Checklist          | `outputs/client-onboarding-automator/{date}/onboarding-checklist.md` |
| 3     | Documents          | `outputs/client-onboarding-automator/{date}/welcome-kit.docx`       |
| 4     | Workspace          | `outputs/client-onboarding-automator/{date}/workspace-setup.md`     |
| 5     | Communications     | `outputs/client-onboarding-automator/{date}/email-sequence.md`      |
| 6     | Manifest           | `outputs/client-onboarding-automator/{date}/manifest.json`          |

## Workflow

### Phase 1: Client Intake

Accept client information in any form:
- **Structured intake form**: JSON or markdown with predefined fields
- **Contract/SOW document**: Extract key details from `.docx` or `.pdf`
- **Pasted notes**: Informal notes from a sales handoff
- **Notion CRM entry**: Fetch client data from Notion database

Extract and formalize:

| Field | Description | Required |
|-------|-------------|----------|
| Client name | Legal entity name | Yes |
| Primary contact | Name, email, phone | Yes |
| Secondary contact | Name, email, phone | No |
| Project name | Engagement title | Yes |
| Start date | Engagement kick-off date | Yes |
| Contract value | Total contract value | No |
| Billing cadence | Monthly / Milestone / Prepaid | No |
| Service tier | Package or plan purchased | Yes |
| Key deliverables | What was promised | Yes |
| Access requirements | Systems, credentials, tools needed from client | No |
| Special instructions | Any non-standard requirements | No |

Save to `client-profile.md`. Present to user for confirmation before proceeding.

### Phase 2: Generate Onboarding Checklist

Create a phased checklist tailored to the service tier:

**Pre-Kickoff (Days -3 to 0):**

| # | Task | Owner | Due |
|---|------|-------|-----|
| 1 | Create shared Drive folder | Provider | Day -3 |
| 2 | Set up Notion project page | Provider | Day -3 |
| 3 | Send welcome email with access links | Provider | Day -2 |
| 4 | Collect client access credentials | Client | Day -1 |
| 5 | Schedule kick-off meeting | Provider | Day -2 |
| 6 | Prepare kick-off agenda | Provider | Day -1 |

**Kick-off (Day 1):**

| # | Task | Owner | Due |
|---|------|-------|-----|
| 7 | Conduct kick-off meeting | Joint | Day 1 |
| 8 | Confirm communication channels | Joint | Day 1 |
| 9 | Review deliverables and timeline | Joint | Day 1 |
| 10 | Assign points of contact | Joint | Day 1 |

**First Week (Days 2-7):**

| # | Task | Owner | Due |
|---|------|-------|-----|
| 11 | Send follow-up summary from kick-off | Provider | Day 2 |
| 12 | Set up recurring status meetings | Provider | Day 3 |
| 13 | Deliver first progress update | Provider | Day 5 |
| 14 | Confirm client satisfaction pulse | Provider | Day 7 |

Save to `onboarding-checklist.md`.

### Phase 3: Generate Documents

Create welcome kit via `anthropic-docx`:

**Welcome Kit Contents:**

| Section | Content |
|---------|---------|
| Welcome letter | Personalized greeting with project context |
| Team introduction | Key personnel with roles and contact info |
| Project overview | Objectives, scope summary, timeline overview |
| Communication plan | Preferred channels, meeting cadence, escalation path |
| Deliverables calendar | Key milestones with expected dates |
| Tools & access | Shared Drive link, Notion workspace link, other tool links |
| FAQ | Common questions and answers for new clients |
| Contact directory | All team members with roles and availability |

Polish Korean text via `sentence-polisher`.

Save to `welcome-kit.docx`.

### Phase 4: Set Up Workspace

Create digital workspace infrastructure:

**Google Drive** (via `gws-drive`):

```
{Client Name}/
├── 01-Contracts/
├── 02-Deliverables/
├── 03-Meeting-Notes/
├── 04-Resources/
└── 05-Invoices/
```

Upload `welcome-kit.docx` to `01-Contracts/`.

**Notion** (via `md-to-notion`):
- Create project page with:
  - Project overview section
  - Deliverables checklist (from Phase 2)
  - Meeting notes subpage
  - Status tracker (On Track / At Risk / Blocked)

**Google Calendar** (via `gws-calendar`):
- Schedule kick-off meeting on the start date
- Create recurring weekly status meeting (if applicable)
- Set reminder for first-week check-in

Log all created resources (links, IDs) to `workspace-setup.md`.

### Phase 5: Communications

Generate an onboarding email sequence:

**Email 1 - Welcome (Day -2):**

| Element | Content |
|---------|---------|
| Subject | "Welcome to {Project Name} - Getting Started" |
| Body | Welcome, team intro, shared Drive link, what to expect next |
| Attachments | welcome-kit.docx |
| CTA | "Please review the welcome kit and confirm your availability for the kick-off" |

**Email 2 - Kick-off Agenda (Day -1):**

| Element | Content |
|---------|---------|
| Subject | "Kick-off Meeting Agenda - {Project Name}" |
| Body | Meeting agenda, preparation items, calendar link |
| CTA | "Please prepare any questions about the project scope" |

**Email 3 - Kick-off Follow-up (Day 2):**

| Element | Content |
|---------|---------|
| Subject | "Kick-off Summary & Next Steps - {Project Name}" |
| Body | Meeting summary, confirmed decisions, action items with owners |
| CTA | "Please confirm the action items assigned to your team" |

**Email 4 - Week 1 Check-in (Day 7):**

| Element | Content |
|---------|---------|
| Subject | "Week 1 Update - {Project Name}" |
| Body | Progress summary, any blockers, upcoming milestones |
| CTA | "Let us know if you have any feedback on the first week" |

Save all drafts to `email-sequence.md`.

Optionally send Email 1 via `gws-gmail` (with user confirmation).

### Phase 6: Deliver

1. Write `manifest.json` with:
   - Client profile summary
   - Checklist item count and completion status
   - Workspace resource links (Drive folder, Notion page, Calendar events)
   - Email sequence status (drafted / sent)
   - File paths and timestamps

2. Post onboarding summary to Slack (if available):
   - Main: "New client onboarded: {Client Name} - {Project Name}"
   - Thread: checklist status, workspace links, next actions

## Customization

Users can provide:
- **Custom checklist template**: Override default checklist with industry-specific tasks
- **Branding**: Logo and colors for welcome kit formatting
- **Email templates**: Existing email templates to merge with generated content
- **Additional workspace tools**: Jira, Linear, Asana board setup instructions
- **SLA requirements**: Include SLA terms in welcome kit and checklist

## Examples

### Example 1: Full client onboarding

User says: "Onboard Acme Corp — they signed the Enterprise plan yesterday"

Actions:
1. Extract client details from contract/CRM
2. Create Google Drive workspace with template folders
3. Set up Notion project page with milestones
4. Schedule kickoff and check-in meetings
5. Send welcome email sequence
6. Generate onboarding tracker dashboard

Result: Complete workspace, scheduled meetings, welcome emails sent, Notion tracker, Slack notification

### Example 2: Korean client onboarding

User says: "신규 고객 온보딩해줘 — B사 엔터프라이즈 플랜"

Actions:
1. Extract details, create Korean-labeled workspace
2. Set up meetings with Korean business hours
3. Send welcome emails in Korean with proper honorifics

Result: Korean workspace, Korean communications, onboarding tracker

## Error Handling

If Drive folder creation fails, log the error and continue with other phases. Workspace setup failures are non-blocking; each resource (Drive, Notion, Calendar) is created independently. Email drafts are always generated locally even if send fails.

## Gotchas

- Drive folder sharing permissions must be set to the client's email domain, not individual emails, unless specified
- Notion workspace sharing requires the client to have a Notion account; include signup instructions if needed
- Calendar event time zones must match the client's location, not the provider's
- Welcome kit should not include internal pricing or margin information
- Email sequence assumes business days; adjust for weekends and holidays
- Always use the client's preferred name/salutation from the intake form, not assumptions
