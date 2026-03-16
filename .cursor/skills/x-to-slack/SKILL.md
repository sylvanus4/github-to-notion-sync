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
  version: "1.1.0"
  category: "execution"
---
# X-to-Slack: Tweet Intelligence Pipeline

Process an X (Twitter) URL, gather context through web research, and post a structured 3-message thread to a specified Slack channel.

## Input

The user provides:
1. **X URL** -- e.g. `https://x.com/user/status/1234567890`
2. **Slack channel name** -- e.g. `#general` or `general`

## Workflow

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
| `deep-research` | `C0A6X68LTN1` | private | 딥 리서치/논문 분석 |
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

### Step 4: Post to Slack (3 Messages)

All messages use Slack mrkdwn format. Rules:
- Use `*bold*` (single asterisk), `_italic_` (underscore)
- Do NOT use `**double asterisks**` or `## headers`
- Write content in Korean
- Limit each message to under 4000 characters

#### Message 1: Title (Channel Post)

Send to the channel using `slack_send_message`:
- Server: `plugin-slack-slack`
- Tool: `slack_send_message`
- Arguments: `channel_id`, `message`

Format:

```
{1-2 line Korean title summarizing the core insight of the tweet}
{original tweet URL (tweet.url)}
>>>
```

The `>>>` at the end creates a blockquote visual separator in Slack.

**CRITICAL**: Capture the `message_ts` (timestamp) from the response. This is needed for thread replies.

#### Message 2: Detailed Summary (Thread Reply)

Send as a thread reply using `slack_send_message` with `thread_ts`:
- Arguments: `channel_id`, `message`, `thread_ts` (from Message 1)

Format:

```
*Tweet 요약*
- 작성자: @{screen_name} ({name})
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

- **FxTwitter API failure**: Report error to user, do not post to Slack.
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
