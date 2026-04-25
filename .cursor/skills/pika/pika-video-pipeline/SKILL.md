---
name: pika-video-pipeline
description: |
  End-to-end video production pipeline: script generation → Pika video creation → post-production planning → optional distribution. Chains video-script-generator (or user-provided script), pika-text-to-video (generation), video-editing-planner (post-production), and optionally video-compress + caption-subtitle-formatter + content-repurposing-engine for distribution. Use when the user asks to "create a video end-to-end", "full video pipeline", "video production pipeline", "produce a video from idea", "script to video", "비디오 파이프라인", "영상 제작 파이프라인", "아이디어에서 영상까지", "스크립트에서 비디오까지", "풀 비디오 제작", "pika-video-pipeline", "영상 기획부터 제작까지", "영상 제작 자동화", or wants a multi-stage video production workflow from concept to deliverable. Do NOT use for single-step video generation without pipeline (use pika-text-to-video). Do NOT use for live video meeting (use pikastream-video-meeting). Do NOT use for NotebookLM video explainers (use nlm-video). Do NOT use for Remotion programmatic motion graphics (use remotion-motion-forge). Do NOT use for video compression only (use video-compress).
metadata:
  author: thakicloud
  version: 0.1.0
  category: pika
  license: Apache-2.0
---

# Pika Video Pipeline

End-to-end pipeline from idea to finished video using Pika v2.2.

## Prerequisites

- All prerequisites from `pika-text-to-video` (Python 3.10+, FAL_KEY)
- No additional script — this is a pure orchestration skill

## Pipeline Phases

```
Phase 1: Script        →  Phase 2: Generation  →  Phase 3: Post-Production  →  Phase 4: Distribution
(video-script-generator)  (pika-text-to-video)    (video-editing-planner)      (optional)
```

### Phase 1 — Script & Storyboard

**Goal**: Produce a structured video script with scenes, timing, and visual direction.

1. **If user provides a topic/idea** (no script):
   - Use `video-script-generator` skill to generate a platform-appropriate script
   - Output: Scene breakdown with prompts, durations, visual cues, and B-roll suggestions

2. **If user provides a script**:
   - Parse the script into individual scenes
   - Extract: prompt text, duration (5s or 10s), visual style notes, aspect ratio preference

3. **If user provides images**:
   - Determine mode: `image-to-video`, `pikascenes`, or `pikaframes` based on quantity and intent
   - Extract scene descriptions from image context or user instructions

**Output**: A scene list — array of objects:
```json
[
  {
    "scene_id": 1,
    "mode": "text-to-video",
    "prompt": "...",
    "duration": 5,
    "resolution": "1080p",
    "aspect_ratio": "16:9",
    "image": null,
    "images": null,
    "effect": null
  }
]
```

Save scene list to `outputs/pika/pipeline-{date}-scenes.json`.

### Phase 2 — Video Generation

**Goal**: Generate video clips for each scene using Pika.

For each scene in the scene list:

```bash
python .cursor/skills/pika/pika-text-to-video/scripts/pika_video_generate.py \
  {mode} \
  --prompt "{prompt}" \
  --resolution {resolution} --duration {duration} --aspect-ratio {aspect_ratio} \
  [--image {image}] [--images {images...}] [--effect {effect}] \
  --output outputs/pika/pipeline-{date}-scene-{scene_id}.mp4
```

**Execution strategy**:
- Run scenes sequentially (fal.ai queue handles parallelism internally)
- Log each result to `outputs/pika/pipeline-{date}-manifest.json`
- On failure: retry once, then skip the scene and log the error

**Checkpoint**: After all scenes complete, present the manifest to the user:
- List of generated clips with file paths
- Any failed scenes
- Total generation cost estimate (~$0.40 × scene count)

Ask: `{N} scenes generated. Proceed to post-production planning, or regenerate any scenes?`

### Phase 3 — Post-Production Plan

**Goal**: Create an editing plan for assembling the clips.

Use `video-editing-planner` skill with the manifest as input:
- Scene order and transitions
- Audio/SFX suggestions
- Color grading direction
- Pacing analysis
- Export specifications

**Optional sub-steps** (if user requests):
- `video-compress` — compress generated clips for target platform
- `caption-subtitle-formatter` — generate subtitles from scene prompts/scripts

Save editing plan to `outputs/pika/pipeline-{date}-edit-plan.md`.

### Phase 4 — Distribution (Optional)

If user requests distribution:
- `content-repurposing-engine` — adapt video description for social platforms
- `hook-generator` — generate attention-grabbing captions
- Upload to Google Drive via `gws-drive` if requested

## Workflow

### Step 1 — Understand intent

Ask if unclear:
- What is the video about? (topic, mood, style)
- Target platform? (YouTube, Shorts, TikTok, Instagram, internal)
- Duration target? (total length, not per-scene)
- Do you have images to include? (determines mode selection)
- Resolution preference? (720p for draft, 1080p for final)

### Step 2 — Execute Phase 1

Generate or parse the script. Present the scene list to the user for approval before proceeding.

### Step 3 — Execute Phase 2

Run Pika generation for each approved scene. Stream progress logs to the user.

### Step 4 — Execute Phase 3

Generate the post-production plan. Present to user.

### Step 5 — Execute Phase 4 (if requested)

Distribute or compress as needed.

## Output Artifacts

| Phase | Stage Name          | Output File                                    |
|-------|---------------------|------------------------------------------------|
| 1     | Script & Storyboard | `outputs/pika/pipeline-{date}-scenes.json`     |
| 2     | Video Generation    | `outputs/pika/pipeline-{date}-scene-{N}.mp4`   |
| 2     | Generation Manifest | `outputs/pika/pipeline-{date}-manifest.json`   |
| 3     | Post-Production     | `outputs/pika/pipeline-{date}-edit-plan.md`     |

```
outputs/pika/
├── pipeline-{date}-scenes.json      # Scene list from Phase 1
├── pipeline-{date}-scene-1.mp4      # Generated clips
├── pipeline-{date}-scene-2.mp4
├── pipeline-{date}-scene-N.mp4
├── pipeline-{date}-manifest.json    # Generation results + metadata
└── pipeline-{date}-edit-plan.md     # Post-production plan
```

## Error Handling

| Phase | Failure | Recovery |
|-------|---------|----------|
| Phase 1 | Script generation fails | Fall back to user-provided bullet points as prompts |
| Phase 2 | Single scene fails | Retry once; skip and log on second failure |
| Phase 2 | FAL_KEY invalid | Stop pipeline, report to user |
| Phase 2 | All scenes fail | Stop pipeline, check API status and key |
| Phase 3 | Editing plan generation fails | Provide raw manifest as fallback |

## Phase 1 Enhancement: Library-Sourced Scenes

When `--from-library` or "use seedance prompts" is requested:
- Replace video-script-generator with seedance-video-prompts selection
- Select N prompts matching the theme (via search or category browse)
- Format each as a scene in the scene list JSON structure

```bash
# Select 5 cinematic prompts as scenes
uv run .cursor/skills/standalone/seedance-video-prompts/scripts/prompt_library.py by-category \
  --category cinematic --limit 5

# Or search for themed prompts
uv run .cursor/skills/standalone/seedance-video-prompts/scripts/prompt_library.py search "nature slow motion" --limit 5
```

Each returned prompt maps to one scene entry:
```json
{
  "scene_id": 1,
  "mode": "text-to-video",
  "prompt": "<prompt text from library>",
  "duration": 5,
  "resolution": "1080p",
  "aspect_ratio": "16:9"
}
```

## Cross-Skill References

| Skill | Role in Pipeline |
|-------|-----------------|
| `video-script-generator` | Phase 1: Script generation |
| `pika-text-to-video` | Phase 2: Video generation (core) |
| `video-editing-planner` | Phase 3: Post-production planning |
| `video-compress` | Phase 3: Optional compression |
| `caption-subtitle-formatter` | Phase 3: Optional subtitles |
| `content-repurposing-engine` | Phase 4: Multi-platform distribution |
| `hook-generator` | Phase 4: Attention-grabbing captions |
| `gws-drive` | Phase 4: Google Drive upload |
| `presentation-strategist` | Pre-Phase 1: Presentation narrative design |
| `seedance-video-prompts` | Phase 1 alt: Library-sourced scene prompts |
