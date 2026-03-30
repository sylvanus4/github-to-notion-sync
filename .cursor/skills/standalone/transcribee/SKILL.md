---
name: transcribee
description: >-
  Transcribe YouTube, Instagram Reels, TikTok, and local audio/video files with
  speaker diarization, then auto-categorize into a self-organizing knowledge
  library. Use when the user asks to transcribe a video URL, podcast, audio
  file, or build a transcript library. Do NOT use for live audio capture,
  real-time streaming, or text-to-speech generation. Korean triggers: "빌드",
  "비디오", "트랜스크립션".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
---
# Transcribee

Transcribe video/audio content with speaker diarization (ElevenLabs) and auto-categorize transcripts into a self-organizing knowledge library (Claude).

## Prerequisites

### System Dependencies

```bash
brew install yt-dlp ffmpeg
```

### API Keys

Configure `~/.local/share/transcribee/.env`:

```bash
ELEVEN_LABS_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

Copy from `.env.example` if setting up for the first time:

```bash
cp ~/.local/share/transcribee/.env.example ~/.local/share/transcribee/.env
```

### Installation Path

The transcribee tool is installed at `~/.local/share/transcribee/`. Run commands from this directory or use the shell alias below.

## Quick Start

```bash
cd ~/.local/share/transcribee

# Transcribe a YouTube video
pnpm exec tsx index.ts "https://www.youtube.com/watch?v=..."

# Transcribe an Instagram Reel
pnpm exec tsx index.ts "https://instagram.com/reel/..."

# Transcribe a TikTok video
pnpm exec tsx index.ts "https://vt.tiktok.com/..."

# Transcribe a local file
pnpm exec tsx index.ts ~/Downloads/podcast.mp3
pnpm exec tsx index.ts ~/Videos/interview.mp4
```

### Shell Alias (Recommended)

Add to `~/.zshrc`:

```bash
alias transcribee="noglob ~/.local/share/transcribee/transcribe.sh"
```

Then use: `transcribee "https://youtube.com/watch?v=..."`

## Workflow

The tool follows a 5-step pipeline:

1. **Download/Extract Audio** -- yt-dlp for URLs, ffmpeg for local video files
2. **Transcribe** -- ElevenLabs `scribe_v1_experimental` with speaker diarization
3. **Read Library** -- Scan existing `~/Documents/transcripts/` structure
4. **Classify** -- Claude Sonnet analyzes content and picks/creates a category folder
5. **Save** -- Write transcript + metadata to `~/Documents/transcripts/{category}/{title}-{date}/`

## Output

Transcripts save to `~/Documents/transcripts/{category}/{title}-{date}/`:

| File | Purpose |
|------|---------|
| `transcript.txt` | Speaker-labeled transcript (paste into LLMs) |
| `metadata.json` | Source info, theme classification, transcription stats |

With `--raw` flag, also saves:

| File | Purpose |
|------|---------|
| `transcript-raw.json` | Full ElevenLabs response with word-level timestamps |

For details on output structure and metadata fields, see [references/output-structure.md](references/output-structure.md).

## Commands

```bash
# Basic transcription
pnpm exec tsx index.ts "<url-or-file>"

# With raw word-level data
pnpm exec tsx index.ts --raw "<url-or-file>"
```

**Always quote URLs** containing `&` or special characters.

## Supported Formats

For the full list of supported audio/video formats and URL patterns, see [references/supported-formats.md](references/supported-formats.md).

Quick reference:
- **URLs**: YouTube, Instagram Reels, TikTok
- **Audio**: mp3, m4a, wav, ogg, flac
- **Video**: mp4, mkv, webm, mov, avi

## Examples

### Example 1: Transcribe a YouTube video

User says: "Transcribe this YouTube video: https://youtube.com/watch?v=abc123"

Actions:
1. Run `cd ~/.local/share/transcribee && pnpm exec tsx index.ts "https://youtube.com/watch?v=abc123"`
2. Wait for transcription to complete
3. Read the output transcript from `~/Documents/transcripts/{category}/{title}-{date}/transcript.txt`
4. Present the transcript to the user

### Example 2: Transcribe a local podcast file

User says: "Transcribe this podcast ~/Downloads/episode42.mp3"

Actions:
1. Run `cd ~/.local/share/transcribee && pnpm exec tsx index.ts ~/Downloads/episode42.mp3`
2. Read the generated transcript
3. Present to the user

### Example 3: Transcribe and summarize

User says: "Transcribe this video and give me key takeaways"

Actions:
1. Run transcription as above
2. Read the generated `transcript.txt`
3. Analyze content and present summary with key takeaways

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `yt-dlp not found` | Missing system dependency | `brew install yt-dlp` |
| `ffmpeg not found` | Missing system dependency | `brew install ffmpeg` |
| `Missing ELEVEN_LABS_API_KEY` | No API key configured | Add key to `~/.local/share/transcribee/.env` |
| `Missing ANTHROPIC_API_KEY` | No API key configured | Add key to `~/.local/share/transcribee/.env` |
| `Unsupported file type` | File extension not supported | Check supported formats in references |
| `File not found` | Invalid local file path | Verify path exists and is accessible |
| Timeout on long videos | ElevenLabs has 20-min timeout | Split long videos or use shorter clips |
