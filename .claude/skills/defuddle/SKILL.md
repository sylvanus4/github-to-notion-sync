---
name: defuddle
description: Extract clean markdown from web pages or YouTube transcripts via Defuddle API — strips noise, returns structured content.
arguments: [url]
---

Extract clean content from `$url`.

## Capabilities

### Web Pages
- Strips ads, sidebars, navigation, UI noise
- Returns markdown with YAML frontmatter (title, author, date, domain)
- Preserves article structure, headings, links, images

### YouTube Videos
- Extracts full transcript with timestamps
- Chapter markers when available
- Speaker diarization

## Usage

```bash
# Web page
defuddle https://example.com/article

# YouTube
defuddle https://www.youtube.com/watch?v=VIDEO_ID
```

## When to Use

- Feeding web content to LLM with minimal noise
- Extracting article text for KB ingestion
- Getting YouTube transcripts for meeting-digest or analysis

## When NOT to Use

- API endpoint calls → use WebFetch or curl
- Browser automation → use agent-browser
- Local audio/video transcription → use transcribee
- Structured JSON data → use appropriate API
