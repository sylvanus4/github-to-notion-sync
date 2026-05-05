# Virtual Couple Travel Vlog

Generate a complete "virtual couple travel vlog" video from a single theme sentence. Produces identity-consistent character grids, travel scene images, animated video clips with Ken Burns effect, ambient background music, and a fully assembled final vlog -- all using OpenAI DALL-E 3 for image generation and FFmpeg for video production. No external video generation API required.

Use when the user asks to "create a virtual couple travel vlog", "generate couple travel content", "travel vlog workflow", "virtual-couple-travel-vlog", "couple travel assets", "커플 여행 브이로그", "가상 커플 여행", or provides a theme like "A young couple in Paris travel vlog". Do NOT use for general video editing (use video-editing-planner). Do NOT use for single image generation without the full vlog pipeline (use muapi-image-studio or pika-text-to-video). Do NOT use for real-person content production (this skill generates AI-generated digital characters only).

---

## Identity

- **Name**: virtual-couple-travel-vlog
- **Version**: 2.0.0
- **Category**: Content Production / Video Pipeline
- **Trigger phrases**: "virtual couple travel vlog", "couple travel vlog", "travel vlog workflow", "generate couple vlog", "커플 여행 브이로그", "가상 커플 여행", "anime couple vlog", "AI travel video"

---

## Operating Rules

1. **Ask before creating** -- Always confirm the output root directory with the user before writing any files. Never assume a default path.
2. **Identity consistency first** -- Generate the 4x4 grid as a single image to lock couple identity, then split into 2x2 sheets. Never generate four separate 2x2 images independently.
3. **No silent installs** -- If dependencies are missing, inform the user and suggest installation commands. Never install packages silently.
4. **No silent credit consumption** -- Before submitting Topview Quick Generate or any paid API call, show estimated cost and get explicit user confirmation.
5. **No file deletion** -- Never delete project files. If cleanup is needed, ask the user for explicit confirmation.
6. **No real portraits** -- To avoid likeness rights and privacy risks, always use fully AI-generated digital characters. Never use real person photos or unauthorized likenesses.
7. **Graceful degradation** -- If video generation APIs are unavailable, still produce the complete manual delivery package (images, prompts, character cards).

---

## Dependencies

Run the dependency checker to verify local tooling:

```bash
python "<skill-folder>/scripts/check-tools.py" --show-install-hints
```

### Required

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Script execution and API calls |
| `openai` Python package | DALL-E 3 image generation |
| Pillow (PIL) | Grid splitting and image manipulation |
| FFmpeg + FFprobe | Ken Burns animation, video concat, audio mixing |
| `OPENAI_API_KEY` in `.env` | Authentication for DALL-E 3 |

### Optional

| Tool | Purpose |
|------|---------|
| Suno / Udio | Higher-quality background music (skill generates synth BGM by default) |

---

## Task List (7-Step DALL-E 3 + FFmpeg Workflow)

| # | Task | Tool | Output |
|---|------|------|--------|
| 1 | Dependency check | Shell | Verify Python, Pillow, FFmpeg, OPENAI_API_KEY |
| 2 | Create project folder + brief | Agent | `outputs/vlog/{date}/brief.md` |
| 3 | Generate character grid (2x2) | DALL-E 3 | `character_grid.png` (1024x1024) |
| 4 | Split grid into 4 poses | Pillow | `characters/{front,side,back,cafe}.png` |
| 5 | Generate 5 scene images | DALL-E 3 | `scenes/scene_01..05.png` (1792x1024) |
| 6 | Animate scenes (Ken Burns) | FFmpeg zoompan | `clips/clip_01..05.mp4` (5s each) |
| 7 | Assemble final vlog + BGM | FFmpeg concat+audio | `final_vlog.mp4` (~25s) |

---

## Tool Routing

| Operation | Primary Tool | Fallback |
|-----------|-------------|----------|
| Character grid | OpenAI DALL-E 3 (1024x1024, hd) | Midjourney / manual |
| Scene images | OpenAI DALL-E 3 (1792x1024, hd) | Midjourney / manual |
| Grid splitting | Pillow `Image.crop()` | Manual crop |
| Image-to-video | FFmpeg `zoompan` (Ken Burns) | Pika / Runway (if API available) |
| Video concat | FFmpeg `concat` demuxer | Manual editor |
| Background music | FFmpeg `sine` + `amix` | Suno / Udio |
| Audio mixing | FFmpeg `volume` + `apad` + `shortest` | Audacity |

---

## Output Structure

```
outputs/vlog/{YYYY-MM-DD}/
  brief.md
  character_grid.png
  characters/
    front.png
    side.png
    back.png
    cafe.png
  scenes/
    scene_01_*.png
    scene_02_*.png
    scene_03_*.png
    scene_04_*.png
    scene_05_*.png
  clips/
    clip_01.mp4
    clip_02.mp4
    clip_03.mp4
    clip_04.mp4
    clip_05.mp4
  vlog_no_music.mp4
  bgm_ambient.m4a
  final_vlog.mp4
```

---

## Key Strategies

### Identity Consistency (2x2 Grid Method)

Generate ONE 2x2 grid image containing the same couple in 4 poses within a single DALL-E 3 call. This locks identity (face, hair, clothing) because the model generates all poses in one context.

Workflow:
1. Generate 2x2 grid (1024x1024) with consistent couple across 4 quadrants.
2. Split locally into 4 pose reference images via Pillow.
3. Reference the couple description in all subsequent scene prompts to maintain consistency.

### Scene Image Prompts

Each scene prompt MUST include the exact character description from the grid prompt to maintain visual consistency across scenes:
- Same clothing, hair color/style, body proportions
- Vary only the background/environment and pose
- Use landscape aspect ratio (1792x1024) for cinematic feel

### Ken Burns Animation (Image-to-Video)

Static images are animated using FFmpeg's `zoompan` filter:
- Slow zoom-in (1.0x to 1.5x over 5 seconds)
- Center-focused pan
- 30fps, 1920x1080 output
- `libx264` encoding with `yuv420p` pixel format

### Synthetic Background Music

FFmpeg generates ambient background music using layered sine waves:
- 3 frequencies (220Hz, 277Hz, 330Hz) for a warm A-minor chord
- `amix` to blend, `lowpass=f=800` for warmth
- Fade in (2s) and fade out (2s) for clean edges
- Duration matches final video length

For higher quality, replace with Suno/Udio-generated BGM.

### Video Assembly Pipeline

```bash
# 1. Concat clips with crossfade transitions
ffmpeg -i clip_01.mp4 -i clip_02.mp4 ... \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=4.5..." \
  vlog_no_music.mp4

# 2. Mix BGM at 60% volume, pad to video length
ffmpeg -i vlog_no_music.mp4 -i bgm_ambient.m4a \
  -filter_complex "[1:a]volume=0.6[bgm];[bgm]apad[bgmpad]" \
  -map 0:v -map "[bgmpad]" -c:v copy -c:a aac -shortest \
  final_vlog.mp4
```

---

## References

- `references/task_list.md` -- 7-step workflow with acceptance criteria
- `references/prompts.md` -- DALL-E 3 prompt templates + FFmpeg command reference
- `references/tooling.md` -- Tool-specific commands and fallback logic

---

## Safety

- All assets are saved under the user-chosen output root directory.
- No file deletion without explicit user confirmation.
- No silent package/skill installation.
- OPENAI_API_KEY consumed per DALL-E 3 call (~$0.08/image HD, ~$0.12/image HD landscape).
- Use only AI-generated digital characters for public-facing content.
- Total estimated cost per vlog: ~$0.72 (6 DALL-E 3 images + FFmpeg local processing).
