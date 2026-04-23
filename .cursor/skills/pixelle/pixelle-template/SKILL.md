---
name: pixelle-template
description: Browse, preview, and customize Pixelle-Video HTML frame templates by resolution and media type. Use when the user asks to "list pixelle templates", "pixelle template", "browse video templates", "preview template", "create custom template", "영상 템플릿", "Pixelle 템플릿", "custom video frame", "pixelle-template", or needs to select or customize an HTML template for Pixelle-Video generation. Do NOT use for video generation (use pixelle-generate). Do NOT use for environment setup (use pixelle-setup). Do NOT use for the full production pipeline (use pixelle-video-pipeline).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "standalone"
---

# pixelle-template

Browse, preview, and customize Pixelle-Video HTML frame templates.

## When to Use

- Select the right template for a video project
- Preview what a template looks like before generating
- Create a custom template for a specific brand or style
- Understand template variable syntax for `template_params`

## Template Directory

All templates live under `vendor/Pixelle-Video/templates/` organized by resolution.

### Naming Convention

| Prefix | AI Media Required | ComfyUI Needed | Description |
|--------|-------------------|----------------|-------------|
| `static_*` | No | No | Text and narration only |
| `image_*` | AI images per scene | Yes (or RunningHub) | Each scene gets a generated image |
| `video_*` | AI video clips per scene | Yes (or RunningHub) | Each scene gets a generated video clip |
| `asset_*` | User-provided assets | No | Uses pre-made images/videos |

### Full Template Catalog

#### Portrait 9:16 (`1080x1920/`)

| Template | Type | Description |
|----------|------|-------------|
| `static_default.html` | Static | Gradient background with centered text card and quote marks |
| `static_excerpt.html` | Static | Quote/excerpt focused layout |
| `image_default.html` | Image | Standard image + narration layout |
| `image_modern.html` | Image | Modern card-based image layout |
| `image_elegant.html` | Image | Elegant style with refined typography |
| `image_blur_card.html` | Image | Blurred image background with text card overlay |
| `image_book.html` | Image | Book/reading style layout |
| `image_cartoon.html` | Image | Cartoon illustration style |
| `image_excerpt.html` | Image | Image with excerpt/quote emphasis |
| `image_fashion_vintage.html` | Image | Vintage fashion aesthetic |
| `image_full.html` | Image | Full-bleed image with text overlay |
| `image_healing.html` | Image | Soft, calming aesthetic |
| `image_health_preservation.html` | Image | Health/wellness themed |
| `image_life_insights.html` | Image | Life wisdom, dark theme |
| `image_life_insights_light.html` | Image | Life wisdom, light theme |
| `image_long_text.html` | Image | Optimized for longer narrations |
| `image_neon.html` | Image | Neon glow aesthetic |
| `image_psychology_card.html` | Image | Psychology fact card style |
| `image_purple.html` | Image | Purple gradient theme |
| `image_satirical_cartoon.html` | Image | Satirical cartoon illustration |
| `image_simple_black.html` | Image | Minimal black background |
| `image_simple_line_drawing.html` | Image | Line drawing art style |
| `video_default.html` | Video | Standard video clip + narration |
| `video_healing.html` | Video | Calming video clips |
| `asset_default.html` | Asset | Pre-made asset layout |

#### Landscape 16:9 (`1920x1080/`)

| Template | Type | Description |
|----------|------|-------------|
| `image_book.html` | Image | Widescreen book/reading style |
| `image_film.html` | Image | Cinematic film frame aesthetic |
| `image_full.html` | Image | Full-bleed widescreen image |
| `image_ultrawide_minimal.html` | Image | Ultra-minimal widescreen layout |
| `image_wide_darktech.html` | Image | Dark tech/futuristic widescreen |

#### Square 1:1 (`1080x1080/`)

| Template | Type | Description |
|----------|------|-------------|
| `image_minimal_framed.html` | Image | Minimal framed image for Instagram/social |

## Template Variable Syntax

Templates use `{{variable}}` or `{{variable=default_value}}` for dynamic content.

### Standard Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{{title}}` | Video/scene title | Set automatically or via `title` param |
| `{{text}}` | Narration text for the current scene | Set by pipeline per scene |
| `{{author=@Pixelle.AI}}` | Author name (with default) | Override via `template_params` |
| `{{describe=...}}` | Author description | Override via `template_params` |
| `{{brand=Pixelle-Video}}` | Brand name | Override via `template_params` |
| `{{background=url}}` | Background image URL | Override via `template_params` |

### Meta Tags

Templates declare required media dimensions via HTML meta tags:

```html
<meta name="template:media-width" content="1024">
<meta name="template:media-height" content="1024">
```

These tell the image/video generation pipeline what dimensions to produce for AI-generated media assets.

## Previewing Templates

Open any template directly in a browser to see its layout:

```bash
open vendor/Pixelle-Video/templates/1080x1920/static_default.html
```

For a quick visual comparison of multiple templates:

```bash
for t in vendor/Pixelle-Video/templates/1080x1920/static_*.html; do
  echo "--- $(basename $t) ---"
  open "$t"
  sleep 1
done
```

## Selecting a Template for Generation

Pass the template path (relative to `templates/`) to `pixelle-generate`:

```python
await core.generate_video(
    text="Your topic here",
    pipeline="standard",
    frame_template="1080x1920/image_modern.html",  # relative to templates/
)
```

### Selection Guide

| Your Goal | Recommended Template |
|-----------|---------------------|
| Quick text-only video (no ComfyUI) | `1080x1920/static_default.html` |
| Standard portrait with AI images | `1080x1920/image_default.html` |
| Cinematic widescreen | `1920x1080/image_film.html` |
| Instagram/social square | `1080x1080/image_minimal_framed.html` |
| Long narration per scene | `1080x1920/image_long_text.html` |
| Dark tech aesthetic | `1920x1080/image_wide_darktech.html` |
| Calming/healing content | `1080x1920/image_healing.html` |

## Creating a Custom Template

### Step 1: Copy an Existing Template

```bash
cp vendor/Pixelle-Video/templates/1080x1920/static_default.html \
   vendor/Pixelle-Video/templates/1080x1920/static_custom.html
```

### Step 2: Edit HTML/CSS

Key rules for custom templates:

1. **Keep meta tags** — `template:media-width` and `template:media-height` are required for AI media generation
2. **Use `{{text}}`** — The pipeline injects narration text into this variable
3. **Use `{{title}}`** — The pipeline injects the video title
4. **Body width must match resolution** — e.g., `width: 1080px` for portrait templates
5. **Page container height must match** — e.g., `height: 1920px` for portrait
6. **Use `{{variable=default}}` syntax** — For optional variables with fallback values

### Step 3: Customize via `template_params`

Override template defaults at generation time without editing HTML:

```python
await core.generate_video(
    text="Your topic",
    pipeline="standard",
    frame_template="1080x1920/static_default.html",
    template_params={
        "author": "ThakiCloud",
        "brand": "AI Platform",
        "describe": "Next-Gen Cloud AI",
        "background": "https://example.com/your-bg.jpg",
    },
)
```

### Template Anatomy

```
template.html
├── <meta> tags          # media-width, media-height
├── <style>              # All CSS (fonts, colors, layout)
├── .background-image    # Optional background layer
├── .gradient-overlay    # Optional gradient on top of background
├── .page-container      # Main layout container (matches resolution)
│   ├── .video-title     # {{title}} goes here
│   ├── .content         # Main content area
│   │   └── .text        # {{text}} (narration) goes here
│   └── .footer          # Brand, author info
└── Optional: media container for image_*/video_* templates
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `image_*` template without ComfyUI/RunningHub | Switch to `static_*` or set up ComfyUI |
| Wrong resolution directory | Match directory to desired aspect ratio |
| Missing `{{text}}` in custom template | Pipeline needs this to inject narration |
| Forgetting meta tags in custom template | Copy them from an existing template |
| Hardcoding text instead of using `{{variable}}` | Use template variable syntax for dynamic content |

## Examples

**User:** "pixelle 템플릿 목록 보여줘" / "list pixelle templates"
→ Print the Full Template Catalog grouped by resolution

**User:** "which template for a YouTube Short without ComfyUI?"
→ Recommend `1080x1920/static_default.html` (text-only, no AI media needed)

**User:** "create a custom template with our brand colors"
→ Follow "Creating a Custom Template" steps, inject brand via `template_params`
