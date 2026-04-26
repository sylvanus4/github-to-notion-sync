---
name: unified-intel-intake
description: >-
  Single entry point for all intelligence sources — news articles, academic
  papers, tweets, blog posts, and RSS feeds. Auto-classifies content type
  and topic, routes to the appropriate processing skill, and posts to the
  correct Slack channel. Use when the user asks to "process this link",
  "classify and route content", "unified intel", "인텔 파이프라인",
  "통합 인텔리전스", "unified-intel-intake", or wants a single pipeline for
  all external information sources. Do NOT use for processing a single tweet
  (use x-to-slack), Bespin news only (use bespin-news-digest), or paper
  review (use paper-review directly).
metadata:
  version: "1.0.0"
  category: "execution"
  author: "thaki"
---
# Unified Intel Intake

Single pipeline that accepts any URL or content source, classifies it, routes to the appropriate processing skill, and delivers to the right Slack channel.

## When to Use

- As part of the daily Intel track in the SOD-to-EOD pipeline
- When processing a batch of mixed URLs (news, papers, tweets)
- When setting up RSS feed monitoring for automatic intake

## Content Type Detection

| Pattern | Type | Processing Skill |
|---------|------|-----------------|
| `arxiv.org`, `*.pdf` (academic) | Paper | `paper-review` or `alphaxiv-paper-lookup` |
| `x.com`, `twitter.com` | Tweet | `x-to-slack` |
| `huggingface.co/papers` | HF Paper | `hf-trending-intelligence` |
| `github.com` (repo/release) | GitHub | `defuddle` + LLM summary |
| `youtube.com`, `youtu.be` | Video | `defuddle` (transcript extraction) + LLM analysis |
| News domains (techcrunch.com, theverge.com, arstechnica.com, wired.com, reuters.com, bloomberg.com, venturebeat.com, zdnet.com, theregister.com, semafor.com), RSS items from news feeds | News Article | `defuddle` + LLM analysis |
| medium.com, substack.com, dev.to, hashnode.dev, personal domains with blog-like URL paths (`/posts/`, `/blog/`, `/articles/`) | Blog | `defuddle` + LLM analysis |
| Unknown domain — extract with `defuddle`, then use LLM to classify based on content structure (byline, dateline, article length → News; personal voice, opinion-heavy → Blog) | Auto-detect | `defuddle` + LLM classification + LLM analysis |

## Topic Classification

After content extraction, classify by primary topic. If multiple topics match, use the one with the strongest keyword density. If tied, prefer the more specific topic (e.g., "Security" over "General Tech"):

| Topic | Keywords | Target Channel |
|-------|----------|---------------|
| AI/ML Infrastructure | GPU, CUDA, inference, training, cluster | `#deep-research-trending` |
| Kubernetes/Cloud Native | K8s, Helm, service mesh, CNCF | `#deep-research-trending` |
| Security | CVE, vulnerability, breach, zero-day | `#security-alerts` |
| Market/Business | funding, acquisition, IPO, revenue | `#market-intel` |
| Research/Papers | paper, arxiv, model, benchmark | `#deep-research-trending` |
| General Tech | framework, library, release, update | `#tech-news` |

## Architecture: Fat Subagent Prompt Pattern

Each URL is processed in an isolated `Task` subagent with a fresh context window.
The orchestrator reads the quality contract from `references/subagent-quality-contract.md`
and embeds it into each subagent prompt alongside item-specific data.

### Why Subagents

Processing N URLs in a single session causes context window exhaustion by item 3-5.
Each subagent gets a fresh context with the full quality contract, producing consistent
quality regardless of batch position.

### Dispatch Loop

```
for each URL in input list:
  1. Pre-classify content type from URL pattern (lightweight, no extraction)
  2. If tweet/paper/hf_paper → route to dedicated skill directly (no subagent needed)
  3. Otherwise → spawn Task(subagent_type="generalPurpose") with:
     - Full quality contract (from references/subagent-quality-contract.md)
     - URL, detected_type, output_file path, index
  4. Wait for subagent completion
  5. Read result JSON from output_file
  6. If result has decision_type → invoke decision-router
  7. Wait 10-15s (Slack rate limiting) before next item
```

### Subagent Return Contract

```json
{
  "status": "completed|skipped|failed",
  "file": "outputs/unified-intel/{date}/item-{index}.json",
  "summary": "one-line Korean outcome",
  "slack_ts": "message_ts (if posted)",
  "quality_score": {
    "msg1_chars": 80,
    "msg2_chars": 800,
    "msg3_chars": 400,
    "websearch_count": 2,
    "extraction_method": "defuddle|webfetch|transcript"
  },
  "classification": {
    "content_type": "news|blog|release|video|github",
    "topic": "ai-infra|k8s|security|market|research|general",
    "relevance_score": 8,
    "urgency": "immediate|daily|weekly"
  }
}
```

## Workflow

### Phase 1: Accept Input (Orchestrator)

Accept one or more content sources:
- Direct URL(s)
- RSS feed URL (poll for new items)
- Gmail message with links (from `gmail-daily-triage`)
- Slack message with shared link

### Phase 2: URL Pre-Classification (Orchestrator — lightweight)

For each URL, pattern-match to detect content type WITHOUT extraction:

| URL Pattern | `detected_type` | Routing |
|-------------|-----------------|---------|
| `arxiv.org` | `paper` | Delegate to `paper-review` or `alphaxiv-paper-lookup` directly |
| `x.com`, `twitter.com` | `tweet` | Delegate to `x-to-slack` directly |
| `huggingface.co/papers` | `hf_paper` | Delegate to `hf-trending-intelligence` directly |
| `youtube.com`, `youtu.be` | `video` | → subagent |
| `github.com` | `github` | → subagent |
| Known news domains | `news` | → subagent |
| Blog-like domains/paths | `blog` | → subagent |
| Everything else | `unknown` | → subagent |

Tweets, papers, and HF papers are routed to their dedicated skills directly by
the orchestrator — no subagent needed for these since they already have their
own session-isolated pipelines.

### Phase 3: Per-URL Subagent Dispatch (Orchestrator → Task subagents)

For each URL that needs subagent processing:

1. Read `references/subagent-quality-contract.md`
2. Spawn `Task(subagent_type="generalPurpose")` with the full quality contract
   and item-specific data (`url`, `detected_type`, `output_file`, `index`)
3. Wait for subagent to complete
4. Read result JSON from `output_file`
5. Wait 10-15 seconds before dispatching the next subagent (Slack rate limiting)

### Phase 4: Post-Dispatch Processing (Orchestrator)

After all subagents complete:

1. **Decision routing**: For items with `decision_type` set, invoke `decision-router`
   - `decision_personal` → `#효정-의사결정`
   - `decision_team` → `#7층-리더방`

2. **Quality validation**: Check each result's `quality_score`:
   - `msg2_chars >= 600` (minimum for substantive summary)
   - `msg3_chars >= 300` (minimum for action items)
   - `websearch_count >= 2` (mandatory research)
   - Log warnings for items below thresholds

3. **Aggregate daily report**: Produce a digest of all processed intel:

```
Daily Intel Digest
==================
Sources Processed: 23
  Papers: 5 (2 full reviews, 3 quick summaries)
  News: 12 (8 relevant, 4 skipped)
  Tweets: 4
  Releases: 2

Top Stories:
1. [Paper] Scaling LLM Inference on K8s — Relevance: 9/10
2. [News] NVIDIA H200 Production Ramp — Relevance: 8/10
3. [Tweet] @karpathy on efficient fine-tuning — Relevance: 7/10
```

### Subagent Internal Processing (reference only)

Each subagent follows the quality contract in `references/subagent-quality-contract.md`:
1. Extract content via `defuddle` (or `WebFetch` fallback)
2. Classify: content_type, topic, relevance_score, urgency
3. If relevance < 5 → skip (write result with `status: "skipped"`)
4. Mandatory web research (2-3 queries)
5. Post 3-message Slack thread to classified channel
6. Self-check quality gates
7. Write result JSON to `output_file`

## Error Handling

| Error | Action |
|-------|--------|
| Unsupported URL format | Log and skip; report "Unsupported URL: <url>" in daily digest; suggest defuddle or x-to-slack for manual processing |
| Content extraction fails | Retry with defuddle; if still fails, log URL and skip; include in digest as "Failed to extract" |
| Classification confidence too low | Route to `#tech-news` for manual review; log with low-confidence flag in daily digest |
| Target channel not found | Fall back to default channel (e.g. `#deep-research-trending`); log channel mapping error for config fix |
| Duplicate content detected | Skip processing; log and deduplicate against recent intake; do not post to Slack |

## Examples

### Example 1: Batch URL processing
User says: "Process these links" + list of URLs
Actions:
1. Extract content from each URL
2. Classify type and topic
3. Route to appropriate skills
4. Post to correct Slack channels
Result: All links processed and distributed

### Example 2: RSS monitoring
User says: "Monitor this RSS feed for relevant items"
Actions:
1. Poll RSS feed for new items
2. Filter by relevance score >= 5
3. Process relevant items through pipeline
Result: Continuous monitoring with automatic Slack posting
