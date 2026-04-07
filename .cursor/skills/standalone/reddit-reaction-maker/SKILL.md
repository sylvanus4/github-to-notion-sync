---
name: reddit-reaction-maker
description: Generate Korean-subtitled YouTube Shorts from Reddit posts/comments via a 6-phase pipeline (scrape → TTS → cards → backgrounds → compose → distribute). No Reddit API key required.
---

# Reddit Reaction Video Maker

## When to Use

Use when the user asks to "make a reddit reaction video", "reddit to shorts", "reddit video", "reddit shorts", "레딧 영상", "레딧 리액션 비디오", "레딧 숏폼", "레딧에서 영상 만들어줘", or wants to convert Reddit posts into short-form vertical videos with Korean narration.

Do NOT use for:
- General video generation without Reddit content (use `pika-text-to-video` or `remotion-motion-forge`)
- Video transcription (use `transcribee`)
- YouTube video editing plans (use `video-editing-planner`)
- Subtitle-only formatting (use `caption-subtitle-formatter`)

## Composable With

| Skill | When |
|-------|------|
| `video-compress` | Output > 50MB and needs compression for upload |
| `caption-subtitle-formatter` | Generate SRT/VTT from TTS segments |
| `content-repurposing-engine` | Repurpose the video script for other platforms |
| `agent-reach` | Fallback Reddit data via `rdt read`/`rdt search` if `.json` endpoint is rate-limited |

## Pipeline (6 Phases)

### Phase 1: Reddit Scrape

Fetch top/hot posts from the target subreddit using Reddit's public `.json` endpoints. No API key needed.

```bash
python -m scripts.main --subreddit korea --time-filter week --output outputs/reddit-reaction
```

Output: `outputs/reddit-reaction/{date}/phase-1-posts.json`

Skip: `--skip-scrape` (reuses cached posts)

### Phase 2: Script + TTS

Generate Korean TTS audio for each post title and top comments using gTTS.

Output: `outputs/reddit-reaction/{date}/phase-2-audio/{post_id}/*.mp3`

Skip: `--skip-tts`

### Phase 3: Card Rendering

Render Reddit-style title and comment cards as PNG images using Pillow with NotoSansKR font.

Output: `outputs/reddit-reaction/{date}/phase-3-cards/{post_id}/*.png`

Skip: `--skip-cards`

### Phase 4: Background Assets

Download background gameplay videos and lofi music via yt-dlp. Cached after first download.

Output: `assets/backgrounds/video/*.mp4`, `assets/backgrounds/audio/*.mp3`

Skip: `--skip-bg`

### Phase 5: Video Composition

Assemble final 9:16 vertical video (1080x1920) using MoviePy: background + dim overlay + card images timed to TTS + background music.

Output: `outputs/reddit-reaction/{date}/reddit_{post_id}_*.mp4`

Skip: `--skip-compose`

### Phase 6: Distribution (Optional)

Post video info and file to Slack `#효정-할일`. Handled by the agent after pipeline completion.

## Running the Skill

### Full pipeline

```bash
cd .cursor/skills/standalone/reddit-reaction-maker
python -m scripts.main --subreddit korea -t week -o ../../../../outputs/reddit-reaction
```

### Resume from Phase 3

```bash
python -m scripts.main --skip-scrape --skip-tts -o ../../../../outputs/reddit-reaction
```

### Custom config

```bash
python -m scripts.main --config custom_config.json
```

## Configuration

Default config lives at `config.json`. See `references/config-options.md` for all options.

Key defaults:
- **subreddit**: `korea`
- **language**: `ko` (Korean TTS and cards)
- **post_limit**: 3
- **video**: 1080x1920, max 58s, 30fps
- **font**: NotoSansKR-Bold.ttf (auto-downloaded)

## Prerequisites

Checked by `/setup-doctor --group reddit-reaction`:

| Tool | Install |
|------|---------|
| ffmpeg | `brew install ffmpeg` |
| yt-dlp | `pip install yt-dlp` |
| Python packages | `pip install requests gTTS moviepy Pillow rich yt-dlp` |
| Font | NotoSansKR-Bold.ttf — auto-downloaded on first run |

## Gotchas

1. **Reddit rate limiting**: The `.json` endpoint returns 429 if hit too frequently. The scraper waits 2s between requests and rotates User-Agent strings. If persistent, use `--skip-scrape` with cached data or fall back to `agent-reach` skill's `rdt` CLI.

2. **yt-dlp failures**: YouTube may block certain regions or videos. The pipeline continues with any available background files; if zero are available, a solid-color background is used.

3. **Font rendering**: If NotoSansKR auto-download fails (network issues), the script falls back to macOS system CJK fonts. On Linux, install `fonts-noto-cjk` manually.

4. **MoviePy 2.0 API**: This skill targets MoviePy 2.x. MoviePy 1.x uses different method names (`set_position` vs `with_position`). Check with `pip show moviepy`.

5. **Large video files**: Raw output can be 50-100MB. Use `video-compress` skill for Slack-friendly sizes (< 25MB).

6. **Korean text in comments**: Some Reddit posts mix English and Korean. The card renderer handles mixed scripts via NotoSansKR which covers Latin + CJK glyphs.
