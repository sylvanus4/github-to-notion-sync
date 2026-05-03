---
name: reclip-media-downloader
description: >-
  Download video and audio files from 1000+ websites (YouTube, TikTok,
  Instagram, X/Twitter, Reddit, Vimeo, etc.) to local disk using `yt-dlp`.
  Supports format selection, quality control, audio extraction, and metadata
  inspection. Use when the user asks to "download video", "download audio",
  "save thi
---

# reclip-media-downloader

Download video and audio files from 1000+ websites (YouTube, TikTok, Instagram, X/Twitter, Reddit, Vimeo, etc.) to local disk using `yt-dlp`. Supports format selection, quality control, audio extraction, and metadata inspection. Use when the user asks to "download video", "download audio", "save this video", "get MP4 from URL", "extract audio from video URL", "download media", "reclip", "yt-dlp download", "영상 다운로드", "비디오 다운로드", "오디오 추출", "미디어 다운로드", "유튜브 다운로드", "동영상 저장", "MP3 추출", "영상 저장해줘", or any request to download actual media files from a URL. Do NOT use for extracting text/markdown from web pages (use defuddle). Do NOT use for transcribing downloaded media (use transcribee after downloading). Do NOT use for compressing video files (use video-compress). Do NOT use for streaming or playback. Do NOT use for web scraping without media download intent (use scrapling or agent-browser).

## Prerequisites

Both tools must be available in `$PATH`. They are shared with the `transcribee` skill.

```bash
# macOS
brew install yt-dlp ffmpeg

# Linux (Debian/Ubuntu)
sudo apt install yt-dlp ffmpeg

# Verify
yt-dlp --version
ffmpeg -version
```

## Modes

### 1. Info Mode — Fetch metadata without downloading

Inspect a URL before committing to a download.

```bash
yt-dlp --no-playlist -j "<URL>"
```

Parse the JSON output to extract:
- `title` — video title
- `duration` — length in seconds
- `thumbnail` — thumbnail URL
- `uploader` — channel/user name
- `formats` — array of available format objects

To list available quality options (video formats with resolution):

```bash
yt-dlp --no-playlist -F "<URL>"
```

### 2. Video Download — Download as MP4

**Best quality (default):**

```bash
yt-dlp --no-playlist \
  -f "bestvideo+bestaudio/best" \
  --merge-output-format mp4 \
  -o "outputs/reclip/$(date +%Y-%m-%d)/%(title).200B s.%(ext)s" \
  "<URL>"
```

**Specific resolution** (use format ID from `-F` output):

```bash
yt-dlp --no-playlist \
  -f "<FORMAT_ID>+bestaudio/best" \
  --merge-output-format mp4 \
  -o "outputs/reclip/$(date +%Y-%m-%d)/%(title).200Bs.%(ext)s" \
  "<URL>"
```

### 3. Audio Extraction — Download as MP3

```bash
yt-dlp --no-playlist \
  -x --audio-format mp3 \
  -o "outputs/reclip/$(date +%Y-%m-%d)/%(title).200Bs.%(ext)s" \
  "<URL>"
```

## Workflow

### Step 1: Validate prerequisites

```bash
command -v yt-dlp && command -v ffmpeg
```

If either is missing, instruct the user to install (see Prerequisites).

### Step 2: Create output directory

```bash
mkdir -p "outputs/reclip/$(date +%Y-%m-%d)"
```

### Step 3: Fetch metadata (recommended)

Run info mode to confirm the URL is valid and show the user what they are about to download (title, duration, available qualities). This avoids wasted bandwidth on wrong URLs.

```bash
yt-dlp --no-playlist -j "<URL>" 2>&1
```

Parse JSON: extract `title`, `duration`, `uploader`, and build a quality menu from `formats` where `vcodec != "none"`, keeping the best bitrate per resolution height.

### Step 4: Execute download

Based on user's choice of format (video or audio) and quality, construct the `yt-dlp` command per the patterns in the Modes section above.

Run with a 5-minute timeout:

```bash
timeout 300 yt-dlp [flags] "<URL>"
```

### Step 5: Verify and report

- Confirm the output file exists at the expected path
- Report: file path, file size (`ls -lh`), duration (from metadata)
- If the download failed, show the last line of stderr for diagnosis

## Output Convention

All downloaded files go to:

```
outputs/reclip/{YYYY-MM-DD}/{sanitized-title}.{ext}
```

Filename sanitization: strip characters `\/:*?"<>|`, truncate title to 200 characters.

The `outputs/reclip/` directory is `.gitignore`d — media files should NOT be committed.

## Bulk Download

Process multiple URLs sequentially. Write URLs to a temporary file and use `yt-dlp --batch-file`:

```bash
# Write URLs one per line
cat > /tmp/reclip-batch.txt << 'EOF'
https://youtube.com/watch?v=xxx
https://twitter.com/user/status/yyy
EOF

yt-dlp --no-playlist \
  -f "bestvideo+bestaudio/best" \
  --merge-output-format mp4 \
  -o "outputs/reclip/$(date +%Y-%m-%d)/%(title).200Bs.%(ext)s" \
  --batch-file /tmp/reclip-batch.txt
```

## Gotchas

- **Playlists**: Always use `--no-playlist` unless the user explicitly wants an entire playlist. Without this flag, a playlist URL downloads ALL videos.
- **Age-restricted content**: Some videos require authentication. Use `--cookies-from-browser chrome` if needed, but warn the user about privacy implications.
- **Geo-blocked videos**: May fail with "Video unavailable". No workaround without a VPN.
- **Rate limiting**: Sites like YouTube may throttle repeated downloads. Space bulk operations.
- **Large files**: 4K videos can be several GB. Check available disk space before downloading.
- **Timeout**: Default 5-minute timeout. For very long videos (>1 hour, 4K), increase timeout or download lower quality.
- **yt-dlp updates**: Run `yt-dlp -U` periodically — site extractors break frequently and updates fix them.

## Downstream Skill Chains

Downloaded media files can feed into these skills:

| Next Skill | Purpose |
|---|---|
| `transcribee` | Transcribe downloaded video/audio with speaker diarization |
| `video-compress` | Compress large downloaded videos for sharing |
| `video-editing-planner` | Plan edits for downloaded footage |
| `caption-subtitle-formatter` | Generate subtitles from transcribed downloaded media |
| `content-repurposing-engine` | Repurpose downloaded video into multi-platform content |
| `pika-video-pipeline` | Use downloaded clips as input for AI video generation |

## Verification Checklist

Before declaring download complete:

- [ ] Output file exists at `outputs/reclip/{date}/{filename}`
- [ ] File size is non-zero (> 0 bytes)
- [ ] File extension matches requested format (.mp4 for video, .mp3 for audio)
- [ ] Report file path, size, and duration to user
