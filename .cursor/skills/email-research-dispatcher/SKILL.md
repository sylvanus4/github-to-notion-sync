---
name: email-research-dispatcher
description: >-
  Extract research-worthy topics from emails, run web research, and post
  structured findings to Slack. Bridges the gap between incoming information
  requests in email and team-accessible research output. Use when the user asks
  to "research emails", "dispatch email research", "이메일 리서치", "메일에서
  리서치할 것 찾아줘", "email-research-dispatcher", or wants to automatically
  extract research topics from incoming emails and distribute findings. Do NOT
  use for general web research without email input (use parallel-web-search),
  email triage without research (use gmail-daily-triage), or single-URL analysis
  (use x-to-slack or defuddle).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "comms-automation"
---
# email-research-dispatcher

Extract research-worthy topics from emails, run web research, and post structured findings to Slack.

## Workflow

1. **Extract topics** — Scan triaged emails (from `gmail-daily-triage`) for research-worthy content: technology mentions, competitor references, market questions, customer technical queries
2. **Research** — For each topic, run `parallel-web-search` with 3-5 targeted queries; optionally use `defuddle` for linked articles
3. **Synthesize** — Produce a structured finding per topic: summary, key data points, relevance to our products/company, source URLs
4. **Classify & post** — Route findings to appropriate Slack channels: `#deep-research-trending` for tech topics, `#press` for news/competitor items, `#효정-할일` for action-required items
5. **GitHub routing** — If the email contains a bug report or feature request, create a GitHub issue in the appropriate project via `gh` CLI

## Composed Skills

- `gmail-daily-triage` — Email classification and topic extraction
- `parallel-web-search` — Multi-query web research
- `defuddle` — Article content extraction from URLs
- Slack MCP — Channel-specific posting
- GitHub CLI (`gh`) — Issue creation for bug reports / feature requests

## Error Handling

| Error | Action |
|-------|--------|
| No research-worthy emails found | Report "No research topics extracted from today's emails" and exit |
| parallel-web-search returns no results for a topic | Log the topic as "no results", skip to next topic |
| Slack channel not found | Fall back to `#효정-할일` as default channel |
| GitHub issue creation fails | Log error with topic details, continue with remaining topics |
| Rate limiting on web search | Add 5-second delay between topics, retry failed topics at end |

## Examples

```
User: "오늘 메일에서 리서치 필요한 거 뽑아서 슬랙에 올려줘"
→ Scans emails → extracts 3 research topics → runs web search → posts to appropriate Slack channels

User: "email-research-dispatcher"
→ Full pipeline: triage → extract → research → synthesize → post to Slack + create GitHub issues
```
