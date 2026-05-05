---
name: chinese-news-digest
description: >-
  Fetch trending content from 3 Chinese news aggregation platforms (NewsNow,
  TopHub Today Tech, SoPilot Hot Tweets), extract top news items, categorize
  each for the appropriate Slack channel, perform web research, and post
  x-to-slack format 3-message threaded summaries to Slack. ALWAYS invoke when
  the user asks to "run Chinese news digest", "중국 뉴스 다이제스트",
  "chinese-news-digest", "중국 뉴스 정리", "중국 트렌딩", "NewsNow 뉴스",
  "今日热榜", "SoPilot", "중국 뉴스 슬랙에 올려줘", "중국 뉴스 수집",
  "chinese news to slack", "중국 핫토픽", or wants daily Chinese-language
  tech/social trend intelligence posted to Slack. Do NOT use for single tweet
  analysis (use x-to-slack). Do NOT use for Bespin news email processing (use
  bespin-news-digest). Do NOT use for general web research without Chinese
  source intent (use parallel-web-search). Do NOT use for HuggingFace trending
  scan (use hf-trending-intelligence).
metadata:
  author: "thaki"
  version: "2.1.0"
  category: "pipeline"
---

# Chinese News Digest Pipeline

Fetch trending topics from 3 Chinese aggregation platforms, select the top 5
most newsworthy items, categorize each for the right Slack channel, run web
research per item, and post x-to-slack format 3-message threads.

> **Pattern**: mirrors `bespin-news-digest` -- sequential processing with
> mandatory WebSearch per item. Direct `scripts/slack_post_message.py` for
> Slack posting (not MCP `slack_send_message`).

## Sources

| # | Platform | URL | Content Type |
|---|----------|-----|-------------|
| 1 | NewsNow (多平台聚合) | `https://newsnow.busiyi.world` | Zhihu, Weibo, Bilibili, Hupu, V2EX aggregation |
| 2 | TopHub Today (今日热榜 - Tech) | `https://tophub.today/c/tech` | GitHub Trending, Product Hunt, Hacker News, tech circle |
| 3 | SoPilot (X Hot Tweets) | `https://sopilot.net/zh/hot-tweets` | X/Twitter viral posts, opinion trends |

## Slack Channel Registry

Categorize each news item to the most appropriate channel:

| Channel Name | Channel ID | When to Use |
|---|---|---|
| `deep-research-trending` | `C0AN34G4QHK` | AI/ML research, deep tech, academic papers, benchmarks |
| `ai-coding-radar` | `C0A7K3TBPK7` | AI coding agents, dev tools, Claude/Cursor/Copilot news |
| `press` | `C0A7NCP33LG` | General tech news, product launches, business/media, social trends |
| `효정-할일` | `C0AA8NT4T8T` | Actionable items requiring personal follow-up |
| `효정-insight` | `C0A8SSPC9RU` | Strategic insights, market analysis |

**Default channel**: `#press` (`C0A7NCP33LG`) when categorization is ambiguous.

## Constraints

**Freedom level**: Low -- follow the 6-step workflow exactly. Do not skip steps,
reorder phases, or invent new output formats.

- All Slack messages in Korean
- Use `scripts/slack_post_message.py` for posting (user identity, not bot)
- NEVER use `slack_send_message` MCP tool for text posts
- Message 1 is plain text only (no mrkdwn formatting)
- Messages 2-3 use `mrkdwn` formatting (`*bold*`, `_italic_`)
- Sequential processing: post all 3 messages for item N before starting item N+1
- Rate limiting: 2-second pause between items to avoid Slack throttling
- Do not add commentary, emojis, or embellishments beyond the specified format
- Match output length to content -- do not pad thin news items with speculation

## Workflow

### Step 1: Fetch Content from All 3 Sources

Use `WebFetch` to retrieve content from each source URL. If a source times out,
retry once. If it still fails, skip that source and proceed with remaining
sources (log a warning).

### Step 2: Extract Top News Items

From the combined content across all 3 sources, identify the **top 5** most
newsworthy items using these criteria:

1. **Impact**: How broadly does this affect the tech/AI/product ecosystem?
2. **Novelty**: Is this genuinely new information (not rehashed)?
3. **Relevance**: Does it matter for AI platform strategy, GPU cloud, or dev tools?
4. **Engagement**: High social engagement signals (likes, comments, shares)
5. **Diversity**: Avoid clustering -- pick items from different topics/sources

For each item, extract:
- **Title**: Original Chinese title (or closest equivalent)
- **Summary**: 2-3 sentence summary in Korean
- **Source platform**: Which of the 3 sources it came from
- **Original URL**: Direct link if available; otherwise the source platform URL
- **Category**: Channel assignment (Step 3)

### Step 3: Categorize for Slack Channels

Assign each item to a Slack channel from the Channel Registry above.
Classification rules:

| Topic Pattern | Channel |
|---|---|
| LLM, foundation model, benchmark, training, inference optimization | `deep-research-trending` |
| AI agent, coding assistant, IDE, developer tool, MCP, Claude, Cursor, Copilot | `ai-coding-radar` |
| Product launch, funding, IPO, social trend, general tech, consumer AI | `press` |
| Actionable for personal workflow (tool to adopt, account to create) | `효정-할일` |
| Strategic market signal, competitive intelligence | `효정-insight` |

### Step 4: Web Research per Item

For each of the 5 items, run `WebSearch` with 2-3 targeted queries to gather:
- Additional context and background
- English-language coverage of the same topic
- Related developments or competing perspectives

### Step 5: Post to Slack (3-Message Thread per Item)

Post each item as a 3-message thread using `scripts/slack_post_message.py`.

#### Message 1: Title + URL (initial post)

```bash
python3 scripts/slack_post_message.py \
    --channel "{channel_id}" \
    --message "{Korean headline}\n{source_url}"
```

**Strict rules for Message 1:**
- EXACTLY 2-3 lines: Korean headline + URL
- NO emojis, NO bold (`*`), NO italic (`_`), NO `mrkdwn` formatting
- Plain text only
- One sentence summarizing the core insight in Korean
- Source URL on the next line

Parse the JSON output to capture `ts` for threading.

#### Message 2: Detailed Summary + Research (thread reply)

```bash
python3 scripts/slack_post_message.py \
    --channel "{channel_id}" \
    --message "{detailed_message}" \
    --thread-ts "{message_1_ts}"
```

Format (Korean, `mrkdwn`):

```
*[Source Platform] 상세 분석*

*핵심 내용*
{3-5 bullet points summarizing the news item}

*배경 및 맥락*
{Background context from web research}

*웹 리서치 결과*
{Key findings from WebSearch -- additional coverage, expert opinions}

*관련 링크*
- {link 1}
- {link 2}
```

#### Message 3: AI/Strategic Insights (thread reply)

```bash
python3 scripts/slack_post_message.py \
    --channel "{channel_id}" \
    --message "{insights_message}" \
    --thread-ts "{message_1_ts}"
```

Format (Korean, `mrkdwn`):

```
*AI/전략 인사이트*

*시사점*
{What this means for AI platform strategy, GPU cloud, or the broader ecosystem}

*액션 아이템*
{Specific actions to consider -- if any}

*경쟁 영향*
{Impact on competitors or market positioning -- if relevant}
```

### Step 6: Completion Summary

After all 5 items are posted, output a summary:

```
중국 뉴스 다이제스트 완료
- 처리된 항목: 5
- 채널별 분포: #press (N), #ai-coding-radar (N), #deep-research-trending (N)
- 소스별 분포: NewsNow (N), TopHub (N), SoPilot (N)
```

## Verification Protocol

Before declaring the pipeline complete, verify:

1. All 3 sources were attempted (log skipped sources with reason)
2. Each posted item has exactly 3 messages (initial + 2 thread replies)
3. Message 1 contains NO mrkdwn formatting (plain text only)
4. Thread replies reference the correct `message_1_ts`
5. No duplicate stories were posted across channels

```
VERDICT: PASS — all 5 items posted with 3-message threads
VERDICT: FAIL — {N} items failed: {reason}
```

Report the verdict honestly at Step 6.

## Output Discipline

- Do not add features or sections beyond the 3-message format
- If a news item has thin content, write a shorter summary -- do not pad
- Do not speculate about implications without evidence from WebSearch
- Match Korean output length to actual content density
- If fewer than 5 newsworthy items exist, post only what qualifies -- do not fill quota with low-quality items

## Honest Reporting

- Report outcomes faithfully: if sources returned no usable content, say so
- Never claim "all items posted successfully" without verifying each `ts` response
- If WebSearch returns no relevant results for an item, state that explicitly in Message 2 rather than fabricating context
- Report source fetch failures, Slack errors, and skipped items transparently

## Required Tools

| Tool | Purpose |
|---|---|
| `WebFetch` | Fetch content from 3 source URLs |
| `WebSearch` | Research each news item for context |
| `Shell` | Execute `scripts/slack_post_message.py` for Slack posting |

## Gotchas

| Symptom | Root Cause | Correct Approach |
|---------|-----------|-----------------|
| WebFetch returns garbled HTML with no readable content | Source uses heavy JS rendering | Try fetching the mobile/API variant, or extract what text is available and supplement with WebSearch |
| WebFetch timeout on any source | Network instability or source downtime | Retry once, then skip source with warning and proceed with remaining sources |
| Same story appears in all 3 sources | Viral content cross-platform | Consolidate into one item; note multi-source coverage in Message 2 |
| `slack_post_message.py` returns `{"ok": false}` | Channel ID mismatch or token expired | Verify channel ID from registry; check SLACK_USER_TOKEN in .env |
| Thread replies post as top-level messages | Missing or malformed `--thread-ts` | Ensure `ts` is parsed from Message 1 JSON output as string (not truncated float) |
| Chinese content renders as mojibake in Slack | Encoding issue in shell escaping | Use heredoc or write message to temp file, then pass via `--message-file` if available |
| Fewer than 5 newsworthy items across all sources | Low-activity period or source issues | Post only qualifying items; do not pad with low-quality fillers |

## Example Invocation

```
/chinese-news-digest
chinese-news-digest
중국 뉴스 다이제스트 실행
중국 뉴스 정리해줘
중국 트렌딩 슬랙에 올려줘
```
