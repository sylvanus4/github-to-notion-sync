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
  version: "2.0.0"
  category: "comms-automation"
---
# email-research-dispatcher

Extract research-worthy topics from emails, run web research, and post structured findings to Slack.

## Architecture: Fat Subagent Prompt Pattern

Each research topic is processed in an **isolated Task subagent** with a fresh context window.
The orchestrator NEVER performs WebSearch + synthesis + Slack posting inline — it delegates
to subagents so each topic gets full token budget for high-quality research and analysis.

### Why Subagents

Processing N topics (typically 3-8) with 3-5 WebSearch queries each, plus synthesis and
Slack posting, accumulates context rapidly. By topic 3-4 in a single session, research
depth and analysis quality degrade. Per-topic subagents eliminate this degradation.

### Dispatch Loop

```
for each topic in extracted_topics:
  1. Read references/subagent-quality-contract.md
  2. Spawn Task(subagent_type="generalPurpose") with:
     - Full quality contract text (verbatim from reference file)
     - Topic-specific data: topic, email_context, email_subject, email_from
     - Output file path: outputs/email-research/{date}/topic-{index}.json
  3. Wait for subagent completion
  4. Read result JSON from disk
  5. Validate quality_score against thresholds
  6. Wait 12 seconds (Slack rate limiting) before next topic
```

### Subagent Return Contract

```json
{
  "status": "completed|skipped|failed",
  "file": "outputs/email-research/{date}/topic-{index}.json",
  "summary": "one-line Korean outcome",
  "slack_ts": "message_ts if posted",
  "quality_score": { "msg1_chars": 200, "msg2_chars": 500, "websearch_count": 3, "sources_cited": 4 },
  "classification": { "topic_type": "...", "target_channel": "...", "relevance_score": 8 },
  "github_issue": { "created": false, "url": null, "repo": null }
}
```

## Pipeline Output Protocol (File-First)

```
outputs/email-research/{date}/
├── topics-extracted.json     # Phase 1 output: all extracted topics
├── topic-0.json              # Subagent result for topic 0
├── topic-1.json              # Subagent result for topic 1
├── ...
└── manifest.json             # Aggregated pipeline summary
```

## Workflow

### Phase 1: Extract Topics (Orchestrator)

Scan triaged emails (from `gmail-daily-triage` output or direct Gmail query) for
research-worthy content:
- Technology mentions (new tools, frameworks, architectures)
- Competitor references (product launches, pricing changes, partnerships)
- Market questions (industry trends, regulation changes)
- Customer technical queries
- Bug reports or feature requests

For each extracted topic, record: `{ topic, email_context, email_subject, email_from }`.
Write all extracted topics to `outputs/email-research/{date}/topics-extracted.json`.

If no research-worthy topics found: report "No research topics extracted" and exit.

### Phase 2: Per-Topic Subagent Dispatch (Orchestrator → Task subagents)

For each topic in `topics-extracted.json`:

1. **Read** `references/subagent-quality-contract.md` (once, cache for all topics)
2. **Dispatch** `Task(subagent_type="generalPurpose")` with prompt containing:
   - The full quality contract text
   - Topic-specific data (topic, email_context, email_subject, email_from, index)
   - Absolute output file path
3. **Wait** for subagent completion
4. **Validate** result JSON: check `quality_score.websearch_count >= 3`,
   `quality_score.msg1_chars >= 200`, `quality_score.msg2_chars >= 400`
5. **Rate limit** — wait 12 seconds before dispatching next topic

### Phase 3: Aggregate & Report (Orchestrator)

After all topics are processed:

1. Read all `topic-{index}.json` files from the output directory
2. Build `manifest.json` summarizing:
   - Total topics extracted
   - Topics completed / skipped / failed
   - Channels posted to with counts
   - GitHub issues created (if any)
   - Aggregate quality scores
3. Log the summary for pipeline reporting

### Orchestrator Post-Dispatch Responsibilities

- Quality validation: re-check character counts from returned `quality_score`
- Failure handling: log failed topics, continue with remaining
- Rate limiting: 12-second gaps between subagent dispatches
- Manifest generation: aggregate all results into `manifest.json`

## Subagent Internal Processing (reference only)

Each subagent follows the quality contract in `references/subagent-quality-contract.md`:

1. **Web Research** — 3-5 WebSearch queries (core, context, competitive, optional deep-dive)
2. **Classify** — Determine topic_type and target Slack channel
3. **Synthesize** — Korean summary with specific data points and relevance analysis
4. **Post 2-Message Slack Thread** — Header+summary (channel post) + detailed analysis (thread reply)
5. **GitHub Issue** — Create issue if topic_type is bug-report or feature-request
6. **Quality Self-Check** — Verify all checklist items before writing result JSON

## Composed Skills

- `gmail-daily-triage` — Email classification and topic extraction
- `parallel-web-search` — Multi-query web research (used by subagents)
- `defuddle` — Article content extraction from URLs (used by subagents)
- Slack MCP (`plugin-slack-slack`) — Channel-specific posting (used by subagents)
- GitHub CLI (`gh`) — Issue creation for bug reports / feature requests (used by subagents)

## Error Handling

| Error | Action |
|-------|--------|
| No research-worthy emails found | Report "No research topics extracted from today's emails" and exit |
| Subagent Task fails for a topic | Log error with topic details, continue with remaining topics |
| Slack channel not found | Subagent falls back to `#효정-할일` as default channel |
| GitHub issue creation fails | Subagent logs error, continues with remaining steps |
| Rate limiting on web search | Subagent retries with 5-second delay |

## Examples

```
User: "오늘 메일에서 리서치 필요한 거 뽑아서 슬랙에 올려줘"
→ Scans emails → extracts 3 topics → dispatches 3 subagents → each posts to Slack

User: "email-research-dispatcher"
→ Full pipeline: triage → extract → dispatch per-topic subagents → aggregate manifest
```

## Quality Gate

The orchestrator validates each subagent's `quality_score`:

| Metric | Minimum | Action if Below |
|--------|---------|-----------------|
| `websearch_count` | 3 | Log quality warning |
| `msg1_chars` | 200 | Log quality warning |
| `msg2_chars` | 400 | Log quality warning |
| `sources_cited` | 3 | Log quality warning |

Topics with `status: "failed"` are logged but do not block the pipeline.

## File Structure

```
.cursor/skills/pipeline/email-research-dispatcher/
├── SKILL.md                                   # This file (orchestrator logic)
└── references/
    └── subagent-quality-contract.md           # Full quality contract for per-topic subagents
```
