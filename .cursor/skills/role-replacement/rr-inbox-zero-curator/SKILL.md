---
name: rr-inbox-zero-curator
version: 1.0.0
description: >-
  Role Replacement Case Study: Inbox Zero / News Curator — unified entry point for
  email-based and social-media-based news curation with topic classification and Slack routing.
  Thin harness composing gmail-daily-triage, bespin-news-digest, x-to-slack,
  unified-intel-intake, and decision-router into a single news-curator role pipeline
  with cross-source deduplication, topic classification, and provenance-tagged Slack distribution.
tags: [role-replacement, harness, news, email, content]
triggers:
  - rr-inbox-zero-curator
  - inbox zero replacement
  - news curator automation
  - 뉴스 큐레이터 대체
  - 인박스 제로
do_not_use:
  - Single article analysis (use x-to-slack)
  - General Gmail operations (use gws-gmail)
  - Stock market news only (use alphaear-news)
  - Email reply drafting (use gws-email-reply or email-auto-reply)
  - Calendar-related email actions (use smart-meeting-scheduler)
composes:
  - gmail-daily-triage
  - bespin-news-digest
  - x-to-slack
  - twitter-timeline-to-slack
  - unified-intel-intake
  - email-research-dispatcher
  - decision-router
  - memkraft
  - ai-context-router
  - defuddle
---

# Role Replacement: Inbox Zero / News Curator

Thin harness that replaces a human News Curator / Inbox Manager by orchestrating
email triage, newsletter extraction, social media intelligence gathering, and
cross-source topic classification into a unified 6-phase daily pipeline with
deduplication via `intel_registry.py` and Slack distribution.

## What This Replaces

| Human Curator Task | Automated By | Skill |
|---|---|---|
| Morning inbox cleanup | Spam deletion, notification labeling, priority classification | `gmail-daily-triage` |
| Newsletter extraction & analysis | Bespin news email → per-article deep analysis + DOCX report | `bespin-news-digest` |
| Twitter monitoring & summary | Timeline scrape → per-tweet 3-message Slack thread | `twitter-timeline-to-slack` |
| Ad-hoc URL analysis | Content extraction + web research + Slack posting | `x-to-slack` |
| Topic routing to teams | Keyword detection + topic classification + channel routing | `unified-intel-intake` |
| Research topic extraction | Email-to-research-topic identification + web research | `email-research-dispatcher` |
| Decision escalation | Keyword-based scope detection + channel routing | `decision-router` |
| Cross-source deduplication | Central URL registry check before processing | `intel_registry.py` |

## Prerequisites

- `gws` CLI installed and authenticated: `gws auth login -s gmail`
- Slack MCP server connected with `SLACK_BOT_TOKEN` and `SLACK_USER_TOKEN` in `.env`
- `intel_registry.py` accessible at `$RESEARCH_REPO/scripts/intelligence/` (graceful degradation if missing)
- MemKraft memory store initialized for sender/topic pattern recall
- `python-docx` installed for DOCX report generation

## Architecture

```
rr-inbox-zero-curator (thin harness)
  │
  Phase 0 ─→ MemKraft Context Pre-load
  │            ├─ Topic interest patterns (recurring research themes)
  │            ├─ Newsletter sender registry (known digest senders)
  │            └─ Channel routing preferences
  │
  Phase 1 ─→ gmail-daily-triage (email cleanup + classification)
  │            ├─ Trash spam
  │            ├─ Label low-priority notifications
  │            ├─ Extract bespin_news links
  │            ├─ Identify reply-needed emails
  │            └─ Summarize unanswered → .docx
  │
  Phase 2 ─→ bespin-news-digest (newsletter deep analysis)
  │            ├─ Fetch latest Bespin news email
  │            ├─ Extract all article URLs
  │            ├─ Per-article: Jina extract + WebSearch + classify
  │            ├─ 3-message Slack thread per article → #bespin-news
  │            ├─ Consolidated DOCX → Google Drive
  │            └─ Summary → #효정-할일
  │
  Phase 3 ─→ twitter-timeline-to-slack (social media intelligence)
  │            ├─ Fetch latest tweets from tracked accounts
  │            ├─ Dedup via intel_registry.py
  │            ├─ Per-tweet: x-to-slack pipeline (3-message thread)
  │            └─ Topic-based channel routing
  │
  Phase 4 ─→ Cross-Source Synthesis & Routing
  │            ├─ Merge email, newsletter, and social signals
  │            ├─ email-research-dispatcher (extract research topics)
  │            ├─ unified-intel-intake (classify & route any remaining URLs)
  │            └─ decision-router (escalate decision-worthy items)
  │
  Phase 5 ─→ MemKraft Write-back & Daily Digest
               ├─ New topic patterns → MemKraft
               ├─ Sender pattern updates → MemKraft
               └─ Consolidated summary → Slack #효정-할일
```

## Pipeline Output Protocol

All outputs persist to `outputs/rr-inbox-zero-curator/{date}/`.

| Phase | Label | Output File |
|---|---|---|
| 0 | context-preload | `phase-0-context-preload.json` |
| 1 | email-triage | `phase-1-email-triage.json` |
| 2 | newsletter-digest | `phase-2-newsletter-digest.json` |
| 3 | social-intel | `phase-3-social-intel.json` |
| 4 | cross-source-synthesis | `phase-4-cross-source-synthesis.json` |
| 5 | digest-writeback | `phase-5-digest-writeback.json` |

Manifest: `outputs/rr-inbox-zero-curator/{date}/manifest.json` following the standard schema
(`pipeline`, `date`, `started_at`, `completed_at`, `phases[]`, `overall_status`, `warnings[]`).

## Phase 0 — MemKraft Context Pre-load

**Purpose**: Recall topic interest patterns and sender registries before processing.

Invoke `ai-context-router` with:
- Query: `"newsletter senders, topic interests, channel routing rules, recent intel themes, blocked senders"`
- `--recency-boost true`

Extract and persist:
- **Newsletter sender registry**: Known digest senders and their processing rules
- **Topic interest weights**: Which research themes to prioritize (AI/ML, cloud, trading, etc.)
- **Channel routing overrides**: User-specific routing preferences beyond default rules
- **Recently processed topics**: To detect topic saturation and adjust novelty scoring
- **Blocked senders/domains**: Skip list for known low-value sources

```json
{
  "newsletter_senders": [
    { "sender": "bespin@bespinglobal.com", "processor": "bespin-news-digest", "frequency": "daily" }
  ],
  "topic_interests": {
    "ai-ml": 0.9, "cloud-infrastructure": 0.8, "trading": 0.7, "open-source": 0.6
  },
  "channel_routing_overrides": {},
  "recent_topics_7d": ["vLLM optimization", "GPU pricing trends"],
  "blocked_domains": []
}
```

**Persist**: Write to `outputs/rr-inbox-zero-curator/{date}/phase-0-context-preload.json`.

## Phase 1 — Email Triage

Delegate the full `gmail-daily-triage` pipeline. This skill handles its own
file-first persistence.

**Context injection**: Pass Phase 0 data to enhance classification:
- Newsletter sender registry → auto-route known newsletter senders
- Blocked domains → skip without opening
- Topic interests → prioritize emails matching high-interest topics

**Subagent delegation**:

```
Run gmail-daily-triage for {date}.
Context from Phase 0:
- Newsletter senders: {newsletter_senders from phase-0 JSON}
- Blocked domains: {blocked_domains from phase-0 JSON}
- Topic interests for priority ranking: {topic_interests from phase-0 JSON}
Return { status, file, summary }.
Key outputs needed:
- reply_needed_count, reply_needed_top3
- bespin_news_links (URLs extracted from Bespin newsletters)
- research_worthy_topics (subjects worth deeper investigation)
- notification_archived_count
- spam_trashed_count
```

**Persist**: Write summary to `outputs/rr-inbox-zero-curator/{date}/phase-1-email-triage.json`
with pointer to gmail-daily-triage outputs.

## Phase 2 — Newsletter Deep Analysis

Delegate to `bespin-news-digest` for comprehensive newsletter processing.

**Pre-condition**: Phase 1 must have detected at least one Bespin news email. If no
Bespin newsletter found, skip this phase and log `"No Bespin newsletter detected — skipping Phase 2"`.

**Subagent delegation**:

```
Run bespin-news-digest for {date}.
Process ALL articles in the latest Bespin news email.
For each article:
1. Extract content via Jina/defuddle
2. Run WebSearch for context
3. Classify AI GPU Cloud relevance
4. Post 3-message Slack thread to #bespin-news
5. Check intel_registry.py for dedup before posting
Generate consolidated DOCX and upload to Google Drive.
Post summary to #효정-할일.
Return { status, file, summary, article_count, drive_url }.
```

**Persist**: Write to `outputs/rr-inbox-zero-curator/{date}/phase-2-newsletter-digest.json`.

## Phase 3 — Social Media Intelligence

Delegate to `twitter-timeline-to-slack` for tracked account monitoring.

**Tracked accounts**: Configured in `outputs/rr-inbox-zero-curator/config.json`
(or default to `hjguyhan` if config missing).

**Deduplication**: Each tweet URL is checked against `intel_registry.py` before
processing. Already-processed tweets are skipped.

**Channel routing**: Inherits from `twitter-timeline-to-slack` default rules:
- Claude/Cursor AI coding topics → `#ai-coding-radar`
- General press/media → `#press`
- Never `#random`

**Subagent delegation**:

```
Run twitter-timeline-to-slack for accounts: {tracked_accounts}.
Dedup each tweet via intel_registry.py before processing.
For each new tweet: run x-to-slack pipeline (3-message Slack thread).
Return { status, file, summary, tweets_processed, tweets_skipped_dedup }.
```

**Persist**: Write to `outputs/rr-inbox-zero-curator/{date}/phase-3-social-intel.json`.

## Phase 4 — Cross-Source Synthesis & Routing

Merge intelligence from all three sources (email, newsletter, social) and perform
cross-source analysis.

### Step 4a: Research Topic Extraction

Read Phase 1 outputs. If `research_worthy_topics` exist, invoke `email-research-dispatcher`:

```
Extract research-worthy topics from today's emails.
Topics identified in triage: {research_worthy_topics from phase-1 JSON}
Run web research for each topic.
Post structured findings to appropriate Slack channels.
Return { status, topics_researched, slack_posts }.
```

### Step 4b: Remaining URL Processing

Read Phase 1 and Phase 2 outputs for any URLs not yet processed through the
newsletter or social pipelines. Route through `unified-intel-intake`:

```
Process remaining URLs from today's email and newsletter outputs.
Classify each by content type (news, paper, tweet, blog) and topic.
Route to appropriate processing skill and Slack channel.
Return { status, urls_processed, urls_skipped }.
```

### Step 4c: Decision Routing

Invoke `decision-router` to scan all Phase 1-3 outputs for decision-worthy items:

```
Scan today's intel outputs for decision-worthy items.
Sources:
- Email triage: {reply_needed emails with strategic implications}
- Newsletter: {articles requiring strategic response}
- Social: {tweets signaling competitive or market changes}
Route:
- Personal decisions → #효정-의사결정
- Team/CTO decisions → #7층-리더방
Return { status, decisions_routed, channels_used }.
```

### Step 4d: Cross-Source Topic Convergence

Identify topics that appear across 2+ sources (email + newsletter, newsletter + Twitter, etc.).
These convergent signals indicate higher-importance trends.

```json
{
  "convergent_topics": [
    {
      "topic": "vLLM performance optimization",
      "sources": ["bespin-newsletter", "twitter/@vaborogang"],
      "signal_strength": "HIGH",
      "recommended_action": "Deep research via parallel-deep-research"
    }
  ]
}
```

**Persist**: Write to `outputs/rr-inbox-zero-curator/{date}/phase-4-cross-source-synthesis.json`.

## Phase 5 — MemKraft Write-back & Daily Digest

### Step 5a: MemKraft Write-back

Write session learnings back to MemKraft via `memkraft-ingest`:

1. **New sender patterns**: Newsletter senders discovered during email triage
2. **Topic frequency updates**: Topics that appeared today (for saturation tracking)
3. **Channel routing adjustments**: Corrections from misrouted content
4. **Research follow-ups**: Open research threads to continue tomorrow

Write with provenance tag `source: rr-inbox-zero-curator`.

### Step 5b: Daily Digest Assembly

Generate a consolidated daily intelligence digest summarizing all phases:

```markdown
## 뉴스 큐레이터 일일 다이제스트 — {YYYY-MM-DD}

### 이메일 현황
- 스팸 삭제: {spam_trashed_count}건
- 알림 정리: {notification_archived_count}건
- 답장 필요: {reply_needed_count}건

### 뉴스레터 분석
- Bespin 뉴스: {article_count}건 분석 완료
- DOCX 리포트: {drive_url}
- 주요 토픽: {top_3_topics}

### 소셜 인텔리전스
- 트윗 처리: {tweets_processed}건
- 중복 스킵: {tweets_skipped_dedup}건

### 크로스 소스 시그널
- 수렴 토픽: {convergent_topic_count}건 (2+ 소스 교차)
- 리서치 디스패치: {topics_researched}건
- 의사결정 라우팅: {decisions_routed}건

### 큐레이터 추천 액션
1. {highest priority follow-up}
2. {second priority}
3. {items to watch tomorrow}
```

Post to Slack `#효정-할일` as a threaded summary.

**Persist**: Write to `outputs/rr-inbox-zero-curator/{date}/phase-5-digest-writeback.json`.

## Deduplication Protocol

Cross-repo URL deduplication is enforced at every content processing boundary:

```bash
RESEARCH_REPO="${RESEARCH_REPO:-$HOME/thaki/research}"
python3 "$RESEARCH_REPO/scripts/intelligence/intel_registry.py" check "<url>"
```

- **Exit 0 (new)**: Proceed with processing.
- **Exit 1 (duplicate)**: Skip and log. Do NOT post to Slack.
- **Registry missing**: Log warning and proceed (graceful degradation).

After successful Slack posting, register the URL:

```bash
python3 "$RESEARCH_REPO/scripts/intelligence/intel_registry.py" save \
  "<url>" "<artifact_path>" \
  --type <tweet|article|newsletter> \
  --channel "<channel_name>" \
  --ts "<message_ts>" \
  --topic intelligence
```

## Topic Classification & Channel Routing

Inherits from `unified-intel-intake` and `x-to-slack` channel registries:

| Topic | Slack Channel | Channel ID |
|---|---|---|
| AI coding agents/tools | `#ai-coding-radar` | `C0A7K3TBPK7` |
| Press/media/content | `#press` | `C0A7NCP33LG` |
| Research/papers/tech analysis | `#deep-research-trending` | `C0AN34G4QHK` |
| Prompt engineering/LLM techniques | `#prompt` | `C0A98HXSVMK` |
| Ideas/brainstorming | `#idea` | `C0A6U3HE3GS` |
| Bespin Global news | `#bespin-news` | (via `bespin-news-digest`) |
| Personal tasks/summaries | `#효정-할일` | `C0AA8NT4T8T` |
| Stock/investment intel | `#효정-주식` | `C0A7V1A09NK` |
| Strategic insights | `#효정-insight` | `C0A8SSPC9RU` |

**Routing rules**:
- Claude/Cursor-specific content → `#ai-coding-radar` ONLY
- Never `#random` for automated posts
- Decision-worthy items → `decision-router` (personal vs team routing)

## Memory Configuration

| Tier | Content | Retention |
|---|---|---|
| HOT | Today's unprocessed URLs, active research threads, pending replies | Session-scoped, 24h |
| WARM | Sender classification patterns, topic frequency histogram, channel routing corrections | 30 days, decayed by attention_decay.py |
| Knowledge | Channel registry, newsletter sender list, topic taxonomy, Slack formatting rules | Persistent in `memory/topics/slack-routing.md`, `memory/topics/preferences.md` |

### MemKraft Integration Points

| Point | Direction | Data |
|---|---|---|
| Phase 0 pre-load | READ | Sender registry, topic interests, routing overrides |
| Phase 4 synthesis | READ | Recent topic frequency for convergence detection |
| Phase 5 write-back | WRITE | New sender patterns, topic updates, routing corrections |

## Error Recovery

| Phase | Failure | Action |
|---|---|---|
| 0 (Context Pre-load) | MemKraft unavailable | Proceed without context enrichment; use default routing rules |
| 1 (Email Triage) | Gmail auth expired | Report error, skip to Phase 3 (social intel can run independently) |
| 2 (Newsletter Digest) | No Bespin email found | Skip phase, log info-level message |
| 2 (Newsletter Digest) | Jina/defuddle extraction fails for an article | Skip that article, continue with remaining; log warning |
| 3 (Social Intel) | FxTwitter API failure | Use agent-reach Twitter fallback; if both fail, skip tweet |
| 3 (Social Intel) | Rate limiting | Process remaining tweets in next invocation; persist progress |
| 4 (Cross-Source) | Research dispatch fails | Skip research; other routing continues |
| 5 (Digest) | Slack posting fails | Write digest to local file; retry Slack in next invocation |

Resume from the last successful `phase-*.json` under `outputs/rr-inbox-zero-curator/{date}/`.

## Security Rules

- No automatic email sending (classification and drafts only)
- No email deletion beyond spam trash (notifications are labeled, not deleted)
- No Gmail filter creation without user confirmation
- No credential or secret content in Slack posts
- Spam email bodies are NOT opened (classification by sender/subject metadata only)
- Social media API calls use public endpoints only (no credential scraping)

## Honest Reporting

- Report outcomes faithfully — never claim all phases passed when any failed
- Never suppress errors, partial results, or skipped phases
- Surface unexpected findings even if they complicate the narrative
- If a phase produces no actionable output, say so explicitly

## Coordinator Synthesis

- Do not reconstruct phase outputs from chat context — always read from persisted files
- Each phase dispatch includes a purpose statement explaining the expected transformation
- File paths and line numbers must be specific, not inferred
- Never delegate with vague instructions like "analyze this" — provide concrete specs

## Subagent Contract

Every subagent dispatch MUST include:
1. **Purpose statement** — one sentence explaining why this subagent exists
2. **Absolute file paths** — all input/output paths as absolute paths
3. **Return contract** — subagent must return JSON: `{"status": "ok|error", "file": "<output_path>", "summary": "<1-line>"}`
4. Load-bearing outputs must be written to disk, not passed via chat context

## Operational Runbook

### Daily Execution

```bash
# Typical invocation (morning routine)
> rr-inbox-zero-curator

# As part of daily-am-orchestrator:
> /daily-am  # Phase 4 triggers this skill

# Newsletter-only mode (skip email triage and social)
> rr-inbox-zero-curator --newsletter-only

# Social-only mode (skip email and newsletter)
> rr-inbox-zero-curator --social-only
```

### Configuration

Edit `outputs/rr-inbox-zero-curator/config.json`:

```json
{
  "tracked_twitter_accounts": ["hjguyhan"],
  "newsletter_senders": ["bespin@bespinglobal.com"],
  "skip_phases": [],
  "convergence_threshold": 2,
  "max_tweets_per_run": 20
}
```

### Health Check

Verify prerequisites before first run:
1. `gws auth status` — Gmail auth valid
2. `.env` contains `SLACK_BOT_TOKEN` and `SLACK_USER_TOKEN`
3. `python3 "$RESEARCH_REPO/scripts/intelligence/intel_registry.py" check "test"` — registry accessible
4. `outputs/rr-inbox-zero-curator/` directory is writable

## Comparison: Human News Curator vs This Skill

| Dimension | Human Curator | rr-inbox-zero-curator |
|---|---|---|
| Cost | $3,000-6,000/mo (part-time) | ~$3-8/day (API + compute) |
| Speed | 2-3 hours for full scan | 15-30 minutes pipeline |
| Coverage | 1-2 sources deeply | 3+ sources in parallel |
| Consistency | Variable attention | Deterministic classification |
| Deduplication | Manual memory | Central URL registry |
| Cross-source detection | Requires deep domain knowledge | Automated convergence scoring |
| Judgment | Superior for nuance and relevance | Rule-based with MemKraft pattern learning |
| Language processing | Native fluency | Korean + English with translation |
| Scalability | Fixed throughput | Scales with API capacity |

### Where Human Curator Still Wins

- Nuanced relevance judgment for ambiguous content
- Relationship-based source curation (knowing which authors to follow)
- Editorial voice and narrative framing
- Detecting subtle sentiment shifts that keyword classifiers miss
- Building and maintaining source relationships

## Examples

### Example 1: Standard morning run

**User says**: "rr-inbox-zero-curator" or "인박스 제로 실행"

**Actions**:
1. Phase 0: Load MemKraft context (sender registry, topic interests)
2. Phase 1: Triage 45 emails — 12 spam trashed, 18 notifications labeled, 8 replies needed, 1 Bespin newsletter detected
3. Phase 2: Process Bespin newsletter — 6 articles extracted, each gets 3-message Slack thread in #bespin-news, DOCX uploaded to Drive
4. Phase 3: Process @hjguyhan timeline — 4 new tweets (2 already in registry, 2 processed), routed to #press and #ai-coding-radar
5. Phase 4: Cross-reference — "vLLM optimization" appears in both newsletter and tweet → convergence signal flagged. 2 research topics dispatched. 1 decision item routed to #효정-의사결정
6. Phase 5: Write 2 new topic patterns to MemKraft. Post daily digest to #효정-할일

**Result**: Inbox at zero, all intelligence curated and distributed, convergent signals flagged.

### Example 2: Newsletter-only mode

**User says**: "rr-inbox-zero-curator --newsletter-only"

**Actions**:
1. Phase 0: Load MemKraft context
2. Phase 2: Process Bespin newsletter only
3. Phase 5: Abbreviated digest

**Result**: Newsletter analysis without email triage or social media processing.

### Example 3: Ad-hoc URL processing

**User says**: "이 URL도 분석해줘: https://x.com/karpathy/status/123456"

**Actions**: Routed to `x-to-slack` pipeline directly (single URL falls outside this harness's batch scope). This harness handles scheduled batch processing, not ad-hoc single URLs.
