---
name: pixelle-generate
description: Generate short-form videos using Pixelle-Video from a topic or script. Supports 3 modes (topic-based AI generation, fixed script, custom assets), voice/TTS selection, visual style, template choice, and BGM. Use when the user asks to "generate short video", "pixelle generate", "create video with pixelle", "숏폼 영상 생성", "Pixelle 영상 만들기", "AI video from topic", "pixelle-generate", or wants to produce a short video using the Pixelle-Video engine. Do NOT use for environment setup (use pixelle-setup). Do NOT use for template management only (use pixelle-template). Do NOT use for the full production pipeline with post-production and distribution (use pixelle-video-pipeline).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "standalone"
---

# pixelle-generate

Generate short-form videos from a topic or script using the Pixelle-Video engine.

## When to Use

- Generate a short video from a topic (AI writes the script)
- Generate a short video from a pre-written script
- Generate a video using custom pre-made assets (images/videos)
- Quick video prototyping without the full pipeline

## Prerequisites

Run `pixelle-setup` first to ensure the environment is ready.

## Generation Modes

### Mode 1: Topic-Based (AI Script Generation)

Provide a topic; the LLM writes narrations per scene automatically.

```python
import asyncio
from pixelle_video import PixelleVideoCore

async def generate_from_topic():
    core = PixelleVideoCore()
    await core.initialize()
    await core.generate_video(
        text="Why AI agents are the future of software development",
        pipeline="standard",
        mode="generate",
        n_scenes=5,
        min_narration_words=5,
        max_narration_words=20,
        frame_template="1080x1920/static_default.html",
        tts_voice="en-US-AriaNeural",
        tts_speed=1.2,
        bgm_volume=0.2,
    )

asyncio.run(generate_from_topic())
```

### Mode 2: Fixed Script

Provide a complete script; each paragraph/line becomes one scene.

```python
async def generate_from_script():
    core = PixelleVideoCore()
    await core.initialize()
    script = """AI agents can now write code autonomously.
They understand context across entire codebases.
The future of development is collaborative AI."""
    await core.generate_video(
        text=script,
        pipeline="standard",
        mode="fixed",
        split_mode="paragraph",
        frame_template="1080x1920/static_default.html",
        tts_voice="en-US-GuyNeural",
    )

asyncio.run(generate_from_script())
```

### Mode 3: Custom Assets (Asset-Based Pipeline)

Use pre-made images or video clips with script.

```python
async def generate_with_assets():
    core = PixelleVideoCore()
    await core.initialize()
    await core.generate_video(
        text="Your narration script here",
        pipeline="asset_based",
        # asset-specific params passed via kwargs
    )

asyncio.run(generate_with_assets())
```

## Parameters Reference

### Content Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `mode` | `"generate"` | `"generate"` (AI writes script) or `"fixed"` (use provided text) |
| `n_scenes` | `5` | Number of scenes to generate (generate mode only) |
| `min_narration_words` | `5` | Minimum words per narration |
| `max_narration_words` | `20` | Maximum words per narration |
| `split_mode` | `"paragraph"` | How to split fixed text: `"paragraph"` or by line |
| `title` | auto-generated | Video title (auto-determined by LLM if omitted) |

### Voice / TTS Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `tts_voice` | config default | Edge-TTS voice name (e.g., `en-US-AriaNeural`, `ko-KR-SunHiNeural`) |
| `tts_speed` | `1.2` | Speech speed multiplier |
| `tts_inference_mode` | config default | TTS inference mode |
| `tts_workflow` | config default | TTS ComfyUI workflow JSON path |
| `voice_id` | — | Voice ID for Index-TTS |
| `ref_audio` | — | Reference audio file path for voice cloning |

### Visual Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `frame_template` | `"1080x1920/static_default.html"` | HTML template for video frames |
| `prompt_prefix` | config default | Prefix prepended to all image prompts |
| `min_image_prompt_words` | `30` | Minimum words for image generation prompts |
| `max_image_prompt_words` | `60` | Maximum words for image generation prompts |
| `media_width` | template default | Output media width in pixels |
| `media_height` | template default | Output media height in pixels |
| `media_workflow` | config default | ComfyUI workflow for image/video generation |
| `template_params` | — | Extra parameters passed to the HTML template |

### Audio / BGM Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `bgm_path` | — | Path to background music file |
| `bgm_volume` | `0.2` | BGM volume (0.0-1.0) |
| `bgm_mode` | `"loop"` | BGM mode: `"loop"` or `"once"` |

### Output Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `output_path` | auto (`output/`) | Custom output directory path |
| `pipeline` | `"standard"` | Pipeline to use: `"standard"`, `"custom"`, `"asset_based"` |

## Available Pipelines

| Pipeline | Use Case |
|----------|----------|
| `standard` | Default — generates content, visuals, TTS, and composes video |
| `custom` | Custom workflow with user-defined pipeline steps |
| `asset_based` | Uses pre-made image/video assets instead of AI generation |

## Template Quick Reference

Templates determine video layout and aspect ratio. Names indicate media requirements:

| Prefix | Requires |
|--------|----------|
| `static_*` | No AI media — text/narration only (no ComfyUI needed) |
| `image_*` | AI-generated images per scene (needs ComfyUI or RunningHub) |
| `video_*` | AI-generated video clips per scene (needs ComfyUI or RunningHub) |

**Common templates:**

| Template | Aspect | Description |
|----------|--------|-------------|
| `1080x1920/static_default.html` | 9:16 portrait | Text-only, no AI media needed |
| `1080x1920/static_excerpt.html` | 9:16 portrait | Quote/excerpt style |
| `1080x1920/image_default.html` | 9:16 portrait | AI image per scene |
| `1080x1920/image_modern.html` | 9:16 portrait | Modern image layout |
| `1920x1080/image_film.html` | 16:9 landscape | Cinematic image layout |
| `1080x1080/image_minimal_framed.html` | 1:1 square | Minimal framed images |

See `pixelle-template` skill for the full catalog and customization guide.

## Edge-TTS Voice Examples

| Voice | Language | Gender |
|-------|----------|--------|
| `en-US-AriaNeural` | English (US) | Female |
| `en-US-GuyNeural` | English (US) | Male |
| `en-GB-SoniaNeural` | English (UK) | Female |
| `ko-KR-SunHiNeural` | Korean | Female |
| `ko-KR-InJoonNeural` | Korean | Male |
| `ja-JP-NanamiNeural` | Japanese | Female |
| `zh-CN-XiaoxiaoNeural` | Chinese | Female |

## Output Structure

```
vendor/Pixelle-Video/output/<timestamp>/
├── final_video.mp4          # Composed video
├── narrations/               # Generated narration texts
├── audio/                    # TTS audio files
├── frames/                   # Rendered frame images/videos
└── metadata.json             # Generation parameters
```

## Execution via Shell

```bash
cd vendor/Pixelle-Video
uv run python -c "
import asyncio
from pixelle_video import PixelleVideoCore

async def main():
    core = PixelleVideoCore()
    await core.initialize()
    await core.generate_video(
        text='Your topic or script here',
        pipeline='standard',
        mode='generate',
        n_scenes=3,
        frame_template='1080x1920/static_default.html',
        tts_voice='en-US-AriaNeural',
    )

asyncio.run(main())
"
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `pvideo` CLI | CLI is broken upstream; use Python API via `PixelleVideoCore` |
| Using `image_*` template without ComfyUI | Switch to `static_*` template or set up ComfyUI/RunningHub |
| Forgetting to call `await core.initialize()` | Always initialize before generating |
| Setting `n_scenes` in fixed mode | `n_scenes` is only for `"generate"` mode; fixed mode auto-splits by text |

## Examples

**User:** "AI 에이전트에 대한 숏폼 영상 만들어줘"
→ Mode 1 (topic-based): topic="AI agents", `static_default.html`, Edge-TTS `ko-KR-SunHiNeural`, 5 scenes

**User:** "generate a 30-second video from this script: ..."
→ Mode 2 (fixed script): pipeline="standard", mode="fixed", split_mode="paragraph"

**User:** "pixelle generate with my own images"
→ Mode 3 (asset-based): pipeline="asset_based", user provides image paths

## Seedance Prompt Integration

In `topic` mode, `seedance-video-prompts` provides tested prompt templates.
Use `prompt_library.py random` to get inspiration or a complete prompt
to pass as the `text` parameter:

```bash
# Get a random prompt for Pixelle topic mode
uv run .cursor/skills/standalone/seedance-video-prompts/scripts/prompt_library.py random

# Search by theme
uv run .cursor/skills/standalone/seedance-video-prompts/scripts/prompt_library.py search "comedy"

# Browse fantasy/surreal prompts for creative videos
uv run .cursor/skills/standalone/seedance-video-prompts/scripts/prompt_library.py by-category --category fantasy-surreal --limit 3
```

The returned prompt text can be used directly as the `text` parameter in any generation mode.
