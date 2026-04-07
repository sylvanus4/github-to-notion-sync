---
name: video-editing-planner
description: >-
  Generate post-production editing plans with scene breakdowns, cut lists,
  transition suggestions, pacing analysis, B-roll placement, audio/SFX notes,
  color grading direction, and export specifications. Takes raw footage
  descriptions or video scripts as input and produces editor-ready plans. Use
  when the user asks to "plan video edits", "create an editing plan", "video
  post-production", "cut list", "scene breakdown", "편집 계획", "영상 편집
  플랜", "컷 리스트", "B-roll 배치", "후반 작업 계획", "video editing plan",
  "edit this video", or wants a structured post-production workflow. Do NOT use
  for video compression or encoding (use video-compress). Do NOT use for
  transcription (use transcribee). Do NOT use for script writing (use
  video-script-generator). Do NOT use for subtitle formatting (use
  caption-subtitle-formatter).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "generation"
---

# Video Editing Planner

Create editor-ready post-production plans from raw footage descriptions or video scripts.

## When to Use

- A video has been filmed and needs a structured editing plan before post-production
- A video script needs a corresponding edit plan for the editor
- Raw footage needs to be organized into a coherent sequence
- The user wants to plan transitions, B-roll, audio, and pacing before opening an NLE

## Workflow

### Step 1: Ingest Source

Accept input as:
- **Video script** — Use sections, timing, and visual cues as the edit blueprint
- **Raw footage log** — List of clips with descriptions, durations, and quality notes
- **Rough cut description** — Existing edit that needs refinement
- **Topic + intent** — Generate an edit plan from conceptual direction

### Step 2: Scene Breakdown

Decompose the video into discrete scenes:

```markdown
### Scene [N]: [Scene Title]

| Attribute | Value |
|-----------|-------|
| **Duration** | [estimated seconds] |
| **Primary footage** | [clip reference or description] |
| **B-roll** | [supplementary footage needed] |
| **Audio** | [dialogue / voiceover / music / SFX] |
| **Text overlays** | [any on-screen text, lower thirds, titles] |
| **Transition IN** | [cut / dissolve / wipe / custom] |
| **Transition OUT** | [cut / dissolve / wipe / custom] |
| **Pacing** | [fast / medium / slow] |
| **Notes** | [special instructions for the editor] |
```

### Step 3: Cut List

Generate a sequential cut list:

```markdown
## Cut List

| # | Timecode | Source | Description | Duration | Transition |
|---|----------|--------|-------------|----------|------------|
| 1 | 0:00:00 | A-cam opening | Wide shot, speaker walks in | 3s | Fade from black |
| 2 | 0:00:03 | Title card | Animated title with music sting | 4s | Cut |
| 3 | 0:00:07 | A-cam CU | Speaker delivers hook line | 8s | Cut |
| 4 | 0:00:15 | B-roll | Screen recording of demo | 12s | L-cut (audio continues) |
| ... | ... | ... | ... | ... | ... |
```

### Step 4: Audio Plan

```markdown
## Audio Plan

### Music
| Section | Track/Mood | Volume | Fade |
|---------|-----------|--------|------|
| Intro (0:00-0:30) | Upbeat, tech-forward | 80% under VO | Fade in 2s |
| Main content | Ambient, low-energy | 20% under VO | Crossfade |
| CTA/Outro | Same as intro | 80%, VO ends | Fade out 3s |

### Sound Effects
| Timecode | SFX | Purpose |
|----------|-----|---------|
| 0:00:00 | Whoosh | Title card transition |
| 0:02:15 | Click/tap | UI interaction on screen recording |
| ... | ... | ... |

### Voiceover Notes
- Record in [quiet room / treated booth]
- Pacing: [words per minute target]
- Pick-up lines needed: [list any re-records]
```

### Step 5: Visual Treatment

```markdown
## Visual Treatment

### Color Grading
- **Base LUT**: [warm/cool/neutral/cinematic]
- **Skin tone priority**: [natural / stylized]
- **B-roll treatment**: [match A-cam / desaturated / high-contrast]

### Graphics & Motion
| Element | Spec |
|---------|------|
| Lower thirds | [style, font, animation direction] |
| Chapter titles | [full-screen / corner / animated] |
| Data callouts | [chart style, animation, duration on screen] |
| End screen | [subscribe button, video suggestions, duration] |

### Framing
- **Aspect ratio**: [16:9 / 9:16 / 1:1]
- **Safe zones**: [title-safe area for platform overlays]
- **Reframing notes**: [any crop/zoom adjustments for multi-platform export]
```

### Step 6: Export Specifications

```markdown
## Export Specifications

| Platform | Resolution | FPS | Codec | Bitrate | Format |
|----------|-----------|-----|-------|---------|--------|
| YouTube | 3840×2160 or 1920×1080 | 30 or 60 | H.264/H.265 | 35-45 Mbps | .mp4 |
| Shorts | 1080×1920 | 30 | H.264 | 20 Mbps | .mp4 |
| TikTok | 1080×1920 | 30 | H.264 | 20 Mbps | .mp4 |
| Reels | 1080×1920 | 30 | H.264 | 20 Mbps | .mp4 |
| Podcast clip | 1920×1080 | 30 | H.264 | 15 Mbps | .mp4 |
```

### Step 7: Output

Combine all sections into a single editing plan document:

```markdown
# Video Editing Plan: [Title]

## Overview
- **Final duration target**: [minutes:seconds]
- **Platform**: [primary platform]
- **Style**: [documentary / vlog / explainer / talking head / montage]
- **Editor notes**: [overall creative direction]

## Scene Breakdown
[Step 2 output]

## Cut List
[Step 3 output]

## Audio Plan
[Step 4 output]

## Visual Treatment
[Step 5 output]

## Export Specifications
[Step 6 output]

## Revision Checklist
- [ ] All scenes accounted for
- [ ] Total duration within target ±10%
- [ ] Audio levels specified for all sections
- [ ] B-roll identified for all talking-head sections
- [ ] Export specs match target platform requirements
```

## Examples

### Example 1: YouTube explainer edit plan

User: "Create an editing plan for this 10-minute YouTube script" + [script file]

Parse the script's sections, generate a scene breakdown with B-roll suggestions for each section, create a cut list with J-cuts and L-cuts at section transitions, specify ambient music under voiceover with energy changes at key moments, and include YouTube-optimized export specs.

### Example 2: Short-form from raw footage

User: "I have 20 minutes of interview footage. Plan edits for a 60-second Reels clip."

Identify the 3-4 strongest soundbites, plan jump cuts between them, suggest text overlay placement for key quotes, specify vertical crop framing, and add trending audio placement cues.

### Example 3: Multi-platform export plan

User: "편집 계획 만들어줘 - YouTube 영상이랑 Shorts 버전 둘 다"

Generate two editing plans from the same footage: a full-length YouTube edit and a condensed Shorts vertical edit. Specify different pacing, framing (16:9 vs 9:16), and which sections to include/exclude for each.

## Error Handling

| Scenario | Action |
|----------|--------|
| No script or footage description provided | Ask: "Do you have a script, footage log, or topic to plan edits for?" |
| Footage duration unknown | Estimate based on script word count or ask the user |
| Target platform not specified | Default to YouTube 16:9 and note the assumption |
| No B-roll available | Suggest stock footage sources, screen recordings, or text-overlay alternatives |
| Edit plan exceeds practical complexity for one editor | Flag complex sections and suggest splitting into editing passes |

## Composability

- **reclip-media-downloader** — Download source footage from URLs before planning edits
- **video-script-generator** — Generate the script that this skill turns into an edit plan
- **video-compress** — Compress the final exported video
- **caption-subtitle-formatter** — Generate subtitles for the edited video
- **transcribee** — Transcribe raw footage to identify best soundbites
- **hook-generator** — Generate alternative hooks to test in the edit
