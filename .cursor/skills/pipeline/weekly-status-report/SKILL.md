---
name: weekly-status-report
description: >-
  Generate automated weekly status reports by aggregating GitHub sprint data,
  Notion project updates, Slack channel summaries, and completed tasks.
  Produces a structured Korean report as .docx + Notion page + Slack post.
  Use when the user asks to "generate weekly report", "weekly status",
  "주간 리포트", "주간 보고서", "weekly-status-report", or wants automated
  weekly reporting. Do NOT use for daily stock reports (use today), GitHub
  activity digests only (use github-sprint-digest), or cross-project portfolio
  reports (use portfolio-report-generator).
metadata:
  version: "1.0.2"
  category: "execution"
  author: "thaki"
---
# Weekly Status Report Generator

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

Aggregate data from multiple sources into a structured weekly status report, replacing the manual 4-hour weekly reporting process.

## When to Use

- End of each sprint week (typically Friday afternoon)
- When management requests a status update
- As part of the EOD pipeline on reporting days

## Configuration

- **Run date** (`{date}`): ISO date `YYYY-MM-DD` for this pipeline run (typically the Friday of the reporting week). Drives all paths under `outputs/weekly-status-report/{date}/`.
- **Report period**: Past 7 calendar days ending on `{date}` unless the user specifies a custom window (still persist the chosen window in `manifest.json`).

## Pipeline Output Protocol (File-First)

All multi-phase work MUST persist intermediate results under:

- **Output directory**: `outputs/weekly-status-report/{date}/`

### Per-phase files

Each phase writes exactly one JSON file:

| Phase | Label | Output file |
| ----- | ----- | ----------- |
| 1 | gather | `outputs/weekly-status-report/{date}/phase-1-gather.json` |
| 2 | classify | `outputs/weekly-status-report/{date}/phase-2-classify.json` |
| 3 | metrics | `outputs/weekly-status-report/{date}/phase-3-metrics.json` |
| 4 | report | `outputs/weekly-status-report/{date}/phase-4-report.json` |
| 5 | docx | `outputs/weekly-status-report/{date}/phase-5-docx.json` |
| 6 | notion | `outputs/weekly-status-report/{date}/phase-6-notion.json` |
| 7 | slack | `outputs/weekly-status-report/{date}/phase-7-slack.json` |

### Manifest

- **Path**: `outputs/weekly-status-report/{date}/manifest.json`
- **Purpose**: Single index of all phases, statuses, artifact paths, and errors for resumability and audit.

#### manifest.json schema

```json
{
  "$schema": "weekly-status-report-manifest/v1",
  "run_id": "string",
  "date": "YYYY-MM-DD",
  "period_start": "YYYY-MM-DD",
  "period_end": "YYYY-MM-DD",
  "phases": [
    {
      "id": 1,
      "label": "gather",
      "status": "pending|running|completed|failed|skipped",
      "output_file": "phase-1-gather.json",
      "completed_at": "ISO-8601|null",
      "error": "string|null"
    }
  ],
  "updated_at": "ISO-8601"
}
```

Repeat `phases[]` entries for `id` 1–7 with labels `gather`, `classify`, `metrics`, `report`, `docx`, `notion`, `slack` and matching `output_file` names.

### Subagent Return Contract

When delegating to subagents, each subagent MUST return **only** this JSON shape (no large payloads in chat):

```json
{
  "status": "completed|failed|skipped",
  "file": "outputs/weekly-status-report/{date}/phase-N-<label>.json",
  "summary": "One-line outcome for the manifest log"
}
```

The orchestrator MUST merge the result into the phase JSON file on disk and update `manifest.json` (`phases[id-1].status`, `completed_at`, `error`).

### Final aggregation rule

Steps that produce the **Korean report body**, **.docx**, **Notion page**, and **Slack post** MUST read inputs **only** from:

- `manifest.json` (phase list, paths, period)
- Prior phase JSON files in `outputs/weekly-status-report/{date}/` (not from in-context memory or earlier chat turns).

### Output Artifacts (file flow)

| Phase | Stage | Output file | Consumed by |
| ----- | ----- | ----------- | ----------- |
| 1 | Gather sources | `phase-1-gather.json` | Phase 2, 4 |
| 2 | Classify / organize | `phase-2-classify.json` | Phase 3, 4 |
| 3 | Metrics | `phase-3-metrics.json` | Phase 4 |
| 4 | Korean report (3P) | `phase-4-report.json` | Phase 5, 6, 7 |
| 5 | DOCX | `phase-5-docx.json` | Phase 6, 7 (optional link) |
| 6 | Notion | `phase-6-notion.json` | Phase 7 |
| 7 | Slack | `phase-7-slack.json` | — |

## Workflow

### Initialization (before Step 1)

1. Resolve `{date}` (default: reporting Friday or user-specified run date).
2. Create the output directory: `mkdir -p outputs/weekly-status-report/{date}/`.
3. Write initial `manifest.json` with `run_id` (e.g. `weekly-{date}`), `period_start` and `period_end` for the 7-day window, all seven phases listed with `status: "pending"`, `output_file` set per the table above, `updated_at` set to now.

### Step 1: Gather Data Sources

Collect data from the past 7 days across all sources:

**GitHub** (via `github-sprint-digest` data):
```bash
gh issue list --state all --json number,title,state,labels,closedAt,assignees --search "updated:>=$(date -v-7d +%Y-%m-%d)"
gh pr list --state all --json number,title,state,mergedAt,author --search "updated:>=$(date -v-7d +%Y-%m-%d)"
```

**Notion** (via `planning-weekly-pulse` data):
- Project status changes
- Completed milestones
- Updated roadmap items

**Slack** (via Slack MCP):
- Key decisions from team channels
- Blockers raised and resolved
- Customer feedback highlights

**Persist & manifest**: Write structured gather results to `outputs/weekly-status-report/{date}/phase-1-gather.json`. Set `manifest.json` phase 1 to `completed` (or `failed` with `error`). Subagents, if used, return only `{ status, file, summary }`; merge into the phase file and manifest.

### Step 2: Classify and Organize

**Inputs**: Read **only** from `outputs/weekly-status-report/{date}/phase-1-gather.json` and `manifest.json` — do not use chat context for raw gathered data.

Group gathered data into standard sections:

1. **Accomplishments**: Merged PRs, closed issues, completed milestones
2. **In Progress**: Open PRs, active issues, ongoing work
3. **Blockers**: Blocked items, unresolved dependencies, stale reviews
4. **Risks**: Overdue items, scope changes, resource constraints
5. **Next Week Plan**: Upcoming milestones, planned work, meetings

**Persist & manifest**: Write classification output to `outputs/weekly-status-report/{date}/phase-2-classify.json`. Update `manifest.json` phase 2. Subagents return only `{ status, file, summary }`.

### Step 3: Generate Metrics

**Inputs**: Read **only** from `outputs/weekly-status-report/{date}/phase-1-gather.json`, `outputs/weekly-status-report/{date}/phase-2-classify.json`, and `outputs/weekly-status-report/{date}/manifest.json`.

Calculate key metrics:
- **Velocity**: Story points completed vs planned
- **PR Cycle Time**: Average time from PR open to merge
- **Issue Resolution**: Issues opened vs closed
- **Sprint Burndown**: Remaining work vs sprint timeline
- **Review Coverage**: PRs reviewed within 24h

**Persist & manifest**: Write metrics to `outputs/weekly-status-report/{date}/phase-3-metrics.json`. Update `manifest.json` phase 3.

### Step 4: Write Report

**Inputs**: Read **only** from `outputs/weekly-status-report/{date}/phase-1-gather.json`, `outputs/weekly-status-report/{date}/phase-2-classify.json`, `outputs/weekly-status-report/{date}/phase-3-metrics.json`, and `outputs/weekly-status-report/{date}/manifest.json`. Do **not** reconstruct sections from memory.

Generate a structured Korean report following the 3P format (Progress, Plans, Problems). Include: title with date range; executive summary (3 sentences); accomplishments with checkmarks and owners; metrics table (week vs prior week); next-week plan; risks/blockers with severity. Use Korean section headings and bullets per output rule.

**Persist & manifest**: Write the full report structure and body (or paths to embedded sections) to `outputs/weekly-status-report/{date}/phase-4-report.json` so later steps depend on file content only. Update `manifest.json` phase 4.

### Step 5: Generate .docx

**Inputs**: Read **only** from `outputs/weekly-status-report/{date}/phase-4-report.json` and `outputs/weekly-status-report/{date}/manifest.json` for report text and metadata — not from prior step narration in context.

Use `anthropic-docx` to create a formatted Word document with:
- Company header/footer
- Table of contents
- Formatted metrics tables
- Color-coded status indicators

**Persist & manifest**: Record absolute path to the generated `.docx`, checksum or size if useful, and status to `outputs/weekly-status-report/{date}/phase-5-docx.json`. Update `manifest.json` phase 5.

### Step 6: Publish to Notion

**Inputs**: Read **only** from `outputs/weekly-status-report/{date}/phase-4-report.json` (and optionally `outputs/weekly-status-report/{date}/phase-5-docx.json` for linked file path) and `outputs/weekly-status-report/{date}/manifest.json` — build Notion content from files, not from chat history.

Use `md-to-notion` to create a Notion page under the weekly reports parent.

**Persist & manifest**: Write Notion page URL, page id, and status to `outputs/weekly-status-report/{date}/phase-6-notion.json`. Update `manifest.json` phase 6.

### Step 7: Post to Slack

**Inputs**: Read **only** from `outputs/weekly-status-report/{date}/manifest.json`, `outputs/weekly-status-report/{date}/phase-4-report.json` (condensed summary fields), `outputs/weekly-status-report/{date}/phase-5-docx.json` (link/path if posted), and `outputs/weekly-status-report/{date}/phase-6-notion.json` (Notion URL). Do **not** rely on unstored context for metrics or accomplishments text.

Post a condensed summary to the team Slack channel with:
- Key metrics as inline stats
- Top 3 accomplishments
- Critical blockers
- Link to full report (Notion page)

**Persist & manifest**: Write Slack channel, message timestamp or permalink, and status to `outputs/weekly-status-report/{date}/phase-7-slack.json`. Set `manifest.json` phase 7 to `completed` and finalize `updated_at`.

## Output

```
Weekly Report Generated
=======================
Period: 2026-03-13 ~ 2026-03-19
Report ID: weekly-2026-W12

Run artifacts (file-first):
- Directory: outputs/weekly-status-report/2026-03-19/
- Manifest: outputs/weekly-status-report/2026-03-19/manifest.json
- Phases: phase-1-gather.json … phase-7-slack.json

Outputs:
- DOCX: path from phase-5-docx.json (e.g. output/reports/weekly-2026-W12.docx)
- Notion: URL from phase-6-notion.json
- Slack: Posted to #team-updates (see phase-7-slack.json)

Metrics Summary:
- Story Points: 21/25 (84%)
- PRs Merged: 8
- Issues Closed: 12
- Blockers: 2 active
```

## Error Handling

| Error | Action |
|-------|--------|
| GitHub API rate limit | Retry with exponential backoff; if exhausted, persist partial data to `phase-1-gather.json`, set phase 1 `failed` or `completed` with warning in JSON; note "GitHub data incomplete" in downstream files |
| Notion MCP not connected | Skip Notion: set phase 6 `skipped` in manifest; persist DOCX path in `phase-5-docx.json`; post to Slack using only `phase-4-report.json` + `phase-5-docx.json`; prompt user to connect Notion |
| No activity in time range | Persist minimal structured content to phase files; `phase-4-report.json` contains "No activity this period" per section; still produce DOCX and Slack per file-first steps |
| DOCX generation fails | Set `phase-5-docx.json` `status: failed`; retry `anthropic-docx`; if still fails, persist markdown path in phase 5 and post from `phase-4-report.json` |
| Slack posting fails | Persist error in `phase-7-slack.json`; retry once; report failure with paths under `outputs/weekly-status-report/{date}/` |
| Mid-pipeline failure | Resume from last `completed` phase using `manifest.json` and existing `phase-*.json` files; do not rely on chat memory |

## Examples

### Example 1: End-of-week report
User says: "Generate weekly report"
Actions:
1. Initialize `outputs/weekly-status-report/{date}/` and `manifest.json`
2. Aggregate 7 days of GitHub, Notion, Slack data → `phase-1-gather.json`
3. Classify → `phase-2-classify.json`; metrics → `phase-3-metrics.json`
4. Write Korean report → `phase-4-report.json` (inputs from phases 1–3 only)
5. DOCX, Notion, Slack from phase files only → `phase-5` through `phase-7` JSON
Result: Complete weekly report; all phases on disk under the dated folder

### Example 2: Custom period
User says: "Weekly report for last two weeks"
Actions:
1. Set `period_start` / `period_end` in `manifest.json` to 14-day window
2. Run phases 1–7; persist comparative metrics in `phase-3-metrics.json` and narrative in `phase-4-report.json`
Result: Two-week report with trend comparison; same file-first layout


## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
