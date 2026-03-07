## Video Compress

Compress video files using ffmpeg with optimized presets. Default: H264-CRF32 (~14.9x compression).

### Usage

Provide a video file path and an optional preset:

```
<path-to-video> [preset]
```

### Presets

| Preset | Description | Typical Ratio |
|---|---|---|
| `h264-crf32` | Default. Strong compression, high quality (veryslow) | ~14.9x |
| `h264-crf28` | Balanced compression (fast) | ~12.2x |
| `720p` | Downscale to 720p | ~61.2x |
| `hevc` | H.265 codec (slow) | ~10.4x |
| `noaudio` | Strip audio track | ~12.2x |
| `all` | Run all presets in parallel | varies |

### Execution

Read and follow the `video-compress` skill (`.cursor/skills/video-compress/SKILL.md`) for detailed instructions, ffmpeg commands, and error handling.

### Examples

```bash
# Default (H264-CRF32)
/video-compress ~/Videos/demo.mov

# Specific preset
/video-compress ~/Videos/demo.mov 720p

# All presets for comparison
/video-compress ~/Videos/demo.mov all

# Custom CRF value
/video-compress ~/Videos/demo.mov h264-crf28
```
