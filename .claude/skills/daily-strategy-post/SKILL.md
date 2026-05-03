---
name: daily-strategy-post
description: >-
  Run multi-role strategic analysis on the day's aggregated intelligence and
  post company/team/product strategy documents to Slack. Synthesizes all daily
  inputs (emails, news, sprint data, research) into actionable strategy
  briefings. Use when the user asks to "post daily strategy", "전략 브리핑 올려줘",
  "daily strategy", "오늘의 전략 분석", "daily-strategy-post", or wants end-of-day
  strategic analysis distributed to the team. Do NOT use for single-role
  analysis (use the specific role-* skill), morning briefings (use
  morning-ship), or investor presentations (use presentation-strategist).
---

# daily-strategy-post

Run multi-role strategic analysis on the day's aggregated intelligence and distribute to Slack.

## Configuration

- **`{date}`**: Pipeline run date (`YYYY-MM-DD`); default to today's date in the operator's timezone unless the user specifies otherwise.
- **Output root**: `outputs/daily-strategy-post/{date}/` (created during Initialization).

## Pipeline Output Protocol (File-First)

- **Output directory**: `outputs/daily-strategy-post/{date}/`
- **Per-phase artifacts**: Each numbered phase writes exactly one JSON file: `outputs/daily-strategy-post/{date}/phase-{N}-{label}.json` (e.g. `phase-1-aggregate.json`, `phase-2-role-dispatch.json`).
- **`manifest.json`**: Stored in the same directory; records every phase, status, output filename, and errors. Update after each phase completes.
- **Subagent Return Contract**: Subagents return only:

  ```json
  { "status": "ok|error|skipped", "file": "<path>", "summary": "<one short paragraph>" }
  ```

  `file` MUST point to the phase JSON written under the output directory when `status` is `ok`.
- **Final-stage rule**: Executive packaging, strategy document finalization, and Slack/Drive distribution MUST read inputs **only** from `phase-*.json` and `manifest.json` on disk — not from prior chat context, not from uncached subagent narration alone.

### `manifest.json` schema

| Field | Type | Description |
| --- | --- | --- |
| `skill` | string | Constant: `"daily-strategy-post"`. |
| `date` | string | Run date `YYYY-MM-DD`. |
| `run_id` | string | Optional unique id (uuid or timestamp) if multiple runs per day. |
| `started_at` | string | ISO 8601 when the run started. |
| `updated_at` | string | ISO 8601 when the manifest was last written. |
| `phases` | array | Ordered phase records. |
| `phases[].phase` | number | Phase index (1-based). |
| `phases[].label` | string | Slug matching the filename (e.g. `aggregate`). |
| `phases[].status` | string | `pending` \| `running` \| `completed` \| `failed` \| `skipped`. |
| `phases[].output_file` | string | Filename only (e.g. `phase-1-aggregate.json`). |
| `phases[].error` | string \| null | Error message when `status` is `failed`. |
| `version` | number | Manifest format version; use `1`. |

Example initial `manifest.json`:

```json
{
  "skill": "daily-strategy-post",
  "date": "2026-04-01",
  "run_id": "",
  "started_at": "2026-04-01T09:00:00+09:00",
  "updated_at": "2026-04-01T09:00:00+09:00",
  "phases": [
    { "phase": 1, "label": "aggregate", "status": "pending", "output_file": "phase-1-aggregate.json", "error": null },
    { "phase": 2, "label": "role-dispatch", "status": "pending", "output_file": "phase-2-role-dispatch.json", "error": null },
    { "phase": 3, "label": "executive-synthesis", "status": "pending", "output_file": "phase-3-executive-synthesis.json", "error": null },
    { "phase": 4, "label": "strategy-documents", "status": "pending", "output_file": "phase-4-strategy-documents.json", "error": null },
    { "phase": 5, "label": "distribute", "status": "pending", "output_file": "phase-5-distribute.json", "error": null }
  ],
  "version": 1
}
```

## Output Artifacts

| Phase | Stage | Output file | Notes |
| --- | --- | --- | --- |
| Init | Directory + manifest | `manifest.json` | Created before phase 1; updated after each phase |
| 1 | Aggregate intelligence | `phase-1-aggregate.json` | Input to phase 2 |
| 2 | Role dispatch | `phase-2-role-dispatch.json` | Input to phase 3 |
| 3 | Executive synthesis | `phase-3-executive-synthesis.json` | Input to phase 4 |
| 4 | Strategy documents | `phase-4-strategy-documents.json` | Input to phase 5 |
| 5 | Distribute | `phase-5-distribute.json` | Slack/Drive receipts; audit trail |

## Workflow

### Initialization (before Phase 1)

1. Create `outputs/daily-strategy-post/{date}/` if it does not exist.
2. Write initial `manifest.json` with all five phases in `pending`, `started_at`, and `updated_at` set.
3. **Persist & manifest**: Confirm the directory exists and `manifest.json` is readable; treat manifest on disk as the source of truth for run state.

### Phase 1 — Aggregate intelligence

Collect the day's outputs: email research findings, Twitter/news intelligence, GitHub sprint digest, knowledge graph updates. Serialize the full bundle (paths, summaries, structured fields) to `phase-1-aggregate.json`.

- **Persist & manifest**: Write `outputs/daily-strategy-post/{date}/phase-1-aggregate.json`. Set phase 1 to `completed` in `manifest.json` (or `failed` with `phases[].error`); refresh `updated_at`.

### Phase 2 — Role dispatch

Run `role-dispatcher` with the aggregated intelligence loaded **from** `phase-1-aggregate.json` (file is the source of truth). Activate CEO, CTO, PM, CSO perspectives at minimum. Write role outputs and execution metadata to `phase-2-role-dispatch.json`.

- **Persist & manifest**: Write `phase-2-role-dispatch.json`; update phase 2 status in `manifest.json`; refresh `updated_at`.

### Phase 3 — Executive synthesis

Invoke `executive-briefing` with inputs read **only** from `phase-2-role-dispatch.json` (and `manifest.json` for ordering/checks). Produce cross-role consensus, conflicts, and prioritized action items; save to `phase-3-executive-synthesis.json`.

- **Persist & manifest**: Write `phase-3-executive-synthesis.json`; update phase 3 in `manifest.json`; refresh `updated_at`.

### Phase 4 — Strategy documents

Generate three focused strategy documents in Korean, sourcing content **only** from on-disk phase outputs (`phase-3-executive-synthesis.json`, and `phase-2-role-dispatch.json` if needed for citations — not from chat memory):

- Company-level: market positioning, competitive response, partnership opportunities
- Team-level: resource allocation, sprint priority adjustments, hiring signals
- Product-level: feature prioritization changes, technical debt priorities, customer-driven adjustments

Store structured sections plus markdown-ready bodies in `phase-4-strategy-documents.json`.

- **Persist & manifest**: Write `phase-4-strategy-documents.json`; update phase 4 in `manifest.json`; refresh `updated_at`.

### Phase 5 — Distribute

Post each document to Slack `#strategy` as threaded messages; optionally upload to Google Drive. Build messages **only** from `phase-4-strategy-documents.json` and `manifest.json` (verify phase 4 `completed`). Write delivery receipts, channel ids, thread timestamps, and Drive file ids to `phase-5-distribute.json`.

- **Persist & manifest**: Write `phase-5-distribute.json`; set phase 5 to `completed` (or `failed` with `error`); refresh `updated_at`.

## Composed Skills

- `role-dispatcher` — 12-role parallel analysis
- `executive-briefing` — Cross-role synthesis
- Slack MCP — Strategy channel posting
- `gws-drive` — Document archival (optional)

## Error Handling

| Error | Action |
|-------|--------|
| Insufficient day's intelligence (no inputs collected) | Write `phase-1-aggregate.json` with `status: insufficient_data`, list missing inputs in JSON, set manifest phase 1 `failed`; report from file contents |
| role-dispatcher partial failure (some roles timeout) | Persist partial results to `phase-2-role-dispatch.json`; note missing perspectives in that file; downstream phases read files only |
| Slack `#strategy` channel not found | Fall back to `#효정-할일`; record actual channel in `phase-5-distribute.json`; notify user of missing channel |
| executive-briefing produces empty synthesis | Persist available role blocks to `phase-3-executive-synthesis.json` with `fallback: individual_roles`; phase 4 reads this file and may format per-role posts |
| Google Drive upload fails | Record failure in `phase-5-distribute.json`; Slack-only delivery; skip Drive, note in manifest error fields if needed |

**Recovery**: If a phase fails, prior `phase-*.json` files under `outputs/daily-strategy-post/{date}/` remain valid checkpoints. Fix the issue and re-run from the failed phase after updating `manifest.json` for that phase to `pending` or `running`.

## Examples

```
User: "오늘 정리된 내용으로 전략 브리핑 만들어서 슬랙에 올려줘"
→ Init manifest → phase-1-aggregate.json → phase-2-role-dispatch.json → phase-3-executive-synthesis.json
  → phase-4-strategy-documents.json → phase-5-distribute.json (Slack reads only phase-4 + manifest)

User: "daily-strategy-post"
→ Full pipeline with outputs under outputs/daily-strategy-post/{date}/; final Slack text from files only
```


## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
