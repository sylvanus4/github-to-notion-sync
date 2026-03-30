---
name: defuddle
description: >-
  Extract clean markdown content from any web page URL or YouTube video
  transcript using the Defuddle API. For web pages: strips ads, sidebars,
  navigation, and UI noise, returning markdown with YAML frontmatter. For
  YouTube URLs: returns full transcripts with timestamps, chapter markers,
  and speaker diarization. Use when the user asks to "read this page",
  "extract content from URL", "get markdown from website", "clean up this
  webpage", "get YouTube transcript", "extract video transcript", "defuddle",
  or when feeding web/video content to an LLM with minimal noise. Do NOT use
  for general web search (use WebSearch), API endpoint calls, browser
  automation (use agent-browser), or fetching structured JSON data from APIs.
  Do NOT use for local audio/video files or Instagram/TikTok transcription
  (use transcribee). Korean triggers: "검색", "데이터", "API", "자동화",
  "트랜스크립트", "유튜브 자막".
metadata:
  author: "thaki"
  version: "1.1.0"
  category: "execution"
---
# Defuddle — Web Page & YouTube Transcript to Clean Markdown

Extract the main content from any web page or YouTube video as clean markdown via the Defuddle API. For web pages, strips ads, sidebars, headers, footers, and navigation clutter. For YouTube videos, returns full transcripts with timestamps, chapters, and speaker diarization.

## Input

The user provides one or more URLs to extract content from.

## Workflow

### Step 1: Extract Content

Run via Shell:

```bash
curl -s "https://defuddle.md/{url_without_protocol}"
```

**CRITICAL**: The URL must omit the protocol prefix (`https://` or `http://`). Examples:

```bash
# Correct
curl -s "https://defuddle.md/example.com/article"

# Incorrect — do not include protocol
curl -s "https://defuddle.md/https://example.com/article"
```

The response is markdown with YAML frontmatter:

```markdown
---
title: "Article Title"
author: "Author Name"
published: 2025-10-20T00:00:00+00:00
source: "https://example.com/article"
domain: "example.com"
description: "Article description."
word_count: 1234
---

Article content in clean markdown...
```

### Step 2: Parse Metadata

Extract metadata from the YAML frontmatter block for downstream use:

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Page title |
| `author` | string | Author name |
| `published` | string | Publication date (ISO 8601) |
| `source` | string | Original URL |
| `domain` | string | Domain name |
| `description` | string | Page description/summary |
| `word_count` | number | Word count of extracted content |

### Step 3: Deliver Content

Based on the user's intent:

- **Display**: Show the markdown content directly to the user
- **Save**: Write to a file via `Write` tool
- **Summarize**: Feed the markdown to the LLM for analysis or summarization
- **Compare**: Extract multiple URLs and compare their content

## Advanced Usage

### Batch Extraction

For multiple URLs, run parallel Shell commands:

```bash
curl -s "https://defuddle.md/example.com/page1"
curl -s "https://defuddle.md/example.com/page2"
```

### Combining with Other Tools

- **Defuddle + Summarization**: Extract clean content, then summarize in the same turn
- **Defuddle + Translation**: Extract English content, translate to Korean
- **Defuddle + Comparison**: Extract two competing articles, compare key points

## YouTube Transcript Extraction

When given a YouTube URL, Defuddle returns a full transcript instead of a web page extraction. The same API endpoint handles both.

### Supported URL Formats

```bash
curl -s "https://defuddle.md/youtube.com/watch?v=VIDEO_ID"
curl -s "https://defuddle.md/youtu.be/VIDEO_ID"
curl -s "https://defuddle.md/m.youtube.com/watch?v=VIDEO_ID"
```

### YouTube Output Format

The response includes timestamps, chapter headers, and speaker labels. See `references/youtube-transcript-format.md` for the full format specification.

```markdown
---
title: "Video Title"
author: "Channel Name"
source: "https://youtube.com/watch?v=VIDEO_ID"
domain: "youtube.com"
word_count: 5432
---

## Chapter Title

**Speaker Name:** [00:00:15] First sentence of the transcript segment...

**Speaker Name:** [00:01:30] Next segment with different speaker...

## Next Chapter

**Speaker Name:** [00:05:45] Content in the next chapter...
```

### YouTube Workflow

1. Detect that the URL is a YouTube link (youtube.com, youtu.be, m.youtube.com)
2. Run `curl -s "https://defuddle.md/{youtube_url_without_protocol}"`
3. Parse the transcript with chapter headers, timestamps, and speaker labels
4. Deliver based on user intent: display, save, summarize, or post to Slack

### YouTube Error Handling

| Error | Symptom | Action |
|-------|---------|--------|
| No transcript available | Response has frontmatter but empty/minimal body | Video may be private, restricted, or lack captions; inform user |
| Wrong language | Transcript is in unexpected language | YouTube auto-captions depend on the video's audio language |
| Missing chapters | No `##` chapter headers in output | Video has no chapter markers set by the uploader |
| Missing diarization | No `**Speaker:**` labels | Single-speaker video or diarization unavailable |

### When to Use Defuddle vs transcribee for YouTube

For a detailed feature-by-feature comparison and pipeline integration recommendations, see [references/transcribee-vs-defuddle.md](references/transcribee-vs-defuddle.md).

| Dimension | defuddle | transcribee |
|-----------|----------|-------------|
| Dependencies | None (HTTP API) | yt-dlp, ffmpeg, ElevenLabs API key |
| Speed | Fast (~seconds) | Slow (download + transcribe) |
| Cost | Free | ElevenLabs API usage |
| Diarization | Built-in ("pretty good") | ElevenLabs scribe_v1 (high accuracy, word-level) |
| Timestamps | Sentence/segment-level | Word-level (with --raw) |
| Chapters | Extracted from YouTube | Not extracted |
| Languages | YouTube's auto-captions | Multi-language (ElevenLabs) |
| Local files | Not supported | Supported (mp3, mp4, etc.) |
| Instagram/TikTok | Not supported | Supported |
| Auto-categorization | No | Yes (Claude classification) |
| **Best for** | Quick YouTube transcript, pipeline integration | High-accuracy diarization, local files, non-YouTube |

### When to Prefer Defuddle over WebFetch

| Scenario | Use |
|----------|-----|
| Page has heavy ads/sidebars/navigation | Defuddle |
| Need markdown with structured frontmatter | Defuddle |
| YouTube video transcript extraction | Defuddle |
| Simple page or API docs | WebFetch is sufficient |
| Need to interact with page elements | Use agent-browser instead |
| Local audio/video transcription | Use transcribee instead |

## Examples

### Example 1: Read a blog post

User says: "Read this article and summarize it: https://stephango.com/file-over-app"

Actions:
1. Run `curl -s "https://defuddle.md/stephango.com/file-over-app"`
2. Parse frontmatter: title, author, word_count
3. Summarize the extracted markdown content for the user

Result: Clean article text without navigation/footer noise, summarized in Korean.

### Example 2: Extract and save documentation

User says: "Save the content from https://docs.example.com/guide as a markdown file"

Actions:
1. Run `curl -s "https://defuddle.md/docs.example.com/guide"`
2. Write the output to a local `.md` file using the Write tool

Result: Clean documentation saved as a local markdown file with frontmatter metadata.

### Example 3: Compare two pages

User says: "Compare the main points of these two articles"

Actions:
1. Run parallel `curl` commands for both URLs via Defuddle
2. Parse both responses
3. Compare key points side-by-side

Result: Structured comparison of both articles' content without UI noise.

### Example 4: Extract YouTube transcript

User says: "Get the transcript from this YouTube video: https://youtube.com/watch?v=abc123"

Actions:
1. Run `curl -s "https://defuddle.md/youtube.com/watch?v=abc123"`
2. Parse frontmatter: title, channel name (author), word_count
3. Display the transcript with timestamps, chapters, and speaker labels

Result: Full transcript with `[HH:MM:SS]` timestamps, `## Chapter` headers, and `**Speaker:**` labels.

### Example 5: YouTube transcript summarization

User says: "Summarize this YouTube video: https://youtu.be/xyz789"

Actions:
1. Run `curl -s "https://defuddle.md/youtu.be/xyz789"`
2. Parse frontmatter for metadata (title, channel)
3. Summarize the extracted transcript, highlighting key points with timestamps

Result: Korean summary with timestamped key takeaways from the video.

### Example 6: YouTube transcript save for research

User says: "Save the transcript from this conference talk for later analysis"

Actions:
1. Run `curl -s "https://defuddle.md/youtube.com/watch?v=conf456"`
2. Write the full transcript to a local `.md` file using the Write tool
3. Report metadata (title, channel, word count, chapter count)

Result: Full transcript saved as markdown with chapters and timestamps preserved.

## Error Handling

| Error | Symptom | Action |
|-------|---------|--------|
| Empty response | `curl` returns empty string | URL may be invalid or blocked; try `WebFetch` as fallback |
| Timeout | `curl` hangs beyond 30s | Add `--max-time 15` flag; report timeout to user |
| No main content found | Response has frontmatter but empty body | Site may use heavy JS rendering; suggest `agent-browser` instead |
| Rate limiting | HTTP 429 or delayed responses | Wait and retry; for batch operations, add 1s delay between requests |
| Invalid URL format | Error or unexpected output | Verify URL has no protocol prefix; strip `https://` before passing |
