---
name: marketing-podcast-ops
description: >-
  Podcast-to-everything content pipeline — transforms a single episode into
  20+ content pieces across LinkedIn, Twitter, newsletters, blog posts,
  YouTube Shorts scripts, with viral scoring and deduplication.
disable-model-invocation: true
---

# Marketing Podcast Ops

One episode to 20+ content pieces. Processes podcast episodes from RSS feeds or transcripts, extracts editorial moments, generates multi-platform content, scores for viral potential, deduplicates, and creates weekly content calendars.

## Triggers

Use when the user asks to:
- "podcast repurpose", "podcast to content", "episode pipeline"
- "podcast content calendar", "episode to social", "repurpose episode"
- "팟캐스트 리퍼포즈", "에피소드 콘텐츠 변환", "팟캐스트 파이프라인"

## Do NOT Use

- For podcast transcription only → use `transcribee`
- For video compression → use `video-compress`
- For general content creation without podcast source → use `kwp-marketing-content-creation`
- For YouTube transcript extraction → use `defuddle`

## Prerequisites

- Python 3.10+
- `pip install anthropic openai feedparser`
- Environment: `ANTHROPIC_API_KEY` (generation), optional `OPENAI_API_KEY` (Whisper transcription)

## Execution Steps

### Step 1: Episode Ingestion
Run `scripts/podcast_pipeline.py` with: `--rss <feed_url>` (latest episode), `--transcript <file>` (local transcript), or `--batch <N>` (process N episodes).

### Step 2: Editorial Extraction
Automatically identifies key quotes, stories, insights, controversial takes, and actionable advice from transcripts.

### Step 3: Multi-Platform Generation
Generates: LinkedIn posts, Twitter threads, newsletter sections, blog post outlines, YouTube Shorts scripts, Instagram captions, and audiogram briefs.

### Step 4: Viral Scoring
Each piece scored on viral potential. Use `--min-score <threshold>` to filter.

### Step 5: Deduplication
Cross-checks against previously generated content to prevent repetition.

### Step 6: Calendar Generation
Run with `--calendar` flag to produce a weekly content distribution calendar.

## Examples

### Example 1: Process latest podcast episode

User: "Repurpose our latest episode into social content"

1. Run `scripts/podcast_pipeline.py --rss https://feed.example.com/podcast`

Result: 20+ content pieces (LinkedIn posts, Twitter threads, newsletter sections, YouTube Shorts scripts) each with viral score.

### Example 2: Batch process with calendar

User: "Process the last 5 episodes and create a content calendar"

1. Run `scripts/podcast_pipeline.py --rss https://feed.example.com/podcast --batch 5 --calendar`

Result: Content pieces for all 5 episodes, deduplicated, with a weekly distribution calendar.

## Error Handling

| Error | Action |
|-------|--------|
| ANTHROPIC_API_KEY not set | Required for content generation; set in `.env` |
| RSS feed unreachable | Verify URL; use `--transcript` for local files as fallback |
| No transcript available | Set `OPENAI_API_KEY` for Whisper transcription or provide transcript manually |
| Dedup collision on re-run | Previously generated content is tracked; only new pieces are output |

## Output

- 20+ content pieces per episode
- Viral score per piece
- Deduplication report
- Weekly content calendar (with --calendar)
