---
name: openmontage
description: >-
  Orchestrate end-to-end video production using OpenMontage -- an agentic
  framework with 11 pipelines, 49 tools, and 400+ agent skills. Covers
  research, scripting, asset generation (video/image/audio/music), Remotion
  composition, FFmpeg rendering, and self-review quality gates. Use when the
  user asks to "produce a video", "create a documentary", "animated
  explainer", "video montage", "openmontage", "agentic video",
  "research-to-video", "video production pipeline", "turn this into a video",
  "create a video from research", "OpenMontage pipeline", "multi-scene video",
  "영상 제작", "비디오 프로덕션", "에이전틱 영상", "다큐멘터리 영상", "애니메이션 설명 영상", or wants to
  orchestrate a full video production workflow from concept to rendered
  output. Do NOT use for single-step video generation via Pika API (use
  pika-text-to-video). Do NOT use for Muapi gateway media pipelines (use
  muapi-media-orchestrator). Do NOT use for Remotion-only motion graphics
  without the full production framework (use remotion-motion-forge). Do NOT
  use for video script writing only (use video-script-generator). Do NOT use
  for post-production editing plans only (use video-editing-planner).
disable-model-invocation: true
---

# OpenMontage -- Agentic Video Production

> World's first open-source agentic video production system.
> Repository: [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage)
> License: AGPL-3.0 | Stars: 1,365+

## What It Does

OpenMontage turns the AI coding assistant into a full video production studio.
The agent orchestrates the entire workflow: research, scripting, asset creation
(video clips, images, voiceover, music, sound effects), Remotion composition,
FFmpeg rendering, and automated quality review.

## Architecture

```
Agent (you)
  |
  +--> Pipeline YAML manifest (defines stages, tools, styles)
  |
  +--> Tools (49 Python modules)
  |      video_gen, image_gen, tts, music_gen, sfx_gen,
  |      enhance, analysis, composition, utility
  |
  +--> Skills (400+ .md files)
  |      pipeline stages, creative techniques, tool usage
  |
  +--> Remotion project (React-based video composition)
  |
  +--> FFmpeg (final render, encoding, post-production)
```

Three-layer knowledge hierarchy:
1. **tools/ + pipeline_defs/** -- executable Python + YAML manifests
2. **skills/** -- agent-facing markdown instructions
3. **.agents/skills/** -- platform-specific agent wrappers

## Prerequisites

```bash
# Clone
git clone https://github.com/calesthio/OpenMontage.git ~/thaki/OpenMontage
cd ~/thaki/OpenMontage

# Python deps
pip install -r requirements.txt

# Node deps (Remotion)
cd remotion && npm install && cd ..

# FFmpeg
brew install ffmpeg   # macOS
# apt install ffmpeg  # Linux

# API keys (.env)
cp .env.example .env
# Fill in provider keys: FAL_KEY, REPLICATE_API_TOKEN, ELEVENLABS_API_KEY, etc.
```

## 11 Production Pipelines

| Pipeline | Description | Key Tools |
|----------|-------------|-----------|
| Animated Explainer | Motion graphics for concepts | image_gen, tts, music_gen |
| Documentary Montage | Fact-based narratives | video_gen, image_gen, tts, sfx_gen |
| Talking Head | Speaker-driven content | video_gen, tts, lipsync |
| Product Showcase | Commercial product videos | image_gen, video_gen, music_gen |
| Tutorial / How-To | Step-by-step instructions | screen_capture, tts, image_gen |
| Social Media Short | Platform-optimized clips | video_gen, image_gen, music_gen |
| Cinematic Story | Narrative film sequences | video_gen, music_gen, sfx_gen |
| Music Video | Audio-synced visuals | video_gen, image_gen, music_gen |
| News Report | Broadcast-style segments | tts, image_gen, video_gen |
| Presentation Video | Slide-to-video conversion | image_gen, tts, music_gen |
| Highlight Reel | Compilation/montage | video_gen, enhance, music_gen |

## Workflow Steps

### Phase 1: Research & Script
1. Read the pipeline YAML manifest to understand required stages
2. Research the topic (web search, document analysis)
3. Write the script with scene breakdowns, shot descriptions, timing

### Phase 2: Asset Generation
4. Generate video clips via configured providers (Kling, Minimax, Runway, Pika, LumaAI)
5. Generate images (Flux, SDXL, Ideogram, Recraft)
6. Generate voiceover via TTS (ElevenLabs, Kokoro, OpenAI, Google)
7. Generate music (Suno, Udio, MusicGen) and sound effects (ElevenLabs SFX)
8. Enhance assets (upscale, extend, interpolate frames)

### Phase 3: Composition & Render
9. Build Remotion composition (React components, timeline, transitions)
10. Run pre-compose validation (duration sync, asset integrity, audio levels)
11. Render via Remotion CLI or FFmpeg

### Phase 4: Review & Delivery
12. Self-review: watch rendered output, score against quality rubric
13. Human approval gate (present for review)
14. Final adjustments and delivery

## Provider System

OpenMontage uses a scored provider selection system. Each provider has
capability scores per task type. The agent selects the best provider based on
quality requirements and budget constraints.

### Video Providers
- **Kling** (v2.0/v1.6) -- high quality, slow
- **Minimax** (video-01-live2d) -- fast, good for animation
- **Runway** (Gen-3 Alpha) -- cinematic quality
- **Pika** (v2.2) -- fast iterations
- **LumaAI** (Dream Machine) -- creative styles
- **Veo** (Google) -- high fidelity
- **Wan** (open-source) -- budget-friendly

### Image Providers
- **Flux** (Pro/Dev/Schnell) -- versatile, fast
- **SDXL** -- open-source, customizable
- **Ideogram** -- text rendering
- **Recraft** (v3) -- design-oriented
- **GPT-Image** (gpt-image-1) -- instruction-following

### Audio Providers
- **ElevenLabs** -- premium TTS + SFX
- **Kokoro** -- open-source TTS
- **OpenAI TTS** -- reliable baseline
- **Suno** -- music generation
- **Udio** -- music generation

## Style System

Styles are defined per pipeline and control visual/audio aesthetics:
- Color grading profiles
- Typography and text overlay rules
- Transition types and timing
- Audio mixing levels
- Aspect ratio and resolution presets

## Production Governance

- **Pre-compose validation**: verify all assets exist, durations match, audio levels are within range
- **Post-render self-review**: agent watches output and scores against rubric
- **Decision audit trail**: all provider choices, parameters, and scores are logged
- **Budget controls**: per-pipeline and per-asset cost tracking
- **Quality gates**: minimum scores required before proceeding to next phase

## Tool Categories

| Category | Count | Examples |
|----------|-------|---------|
| Video Generation | 8 | kling_gen, minimax_gen, runway_gen |
| Image Generation | 7 | flux_gen, sdxl_gen, ideogram_gen |
| TTS / Voice | 5 | elevenlabs_tts, kokoro_tts, openai_tts |
| Music Generation | 3 | suno_gen, udio_gen, musicgen |
| Sound Effects | 2 | elevenlabs_sfx, freesound |
| Enhancement | 6 | upscale, extend, interpolate, denoise |
| Analysis | 4 | scene_detect, audio_analyze, quality_score |
| Composition | 5 | remotion_compose, ffmpeg_concat, overlay |
| Utility | 9 | download, convert, trim, merge, metadata |

## Key Commands

```bash
# List available pipelines
ls pipeline_defs/

# Run a pipeline
python run_pipeline.py --pipeline animated_explainer --topic "Your Topic"

# Render with Remotion
cd remotion && npx remotion render src/index.ts Main out/video.mp4

# FFmpeg post-production
ffmpeg -i input.mp4 -vf "scale=1920:1080" -c:v libx264 -crf 18 output.mp4
```

## Integration with Existing Skills

OpenMontage complements but does NOT replace:
- `pika-text-to-video` -- OpenMontage can USE Pika as one of its video providers
- `remotion-motion-forge` -- OpenMontage uses Remotion internally for composition
- `video-script-generator` -- OpenMontage includes its own scripting stage
- `muapi-media-orchestrator` -- different API gateway, non-overlapping providers
- `video-editing-planner` -- OpenMontage has built-in editing via FFmpeg

## References

- [Full README](references/README.md) -- comprehensive documentation
- [File Structure](references/file_structure.md) -- complete repository layout
- [Known Issues](references/issues.md) -- open GitHub issues
