# Supported Formats

## URL Sources

| Platform | URL Patterns |
|----------|-------------|
| YouTube | `youtube.com/watch?v=...`, `youtu.be/...` |
| Instagram | `instagram.com/reel/...`, `instagram.com/p/...` |
| TikTok | `vt.tiktok.com/...`, `tiktok.com/@user/video/...` |

All URL downloads use yt-dlp. YouTube URLs use `android,web` player clients to bypass restrictions.

## Local File Formats

### Audio (direct transcription)

| Extension | Format |
|-----------|--------|
| `.mp3` | MPEG Audio Layer 3 |
| `.m4a` | MPEG-4 Audio |
| `.wav` | Waveform Audio |
| `.ogg` | Ogg Vorbis |
| `.flac` | Free Lossless Audio Codec |

### Video (audio extracted via ffmpeg)

| Extension | Format |
|-----------|--------|
| `.mp4` | MPEG-4 Video |
| `.mkv` | Matroska Video |
| `.webm` | WebM Video |
| `.mov` | QuickTime Movie |
| `.avi` | Audio Video Interleave |

Video files have audio extracted to m4a (AAC, 192kbps) before transcription.

## Input Detection

The tool auto-detects input type:
- Starts with `http://` or `https://` → URL mode (yt-dlp download)
- Otherwise → local file mode (direct read or ffmpeg extraction)
