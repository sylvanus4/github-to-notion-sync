---
name: muapi-cinema
description: >-
  Add professional cinema-grade camera, lens, and aperture modifiers to AI video
  generation prompts via the Muapi.ai gateway. Supports 10 camera movements (static,
  pan, tilt, dolly, zoom, crane, tracking, handheld, orbit, aerial), 8 lens types
  (wide-angle to telephoto), focal length control (14mm-200mm), and 6 aperture modes.
  Constructs cinematically-enriched prompts that feed into T2V/I2V models.
  Use when the user asks to "add camera movement", "cinematic video", "dolly shot",
  "crane shot", "cinema controls", "muapi-cinema", "lens selection", "aperture control",
  "cinematic prompt", "카메라 무빙", "시네마 컨트롤", "영화적 영상", "렌즈 선택",
  "조리개", "시네마틱 프롬프트", or any request to enhance video generation with
  professional camera and lens parameters.
  Do NOT use for basic video generation without cinema controls (use pika-text-to-video).
  Do NOT use for lip sync (use muapi-lipsync).
  Do NOT use for image generation (use muapi-image-studio).
  Do NOT use for video editing/post-production (use video-editing-planner).
---

# Muapi Cinema Studio

Enhance AI video generation with professional cinematography controls -- camera movements, lens types, focal lengths, and aperture effects.

## Prerequisites

| Requirement | Check |
|---|---|
| `MUAPI_API_KEY` in environment | `echo $MUAPI_API_KEY` |
| Python packages: `httpx`, `pydantic` | `pip list \| grep -E 'httpx\|pydantic'` |
| Muapi service module | `python -c "from app.services.muapi import build_cinema_prompt, CinemaSettings"` (from `backend/`) |

## How It Works

The Cinema Studio modifies user prompts by appending professional cinematography descriptors. A base prompt like "a woman walking through a garden" becomes:

> "a woman walking through a garden, tracking shot, anamorphic lens, 35mm focal length, medium depth of field with background separation"

These enriched prompts are then sent to any T2V or I2V model via the Muapi.ai gateway.

## Camera Movements

| Movement | Prompt Modifier | Best For |
|---|---|---|
| `static` | "static shot, locked-off camera" | Stability, dialogue scenes |
| `pan` | "smooth horizontal pan" | Revealing environments |
| `tilt` | "smooth vertical tilt" | Revealing height, buildings |
| `dolly` | "smooth dolly forward movement" | Drawing viewer into scene |
| `zoom` | "smooth zoom" | Focusing attention |
| `crane` | "crane shot, sweeping vertical movement" | Establishing shots, grandeur |
| `tracking` | "tracking shot, following the subject" | Action, walking scenes |
| `handheld` | "handheld camera movement, documentary style" | Realism, urgency |
| `orbit` | "orbit shot, camera circles around the subject" | 3D reveal, product showcase |
| `aerial` | "aerial shot, drone perspective" | Landscapes, establishing context |

## Lens Types

| Lens | Prompt Modifier | Characteristics |
|---|---|---|
| `wide_angle` | "wide-angle lens" | Expansive, spatial distortion |
| `standard` | "standard lens, natural perspective" | Natural look |
| `telephoto` | "telephoto lens, compressed perspective" | Subject isolation |
| `macro` | "macro lens, extreme close-up detail" | Tiny details |
| `fisheye` | "fisheye lens, extreme barrel distortion" | Creative, immersive |
| `anamorphic` | "anamorphic lens" | Cinematic widescreen, lens flares |
| `tilt_shift` | "tilt-shift lens, selective focus" | Miniature effect |
| `prime` | "prime lens, sharp rendering" | Sharpness, low-light |

## Focal Length

Focal length maps to perspective descriptors:

| Range (mm) | Descriptor |
|---|---|
| 14-20 | "ultra wide-angle perspective, dramatic spatial distortion" |
| 21-34 | "wide-angle perspective" |
| 35-59 | "standard field of view, natural perspective" |
| 60-84 | "moderate telephoto, slight compression" |
| 85-134 | "telephoto perspective, compressed depth" |
| 135-200 | "long telephoto, heavily compressed, isolated subject" |

## Aperture Effects

| Setting | Descriptor |
|---|---|
| `wide_open` | "extremely shallow depth of field, creamy bokeh, f/1.4" |
| `shallow` | "shallow depth of field with bokeh, f/2.8" |
| `moderate` | "moderate depth of field, f/5.6" |
| `deep` | "deep depth of field, most elements in focus, f/11" |
| `maximum` | "maximum depth of field, everything sharp, f/16" |
| `cinematic` | "medium depth of field with background separation" |

## Usage

### Basic cinematic video

```python
from app.services.muapi import muapi_client, build_cinema_prompt, CinemaSettings

settings = CinemaSettings(
    camera="tracking",
    lens="anamorphic",
    focal_length=35,
    aperture="cinematic",
)

enriched = build_cinema_prompt("a samurai walking through autumn leaves", settings)
# → "a samurai walking through autumn leaves, tracking shot, following the subject,
#    anamorphic lens, 35mm focal length, standard field of view, natural perspective,
#    medium depth of field with background separation"

result = await muapi_client.generate_video(
    endpoint="wan-t2v",
    prompt=enriched,
    resolution="720p",
)
```

### Aerial establishing shot

```python
settings = CinemaSettings(
    camera="aerial",
    lens="wide_angle",
    focal_length=16,
    aperture="deep",
)

enriched = build_cinema_prompt("a coastal city at sunset", settings)
result = await muapi_client.generate_video(
    endpoint="wan-i2v-720p",
    prompt=enriched,
    image_url=city_photo_url,
)
```

### Product showcase orbit

```python
settings = CinemaSettings(
    camera="orbit",
    lens="prime",
    focal_length=50,
    aperture="shallow",
)

enriched = build_cinema_prompt("a luxury watch on a marble surface", settings)
result = await muapi_client.generate_video(
    endpoint="wan-t2v",
    prompt=enriched,
)
```

## Combination Recipes

| Use Case | Camera | Lens | Focal | Aperture |
|---|---|---|---|---|
| Interview / talking head | static | prime | 85 | shallow |
| Product reveal | orbit | macro | 100 | wide_open |
| Establishing shot | crane | wide_angle | 24 | deep |
| Action chase | tracking | standard | 35 | moderate |
| Dream sequence | dolly | anamorphic | 50 | cinematic |
| Documentary | handheld | standard | 35 | moderate |
| Landscape | aerial | wide_angle | 16 | maximum |
| Portrait film | static | telephoto | 135 | wide_open |

## Error Handling

| Error | Cause | Resolution |
|---|---|---|
| Invalid camera value | Unsupported camera movement | Use one of the 10 supported movements |
| Invalid lens value | Unsupported lens type | Use one of the 8 supported lens types |
| Focal length out of range | Value outside 14-200mm | Adjust to supported range |
| Invalid aperture | Unsupported aperture setting | Use one of the 6 aperture modes |

## Prompt Library Integration

When enriching prompts with camera/lens modifiers, `seedance-video-prompts`
provides pre-tested base prompts optimized for Seedance 2.0. The workflow:

1. Select a base prompt from seedance-video-prompts (search or random)
2. Apply camera movement, lens type, and aperture modifiers from this skill
3. Pass the enriched prompt to the T2V model

```bash
# Get a cinematic base prompt
uv run .cursor/skills/standalone/seedance-video-prompts/scripts/prompt_library.py random --category cinematic

# Then enrich with cinema settings
# base_prompt + ", tracking shot, anamorphic lens, 35mm, cinematic depth of field"
```

## Integration with Other Skills

- **muapi-image-studio**: Generate the source image, then apply cinema controls for I2V
- **muapi-lipsync**: Generate talking-head video first, then apply cinema-grade re-generation
- **muapi-media-orchestrator**: Use cinema as part of an end-to-end media pipeline
- **video-script-generator**: Write the script, then apply cinema settings per scene
- **presentation-strategist**: Plan visual direction, then execute with cinema controls
- **pika-text-to-video**: Alternative video backend; cinema prompts are model-agnostic text
- **seedance-video-prompts**: 605+ curated base prompts for cinema enrichment

## Environment Variables

Same as muapi-image-studio (shared Muapi service configuration).
