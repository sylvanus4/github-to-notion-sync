---
name: nano-banana
description: >-
  Generate and edit images via Google GenAI (gemini-3.1-flash-image-preview)
  with a built-in prompt library of 7,600+ curated prompts classified into
  4 tiers. Runs locally with uv — zero gateway, zero Muapi dependency.
author: LichAmnesia (adapted for Cursor by ThakiCloud)
version: 2.0.0
category: standalone
---

# Nano Banana — Direct Google GenAI Image Generation + Prompt Library

Generate or edit images using Google's `gemini-3.1-flash-image-preview` model
through a local Python script executed via `uv run`. Includes a curated
library of 7,600+ prompts from the BananaX ecosystem, classified into a
4-tier taxonomy (photography / design / creative / ui_ux) with search,
browse, random, and one-click generation.

## When to Use

Use when the user asks to:

- "generate an image with nano banana"
- "nano-banana로 이미지 만들어줘"
- "direct gemini image generation"
- "edit this image with nano banana"
- "nano banana 2"
- "gemini flash image"
- "nano-banana"
- "나노 바나나"
- "Google GenAI 이미지 생성"
- "gemini-3.1-flash-image-preview"
- "browse nano banana prompts"
- "나노 바나나 프롬프트 검색"
- "search prompt library"
- "random prompt from library"
- "generate image from prompt ID"
- "프롬프트 라이브러리"
- "nano banana library stats"

## When NOT to Use

- For Muapi.ai gateway T2I/I2V (100+ models, multi-reference) → use `muapi-image-studio`
- For Pika video generation → use `pika-text-to-video`
- For static design/poster without AI generation → use `anthropic-canvas-design`
- For cinema-grade video prompts → use `muapi-cinema`

## Key Differentiator

`muapi-image-studio` routes through the Muapi.ai gateway and supports 100+
models including Nano Banana as one option among many. **This skill** calls
the Google GenAI API directly — simpler setup, lower latency for
Nano Banana–specific work, and full control over resolution and edit mode.
Additionally, this skill includes a **7,600+ prompt library** with taxonomy
browsing, search, and one-click generation — no other image skill has this.

## Prerequisites

- `uv` installed (`brew install uv` or `pip install uv`)
- `GEMINI_API_KEY` set in `.env` (already configured in this project)

## Capabilities

| Mode | Description |
|------|-------------|
| **Text-to-Image** | Generate images from text prompts |
| **Image Editing** | Edit existing images with text instructions |
| **Resolution Control** | 512, 1K (default), 2K, 4K |
| **Auto-Resolution** | Detects optimal output size from input image dimensions |
| **Prompt Library** | Browse, search, and generate from 7,600+ curated prompts |

## Usage — Image Generation

### Text-to-Image

```bash
cd /Users/hanhyojung/thaki/ai-model-event-stock-analytics
uv run .cursor/skills/standalone/nano-banana/scripts/generate_image.py \
  --prompt "A serene mountain lake at sunrise, photorealistic" \
  --filename "mountain_lake.png" \
  --resolution 2K
```

### Image Editing

```bash
uv run .cursor/skills/standalone/nano-banana/scripts/generate_image.py \
  --prompt "Add a rainbow across the sky" \
  --filename "edited.png" \
  --input-image "original.png"
```

### With Output Directory

```bash
uv run .cursor/skills/standalone/nano-banana/scripts/generate_image.py \
  --prompt "Corporate logo, minimalist" \
  --filename "logo.png" \
  --output-dir outputs/images/
```

## Usage — Prompt Library

### Search Prompts

```bash
uv run .cursor/skills/standalone/nano-banana/scripts/prompt_library.py \
  search "sunset landscape" --limit 5 --verbose
```

### Browse by Taxonomy

```bash
uv run .cursor/skills/standalone/nano-banana/scripts/prompt_library.py browse
uv run .cursor/skills/standalone/nano-banana/scripts/prompt_library.py browse photography
uv run .cursor/skills/standalone/nano-banana/scripts/prompt_library.py browse photography/portrait --limit 5
```

### Random Prompt

```bash
uv run .cursor/skills/standalone/nano-banana/scripts/prompt_library.py random --tier creative --count 3
```

### Show Prompt Details

```bash
uv run .cursor/skills/standalone/nano-banana/scripts/prompt_library.py show --id 12445
```

### Generate from Library Prompt

```bash
uv run .cursor/skills/standalone/nano-banana/scripts/prompt_library.py \
  generate --id 12445 --resolution 2K --output-dir outputs/images/
```

### Library Statistics

```bash
uv run .cursor/skills/standalone/nano-banana/scripts/prompt_library.py stats
```

## CLI Arguments — generate_image.py

| Flag | Short | Required | Description |
|------|-------|----------|-------------|
| `--prompt` | `-p` | Yes | Image description or edit instruction |
| `--filename` | `-f` | Yes | Output filename (PNG) |
| `--input-image` | `-i` | No | Source image for edit mode |
| `--resolution` | `-r` | No | `512` / `1K` / `2K` / `4K` (default: `1K`) |
| `--output-dir` | `-o` | No | Output directory (default: cwd) |
| `--api-key` | `-k` | No | Override env key |
| `--model` | `-m` | No | Model name override |

## CLI Arguments — prompt_library.py

| Subcommand | Key Flags | Description |
|------------|-----------|-------------|
| `search <query>` | `--limit`, `--verbose` | Keyword search across titles, tags, categories |
| `browse [path]` | `--limit`, `--verbose` | Navigate the 4-tier taxonomy |
| `random` | `--tier`, `--count` | Get random prompts, optionally filtered by tier |
| `stats` | — | Library-wide statistics |
| `show` | `--id` | Detailed view of a single prompt |
| `generate` | `--id`, `--resolution`, `--output-dir`, `--api-key` | Generate image from a library prompt |

## API Key Resolution Order

1. `--api-key` CLI flag
2. `GEMINI_API_KEY` environment variable
3. `GOOGLE_API_KEY` environment variable

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Missing API key or input image load failure |
| 2 | API call failure |
| 3 | No image in response |

## Prompt Library — 4-Tier Taxonomy

| Tier | Subcategories | Focus |
|------|--------------|-------|
| `photography` | portrait, landscape, product, food, architecture, animal, cinematic, fashion, street, macro | Camera-oriented realism |
| `design` | logo, poster, packaging, typography, infographic, mockup | Graphic design artifacts |
| `creative` | 3d_render, illustration, anime, abstract, character, vintage, pixel_art, fantasy, sci_fi | Artistic expression |
| `ui_ux` | app_ui, dashboard, web_ui, ux_flow | Interface mockups |

~15% of prompts use the BananaX 7-part structured format (tone, visual identity,
image style, typography, content connection, constraints, self-check) which is
auto-converted to natural language by `prompt_library.py`.
See `references/bananax-guide.md` for the full structure reference.

## Data Refresh

To re-download the latest prompts from the upstream GitHub repository:

```bash
uv run .cursor/skills/standalone/nano-banana/scripts/fetch_prompts.py
```

This overwrites `data/prompts.json` and regenerates `data/taxonomy.json`.

## Agent Execution Pattern

When invoking this skill as an agent:

1. Determine mode: text-to-image, image editing, or prompt library operation
2. For library operations, construct the `uv run prompt_library.py` command
3. For direct generation, construct the `uv run generate_image.py` command
4. Execute via Shell tool
5. Report results to the user

## File Structure

```
.cursor/skills/standalone/nano-banana/
├── SKILL.md                          # This file
├── scripts/
│   ├── generate_image.py             # Core generation script
│   ├── prompt_library.py             # Prompt library CLI
│   └── fetch_prompts.py              # Data fetcher + classifier
├── data/
│   ├── prompts.json                  # 7,600+ curated prompts
│   └── taxonomy.json                 # 4-tier classification index
└── references/
    └── bananax-guide.md              # BananaX 7-part structure reference
```
