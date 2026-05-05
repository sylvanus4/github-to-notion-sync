# Tooling and Fallbacks

## Dependency Check

Before running the workflow, verify these prerequisites:

```bash
python3 -c "import openai; print('openai OK')"
python3 -c "from PIL import Image; print('Pillow OK')"
ffmpeg -version | head -1
echo "OPENAI_API_KEY=${OPENAI_API_KEY:+SET}"
```

### Required

| Tool | Purpose | Install |
|------|---------|---------|
| Python 3.10+ | Script execution | System default |
| `openai` package | DALL-E 3 API calls | `pip install openai` |
| Pillow (PIL) | Grid splitting | `pip install Pillow` |
| FFmpeg + FFprobe | Video animation & assembly | `brew install ffmpeg` (macOS) |
| `OPENAI_API_KEY` | DALL-E 3 authentication | Set in `.env` |

### Optional

| Tool | Purpose |
|------|---------|
| Suno / Udio | Higher-quality background music (replaces synthetic BGM) |
| Pika / Runway | Image-to-video with motion (replaces Ken Burns if API available) |

## Image Generation: OpenAI DALL-E 3

### Character Grid (2x2)

```python
import openai, os, urllib.request

client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'])
response = client.images.generate(
    model='dall-e-3',
    prompt='<CHARACTER_GRID_PROMPT>',
    size='1024x1024',
    quality='hd',
    n=1
)
urllib.request.urlretrieve(response.data[0].url, 'character_grid.png')
```

- Size: 1024x1024 (square for even quadrant split)
- Quality: `hd` for detail retention after splitting
- Cost: ~$0.08 per image

### Scene Images (landscape)

```python
response = client.images.generate(
    model='dall-e-3',
    prompt='<SCENE_PROMPT>',
    size='1792x1024',
    quality='hd',
    n=1
)
```

- Size: 1792x1024 (landscape for cinematic Ken Burns)
- Quality: `hd` for zoompan detail
- Cost: ~$0.12 per image
- Rate limit: add `time.sleep(1)` between calls

## Grid Splitting: Pillow

```python
from PIL import Image
import os

grid = Image.open('character_grid.png')
w, h = grid.size
hw, hh = w // 2, h // 2

poses = ['front', 'side', 'back', 'cafe']
coords = [(0, 0, hw, hh), (hw, 0, w, hh), (0, hh, hw, h), (hw, hh, w, h)]

os.makedirs('characters', exist_ok=True)
for name, box in zip(poses, coords):
    grid.crop(box).save(f'characters/{name}.png')
```

## Image-to-Video: FFmpeg Ken Burns

Animate a static image with a slow zoom-in effect:

```bash
ffmpeg -y -loop 1 -i scene.png \
  -vf "zoompan=z='min(zoom+0.0015,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=150:s=1920x1080:fps=30" \
  -t 5 -c:v libx264 -pix_fmt yuv420p clip.mp4
```

Parameters:
- `zoom+0.0015`: zoom speed (1.0x to ~1.5x over 5s)
- `d=150`: 5 seconds at 30fps
- `s=1920x1080`: output resolution
- `-t 5`: duration limit

### Fallback: Pika / Runway

If image-to-video APIs are available with real motion:
```python
# Pika API example (if PIKA_API_KEY available)
# Produces actual camera movement and subject animation
# Superior to Ken Burns but requires API access
```

## Video Concatenation: FFmpeg

### Simple concat (same codec)

```bash
# Create file list
for f in clips/clip_*.mp4; do echo "file '$f'"; done > clips/filelist.txt

# Concat without re-encoding
ffmpeg -y -f concat -safe 0 -i clips/filelist.txt -c copy vlog_no_music.mp4
```

### With crossfade transitions

```bash
ffmpeg -y -i clip_01.mp4 -i clip_02.mp4 -i clip_03.mp4 -i clip_04.mp4 -i clip_05.mp4 \
  -filter_complex "\
    [0:v][1:v]xfade=transition=fade:duration=0.5:offset=4.5[v01];\
    [v01][2:v]xfade=transition=fade:duration=0.5:offset=9.0[v012];\
    [v012][3:v]xfade=transition=fade:duration=0.5:offset=13.5[v0123];\
    [v0123][4:v]xfade=transition=fade:duration=0.5:offset=18.0[vout]" \
  -map "[vout]" -c:v libx264 -pix_fmt yuv420p vlog_no_music.mp4
```

## Background Music: FFmpeg Synthesis

Generate warm ambient chord (A-minor: 220Hz + 277Hz + 330Hz):

```bash
ffmpeg -y \
  -f lavfi -i "sine=frequency=220:duration=25" \
  -f lavfi -i "sine=frequency=277:duration=25" \
  -f lavfi -i "sine=frequency=330:duration=25" \
  -filter_complex "\
    [0:a]volume=0.15[a0];\
    [1:a]volume=0.12[a1];\
    [2:a]volume=0.10[a2];\
    [a0][a1][a2]amix=inputs=3:duration=first[mixed];\
    [mixed]afade=t=in:ss=0:d=2,afade=t=out:st=23:d=2,lowpass=f=800[out]" \
  -map "[out]" -c:a aac -b:a 128k bgm_ambient.m4a
```

## Audio Mixing: Final Assembly

```bash
ffmpeg -y -i vlog_no_music.mp4 -i bgm_ambient.m4a \
  -filter_complex "[1:a]volume=0.6[bgm];[bgm]apad[bgmpad]" \
  -map 0:v -map "[bgmpad]" \
  -c:v copy -c:a aac -b:a 128k -shortest \
  final_vlog.mp4
```

- `volume=0.6`: BGM at 60% to not overpower visuals
- `apad`: extend audio to match video length
- `-shortest`: trim to video duration
- `-c:v copy`: no video re-encoding (fast)

## Cost Estimation

| Asset | Count | Cost Each | Total |
|-------|-------|-----------|-------|
| Character grid (1024x1024 HD) | 1 | $0.08 | $0.08 |
| Scene images (1792x1024 HD) | 5 | $0.12 | $0.60 |
| FFmpeg processing | N/A | $0.00 | $0.00 |
| **Total** | | | **~$0.68** |

## Fallback Chain

```
DALL-E 3 (primary)
  ↓ rate limit / quota
Retry with exponential backoff (3 attempts)
  ↓ persistent failure
Manual image provision (user uploads)
  ↓
FFmpeg Ken Burns (always available locally)
```
