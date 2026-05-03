---
name: meeting-intelligence-system
description: >-
  End-to-end meeting intelligence pipeline that ingests transcripts, extracts
  decisions and action items with structured tracking, logs decisions to a
  persistent decision register, creates calendar follow-ups, analyzes trends
  across meeting series, and delivers structured Korean summaries to Notion
  and Slack. Extends meeting-digest with CRM-style decision tracking, action
  item lifecycle, and multi-meeting trend analysis. Use when the user asks to
  "analyze meeting and track decisions", "meeting intelligence",
  "meeting-intelligence-system", "회의 인텔리전스", "회의 분석 + 의사결정 추적", "회의 트렌드 분석",
  "액션 아이템 추적 포함 회의 분석", "multi-meeting analysis", "meeting series trends", or
  wants a meeting summary with decision logging, action tracking, and calendar
  integration. Do NOT use for simple meeting summary without tracking (use
  meeting-digest). Do NOT use for action item tracking without meeting context
  (use meeting-action-tracker). Do NOT use for decision logging without
  meeting context (use decision-tracker).
---

# Meeting Intelligence System

Turn meeting transcripts into tracked decisions, owned action items with calendar reminders, and multi-meeting trend insights.

## When to Use

- A meeting transcript needs analysis AND persistent decision/action tracking
- Recurring meeting series need trend analysis (velocity, completion rates, blockers)
- Teams need automated follow-up scheduling after meetings
- Management wants decision audit trails with rationale and participants

## Output Artifacts

| Phase | Stage Name         | Output File                                                  |
| ----- | ------------------ | ------------------------------------------------------------ |
| 1     | Ingest             | `outputs/meeting-intelligence-system/{date}/raw-transcript.md`|
| 2     | Analyze            | `outputs/meeting-intelligence-system/{date}/analysis.md`      |
| 3     | Decisions          | `outputs/meeting-intelligence-system/{date}/decisions.md`     |
| 4     | Actions            | `outputs/meeting-intelligence-system/{date}/action-items.md`  |
| 5     | Trends             | `outputs/meeting-intelligence-system/{date}/trends.md`        |
| 6     | Summary            | `outputs/meeting-intelligence-system/{date}/summary.md`       |
| 6     | Manifest           | `outputs/meeting-intelligence-system/{date}/manifest.json`    |

## Workflow

### Phase 1: Ingest

Accept meeting transcript in any form:
- **File path**: Read transcript directly (`.txt`, `.md`, `.docx`)
- **Notion URL**: Fetch via Notion MCP
- **Pasted text**: Accept inline transcript
- **Meeting recording URL**: Extract via `defuddle` if supported

Delegate to `meeting-digest` Phase 1-2:
1. Parse transcript into structured content
2. Classify meeting type (standup, planning, review, 1:1, all-hands, external)

Save raw parsed content to `raw-transcript.md`.

### Phase 2: Analyze

Run `meeting-digest` Phase 3 (PM sub-skill analysis). Extract:

| Element | Description |
|---------|-------------|
| Decisions | Explicit agreements with context and participants |
| Action items | Tasks with implicit/explicit owners and deadlines |
| Key discussion points | Major topics with positions taken |
| Sentiment | Overall meeting tone (constructive/contentious/routine) |
| Blockers | Issues raised that prevent progress |
| Open questions | Unresolved items needing follow-up |

Save structured analysis to `analysis.md`.

### Phase 3: Decision Log

For each decision extracted in Phase 2, create a structured decision entry using `decision-tracker` patterns:

| Field | Description |
|-------|-------------|
| Decision ID | Auto-incrementing `DEC-{YYYYMMDD}-{N}` |
| Title | 1-line summary of the decision |
| Context | What problem or question triggered the decision |
| Rationale | Why this option was chosen over alternatives |
| Alternatives considered | Other options discussed |
| Participants | Who was involved in making the decision |
| Follow-up date | When to revisit (if applicable) |
| Status | proposed / approved / implemented / revised |

Save to `decisions.md`. Optionally log to Notion Decision Log database via `decision-tracker`.

### Phase 4: Action Item Tracking

For each action item from Phase 2, create a structured entry using `meeting-action-tracker` patterns:

| Field | Description |
|-------|-------------|
| Action ID | `ACT-{YYYYMMDD}-{N}` |
| Description | Clear, actionable task description |
| Owner | Assigned person (from transcript context) |
| Deadline | Explicit date or inferred from context |
| Priority | P0 (urgent) / P1 (high) / P2 (medium) / P3 (low) |
| Dependencies | Other actions or decisions this depends on |
| Status | open / in-progress / completed / overdue |

Save to `action-items.md`.

Optionally create calendar reminders via `gws-calendar`:
- Deadline reminder 1 day before due date
- Follow-up check 3 days after due date if not marked complete

### Phase 5: Trend Analysis (conditional)

If prior meeting data exists in `outputs/meeting-intelligence-system/`:

1. Scan previous meeting outputs in the same series (matched by participants or meeting title)
2. Compute metrics:

| Metric | Calculation |
|--------|-------------|
| Decision velocity | Decisions per meeting over time |
| Action completion rate | Completed / Total actions from prior meetings |
| Recurring blockers | Blockers appearing in 2+ consecutive meetings |
| Topic continuity | Topics carried over from prior meetings |
| Sentiment trend | Meeting tone trajectory |

3. Save trend analysis to `trends.md` with charts described in markdown table format

If no prior data exists, skip this phase and note "First meeting in series" in manifest.

### Phase 6: Deliver

1. Compile Korean structured summary to `summary.md`:
   - Meeting metadata (date, participants, type, duration)
   - Top 3 decisions with rationale
   - Action items table (owner, deadline, priority)
   - Key discussion highlights
   - Trend highlights (if available)
   - Polish Korean text via `sentence-polisher`

2. Write `manifest.json` with file paths, timestamps, meeting metadata, and phase completion status

3. Push to Notion sub-pages via `md-to-notion`:
   - Summary page
   - Action items page (as checklist)

4. Post summary thread to Slack (if Slack MCP available)

## Examples

### Example 1: Full meeting intelligence from transcript

User says: "Run meeting intelligence on this Zoom transcript"

Actions:
1. Ingest transcript, extract structured summary with meeting-digest
2. Log decisions to Notion Decision Log with rationale and participants
3. Create action items with owners and 24h/48h/72h Slack reminders
4. Save all artifacts to `outputs/meeting-intelligence-system/{date}/`

Result: Korean summary, decision log entries, tracked action items, Slack notifications

### Example 2: Multi-meeting trend analysis

User says: "Analyze trends across our last 5 sprint meetings"

Actions:
1. Retrieve 5 meeting records from Notion
2. Cross-reference decisions, recurring topics, and unresolved actions
3. Generate trend report with topic frequency, decision velocity, action completion rate

Result: Trend analysis .docx with charts and executive summary

## Error Handling

If Phase 3 or 4 fails, Phase 2 output at `analysis.md` remains valid. Fix the issue and re-run from the failed phase. Trend analysis (Phase 5) is optional and does not block delivery.

## Gotchas

- Transcript quality varies wildly; if speaker attribution is missing, do not fabricate owners for action items -- mark as "TBD"
- Decision detection requires explicit agreement language ("we decided", "let's go with"); implicit consensus is flagged as "proposed" not "approved"
- Calendar integration requires `gws-calendar` MCP access; skip gracefully if unavailable
- Trend analysis needs 2+ prior meetings to produce meaningful metrics; single prior meeting gets basic comparison only
