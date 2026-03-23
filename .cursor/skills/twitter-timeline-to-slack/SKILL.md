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
  version: "2.1.0"
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

See [references/cookie-validation.md](references/cookie-validation.md) for the full validation and registration flow (Steps 0a–0c).

### Phase 1: Fetch Tweets

Run the fetch script to collect tweets:

```bash
cd scripts/twitter && node run_pipeline.js --fetch-only
```

The `--user` flag is supported to override the default screen name:

```bash
cd scripts/twitter && node run_pipeline.js --fetch-only --user someuser
```

This uses twittxr (Twitter Syndication API wrapper) to fetch up to 100 tweets. Falls back to FxTwitter API for individual tweet enrichment.

### Phase 2: Classify and Route

For each tweet, the classifier analyzes text content against keyword rules and routes to the best Slack channel. See [references/classification-rules.md](references/classification-rules.md) for the full rule set.

| Category | Target Channel | Strictness |
|----------|----------------|------------|
| AI Coding | `#ai-coding-radar` | Very strict — only Claude Code / Cursor practical tips |
| Prompt Engineering | `#prompt` | Moderate |
| Research | `#deep-research` | Moderate — papers, models, benchmarks |
| Stock/Finance | `#효정-주식` | Moderate — crypto, stocks, macro, prediction markets |
| Ideas | `#idea` | Moderate — business insights, frameworks, patterns (absorbs business keywords from insight) |
| Insights | `#효정-insight` | Very strict — pure analysis, learning methods only (축소 운영) |
| Tasks | `#효정-할일` | Low |
| Press/News (DEFAULT) | `#press` | Broad — catch-all for everything else |

### Phase 2.5: Thread Deduplication and Context Loading

Before posting, read `outputs/twitter/{screen_name}/tweets.json` and check each unposted tweet's thread metadata:

- **Skip** tweets where `skip_reason === "thread_member"` — these are part of a thread that will be posted via the primary tweet.
- For tweets where `is_thread === true`, load the `thread` array and `thread_text` field. These contain the full self-reply chain (oldest-first) reconstructed by the pipeline.
- The `thread_text` field contains the combined text of all tweets in the thread, joined by `\n\n---\n\n`.

### Phase 3: Post via x-to-slack (FULL workflow per tweet)

**CRITICAL**: Each tweet MUST go through the complete x-to-slack workflow. Do NOT shortcut or summarize from raw tweet text alone.

#### EXECUTION CONSTRAINT (CRITICAL — READ BEFORE PROCEEDING)

Phase 3 MUST be executed by the MAIN agent — NOT delegated to subagents via
the Task tool. Subagents produce drastically lower quality because they lack:
- The full message templates and formatting rules
- Quality gate context and character count minimums
- WebSearch depth and follow-up capability
- Access to the reference examples that define expected output quality

If you find yourself wanting to use the Task tool to "process tweets in parallel"
or "handle each tweet via subagent" — STOP. This is the #1 cause of quality
degradation. Process each tweet yourself, sequentially, in the main context.

**Prohibited patterns:**
- `Task tool` with prompt "process this tweet" or "post tweet to Slack"
- Batching multiple tweets into a single subagent prompt
- Summarizing tweet content without FxTwitter enrichment + WebSearch
- Producing Message 2 shorter than 800 characters or Message 3 shorter than 400 characters

#### BATCH LIMIT

Process a maximum of **5 tweets per invocation**. This prevents context window
exhaustion which causes quality degradation in later tweets.

- If more than 5 unposted tweets exist, process the 5 oldest first
- After completing 5 tweets, report: "5/N tweets processed. Re-invoke
  `/twitter-timeline-to-slack` to continue with the next batch."
- Always pass `--limit 5` to `run_pipeline.js` unless the user explicitly
  requests more via `--limit N`
- The user can override with `--limit N` but quality may degrade beyond 7

The manifest from Phase 2 provides pre-computed fields for each tweet:
- `has_media` / `media_type` / `media_url` — pre-extracted best media URL from tweets.json
- `classified_channel` / `classified_topic` — from Phase 2 classification
- `is_thread` / `thread_text` / `thread_count` — thread metadata

For each unposted tweet (oldest first, excluding `skip_reason: "thread_member"`), execute ALL of the following steps:

#### Step 3a: FxTwitter API Enrichment

Convert the tweet URL by replacing `x.com` with `api.fxtwitter.com`. Use `WebFetch` to retrieve the full JSON response.

Extract from the response:
- `tweet.text` -- full tweet content
- `tweet.author.name` + `tweet.author.screen_name` -- author identity
- `tweet.author.description` -- author bio/context (include in summary)
- `tweet.likes`, `tweet.retweets`, `tweet.views` -- engagement metrics
- `tweet.quote` -- quoted tweet (if present, extract its text, author, and key data)
- `tweet.media` -- attached images or videos
- `tweet.created_at` -- timestamp

**Thread enrichment**: If `is_thread === true` in tweets.json, also fetch the ROOT tweet URL (`thread[0].url` from the DB) via FxTwitter to get the root tweet's engagement stats and author info. Use the root tweet's engagement metrics (likes, retweets, views) as the primary stats since the root typically has higher engagement. Keep the full `thread_text` from the DB as the primary content source.

If FxTwitter returns `code !== 200`, log the error and skip this tweet.

#### Step 3b: Web Research (2-3 queries per tweet)

Based on the enriched tweet content (use `thread_text` for thread tweets, single `tweet.text` otherwise):
1. Identify 2-3 key topics, technologies, people, or entities mentioned across the full content
2. Run `WebSearch` for each to gather:
   - Background context
   - Recent developments
   - Broader implications
3. Collect relevant URLs for the "참고 링크" section

This step is **mandatory** -- never skip research. Even for simple tweets, at least 2 searches provide valuable context. For thread tweets, research should cover topics from ALL tweets in the thread, not just the first one.

#### Step 3c: Topic Classification for Message 3

Classify whether the tweet topic relates to **AI GPU Cloud** based on:
- Mentions GPU, CUDA, NVIDIA, AMD ROCm, TPU, NPU, or AI accelerators
- Discusses cloud infrastructure (AWS, GCP, Azure) in an AI/ML context
- Covers ML training/inference infrastructure, model serving, or AI platform services
- References GPU cluster management, orchestration (Kubernetes for AI), or MLOps
- Discusses AI chip market, GPU supply/demand, or cloud GPU pricing

If any criterion matches strongly → use **Message 3A** template.
If none match → use **Message 3B** template (topic-specific insights with action items).

#### Step 3d: Find Slack Channel

Use the classified channel from Phase 2. Look up the `channel_id` from `outputs/twitter/slack-channels.json`.

If the channel is not in the local registry, search via MCP:
- Server: `plugin-slack-slack`
- Tool: `slack_search_channels`
- Query: the channel name

#### Step 3e: Post 3-Message Slack Thread

All messages use Slack mrkdwn format. Rules:
- Use `*bold*` (single asterisk), `_italic_` (underscore)
- Do NOT use `**double asterisks**` or `## headers`
- Write content in Korean
- Limit each message to under 4000 characters

**Message 1: Title (Channel Post)**

```
{1-2 line Korean title summarizing the core insight}
{original tweet URL}
>>>
```

CRITICAL: Capture the `message_ts` from the response for thread replies.

**Media Upload (between Message 1 and Message 2) — MANDATORY CHECK**

After posting Message 1 and capturing `message_ts`, you **MUST** check for media. The manifest includes pre-extracted media info for each tweet:

- `has_media` (boolean) — whether the tweet contains any media
- `media_type` — `"video"` or `"photo"`
- `media_url` — direct download URL (highest-bitrate mp4 for video, original jpg for photo)

**Decision tree:**

1. **If `has_media === true` in the manifest** → use `media_url` directly.
2. **If manifest `media_url` is null but FxTwitter response has `tweet.media`** → extract manually:
   - Videos: from `tweet.media.videos[0].formats`, pick the entry with the highest `bitrate` where `container === "mp4"`. Fallback: `tweet.media.videos[0].url`.
   - Photos: use `tweet.media.photos[0].url`.
3. **If neither source has media** → skip to Message 2.

Run the upload script via Shell:

```bash
cd scripts/twitter && node upload_media_to_slack.js \
  --url "<media_url>" \
  --channel "<channel_id>" \
  --thread-ts "<message_ts>" \
  --title "<author_screen_name> - media"
```

If the upload fails, log the error and **continue** with Message 2. Media upload failure must NOT block the rest of the thread.

**CRITICAL**: Do NOT skip this step. Every tweet with `has_media: true` MUST have a media upload attempt. This is a quality gate requirement.

**Message 2: Detailed Summary (Thread Reply)**

Send with `thread_ts` from Message 1.

Use the **thread variant** when `is_thread === true`, otherwise use the **single tweet variant**.

**Single tweet variant** (`is_thread === false`):

```
*Tweet 요약*
- 작성자: @{screen_name} ({name}) — {author bio/context}
- 반응: ❤️ {likes} | 🔁 {retweets} | 👀 {views}
- 작성일: {created_at}

*핵심 내용*
{Tweet 내용을 한국어로 상세 요약. 원문이 영어인 경우 번역 포함.
구체적 수치, 기술명, 제품명 등을 빠짐없이 포함.}

{인용 트윗이 있는 경우:}
*인용 트윗 (@{quote.author.screen_name} — {quote author context})*
{quote.text를 한국어로 상세 요약. 구체적 수치와 핵심 주장 포함.}

*추가 조사 결과*
{WebSearch로 수집한 관련 정보를 상세 bullet point로 정리}
- *{토픽1}*: {배경 설명과 최신 동향}
- *{토픽2}*: {기술적 의미와 영향}
- *{토픽3}*: {산업 맥락과 시사점}

*참고 링크*
- <{url1}|{title1}>
- <{url2}|{title2}>
- <{url3}|{title3}>
```

**BAD output (subagent quality — DO NOT produce this):**
```
원문 요약 (@username)
개발자가 X를 시도했다는 내용. 조회 약 4만.
```
```
리서치 컨텍스트
일반적인 배경 설명. 별도 검증 필요.
```

This is what subagent delegation and context pressure produce: no author bio,
no emoji-formatted engagement stats, no structured sections, no WebSearch findings,
no reference links, no analytical depth. This is **never acceptable**.

**GOOD output (expected quality — ALWAYS produce this level):**
See Example 2 in the Examples section below for a complete reference. Every post
MUST match that level of detail: author bio, emoji stats, 핵심 내용 with 3+ sentences,
추가 조사 결과 with specific data points from WebSearch, 2+ 참고 링크, and
a topic-specific Message 3 with concrete Action Items.

**Thread variant** (`is_thread === true`):

Use the `thread` array from tweets.json to show all tweets in the thread numbered sequentially. Use the ROOT tweet's engagement stats (first tweet in chain typically has higher engagement).

```
*Tweet 요약*
- 작성자: @{screen_name} ({name}) — {author bio/context}
- 반응: ❤️ {root_likes} | 🔁 {root_retweets} | 👀 {root_views} _(루트 트윗 기준)_
- 작성일: {created_at}
- 📎 스레드: {N}개 트윗

*스레드 전문*
1️⃣ {thread[0].text}

2️⃣ {thread[1].text}

{... continue for each tweet in thread ...}

*핵심 내용*
{스레드 전체 내용을 한국어로 종합 분석. 개별 트윗이 아닌 스레드 전체를
하나의 서사로 요약. 원문이 영어인 경우 번역 포함.
구체적 수치, 기술명, 제품명 등을 빠짐없이 포함.}

{인용 트윗이 있는 경우:}
*인용 트윗 (@{quote.author.screen_name} — {quote author context})*
{quote.text를 한국어로 상세 요약. 구체적 수치와 핵심 주장 포함.}

*추가 조사 결과*
{WebSearch로 수집한 관련 정보를 상세 bullet point로 정리.
스레드 전체 내용을 기반으로 리서치.}
- *{토픽1}*: {배경 설명과 최신 동향}
- *{토픽2}*: {기술적 의미와 영향}
- *{토픽3}*: {산업 맥락과 시사점}

*참고 링크*
- <{url1}|{title1}>
- <{url2}|{title2}>
- <{url3}|{title3}>
```

**Message 3A: AI GPU Cloud related (Thread Reply)**

```
*AI GPU Cloud 서비스 인사이트*

{이 트윗 주제가 AI GPU Cloud / AI 플랫폼 서비스에 어떤 의미를 가지는지 분석}

*핵심 시사점*
- {GPU 클라우드 인프라 관점에서의 인사이트}
- {AI 플랫폼 서비스에 미칠 영향}
- {팀이 취해야 할 액션 또는 고려사항}

*적용 가능성*
{구체적으로 우리 서비스에 어떻게 적용하거나 대응할 수 있는지}
```

**Message 3B: Topic-specific (Thread Reply)**

```
*{주제} 인사이트*

{이 콘텐츠의 주제와 관련된 핵심 분석}

*핵심 시사점*
- {해당 분야의 트렌드 및 의미}
- {기술적/비즈니스적 영향}
- {주목할 점}

*Action Items*
- {팀에서 검토하거나 논의할 사항}
- {추가 조사가 필요한 영역}
- {적용 또는 대응 방안}
```

#### Step 3f: Update Local DB

After successful posting, update `tweets.json`:
- Set `posted_to_slack: true`
- Set `slack_channel` to the channel name
- Set `slack_ts` to the `message_ts` from Message 1
- Set `classified_topic` to the classification result

#### Step 3f-verify: Quality Self-Check (MANDATORY)

Before proceeding to the next tweet, verify the posted thread against ALL
quality gate items. If ANY item below is missing, you MUST edit or re-post
the deficient message:

- [ ] Message 1 has a substantive Korean title (not just a translation of
      the tweet — add analytical framing)
- [ ] Message 2 includes author bio context (not just @handle)
- [ ] Message 2 includes engagement stats with ❤️/🔁/👀 emoji formatting
- [ ] Message 2 "핵심 내용" section has 3+ sentences of substantive analysis
- [ ] Message 2 "추가 조사 결과" has specific findings from 2+ WebSearches
      (not generic background — cite specific data points, dates, numbers)
- [ ] Message 2 "참고 링크" has 2+ URLs from WebSearch results
- [ ] Message 3 has topic-specific analysis (not generic filler like
      "이 콘텐츠는 흥미롭습니다")
- [ ] Message 3 Action Items are concrete and actionable
- [ ] Media upload was attempted if `has_media === true`

**RED FLAG**: If your Message 2 is shorter than 800 characters or Message 3
is shorter than 400 characters, the output is almost certainly too shallow.
Go back and add depth — re-run WebSearch if needed, expand the analysis,
add more specific data points.

See [references/quality-enforcement.md](references/quality-enforcement.md) for
the full quality gate with BAD vs GOOD output examples.

#### Step 3g: Decision Extraction (skip if `skip-decisions`)

Evaluate whether the tweet warrants a DECISION post. Default to NOT posting — only post when the decision signal is clear and actionable.

See [references/decision-template.md](references/decision-template.md) for detection criteria, the DECISION post template, and channel routing rules.

#### Step 3h: Rate Limiting

Wait 10-15 seconds before processing the next tweet to avoid Slack rate limits.

### Quality Gate

The authoritative quality checklist is in **Step 3f-verify** above. For the full quality gate with BAD vs GOOD output examples and thread-specific checks, see [references/quality-enforcement.md](references/quality-enforcement.md).

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
           → Read thread data from tweets.json (is_thread, thread, thread_text)
           → WebFetch FxTwitter API (enrichment; fetch root tweet too for threads)
           → WebSearch x 2-3 (research based on thread_text for threads)
           → Slack Message 1 (title post)
           → Media upload if photo/video exists (upload_media_to_slack.js)
           → Slack Message 2 (thread variant if is_thread) + Message 3 (thread replies)
           → Update tweets.json (status)
           → Wait 10-15s (rate limit)
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
4. For each tweet, execute Phase 3 (full x-to-slack workflow):
   a. WebFetch FxTwitter API for enriched data
   b. WebSearch 2-3 queries for context
   c. Post 3-message Slack thread with full templates
5. Update tweets.json with posting status after each tweet
6. Wait 10-15s between tweets

### Example 2: Expected output quality

For a tweet like `https://x.com/altryne/status/2032223053116260367`:

**Message 1 (channel post):**
```
Shopify CEO가 Karpathy의 Autoresearch로 20년 된 Liquid 엔진을 53% 빠르게 만들다 — AI 코딩 에이전트의 실전 성능 최적화 사례
https://x.com/altryne/status/2032223053116260367
>>>
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
월가 AI 에이전트를 1인 오픈소스로 구현 — 리서치, 퀀트, 트레이딩, 리스크 관리 풀스택
https://x.com/quantscience_/status/2032849537975357665
>>>
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
- **twittxr API failure**: Log error, continue with existing tweets in DB
- **FxTwitter fetch failure**: Use raw tweet data from twittxr as fallback
- **Slack channel not found**: Skip tweet, log warning
- **Rate limit**: Configurable via `TWEET_POST_DELAY_MS` env var (default: 12000ms)

## Composed Skills

This skill orchestrates:
- **x-to-slack** -- Core tweet → Slack posting pipeline (FxTwitter enrichment + WebSearch + 3-message thread). Phase 3 follows its FULL workflow for each tweet.
- **scrapling** or **agent-browser** -- Fallback for tweet fetching if twittxr fails

## Decision Channels

| Channel | ID | Scope |
|---|---|---|
| `효정-의사결정` | `C0ANBST3KDE` | Personal decisions (tool adoption, portfolio) |
| `7층-리더방` | `C0A6Q7007N2` | Team/CTO decisions (infra, strategy, competitive) |

Step 3g uses these channels. See [references/decision-template.md](references/decision-template.md) for the full decision routing rules.

## MCP Tool Reference

| Tool | Server | Purpose |
|---|---|---|
| `slack_search_channels` | `plugin-slack-slack` | Find channel_id by name |
| `slack_send_message` | `plugin-slack-slack` | Post messages and thread replies |
| `slack_read_channel` | `plugin-slack-slack` | Fallback to find message_ts |

## File Structure

```
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
    archive/              # Daily snapshots
```
