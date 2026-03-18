# YouTube Transcript Format — Defuddle Output Specification

## Overview

When Defuddle processes a YouTube URL, it returns a markdown document with the video's transcript instead of a web page extraction. The format includes YAML frontmatter, chapter headers, timestamps, and speaker labels.

## YAML Frontmatter

```yaml
---
title: "Video Title"
author: "Channel Name"
source: "https://youtube.com/watch?v=VIDEO_ID"
domain: "youtube.com"
description: "Video description text"
word_count: 5432
---
```

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Video title |
| `author` | string | Channel name |
| `source` | string | Original YouTube URL |
| `domain` | string | Always `youtube.com` |
| `description` | string | Video description (may be truncated) |
| `word_count` | number | Total word count of the transcript body |

## Timestamps

Timestamps appear inline before transcript segments in the format `[HH:MM:SS]`.

```markdown
[00:00:15] Welcome to today's session on large language models...
[00:01:30] The first topic we'll cover is tokenization...
```

For shorter videos, timestamps may use `[MM:SS]` format.

## Chapter Headers

If the video has YouTube chapter markers, they appear as `##` headers:

```markdown
## Introduction

[00:00:00] Welcome everyone...

## Tokenization Deep Dive

[00:05:30] Let's start with how tokenization works...

## Training at Scale

[00:15:00] Now let's talk about distributed training...
```

Videos without chapter markers produce a flat transcript without `##` headers.

## Speaker Diarization

When multiple speakers are detected, each segment is prefixed with the speaker name in bold:

```markdown
**Host:** [00:00:15] Welcome to the show. Today we have a special guest.

**Guest:** [00:00:22] Thanks for having me. I'm excited to be here.

**Host:** [00:00:28] Let's dive right in. Tell us about your latest research.
```

Speaker labels are based on Defuddle's built-in diarization. Accuracy is described as "pretty good" — sufficient for readability but not word-level precise like ElevenLabs.

Single-speaker videos may omit speaker labels entirely.

## Complete Example

```markdown
---
title: "Building AI Agents with Claude"
author: "Anthropic"
source: "https://youtube.com/watch?v=example123"
domain: "youtube.com"
description: "Learn how to build production AI agents..."
word_count: 8234
---

## Introduction

**Speaker 1:** [00:00:00] Hello everyone, welcome to our deep dive into building AI agents with Claude.

**Speaker 1:** [00:00:12] Today we'll cover three main topics: agent architecture, tool use, and production deployment.

## Agent Architecture

**Speaker 1:** [00:02:15] The first thing to understand about agent architecture is the ReAct loop...

**Speaker 2:** [00:05:30] That's a great point. In our experience at Anthropic, we've found that...

## Tool Use Patterns

**Speaker 1:** [00:12:00] Let's move on to tool use. The key insight here is...

## Production Deployment

**Speaker 2:** [00:25:00] For production deployment, there are several critical considerations...

## Q&A

**Audience:** [00:40:00] How do you handle rate limiting in production?

**Speaker 1:** [00:40:08] Great question. We recommend implementing exponential backoff...
```

## Parsing Tips

- **Chapter count**: Count `## ` headers (level-2 headings)
- **Speaker count**: Count unique `**Name:**` patterns
- **Duration estimate**: Use the last timestamp in the transcript
- **Key point extraction**: Look for segments immediately after chapter headers
