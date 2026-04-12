---
name: x-to-slack
description: >-
  Fetches tweet content from X/Twitter via FxTwitter API, performs web
  research, and posts structured intelligence to Slack in a 3-message thread.
  Use when user shares an X/Twitter link (x.com or twitter.com URL) and wants to
  analyze it for Slack posting, or says "tweet to slack", "share this tweet",
  "x-to-slack". Do NOT use for general Slack messaging, channel management, or
  non-Twitter content sharing. Korean triggers: "분석", "검색", "리서치", "API".
metadata:
  author: "thaki"
  version: "1.2.0"
  category: "execution"
---
# X-to-Slack: Tweet Intelligence Pipeline

> **Note**: This is the project-level Twitter-only handler (v1.1.0). The canonical universal handler supporting Twitter, GitHub, YouTube (with Defuddle transcript), and articles is at `~/.cursor/skills/pipeline/x-to-slack/SKILL.md` (v2.2.0). Use the user-level version for non-Twitter URLs.

Process an X (Twitter) URL, gather context through web research, and post a structured 3-message thread to a specified Slack channel.

## Input

The user provides:
1. **X URL** -- e.g. `https://x.com/user/status/1234567890`
2. **Slack channel name** -- e.g. `#general` or `general`

## Workflow

### Step 0.5: Cross-Repo Dedup Check (MANDATORY)

Before any processing, check the central intelligence registry to avoid duplicate Slack posts across repos/machines.

```bash
RESEARCH_REPO="${RESEARCH_REPO:-$HOME/thaki/research}"
python3 "$RESEARCH_REPO/scripts/intelligence/intel_registry.py" check "<tweet_url>"
```

- **Exit 0 (new)**: Proceed with the pipeline.
- **Exit 1 (duplicate)**: Report `"이미 처리된 URL입니다 (처음 처리: {first_seen}, 소스: {source_repo})"` and STOP. Do NOT post to Slack.

If the research repo or `intel_registry.py` is not found, log a warning and proceed (graceful degradation).

### Step 1: Fetch Tweet via FxTwitter API

Convert the URL by replacing `x.com` or `twitter.com` with `api.fxtwitter.com`. Use `WebFetch` to retrieve the JSON.

For response schema, field extraction details, and error codes, see [references/fxtwitter-api.md](references/fxtwitter-api.md).

Extract: `tweet.text`, `tweet.author.name`, `tweet.author.screen_name`, `tweet.likes`, `tweet.retweets`, `tweet.views`, `tweet.url`, `tweet.quote`, `tweet.media`.

If `code` is not `200`, inform the user of the error and do not proceed.

### Step 2: Additional Web Research

Based on the tweet content:
1. Identify 2-3 key topics, technologies, or entities mentioned.
2. Run `WebSearch` for each to gather background, recent developments, and implications.
3. Collect relevant findings for the summary.

### Step 3: Find Slack Channel

#### Step 3a: Channel Registry Lookup (fast path)

Strip the `#` prefix from the user-provided channel name and look it up in the registry below.
If found, use the `channel_id` directly — skip the MCP search entirely.

| Channel Name | Channel ID | Type | Description |
|---|---|---|---|
| `research` | `C0A7GBRK2SW` | private | 리서치/논문/기술 분석 |
| `ai-coding-radar` | `C0A7K3TBPK7` | public | AI 코딩 에이전트/도구 동향 |
| `press` | `C0A7NCP33LG` | public | 언론/미디어/콘텐츠 |
| `research-pr` | `C0A7FS8UC66` | public | 리서치 PR |
| `prompt` | `C0A98HXSVMK` | public | 프롬프트 엔지니어링/LLM 기법 |
| `deep-research-trending` | `C0AN34G4QHK` | private | 딥 리서치/논문 분석/트렌딩 |
| `idea` | `C0A6U3HE3GS` | public | 아이디어/브레인스토밍 |
| `random` | `C0A6CLTNARM` | public | 일반/기타 |
| `효정-할일` | `C0AA8NT4T8T` | private | 개인 태스크/할일 |
| `효정-주식` | `C0A7V1A09NK` | private | 주식/투자/트레이딩 |
| `효정-insight` | `C0A8SSPC9RU` | private | 전략 인사이트/분석 |

#### Step 3b: MCP Search (fallback)

If the channel name is **not** in the registry, search via MCP:

- Server: `plugin-slack-slack`
- Tool: `slack_search_channels`
- Query: the channel name the user provided (strip `#` prefix if present)

Extract the `channel_id` from the search results. If multiple matches, pick the closest **exact** name match.

#### Step 3c: Private channel fallback

If `slack_search_channels` returns no exact match, the channel may be private. Use `slack_search_public_and_private` to find it:

- Server: `plugin-slack-slack`
- Tool: `slack_search_public_and_private`
- Arguments: `query`: `"in:{channel_name}"`, `channel_types`: `"private_channel"`, `limit`: `1`, `response_format`: `"detailed"`

The response will contain `Channel: #channel-name (ID: C0XXXXXXXX)`. Extract the `channel_id` from this.

If all steps fail to find a channel, ask the user to clarify.

### Step 3.5: Pre-Post Quality Gate

Before posting to Slack, verify all 3 thread messages are ready:
- [ ] Message 1 (Title): Bold Korean title with topic emoji, one-line summary, and direct tweet URL
- [ ] Message 2 (Summary): Contains Korean summary, 3+ key insights from web research, source links
- [ ] Message 3 (AI GPU Cloud): Contains ThakiCloud relevance analysis OR explicit "관련 없음" statement
- [ ] All messages use Slack mrkdwn (not markdown) — no `**` or `##`
- [ ] Media attachments prepared via 3-step Slack upload flow if original tweet has images/video

If web research returned no relevant results, note this in Message 2 rather than omitting the section. See [assets/templates/slack-thread.md](assets/templates/slack-thread.md) for the 3-message template structure.

### Step 4: Post to Slack (3 Messages)

All messages use Slack mrkdwn format. Rules:
- Use `*bold*` (single asterisk), `_italic_` (underscore)
- Do NOT use `**double asterisks**` or `## headers`
- Write content in Korean
- Limit each message to under 4000 characters

FORMATTING RULES — VIOLATING ANY OF THESE IS A QUALITY FAILURE:

0. **MESSAGE 1 IS PLAIN TEXT ONLY** — exactly 2 lines: one Korean headline sentence + source URL.
   NO emojis, NO bold, NO italic, NO author info, NO engagement stats, NO "원문 보기", NO flag emojis.
   Author/engagement data belongs ONLY in Message 2.
1. NO decorative emojis in section headers or body text (Messages 2 and 3).
   - ALLOWED emojis (exhaustive list, Message 2/3 only): ❤️ 🔁 👀 📎 1️⃣ 2️⃣ 3️⃣ (engagement stats and thread numbering only)
   - FORBIDDEN everywhere: 🔍 💡 🚀 📊 🎯 ✅ ⚡ 🔗 📌 💰 🏆 🧠 👤 📝 or ANY other decorative emoji
   - Flag emojis (🇮🇹 🇺🇸 🇰🇷 etc.) are FORBIDDEN everywhere
2. ALL body text MUST be in Korean. English is allowed ONLY for:
   - Proper nouns (product names, person names, company names)
   - Technical terms with no standard Korean translation
   - URLs and code snippets
3. Section headers (Messages 2 and 3 only) use *bold text* ONLY — no emojis before or after.
   Correct: *핵심 내용*
   Wrong:   🔍 *핵심 내용* or 💡 Key Insights
4. Do NOT invent new section headers. Use ONLY the headers defined in the template:
   *Tweet 요약*, *핵심 내용*, *인용 트윗*, *추가 조사 결과*, *참고 링크*,
   *AI GPU Cloud 서비스 인사이트*, *핵심 시사점*, *적용 가능성*,
   *Action Items*, *{주제} 인사이트*
5. Do NOT add decorative separators (═══, ───, *** etc.)
6. Media upload is MANDATORY — if the tweet has photos or videos, upload them. HARD FAILURE if skipped.

#### Message 1: Title (Channel Post)

Send to the channel using `slack_send_message`:
- Server: `plugin-slack-slack`
- Tool: `slack_send_message`
- Arguments: `channel_id`, `message`

Format — Message 1 is EXACTLY 2-3 lines, nothing more:

```
{Korean headline — one sentence summarizing the core insight or news}
{source URL}
```

**Message 1 MUST contain ONLY:**
1. A concise Korean headline (one sentence, no emoji prefix, no bold markup)
2. The original tweet URL

**Message 1 MUST NOT contain (these belong in Message 2):**
- Author info (`@username`, name, bio, follower count) — NEVER in Message 1
- Engagement stats (likes, retweets, views, bookmarks) — NEVER in Message 1
- "원문 보기" link text — NEVER in Message 1
- Flag emojis (🇮🇹 🇺🇸 🇰🇷 etc.) — NEVER in Message 1
- Decorative emojis (🧠 👤 🔗 📝 🔍 💡 🚀 etc.) — NEVER in Message 1
- Multiple lines of description — NEVER in Message 1
- Bold/italic formatting — NEVER in Message 1

Anti-pattern (HARD FAILURE — must never produce this):
```
🧠 Claude Code + Obsidian = 세컨드 브레인 구축 완전 가이드
👤 @defileo | DeFi & AI 인사이트 크리에이터 (팔로워 41.7K)
🔗 원문 보기
🇮🇹 👀 365만 | ❤️ 5,331 | 🔄 429 | 📝 26,583
```

Correct example:
```
Claude Code + Obsidian으로 세컨드 브레인 구축하는 완전 가이드 — Karpathy LLM Wiki 기반 지식 관리 시스템
https://x.com/defileo/status/2042241063612502162
```

**CRITICAL**: Capture the `message_ts` (timestamp) from the response. This is needed for thread replies.

#### Message 2: Detailed Summary (Thread Reply)

Send as a thread reply using `slack_send_message` with `thread_ts`:
- Arguments: `channel_id`, `message`, `thread_ts` (from Message 1)

Format:

```
*Tweet 요약*
- 작성자: @{screen_name} ({name}) — {author bio/description}
- 반응: ❤️ {likes} | 🔁 {retweets} | 👀 {views}
- 작성일: {created_at}

*핵심 내용*
{Tweet 내용을 한국어로 요약 정리. 원문이 영어인 경우 번역 포함.}

{인용 트윗이 있는 경우:}
*인용 트윗 (@{quote.author.screen_name})*
{quote.text 요약}

*추가 조사 결과*
{WebSearch로 수집한 관련 정보를 bullet point로 정리}
- {관련 배경 정보}
- {최근 동향}
- {영향 및 의미}

*참고 링크*
- {검색에서 발견한 관련 URL들}
```

#### Message 3: AI GPU Cloud Insights (Thread Reply)

Send as another thread reply with the same `thread_ts`.

Format:

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

#### Message 3B: Topic-specific (Thread Reply) — when NOT AI GPU Cloud related

If the tweet topic is not directly related to AI GPU Cloud / AI platform services, use this topic-specific template instead of Message 3A:

```
*{주제} 인사이트*

{이 트윗 주제에 대한 심층 분석 — 시장 영향, 기술적 의미, 전략적 시사점 등}

*핵심 시사점*
- {해당 분야/주제 관점에서의 인사이트}
- {산업/시장에 미칠 영향}
- {관련 트렌드 및 향후 전망}

*Action Items*
- {구체적이고 실행 가능한 후속 조치}
- {모니터링해야 할 사항}
- {추가 리서치가 필요한 영역}
```

### Step 5: Long-Form Detection → x-to-notion (optional)

After completing the Slack thread, evaluate whether the tweet qualifies as **long-form content** worth archiving to Notion.

**Detection criteria** (ANY match triggers Notion publishing):

| Criterion | Threshold |
|---|---|
| Tweet text length | > 500 characters |
| X Article | `tweet.article` exists in FxTwitter response |
| Thread | Self-reply thread with 3+ tweets |
| Quote + body combined | Total text (tweet + quote) > 400 characters |

**Execution**:

If any criterion matches, invoke the `x-to-notion` skill with the original tweet URL:

1. Log: `"장문 콘텐츠 감지 — Notion 아카이브 시작 ({criterion})"`
2. Run x-to-notion pipeline (Phase 1–5) with:
   - `url`: the original tweet URL
   - `parent_page_id`: default (`3239eddc34e680e8a7a5d5b5eac18b38`)
3. After x-to-notion completes, add a **4th Slack thread reply** to the existing thread:

```
*Notion 아카이브*
장문 콘텐츠가 Notion에 전문 번역·보관되었습니다.
{Notion page URL}
```

**Error handling**: If x-to-notion fails, log the error but do NOT fail the overall x-to-slack pipeline. The Slack thread is already posted successfully.

**Skip flag**: If the user passes `skip-notion`, skip this step entirely.

### Step 6: Artifact Save & URL Registration (MANDATORY)

After Slack posting completes (and optional x-to-notion), save the intelligence artifact to the research repo and register the URL.

#### Step 6a: Generate Markdown Artifact

Create a markdown file summarizing this tweet's intelligence:

```markdown
---
url: {tweet_url}
author: @{screen_name}
date: {created_at}
slack_channel: {channel_name}
slack_ts: {message_ts}
topic: {classified_topic}
---
# {Korean title from Message 1}

{Message 2 content (full Korean summary with research)}

{Message 3 content (insights and action items)}
```

Save to a temporary file, e.g. `/tmp/x-to-slack-{tweet_id}.md`.

#### Step 6b: Save to Research Repo

```bash
RESEARCH_REPO="${RESEARCH_REPO:-$HOME/thaki/research}"
python3 "$RESEARCH_REPO/scripts/intelligence/intel_registry.py" save \
  "{tweet_url}" "/tmp/x-to-slack-{tweet_id}.md" \
  --type tweet \
  --channel "{channel_name}" \
  --ts "{message_ts}" \
  --topic intelligence
```

This copies the artifact to `~/thaki/research/outputs/intelligence/{date}/{slug}.md` and registers the URL in the central dedup registry.

If the research repo is not found, log a warning and skip (graceful degradation). The Slack post is still complete.

## Examples

### Example 1: English tech tweet

User says: "https://x.com/kaborogang/status/1893370063134626098 ai-gpu-cloud 채널에 올려줘"

Actions:
1. Fetch tweet via `api.fxtwitter.com/kaborogang/status/1893370063134626098`
2. WebSearch for key topics mentioned in the tweet
3. Find `ai-gpu-cloud` channel via `slack_search_channels`
4. Post 3-message thread (title, summary with research, GPU Cloud insights)

Result: Structured Korean-language thread posted to #ai-gpu-cloud

### Example 2: Korean tweet with quote

User says: "x-to-slack https://x.com/user/status/123 #general"

Actions:
1. Fetch tweet — detect quote tweet in `tweet.quote`
2. WebSearch for topics from both the main tweet and quote
3. Find `general` channel
4. Message 2 includes quoted tweet summary section

Result: Thread with quote tweet context included

## Error Handling

- **FxTwitter API failure**: Try Agent-Reach Twitter channel as fallback: `twitter read {tweet_id}` (requires TWITTER_COOKIE configured via agent-reach). If twitter-cli is also unavailable or fails, report error to user and do not post to Slack.
- **Channel not found (public)**: Fall back to `slack_search_public_and_private` with `in:{channel_name}` and `channel_types: "private_channel"`. If still not found, ask user to provide correct channel name.
- **Missing thread_ts**: If Message 1 response doesn't include `message_ts`, use `slack_read_channel` to find the most recent message just posted.
- **Tweet has no text**: Still process if media or quote exists; note empty text in summary.

## MCP Tool Reference

| Tool | Server | Purpose |
|---|---|---|
| `slack_search_channels` | `plugin-slack-slack` | Find public channel_id by name |
| `slack_search_public_and_private` | `plugin-slack-slack` | Fallback: find private channel_id via `in:{name}` query |
| `slack_send_message` | `plugin-slack-slack` | Post messages and thread replies |
| `slack_read_channel` | `plugin-slack-slack` | Fallback to find message_ts |
