---
name: remotion-motion-forge
description: >-
  Generate production-quality motion graphics videos programmatically using
  Remotion (React-based video renderer). Extracts design tokens from the
  project's design system, scaffolds a Remotion project, generates React video
  compositions from user intent, and renders to .mp4 via CLI. Supports 4
  template types: AppDemo, FeatureHighlight, DSShowcase, PromoReel. Use when
  the user asks to "create motion graphics", "generate video from design
  system", "app demo video", "Remotion video", "motion forge", "render video
  from code", "programmatic video", "모션 그래픽스", "Remotion 비디오", "앱 데모 영상", "디자인
  시스템 영상", "모션 포지", "프로그래매틱 비디오", "B-roll 생성", "프로모 영상", or wants to turn
  design system tokens into animated video content without After Effects. Do
  NOT use for static architecture diagrams (use visual-explainer). Do NOT use
  for slide deck generation (use anthropic-pptx or nlm-slides). Do NOT use for
  NotebookLM video explainers (use nlm-video). Do NOT use for video script
  writing only (use video-script-generator). Do NOT use for post-production
  editing plans only (use video-editing-planner). Do NOT use for video
  compression only (use video-compress). Do NOT use for interactive HTML demos
  without video output (use demo-forge). Do NOT use for subtitle/caption
  formatting (use caption-subtitle-formatter).
disable-model-invocation: true
---

# Remotion Motion Forge — Programmatic Motion Graphics Generator

Generate production-quality `.mp4` motion graphics from the project's design system using Remotion. No After Effects required — everything is React code rendered via CLI.

## Usage

```
/remotion-motion-forge                          # interactive — asks for intent
/remotion-motion-forge --template AppDemo       # app interaction walkthrough
/remotion-motion-forge --template PromoReel     # YouTube B-roll / social promo
/remotion-motion-forge --template DSShowcase    # design system before/after
/remotion-motion-forge --template FeatureHighlight  # single feature spotlight
/remotion-motion-forge --format 16:9            # landscape (default)
/remotion-motion-forge --format 9:16            # vertical (Shorts/Reels)
/remotion-motion-forge --duration 30            # target duration in seconds
/remotion-motion-forge --skip-compress          # skip final compression step
/remotion-motion-forge --script-input <path>    # use video-script-generator output as scene guide
```

## Prerequisites

Before running, verify these are installed:

| Dependency | Min Version | Check Command |
|------------|-------------|---------------|
| Node.js | 18+ | `node --version` |
| npm or pnpm | any | `npm --version` |
| ffmpeg | any | `ffmpeg -version` |
| `DESIGN.md` | — | File exists at project root |

If prerequisites are missing, report which ones and stop. Do not attempt partial execution.

## Workflow

This skill follows a 3-phase pipeline. Each phase persists intermediate outputs to disk per `pipeline-skill-intermediate-persistence.mdc`.

### Phase 1: Design System Extraction

**Goal**: Convert `DESIGN.md` and `.cursor/rules/design-system.mdc` into Remotion-consumable TypeScript tokens.

1. Read `DESIGN.md` (Refined Swiss theme — colors, typography, spacing, radii, shadows, animations)
2. Read `.cursor/rules/design-system.mdc` for canonical token values
3. Generate `remotion/tokens/design-tokens.ts` exporting:

```typescript
export const colors = {
  brand: { 50: '#eff6ff', 100: '#dbeafe', /* ... */ 600: '#2563eb', 900: '#1e3a8a' },
  accent: { 400: '#fb923c', 500: '#f97316', 600: '#ea580c' },
  surface: { light: '#F9FAFB', dark: '#111827', card: { light: '#FFFFFF', dark: '#1F2937' } },
  foreground: { primary: { light: '#111827', dark: '#F3F4F6' }, secondary: { light: '#4B5563', dark: '#9CA3AF' } },
  status: { success: '#16a34a', error: '#dc2626', warning: '#d97706' },
};

export const typography = {
  fontFamily: { sans: 'Inter, system-ui, sans-serif', mono: 'JetBrains Mono, monospace' },
  size: { xs: 12, sm: 14, base: 16, lg: 18, xl: 20, '2xl': 24, '3xl': 30 },
  weight: { normal: 400, medium: 500, semibold: 600, bold: 700 },
};

export const spacing = { 1: 4, 2: 8, 3: 12, 4: 16, 5: 20, 6: 24, 8: 32, 10: 40, 12: 48 };
export const radii = { lg: 8, full: 9999 };
export const shadows = { sm: '0 1px 2px rgba(0,0,0,0.05)', xl: '0 20px 25px rgba(0,0,0,0.1)' };

export const animations = {
  duration: { fast: 150, normal: 300, slow: 500, enter: 200, exit: 150 },
  easing: { default: 'ease', in: 'ease-in', out: 'ease-out', inOut: 'ease-in-out' },
};
```

4. Write the file to `remotion/tokens/design-tokens.ts`
5. Persist Phase 1 manifest: `outputs/motion-forge/{date}/phase-1-tokens.json`

**Checkpoint**: Verify `design-tokens.ts` compiles without TypeScript errors.

### Phase 2: Remotion Project Scaffolding

**Goal**: Set up Remotion in a `remotion/` subdirectory if not already present.

**Skip condition**: If `remotion/package.json` already exists with `remotion` in dependencies, skip to Phase 3.

1. Create `remotion/package.json`:
```json
{
  "name": "motion-forge-remotion",
  "private": true,
  "scripts": {
    "studio": "remotion studio",
    "render": "remotion render"
  },
  "dependencies": {
    "remotion": "^4.0.0",
    "@remotion/cli": "^4.0.0",
    "@remotion/player": "^4.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "@types/react": "^18.0.0"
  }
}
```

2. Create `remotion/tsconfig.json`:
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "outDir": "dist",
    "baseUrl": ".",
    "paths": { "@tokens/*": ["tokens/*"], "@components/*": ["components/*"] }
  },
  "include": ["**/*.ts", "**/*.tsx"]
}
```

3. Create entry point `remotion/index.ts`:
```typescript
import { registerRoot } from "remotion";
import { RemotionRoot } from "./Root";
registerRoot(RemotionRoot);
```

4. Create `remotion/Root.tsx` with an empty composition registry (compositions will be added in Phase 3)

5. Create directory structure:
```
remotion/
  index.ts
  Root.tsx
  tokens/design-tokens.ts     (from Phase 1)
  compositions/               (empty, populated in Phase 3)
  components/                 (empty, populated in Phase 3)
  package.json
  tsconfig.json
```

6. Run `npm install` inside `remotion/`
7. Persist Phase 2 manifest: `outputs/motion-forge/{date}/phase-2-scaffold.json`

**Checkpoint**: Verify `npx remotion compositions remotion/index.ts` runs without errors.

### Phase 3: Composition Generation and Rendering

**Goal**: Generate a React video composition from user intent, register it, render to `.mp4`.

1. **Parse user intent**: Determine template type, content, format, and duration from user input.

2. **Select template**: Match intent to one of 4 composition types (see Templates section below).

3. **Generate composition component**: Write a `.tsx` file under `remotion/compositions/` using:
   - `useCurrentFrame()` + `useVideoConfig()` for animation timing
   - `interpolate()` for smooth property transitions (opacity, position, scale)
   - `spring()` for physics-based motion
   - `AbsoluteFill` for layout
   - `Sequence` for scene ordering
   - Design tokens from `@tokens/design-tokens`

4. **Generate supporting components**: Write reusable components under `remotion/components/` as needed (phone mockups, text reveals, code blocks, transitions).

5. **Register in Root.tsx**: Add `<Composition />` entry with id, dimensions, fps (30), and duration.

6. **Render**:
```bash
cd remotion && npx remotion render index.ts <CompositionId> ../outputs/motion-forge/{date}/<name>.mp4 --codec h264
```

7. **Compress** (unless `--skip-compress`): Invoke the `video-compress` skill on the rendered file.

8. **Persist Phase 3 outputs**:
   - Video file: `outputs/motion-forge/{date}/{name}.mp4`
   - Render log: `outputs/motion-forge/{date}/render-log.json` (duration, file size, composition id, render time)

**Checkpoint**: Verify the output `.mp4` exists and has a non-zero file size.

## Templates

### AppDemo — App Interaction Walkthrough

| Property | Value |
|----------|-------|
| Default resolution | 1920×1080 (16:9) |
| Duration | 30–60 seconds |
| Scenes | Title card → Feature walkthrough (2-4 scenes) → CTA |
| Key components | `AnimatedPhone`, `ScreenTransition`, `TextReveal`, `FeatureAnnotation` |
| Best for | Product demos, YouTube B-roll, sales materials |

### FeatureHighlight — Single Feature Spotlight

| Property | Value |
|----------|-------|
| Default resolution | 1920×1080 (16:9) |
| Duration | 15–30 seconds |
| Scenes | Hook (3s) → Feature showcase → Key benefit → CTA |
| Key components | `ZoomReveal`, `CodeBlock`, `MetricCounter`, `TextReveal` |
| Best for | Feature announcements, changelog visuals, sprint demos |

### DSShowcase — Design System Before/After

| Property | Value |
|----------|-------|
| Default resolution | 1920×1080 (16:9) |
| Duration | 20–40 seconds |
| Scenes | "Before" state → Animated transition → "After" state → Token callouts |
| Key components | `SplitScreen`, `TokenBadge`, `ColorSwatch`, `TypographyScale` |
| Best for | Design system updates, style guide videos, team education |

### PromoReel — Social Media Promo / YouTube B-roll

| Property | Value |
|----------|-------|
| Default resolution | 1080×1920 (9:16 for Shorts/Reels) or 1920×1080 (16:9 for YouTube) |
| Duration | 15–60 seconds |
| Scenes | Hook (1-3s) → Value proposition (3-5 scenes) → CTA |
| Key components | `KineticText`, `LogoReveal`, `ParticleBackground`, `SlideTransition` |
| Best for | Instagram Reels, TikTok, YouTube Shorts, app store previews |

## Output Artifacts

| Phase | Artifact | Path |
|-------|----------|------|
| 1 | Design tokens TypeScript | `remotion/tokens/design-tokens.ts` |
| 1 | Phase manifest | `outputs/motion-forge/{date}/phase-1-tokens.json` |
| 2 | Remotion project directory | `remotion/` |
| 2 | Phase manifest | `outputs/motion-forge/{date}/phase-2-scaffold.json` |
| 3 | Rendered video | `outputs/motion-forge/{date}/{name}.mp4` |
| 3 | Render log | `outputs/motion-forge/{date}/render-log.json` |

## Integration with Existing Skills

| Skill | How to Integrate |
|-------|-----------------|
| `demo-forge` | When `demo-forge --mode video` is requested and Remotion is available, delegate actual video rendering to this skill; demo-forge continues to handle HTML/script modes |
| `video-script-generator` | Feed a structured video script as `--script-input` to guide composition scene ordering and timing |
| `video-editing-planner` | Reference rendered clips from this skill in post-production plans |
| `video-compress` | Called automatically at Phase 3 step 7 unless `--skip-compress` is passed |
| `content-repurposing-engine` | Generate video script outlines that this skill renders into actual video |
| `design-system-tracker` | When DS changes are detected, trigger `DSShowcase` template to visualize before/after |
| `hook-generator` | Generate attention hooks for the first 1-3 seconds of `PromoReel` compositions |

## Examples

### Example 1: YouTube B-roll from design system

User: "Create a 30-second YouTube B-roll showcasing our platform's design system"

Execution:
1. Phase 1: Extract tokens from DESIGN.md → `remotion/tokens/design-tokens.ts`
2. Phase 2: Scaffold Remotion project (if needed)
3. Phase 3: Generate `PromoReel` composition with brand colors, typography scale animation, component showcase scenes
4. Render at 1920×1080, 30fps, 30s → `outputs/motion-forge/2026-04-04/platform-broll.mp4`
5. Compress via `video-compress`
6. Report: file path, 30s duration, file size, render time

### Example 2: Feature announcement Reel

User: "앱 데모 영상 만들어줘 — 새 검색 필터 기능 강조, 인스타 릴스용"

Execution:
1. Tokens already extracted → skip Phase 1
2. Remotion already scaffolded → skip Phase 2
3. Generate `FeatureHighlight` composition at 1080×1920 (9:16), 20s
4. Scenes: Hook (search icon zoom) → Filter panel animation → Results update → CTA
5. Render → `outputs/motion-forge/2026-04-04/search-filter-reel.mp4`

### Example 3: Design system update visualization

User: "Visualize the color palette change from the last design system update"

Execution:
1. Use existing tokens
2. Generate `DSShowcase` composition: split-screen old vs new palette, animated transition, token labels
3. Render at 1920×1080, 25s → `outputs/motion-forge/2026-04-04/ds-palette-update.mp4`

### Example 4: Pipeline integration with video-script-generator

User: `/video-script` → generates script → `/remotion-motion-forge --script-input outputs/scripts/demo-script.md`

Execution: Parse the script's scene structure, map to composition `Sequence` blocks, generate and render.

## Error Handling

| Scenario | Action |
|----------|--------|
| Node.js < 18 | Report: "Remotion requires Node.js 18+. Current: {version}. Upgrade before proceeding." Stop. |
| ffmpeg not installed | Report: "ffmpeg is required for video encoding. Install via `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Linux)." Stop. |
| `DESIGN.md` missing | Report: "DESIGN.md not found at project root. Run design system documentation first." Stop. |
| Remotion render timeout (> 5 min) | Kill process, report partial render status, suggest reducing duration or complexity. |
| TypeScript compilation error in composition | Show the error, attempt auto-fix for common issues (missing imports, type mismatches). If unfixable, report with the error and the generated file path. |
| npm install fails | Report the error output. Common fix: clear `node_modules` and retry, or check Node.js version compatibility. |
| Output video is 0 bytes | Remotion render likely failed silently. Re-run with `--log=verbose` and report the full output. |
| Disk space insufficient | Check available space before render. Warn if < 1 GB free. |

## Troubleshooting

- **"Cannot find module remotion"**: Run `cd remotion && npm install` to install dependencies.
- **Render produces black frames**: Ensure compositions use `AbsoluteFill` with explicit background colors from design tokens. Transparent backgrounds render as black in h264.
- **Slow render (> 2 min for 30s video)**: Remotion renders are CPU-bound. Reduce resolution for drafts: `--scale 0.5`. Final render at full resolution.
- **"No compositions found"**: Verify `remotion/Root.tsx` has at least one `<Composition />` registered and `remotion/index.ts` calls `registerRoot`.
- **Font rendering issues**: Remotion uses the system's installed fonts. Ensure Inter is installed, or use `@remotion/google-fonts` package.
