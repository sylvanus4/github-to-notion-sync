---
name: stock-content-printer
description: >-
  > Master orchestrator for the stock content automation pipeline — from daily
  analysis to multi-channel content distribution.
---

# Stock Content Printer

> Master orchestrator for the stock content automation pipeline — from daily analysis to multi-channel content distribution.

## Trigger Conditions

Use when the user asks to:
- "generate stock content", "stock content printer", "create trading posts"
- "run content pipeline", "콘텐츠 파이프라인", "주식 콘텐츠 생성"
- "post stock analysis to Twitter", "create YouTube Shorts from analysis"
- "send newsletter", "affiliate content", "outreach emails"
- "stock-content-printer", "/stock-content"

Do NOT use for:
- Running the daily stock analysis pipeline itself (use `today`)
- Downloading stock data (use `weekly-stock-update` or `stock-csv-downloader`)
- Single tweet posting without content generation (use `x-to-slack`)
- General Slack messaging (use `kwp-slack-slack-messaging`)

## Overview

End-to-end pipeline that transforms daily stock analysis outputs into multi-channel content:

```
today pipeline outputs → Content Generation → Slack Approval → Distribution
                         (LLM-powered)        (Block Kit)       (Twitter, YouTube, Email)
```

## Architecture

### Scripts (backend/scripts/)

| Script | Purpose |
|--------|---------|
| `content_generator.py` | Generate drafts for all channels from screener/news data |
| `slack_content_approval.py` | Post drafts to Slack with approve/reject buttons |
| `twitter_poster.py` | Post approved tweets with OAuth 1.0a + rate limiting |
| `youtube_shorts_pipeline.py` | TTS narration + chart frames + ffmpeg assembly |
| `email_sender.py` | Newsletter and outreach via gws CLI |
| `affiliate_poster.py` | Affiliate content tweets |

### API Endpoints (backend/app/api/v1/content_approval.py)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/content-approval/slack/interactions` | POST | Slack interactive message webhook |
| `/content-approval/drafts/{date}` | GET | List drafts for a date |
| `/content-approval/drafts/{date}/{index}` | GET/PUT | Get or edit a draft |
| `/content-approval/drafts/{date}/{index}/approve` | POST | Approve via API |
| `/content-approval/approved/{date}` | GET | List approved content |

### Config (config/content-templates.json)

Prompt templates for each channel with structured output schemas.

### GitHub Actions (.github/workflows/daily-content.yml)

Runs after `daily-today.yml` — generates, approves, and distributes content.

## Execution Steps

### Step 1: Generate Content Drafts

```bash
cd backend
python scripts/content_generator.py --date $(date +%Y-%m-%d)
```

Channels: `twitter`, `youtube_shorts`, `newsletter`, `affiliate`, `outreach`.
Output: `outputs/content/drafts/drafts-YYYY-MM-DD.json`

### Step 2: Send for Slack Approval

```bash
python scripts/slack_content_approval.py --date $(date +%Y-%m-%d)
```

Posts to `#효정-할일` with approve/edit/reject buttons.

### Step 3: Distribute Approved Content

After approval, post to each channel:

```bash
# Twitter
python scripts/twitter_poster.py --date $(date +%Y-%m-%d) --interval 900

# YouTube Shorts
python scripts/youtube_shorts_pipeline.py --date $(date +%Y-%m-%d)

# Newsletter
python scripts/email_sender.py --date $(date +%Y-%m-%d) --channel newsletter

# Affiliate
python scripts/affiliate_poster.py --date $(date +%Y-%m-%d)

# Outreach
python scripts/email_sender.py --date $(date +%Y-%m-%d) --channel outreach
```

### Full Pipeline (automated)

```bash
# Generate + approve + post (all channels)
python scripts/content_generator.py --date $(date +%Y-%m-%d) && \
python scripts/slack_content_approval.py --date $(date +%Y-%m-%d)
# ... await approval, then:
python scripts/twitter_poster.py --date $(date +%Y-%m-%d)
```

## Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `ANTHROPIC_API_KEY` | Yes | Content generation via Claude API |
| `SLACK_BOT_TOKEN` | Yes | Slack approval posting |
| `TWITTER_API_KEY` | For Twitter | OAuth 1.0a consumer key |
| `TWITTER_API_SECRET` | For Twitter | OAuth 1.0a consumer secret |
| `TWITTER_ACCESS_TOKEN` | For Twitter | User access token |
| `TWITTER_ACCESS_SECRET` | For Twitter | User access token secret |
| `NEWSLETTER_RECIPIENTS` | For email | Comma-separated recipient list |

## Sub-Skills

This skill composes:
- `today` — Provides screener/news data inputs
- `daily-stock-check` — Signal generation
- `kwp-slack-slack-messaging` — Slack message formatting
- `gws-gmail` — Email distribution
- `video-compress` — Optional video optimization

## Extra Channels

Additional distribution channels available via `extra_channels.py`:

```bash
# Telegram
python scripts/extra_channels.py --date $(date +%Y-%m-%d) --channel telegram

# Discord
python scripts/extra_channels.py --date $(date +%Y-%m-%d) --channel discord

# LinkedIn
python scripts/extra_channels.py --date $(date +%Y-%m-%d) --channel linkedin

# Podcast (audio-only TTS from newsletter)
python scripts/extra_channels.py --date $(date +%Y-%m-%d) --channel podcast

# RSS Feed (append to outputs/content/rss/feed.xml)
python scripts/extra_channels.py --date $(date +%Y-%m-%d) --channel rss
```

Extra environment variables: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `DISCORD_WEBHOOK_URL`, `LINKEDIN_ACCESS_TOKEN`.

## Dry Run

```bash
python scripts/content_generator.py --date 2026-03-20 --dry-run
python scripts/twitter_poster.py --date 2026-03-20 --dry-run
python scripts/youtube_shorts_pipeline.py --date 2026-03-20 --dry-run
python scripts/email_sender.py --date 2026-03-20 --channel newsletter --dry-run
```
