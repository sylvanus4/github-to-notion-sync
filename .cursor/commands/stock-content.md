---
description: Generate and distribute stock analysis content across Twitter, YouTube, Newsletter, Affiliate, and Outreach channels
---

Run the stock content automation pipeline:

1. **Read** the `stock-content-printer` skill for full workflow reference
2. **Generate** content drafts from today's pipeline outputs using `content_generator.py`
3. **Post** drafts to Slack `#효정-할일` for approval using `slack_content_approval.py`
4. **After approval**, distribute to configured channels:
   - Twitter: `twitter_poster.py` (rate-limited)
   - YouTube Shorts: `youtube_shorts_pipeline.py` (TTS + charts + ffmpeg)
   - Newsletter: `email_sender.py --channel newsletter`
   - Affiliate: `affiliate_poster.py`
   - Outreach: `email_sender.py --channel outreach`

Default date is today. Override with `--date YYYY-MM-DD`.

Use `--dry-run` on any script to preview without posting.
