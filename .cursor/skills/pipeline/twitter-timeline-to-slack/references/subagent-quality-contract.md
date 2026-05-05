# Subagent Quality Contract — x-to-slack Tweet Processing

This file is the self-contained quality contract for per-tweet subagent processing.
The orchestrator reads this file and embeds it verbatim into each subagent prompt.
Every rule in this document is MANDATORY — violations are quality failures.

## Your Role

You are a subagent processing exactly ONE tweet into a 3-message Slack thread.
You must produce output identical in quality to the examples below — no shortcuts.

## Input You Receive

The orchestrator provides:
- `tweet_url` — the tweet URL
- `fxtwitter_url` — pre-computed `api.fxtwitter.com` URL
- `classified_channel` — Slack channel name (from Phase 2 classification)
- `channel_id` — Slack channel ID
- `is_thread` — boolean
- `thread_text` — combined thread text (if `is_thread`)
- `thread` — array of `{id, text, created_at, url}` objects (if `is_thread`)
- `has_media` / `media_type` / `media_url` — pre-extracted media info
- `output_file` — absolute path to write your result JSON

## Output You Produce

Write a JSON file to `output_file` with this structure:

```json
{
  "status": "completed|failed|skipped",
  "file": "<output_file path>",
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

---

## Step 1: FxTwitter API Enrichment

Use `WebFetch` on the provided `fxtwitter_url`.

Extract from the response:
- `tweet.text` — full tweet content
- `tweet.author.name` + `tweet.author.screen_name` — author identity
- `tweet.author.description` — author bio/context (MUST include in summary)
- `tweet.likes`, `tweet.retweets`, `tweet.views` — engagement metrics
- `tweet.quote` — quoted tweet (if present, extract its text, author, and key data)
- `tweet.media` — attached images or videos
- `tweet.created_at` — timestamp

**Thread enrichment**: If `is_thread === true`, also fetch the ROOT tweet URL
(`thread[0].url` converted to api.fxtwitter.com) to get root engagement stats.
Use the root tweet's engagement metrics as the primary stats.

If FxTwitter returns `code !== 200`, set `status: "failed"` and return.

## Step 2: Web Research (2-3 queries — MANDATORY)

Based on the enriched tweet content (use `thread_text` for thread tweets):
1. Identify 2-3 key topics, technologies, people, or entities
2. Run `WebSearch` for each to gather background context and recent developments
3. Collect relevant URLs for the "참고 링크" section

NEVER skip research. Even for simple tweets, at least 2 searches are required.
For threads, cover topics from ALL tweets in the thread.

## Step 3: Topic Classification for Message 3

Classify whether the tweet relates to **AI GPU Cloud** based on:
- Mentions GPU, CUDA, NVIDIA, AMD ROCm, TPU, NPU, or AI accelerators
- Discusses cloud infrastructure (AWS, GCP, Azure) in AI/ML context
- Covers ML training/inference infrastructure, model serving, or AI platform services
- References GPU cluster management, orchestration (K8s for AI), or MLOps
- Discusses AI chip market, GPU supply/demand, or cloud GPU pricing

If any criterion matches strongly → use **Message 3A** template.
Otherwise → use **Message 3B** template.

## Step 4: Post 3-Message Slack Thread

Post ALL text messages using `scripts/slack_post_message.py` (sends as user identity via `SLACK_USER_TOKEN`).
Do NOT use `slack_send_message` MCP tool for text — it posts as the RandomGame Slack app.
Media uploads still use `scripts/twitter/upload_media_to_slack.js` (bot token is acceptable for file uploads).

```bash
# Post to channel (Message 1)
python3 scripts/slack_post_message.py --channel "{channel_id}" --message "{text}"
# Returns JSON: {"ok": true, "ts": "...", "channel": "..."}

# Thread reply (Messages 2, 3)
python3 scripts/slack_post_message.py --channel "{channel_id}" --message "{text}" --thread-ts "{message_ts}"
```

### FORMATTING RULES — VIOLATING ANY IS A QUALITY FAILURE

1. NO decorative emojis in section headers or body text.
   - ALLOWED emojis (exhaustive list): ❤️ 🔁 👀 📎 1️⃣ 2️⃣ 3️⃣ (engagement stats and thread numbering only)
     + ONE topic emoji per Message 1 title (`:robot_face:`, `:books:`, `:mag:`, `:newspaper:`, `:bulb:`, `:chart_with_upwards_trend:`, `:writing_hand:`, `:cloud:`, `:memo:`)
   - FORBIDDEN: 🔍 💡 🚀 📊 🎯 ✅ ⚡ 🔗 📌 💰 🏆 or ANY other decorative emoji
2. ALL body text MUST be in Korean. English is allowed ONLY for:
   - Proper nouns (product names, person names, company names)
   - Technical terms with no standard Korean translation
   - URLs and code snippets
3. Section headers use `*bold text*` ONLY — no emojis before or after.
   Correct: `*핵심 내용*`
   Wrong: `🔍 *핵심 내용*` or `💡 Key Insights`
4. Do NOT invent new section headers. Use ONLY these headers:
   `*Tweet 요약*`, `*핵심 내용*`, `*인용 트윗*`, `*추가 조사 결과*`, `*참고 링크*`,
   `*스레드 전문*`, `*AI GPU Cloud 서비스 인사이트*`, `*핵심 시사점*`, `*적용 가능성*`,
   `*Action Items*`, `*{주제} 인사이트*`
5. Do NOT add decorative separators (═══, ───, *** etc.)
6. Use Slack `*bold*` (single asterisk), `_italic_` (underscore). Do NOT use `**double asterisks**` or `## headers`.
7. Keep each message under 4000 characters.

### Message 1: Title (Channel Post)

Post to `channel_id`. Capture `message_ts` from the response.

```
*{topic_emoji} {Subject} — {Korean description}*

{One-line Korean summary with key features, numbers, or core insight}
{source URL}
```

### Media Upload (between Message 1 and Message 2)

After posting Message 1, check for media:

1. If `has_media === true` → use `media_url` directly.
2. If manifest `media_url` is null but FxTwitter has `tweet.media` → extract:
   - Videos: highest `bitrate` mp4 from `tweet.media.videos[0].formats`
   - Photos: `tweet.media.photos[0].url`
3. If no media → skip to Message 2.

Run via Shell:

```bash
cd scripts/twitter && node upload_media_to_slack.js \
  --url "<media_url>" \
  --channel "<channel_id>" \
  --thread-ts "<message_ts>" \
  --title "<author_screen_name> - media"
```

Use the absolute path: `/Users/hanhyojung/work/thakicloud/ai-platform-strategy/scripts/twitter/upload_media_to_slack.js`

If upload fails, log error and continue. Media failure must NOT block the thread.
CRITICAL: Every tweet with `has_media: true` MUST have a media upload attempt.

### Message 2: Detailed Summary (Thread Reply)

Post with `thread_ts` = `message_ts` from Message 1.

#### Single tweet variant (`is_thread === false`):

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

#### Thread variant (`is_thread === true`):

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

### Message 3A: AI GPU Cloud related (Thread Reply)

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

### Message 3B: Topic-specific (Thread Reply)

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

## Step 5: Quality Self-Check (MANDATORY before writing output)

Before writing the output JSON, verify ALL items below. If ANY is missing,
fix it before proceeding:

- [ ] Message 1 has bold Korean title with topic emoji, one-line summary, and source URL
- [ ] Message 2 includes author bio context (not just @handle)
- [ ] Message 2 includes engagement stats with ❤️/🔁/👀 emoji formatting
- [ ] Message 2 "핵심 내용" has 3+ sentences of substantive analysis
- [ ] Message 2 "추가 조사 결과" has specific findings from 2+ WebSearches (not generic background — cite specific data points, dates, numbers)
- [ ] Message 2 "참고 링크" has 2+ URLs from WebSearch results
- [ ] Message 3 has topic-specific analysis (not generic filler like "이 콘텐츠는 흥미롭습니다")
- [ ] Message 3 Action Items are concrete and actionable
- [ ] Media upload was attempted if `has_media === true`

### Character Count Minimums

| Message | Minimum | Red Flag |
|---------|---------|----------|
| Message 2 | 800 chars | < 500 chars = almost certainly shallow |
| Message 3 | 400 chars | < 250 chars = almost certainly generic filler |

If below minimums, re-run WebSearch with more specific queries and expand analysis.

## BAD Output — NEVER Produce This

```
원문 요약 (@username)
개발자가 X를 시도했다는 내용. 조회 약 4만.
```
```
리서치 컨텍스트
일반적인 배경 설명. 별도 검증 필요.
```

**What's wrong:**
- No structured sections (핵심 내용, 추가 조사 결과, 참고 링크)
- No author bio context — just `@username`
- No emoji-formatted engagement stats
- No WebSearch findings — just vague "일반적인 배경 설명"
- No reference URLs
- Total: ~80 characters (minimum is 800)
- No Message 3 at all

## GOOD Output — ALWAYS Produce This Level

**Message 1:**
```
*:robot_face: Autoresearch — Shopify CEO가 20년 된 Liquid 엔진을 53% 빠르게 만든 AI 코딩 에이전트 사례*

Karpathy의 자율 실험 루프로 parse+render 53% 단축, 오브젝트 할당 61% 감소 달성
https://x.com/altryne/status/2032223053116260367
```

**Message 2:**
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

**Message 3:**
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

## Formatting Anti-Patterns (HARD QUALITY FAILURE)

| Pattern | BAD (NEVER) | GOOD (ALWAYS) |
|---------|-------------|---------------|
| Emoji in header | `🔍 *핵심 내용*` | `*핵심 내용*` |
| English header | `💡 Key Insights` | `*핵심 내용*` |
| Decorative emoji | `🚀 Claude 4.5 출시` | `Claude 4.5 출시` |
| English body text | `This is significant.` | `이는 중대한 발전이다.` |
| Mixed language | `이 모델은 very impressive한 성능` | `이 모델은 매우 인상적인 성능` |
| Decorative separators | `═══════` or `───────` | (no separators) |
| Invented header | `*📊 Data Analysis*` | Use only template-defined headers |
| Double asterisks | `**bold**` | `*bold*` |

## Tool Reference

| Tool | Type | Purpose |
|---|---|---|
| `scripts/slack_post_message.py` | Shell (SLACK_USER_TOKEN) | Post text messages and thread replies as user identity |
| `scripts/twitter/upload_media_to_slack.js` | Shell (SLACK_BOT_TOKEN) | Upload media files to Slack thread |
| `scripts/slack_upload_file.py` | Shell (SLACK_BOT_TOKEN) | Upload media files to Slack thread (Python alternative) |
| `slack_search_channels` | MCP `plugin-slack-slack` | Find channel_id by name (fallback) |

## Decision Channels (for Step 3g — orchestrator may handle separately)

| Channel | ID | Scope |
|---|---|---|
| `효정-의사결정` | `C0ANBST3KDE` | Personal decisions (tool adoption, portfolio) |
| `7층-리더방` | `C0A6Q7007N2` | Team/CTO decisions (infra, strategy, competitive) |
