---
name: ffmpeg-toolkit
description: >-
  Comprehensive ffmpeg/ffprobe CLI toolkit for multimedia operations beyond simple compression.
  ALWAYS invoke when the user asks to "convert video format", "trim video", "extract audio",
  "merge videos", "add subtitles", "create gif", "generate thumbnail", "change resolution",
  "adjust bitrate", "apply video filter", "map streams", "create HLS", "segment video",
  "probe media info", "mux audio video", "strip audio", "rotate video", "crop video",
  "concat videos", "watermark video", "speed up video", "slow down video", "extract frames",
  "transcode", "remux", "normalize audio", "ffmpeg", "ffprobe", "비디오 변환", "영상 자르기",
  "오디오 추출", "영상 합치기", "자막 삽입", "자막 번인", "GIF 변환", "썸네일 추출",
  "해상도 변경", "비트레이트 조정", "필터 적용", "HLS 생성", "미디어 정보", "영상 회전",
  "영상 크롭", "워터마크", "속도 변경", "프레임 추출", "오디오 정규화", "ffmpeg-toolkit",
  "burn subtitles", "embed srt", "hardcode subtitles", "batch convert", "일괄 변환",
  "메타데이터", "metadata", "hardware acceleration", "하드웨어 가속".
  Do NOT use for video compression only without other operations (use video-compress).
  Do NOT use for AI-powered video generation (use pika-text-to-video).
  Do NOT use for video editing plans without ffmpeg execution (use video-editing-planner).
  Do NOT use for downloading videos from URLs (use reclip-media-downloader).
  Do NOT use for subtitle file formatting from transcripts (use caption-subtitle-formatter).
metadata:
  author: "thaki"
  version: "1.3.0"
  category: "execution"
  platforms: [darwin, linux]
  tags: [ffmpeg, ffprobe, video, audio, multimedia, transcode, encode, mux, filter, hls, dash, gif, subtitle, streaming]
---

# ffmpeg-toolkit

Comprehensive CLI toolkit wrapping ffmpeg 7.x and ffprobe for granular multimedia operations. Exposes the full parameter surface of ffmpeg through structured workflows covering 15 operation categories.

## Quick Reference

Find the right category instantly:

| I want to... | Category | Key Flag |
|---|---|---|
| Change container (MKV to MP4) | 1: Format Conversion | `-c:v copy -c:a aac` |
| Cut a clip from a video | 2: Trimming | `-ss -to -c copy` |
| Extract / replace / normalize audio | 3: Audio Operations | `-vn`, `-an`, `loudnorm` |
| Resize video | 4: Resolution | `-vf scale=W:H` |
| Control quality / file size | 5: Bitrate | `-crf`, `-b:v`, 2-pass |
| Crop, rotate, watermark, speed | 6: Video Filters | `-vf` chain |
| Pick specific streams | 7: Stream Mapping | `-map` |
| Join multiple files | 8: Concatenation | `-f concat` or `filter_complex` |
| Extract frames / thumbnails | 9: Thumbnails | `-frames:v 1` |
| Create animated GIF | 10: GIF | palette 2-pass |
| Adaptive streaming | 11: HLS/DASH | `-hls_time`, `-f dash` |
| Inspect media properties | 12: ffprobe | `ffprobe -show_streams` |
| Add / burn / extract subtitles | 13: Subtitles | `-vf subtitles=`, `-c:s` |
| Process many files at once | 14: Batch | `for f in *.ext` loop |
| Edit metadata tags | 15: Metadata | `-metadata`, `-map_metadata` |

## Constraints

- **Low freedom**: every ffmpeg command is constructed from validated parameters, never from unfiltered user prose
- Always validate input files exist before building commands
- Always use `-y` flag to overwrite output without interactive prompts
- Never delete or overwrite the original source file
- Output filenames follow `{stem}_{operation}.{ext}` convention in the same directory as input
- For commands expected to run >30s, use `block_until_ms: 0` to background
- Never commit output media files to git
- Prefer hardware-accelerated codecs when available (`h264_videotoolbox` on macOS, `h264_nvenc` on NVIDIA)
- Cap filter chain complexity at 10 filters per command; split into multi-pass for more
- Always quote file paths containing spaces with double quotes

## Prerequisites

- `ffmpeg` >= 6.0 (verified: `ffmpeg -version`)
- `ffprobe` >= 6.0 (bundled with ffmpeg)
- macOS: `brew install ffmpeg`; Linux: `apt install ffmpeg` or `dnf install ffmpeg`

## Workflow

### Step 0: Probe Input

Before any operation, probe the input to understand its streams:

```bash
ffprobe -v quiet -print_format json -show_format -show_streams "<INPUT>"
```

Extract and report:
- Container format, duration, overall bitrate
- Video: codec, resolution, fps, pixel format, bitrate
- Audio: codec, sample rate, channels, bitrate
- Subtitle streams (if any)

This data drives parameter selection in subsequent steps.

### Step 1: Select Operation Category

Match the user's request to one of the 12 categories below. If multiple categories apply, chain them in a single ffmpeg command using filter_complex or multi-output.

### Step 2: Build Command

Construct the ffmpeg command from validated parameters. Use the category-specific reference sections below.

### Step 3: Execute

Run the command. For long operations (>30s estimated from input duration and operation), background it.

### Step 4: Verify Output

After execution:
1. Check exit code (0 = success)
2. Probe the output file to confirm expected properties
3. Report: input size, output size, duration match, stream properties

## Operation Categories

### Category 1: Format Conversion

Convert between container formats while preserving or re-encoding streams.

| Parameter | Description | Example Values |
|-----------|-------------|----------------|
| `-c:v` | Video codec | `libx264`, `libx265`, `libvpx-vp9`, `libaom-av1`, `copy` |
| `-c:a` | Audio codec | `aac`, `libopus`, `libmp3lame`, `pcm_s16le`, `copy` |
| `-f` | Force output format | `mp4`, `mkv`, `webm`, `mov`, `avi`, `flv` |
| `-movflags +faststart` | MP4 web optimization | Required for MP4 web playback |

Common conversions:
- MKV to MP4: `-c:v copy -c:a aac -movflags +faststart`
- MOV to WebM: `-c:v libvpx-vp9 -crf 30 -c:a libopus`
- Any to GIF: see Category 10

### Category 2: Trimming and Splitting

Cut segments from media files.

| Parameter | Description | Example |
|-----------|-------------|---------|
| `-ss` | Start time (before `-i` = fast seek) | `00:01:30`, `90` |
| `-to` | End time | `00:02:45` |
| `-t` | Duration from start point | `60` (60 seconds) |
| `-c copy` | Stream copy (no re-encode, fast) | Keyframe-aligned |
| `-avoid_negative_ts make_zero` | Fix PTS after cutting | Required with `-ss` before `-i` |

Fast trim (stream copy): `-ss 00:01:30 -i input.mp4 -to 00:02:45 -c copy -avoid_negative_ts make_zero output.mp4`
Precise trim (re-encode): `-i input.mp4 -ss 00:01:30 -to 00:02:45 -c:v libx264 -c:a aac output.mp4`

### Category 3: Audio Operations

Extract, replace, strip, normalize, or convert audio.

| Operation | Command Pattern |
|-----------|----------------|
| Extract audio | `-i input.mp4 -vn -c:a copy output.aac` |
| Strip audio | `-i input.mp4 -an -c:v copy output.mp4` |
| Replace audio | `-i video.mp4 -i audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4` |
| Normalize (EBU R128, 1-pass) | `-i input.mp4 -af loudnorm=I=-16:TP=-1.5:LRA=11 -c:v copy output.mp4` |
| Normalize (EBU R128, 2-pass accurate) | Pass 1: `ffmpeg -i input.mp4 -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null /dev/null 2>&1 \| grep -A20 "Parsed_loudnorm"` → extract measured_I, measured_TP, measured_LRA, measured_thresh, offset. Pass 2: `ffmpeg -i input.mp4 -af "loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=<val>:measured_TP=<val>:measured_LRA=<val>:measured_thresh=<val>:offset=<val>:linear=true" -c:v copy output.mp4` |
| Volume adjust | `-i input.mp4 -af "volume=1.5" -c:v copy output.mp4` |
| Convert to MP3 | `-i input.wav -c:a libmp3lame -b:a 192k output.mp3` |
| Fade in/out | `-af "afade=t=in:ss=0:d=2,afade=t=out:st=58:d=2"` |

### Category 4: Resolution and Scaling

Change video dimensions.

| Parameter | Description | Example |
|-----------|-------------|---------|
| `-vf scale=W:H` | Scale to exact size | `scale=1920:1080` |
| `-vf scale=W:-1` | Scale width, auto height | `scale=1280:-1` (720p) |
| `-vf scale=-1:H` | Scale height, auto width | `scale=-1:720` |
| `-vf scale=W:H:force_original_aspect_ratio=decrease` | Fit within bounds | Preserves aspect ratio |
| `-vf "scale=W:H,pad=W:H:(ow-iw)/2:(oh-ih)/2"` | Scale + letterbox | Center with black bars |

### Category 5: Bitrate and Quality Control

Control output quality and file size.

| Mode | Parameter | Description |
|------|-----------|-------------|
| CRF (recommended) | `-crf N` | 0=lossless, 23=default, 51=worst. H264: 18-28 typical |
| CBR | `-b:v Nk` | Constant bitrate: `2000k`, `5000k` |
| VBR | `-minrate Nk -maxrate Nk -bufsize Nk` | Variable bitrate with bounds |
| 2-pass | Pass 1: `-pass 1 -f null /dev/null`; Pass 2: `-pass 2` | Best for target file size |
| Target size | Calculate: `bitrate = target_size_bits / duration_seconds` | Use 2-pass with computed bitrate |

Preset speed vs compression: `-preset ultrafast|superfast|veryfast|faster|fast|medium|slow|slower|veryslow`

### Category 6: Video Filters

Apply visual transformations via `-vf` (single) or `-filter_complex` (multi-input).

| Filter | Syntax | Purpose |
|--------|--------|---------|
| `crop` | `crop=w:h:x:y` | Crop region |
| `rotate` | `rotate=PI/2` (radians) | Arbitrary rotation |
| `transpose` | `transpose=1` (90 CW) | 90-degree rotations |
| `hflip` / `vflip` | `hflip` | Mirror |
| `setpts` | `setpts=0.5*PTS` | Speed up 2x |
| `fps` | `fps=30` | Change framerate |
| `drawtext` | `drawtext=text='Hello':fontsize=24:fontcolor=white:x=10:y=10` | Text overlay |
| `overlay` | `overlay=W-w-10:H-h-10` (filter_complex) | Watermark |
| `eq` | `eq=brightness=0.1:contrast=1.2:saturation=1.3` | Color adjustment |
| `unsharp` | `unsharp=5:5:1.0` | Sharpen |
| `boxblur` | `boxblur=10:1` | Blur |
| `colorchannelmixer` | `colorchannelmixer=.3:.4:.3:0:.3:.4:.3:0:.3:.4:.3` | Grayscale |
| `deinterlace` | `yadif` | Deinterlace |
| `denoise` | `nlmeans` or `hqdn3d` | Noise reduction |
| `pad` | `pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black` | Add padding |

Chain filters with commas: `-vf "scale=1280:-1,fps=30,eq=brightness=0.05"`

### Category 7: Stream Mapping

Select specific streams from multi-stream files.

| Parameter | Description | Example |
|-----------|-------------|---------|
| `-map 0` | All streams from input 0 | Default behavior |
| `-map 0:v:0` | First video stream | Video only |
| `-map 0:a:1` | Second audio stream | Language selection |
| `-map 0:s:0` | First subtitle stream | Subtitle extraction |
| `-map -0:d` | Exclude data streams | Clean output |

Multi-input mapping: `-i video.mp4 -i audio.m4a -i subs.srt -map 0:v -map 1:a -map 2:s`

### Category 8: Concatenation

Join multiple media files sequentially.

**Method 1: concat demuxer** (same codec, fast):
```bash
# Create file list
echo "file 'part1.mp4'" > list.txt
echo "file 'part2.mp4'" >> list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4
```

**Method 2: filter_complex** (different codecs, re-encode):
```bash
ffmpeg -i part1.mp4 -i part2.mp4 -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[outv][outa]" -map "[outv]" -map "[outa]" output.mp4
```

### Category 9: Thumbnail and Frame Extraction

| Operation | Command |
|-----------|---------|
| Single frame at time | `-ss 00:00:05 -i input.mp4 -frames:v 1 thumb.jpg` |
| Every N seconds | `-i input.mp4 -vf "fps=1/10" frame_%04d.jpg` |
| Tile/contact sheet | `-vf "fps=1/30,scale=320:-1,tile=5x4" -frames:v 1 sheet.jpg` |
| Best quality frame | `-ss 5 -i input.mp4 -frames:v 1 -q:v 2 thumb.jpg` |
| Animated preview | `-ss 10 -t 3 -i input.mp4 -vf "fps=10,scale=480:-1" preview.gif` |

### Category 10: GIF Creation

```bash
# Step 1: Generate palette for quality
ffmpeg -i input.mp4 -ss 5 -t 3 -vf "fps=15,scale=480:-1:flags=lanczos,palettegen" palette.png

# Step 2: Create GIF with palette
ffmpeg -i input.mp4 -i palette.png -ss 5 -t 3 -filter_complex "[0:v]fps=15,scale=480:-1:flags=lanczos[v];[v][1:v]paletteuse" output.gif
```

Parameters: fps (10-15 typical), scale width (320-640), duration (-t), start (-ss).

### Category 11: HLS/DASH Streaming

**HLS (HTTP Live Streaming):**
```bash
ffmpeg -i input.mp4 -c:v libx264 -c:a aac -hls_time 6 -hls_list_size 0 \
  -hls_segment_filename "segment_%03d.ts" playlist.m3u8
```

| Parameter | Description | Typical |
|-----------|-------------|---------|
| `-hls_time` | Segment duration (seconds) | 4-10 |
| `-hls_list_size` | Max playlist entries (0=all) | 0 |
| `-hls_segment_type` | `mpegts` or `fmp4` | mpegts |

**Multi-bitrate HLS** (adaptive streaming):
```bash
# 360p variant
ffmpeg -i input.mp4 -c:v libx264 -b:v 800k -c:a aac -b:a 96k \
  -vf scale=-2:360 -hls_time 6 -hls_list_size 0 \
  -hls_segment_filename "360p_%03d.ts" 360p.m3u8

# 720p variant
ffmpeg -i input.mp4 -c:v libx264 -b:v 2500k -c:a aac -b:a 128k \
  -vf scale=-2:720 -hls_time 6 -hls_list_size 0 \
  -hls_segment_filename "720p_%03d.ts" 720p.m3u8

# Master playlist (manual)
cat > master.m3u8 <<'MASTER'
#EXTM3U
#EXT-X-STREAM-INF:BANDWIDTH=896000,RESOLUTION=640x360
360p.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=2628000,RESOLUTION=1280x720
720p.m3u8
MASTER
```

**DASH:**
```bash
ffmpeg -i input.mp4 -c:v libx264 -c:a aac \
  -f dash -seg_duration 4 -use_template 1 -use_timeline 1 manifest.mpd
```

### Category 12: ffprobe Analysis

Detailed media inspection beyond Step 0.

| Query | Command |
|-------|---------|
| Duration only | `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 input.mp4` |
| Resolution | `ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 input.mp4` |
| Codec info | `ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,profile,level -of json input.mp4` |
| Bitrate | `ffprobe -v error -show_entries format=bit_rate -of default=noprint_wrappers=1:nokey=1 input.mp4` |
| Frame count | `ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=noprint_wrappers=1:nokey=1 input.mp4` |
| Keyframe intervals | `ffprobe -v error -select_streams v:0 -show_entries frame=pict_type,pts_time -of csv input.mp4 \| grep I` |
| Stream list | `ffprobe -v error -show_entries stream=index,codec_type,codec_name -of json input.mp4` |
| Chapter list | `ffprobe -v error -show_chapters -of json input.mp4` |
| Full JSON report | `ffprobe -v quiet -print_format json -show_format -show_streams input.mp4` |

### Category 13: Subtitle Operations

Burn-in (hardcode) or embed (soft) subtitles into video files.

| Operation | Command Pattern |
|---|---|
| Burn-in SRT (hardcode, permanent) | `-i input.mp4 -vf "subtitles=subs.srt:force_style='FontSize=24,FontName=Arial'" -c:a copy output.mp4` |
| Burn-in ASS/SSA (styled) | `-i input.mp4 -vf "ass=styled.ass" -c:a copy output.mp4` |
| Embed as soft subtitle (MKV) | `-i input.mp4 -i subs.srt -c:v copy -c:a copy -c:s srt output.mkv` |
| Embed as soft subtitle (MP4, mov_text) | `-i input.mp4 -i subs.srt -c:v copy -c:a copy -c:s mov_text output.mp4` |
| Extract subtitle to file | `-i input.mkv -map 0:s:0 output.srt` |
| Burn-in with custom position | `-vf "subtitles=subs.srt:force_style='Alignment=6,MarginV=40'"` (top-center) |
| Multiple subtitle tracks | `-i video.mp4 -i en.srt -i ko.srt -map 0:v -map 0:a -map 1 -map 2 -c:v copy -c:a copy -c:s srt -metadata:s:s:0 language=eng -metadata:s:s:1 language=kor output.mkv` |

Gotcha: Burn-in requires video re-encoding (cannot use `-c:v copy`). Soft embed with `-c:v copy` is fast but limited to containers that support subtitles (MKV=most, MP4=mov_text only).

### Category 14: Batch Processing

Process multiple files with consistent parameters.

```bash
# Batch convert all MKV to MP4
for f in *.mkv; do
  ffmpeg -y -i "$f" -c:v libx264 -crf 23 -c:a aac -movflags +faststart "${f%.mkv}.mp4"
done

# Batch extract audio from all videos in a directory
for f in *.mp4; do
  ffmpeg -y -i "$f" -vn -c:a copy "${f%.mp4}_audio.aac"
done

# Batch resize to 720p
for f in *.mp4; do
  ffmpeg -y -i "$f" -vf scale=-2:720 -c:v libx264 -crf 23 -c:a copy "${f%.mp4}_720p.mp4"
done

# Parallel batch (4 jobs at once, requires GNU parallel)
find . -name "*.mov" | parallel -j4 'ffmpeg -y -i {} -c:v libx264 -crf 23 -c:a aac {.}.mp4'
```

Gotcha: Always use `"$f"` (quoted) in loops to handle filenames with spaces. Use `${f%.ext}` parameter expansion rather than sed/basename for output naming.

### Category 15: Metadata Manipulation

Read, write, and strip metadata tags.

| Operation | Command Pattern |
|---|---|
| Add title | `-metadata title="My Video"` |
| Add multiple tags | `-metadata title="Title" -metadata artist="Name" -metadata year="2026"` |
| Strip all metadata | `-map_metadata -1` |
| Copy metadata from another file | `-i source.mp4 -map_metadata 0 -c copy output.mp4` |
| Set language for audio track | `-metadata:s:a:0 language=kor` |
| Add chapter markers from file | `-i input.mp4 -i chapters.txt -map_metadata 1 -c copy output.mp4` |
| Set rotation (display matrix) | `-metadata:s:v rotate="90"` |

Read metadata: `ffprobe -v error -show_entries format_tags -of json input.mp4`

## Hardware Acceleration Detection

Before building commands, check available hardware encoders:

```bash
# macOS VideoToolbox
ffmpeg -hide_banner -encoders 2>/dev/null | grep -q videotoolbox && echo "HW: videotoolbox"

# NVIDIA NVENC
ffmpeg -hide_banner -encoders 2>/dev/null | grep -q nvenc && echo "HW: nvenc"

# Intel QSV
ffmpeg -hide_banner -encoders 2>/dev/null | grep -q qsv && echo "HW: qsv"

# VA-API (Linux)
ffmpeg -hide_banner -encoders 2>/dev/null | grep -q vaapi && echo "HW: vaapi"
```

Fallback chain: `h264_videotoolbox` (macOS) > `h264_nvenc` (NVIDIA) > `h264_qsv` (Intel) > `libx264` (software).
Hardware encoders are faster but may not support all `-vf` filters. If a filter chain fails with HW encoder, retry with `libx264`.

## Progress Monitoring

For long-running encodes, monitor progress:

```bash
# Print progress to stderr (default, human-readable)
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -stats output.mp4

# Machine-readable progress (for scripts)
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -progress pipe:1 output.mp4 2>/dev/null

# Estimate completion: compare frame= in output against total frames
TOTAL=$(ffprobe -v error -count_frames -select_streams v:0 \
  -show_entries stream=nb_read_frames -of default=noprint_wrappers=1:nokey=1 input.mp4)
echo "Total frames: $TOTAL"
```

For backgrounded operations, redirect progress to a file: `-progress /tmp/ffmpeg_progress.log`

## Output Naming Convention

| Operation | Output Pattern | Example |
|-----------|---------------|---------|
| Format conversion | `{stem}.{new_ext}` | `demo.webm` |
| Trim | `{stem}_trim_{start}-{end}.{ext}` | `demo_trim_90-165.mp4` |
| Audio extract | `{stem}_audio.{audio_ext}` | `demo_audio.aac` |
| Scale | `{stem}_{width}p.{ext}` | `demo_720p.mp4` |
| Filter | `{stem}_{filter}.{ext}` | `demo_grayscale.mp4` |
| Concat | `concat_{count}_{stem}.{ext}` | `concat_3_clips.mp4` |
| Thumbnail | `{stem}_thumb_{time}.jpg` | `demo_thumb_5s.jpg` |
| GIF | `{stem}.gif` | `demo.gif` |
| HLS | `{stem}/playlist.m3u8` | `demo/playlist.m3u8` |

## Output Size Estimation

Estimate output file size before encoding to avoid disk-full errors and set user expectations:

```
Target bitrate (kbps) = Target size (MB) * 8192 / Duration (seconds)

Examples:
  100 MB target, 600s video: 8192 * 100 / 600 = ~1365 kbps total
  Subtract audio (~128 kbps): video bitrate = ~1237 kbps

Quick estimates by CRF (H.264, 1080p, 30fps):
  CRF 18: ~8-12 Mbps (~60-90 MB/min)
  CRF 23: ~3-5 Mbps  (~22-37 MB/min)
  CRF 28: ~1-2 Mbps  (~7-15 MB/min)
```

For precise target sizing, use 2-pass encoding (Category 5) with the computed bitrate.

## Dry-Run Validation

Before executing a potentially expensive encode, verify the command parses correctly:

```bash
# Validate input — check streams without encoding
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,duration \
  -of json input.mp4

# Dry-run — process 5 seconds only to test the full pipeline
ffmpeg -i input.mp4 -t 5 -c:v libx264 -crf 23 -c:a aac test_clip.mp4

# Null output — verify filters and mapping without writing a file
ffmpeg -i input.mp4 -vf "scale=1280:720,fps=30" -f null /dev/null
```

Use `-f null /dev/null` to validate filter chains, stream mapping, and codec compatibility without producing output. Check exit code 0 before running the full encode.

## Error Handling

| Error | Symptom | Recovery |
|-------|---------|----------|
| File not found | `No such file or directory` | Verify path with `ls -la`; check for spaces in path |
| Codec not available | `Unknown encoder` | Check `ffmpeg -encoders \| grep <codec>`; install full ffmpeg build |
| Filter not found | `No such filter` | Check `ffmpeg -filters \| grep <filter>` |
| Permission denied | `Permission denied` | Check write permissions on output directory |
| Disk full | `No space left on device` | Run `df -h .` before starting |
| Invalid filter graph | `Error initializing filter` | Validate filter syntax; check input stream properties match filter requirements |
| Seek beyond duration | Truncated output | Probe duration first; clamp seek values |
| Concat codec mismatch | Garbled output with `-c copy` | Use filter_complex method (Method 2) instead |

## Gotchas

- `-ss` BEFORE `-i` enables fast seek (keyframe-based, imprecise by up to a GOP). After `-i` enables frame-accurate seek but reads from the start (slow on large files). Combine both: `-ss <approx> -i input -ss <fine_offset>` for best of both.
- MP4 container requires `-movflags +faststart` for web streaming; without it, the moov atom sits at the end and browsers cannot play while downloading.
- `scale=-1:720` can produce odd pixel dimensions (ffmpeg errors). Use `scale=-2:720` to force even numbers.
- GIF without palette generation produces banding artifacts. Always use the 2-pass palette method.
- Concat demuxer (`-f concat`) requires all files have identical codecs, resolution, and sample rate. Any mismatch requires the filter_complex method.
- `loudnorm` filter requires 2-pass for accurate normalization: first pass with `-f null /dev/null` to measure, second pass with measured values.
- Hardware encoders (`h264_videotoolbox`, `h264_nvenc`) do not support all CRF values or filter chains. Fall back to `libx264` if hardware encoding fails.
- When using `-filter_complex` with `-map`, you MUST map the named outputs explicitly; unmapped streams are silently dropped.

## Anti-Example -- Do NOT produce output like this:

> "Here's the ffmpeg command to convert your video:
> `ffmpeg -i input.mp4 output.webm`
> This should work for most cases."

This fails because: no codec specified (ffmpeg guesses poorly), no quality parameters, no `-y` flag, no validation of input existence, no output naming convention, no verification of result. Every ffmpeg command must have explicit codec, quality, and container parameters.

## See Also

- **video-compress** -- Optimized presets for compression-only workflows (simpler, preset-driven)
- **reclip-media-downloader** -- Download source videos from URLs before processing
- **caption-subtitle-formatter** -- Format subtitle files (SRT/VTT) from transcripts
- **video-editing-planner** -- Plan post-production edits (cut lists, transitions) without executing
- **pika-text-to-video** -- AI-generated video from text prompts
- **video-script-generator** -- Write video scripts with timing and visual direction
