---
name: stitch-remotion
description: >-
  Generate professional walkthrough videos from Stitch projects using Remotion
  with smooth transitions, zoom effects, and text overlays.
---

# Stitch to Remotion Walkthrough Videos

Generate professional walkthrough videos from Stitch projects using Remotion with smooth transitions, zoom effects, and contextual text overlays.

Ported from [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) `remotion`, adapted for Cursor IDE.

## Cursor & Thaki workspace

- **Read** — Screen list from Stitch MCP, `screens.json` / manifests under `.stitch/`, and any existing Remotion project (e.g. `remotion/` in an app or `remotion-motion-forge` output paths).
- **Write** — Generated compositions, `screens.json`, and rendered `output.mp4` under the chosen package (keep large binaries out of unrelated packages).
- **Shell** — `npm run dev` (Remotion Studio), `npx remotion render`, `ffmpeg` post-processing; run from the Remotion package directory.
- **Grep** — Find existing `Composition` / `staticFile` usage to match Thaki’s Remotion style.
- **Task** — Optional: parallel asset download + component codegen for long walkthroughs.

## Triggers

Use when the user asks to "create Stitch walkthrough video", "Stitch 워크스루 영상", "Stitch to video", "Stitch 영상 생성", "stitch-remotion", "Stitch Remotion 비디오", "design walkthrough video", "디자인 워크스루 비디오", "Stitch 프로젝트 영상", or wants to create a video showcasing Stitch-designed screens with professional transitions.

Do NOT use for general Remotion video production without Stitch input (use remotion-motion-forge). Do NOT use for Pika AI video generation (use pika-text-to-video). Do NOT use for video compression only (use video-compress). Do NOT use for video scripts without Stitch screens (use video-script-generator). Do NOT use for design review (use design-qa-checklist).

## Prerequisites

- Stitch MCP server with a project containing designed screens
- Node.js 18+ and npm
- Remotion dependencies (`remotion`, `@remotion/cli`, `@remotion/transitions`)
- ffmpeg for final rendering

## Workflow

### Step 1 — Gather Screen Assets
1. List Stitch project screens via MCP
2. Download screenshots (append `=w{width}` for full resolution)
3. Create `screens.json` manifest with metadata

### Step 2 — Generate Remotion Components
- `ScreenSlide.tsx` — Individual screen display with zoom/fade animations
- `WalkthroughComposition.tsx` — Main composition sequencing all screens
- Configure frame rate (30fps default) and dimensions

### Step 3 — Transitions
Use `@remotion/transitions`: fade, slide, zoom with spring animations.

### Step 4 — Text Overlays
Add screen titles, feature callouts, descriptions, and progress indicators.

### Step 5 — Preview & Render
```bash
npm run dev          # Remotion Studio preview
npx remotion render WalkthroughComposition output.mp4
```

## Video Patterns

| Pattern | Description |
|---------|-------------|
| Simple Slide Show | 3-5s per screen, cross-fade, bottom title overlay |
| Feature Highlight | Zoom into regions, animated arrows, slow-motion emphasis |
| User Flow | Sequential slides, numbered steps, animated paths |

## Integration

- Chain after `stitch-design` or `stitch-loop` for design→video workflow
- Use with `video-compress` for optimized output
- Use with `caption-subtitle-formatter` for adding subtitles
