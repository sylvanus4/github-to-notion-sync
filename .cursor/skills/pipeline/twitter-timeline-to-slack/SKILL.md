---
name: twitter-timeline-to-slack
description: >-
  Fetch the latest tweets from a Twitter/X user's profile, store locally with
  deduplication, classify each tweet by topic, and post to the appropriate Slack
  channel using the x-to-slack pipeline with rate limiting. Supports batch
  processing and resumable posting. Use when the user asks to "fetch tweets
  from timeline", "post timeline to slack", "twitter timeline", "scrape tweets",
  "twitter-timeline-to-slack", or wants to batch-process a user's tweets to
  Slack. Do NOT use for posting a single tweet URL (use x-to-slack). Do NOT use
  for general Slack messaging (use kwp-slack-slack-messaging). Do NOT use for
  Twitter scraping without Slack posting (use scrapling or agent-browser).
  Korean triggers: "타임라인", "트위터 타임라인", "트윗 일괄", "트윗 스크래핑".
metadata:
  author: "thaki"
  version: "2.2.0"
  category: "execution"
---
# Twitter Timeline to Slack Pipeline

Fetch a user's latest tweets, classify by topic, and post each to the appropriate Slack channel via the x-to-slack skill.

## Input

The user provides:
1. **Twitter screen name** (optional, default: `hjguyhan`) -- e.g. `someuser` or `@someuser`
2. **Options** (optional):
   - `--limit N` -- max tweets to post (default: all unposted)
   - `--dry-run` -- classify without posting
   - `--fetch-only` -- fetch and store only, no posting

When invoked without a screen name (e.g. `/twitter-timeline-to-slack` or "트위터 타임라인 슬랙에 올려줘"), default to `hjguyhan`.

## Prerequisites

- `TWITTER_COOKIE` must be set in `.env` (Twitter session cookie for Syndication API)
- Channel DB must exist at `outputs/twitter/slack-channels.json`

## Workflow

### Phase 0: Cookie Validation

Verify `TWITTER_COOKIE` is set and functional before fetching. If missing or expired, guide the user through interactive registration.

See [references/cookie-validation.md](references/cookie-validation.md) for the full validation and registration flow (Steps 0a-0c).

### Phase 0.5: Cross-Repo Dedup Sync

Before fetching and posting, load the central intelligence registry to filter out already-processed tweets across all repos and machines.

For each tweet URL that would be posted, check against the registry:

```bash
python3 "scripts/intelligence/intel_registry.py" check "<tweet_url>"
```

- **Exit 0 (new)**: Include in the batch for processing.
- **Exit 1 (duplicate)**: Mark as `skip_reason: "cross_repo_duplicate"` in tweets.json and skip.

If `intel_registry.py` is not found, log a warning and proceed without cross-repo dedup (graceful degradation). Local dedup via tweets.json still applies.

### Phase 1: Fetch Tweets

Run the fetch script to collect tweets:

```bash
cd scripts/twitter && node run_pipeline.js --fetch-only
```

The `--user` flag is supported to override the default screen name:

```bash
cd scripts/twitter && node run_pipeline.js --fetch-only --user someuser
```

This uses twittxr (Twitter Syndication API wrapper) to fetch up to 100 tweets. Falls back to FxTwitter API for individual tweet enrichment. If both twittxr and FxTwitter fail, try Agent-Reach Twitter channel: `twitter search "{screen_name}" --limit 20` (requires TWITTER_COOKIE configured via `agent-reach configure twitter`).

### Phase 2: Classify and Route

For each tweet, the classifier analyzes text content against keyword rules and routes to the best Slack channel. See [references/classification-rules.md](references/classification-rules.md) for the full rule set.

| Category | Target Channel | Strictness |
|----------|----------------|------------|
| AI Coding | `#ai-coding-radar` | Very strict — only Claude Code / Cursor practical tips |
| Prompt Engineering | `#prompt` | Moderate |
| Research | `#deep-research-trending` | Moderate — papers, models, benchmarks |
| Stock/Finance | `#효정-주식` | Moderate — crypto, stocks, macro, prediction markets |
| Ideas | `#idea` | Moderate — business insights, frameworks, patterns (absorbs business keywords from insight) |
| Insights | `#효정-insight` | Very strict — pure analysis, learning methods only (축소 운영) |
| Tasks | `#효정-할일` | Low |
| Image/Visual AI | `#효정-이미지` | Moderate — AI image/video/music generation, generative art |
| Press/News (DEFAULT) | `#press` | Broad — catch-all for everything else |

### Phase 2.5: Thread Deduplication and Context Loading

Before posting, read `outputs/twitter/{screen_name}/tweets.json` and check each unposted tweet's thread metadata:

- **Skip** tweets where `skip_reason === "thread_member"` — these are part of a thread that will be posted via the primary tweet.
- For tweets where `is_thread === true`, load the `thread` array and `thread_text` field. These contain the full self-reply chain (oldest-first) reconstructed by the pipeline.
- The `thread_text` field contains the combined text of all tweets in the thread, joined by `\n\n---\n\n`.

### Phase 3: Post via x-to-slack (Subagent-per-Tweet Dispatch)

**CRITICAL**: Each tweet MUST go through the complete x-to-slack workflow. Do NOT shortcut or summarize from raw tweet text alone.

#### Architecture: Fat Subagent Prompt Pattern

Each tweet is processed by a **dedicated Task subagent** with a fresh context window.
The orchestrator embeds the full quality contract (templates, formatting rules,
quality gates, examples) into each subagent prompt so quality is identical to
main-agent execution — without context window exhaustion.

**Why subagents work now:**
- Each subagent receives the **full quality contract** from
  [references/subagent-quality-contract.md](references/subagent-quality-contract.md)
- Each subagent gets a **fresh context window** — no degradation from prior tweets
- No batch limit needed — process all unposted tweets in one invocation
- File-first persistence: subagent writes results to disk, orchestrator reads them

#### Dispatch Loop

For each unposted tweet (newest first, excluding `skip_reason: "thread_member"`):

1. **Read** the quality contract file: `references/subagent-quality-contract.md`
2. **Prepare** tweet-specific input data (URL, FxTwitter URL, classified channel,
   channel_id, thread info, media info, output file path)
3. **Spawn** `Task(subagent_type="generalPurpose")` with:
   - The full quality contract text (embedded verbatim in the prompt)
   - Tweet-specific data as structured input
   - Output file path: `outputs/twitter/{screen_name}/results/tweet-{id}.json`
4. **Wait** for subagent completion
5. **Read** the result JSON from disk
6. **Validate** quality: check `quality_score.msg2_chars >= 800` and `msg3_chars >= 400`
   - If below thresholds, log a warning (do not re-dispatch — the fresh context
     means the subagent had optimal conditions)
7. **Update** `tweets.json` with posting status (Step 3f)
8. **Save** intelligence artifact (Step 3f-intel)
9. **Wait** 10-15 seconds before next tweet (rate limiting)

#### Subagent Return Contract

Each subagent writes a JSON file to the specified output path:

```json
{
  "status": "completed|failed|skipped",
  "file": "outputs/twitter/.../tweet-{id}.json",
  "summary": "one-line Korean outcome description",
  "slack_ts": "message_ts from Message 1 (if posted)",
  "quality_score": {
    "msg1_chars": 150,
    "msg2_chars": 1200,
    "msg3_chars": 600,
    "websearch_count": 3,
    "media_uploaded": true
  },
  "tweet_url": "<original tweet URL>",
  "channel": "<channel name>",
  "posted_at": "<ISO timestamp>"
}
```

The manifest from Phase 2 provides pre-computed fields for each tweet:
- `has_media` / `media_type` / `media_url` — pre-extracted best media URL from tweets.json
- `classified_channel` / `classified_topic` — from Phase 2 classification
- `is_thread` / `thread_text` / `thread_count` — thread metadata

### Orchestrator Post-Dispatch Responsibilities

After each subagent completes and writes its result JSON to disk, the orchestrator
performs the following steps before dispatching the next tweet.

#### Step 3f: Update Local DB

After successful posting, update `tweets.json` (ALL fields are MANDATORY):
- Set `status` to `"posted"` (CRITICAL — without this, the tweet will be reprocessed and posted again)
- Set `posted_to_slack: true`
- Set `slack_channel` to the channel name
- Set `slack_ts` to the `message_ts` from Message 1
- Set `classified_topic` to the classification result
- Set `posted_at` to current ISO timestamp

**WARNING**: If `status` remains `"pending"` while `posted_to_slack` is `true`, the pipeline will treat the tweet as unprocessed and post it again, causing duplicates.

#### Step 3f-intel: Intelligence Artifact Save (after local DB update)

After updating tweets.json, save an intelligence artifact to the research repo and register the URL in the central dedup registry.

1. Generate a markdown artifact with YAML frontmatter (url, author, date, channel, topic) and the full Message 2 + Message 3 content.
2. Save and register via:

```bash
python3 "scripts/intelligence/intel_registry.py" save \
  "{tweet_url}" "/tmp/timeline-{tweet_id}.md" \
  --type tweet \
  --channel "{channel_name}" \
  --ts "{message_ts}" \
  --topic intelligence
```

If `intel_registry.py` is not found, log a warning and skip (graceful degradation). The Slack post is already complete.

### Subagent Internal Processing (reference only)

Each Task subagent autonomously performs the full per-tweet workflow.
The authoritative specification is in [references/subagent-quality-contract.md](references/subagent-quality-contract.md).

Summary of subagent responsibilities:
- **FxTwitter API enrichment**: Fetch full tweet data; for threads, also fetch root tweet
- **Web Research**: 2-3 mandatory WebSearch queries per tweet
- **Topic classification**: Determine Message 3 variant (AI GPU Cloud vs topic-specific)
- **Slack channel lookup**: Resolve channel_id from classified channel name
- **3-message Slack thread**: Post Message 1 (title), media upload, Message 2 (analysis), Message 3 (insights)
- **Quality self-check**: Verify character minimums (msg2 >= 800, msg3 >= 400) and section completeness
- **Decision extraction**: Post to decision channels when warranted (skip if `skip-decisions`)
- **Long-form detection**: Auto-invoke x-to-notion for long content (skip if `skip-notion`)

### Quality Gate

Quality enforcement is embedded in each subagent prompt via the quality contract.
The orchestrator validates returned `quality_score` metrics after each subagent completes:
- `msg2_chars >= 800` and `msg3_chars >= 400` — if below, log a warning
- `websearch_count >= 2` — if below, log a warning

See [references/quality-enforcement.md](references/quality-enforcement.md) for
BAD vs GOOD output examples.

### Phase 4: Local Storage

Tweets are stored with deduplication at `outputs/twitter/{screen_name}/tweets.json`. Each tweet tracks: `id`, `url`, `text`, `created_at`, `posted_to_slack`, `slack_channel`, `classified_topic`, `is_thread`, `thread`, `thread_text`, `thread_member_of`, `skip_reason`, `media`.

Thread-related fields:
- `is_thread` (boolean) -- true when tweet is part of a self-reply chain with 2+ tweets
- `thread` (array|null) -- ordered list of `{id, text, created_at, url}` objects, oldest first
- `thread_text` (string|null) -- combined text of all thread tweets, joined by `\n\n---\n\n`
- `thread_member_of` (string|null) -- ID of the primary tweet when this tweet was deduped
- `skip_reason` (string|null) -- `"thread_member"` when this tweet was skipped due to dedup

Daily snapshots are archived to `outputs/twitter/{screen_name}/archive/YYYY-MM-DD.json`.

## Running the Pipeline

### Execution Flow

```
Phase 1:   node scripts/twitter/run_pipeline.js --fetch-only
           → tweets.json updated with new tweets

Phase 2:   run_pipeline.js classifies each unposted tweet using classify_tweet.js rules
           (uses thread_text for classification when available)

Phase 2.5: run_pipeline.js deduplicates thread members
           → thread member tweets marked skip_reason: "thread_member"
           → only primary tweet (longest chain) kept per thread

Phase 3:   For EACH unposted tweet (excluding thread members):
           → Orchestrator reads subagent-quality-contract.md
           → Orchestrator spawns Task subagent with fat prompt + tweet data
           → Subagent performs full workflow autonomously (fresh context):
               FxTwitter enrichment → WebSearch → 3-message Slack thread → quality self-check
           → Subagent writes result JSON to outputs/twitter/{screen_name}/
           → Orchestrator reads result file, validates quality_score
           → Orchestrator updates tweets.json (status, slack_ts)
           → Orchestrator waits 10-15s (rate limit) before next subagent
```

### Script Commands

```bash
cd scripts/twitter

# Fetch tweets from timeline (Phase 1 only, default: @hjguyhan)
node run_pipeline.js --fetch-only

# Fetch for a different user
node run_pipeline.js --fetch-only --user someuser

# Fetch + classify without posting (dry run)
node run_pipeline.js --dry-run

# Full pipeline with limit
node run_pipeline.js --limit 5
```

## Examples

### Example 1: First run

User says: "hjguyhan 타임라인 트윗 슬랙에 올려줘"

Actions:
1. Run `node scripts/twitter/run_pipeline.js --fetch-only` to fetch tweets
2. Read `outputs/twitter/hjguyhan/tweets.json` for unposted tweets
3. Classify each tweet by topic → determine target channel
4. Read `references/subagent-quality-contract.md` for subagent prompt template
5. For each unposted tweet, dispatch a Task subagent with the fat prompt + tweet data
   → Subagent autonomously: FxTwitter enrichment → WebSearch → 3-message Slack thread
   → Subagent writes result JSON to disk
6. Orchestrator reads each result file, validates quality_score, updates tweets.json
7. Wait 10-15s between subagent dispatches (rate limiting)

### Example 2: Expected output quality

For a tweet like `https://x.com/altryne/status/2032223053116260367`:

**Message 1 (channel post):**
```
*:robot_face: Autoresearch — Shopify CEO가 20년 된 Liquid 엔진을 53% 빠르게 만든 AI 코딩 에이전트 사례*

Karpathy의 자율 실험 루프로 parse+render 53% 단축, 오브젝트 할당 61% 감소 달성
https://x.com/altryne/status/2032223053116260367
```

**Message 2 (thread reply) — MUST include all sections:**
```
*Tweet 요약*
- 작성자: @altryne (Alex Volkov) — @thursdai_pod 호스트, @wandb AI Evangelist
- 반응: ❤️ 2,240 | 🔁 106 | 👀 373K
- 작성일: 2026-03-12

*핵심 내용*
Alex Volkov이 Shopify CEO Tobi Lütke가 Andrej Karpathy의 Autoresearch 기법을
사용해 20년 된 프로덕션 템플릿 엔진(Liquid)의 성능을 51% 개선한 사례를 소개.
"이것이 모든 곳에 적용되면 진정한 foom(폭발적 성장)이 온다"고 평가.

*인용 트윗 (@tobi — Shopify CEO)*
Liquid 코드베이스에 /autoresearch를 실행한 결과:
• parse+render 시간 *53% 단축* (7,469 → 3,534μs)
• 오브젝트 할당 *61% 감소* (62,620 → 24,530)
• 약 120개 자동 실험 중 93개 커밋 생존, 974개 유닛 테스트 모두 통과

*추가 조사 결과*
- *Autoresearch란?*: Karpathy가 2026년 3월 초 공개한 프레임워크.
  AI 에이전트가 자율적으로 코드 수정 → 벤치마크 → 유지/폐기를 반복하는
  hill-climbing 루프
- *주요 최적화 기법*: StringScanner를 String#byteindex로 교체(파싱 40% 향상),
  정수 0-999 사전 계산으로 렌더당 267개 할당 절감
- *Liquid의 규모*: 560만 개 Shopify 스토어를 구동하는 Ruby 템플릿 엔진.
  GC가 전체 CPU 시간의 74%를 차지

*참고 링크*
- <https://github.com/karpathy/autoresearch|Karpathy autoresearch GitHub>
- <https://simonwillison.net/2026/Mar/13/liquid/|Simon Willison 분석>
- <https://awesomeagents.ai/news/shopify-ceo-ai-agent-liquid-engine-53-faster/|Awesome Agents 기사>
```

**Message 3 (thread reply) — topic-specific, NOT generic:**
```
*AI 코딩 에이전트 성능 최적화 인사이트*

이 사례는 AI 코딩 에이전트의 활용 패러다임이 "코드 생성"에서 "자율 성능 엔지니어링"으로
확장되고 있음을 보여줍니다.

*핵심 시사점*
- *Autoresearch 패턴의 보편화*: "측정 가능한 메트릭 + 자동 실험 루프"라는
  공식이 많은 도메인에 적용 가능
- *인간 전문가가 놓친 최적화를 AI가 발견*: 하나하나는 단순하지만 조합 효과가 53%
- *안전성 검증*: 974개 테스트 전체 통과 — 자동화된 테스트가 에이전트의 안전망

*Action Items*
- 우리 코드베이스에서 autoresearch 패턴 적용 가능성 탐색
- 필수 조건 확인: 결정적 평가 메트릭 + 테스트 스위트 + Git 롤백
- Tobi도 "오버핏 가능성" 언급 — 프로덕션 검증 필수
```

### Example 3: Thread tweet posting

A user posted a 2-tweet thread. Both tweets appear in the timeline:
- Root: `https://x.com/quantscience_/status/2032849534397649025` — "This is wild. Someone just open-sourced a 1-person Wall Street AI agent..."
- Reply: `https://x.com/quantscience_/status/2032849537975357665` — "Get it here: https://github.com/TraderAlice/OpenAlice..."

After `run_pipeline.js`:
- The reply tweet has `is_thread: true`, `thread: [{root}, {reply}]`, `thread_text: "combined..."`
- The root tweet is marked `skip_reason: "thread_member"` (deduped — reply has the longer chain)
- Only the reply tweet appears in the manifest

**Message 1 (channel post):**
```
*:chart_with_upwards_trend: OpenAlice — 월가 AI 에이전트를 1인 오픈소스로 구현한 풀스택 트레이딩 시스템*

리서치, 퀀트, 트레이딩, 리스크 관리 에이전트를 100% 오픈소스로 공개
https://x.com/quantscience_/status/2032849537975357665
```

**Message 2 (thread reply — thread variant):**
```
*Tweet 요약*
- 작성자: @quantscience_ (QuantScience) — 퀀트 트레이딩 & AI 콘텐츠 크리에이터
- 반응: ❤️ 1,082 | 🔁 158 | 👀 27,906 _(루트 트윗 기준)_
- 작성일: 2026-03-14
- 📎 스레드: 2개 트윗

*스레드 전문*
1️⃣ This is wild.

Someone just open-sourced a 1-person Wall Street AI agent that comes with:

- Research Desk
- Quant team
- Trading floor
- Risk Management

100% open source:

2️⃣ Get it here: https://github.com/TraderAlice/OpenAlice

🚨Still trading manually in 2026?

You're not alone. But the window to change that is closing.

*핵심 내용*
누군가가 월스트리트 수준의 1인 AI 트레이딩 에이전트를 완전히 오픈소스로 공개했다.
리서치 데스크, 퀀트 팀, 트레이딩 플로어, 리스크 관리 기능을 모두 갖춘 풀스택 시스템.
GitHub repo: TraderAlice/OpenAlice

*추가 조사 결과*
- *OpenAlice 프로젝트*: LLM 기반 자율 트레이딩 에이전트 프레임워크.
  멀티에이전트 아키텍처로 각 역할(리서치, 퀀트, 트레이딩, 리스크)을 분리
- *1인 월스트리트 트렌드*: AI로 개인 트레이더가 기관급 인프라를 구축하는 흐름 가속화

*참고 링크*
- <https://github.com/TraderAlice/OpenAlice|OpenAlice GitHub>
- <https://...|관련 기사>
```

### Example 4: Default invocation (no screen name)

User says: "/twitter-timeline-to-slack" or "트위터 타임라인 슬랙에 올려줘"

Actions:
1. Default to `hjguyhan` (no screen name needed)
2. Phase 0: Check TWITTER_COOKIE in `.env` → if missing/expired, run cookie registration
3. Run fetch — only new tweets added (existing IDs skipped)
4. Only unposted tweets are processed through Phase 3 (thread members with `skip_reason` are excluded)
5. Previously posted tweets are not re-posted

## Error Handling

- **TWITTER_COOKIE missing or expired**: Trigger Phase 0 cookie registration flow — guide user to copy cookie from browser and save to `.env`
- **twittxr API failure**: Log error, try Agent-Reach Twitter channel (`twitter timeline {screen_name} --limit 20`) as fallback. Continue with existing tweets in DB if both fail.
- **FxTwitter fetch failure**: Use raw tweet data from twittxr as fallback. If twittxr data is also unavailable, try `twitter read {tweet_id}` via agent-reach.
- **Slack channel not found**: Skip tweet, log warning
- **Rate limit**: Configurable via `TWEET_POST_DELAY_MS` env var (default: 12000ms)

## Composed Skills

This skill orchestrates:
- **x-to-slack** -- Quality contract reference for per-tweet processing. Each tweet is dispatched to a Task subagent that follows the x-to-slack workflow autonomously with a fresh context window.
- **scrapling** or **agent-browser** -- Fallback for tweet fetching if twittxr fails

## Decision Channels

| Channel | ID | Scope |
|---|---|---|
| `효정-의사결정` | `C0ANBST3KDE` | Personal decisions (tool adoption, portfolio) |
| `7층-리더방` | `C0A6Q7007N2` | Team/CTO decisions (infra, strategy, competitive) |

Step 3g uses these channels. See [references/decision-template.md](references/decision-template.md) for the full decision routing rules.

## Slack Posting Identity

Text messages are posted via `scripts/slack_post_message.py` (uses `SLACK_USER_TOKEN`) so they appear from the user, not the RandomGame Slack app. Media uploads continue to use `scripts/slack_upload_file.py`. The subagent quality contract already enforces this rule. See `.cursor/rules/slack-posting-identity.mdc` for the global policy.

## MCP Tool Reference

| Tool | Server | Purpose |
|---|---|---|
| `slack_search_channels` | `plugin-slack-slack` | Find channel_id by name |
| `slack_read_channel` | `plugin-slack-slack` | Fallback to find message_ts |
| `scripts/slack_post_message.py` | Shell (`SLACK_USER_TOKEN`) | Post text messages and thread replies as user identity |
| `scripts/slack_upload_file.py` | Shell (direct Slack API) | Upload media files to Slack via `files.uploadV2` |

## File Structure

```
.cursor/skills/pipeline/twitter-timeline-to-slack/
  SKILL.md                          # This orchestrator skill
  references/
    subagent-quality-contract.md    # Fat subagent prompt template (templates, rules, examples)
    quality-enforcement.md          # Legacy quality reference (absorbed into subagent contract)
    decision-template.md            # Decision channel routing rules

scripts/twitter/
  fetch_timeline.js           # Tweet fetcher (twittxr + FxTwitter fallback)
  classify_tweet.js           # Topic classifier with keyword rules
  run_pipeline.js             # Fetch + classify orchestration (Phase 1-2 only)
  enrich_and_manifest.js      # FxTwitter enrichment + manifest generation
  upload_media_to_slack.js    # Download media from URL + upload to Slack thread
  package.json                # Dependencies

outputs/twitter/
  slack-channels.json     # Channel ID registry
  {screen_name}/
    tweets.json           # Main tweet DB with posting status
    results/              # Per-tweet subagent result JSONs
    archive/              # Daily snapshots
```


## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
