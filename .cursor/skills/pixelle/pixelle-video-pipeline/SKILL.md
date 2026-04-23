---
name: pixelle-video-pipeline
description: End-to-end short-form video production pipeline orchestrating Pixelle-Video with 8+ existing skills across 4 phases — scripting, generation, post-production, and distribution. Use when the user asks to "pixelle pipeline", "end-to-end short video", "full video production with pixelle", "숏폼 파이프라인", "Pixelle 전체 파이프라인", "pixelle-video-pipeline", "short-form video pipeline", "produce and distribute video", or wants a complete video workflow from idea to multi-platform distribution. Do NOT use for single-step generation without post-production (use pixelle-generate). Do NOT use for Pika-only video generation (use pika-video-pipeline). Do NOT use for template browsing only (use pixelle-template). Do NOT use for environment setup (use pixelle-setup).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "pipeline"
---

# pixelle-video-pipeline

End-to-end short-form video production pipeline composing Pixelle-Video with existing media skills.

## When to Use

- Produce a polished short-form video from an idea or topic
- Generate video with professional scripting, hooks, subtitles, and compression
- Create multi-platform content from a single video production run
- Run the full workflow: script → generate → post-produce → distribute

## Pipeline Architecture

```
Phase 1: Script & Hook
├── video-script-generator  →  Structured platform-native script
└── hook-generator          →  Attention-grabbing opening line

Phase 2: Generate Video
├── pixelle-template        →  Select frame template by aspect ratio
└── pixelle-generate        →  Core video generation via Pixelle-Video API

Phase 3: Post-Production
├── video-compress          →  Optimize file size for web delivery
└── caption-subtitle-formatter  →  Generate SRT/VTT subtitle files

Phase 4: Distribution
├── content-repurposing-engine  →  Adapt for YouTube, TikTok, LinkedIn, etc.
└── video-editing-planner       →  Post-production editing notes
```

## Prerequisites

Run `pixelle-setup` once before first use. Verify with:

```bash
cd vendor/Pixelle-Video && uv run python -c "from pixelle_video import PixelleVideoCore; print('OK')"
```

## Full Pipeline Execution

### Step 1: Define the Project

Gather inputs before starting:

| Input | Required | Example |
|-------|----------|---------|
| Topic or script | Yes | "Why AI agents are the future of software development" |
| Target platform | Yes | YouTube Shorts, TikTok, Instagram Reels, LinkedIn |
| Aspect ratio | Yes | Portrait (9:16), Landscape (16:9), Square (1:1) |
| Language | Yes | English, Korean, Japanese, Chinese |
| Tone | No | Professional, casual, educational, inspirational |
| Brand overrides | No | `template_params` for author/brand/colors |

### Step 2: Phase 1 — Script & Hook

Use `video-script-generator` to create a structured script, then `hook-generator` for the opening.

**Script generation:**
- For YouTube Shorts/TikTok: 30-60 second script, 3-5 scenes
- For Instagram Reels: 15-30 seconds, 2-4 scenes
- For educational content: 60-90 seconds, 5-8 scenes

**Hook generation:**
- Request hooks matching the target platform
- Select the highest-impact hook for the opening scene

**Output:** A structured script with hook + narration lines ready for Pixelle-Video's `fixed` mode.

### Step 3: Phase 2 — Generate Video

#### Template Selection (via pixelle-template)

| Platform | Aspect | Recommended Templates |
|----------|--------|----------------------|
| YouTube Shorts / TikTok / Reels | 9:16 | `1080x1920/static_default.html` (no ComfyUI) or `1080x1920/image_default.html` |
| YouTube standard | 16:9 | `1920x1080/image_film.html` or `1920x1080/image_full.html` |
| Instagram / LinkedIn | 1:1 | `1080x1080/image_minimal_framed.html` |

#### Video Generation (via pixelle-generate)

Feed the Phase 1 script into Pixelle-Video:

```python
import asyncio
from pixelle_video import PixelleVideoCore

async def generate():
    core = PixelleVideoCore()
    await core.initialize()

    script = """Your hook line goes here as scene 1.
Scene 2 narration from the script.
Scene 3 narration continues.
Closing scene with call to action."""

    await core.generate_video(
        text=script,
        pipeline="standard",
        mode="fixed",
        split_mode="paragraph",
        frame_template="1080x1920/static_default.html",
        tts_voice="en-US-AriaNeural",
        tts_speed=1.2,
        bgm_volume=0.15,
        template_params={
            "author": "ThakiCloud",
            "brand": "AI Platform",
        },
    )

asyncio.run(generate())
```

**Output:** Raw video at `vendor/Pixelle-Video/output/<timestamp>/final_video.mp4`

### Step 4: Phase 3 — Post-Production

#### Video Compression (via video-compress)

Compress the raw output for web delivery:

```bash
# Locate the latest output
VIDEO=$(ls -td vendor/Pixelle-Video/output/*/final_video.mp4 | head -1)

# Compress with video-compress skill guidance
ffmpeg -i "$VIDEO" -c:v libx264 -crf 23 -preset medium \
  -c:a aac -b:a 128k -movflags +faststart \
  "outputs/pixelle-video/$(date +%Y-%m-%d)/compressed.mp4"
```

Target sizes by platform:

| Platform | Max Size | Resolution |
|----------|----------|------------|
| YouTube Shorts | 60 MB | 1080x1920 |
| TikTok | 287 MB | 1080x1920 |
| Instagram Reels | 250 MB | 1080x1920 |
| LinkedIn | 200 MB | 1080x1080 or 1920x1080 |

#### Subtitle Generation (via caption-subtitle-formatter)

Extract narration text from the script and generate SRT/VTT files:

1. Collect narration text per scene with timing from the generated audio durations
2. Format as SRT with reading-speed validation (CPS limits)
3. Output `.srt` alongside the compressed video

### Step 5: Phase 4 — Distribution

#### Content Repurposing (via content-repurposing-engine)

Transform the video script into platform-native text posts:

- Twitter/X thread summarizing key points
- LinkedIn post with professional framing
- Blog post summary with embedded video
- Newsletter snippet

#### Editing Plan (via video-editing-planner)

Generate a post-production plan for further refinement:

- Scene-by-scene cut list with timing
- B-roll placement suggestions
- Transition recommendations
- Color grading direction
- Export specifications per platform

## Quick-Start: Minimal Pipeline

For the fastest path from idea to video (text-only, no ComfyUI):

```bash
cd vendor/Pixelle-Video
uv run python -c "
import asyncio
from pixelle_video import PixelleVideoCore

async def quick_pipeline():
    core = PixelleVideoCore()
    await core.initialize()
    await core.generate_video(
        text='Why AI agents are the future of software development',
        pipeline='standard',
        mode='generate',
        n_scenes=4,
        frame_template='1080x1920/static_default.html',
        tts_voice='en-US-AriaNeural',
        tts_speed=1.2,
        bgm_volume=0.15,
    )
    print('Video generated! Check vendor/Pixelle-Video/output/')

asyncio.run(quick_pipeline())
"
```

Then compress and copy:

```bash
VIDEO=$(ls -td vendor/Pixelle-Video/output/*/final_video.mp4 | head -1)
mkdir -p outputs/pixelle-video/$(date +%Y-%m-%d)
ffmpeg -i "$VIDEO" -c:v libx264 -crf 23 -preset medium \
  -c:a aac -b:a 128k -movflags +faststart \
  "outputs/pixelle-video/$(date +%Y-%m-%d)/final.mp4"
```

## Output Structure

```
outputs/pixelle-video/{date}/
├── final.mp4                  # Compressed video
├── final.srt                  # Subtitles (SRT)
├── final.vtt                  # Subtitles (VTT)
├── script.md                  # Generated script
├── hook.md                    # Selected hook
├── editing-plan.md            # Post-production notes
├── repurposed/                # Multi-platform content
│   ├── twitter-thread.md
│   ├── linkedin-post.md
│   └── blog-summary.md
└── raw/                       # Original Pixelle-Video output
    └── final_video.mp4
```

## Skill Composition Map

| Phase | Skill | Role | Required |
|-------|-------|------|----------|
| 1 | `video-script-generator` | Platform-native script with timing | Yes |
| 1 | `hook-generator` | Attention-grabbing opening | Yes |
| 2 | `pixelle-template` | Template selection guidance | Yes |
| 2 | `pixelle-generate` | Core video generation | Yes |
| 3 | `video-compress` | File size optimization | Yes |
| 3 | `caption-subtitle-formatter` | SRT/VTT subtitle files | Recommended |
| 4 | `content-repurposing-engine` | Multi-platform text content | Optional |
| 4 | `video-editing-planner` | Post-production editing notes | Optional |

## Platform-Specific Presets

### YouTube Shorts

```python
{
    "n_scenes": 4,
    "frame_template": "1080x1920/static_default.html",
    "tts_speed": 1.3,
    "bgm_volume": 0.1,
    "max_narration_words": 15,
}
```

### TikTok

```python
{
    "n_scenes": 5,
    "frame_template": "1080x1920/image_modern.html",
    "tts_speed": 1.2,
    "bgm_volume": 0.2,
    "max_narration_words": 20,
}
```

### LinkedIn Professional

```python
{
    "n_scenes": 6,
    "frame_template": "1080x1080/image_minimal_framed.html",
    "tts_speed": 1.0,
    "bgm_volume": 0.1,
    "max_narration_words": 25,
}
```

## Language-to-Voice Mapping

Select TTS voice based on target language:

| Language | Edge-TTS Voice | Notes |
|----------|---------------|-------|
| English | `en-US-AriaNeural` (F) / `en-US-GuyNeural` (M) | Default for English content |
| Korean | `ko-KR-SunHiNeural` (F) / `ko-KR-InJoonNeural` (M) | Use for Korean-language scripts |
| Japanese | `ja-JP-NanamiNeural` (F) / `ja-JP-KeitaNeural` (M) | |
| Chinese | `zh-CN-XiaoxiaoNeural` (F) / `zh-CN-YunxiNeural` (M) | Mandarin |
| Spanish | `es-ES-ElviraNeural` (F) / `es-ES-AlvaroNeural` (M) | |

Pass the selected voice as `tts_voice` parameter to `pixelle-generate`.

## Constraints

- **Freedom level:** MEDIUM — follow the 4-phase structure; skip individual phases only when the user explicitly requests it
- **ComfyUI dependency:** Phase 2 with `image_*` or `video_*` templates requires a running ComfyUI instance; fall back to `static_*` templates if unavailable
- **LLM dependency:** Phase 1 script generation and Phase 2 AI content require a configured LLM (Ollama or OpenAI-compatible)
- **Max duration:** Single pipeline run should target 30–90 second output videos; longer formats need manual segment planning

## Output Format

Each pipeline run produces a structured output directory:

```
outputs/pixelle-video/{YYYY-MM-DD}/{slug}/
├── manifest.json          # Pipeline metadata, phases completed, parameters used
├── phase1-script.md       # Generated script and hook
├── phase2-video.mp4       # Raw Pixelle-Video output
├── phase3-compressed.mp4  # Compressed final video
├── phase3-subtitles.srt   # Generated subtitle file
└── phase4-repurpose.md    # Multi-platform content variants
```

## Coordinator Synthesis

This skill is the **single orchestrator** for Pixelle-Video production. It:

1. **Does not duplicate** sub-skill logic — delegates script generation to `video-script-generator`, compression to `video-compress`, etc.
2. **Adds value** by sequencing phases with dependency awareness (Phase 2 needs Phase 1 output) and passing intermediate artifacts between skills
3. **Merges outputs** from parallel sub-skills (e.g., hook + script in Phase 1) into a unified context for downstream phases
4. **Reports the pipeline manifest** — every run produces `manifest.json` with timing, parameters, and phase completion status

## Subagent Contract

When delegating to sub-skills via subagents:

| Phase | Skill Delegated | Input Contract | Expected Output | Blocking? |
|-------|----------------|----------------|-----------------|-----------|
| 1a | `video-script-generator` | Topic string + platform + duration target | `{dir}/phase1-script.md` | **BLOCKING** — Phase 2 cannot start without script |
| 1b | `hook-generator` | Topic + script summary + platform | `{dir}/phase1-hook.md` | Non-blocking — pipeline continues with script-only if hook fails |
| 2 | `pixelle-generate` | `{dir}/phase1-script.md` + template + voice + visual params | `{dir}/phase2-raw.mp4` | **BLOCKING** — Phase 3 cannot start without video |
| 3a | `video-compress` | `{dir}/phase2-raw.mp4` + target size | `{dir}/phase3-compressed.mp4` | **BLOCKING** — final deliverable requires compression |
| 3b | `caption-subtitle-formatter` | Script text from `{dir}/phase1-script.md` + audio timing | `{dir}/phase3-subtitles.srt` | Non-blocking — video is usable without subtitles |
| 4a | `content-repurposing-engine` | Script from `{dir}/phase1-script.md` + platform list | `{dir}/repurposed/*.md` | Non-blocking — entire Phase 4 is optional |
| 4b | `video-editing-planner` | Video metadata + target platforms | `{dir}/phase4-edit-plan.md` | Non-blocking — entire Phase 4 is optional |

Where `{dir}` = `outputs/pixelle-video/{YYYY-MM-DD}/{slug}/`

**Failure handling rules:**
- If a **BLOCKING** subagent fails → abort the pipeline, log the error in `manifest.json`, report the failing phase
- If a **non-blocking** subagent fails → log the error, set the phase status to `PARTIAL`, continue with remaining phases
- Each subagent must return its output file path. Verify file exists and size > 0 before passing to the next phase.

## Honest Reporting

- Report each phase outcome faithfully — if Phase 2 video generation fails due to LLM timeout, say so; do not fabricate a success
- Include actual file sizes, durations, and compression ratios in the final summary
- If a phase is skipped (user request or missing prerequisite), explicitly note it as `SKIPPED` with the reason in `manifest.json`
- Never claim "video ready for upload" unless Phase 3 compression has actually completed

## Verification

Before reporting completion, verify each checkpoint:

1. **Phase 1 complete:** Script markdown exists with scene breaks AND at least 1 hook variant generated
2. **Phase 2 complete:** `.mp4` file exists at the expected output path AND file size > 0
3. **Phase 3 complete:** Compressed `.mp4` exists AND `.srt` file passes format validation
4. **Phase 4 complete:** At least 1 platform variant generated AND `manifest.json` written

Run final check:
```bash
ls -lh outputs/pixelle-video/$(date +%Y-%m-%d)/
cat outputs/pixelle-video/$(date +%Y-%m-%d)/manifest.json | python3 -m json.tool
```

If any checkpoint fails, do NOT mark the pipeline as successful. Report the failing phase and suggest remediation.

## Manifest Schema

The `manifest.json` output file MUST contain these fields:

```json
{
  "pipeline_id": "pixelle-{date}-{slug}",
  "created_at": "2026-04-23T14:30:00Z",
  "topic": "original user topic string",
  "platform": "youtube-shorts | tiktok | reels | generic",
  "phases": {
    "phase1_script": { "status": "COMPLETED | FAILED | SKIPPED", "output": "script.md", "hook": "hook.md" },
    "phase2_generate": { "status": "...", "output": "raw_video.mp4", "template": "1080x1920/static_default.html", "duration_sec": 45 },
    "phase3_post": { "status": "...", "compressed": "video_compressed.mp4", "subtitles": "subtitles.srt", "size_mb": 8.2 },
    "phase4_distribute": { "status": "...", "variants": ["tiktok.md", "reels.md"], "edit_plan": "edit_plan.md" }
  },
  "final_video": "video_compressed.mp4",
  "total_duration_sec": 120,
  "errors": []
}
```

Required fields: `pipeline_id`, `created_at`, `topic`, `platform`, `phases`, `final_video`. Optional: `errors` (array of error strings from any failed phase).

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping Phase 1 script generation | Raw topics produce lower quality; structured scripts are better |
| Using `image_*` template without ComfyUI | Use `static_*` templates for text-only (no ComfyUI needed) |
| Not compressing before upload | Raw output can be 100MB+; always compress in Phase 3 |
| Forgetting subtitles | Most platforms auto-play muted; subtitles are critical for engagement |
| Generating only one platform format | Use Phase 4 repurposing to maximize content ROI |

## Examples

**User:** "AI 에이전트에 대한 숏폼 영상 만들어줘, 유튜브 쇼츠용으로"
→ Full 4-phase pipeline: script via `video-script-generator` (YouTube Shorts, 60s) → hook via `hook-generator` → `pixelle-generate` with `static_default.html` 1080x1920 + Edge-TTS `ko-KR-SunHiNeural` → compress to <25MB → SRT subtitles → repurpose for TikTok/Reels

**User:** "run pixelle pipeline for 'Why Rust is replacing C++' targeting TikTok"
→ Preset: TikTok (1080x1920, 30s, `en-US-GuyNeural`) → Phase 1-4 sequential

**User:** "pixelle pipeline --skip-phase4"
→ Run Phases 1-3 only, skip distribution; output raw compressed video + subtitles
