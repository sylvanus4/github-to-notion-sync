---
name: hf-leaderboard-tracker
description: >-
  Track AI model leaderboard rankings across Open LLM Leaderboard, Chatbot
  Arena, and video generation benchmarks. Detects rank changes, new entries, and
  category leaders by comparing against previous snapshots. Posts structured
  Slack threads to #deep-research-trending with highlighted movers. Use when the user asks
  to "check leaderboard rankings", "HF leaderboard", "model rankings",
  "leaderboard changes", "Open LLM Leaderboard", "Chatbot Arena rankings",
  "리더보드 추적", "모델 랭킹", "벤치마크 순위", "HF 리더보드", "leaderboard
  tracker", "rank movers", or wants to track AI model benchmark performance over
  time. Do NOT use for topic-focused trending scan (use hf-topic-radar). Do NOT
  use for the full daily AI radar pipeline (use hf-trending-intelligence). Do NOT
  use for general model search (use hf-models). Do NOT use for model evaluation
  execution (use hf-evaluation).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "research"
---

# Leaderboard Tracker — AI Model Benchmark Rankings

Track AI model leaderboard positions, detect rank changes and new entries,
and distribute structured delta reports to Slack.

## Prerequisites

- `hf` CLI installed and authenticated (see `hf-hub` skill)
- Slack MCP configured for posting (channel: `#deep-research-trending` — `C0AN34G4QHK`)
- `jq` for JSON processing

## Required Skills

- `hf-dataset-viewer` — fetch leaderboard results from HF datasets
- `defuddle` — extract leaderboard tables from web pages
- `kwp-slack-slack-messaging` — Slack distribution

## Reference Files

- `references/leaderboard-sources.md` — URLs, dataset IDs, and extraction strategies
- `references/report-template.md` — Slack and markdown report templates

## Input

- **Leaderboards** (optional): Which leaderboards to check (default: all from config)
- **Category** (optional): Filter by model category (e.g., "chat", "reasoning", "video")

## Pipeline Phases

### Phase 1 — Fetch Open LLM Leaderboard

The Open LLM Leaderboard publishes results as a HuggingFace dataset.

```bash
# Fetch the latest leaderboard results via dataset viewer API
# Dataset: open-llm-leaderboard/results
```

Use `hf-dataset-viewer` skill to query the dataset:
1. Fetch the first 100 rows sorted by average score descending
2. Extract: model name, average score, individual benchmark scores, parameter count, architecture
3. **Validate:** discard rows where model name is empty or score is null/NaN
4. Filter by user-specified category if provided
5. Assign rank numbers (1-based) after filtering and validation

**Output:** `llm_rankings[]` — `{rank, model, avg_score, params, architecture, scores{}}`

### Phase 2 — Fetch Chatbot Arena Rankings

Extract Chatbot Arena Elo rankings from `https://lmarena.ai/`.

Use `defuddle` to fetch the page content, then parse the ranking table:
1. Extract: model name, Elo rating, votes, organization
2. Sort by Elo rating descending
3. Assign rank numbers

If `defuddle` cannot extract structured data (dynamic JS), fall back to
`parallel-web-search` with query `"chatbot arena leaderboard rankings site:lmarena.ai 2026"`.

**Output:** `arena_rankings[]` — `{rank, model, elo, votes, org}`

### Phase 3 — Fetch Video Generation Leaderboard

For video generation benchmarks, query VBench or similar sources.

Strategy (in order of preference):
1. Check if a VBench dataset exists on HF: `hf datasets ls --search "vbench" --sort downloads -q --limit 5`
2. If dataset exists, use `hf-dataset-viewer` to fetch results
3. If no dataset, use `defuddle` on the VBench project page
4. Fall back: use `parallel-web-search` for `"video generation benchmark leaderboard 2026"`

**Output:** `video_rankings[]` — `{rank, model, score, metrics{}}`

### Phase 4 — Delta Detection

Compare current rankings against the previous snapshot stored in
`output/hf-leaderboard/`.

**Snapshot file format:** `output/hf-leaderboard/{LEADERBOARD}-latest.json`

```json
{
  "date": "2026-03-20",
  "leaderboard": "open-llm-leaderboard",
  "rankings": [...]
}
```

**Detection logic:**
1. Load previous snapshot (if exists)
2. For each current entry, find its previous rank by exact model name match
3. Classify changes:
   - **NEW**: model not in previous snapshot
   - **UP**: rank improved by 2+ positions (lower number)
   - **DOWN**: rank declined by 2+ positions
   - **STABLE**: rank unchanged (within ±1)
   - **SIGNIFICANT**: rank changed by 5+ positions in either direction
4. Compute `delta = previous_rank - current_rank` (positive = improved)

**Significance threshold:** Only changes of ±2 or more ranks are reported as
UP/DOWN. Changes of ±1 are treated as STABLE to avoid noise from minor
fluctuations. Changes of ±5 or more are flagged as SIGNIFICANT movers.

**First run handling:** If no previous snapshot exists, mark all entries as NEW
and save current data as the baseline. Report "Initial baseline established"
instead of delta analysis.

**Output:** `deltas[]` — `{model, current_rank, previous_rank, delta, status}`

### Phase 5 — Save Snapshots

Save current rankings as the new "latest" snapshot for future delta detection.

```
output/hf-leaderboard/open-llm-leaderboard-latest.json
output/hf-leaderboard/arena-latest.json
output/hf-leaderboard/video-gen-latest.json
```

Also save a dated archive copy:
```
output/hf-leaderboard/archive/{LEADERBOARD}-{DATE}.json
```

### Phase 6 — Report Generation

Generate a structured markdown report.

```markdown
# AI Leaderboard Tracker — {DATE}

## Summary
{1-2 sentences: leaderboards checked, notable movers, new entries}

## Open LLM Leaderboard

### Top 10
| Rank | Model | Avg Score | Params | Change |
|------|-------|-----------|--------|--------|
| 1 | {model} | {score} | {params}B | {status_icon} {delta} |

### Notable Movers
- {model}: #{old} -> #{new} ({delta_explanation})

### New Entries
- {model}: debuted at #{rank} ({score})

## Chatbot Arena
(same structure)

## Video Generation
(same structure)

## Cross-Leaderboard Insights
{Models performing well across multiple leaderboards}
```

**Output:** `output/hf-leaderboard/{DATE}-leaderboard-report.md`

### Phase 7 — Distribute to Slack

Post to `#deep-research-trending` (`C0AN34G4QHK`) as a threaded message.

**Main message:** Summary with biggest movers across all leaderboards

**Thread reply per leaderboard:**
- Top 5 models with scores
- New entries highlighted
- Biggest rank changes (up and down)

**"No changes" handling:** If all rankings are STABLE (within ±1) with no new
entries and no SIGNIFICANT movers (±5 ranks), do NOT post to Slack. Instead,
log "No significant leaderboard changes on {DATE}" and skip distribution.
This prevents Slack noise on quiet days.

Follow `references/report-template.md` for formatting.

## Output Summary

- **Leaderboard Report** (markdown) — `output/hf-leaderboard/{DATE}-leaderboard-report.md`
- **Snapshots** (JSON) — `output/hf-leaderboard/{LEADERBOARD}-latest.json`
- **Archive** (JSON) — `output/hf-leaderboard/archive/{LEADERBOARD}-{DATE}.json`
- **Slack Thread** — in `#deep-research-trending` (only when changes detected)

## Examples

### Example 1: First run (no previous snapshot)

User says: "HF 리더보드 체크해줘"

Actions:
1. Fetch all 3 leaderboards (Open LLM, Arena, Video Gen)
2. No previous snapshots found → establish baseline
3. Save snapshots to `output/hf-leaderboard/`
4. Post "Initial baseline established" to Slack with top 10 per leaderboard

Result: Baseline snapshots saved, future runs will detect changes

### Example 2: Delta detection run

User says: "Check leaderboard changes"

Actions:
1. Fetch current rankings from all leaderboards
2. Compare against previous snapshots
3. Detect: 2 new entries, 3 rank movers, 1 model dropped
4. Post detailed delta thread to Slack

Result: Report highlighting what changed since last check

### Example 3: No changes detected

User says: "leaderboard tracker"

Actions:
1. Fetch current rankings
2. Compare against previous snapshots
3. All entries STABLE, no new models
4. Save updated snapshots but skip Slack posting

Result: "No significant leaderboard changes" logged locally, no Slack noise

## Error Recovery

| Phase | Error | Recovery |
|-------|-------|----------|
| 1 | Dataset viewer API fails | Fall back to `defuddle` on leaderboard web page |
| 2 | Arena page not extractable | Use web search results; mark as "partial data" |
| 3 | No video benchmark found | Skip video section; note in report |
| 4 | No previous snapshot | Establish baseline; report as "initial run" |
| 5 | Cannot write snapshot | Log error; continue with Slack posting |
| 7 | Slack post fails | Save report locally; log error |
| 7 | No changes detected | Skip Slack; log "no changes" — not a failure |
