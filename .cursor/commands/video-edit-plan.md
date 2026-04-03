## Video Editing Planner

Generate post-production editing plans with scene breakdowns, cut lists, transition suggestions, pacing analysis, B-roll placement, audio/SFX notes, and export specifications.

### Usage

```
# From a video script
/video-edit-plan "outputs/video-scripts/ai-agents-youtube.md"

# From raw footage description
/video-edit-plan "20 minutes of interview footage" --target 60s --platform reels

# Multi-platform export plan
/video-edit-plan "script.md" --platforms youtube,shorts
```

### Workflow

1. **Ingest** — Accept video script, footage log, rough cut description, or topic
2. **Scene Breakdown** — Decompose into scenes with footage, B-roll, audio, overlays, transitions, pacing
3. **Cut List** — Generate sequential edit timeline with timecodes
4. **Audio Plan** — Specify music, SFX, voiceover notes per section
5. **Visual Treatment** — Define color grading, graphics, framing, safe zones
6. **Export Specs** — Resolution, FPS, codec, bitrate per target platform

### Output

Complete editing plan document with scene breakdown, cut list, audio plan, visual treatment, export specifications, and revision checklist.

### Execution

Read and follow the `video-editing-planner` skill (`.cursor/skills/standalone/video-editing-planner/SKILL.md`).
