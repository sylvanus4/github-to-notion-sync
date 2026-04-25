---
name: muapi-media-orchestrator
description: >-
  End-to-end media production pipeline orchestrating muapi-image-studio, muapi-cinema,
  muapi-lipsync, and distribution skills into multi-stage workflows. Supports 5 pipeline
  modes: product-showcase (image→cinema video→compress→distribute), talking-head
  (portrait+audio→lipsync→subtitles→distribute), content-series (batch image generation
  with consistent style), cinematic-story (multi-scene video with transitions), and
  custom pipeline (user-defined stage composition).
  Use when the user asks to "full media pipeline", "end-to-end video production",
  "media orchestrator", "muapi-media-orchestrator", "product video pipeline",
  "talking head pipeline", "content series", "cinematic story", "multi-stage media",
  "미디어 파이프라인", "종합 미디어 제작", "영상 제작 파이프라인", "콘텐츠 시리즈",
  "시네마틱 스토리", or any request to chain multiple Muapi generation steps into
  a single coherent production workflow.
  Do NOT use for single-step image generation (use muapi-image-studio).
  Do NOT use for single-step lip sync (use muapi-lipsync).
  Do NOT use for cinema prompt building alone (use muapi-cinema).
  Do NOT use for Pika-only video pipelines (use pika-video-pipeline).
  Do NOT use for non-Muapi media workflows (use video-editing-planner).
---

# Muapi Media Orchestrator

Chain multiple Muapi.ai generation capabilities into production-ready media workflows.

## Prerequisites

| Requirement | Check |
|---|---|
| `MUAPI_API_KEY` in environment | `echo $MUAPI_API_KEY` |
| Muapi service module | `python -c "from app.services.muapi import muapi_client"` (from `backend/`) |
| Sibling skills installed | muapi-image-studio, muapi-cinema, muapi-lipsync |

## Pipeline Modes

### 1. Product Showcase

Generate a product image, then animate it with cinema-grade camera movements.

```
[Text prompt] → muapi-image-studio (T2I)
    → [Generated image] → muapi-cinema (enriched prompt)
        → Muapi I2V model → [Video]
            → video-compress → [Optimized video]
                → Slack / Google Drive distribution
```

**Stages:**
1. Generate product hero image via T2I model (e.g., `flux-1.1-pro`)
2. Build cinema prompt with orbit camera, macro lens, shallow DOF
3. Submit image + enriched prompt to I2V model (e.g., `wan-i2v-720p`)
4. Compress output for distribution
5. Post to Slack / upload to Drive

### 2. Talking Head

Create a professional talking-head video from a portrait and audio.

```
[Portrait + Audio] → muapi-lipsync (e.g., infinitetalk)
    → [Talking video] → video-compress
        → caption-subtitle-formatter → [Subtitled video]
            → content-repurposing-engine → [Multi-platform variants]
```

**Stages:**
1. Upload portrait and audio to Muapi
2. Generate lip-synced video via lipsync model
3. Compress video
4. Generate subtitles from audio (via transcribee)
5. Format subtitles and overlay
6. Repurpose for multiple platforms (YouTube, LinkedIn, etc.)

### 3. Content Series

Batch-generate a series of images with consistent style for campaigns.

```
[Style reference + N prompts] → muapi-image-studio (batch T2I)
    → [N images with consistent style]
        → Optional: animate select images via I2V
```

**Stages:**
1. Define style parameters (model, aspect ratio, style reference)
2. Generate batch of images with sequential prompts
3. Quality-check outputs
4. Optionally animate key frames to video

### 4. Cinematic Story

Multi-scene video production with planned camera work per scene.

```
[Script with N scenes] → For each scene:
    muapi-cinema (scene-specific settings)
        → muapi T2V/I2V → [Scene video]
    → Concatenation plan → video-editing-planner
```

**Stages:**
1. Break script into scenes with camera direction per scene
2. Generate cinema-enriched prompts per scene
3. Generate videos per scene
4. Produce editing plan with transitions
5. Output as editing brief or assembled video

### 5. Custom Pipeline

User-defined stage composition from available capabilities.

```
[User defines stages] → Sequential execution with intermediate outputs
```

Available stage types:
- `generate_image`: T2I or I2I generation
- `generate_video`: T2V or I2V generation
- `lipsync`: Audio-driven lip sync
- `cinema_enrich`: Apply cinema settings to prompt
- `upload_file`: Upload local file to Muapi CDN
- `compress`: Compress video output
- `distribute`: Post to Slack / Drive

## Workflow Execution Pattern

```python
import asyncio
from app.services.muapi import (
    muapi_client,
    build_cinema_prompt,
    CinemaSettings,
    ModelCategory,
    get_models_by_category,
)

async def product_showcase(product_description: str):
    # Stage 1: Generate product image
    image_result = await muapi_client.generate_image(
        endpoint="flux-1.1-pro",
        prompt=f"professional product photograph, {product_description}, "
               f"studio lighting, white background, 8k",
        aspect_ratio="1:1",
    )

    # Stage 2: Build cinematic prompt
    settings = CinemaSettings(
        camera="orbit",
        lens="macro",
        focal_length=100,
        aperture="shallow",
    )
    cinema_prompt = build_cinema_prompt(
        f"elegant product rotation, {product_description}", settings
    )

    # Stage 3: Animate with I2V
    video_result = await muapi_client.generate_video(
        endpoint="wan-i2v-720p",
        prompt=cinema_prompt,
        image_url=image_result.output_url,
        resolution="720p",
    )

    return {
        "image_url": image_result.output_url,
        "video_url": video_result.output_url,
        "cinema_prompt": cinema_prompt,
    }
```

## Error Handling & Recovery

| Stage Failure | Recovery Strategy |
|---|---|
| Image generation fails | Retry with different model or simplified prompt |
| Video generation fails | Fall back to lower resolution, retry |
| Lipsync fails | Try alternative lipsync model |
| Upload fails | Retry with exponential backoff |
| Timeout on long video | Increase poll_max_attempts, check Muapi status |

Pipeline-level: Each stage persists its output URL. If a later stage fails, earlier results remain accessible for manual continuation or retry from the failed stage.

## Integration with Existing Skills

| Skill | Role in Pipeline |
|---|---|
| muapi-image-studio | Stage: image generation (T2I / I2I) |
| muapi-cinema | Stage: prompt enrichment with camera/lens |
| muapi-lipsync | Stage: audio-driven talking-head generation |
| video-compress | Post-stage: optimize file size |
| caption-subtitle-formatter | Post-stage: add subtitles |
| transcribee | Pre-stage: extract transcript for subtitles |
| content-repurposing-engine | Post-stage: multi-platform variants |
| video-script-generator | Pre-stage: write scene scripts |
| presentation-strategist | Pre-stage: plan visual narrative |
| gws-drive | Distribution: upload to Google Drive |
| kwp-slack-slack-messaging | Distribution: post to Slack channel |

## Concurrency & Cost

- Image generation: ~10-30 seconds per image
- Video generation: ~1-5 minutes per clip
- Lipsync: ~2-10 minutes depending on audio length
- Batch image series: Parallelize up to 3 concurrent requests
- Multi-scene video: Sequential (each scene depends on prompt consistency)

## Prompt Library as Input Source

For any pipeline mode, the initial text prompt can be sourced from
`seedance-video-prompts` instead of user-provided text:

```bash
# Random prompt for product showcase
uv run .cursor/skills/standalone/seedance-video-prompts/scripts/prompt_library.py random --category photography

# Search for themed prompts for cinematic story
uv run .cursor/skills/standalone/seedance-video-prompts/scripts/prompt_library.py search "fashion runway"

# Browse categories for content series
uv run .cursor/skills/standalone/seedance-video-prompts/scripts/prompt_library.py stats
```

Seedance prompts are model-agnostic text and work with all Muapi T2V/I2V endpoints.

## Environment Variables

Same as muapi-image-studio (shared Muapi service configuration).
