---
name: seedance-video-prompts
description: >-
  Browse, search, and retrieve 605+ curated Seedance 2.0 video generation
  prompts from OpenNana. Categories: cinematic, ultra-realistic, photography,
  nature, character, fashion, comedy, animation, fantasy-surreal, sports-action,
  narrative, and more. Outputs prompts ready for pika-text-to-video,
  muapi-cinema, pixelle-generate, or any T2V model.
author: OpenNana community (collected by ThakiCloud)
version: 1.0.0
category: standalone
---

# Seedance 2.0 Video Prompt Library

Browse, search, and discover 605+ curated video generation prompts tested
with Seedance 2.0. Each prompt includes English text, optional Chinese
translation, category/tag metadata, and reference video URLs. No generation
capability — purely a prompt discovery and retrieval tool.

## When to Use

Use when the user asks to:

- "seedance prompt", "seedance 2.0 prompt"
- "browse video prompts", "video prompt library"
- "random video prompt", "get a video prompt"
- "search video prompts for cinematic"
- "find a seedance prompt about rain"
- "시던스 프롬프트", "비디오 프롬프트 검색"
- "영상 프롬프트 라이브러리", "랜덤 영상 프롬프트"
- "seedance-video-prompts"
- "T2V prompt inspiration"
- "video generation prompt ideas"

## When NOT to Use

- For AI video generation execution → use `pika-text-to-video` or `pixelle-generate`
- For cinema camera/lens modifiers → use `muapi-cinema`
- For image generation prompts → use `nano-banana`
- For video scripting with scenes/timing → use `video-script-generator`
- For end-to-end video production pipelines → use `pika-video-pipeline` or `muapi-media-orchestrator`

## Prerequisites

- `uv` installed (`brew install uv` or `pip install uv`)
- No API keys required — all data is local

## Prompt Library — 16 Categories

| Category | Count | Focus |
|----------|------:|-------|
| `cinematic` | 141 | Film-quality scenes, camera work, dramatic lighting |
| `fantasy-surreal` | 57 | Surreal concepts, magical scenes, dreamscapes |
| `sports-action` | 42 | Dynamic movement, athletic scenes, extreme sports |
| `photography` | 37 | Photo-realistic styles, lens effects, composition |
| `ultra-realistic` | 35 | Hyper-real human/object detail |
| `fashion` | 30 | Fashion, beauty, styling, runway |
| `character` | 27 | Character-focused scenes, portraits in motion |
| `narrative` | 26 | Story-driven scenes, sequential events |
| `comedy` | 17 | Humorous situations, comedic timing |
| `nature` | 16 | Landscapes, weather, natural phenomena |
| `animation` | 15 | Animated styles, cartoon, stop-motion |
| `architecture-urban` | 15 | City scenes, buildings, urban environments |
| `mood-aesthetic` | 13 | Atmospheric, mood-driven, aesthetic-focused |
| `technology` | 6 | Tech, sci-fi gadgets, digital interfaces |
| `food-product` | 4 | Food photography, product shots |
| `other` | 124 | Uncategorized or cross-category prompts |

## Usage

### Search Prompts

```bash
uv run .cursor/skills/standalone/seedance-video-prompts/scripts/prompt_library.py \
  search "cinematic rain" --limit 5 --verbose
```

### Browse by Category

```bash
uv run .cursor/skills/standalone/seedance-video-prompts/scripts/prompt_library.py browse
uv run .cursor/skills/standalone/seedance-video-prompts/scripts/prompt_library.py browse cinematic --limit 5
uv run .cursor/skills/standalone/seedance-video-prompts/scripts/prompt_library.py browse fantasy-surreal --limit 3 --verbose
```

### Category Distribution

```bash
uv run .cursor/skills/standalone/seedance-video-prompts/scripts/prompt_library.py by-category
```

### Random Prompt

```bash
uv run .cursor/skills/standalone/seedance-video-prompts/scripts/prompt_library.py random --count 3
uv run .cursor/skills/standalone/seedance-video-prompts/scripts/prompt_library.py random --category cinematic --count 2
```

### Show Prompt Details

```bash
uv run .cursor/skills/standalone/seedance-video-prompts/scripts/prompt_library.py show --id 13389
```

### Library Statistics

```bash
uv run .cursor/skills/standalone/seedance-video-prompts/scripts/prompt_library.py stats
```

## CLI Arguments

| Subcommand | Key Flags | Description |
|------------|-----------|-------------|
| `search <query>` | `--limit`, `--verbose` | Keyword search across titles, tags, prompts |
| `browse [category]` | `--limit`, `--verbose` | List categories or browse a specific one |
| `by-category` | — | Bar chart of prompt distribution by category |
| `random` | `--category`, `--count` | Random prompts, optionally filtered by category |
| `stats` | — | Library-wide statistics (authors, languages, videos) |
| `show` | `--id` | Detailed view of a single prompt with video URLs |

## Integration with Video Generation Skills

This skill provides **prompt text** that feeds into video generation skills:

1. **pika-text-to-video** — Use the returned `prompt` field as the `prompt` argument
2. **muapi-cinema** — Use as a base prompt, then apply camera/lens modifiers
3. **pixelle-generate** — Use as the `text` parameter in topic mode
4. **pika-video-pipeline** — Source scene prompts for multi-scene production
5. **muapi-media-orchestrator** — Use as initial text for any pipeline mode
6. **video-script-generator** — Reference for proven scene descriptions

### Workflow Example

```bash
# 1. Find a cinematic prompt
uv run .cursor/skills/standalone/seedance-video-prompts/scripts/prompt_library.py \
  random --category cinematic --count 1

# 2. Copy the prompt text and use it with pika-text-to-video
# (the generation skill handles the actual video creation)
```

## Agent Execution Pattern

When invoking this skill as an agent:

1. Determine the operation: search, browse, random, stats, or show
2. Construct the `uv run prompt_library.py` command with appropriate flags
3. Execute via Shell tool
4. Parse the output and present to the user
5. If the user wants to generate video from a prompt, hand off to the appropriate video generation skill with the prompt text

## Data Source

Prompts collected from [OpenNana Awesome Prompt Gallery](https://opennana.com/awesome-prompt-gallery?media_type=video&model=Seedance%202.0)
on 2026-04-25. Each prompt has been tested with the Seedance 2.0 model.

## File Structure

```
.cursor/skills/standalone/seedance-video-prompts/
├── SKILL.md                          # This file
├── data/
│   ├── prompts.json                  # 605 curated video prompts
│   └── taxonomy.json                 # 16-category classification index
└── scripts/
    └── prompt_library.py             # CLI: search, browse, random, stats
```
