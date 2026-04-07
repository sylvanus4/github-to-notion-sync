# Config Options Reference

All options set in `config.json` at the skill root.

## Reddit Scraping

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `subreddit` | string | `"korea"` | Subreddit to scrape (without `r/` prefix) |
| `post_limit` | int | `3` | Max posts to fetch per run |
| `min_upvotes` | int | `50` | Minimum upvotes to include a post |
| `min_comments` | int | `5` | Minimum comments to include a post |
| `max_comment_length` | int | `300` | Truncate comments longer than this |
| `top_comments` | int | `5` | Max comments per post |

## Audio / TTS

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `language` | string | `"ko"` | gTTS language code. `ko` = Korean, `en` = English, `ja` = Japanese |

## Video

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `video_width` | int | `1080` | Output video width in pixels |
| `video_height` | int | `1920` | Output video height in pixels |
| `max_duration_seconds` | int | `58` | Max video duration (YouTube Shorts limit is 60s) |
| `fps` | int | `30` | Frames per second |
| `bg_opacity` | float | `0.7` | Background video visibility (0.0 = fully dimmed, 1.0 = no dim) |
| `screenshot_scale` | float | `0.9` | Card width as fraction of video width |
| `bgm_enabled` | bool | `true` | Enable background music |
| `bgm_volume` | float | `0.15` | Background music volume (0.0-1.0) |

## Rendering

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `font` | string | `"NotoSansKR-Bold.ttf"` | Font file for card text. Auto-downloaded if not found |
| `watermark` | string | `""` | Optional watermark text overlaid on video |

## Assets

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `background_dir` | string | `"assets/backgrounds"` | Directory for cached background videos/audio |

## Distribution

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `slack_channel` | string | `"C0AA8NT4T8T"` | Slack channel ID for posting video results |
