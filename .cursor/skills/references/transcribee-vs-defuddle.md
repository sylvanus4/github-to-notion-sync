# transcribee vs defuddle: YouTube Transcript Comparison

## Quick Decision Guide

- **Need a quick YouTube transcript?** → Use `defuddle`
- **Need word-level timestamps or high-accuracy diarization?** → Use `transcribee`
- **Working with local audio/video files?** → Use `transcribee` (defuddle is HTTP-only)
- **Processing Instagram Reels or TikTok?** → Use `transcribee`
- **Building an auto-categorized knowledge library?** → Use `transcribee`
- **Integrating into a pipeline (x-to-slack, paper-review)?** → Use `defuddle`

## Feature Comparison

| Dimension | transcribee | defuddle YouTube |
|-----------|-------------|------------------|
| **Dependencies** | yt-dlp, ffmpeg, ElevenLabs API key, Anthropic API key | None (HTTP API call) |
| **Setup** | Install system deps + configure API keys | Zero setup |
| **Speed** | Slow (download audio → upload → transcribe → classify) | Fast (single HTTP request, ~seconds) |
| **Cost** | ElevenLabs API usage per minute of audio | Free |
| **Diarization** | ElevenLabs scribe_v1 (high accuracy, word-level) | Defuddle built-in ("pretty good", segment-level) |
| **Timestamps** | Word-level (with `--raw` flag) | Sentence/segment-level `[HH:MM:SS]` |
| **Chapters** | Not extracted from YouTube | Extracted from YouTube chapter markers |
| **Languages** | Multi-language (ElevenLabs supports 32+ languages) | YouTube's auto-captions (depends on video) |
| **Local files** | Supported (mp3, mp4, wav, m4a, etc.) | Not supported |
| **YouTube** | Supported (downloads via yt-dlp) | Supported (API extraction) |
| **Instagram Reels** | Supported | Not supported |
| **TikTok** | Supported | Not supported |
| **Auto-categorization** | Yes (Claude classification into knowledge library) | No |
| **Output format** | Markdown with speaker labels and timestamps | Markdown with YAML frontmatter, chapters, timestamps, speakers |
| **Knowledge library** | Auto-organized by topic/category | N/A |
| **Offline capability** | Partial (needs API for transcription) | No (requires internet) |

## When Each Excels

### defuddle is better when:

1. **Speed matters** — Pipeline integration where latency is critical (x-to-slack, paper-review)
2. **No setup required** — Quick transcript without installing dependencies
3. **Chapters needed** — YouTube chapter markers are valuable for the use case
4. **Cost-sensitive** — Free vs per-minute API charges
5. **Sufficient diarization** — "Pretty good" speaker identification is enough

### transcribee is better when:

1. **Accuracy is paramount** — Legal transcription, precise quote attribution
2. **Word-level timestamps** — Needed for audio editing or precise citations
3. **Non-YouTube sources** — Local recordings, Instagram, TikTok, podcast files
4. **Multi-language** — Video in a language YouTube doesn't auto-caption well
5. **Knowledge building** — Auto-categorized library with Claude classification

## Pipeline Integration Recommendations

| Pipeline | Recommended Tool | Reason |
|----------|-----------------|--------|
| x-to-slack YouTube handler | defuddle | Speed + chapters for Slack summary |
| paper-review (YouTube lecture) | defuddle | Quick extraction, chapters map to paper sections |
| nlm-arxiv-slides (conference talk) | defuddle | Fast, chapters provide slide boundaries |
| meeting-digest (YouTube recording) | defuddle | Quick transcript for meeting analysis |
| Knowledge library building | transcribee | Auto-categorization + high-accuracy diarization |
| Interview transcription | transcribee | Word-level timestamps + precise diarization |
| Podcast processing | transcribee | Local file support + multi-speaker accuracy |
