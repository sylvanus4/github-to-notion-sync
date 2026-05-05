# Video-to-Text

Extract audio from online videos and transcribe to text with speaker diarization. Two-phase pipeline: yt-dlp audio extraction, then transcribee ElevenLabs transcription. Covers Twitter/X, YouTube, Instagram, TikTok, and 1000+ yt-dlp-supported sites.

## When to Use

- User shares a video URL and wants the spoken content as text
- "extract audio from video", "transcribe this video", "video to text", "what are they saying"
- "비디오 텍스트 추출", "영상 음성 추출", "트윗 비디오 텍스트", "유튜브 텍스트 추출"
- "영상 내용 텍스트로", "비디오 전사", "동영상 음성 텍스트", "video transcript"
- User pastes a video URL from Twitter/X, YouTube, TikTok, Instagram, Reddit, Vimeo

## When NOT to Use

- YouTube transcript extraction via existing captions (use `defuddle` -- returns embedded subtitles without download)
- Local audio/video file already on disk (use `transcribee` directly with the file path)
- Video download without transcription intent (use `reclip-media-downloader`)
- Live audio capture or real-time streaming
- Subtitle file formatting from existing transcript (use `caption-subtitle-formatter`)

## Prerequisites

- `yt-dlp` installed (`brew install yt-dlp`)
- `ffmpeg` installed (`brew install ffmpeg`)
- `ELEVENLABS_API_KEY` in environment
- transcribee project dependencies installed (`cd ~/thaki/ai-platform-strategy && pnpm install`)

## Output Artifacts

| Phase | Stage | Output File | Purpose |
|-------|-------|-------------|---------|
| 1 | Audio Download | `/tmp/video-to-text-{id}.mp3` | Extracted audio |
| 2 | Transcription | `outputs/transcripts/{date}-{id}.json` | Timestamped transcript with speaker labels |
| 2 | Transcription | `outputs/transcripts/{date}-{id}.txt` | Plain text transcript |

## Procedure

### Phase 1: Audio Download

```bash
cd /tmp && yt-dlp -x --audio-format mp3 --no-playlist -o "video-to-text-%(id)s.%(ext)s" "<VIDEO_URL>"
```

Key flags:
- `-x`: extract audio only
- `--audio-format mp3`: standardize format
- `--no-playlist`: prevent playlist expansion
- `-o "video-to-text-%(id)s.%(ext)s"`: predictable filename

**Fallback chain** (try in order if the default command fails):
1. `--cookies-from-browser chrome` for auth-gated content
2. `--user-agent "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"` for UA blocks
3. `--extractor-args "twitter:api=syndication"` for Twitter API issues

After download, verify the file exists and check size:
```bash
ls -lh /tmp/video-to-text-*.mp3
```

### Phase 2: Transcription

```bash
cd ~/thaki/ai-platform-strategy && pnpm exec tsx scripts/transcribee/index.ts "/tmp/video-to-text-<ID>.mp3"
```

Output saved to `outputs/transcripts/`.

**If transcribee fails** (missing API key, service down): extract audio duration with `ffprobe` and report the failure with duration info so the user knows what content exists.

### Phase 3: Deliver Results

1. Read the transcript file from `outputs/transcripts/`
2. Present to user: speaker-labeled transcript + Korean summary of key points
3. Clean up temp audio: `rm /tmp/video-to-text-*.mp3`

## Gotchas

- Twitter/X URLs with `?s=20` query params work fine with yt-dlp; do not strip them
- Some Twitter videos are audio-less (GIFs, silent clips); yt-dlp will still produce an mp3 but it will be silent -- check file size (< 10KB = likely silent)
- yt-dlp auto-updates its extractors; run `yt-dlp -U` if extraction fails on a previously working site
- ElevenLabs free tier: 10,000 chars/month transcription limit; check `outputs/transcripts/` for existing transcripts before re-processing

## Constraints

- Audio > 100MB: warn user about processing time before proceeding
- Always clean up `/tmp/video-to-text-*` files after successful transcription
- Never re-download if the audio file already exists in `/tmp/` with matching ID
