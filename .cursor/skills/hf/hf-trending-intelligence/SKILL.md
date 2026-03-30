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

## 출력 언어

**모든 출력물은 한국어로 작성한다.** 리포트(markdown), Slack 메시지, Notion 페이지, 인사이트 분석 모두 한글로 작성. 논문 제목, 모델명, 데이터셋명 등 고유명사는 원어 그대로 유지.

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
- **Topics** (default: `LLM, video-generation`): Topic filter using HF tags from `hf-topic-radar/references/topic-config.md`. Phase 1.5 (topic-focused model/space scan) runs by default with these topics. Pass `--skip-topics` to disable and revert to v1.0 paper-only behavior.
- **--leaderboard** (optional): 명시적으로 전달해야 Phase 2.5 (leaderboard cross-reference)가 실행된다. 디폴트로는 실행하지 않음.

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

### Phase 1.5 — Topic-Focused Model & Space Trending

**Activation:** Runs by default with topics `LLM, video-generation`. Skipped only when `--skip-topics` is explicitly passed.

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

### Phase 2.5 — Leaderboard Cross-Reference (Optional)

**Activation:** `--leaderboard` 플래그를 명시적으로 전달해야 실행된다. 디폴트로는 비활성화.

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

한국어로 구조화된 마크다운 리포트를 생성한다:

```markdown
# AI 리서치 레이더 — YYYY-MM-DD

## 요약
(오늘의 트렌드 2-3문장 요약)

## 트렌딩 TOP 5

### 1. [PAPER_TITLE] — HOT 🔥
- **점수:** 0.85
- **논문:** PAPER_ID (↑ UPVOTES 추천)
- **모델:** N개, 대표: MODEL_ID (X 다운로드)
- **데이터셋:** N개
- **커뮤니티:** N개 토론 진행 중
- **외부 반응:** N개 웹 언급, M개 GitHub 구현체
- **핵심 인사이트:** (이것이 왜 중요한지 1문장 분석)

## 모델 지형 변화
(부상 중인 모델과 하락 중인 모델)

## 데이터셋 공백
(논문은 있지만 학습 데이터가 부족한 연구 영역)

## 커뮤니티 시그널
(가장 활발한 토론과 떠오르는 논쟁)

## 실행 제언
(팀을 위한 권장 사항)
```

**Output:** `outputs/hf-trending/YYYY-MM-DD-radar.md` (한국어)

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

Post the report to Slack and Notion. **Slack 메시지는 반드시 한글로 작성한다.**

**Slack (#deep-research-trending):**

1. **Main message** — 논문 중심 Executive Summary:
```
🔬 HuggingFace 트렌딩 인텔리전스 리포트 | YYYY-MM-DD
수집 논문: N편 | 분석 범위: Top 10 크로스-레퍼런스, Top 5 웹 리서치

*Executive Summary*
YYYY-MM-DD HuggingFace 트렌딩 분석 결과, N가지 핵심 트렌드 부상:
🔥 *HOT* — {HOT 카테고리 요약}
🌡️ *WARM* — {WARM 카테고리 요약}
❄️ *COOL* — {COOL 카테고리 요약}

특히 {Top1_논문} ({upvotes} upvotes, score {score})은 {1문장 인사이트}, {Top2_논문} ({upvotes} upvotes, score {score})은 {1문장 인사이트}.
```

2. **Thread reply 1** — HOT 논문 상세:
   각 HOT 논문별 점수, upvotes, 관련 모델/데이터셋 수, 웹 반응 요약

3. **Thread reply 2** — 토픽 레이더 하이라이트 (Phase 1.5 결과):
   토픽별 트렌딩 모델/스페이스 상위 항목

4. **Thread reply 3** (optional, `--leaderboard` 시에만) — 리더보드 TOP 10

**Notion:**
Use `md-to-notion` to publish the full report (한국어) as a Notion page under the research parent.

**Output:** Slack thread + Notion page URL

## Output Summary

- **Intelligence Report** (markdown) — `outputs/hf-trending/YYYY-MM-DD-radar.md`
- **HF Collection** — monthly curated collection of HOT papers/models
- **Slack Thread** — in `#deep-research-trending`
- **Notion Page** — permanent archive

## Examples

### Example 1: Default radar (논문 + 토픽 레이더)

User says: "Run daily AI radar" or `/hf-trending`

Actions:
1. Run Phase 1 (paper scan — 30 papers)
2. Run Phase 1.5 (topic radar: LLM + video-generation)
3. Run Phase 2 (cross-reference — top 10 papers)
4. Skip Phase 2.5 (leaderboard — 디폴트 비활성)
5. Run Phase 3 (web enrichment — top 5 papers)
6. Run Phases 4-7 (scoring, report, curate, distribute)

Result: HOT/WARM/COOL 분류된 논문 중심 리포트 + 토픽별 트렌딩 모델/스페이스, Slack thread, Notion page

### Example 2: Custom topic override

User says: "HF 종합 트렌딩 — multi-LLM 중심으로" or `/hf-trending topics=multi-LLM`

Actions:
1. Run Phase 1 (paper scan)
2. Run Phase 1.5 (topic radar for multi-LLM only — overrides default)
3. Run Phase 2-3 (cross-reference + web enrichment)
4. Run Phases 4-7

Result: multi-modal LLM 중심 트렌드 리포트

### Example 3: Leaderboard 포함 모드

User says: `/hf-trending --leaderboard`

Actions:
1. Run Phase 1-1.5 (papers + topic radar)
2. Run Phase 2 (cross-reference)
3. Run Phase 2.5 (leaderboard cross-reference — 명시적 활성화)
4. Run Phases 3-7

Result: 논문 + 토픽 + 리더보드 랭킹 포함 풀 리포트

### Example 4: Legacy paper-only mode

User says: "AI research radar --skip-topics"

Actions:
1. Run Phase 1 (paper scan)
2. Skip Phase 1.5 and 2.5
3. Run Phases 2-7 normally

Result: 논문 전용 레이더 (v1.0 behavior)

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
