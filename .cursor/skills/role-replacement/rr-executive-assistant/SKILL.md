---
name: rr-executive-assistant
version: 1.0.0
description: >-
  Role Replacement Case Study: Executive Assistant — orchestrates daily calendar briefing,
  email triage, decision routing, and Slack cleanup with MemKraft-powered context pre-loading.
  Thin harness composing google-daily, ai-brief, decision-router, and slack-orphan-cleaner
  into a single EA role pipeline with provenance-tagged memory integration.
tags: [role-replacement, harness, productivity, google-workspace]
triggers:
  - rr-executive-assistant
  - executive assistant replacement
  - EA automation
  - 비서 대체
  - EA 역할 대체
do_not_use:
  - Individual Google Workspace operations (use gws-* skills directly)
  - Stock analysis briefing (use today)
  - General Slack messaging (use kwp-slack-slack-messaging)
  - Calendar-only briefing (use calendar-daily-briefing)
  - Email-only triage without EA context (use gmail-daily-triage)
composes:
  - google-daily
  - calendar-daily-briefing
  - gmail-daily-triage
  - decision-router
  - slack-orphan-cleaner
  - memkraft
  - ai-brief
  - ai-context-router
  - sentence-polisher
---

# Role Replacement: Executive Assistant

Thin harness that replaces a human Executive Assistant by orchestrating existing
pipeline skills into a 5-phase daily workflow with MemKraft-powered context
pre-loading and provenance-tagged decision routing.

## What This Replaces

| Human EA Task | Automated By | Skill |
|---|---|---|
| Morning schedule briefing | Calendar classification + focus window calc | `calendar-daily-briefing` |
| Email triage & draft replies | Sender-aware classification + tone-matched drafts | `gmail-daily-triage` |
| Decision escalation | Keyword detection + scope routing | `decision-router` |
| Context recall ("remind me about...") | Provenance-tagged memory retrieval | `memkraft` → `ai-context-router` |
| Slack housekeeping | Orphaned thread deletion | `slack-orphan-cleaner` |
| Daily summary distribution | Threaded Slack posts + Drive upload | `google-daily` Phase 4 |

## Prerequisites

- `gws` CLI installed and authenticated: `gws auth login -s drive,gmail,calendar`
- Slack MCP server connected with `SLACK_BOT_TOKEN` and `SLACK_USER_TOKEN` in `.env`
- MemKraft memory store initialized (see `memkraft` skill)
- Memory topic files exist under `memory/topics/`

## Architecture

```
rr-executive-assistant (thin harness)
  │
  Phase 0 ─→ ai-context-router (MemKraft pre-load)
  │            ├─ MemKraft: recent sessions, preferences, unresolved items
  │            └─ Wiki: relevant policies, runbooks, team knowledge
  │
  Phase 1 ─→ google-daily (6-phase pipeline)
  │            ├─ Phase 1: calendar-daily-briefing
  │            ├─ Phase 2: gmail-daily-triage
  │            ├─ Phase 3: Drive upload
  │            ├─ Phase 3.5: quality gate
  │            ├─ Phase 4: Slack notify (threaded)
  │            ├─ Phase 4.5: decision extraction → decision-router
  │            ├─ Phase 5: memory sync
  │            └─ Phase 6: slack-orphan-cleaner
  │
  Phase 2 ─→ Context enrichment (merge MemKraft with google-daily output)
  │
  Phase 3 ─→ Provenance-tagged EA briefing assembly
  │
  Phase 4 ─→ MemKraft write-back (session learnings)
```

## Pipeline Output Protocol

All outputs persist to `outputs/rr-executive-assistant/{date}/`.

| Phase | Label | Output File |
|---|---|---|
| 0 | context-preload | `phase-0-context-preload.json` |
| 1 | google-daily | `phase-1-google-daily.json` (summary referencing `outputs/google-daily/{date}/`) |
| 2 | context-enrichment | `phase-2-context-enrichment.json` |
| 3 | ea-briefing | `phase-3-ea-briefing.json` |
| 4 | memory-writeback | `phase-4-memory-writeback.json` |

Manifest: `outputs/rr-executive-assistant/{date}/manifest.json` following the standard schema
(`pipeline`, `date`, `started_at`, `completed_at`, `phases[]`, `overall_status`, `warnings[]`).

## Phase 0 — MemKraft Context Pre-load

**Purpose**: Pre-load personal context BEFORE the Google Workspace pipeline runs,
so calendar and email processing can leverage historical patterns.

Invoke `ai-context-router` with:
- Query: `"today's priorities, recent EA decisions, pending follow-ups, recurring sender patterns, calendar preferences"`
- `--recency-boost true`

Extract and persist:
- **Recent decisions**: Last 7 days of decision-router outputs
- **Sender patterns**: Recurring colleague communication patterns from MemKraft
- **Calendar preferences**: Meeting prep lead times, focus window preferences
- **Unresolved items**: Open action items carrying over from previous days

```json
{
  "context_sources": {
    "memkraft": { "entries_loaded": 12, "recency_days": 7 },
    "wiki": { "topics_matched": ["preferences", "slack-routing"] }
  },
  "sender_patterns": [
    { "sender": "kim@thakicloud.co.kr", "frequency": "daily", "typical_action": "reply-needed" }
  ],
  "unresolved_items": ["Follow up on GPU pricing proposal", "Reply to partner inquiry"],
  "calendar_preferences": { "focus_window_min_minutes": 30, "prep_lead_time_minutes": 15 }
}
```

**Persist**: Write to `outputs/rr-executive-assistant/{date}/phase-0-context-preload.json`.

## Phase 1 — Google Daily Pipeline

Delegate the full `google-daily` pipeline (6 internal phases). The google-daily
skill handles its own file-first persistence to `outputs/google-daily/{date}/`.

**Context injection**: Pass Phase 0 sender patterns to gmail-daily-triage so
recurring senders get priority classification. Pass calendar preferences to
calendar-daily-briefing for focus window thresholds.

**Subagent delegation**: Run as a single subagent with explicit inputs:

```
Run google-daily for {date}.
Context from Phase 0:
- Sender patterns: {sender_patterns from phase-0 JSON}
- Calendar preferences: {calendar_preferences from phase-0 JSON}
- Unresolved items to watch for in email: {unresolved_items from phase-0 JSON}
Return { status, file, summary }.
```

**Persist**: Write summary reference to `outputs/rr-executive-assistant/{date}/phase-1-google-daily.json`
with pointer to `outputs/google-daily/{date}/manifest.json`.

## Phase 2 — Context Enrichment

Merge google-daily outputs with MemKraft context to produce enriched insights
that a human EA would provide:

1. **Read** `outputs/google-daily/{date}/phase-1-calendar.json` and
   `outputs/google-daily/{date}/phase-2-gmail.json` from disk.
2. **Cross-reference** calendar events with MemKraft sender patterns:
   - Flag meetings with people who sent emails today (conversation continuity)
   - Flag meetings that relate to unresolved items from Phase 0
3. **Priority re-ranking**: Apply MemKraft preferences to adjust event priority
   (e.g., user prefers morning focus blocks, user's boss always gets HIGH).
4. **Draft enhancement**: Run `sentence-polisher` on gmail reply drafts to
   match the user's personal communication style from MemKraft preferences.

**Persist**: Write enrichment results to `outputs/rr-executive-assistant/{date}/phase-2-context-enrichment.json`.

## Phase 3 — EA Briefing Assembly

Generate the provenance-tagged Executive Assistant briefing by reading Phase 0-2
outputs from disk. Format follows `ai-brief` provenance structure.

### Briefing Template

```markdown
## EA 브리핑 — {YYYY-MM-DD}

### Personal Context (MemKraft)
- [RECENT] {yesterday's key decisions and outcomes}
- [PREFERENCE] {working style preferences relevant to today}
- [UNRESOLVED] {open items carrying over — count and top 3}

### 오늘의 일정
| 시간 | 일정 | 우선순위 | 준비사항 |
|---|---|---|---|
| {time} | {event} | {HIGH/MED/LOW} | {prep notes + MemKraft context} |

집중 가능 시간: {focus windows from calendar}

### 이메일 요약
- 답장 필요: {count}건 — {top 3 senders with MemKraft relationship context}
- 팀원 메일: {count}건
- 뉴스: {count}건
- 알림 정리: {count}건 → Low Priority

### 의사결정 필요 항목
{count}건이 decision channels로 라우팅됨
- Personal (#효정-의사결정): {count}건
- Team (#7층-리더방): {count}건

### EA 추천 액션
Based on schedule density and pending items:
1. {top priority with reasoning}
2. {second priority}
3. {items to defer until focus window}
```

All outputs in Korean. Technical terms in English.

**Persist**: Write to `outputs/rr-executive-assistant/{date}/phase-3-ea-briefing.json`.

## Phase 4 — MemKraft Write-back

After the pipeline completes, write session learnings back to MemKraft:

1. **New sender patterns** discovered during email triage
2. **Decision outcomes**: Items routed to decision channels (for future reference)
3. **Calendar insights**: Meeting patterns (e.g., "Tuesdays are heavy meeting days")
4. **Unresolved carry-forward**: Items not addressed today → HOT tier

Write via `memkraft-ingest` with provenance tag `source: rr-executive-assistant`.

**Persist**: Write to `outputs/rr-executive-assistant/{date}/phase-4-memory-writeback.json`.

## Memory Configuration

| Tier | Content | Retention |
|---|---|---|
| HOT | Today's unresolved items, active decision items, meeting prep notes | Session-scoped, 24h |
| WARM | Sender communication patterns, calendar density trends, recurring topics | 30 days, decayed by attention_decay.py |
| Knowledge | Team routing rules, Slack channel registry, email classification policies | Persistent in `memory/topics/slack-routing.md`, `memory/topics/preferences.md` |

### MemKraft Integration Points

| Point | Direction | Data |
|---|---|---|
| Phase 0 pre-load | READ | Sender patterns, calendar prefs, unresolved items |
| Phase 2 enrichment | READ | Communication style, relationship context |
| Phase 4 write-back | WRITE | New patterns, decision outcomes, carry-forward items |

## Slack Configuration

Inherits from `google-daily`:

| Key | Value |
|---|---|
| Main Channel | `#효정-할일` (`C0AA8NT4T8T`) |
| Decision (Personal) | `#효정-의사결정` (`C0ANBST3KDE`) |
| Decision (Team) | `#7층-리더방` (`C0A6Q7007N2`) |

## Error Recovery

| Phase | Failure | Action |
|---|---|---|
| 0 (Context Pre-load) | MemKraft unavailable | Proceed without context enrichment; log warning |
| 1 (Google Daily) | Partial failure | google-daily handles internally; this harness reads manifest status |
| 2 (Context Enrichment) | Cross-reference fails | Skip enrichment; use raw google-daily output |
| 3 (EA Briefing) | Assembly error | Post raw google-daily summary instead |
| 4 (Memory Write-back) | MemKraft write fails | Log warning; pipeline still succeeds |

Resume from the last successful `phase-*.json` under `outputs/rr-executive-assistant/{date}/`.

## Security Rules

Inherited from `google-daily`:
- No automatic email sending (draft replies in Slack threads only)
- No calendar event deletion
- No Gmail filter creation without user confirmation
- No credential/secret file uploads
- No spam body opening (classify by sender/subject only)

## Honest Reporting

- Report outcomes faithfully — never claim all phases passed when any failed
- Never suppress errors, partial results, or skipped phases
- Surface unexpected findings even if they complicate the narrative
- If a phase produces no actionable output, say so explicitly

## Coordinator Synthesis

- Do not reconstruct phase outputs from chat context — always read from persisted files
- Each phase dispatch includes a purpose statement explaining the expected transformation
- File paths and line numbers must be specific, not inferred
- Never delegate with vague instructions like "analyze this" — provide concrete specs

## Subagent Contract

Every subagent dispatch MUST include:
1. **Purpose statement** — one sentence explaining why this subagent exists
2. **Absolute file paths** — all input/output paths as absolute paths
3. **Return contract** — subagent must return JSON: `{"status": "ok|error", "file": "<output_path>", "summary": "<1-line>"}`
4. Load-bearing outputs must be written to disk, not passed via chat context

## Operational Runbook

### Daily Execution

```bash
# Typical invocation (morning routine)
# Via daily-am-orchestrator or direct:
> rr-executive-assistant

# Or as part of morning-ship:
> /morning-ship  # includes google-daily which this skill wraps
```

### Manual Override

```bash
# Skip decision routing (quiet mode)
> rr-executive-assistant --skip-decisions

# Quick mode (calendar + MemKraft only, no email triage)
> rr-executive-assistant --quick
```

### Health Check

Verify prerequisites before first run:
1. `gws auth status` — Google Workspace auth valid
2. `.env` contains `SLACK_BOT_TOKEN` and `SLACK_USER_TOKEN`
3. `memory/topics/preferences.md` exists with sender patterns
4. `outputs/google-daily/` directory is writable

## Comparison: Human EA vs This Skill

| Dimension | Human EA | rr-executive-assistant |
|---|---|---|
| Cost | $4,000-8,000/mo | ~$2-5/day (API + compute) |
| Availability | Business hours | 24/7 |
| Context recall | Limited by memory | Full MemKraft history |
| Consistency | Variable | Deterministic pipeline |
| Judgment | Superior for ambiguous situations | Rule-based with decision-router escalation |
| Personalization | Learns over months | MemKraft patterns from day 1 |
| Limitation | Single-threaded | Parallel subagent execution |

### Where Human EA Still Wins

- Ambiguous social situations requiring emotional intelligence
- Phone calls and in-person meeting logistics
- Relationship management beyond email/Slack
- Crisis situations requiring real-time judgment

## Examples

### Example 1: Standard morning run

**User says**: "rr-executive-assistant" or "비서 대체 실행"

**Actions**:
1. Phase 0: Load MemKraft context (12 recent entries, 3 unresolved items)
2. Phase 1: Run google-daily (8 calendar events, 23 emails triaged)
3. Phase 2: Cross-reference — flag 2 meetings with today's email senders
4. Phase 3: Generate provenance-tagged EA briefing in Korean
5. Phase 4: Write 3 new sender patterns + 2 carry-forward items to MemKraft

**Result**: Structured briefing posted to Slack with context a human EA would provide.

### Example 2: Quick mode before a meeting

**User says**: "rr-executive-assistant --quick"

**Actions**:
1. Phase 0: Load MemKraft context (focus on meeting-related items)
2. Phase 1: Run calendar-daily-briefing only (skip email triage)
3. Phase 3: Generate abbreviated briefing
4. Phase 4: Minimal write-back

**Result**: 30-second briefing with today's schedule and MemKraft context.
