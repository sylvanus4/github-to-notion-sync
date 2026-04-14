# BananaX 7-Part Prompt Structure Guide

Reference for constructing and converting BananaX-format structured prompts
for the Nano Banana `gemini-3.1-flash-image-preview` model.

## 7-Part YAML Structure

BananaX prompts use a structured JSON/YAML schema with these fields:

| # | Field | Type | Purpose |
|---|-------|------|---------|
| 1 | `tone` | string | Emotional atmosphere (e.g. "playful", "dramatic", "serene") |
| 2 | `visual_identity` | string | Core scene description — subject, setting, lighting |
| 3 | `image_style` | object/string | Rendering style, camera settings, specific techniques |
| 4 | `typography` | string | Text overlay guidance (font family, placement, styling) |
| 5 | `content_connection` | string | Narrative intent — what meaning the image should convey |
| 6 | `constraints` | list[string] | Hard rules — things to avoid or enforce |
| 7 | `self_check` | string | Verification question for output quality (not sent to model) |

### `image_style` Sub-fields

When `image_style` is an object:

```yaml
image_style:
  main_style: "cinematic photography"
  specific_styles:
    - "golden hour lighting"
    - "bokeh effect"
    - "shallow depth of field"
  camera_settings:
    camera_type: "mirrorless"
    lens: "85mm f/1.4"
    lighting: "natural window light"
```

## Conversion Rules — Structured → Natural Language

The `prompt_library.py` CLI converts structured prompts to natural language
for the Nano Banana model using these rules:

1. **tone** → `Create an image with a {tone} tone.`
2. **visual_identity** → Sentence as-is (capitalize if needed)
3. **image_style.main_style** → `Style: {main_style}.`
4. **image_style.specific_styles** → Comma-joined list appended to style
5. **image_style.camera_settings** → `Camera: {key}: {value}, ...`
6. **typography** → `Typography: {value}.`
7. **content_connection** → Sentence as-is
8. **constraints** → `Constraints: {item1}; {item2}; ...`
9. **self_check** → Omitted (internal QA only, not sent to model)

### Example Conversion

**Structured:**

```json
{
  "tone": "playful",
  "visual_identity": "a young woman on a train, looking out the window",
  "image_style": {
    "main_style": "cinematic photography",
    "specific_styles": ["golden hour lighting", "bokeh effect"],
    "camera_settings": {"lens": "85mm f/1.4", "lighting": "natural window light"}
  },
  "constraints": ["no explicit branding", "focus on the woman"]
}
```

**Natural language output:**

> Create an image with a playful tone. A young woman on a train, looking out
> the window. Style: cinematic photography. golden hour lighting, bokeh effect.
> Camera: lens: 85mm f/1.4, lighting: natural window light. Constraints: no
> explicit branding; focus on the woman.

## Prompt Types in the Library

The 7,600+ prompts in `data/prompts.json` have two formats:

| Type | `prompt` field | Proportion |
|------|---------------|------------|
| Plain text | `string` — ready-to-use natural language | ~85% |
| Structured BananaX | `object` — 7-part JSON requiring conversion | ~15% |

The `prompt_library.py` CLI handles both types transparently. The `show`
and `generate` subcommands auto-detect the format and convert as needed.

## 4-Tier Taxonomy

Prompts are classified by keyword matching into:

| Tier | Subcategories | Focus |
|------|--------------|-------|
| `photography` | portrait, landscape, product, food, architecture, animal, cinematic, fashion, street, macro | Camera-oriented realism |
| `design` | logo, poster, packaging, typography, infographic, mockup | Graphic design artifacts |
| `creative` | 3d_render, illustration, anime, abstract, character, vintage, pixel_art, fantasy, sci_fi | Artistic expression |
| `ui_ux` | app_ui, dashboard, web_ui, ux_flow | Interface mockups |

Classification is rule-based (no LLM) using title, tags, category, and style
fields. See `fetch_prompts.py` for the full keyword mapping.

## Style Selection Guide

When choosing prompts for specific goals:

| Goal | Recommended Tier/Sub | Model Hint |
|------|---------------------|------------|
| Product photography | photography/product | Use `--resolution 2K` or `4K` |
| Social media graphics | design/poster | Add brand colors to prompt |
| App mockups | ui_ux/app_ui | Specify device frame in prompt |
| Artistic exploration | creative/* | Experiment with `random --tier creative` |
| Food content | photography/food | Natural lighting keywords improve results |
| Character design | creative/character | Include pose and expression details |

## Tips for Nano Banana Model

- Keep prompts under 300 words for best results
- The model excels at photorealistic styles — structured prompts with
  camera settings produce the strongest outputs
- For edit mode (`--input-image`), use short imperative instructions
- Resolution `1K` is the sweet spot for speed vs. quality; use `2K`/`4K`
  for print-quality output
