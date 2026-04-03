---
description: "Podcast-to-everything content pipeline — episode to 20+ content pieces with viral scoring"
argument-hint: "[rss|transcript|batch|calendar] [feed URL or file path]"
---

# Marketing Podcast Ops

Read and follow the skill at `.cursor/skills/marketing/marketing-podcast-ops/SKILL.md`.

## Your Task

User input: $ARGUMENTS

Run the podcast content pipeline:

```bash
# From RSS feed (latest episode)
python scripts/podcast_pipeline.py --rss <feed_url>

# From local transcript
python scripts/podcast_pipeline.py --transcript <file>

# Batch processing
python scripts/podcast_pipeline.py --batch <N>

# With calendar generation
python scripts/podcast_pipeline.py --rss <feed_url> --calendar
```

Requires: `ANTHROPIC_API_KEY`. Optional: `OPENAI_API_KEY` (for Whisper transcription).
