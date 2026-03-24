---
name: hf-trending-intelligence
description: >-
  Autonomous daily intelligence pipeline that cross-references HF papers,
  models, datasets, spaces, leaderboards, and community activity to detect
  emerging AI trends before they go mainstream. Supports optional topic filtering
  (LLM, multi-LLM, video-generation, etc.) for focused scans. Produces a scored
  intelligence report and distributes to Slack + Notion. Use when the user asks
  to "run daily AI radar", "trending intelligence", "AI research radar", "detect
  AI trends", "daily paper intelligence", "AI 트렌드 레이더", "일일 AI
  인텔리전스", "트렌딩 분석", "연구 레이더", "HF 종합 트렌딩", or wants to know
  what's trending across the HF ecosystem today. Do NOT use for full paper review
  with PM analysis (use paper-review). Do NOT use for daily stock analysis (use
  today). Do NOT use for general web research only (use parallel-web-search). Do
  NOT use for paper browsing without cross-referencing (use hf-papers). Do NOT
  use for topic-only scan without full cross-referencing (use hf-topic-radar). Do
  NOT use for leaderboard-only tracking (use hf-leaderboard-tracker).
metadata:
  author: "thaki"
  version: "2.0.0"
  category: "research"
---

# Trending Intelligence — Daily AI Research Radar

Autonomous daily pipeline that detects emerging AI trends by cross-referencing
papers, models, datasets, and community buzz on Hugging Face Hub.

## Prerequisites

- `hf` CLI installed and authenticated (see `hf-hub` skill)
- Slack MCP configured for posting (channel: `#deep-research-trending` — `C0AN34G4QHK`)
- Notion MCP configured for page creation
- `jq` for JSON processing

## Required Skills

- `hf-papers` — daily paper listing
- `hf-models` — model search and info
- `hf-spaces` — trending space search
- `hf-collections` — curate trending items
- `hf-discussions` — measure community activity
- `hf-dataset-viewer` — dataset info
- `hf-topic-radar` — topic-focused model/space scanning (composable sub-skill)
- `hf-leaderboard-tracker` — leaderboard cross-reference data
- `parallel-web-search` — external signal enrichment
- `md-to-notion` — permanent Notion archive
- `kwp-slack-slack-messaging` — Slack distribution

## Reference Files

- `references/scoring-rubric.md` — composite scoring weights and thresholds
- `references/report-template.md` — intelligence report markdown template
- `references/collection-naming.md` — naming convention for monthly collections

## Input

- **Date** (optional): Defaults to `today`; can specify a specific date
- **Focus area** (optional): Filter by domain (e.g., "NLP", "vision", "multimodal")
- **Topics** (optional): Topic filter using HF tags from `hf-topic-radar/references/topic-config.md`. When specified, adds Phase 1.5 (topic-focused model/space scan) and Phase 2.5 (leaderboard cross-reference). Without this parameter, behavior is identical to v1.0.

## Pipeline Phases

### Phase 1 — Paper Scan

Fetch today's trending papers from HF Hub.

```bash
hf papers ls --date today --sort trending --limit 30 --format json
```

**Processing:**
1. Parse JSON response
2. Extract paper IDs, titles, upvote counts, authors
3. Generate keyword lists from each paper title for cross-referencing
4. If focus area specified, filter papers by keyword relevance

**Output:** List of 30 papers with IDs, titles, keywords, and upvote counts

### Phase 1.5 — Topic-Focused Model & Space Trending (Conditional)

**Activation:** Only runs when `topics` parameter is provided.

Invoke `hf-topic-radar` as a composable sub-skill, running Phases 1-5 only
(model scan, space scan, paper filter, dedup, scoring). Skip Phase 6-7
(report/Slack) — those are handled by this skill's own distribution phase.

```
topic_results = hf-topic-radar(topics=user_topics, date=date, distribute=false)
```

**Processing:**
1. Collect topic radar's `trend_items[]` output
2. Cross-reference with Phase 1 papers: link topic radar items to papers by
   author/org or keyword overlap
3. Add topic-tagged items to the main pipeline for scoring in Phase 4

**Output:** Additional scored items tagged with topics, merged into the main pipeline

### Phase 2 — Cross-Reference (Parallel)

For each of the top 10 papers, run 3 parallel searches to measure ecosystem impact.

**Subagent 1 — Model Association:**
```bash
hf models ls --search "PAPER_KEYWORDS" --sort downloads -q --limit 10
```
Count how many models reference or implement this paper's technique.

**Subagent 2 — Dataset Association:**
```bash
# Use hf-dataset-viewer to check if related datasets exist
# Search by paper keywords
hf datasets ls --search "PAPER_KEYWORDS" --sort downloads -q --limit 10
```
Count associated datasets.

**Subagent 3 — Community Buzz:**
For repos associated with top papers:
```bash
hf discussions list REPO_ID --status open --format json
```
Count open discussions as a proxy for community engagement.

**Constraint:** Max 4 concurrent subagents.

**Output per paper:** `{model_count, dataset_count, discussion_count}`

### Phase 2.5 — Leaderboard Cross-Reference (Conditional)

**Activation:** Only runs when `topics` parameter is provided.

Check if `hf-leaderboard-tracker` has recent snapshot data in
`output/hf-leaderboard/`. If snapshots exist and are less than 7 days old,
cross-reference top papers and models with leaderboard positions.

**Processing:**
1. Load latest snapshots from `output/hf-leaderboard/*-latest.json`
2. For each top-scoring paper/model from Phase 2, check if it appears on any
   leaderboard
3. If found: add leaderboard rank and score to the item's metadata
4. Flag items that are both trending AND top-ranked on leaderboards as
   "leaderboard-validated" — these get a scoring bonus in Phase 4

**Scoring bonus:** Items appearing on a leaderboard get +0.10 to their
final trend score (capped at 1.0).

**Output:** Enriched items with optional `leaderboard_rank` and `leaderboard_score` fields

### Phase 3 — Web Enrichment

For the top 5 papers by upvotes, search the wider web for external signals.

Use `parallel-web-search` skill with queries:
- `"PAPER_TITLE" site:twitter.com OR site:x.com`
- `"PAPER_TITLE" blog post 2026`
- `"PAPER_TITLE" github implementation`

**Processing:**
1. Count external mentions per paper
2. Identify notable reactions (industry leaders, major labs)
3. Flag papers with implementations on GitHub

**Output per paper:** `{web_mentions, github_repos, notable_reactions[]}`

### Phase 4 — Trend Scoring

Compute a composite score for each paper:

```
trend_score = (
  0.30 * normalize(paper_upvotes) +
  0.20 * normalize(model_downloads) +
  0.20 * normalize(dataset_activity) +
  0.15 * normalize(discussion_count) +
  0.15 * normalize(web_mentions)
)
```

See `references/scoring-rubric.md` for normalization rules and thresholds.

**Classification:**
- Score >= 0.7: **HOT** — likely to become mainstream within 2 weeks
- Score 0.4-0.7: **WARM** — emerging, worth monitoring
- Score < 0.4: **COOL** — early stage, low ecosystem impact

**Output:** Ranked list of papers with scores and classifications

### Phase 5 — Intelligence Report

Generate a structured markdown report:

```markdown
# AI Research Radar — YYYY-MM-DD

## Executive Summary
(2-3 sentence overview of today's trends)

## Top 5 Emerging Trends

### 1. [PAPER_TITLE] — HOT 🔥
- **Score:** 0.85
- **Paper:** PAPER_ID (↑ UPVOTES upvotes)
- **Models:** N models, top: MODEL_ID (X downloads)
- **Datasets:** N datasets
- **Community:** N open discussions
- **External:** N web mentions, M GitHub implementations
- **Key Insight:** (1-sentence analysis of why this matters)

## Model Landscape Shifts
(Models gaining or losing traction)

## Dataset Gaps
(Research areas with papers but no training data)

## Community Signals
(Most active discussions and emerging debates)

## Actionable Insights
(Recommendations for the team)
```

**Output:** `output/hf-intelligence/YYYY-MM-DD-radar.md`

### Phase 6 — Curate

Maintain a running HF collection for monthly trends.

```bash
# Create monthly collection if it doesn't exist
COLLECTION_SLUG=$(hf collections ls --owner hyojunguy --search "trending-$(date +%Y-%m)" -q | head -1)
if [ -z "$COLLECTION_SLUG" ]; then
  hf collections create "AI Trends $(date +%Y-%m)" \
    --description "Auto-curated trending papers and models" \
    --namespace hyojunguy
fi

# Add HOT papers to the collection
hf collections add-item "$COLLECTION_SLUG" PAPER_ID paper --note "Score: 0.85 — HOT"
```

**Output:** Updated monthly collection with new HOT items

### Phase 7 — Distribute

Post the report to Slack and Notion.

**Slack (#deep-research-trending):**
1. Main message: Executive summary with top 3 trends
2. Thread reply 1: Full trend list with scores
3. Thread reply 2: Actionable insights and dataset gaps

**Notion:**
Use `md-to-notion` to publish the full report as a Notion page under the research parent.

**Output:** Slack thread + Notion page URL

## Output Summary

- **Intelligence Report** (markdown) — `output/hf-intelligence/YYYY-MM-DD-radar.md`
- **HF Collection** — monthly curated collection of HOT papers/models
- **Slack Thread** — in `#deep-research-trending`
- **Notion Page** — permanent archive

## Examples

### Example 1: Default radar (no topic filter)

User says: "Run daily AI radar"

Actions:
1. Run Phases 1-7 (paper scan → cross-reference → web enrichment → scoring → report → curate → distribute)
2. Skip Phase 1.5 and 2.5 (no topics specified)
3. Behavior identical to v1.0

Result: Full radar report with top trending papers, Slack thread, Notion page

### Example 2: Topic-enhanced radar

User says: "HF 종합 트렌딩 — LLM, video generation 중심으로"

Actions:
1. Run Phase 1 (paper scan)
2. Run Phase 1.5 (topic radar for LLM + video generation)
3. Run Phase 2 (cross-reference)
4. Run Phase 2.5 (leaderboard cross-reference using cached snapshots)
5. Items appearing on leaderboards get +0.10 scoring bonus
6. Run Phases 3-7 with enriched data

Result: Enhanced report with topic-tagged items, leaderboard-validated trends, richer insights

### Example 3: Focused area without topic tags

User says: "AI research radar focused on NLP"

Actions:
1. Run Phase 1 with focus_area="NLP" (keyword filter on papers)
2. Skip Phase 1.5 (no topics parameter, only focus_area)
3. Run Phases 2-7 normally

Result: Paper-centric radar filtered by NLP keywords, no model/space topic scan

## Error Recovery

| Phase | Error | Recovery |
|-------|-------|----------|
| 1 | No papers for today | Fall back to yesterday; report "no papers today" |
| 2 | Cross-reference search fails | Continue with available data; mark missing dimensions |
| 3 | Web search rate-limited | Skip web enrichment; score with 4 dimensions only |
| 4 | All scores below threshold | Report "quiet day" with top papers by upvotes only |
| 6 | Collection create fails | Continue without curation; log error |
| 7 | Slack post fails | Save report locally; retry in next run |
| 7 | Notion upload fails | Save report locally; manual upload later |
