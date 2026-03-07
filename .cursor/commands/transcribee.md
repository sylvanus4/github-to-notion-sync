## Transcribee

Transcribe video/audio content with speaker diarization and auto-categorize into a knowledge library.

### Usage

Provide a URL or local file path:

```
https://www.youtube.com/watch?v=abc123
```

```
~/Downloads/podcast.mp3
```

### Workflow

1. **Download audio** -- yt-dlp for URLs, ffmpeg for local video files
2. **Transcribe** -- ElevenLabs `scribe_v1_experimental` with speaker diarization
3. **Classify** -- Claude Sonnet analyzes content and picks/creates a category folder
4. **Save** -- Write transcript + metadata to `~/Documents/transcripts/{category}/{title}-{date}/`
5. **Present** -- Read transcript and present results to the user

### Execution

Read and follow the `transcribee` skill (`.cursor/skills/transcribee/SKILL.md`) for prerequisites, commands, output structure, and error handling.

### Examples

YouTube video:
```
https://www.youtube.com/watch?v=abc123
```

Instagram Reel:
```
https://instagram.com/reel/xyz789
```

TikTok:
```
https://vt.tiktok.com/ZS6abc123/
```

Local audio file:
```
~/Downloads/episode42.mp3
```

With raw word-level data:
```
--raw https://www.youtube.com/watch?v=abc123
```
