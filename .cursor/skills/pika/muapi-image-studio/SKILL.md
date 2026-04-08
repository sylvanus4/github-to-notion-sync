---
name: muapi-image-studio
description: >-
  Generate images via the Muapi.ai gateway — text-to-image (T2I) and image-to-image (I2I)
  with 100+ models (Flux, SDXL, Midjourney-style, etc.), multi-image reference input (up to 14),
  aspect ratio control, and async result polling.
  Use when the user asks to "generate an image", "create AI art", "text to image",
  "image to image", "Muapi image", "muapi-image-studio", "Flux image", "SDXL generate",
  "multi-reference image", "이미지 생성", "AI 이미지", "텍스트 투 이미지", "이미지 투 이미지",
  "멀티 레퍼런스 이미지", or any request to produce AI-generated images via the Muapi gateway.
  Do NOT use for video generation (use pika-text-to-video or muapi-media-orchestrator).
  Do NOT use for lip sync (use muapi-lipsync).
  Do NOT use for cinema prompt tuning without image generation (use muapi-cinema).
  Do NOT use for static design/poster work without AI generation (use anthropic-canvas-design).
---

# Muapi Image Studio

Generate AI images through the Muapi.ai gateway with 100+ models across text-to-image and image-to-image categories.

## Prerequisites

| Requirement | Check |
|---|---|
| `MUAPI_API_KEY` in environment | `echo $MUAPI_API_KEY` |
| Python packages: `httpx`, `pydantic` | `pip list \| grep -E 'httpx\|pydantic'` |
| Muapi service module | `python -c "from app.services.muapi import muapi_client"` (from `backend/`) |

## Capabilities

### Text-to-Image (T2I)

Generate images from text prompts using models like Flux Dev/Pro, Nano Banana, Recraft V3, Ideogram, etc.

**Supported parameters:**
- `prompt` (required): Text description of the desired image
- `aspect_ratio`: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `21:9`, `9:21`
- Model-specific extras (varies by model)

### Image-to-Image (I2I)

Transform existing images using reference inputs. Some models accept up to 14 reference images.

**Supported parameters:**
- `prompt` (required): Text description guiding the transformation
- `image_urls`: List of 1-14 reference image URLs
- `aspect_ratio`: Same options as T2I
- Model-specific extras

### Multi-Image Reference

A distinguishing feature: provide multiple reference images to guide the generation. The service uploads local files via the Muapi file upload endpoint and passes the resulting URLs.

## Workflow

```
1. User provides prompt + optional reference images + model preference
2. Resolve model → look up endpoint from POPULAR_MODELS registry
3. Upload any local image files → get hosted URLs
4. Submit generation request → receive request_id
5. Poll for completion (2s intervals, up to 30 min)
6. Return output URL(s) and metadata
```

## Usage

### Quick T2I generation

```python
import asyncio
from app.services.muapi import muapi_client, get_models_by_category, ModelCategory

async def generate():
    result = await muapi_client.generate_image(
        endpoint="flux-dev",
        prompt="A cyberpunk cityscape at golden hour, neon reflections on wet streets",
        aspect_ratio="16:9",
    )
    print(f"Image URL: {result.output_url}")
    print(f"Completed in status: {result.status}")

asyncio.run(generate())
```

### I2I with reference images

```python
async def transform():
    # Upload local file first
    upload = await muapi_client.upload_file("/path/to/reference.png")

    result = await muapi_client.generate_image(
        endpoint="nano-banana",
        prompt="Transform into oil painting style, rich textures",
        image_urls=[upload.url],
        aspect_ratio="1:1",
    )
    print(f"Result: {result.output_url}")
```

### Multi-image composition

```python
async def multi_ref():
    urls = []
    for path in ["ref1.png", "ref2.png", "ref3.png"]:
        u = await muapi_client.upload_file(path)
        urls.append(u.url)

    result = await muapi_client.generate_image(
        endpoint="nano-banana",
        prompt="Combine elements from all references into a cohesive scene",
        image_urls=urls,
    )
    print(f"Result: {result.output_url}")
```

## Available Models (Representative)

### T2I Models
| Model | Endpoint | Notes |
|---|---|---|
| Nano Banana | `nano-banana` | Multi-image input, fast |
| Flux Dev | `flux-dev` | High quality, balanced |
| Flux Pro 1.1 | `flux-pro-v1.1` | Premium quality |
| Recraft V3 | `recraft-v3` | Versatile style |
| Ideogram V2 | `ideogram-v2` | Strong text rendering |
| Flux Kontext Pro | `flux-kontext-pro` | Context-aware |
| Seedream 3.0 | `seedream-3.0` | Fast, high detail |
| HiDream I1 Full | `hidream-i1-full` | Full resolution |

### I2I Models
| Model | Endpoint | Notes |
|---|---|---|
| Flux Redux Dev | `flux-redux-dev` | Style transfer |
| Flux Depth Pro | `flux-depth-pro` | Depth-aware |
| Flux Canny Pro | `flux-canny-pro` | Edge-guided |

### Listing all models programmatically

```python
from app.services.muapi.models import get_models_by_category, ModelCategory

t2i = get_models_by_category(ModelCategory.T2I)
i2i = get_models_by_category(ModelCategory.I2I)
for m in t2i + i2i:
    print(f"{m.name}: endpoint={m.endpoint}, inputs={m.inputs}")
```

## Error Handling

| Error | Cause | Resolution |
|---|---|---|
| `MuapiError` | API returned non-2xx | Check API key, endpoint validity |
| `MuapiTimeoutError` | Polling exceeded max attempts | Increase `MUAPI_POLL_MAX_ATTEMPTS` or retry |
| `MuapiJobFailedError` | Generation failed server-side | Check prompt content, try different model |

## Integration with Other Skills

- **muapi-cinema**: Apply cinematic prompt modifiers before calling this skill
- **muapi-media-orchestrator**: This skill is invoked as part of the full media pipeline
- **video-script-generator**: Generate image assets for video storyboards
- **content-repurposing-engine**: Create platform-specific image variants

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `MUAPI_API_KEY` | (required) | API key for Muapi.ai gateway |
| `MUAPI_BASE_URL` | `https://api.muapi.ai` | API base URL |
| `MUAPI_POLL_INTERVAL` | `2.0` | Seconds between poll requests |
| `MUAPI_POLL_MAX_ATTEMPTS` | `900` | Max polling attempts before timeout |
| `MUAPI_REQUEST_TIMEOUT` | `30.0` | HTTP request timeout in seconds |
