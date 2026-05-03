---
name: hf-topic-radar
description: >-
  Topic-focused HuggingFace trending scan that fetches trending models,
  spaces, and papers for user-configured AI topics (LLM, multi-LLM, video
  generation, etc.), deduplicates cross-source items, scores and ranks
  results, and posts structured Slack threads to #deep-research-trending. Use
  when the user asks to "scan HF for trending LLMs", "HF topic radar", "what's
  hot on HuggingFace for video generation", "HF 토픽 레이더", "허깅페이스 트렌딩", "HF 관심
  분야 트렌딩", "topic-focused HF scan", "run topic radar", or wants to know what's
  trending on HuggingFace in specific AI domains. Do NOT use for full paper
  review with PM analysis (use paper-review). Do NOT use for the full daily AI
  radar pipeline (use hf-trending-intelligence). Do NOT use for leaderboard
  rankings and benchmark scores (use hf-leaderboard-tracker). Do NOT use for
  general model search without trending context (use hf-models).
---

# Topic Radar — HuggingFace Trending by Topic

Scan HuggingFace Hub for trending models, spaces, and papers filtered by
configurable AI topics. Produces a deduplicated, scored report and distributes
to Slack.

## 출력 언어

**모든 출력물은 한국어로 작성한다.** 리포트(markdown), Slack 메시지 모두 한글로 작성. 모델명, 데이터셋명, 논문 제목 등 고유명사는 원어 그대로 유지.

## Prerequisites

- `hf` CLI installed and authenticated (see `hf-hub` skill)
- Slack MCP configured for posting (channel: `#deep-research-trending` — `C0AN34G4QHK`)
- `jq` for JSON processing

## Required Skills

- `hf-models` — trending model search
- `hf-spaces` — trending space search
- `hf-papers` — daily paper listing
- `kwp-slack-slack-messaging` — Slack distribution

## Reference Files

- `references/topic-config.md` — configurable topic list with HF tags and keywords
- `references/slack-format.md` — Slack thread message templates

## Input

- **Topics** (optional): Override default topics from `references/topic-config.md`
- **Date** (optional): Defaults to `today`
- **Limit** (optional): Number of items per source per topic (default: 10)

## Pipeline Phases

### Phase 1 — Model Scan

For each topic in `references/topic-config.md`, fetch trending models.

```bash
hf models ls --filter {hf_tag} --sort trending_score --limit 10 --format json
```

If multiple tags exist for a topic, run each tag query and merge results.

**Processing:**
1. Parse JSON; extract model ID, author/org, downloads, likes, trending score
2. Tag each result with its source topic
3. Collect all results into a unified models list

**Output:** `models[]` — list of `{id, author, downloads, likes, trending_score, topic}`

### Phase 2 — Space Scan

For each topic, fetch trending spaces.

```bash
hf spaces ls --search {keyword} --sort trending --limit 10 --format json
```

**Processing:**
1. Parse JSON; extract space ID, author/org, likes, SDK type
2. Tag each result with its source topic

**Output:** `spaces[]` — list of `{id, author, likes, sdk, topic}`

### Phase 3 — Paper Scan

Fetch today's trending papers and filter by topic keywords.

```bash
hf papers ls --date today --sort trending --limit 30 --format json
```

**Processing:**
1. Parse full paper list
2. For each topic, filter papers whose title or summary contains any of the topic's keywords
3. If a paper matches multiple topics, assign it to the topic with the most keyword hits

**Output:** `papers[]` — list of `{id, title, upvotes, authors, topic}`

### Phase 4 — Deduplication and Cross-Linking

Merge the three source lists to remove duplicate coverage of the same work.

**Dedup rules:**
1. Same author/org appearing across models, spaces, and papers → merge into a single "trend item"
2. Title similarity > 80% (case-insensitive, ignoring common stopwords) → merge
3. Paper ID referenced in a model card → link them

**Output:** `trend_items[]` — deduplicated items, each with:
- `primary_type`: `model` | `space` | `paper`
- `linked_items[]`: related items from other sources
- `topic`: assigned topic

### Phase 5 — Scoring

Score each trend item using an adapted version of the trending-intelligence rubric.

```
topic_score = (
  0.35 * normalize(primary_metric) +
  0.25 * normalize(cross_source_count) +
  0.20 * normalize(likes_or_upvotes) +
  0.20 * normalize(recency)
)
```

Where:
- `primary_metric`: downloads (model), likes (space), upvotes (paper)
- `cross_source_count`: number of linked items from other sources (0-3)
- `likes_or_upvotes`: combined likes/upvotes across all linked items
- `recency`: 1.0 if today, 0.8 if yesterday, 0.5 if this week, 0.2 otherwise

**Classification:**
- Score >= 0.7: **HOT**
- Score 0.4-0.69: **WARM**
- Score < 0.4: **COOL**

**Output:** Ranked `trend_items[]` with scores and labels, sorted by score descending within each topic group

### Phase 6 — Report Generation

Generate a structured markdown report. All items within each section MUST be
sorted by score descending (highest first).

**Completeness rule:** Every topic section MUST show all 3 source types even if
a source returned 0 results. Use "(0 models found)" rather than omitting the row.

```markdown
# HF 토픽 레이더 — {DATE}

## 요약
{스캔된 토픽, 총 항목 수, HOT 개수를 1-2문장으로 요약}
소스: 모델 {N}개, 스페이스 {N}개, 논문 {N}편 스캔

## {TOPIC_NAME}

### HOT 항목 (점수 내림차순)
| 순위 | 항목 | 유형 | 점수 | 주요 지표 | 연결 |
|------|------|------|------|----------|------|
| 1 | {item_id} | 모델 | 0.85 | 12K 다운로드 | 논문, 스페이스 |

### WARM 항목 (점수 내림차순)
(동일 테이블 형식)

## 교차 토픽 하이라이트
{여러 토픽에 걸쳐 등장하는 항목 — 수렴 트렌드 분석}

## 실행 제언
각 인사이트는 반드시 다음 구조를 따른다:
1. **[동사] [구체적 대상]** — [데이터 근거] → [기대 효과]
   예시: "Qwen3-VL 내부 활용 검토" — Multi-LLM 트렌딩 1위, 관련 논문 3편 → 문서 이해 30% 개선 가능

"계속 모니터링"이나 "이 분야는 성장 중" 같은 모호한 인사이트 금지.
```

**Output:** `outputs/hf-trending/{DATE}-topic-radar.md`

### Phase 7 — Distribute to Slack

Post to `#deep-research-trending` (`C0AN34G4QHK`) as a threaded message.

**Main message:** Summary line + HOT items count per topic

**Thread reply per topic:** Top 5 items with:
- Item name, type, score label
- Key metric (downloads/likes/upvotes)
- Cross-source links
- 1-sentence insight

**Final thread reply:** Cross-topic highlights and actionable insights

Follow `references/slack-format.md` for mrkdwn formatting.

## Output Summary

- **Topic Radar Report** (markdown) — `outputs/hf-trending/{DATE}-topic-radar.md`
- **Slack Thread** — in `#deep-research-trending`

## Examples

### Example 1: Default topic scan

User says: "HF 토픽 레이더 돌려줘"

Actions:
1. Load default topics (LLM, Multi-LLM, Video Generation) from `references/topic-config.md`
2. Run Phases 1-7 with all 3 topics
3. Post 4-message Slack thread: summary + 1 reply per topic

Result: Report at `outputs/hf-trending/2026-03-20-topic-radar.md`, Slack thread in #deep-research-trending

### Example 2: Single topic scan

User says: "What's hot on HuggingFace for video generation?"

Actions:
1. Parse "video generation" as the single topic
2. Run pipeline with only video generation tags/keywords
3. Post 2-message Slack thread: summary + video generation results

Result: Focused report with video-only trending models, spaces, and papers

### Example 3: Custom topic

User says: "Scan HF for trending audio models"

Actions:
1. Recognize "audio" as a custom topic not in config
2. Use HF tags `audio-classification`, `text-to-audio`, `automatic-speech-recognition`
3. Use keywords "audio", "speech", "TTS", "ASR"
4. Run full pipeline for this ad-hoc topic

Result: One-time audio-focused topic radar without modifying the config file

## Error Recovery

| Phase | Error | Recovery |
|-------|-------|----------|
| 1 | Model search returns empty | Skip topic for models; continue with spaces/papers |
| 2 | Space search returns empty | Continue with models/papers |
| 3 | No papers for today | Fall back to yesterday's papers |
| 4 | Dedup merges too aggressively | Log merge decisions; keep separate if similarity < 80% |
| 7 | Slack post fails | Save report locally; log error |
