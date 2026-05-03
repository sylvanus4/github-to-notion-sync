---
name: video-compress
description: >-
  Compress video files using ffmpeg with optimized presets. Use when the user
  asks to compress, shrink, or re-encode a video file, or mentions ffmpeg,
  demo recording, screen capture, video size reduction, or says "make this
  video smaller". Do NOT use for audio-only compression, image optimization,
  video editing/trimming, or format conversion without size reduction intent.
  Korean triggers: "비디오", "압축", "최적화".
---

# Video Compress

Compress video files using ffmpeg with configurable presets. Default preset is **H264-CRF32** (~14.9x compression, 93.3% size reduction).

## Input

The user provides:
1. **Video file path** (required) -- e.g. `~/Videos/demo.mov`
2. **Preset name** (optional) -- defaults to `h264-crf32`

## Presets

| Preset | Codec | CRF | ffmpeg Preset | Audio | Extra | Typical Ratio |
|---|---|---|---|---|---|---|
| `h264-crf32` (default) | libx264 | 32 | veryslow | AAC 96k | - | ~14.9x |
| `h264-crf28` | libx264 | 28 | fast | AAC 128k | - | ~12.2x |
| `720p` | libx264 | 28 | fast | AAC 128k | scale=1280:-1 | ~61.2x |
| `hevc` | libx265 | 28 | slow | AAC 128k | - | ~10.4x |
| `noaudio` | libx264 | 28 | fast | none | -an | ~12.2x |
| `all` | - | - | - | - | all presets in parallel | varies |

### Custom Parameters

Users may override defaults by specifying:
- **CRF value** (0-51, lower = higher quality, larger file)
- **Resolution** (e.g. `1280:-1` for 720p, `1920:-1` for 1080p)
- **Audio bitrate** (e.g. `64k`, `128k`, `256k`)
- **Codec** (`libx264`, `libx265`)

When custom parameters are given, build the ffmpeg command manually instead of using a preset.

## Workflow

### Step 1: Validate Input

Check that the input file exists and has a recognized video extension:

```bash
ls -lh "<INPUT_FILE>"
```

Supported extensions: `.mov`, `.mp4`, `.avi`, `.mkv`, `.webm`, `.flv`, `.m4v`, `.wmv`, `.ts`

If the file does not exist or is not a video, inform the user and stop.

### Step 2: Check ffmpeg

```bash
command -v ffmpeg
```

If ffmpeg is not found, install it:

| OS | Command |
|---|---|
| macOS (Homebrew) | `brew install ffmpeg` |
| Debian/Ubuntu | `sudo apt-get update && sudo apt-get install -y ffmpeg` |
| RHEL/CentOS/Fedora | `sudo dnf install -y ffmpeg` (or `sudo yum install -y ffmpeg`) |

Detect OS via `$OSTYPE` or by checking `/etc/debian_version`, `/etc/redhat-release`.

### Step 3: Record Original Size

```bash
ORIGINAL_SIZE=$(stat -f%z "<INPUT_FILE>" 2>/dev/null || stat -c%s "<INPUT_FILE>")
```

Store the raw byte count for the compression report.

### Step 4: Build and Run ffmpeg Command

Output file naming: `{name}_{preset}.mp4` in the same directory as the input.

For exact ffmpeg commands per preset, see [references/preset-commands.md](references/preset-commands.md).

Add `-y` flag to overwrite existing output files without prompting.

For long-running compressions (especially `veryslow` preset), use `block_until_ms: 0` in the Shell tool to background the process, then poll the terminal output for completion.

### Step 5: Compression Report

After compression completes, compare original vs compressed size and present ratio/reduction.

For report format templates (single preset and all-presets comparison), see [references/preset-commands.md](references/preset-commands.md).

## Examples

### Example 1: Default preset

User says: "~/Videos/demo.mov 영상 압축해줘"

Actions:
1. Validate `~/Videos/demo.mov` exists
2. Check ffmpeg installed
3. Run h264-crf32 preset (default)
4. Report: 208 MB → 14.5 MB (14.9x, 93.3% reduction)

Result: `~/Videos/demo_h264_crf32.mp4` created

### Example 2: Custom CRF value

User says: "이 영상 CRF 24로 좀 더 고화질로 압축해줘 ~/screen.mov"

Actions:
1. Validate file
2. Build custom command: `ffmpeg -y -i ~/screen.mov -vcodec libx264 -crf 24 -preset fast -acodec aac -b:a 128k ~/screen_custom.mp4`
3. Report compression results

Result: Higher quality output at CRF 24

## Error Handling

| Error | Action |
|---|---|
| File not found | Inform user with the exact path that was checked |
| Unsupported extension | List supported formats and ask user to confirm |
| ffmpeg not installed + install fails | Provide manual install instructions |
| ffmpeg encoding failure | Show the ffmpeg stderr output to the user |
| Output file already exists | Add `-y` flag to overwrite, or ask user |
| Disk space insufficient | Check available space with `df -h .` before starting |

## See Also

- **reclip-media-downloader** — Download source videos from URLs (YouTube, TikTok, etc.) before compressing them with this skill.

## Notes

- Compressed files are local artifacts; never commit or push them
- The `veryslow` preset (used by `h264-crf32`) trades encoding speed for better compression -- expect longer runtimes on large files
- HEVC (H.265) produces slightly larger files at the same CRF due to different codec characteristics, but offers better quality-per-bit at lower CRFs
- For screen recordings and demos, `h264-crf32` or `720p` are recommended
