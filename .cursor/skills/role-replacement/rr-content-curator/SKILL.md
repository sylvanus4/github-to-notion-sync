---
name: rr-content-curator
version: 1.0.0
description: >-
  Role Replacement Case Study: Content Curator / Media Intelligence — unified content
  intelligence pipeline that replaces a dedicated content curator by orchestrating
  multi-source intake (Twitter timelines, company news emails, ad-hoc URLs), topic
  classification with Slack channel routing, batch processing with cross-repo dedup,
  content repurposing for high-value items, and daily velocity reporting. Thin harness
  composing twitter-timeline-to-slack, x-to-slack, bespin-news-digest, unified-intel-intake,
  content-repurposing-engine, and decision-router into a unified content curation role
  pipeline with MemKraft-powered editorial memory, quality gate enforcement, and
  automated Slack distribution across 11+ channels.
tags: [role-replacement, harness, content, media, intelligence, curation, multi-source]
triggers:
  - rr-content-curator
  - content curator replacement
  - media intelligence automation
  - content curation pipeline
  - daily content intake
  - multi-source intel pipeline
  - 콘텐츠 큐레이터 대체
  - 미디어 인텔리전스
  - 콘텐츠 파이프라인
  - 일일 콘텐츠 인테이크
  - 멀티소스 인텔 파이프라인
do_not_use:
  - Single tweet URL without pipeline orchestration (use x-to-slack directly)
  - General Slack messaging without content curation context (use kwp-slack-slack-messaging)
  - Stock market news aggregation without content curation (use alphaear-news)
  - Paper review without curation pipeline (use paper-review)
  - Podcast repurposing (use marketing-podcast-ops)
  - Brand voice enforcement without content context (use kwp-brand-voice-brand-voice-enforcement)
composes:
  - twitter-timeline-to-slack
  - x-to-slack
  - bespin-news-digest
  - unified-intel-intake
  - content-repurposing-engine
  - content-repurposing-engine-pro
  - decision-router
  - memkraft
  - ai-context-router
  - tech-trend-analyzer
  - defuddle
  - long-form-compressor
  - sentence-polisher
  - hook-generator
---

# Role Replacement: Content Curator / Media Intelligence

## Human Role Being Replaced

A dedicated Content Curator who manually:
- Monitors 5+ Twitter accounts, company newsletters, and RSS feeds daily
- Reads each article, classifies by topic and relevance, routes to the correct Slack channel
- Performs web research to add context and implications to raw content
- Identifies decision-worthy items and escalates to leadership
- Repurposes high-value content for LinkedIn, newsletter, and internal distribution
- Tracks what has been processed to avoid duplicates across machines and sessions
- Maintains editorial memory of recurring topics, preferred sources, and channel routing preferences

This skill replaces 3-4 hours of daily manual curation work.

## Architecture

```
Phase 0: MemKraft Context Pre-load
  └─ ai-context-router → editorial memory, channel preferences, source quality scores

Phase 1: Multi-Source Intake (parallel fan-out)
  ├─ 1A: twitter-timeline-to-slack (batch: default @hjguyhan + configured accounts)
  ├─ 1B: bespin-news-digest (company newsletter pipeline)
  └─ 1C: unified-intel-intake (ad-hoc URLs, RSS items, Gmail-forwarded links)

Phase 2: Quality Assurance & Gap Analysis
  └─ Cross-source theme detection → coverage gap identification

Phase 3: High-Value Content Repurposing (conditional)
  └─ content-repurposing-engine → multi-platform output for top items

Phase 4: Decision Routing & Daily Digest
  ├─ decision-router → #효정-의사결정 / #7층-리더방
  └─ Daily velocity report → #효정-할일

Phase 5: MemKraft Write-back & Session Close
  └─ Update editorial memory: new sources, topic trends, routing corrections
```

## Execution

### Phase 0: MemKraft Context Pre-load

Before processing any content, load editorial context from personal memory:

```
ai-context-router query:
  - "content curation preferences and channel routing overrides"
  - "source quality scores and blocked domains"
  - "recent topic velocity trends for content prioritization"
  - "recurring editorial patterns and corrections from past sessions"
```

**MemKraft layers loaded:**
- **HOT**: Today's already-processed URLs (dedup), active routing overrides
- **WARM**: Source reliability scores (last 30 days), topic frequency patterns, channel routing corrections from user feedback
- **Knowledge**: Channel routing matrix, topic classification rules, quality gate thresholds

Store loaded context as `editorial_context` for all downstream phases.

### Phase 1: Multi-Source Intake (Parallel Fan-out)

Launch up to 3 intake pipelines in parallel. Each pipeline runs independently with its own dedup, classification, and Slack posting. Cross-source dedup is handled by the shared `intel_registry.py`.

#### Phase 1A: Twitter Timeline Processing

Invoke `twitter-timeline-to-slack` with MemKraft-enhanced parameters:

1. **Source accounts**: Default `hjguyhan` + any accounts from `editorial_context.tracked_accounts`
2. **Batch limit**: 5 tweets per account per invocation (quality gate constraint)
3. **MemKraft enhancement**: Before classification, check `editorial_context` for:
   - Channel routing overrides (user previously corrected a classification)
   - Source quality scores (deprioritize low-quality accounts)
   - Topic velocity alerts (flag if a topic has >3 items today already)

**Execution constraint**: twitter-timeline-to-slack Phase 3 MUST run in main agent context (not subagents) per the skill's critical constraint. This phase is the most time-consuming.

**Cross-repo dedup**: `intel_registry.py check` runs automatically within twitter-timeline-to-slack Phase 0.5.

**Output**: Posted Slack threads in topic-appropriate channels, updated `tweets.json`, intelligence artifacts saved to research repo.

#### Phase 1B: Company Newsletter Processing

Invoke `bespin-news-digest` as a complete pipeline:

1. Gmail fetch → parse article URLs → per-article analysis → DOCX → Drive upload → summary Slack
2. All articles posted to `#bespin-news` (fixed routing per skill rules)
3. Decision items flagged for Phase 4 consolidation

**MemKraft enhancement**: Before Step 3b (web research), inject relevant context from `editorial_context`:
- Prior coverage of the same company/topic (avoid redundant research)
- Team's stated interest level in specific technology areas (adjust research depth)

**Output**: 3-message Slack threads in `#bespin-news`, DOCX on Drive, decision flags.

#### Phase 1C: Ad-hoc URL Processing

Invoke `unified-intel-intake` for any queued items:

1. **Input sources**: Pipeline inbox items, Gmail-forwarded links, user-provided URLs
2. **Classification**: Auto-detect content type (paper, tweet, news, blog, video, GitHub repo)
3. **Routing**: Topic-based channel assignment per `unified-intel-intake` classification rules
4. **Processing depth**: Relevance score determines depth:
   - Score >= 7: Full pipeline (paper-review for papers, full x-to-slack for tweets)
   - Score 4-6: Quick summary via defuddle + LLM analysis
   - Score < 4: Log to archive only

**MemKraft enhancement**: Use `editorial_context.source_quality_scores` to adjust relevance scoring. Trusted sources get +1 boost, flagged domains get -2 penalty.

**Output**: Processed content posted to appropriate Slack channels.

### Phase 2: Quality Assurance & Gap Analysis

After all Phase 1 pipelines complete, perform cross-source analysis:

#### 2a: Cross-Source Theme Detection

Read today's processed content from:
- `outputs/twitter/{screen_name}/tweets.json` (today's posted items)
- `outputs/bespin-news-digest/{date}/phase-3-per-article-pipeline.json`
- Any `unified-intel-intake` daily digest outputs

Identify themes appearing across 2+ sources. Flag as "converging signals" for the daily digest.

#### 2b: Coverage Gap Identification

Compare today's topics against `editorial_context.expected_coverage_areas`:
- If a tracked topic area has zero coverage today, flag as "coverage gap"
- If a topic has >5 items, flag as "topic saturation" (may indicate breaking news)

#### 2c: Quality Spot-Check

For 1-2 random Slack threads posted today, verify against the quality gate:
- Message 2 has 800+ characters with specific research findings
- Message 3 has 400+ characters with actionable insights
- Media upload was attempted for tweets with media
- All Korean content, no forbidden emojis

Log quality score to `editorial_context` for trend tracking.

### Phase 3: High-Value Content Repurposing (Conditional)

For content items scoring relevance >= 8 or engagement >= 90th percentile:

1. **Select candidates**: Pick top 1-3 items from today's intake based on:
   - Relevance score (from unified-intel-intake or editorial judgment)
   - Engagement metrics (likes, retweets, views from FxTwitter)
   - Topic alignment with `editorial_context.repurposing_priorities`

2. **Generate hooks**: Invoke `hook-generator` for each candidate to produce platform-specific opening lines

3. **Repurpose**: Invoke `content-repurposing-engine` with selected platforms:
   - LinkedIn post (always for high-value items)
   - Newsletter section (if weekly newsletter is upcoming)
   - Slack Canvas summary (for internal deep-dives)
   - Twitter thread draft (for original account posting)

4. **Polish**: Run `sentence-polisher` on all Korean outputs

5. **Output**: Save repurposed content to `outputs/content-curator/{date}/repurposed/`

**Skip condition**: If no items meet the relevance/engagement threshold, skip Phase 3 entirely.

### Phase 4: Decision Routing & Daily Digest

#### 4a: Consolidated Decision Routing

Collect all decision flags from Phase 1A (twitter-timeline-to-slack Step 3g), Phase 1B (bespin-news-digest Phase 6.5), and Phase 1C (unified-intel-intake Step 6):

Invoke `decision-router` for each flagged item:
- Personal decisions → `#효정-의사결정` (`C0ANBST3KDE`)
- Team/CTO decisions → `#7층-리더방` (`C0A6Q7007N2`)

#### 4b: Daily Content Velocity Report

Post a consolidated daily curation digest to `#효정-할일` (`C0AA8NT4T8T`):

```
*콘텐츠 큐레이션 일일 리포트* ({YYYY-MM-DD})

*처리 현황*
- Twitter: {N}건 처리 ({M} accounts)
- 뉴스레터: {N}건 기사 분석
- Ad-hoc URLs: {N}건 처리
- 중복 필터링: {N}건 스킵
- 총 Slack 쓰레드: {N}건

*채널별 분배*
- #ai-coding-radar: {N}건
- #deep-research-trending: {N}건
- #press: {N}건
- #bespin-news: {N}건
- #효정-주식: {N}건
- 기타: {N}건

*주요 테마*
{Top 3 converging themes from Phase 2a — 1 line each}

*커버리지 갭*
{Any gaps detected in Phase 2b, or "없음"}

*리퍼포징*
{N items repurposed for {platforms}, or "해당 없음"}

*의사결정 항목*
{N items routed: {personal_count} 개인 / {team_count} 팀}

*품질 스팟체크*
{Quality score from Phase 2c: PASS/WARN with specifics}
```

### Phase 5: MemKraft Write-back & Session Close

After all phases complete, update editorial memory:

```
memkraft-ingest entries:
  - topic: "content-curation-session"
    content: "Processed {total} items on {date}. Themes: {top_themes}. Gaps: {gaps}. Quality: {score}."
    tier: WARM
    provenance: rr-content-curator

  - topic: "source-quality-update"
    content: "{source_account} quality score: {adjusted_score} (based on {engagement_avg})"
    tier: WARM
    provenance: rr-content-curator

  - topic: "channel-routing-corrections"
    content: "{any user corrections to routing decisions from today}"
    tier: HOT
    provenance: rr-content-curator
```

## Channel Routing Matrix

Authoritative routing table. Phase 1 skills use their internal classification, but this matrix serves as the canonical reference and override source.

| Category | Target Channel | Channel ID | Source Skills |
|----------|----------------|------------|-------------|
| AI Coding (Claude/Cursor only) | `#ai-coding-radar` | `C0A7K3TBPK7` | twitter-timeline-to-slack |
| Prompt Engineering | `#prompt` | `C0A98HXSVMK` | twitter-timeline-to-slack |
| Research / Papers / Trending | `#deep-research-trending` | `C0AN34G4QHK` | twitter-timeline-to-slack, unified-intel-intake |
| Stock / Finance / Crypto | `#효정-주식` | `C0A7V1A09NK` | twitter-timeline-to-slack |
| Ideas / Business Insights | `#idea` | `C0A6U3HE3GS` | twitter-timeline-to-slack |
| Strategic Insights (strict) | `#효정-insight` | `C0A8SSPC9RU` | twitter-timeline-to-slack |
| Company News (Bespin) | `#bespin-news` | `C0ANL38CBPG` | bespin-news-digest (fixed) |
| Press / News (default) | `#press` | `C0A7NCP33LG` | twitter-timeline-to-slack, unified-intel-intake |
| Tasks / Follow-ups | `#효정-할일` | `C0AA8NT4T8T` | daily digest, summaries |
| Personal Decisions | `#효정-의사결정` | `C0ANBST3KDE` | decision-router |
| Team/CTO Decisions | `#7층-리더방` | `C0A6Q7007N2` | decision-router |

## Output Protocol (File-First)

```
outputs/content-curator/{date}/
├── manifest.json                         # Pipeline run status
├── phase-0-memkraft-context.json         # Loaded editorial context summary
├── phase-1a-twitter-summary.json         # Twitter processing counts
├── phase-1b-bespin-summary.json          # Newsletter processing counts
├── phase-1c-adhoc-summary.json           # Ad-hoc URL processing counts
├── phase-2-quality-analysis.json         # Cross-source themes, gaps, quality check
├── phase-3-repurposed/                   # Repurposed content files (conditional)
│   ├── {slug}-linkedin.md
│   ├── {slug}-newsletter.md
│   └── {slug}-twitter-thread.md
├── phase-4-daily-digest.json             # Velocity report data
└── phase-5-memkraft-writeback.json       # Memory entries written
```

## Prerequisites

| Requirement | Check | Recovery |
|------------|-------|----------|
| `TWITTER_COOKIE` in `.env` | `grep TWITTER_COOKIE .env` | Guide cookie registration per twitter-timeline-to-slack Phase 0 |
| `gws` CLI authenticated | `gws gmail +triage --max 1` | `gws auth login -s gmail` |
| Slack MCP available | Test `slack_send_message` | Check `.env` SLACK tokens |
| `intel_registry.py` accessible | `ls $HOME/thaki/research/scripts/intelligence/intel_registry.py` | Graceful degradation (local dedup only) |
| `python-docx` installed | `python3 -c "import docx"` | `pip install python-docx -q` |
| Channel DB exists | `ls outputs/twitter/slack-channels.json` | Create from Channel Routing Matrix above |

## Memory Configuration

```yaml
memkraft:
  tiers:
    HOT:
      - today's processed URLs and dedup state
      - active channel routing overrides from user corrections
      - current batch processing state (resume on crash)
    WARM:
      - source account quality scores (30-day rolling)
      - topic frequency patterns and velocity trends
      - channel routing correction history
      - repurposing candidate preferences
    Knowledge:
      - channel routing matrix (canonical)
      - topic classification rules and keyword sets
      - quality gate thresholds and enforcement history
      - editorial style preferences (emoji rules, language rules)

  provenance_tag: rr-content-curator
  dream_cycle_hook: consolidate daily velocity data into weekly trends
```

## Slack Integration

| Destination | Channel ID | Content |
|------------|------------|---------|
| Topic channels (11+) | See routing matrix | Per-item 3-message threads |
| `#효정-할일` | `C0AA8NT4T8T` | Daily velocity report |
| `#효정-의사결정` | `C0ANBST3KDE` | Personal decision items |
| `#7층-리더방` | `C0A6Q7007N2` | Team/CTO decision items |

## Error Recovery

| Phase | Failure | Recovery |
|-------|---------|----------|
| Phase 0 | MemKraft unavailable | Proceed with default editorial rules (no personalization) |
| Phase 1A | TWITTER_COOKIE expired | Log warning, skip Twitter, continue with 1B/1C |
| Phase 1A | twittxr API failure | Fall back to FxTwitter → Agent-Reach chain per skill spec |
| Phase 1B | No Bespin email found | Skip Phase 1B, note in daily digest |
| Phase 1B | Gmail auth expired | `gws auth login -s gmail`, retry once |
| Phase 1C | No queued URLs | Skip Phase 1C (expected on quiet days) |
| Phase 1 (all) | All three sources fail | Post error alert to `#효정-할일`, exit |
| Phase 2 | No content processed | Skip Phase 2-3, generate minimal digest in Phase 4 |
| Phase 3 | content-repurposing-engine fails | Log error, skip repurposing (non-critical) |
| Phase 4 | Slack rate limit | Wait 20s, retry; if persistent, queue for next invocation |
| Phase 5 | MemKraft write failure | Log warning, write to local fallback file |

## Security & Compliance

- `TWITTER_COOKIE`, `SLACK_TOKEN` never logged or persisted in output files
- `intel_registry.py` prevents cross-repo duplicate posting (dedup boundary)
- Decision items are posted only to designated channels (scope-gated)
- No PII extracted from tweet author bios beyond public profile data
- Content repurposing preserves source attribution (never claim as original)

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

## Examples

**Standard daily dispatch:**
User: "rr-content-curator" or "콘텐츠 큐레이터 대체"
→ Runs full pipeline: twitter timeline scan → bespin news → x-to-slack per article → unified intel → Slack distribution

**Single-URL analysis:**
User: "rr-content-curator" with a specific tweet URL
→ Phase Guard detects URL input, routes directly to x-to-slack with full 3-message thread format

## Operational Runbook

### Daily Invocation (Recommended: 8:00 AM after google-daily)

```
/rr-content-curator
```

Or as part of `daily-am-orchestrator` Phase 5 (news/content track).

### Ad-hoc URL Processing

```
/rr-content-curator --urls "https://example.com/article1" "https://x.com/user/status/123"
```

Routes each URL through `unified-intel-intake` classification.

### Override Channel Routing

```
/rr-content-curator --route-override "ai-coding-radar:prompt" --for-session
```

Temporarily routes AI Coding items to `#prompt` for this session only. Persisted to MemKraft HOT tier for session duration.

### Dry Run (Classification Only)

```
/rr-content-curator --dry-run
```

Fetches and classifies all sources without posting to Slack. Outputs classification report to `outputs/content-curator/{date}/dry-run-report.json`.

## Comparison: Human Content Curator vs. rr-content-curator

| Dimension | Human Curator | rr-content-curator |
|-----------|--------------|-------------------|
| Sources monitored | 3-5 (attention limit) | Unlimited (parallel pipelines) |
| Articles/day | 10-20 (manual reading) | 30-50+ (automated extraction) |
| Research depth per item | Varies (fatigue after 10+) | Consistent (2-3 WebSearches per item) |
| Channel routing accuracy | High but inconsistent under load | Keyword-rule-based + MemKraft corrections |
| Dedup across machines | Manual memory (error-prone) | `intel_registry.py` centralized (exact) |
| Decision detection | Judgment-based (good but slow) | Rule-based + MemKraft patterns (fast, improvable) |
| Content repurposing | Time-constrained (usually skipped) | Automatic for high-value items |
| Editorial memory | Personal notes (lost on vacation) | MemKraft persistent (survives sessions) |
| Quality consistency | Degrades with volume | Gate-enforced (800 char min, media mandatory) |
| Daily reporting | Manual summary (often skipped) | Automated velocity report with gap analysis |
| Cost | $50K-80K/year FTE equivalent | ~$5-10/day in API + compute costs |

## Subagent Contract

When spawning Task tool subagents for Phase 1 pipelines:

- Pass **absolute file paths** for all input/output locations
- Require return: `{ "status": "completed|failed|skipped", "file": "<phase-output-path>", "summary": "<one-line>" }`
- Include purpose: "You are a content intake subagent processing {source_type} for the daily curation pipeline"
- Phase 1A (twitter-timeline-to-slack) MUST NOT be delegated to subagents for Phase 3 posting (critical quality constraint)
- Phase 1B and 1C can run as subagents with return contract enforcement
