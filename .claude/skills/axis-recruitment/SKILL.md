---
name: axis-recruitment
description: >-
  Axis 1 of the 6-Axis Personal Assistant. Recruitment management — job
  application tracking, interview preparation, resume optimization, company
  research, and career strategy. Maintains a persistent job pipeline and
  provides daily briefings on application status. Use when the user asks for
  "axis recruitment", "recruitment axis", "채용 축", "job axis",
  "axis-recruitment", or wants career and recruitment management. Do NOT use
  for general company research without recruitment context (use
  parallel-deep-research). Do NOT use for calendar management (use axis-life).
---

# Axis 1: Recruitment

Manages the full recruitment lifecycle: job discovery, application tracking,
company research, interview preparation, resume optimization, and career
strategy. Maintains a persistent job pipeline with stages.

## Principles

- **Single Responsibility**: Only recruitment and career management
- **Context Isolation**: Writes to `outputs/axis/recruitment/{date}/`
- **Failure Isolation**: Company research failure does not block pipeline status
- **File-First Data Bus**: Job pipeline as a JSON file for cross-axis use

## Phase Guard Protocol

Before running portal scans or inbox checks, verify that today's outputs
do not already exist. If they do, SKIP the phase and reuse existing data.

| Phase | Guard File | Skip Condition |
|-------|-----------|----------------|
| 1 (Portal scan) | `outputs/axis/recruitment/{date}/portal-scan.json` | File exists |
| 2 (Inbox filter) | `outputs/axis/recruitment/{date}/inbox-candidates.json` | File exists |

Pass `--force` to bypass all guards and re-run from scratch.
When a phase is skipped, log `REUSED — {guard_file}` in the dispatch manifest.

## Composed Skills

### Research
- `parallel-deep-research`, `199-deep-research` — deep company research
- `kwp-sales-account-research` — company intel (repurposed for target employers)
- `kwp-common-room-account-research` — company signals
- `tech-trend-analyzer` — evaluate company tech stack

### Interview Prep
- `kwp-human-resources-interview-prep` — structured interview plans
- `kwp-sales-call-prep` — meeting preparation (repurposed for interviews)
- `presentation-strategist` — presentation skills for case studies
- `adaptive-tutor` — practice technical topics

### Resume & Profile
- `pm-toolkit` — resume review against PM best practices
- `kwp-marketing-brand-voice` — personal brand consistency
- `anthropic-docx` — resume/cover letter generation

### Content & Networking
- `content-repurposing-engine` — LinkedIn posts from work achievements
- `hook-generator` — attention-grabbing opener for cover letters
- `kwp-sales-draft-outreach` — networking email drafts

### Pipeline Monitoring
- `portal-scanner` — scrape job boards for new listings
- `evaluation-engine` — score opportunities against criteria
- `report-archiver` — archive pipeline snapshots

### Communication
- `gws-email-reply` — respond to recruiter emails
- `sentence-polisher` — polish application materials

## Workflow

### Morning Run (triggered by `axis-dispatcher` ~07:30)

```
Phase 1: Pipeline status        → outputs/axis/recruitment/{date}/pipeline-status.json
Phase 2: New opportunities scan → outputs/axis/recruitment/{date}/new-opportunities.json
Phase 3: Interview prep check   → outputs/axis/recruitment/{date}/interview-prep.json
Phase 4: Recruitment brief      → outputs/axis/recruitment/{date}/recruitment-briefing.md
```

**Phase 1 — Pipeline Status** *(guarded)*
Check Phase Guard: if `outputs/axis/recruitment/{date}/portal-scan.json` exists,
SKIP. Otherwise read `outputs/axis/recruitment/job-pipeline.json` (persistent).
Count applications by stage (Applied, Phone Screen, Technical, Onsite, Offer,
Rejected). Flag items with upcoming deadlines or stale status (>7 days in
same stage). Write to `portal-scan.json`.

**Phase 2 — New Opportunities Scan** *(guarded)*
Check Phase Guard: if `outputs/axis/recruitment/{date}/inbox-candidates.json`
exists, SKIP. Otherwise check configured job boards / email for new relevant
positions. Score each against criteria (role fit, company match, location,
compensation). Write top candidates to `inbox-candidates.json`.

**Phase 3 — Interview Prep Check**
For any pipeline items in Phone Screen / Technical / Onsite stage with
interviews scheduled today or tomorrow:
- Generate prep brief via `kwp-human-resources-interview-prep`
- Include company research via `parallel-deep-research`
Write to `interview-prep.json`.

**Phase 4 — Recruitment Brief**
Compile Korean recruitment briefing:
1. Pipeline summary (count by stage)
2. Items needing action today
3. Upcoming interviews
4. New opportunities worth applying to

### Evening Run (triggered by `axis-dispatcher` ~17:00)

```
Phase E1: Application follow-up → outputs/axis/recruitment/{date}/followups.json
Phase E2: Pipeline update       → outputs/axis/recruitment/{date}/pipeline-updates.json
```

**Phase E1 — Follow-up Check**
Identify applications past 7 days without response. Draft follow-up emails.

**Phase E2 — Pipeline Updates**
Process any status changes from today (interview completions, rejections,
offers received).

## Output Artifacts

| Phase | Output File | Description |
|-------|-------------|-------------|
| 1 | `outputs/axis/recruitment/{date}/pipeline-status.json` | Pipeline by stage |
| 2 | `outputs/axis/recruitment/{date}/new-opportunities.json` | New job matches |
| 3 | `outputs/axis/recruitment/{date}/interview-prep.json` | Interview prep briefs |
| 4 | `outputs/axis/recruitment/{date}/recruitment-briefing.md` | Morning brief |
| E1 | `outputs/axis/recruitment/{date}/followups.json` | Follow-up drafts |
| E2 | `outputs/axis/recruitment/{date}/pipeline-updates.json` | Status changes |

## Persistent State

| File | Purpose |
|------|---------|
| `outputs/axis/recruitment/job-pipeline.json` | Master job application tracker |
| `outputs/axis/recruitment/criteria-config.json` | Job fit scoring criteria |

Job pipeline schema:
```json
[
  {
    "id": "job-001",
    "company": "Anthropic",
    "role": "AI Research Engineer",
    "stage": "applied",
    "applied_date": "2026-04-01",
    "last_update": "2026-04-05",
    "next_action": "Follow up if no response by 2026-04-08",
    "interview_date": null,
    "notes": "Referred by contact in #deep-research",
    "score": 92,
    "url": "https://anthropic.com/careers/..."
  }
]
```

### Pipeline Stages
`discovered` → `researching` → `applied` → `phone_screen` → `technical` → `onsite` → `offer` → `accepted` / `rejected` / `withdrawn`

## On-Demand Operations

- `/job add <company> <role> [url]` — Add to pipeline
- `/job update <id> <stage>` — Move to new stage
- `/job prep <id>` — Generate interview prep for specific application
- `/job research <company>` — Deep company research

## Slack Channel

- `#효정-할일` — recruitment brief, interview reminders

## Automation Level

Tracked centrally in `outputs/axis/automation-levels.json`.
Full protocol: `axis-dispatcher/references/automation-levels.md`.

- **Level 0 (current)**: Report only — pipeline status and prep reminders
- **Level 1**: Auto-scan job boards + suggest applications with scoring
- **Level 2**: Auto-generate resume tailoring and interview prep docs

Job applications and outreach emails NEVER auto-send (safety constraint).

## Error Recovery

Follow the protocol in `axis-dispatcher/references/failure-alerting.md`.

Job board scanning may fail due to anti-bot measures. If scanning fails,
report the failure and skip to Phase 3 (interview prep doesn't depend on
new opportunity scanning).

Write errors to `outputs/axis/recruitment/{date}/errors.json` using the
standard error record format (severity S1-S4, phase, impact, recovery).

## Gotchas

- Job pipeline is manually maintained — the axis tracks status but the
  user must confirm stage transitions
- Interview prep requires lead time — schedule prep generation for
  interviews 2+ days out, not same-day
- Company research can be expensive (many web searches); cache results
  in `outputs/axis/recruitment/{company}/research.md`
