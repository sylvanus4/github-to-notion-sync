## Remotion Motion Forge

Generate production-quality motion graphics videos programmatically using Remotion. Extracts design tokens, scaffolds a Remotion project, generates React video compositions from user intent, and renders to `.mp4`.

### Usage

```
# Interactive — asks for intent
/remotion-motion-forge

# App demo walkthrough (16:9, 45s)
/remotion-motion-forge --template AppDemo "Platform dashboard walkthrough"

# Instagram Reel / YouTube Short (9:16, 20s)
/remotion-motion-forge --template PromoReel --format 9:16 --duration 20 "AI platform promo"

# Design system before/after visualization
/remotion-motion-forge --template DSShowcase "Color palette update"

# Feature spotlight with metrics
/remotion-motion-forge --template FeatureHighlight --duration 25 "New search filter feature"

# Use a video-script-generator output as scene guide
/remotion-motion-forge --script-input outputs/scripts/demo-script.md --template AppDemo

# Skip compression step
/remotion-motion-forge --template PromoReel --skip-compress "Quick draft promo"
```

### Templates

| Template | Use Case | Default Format | Duration |
|----------|----------|----------------|----------|
| `AppDemo` | App interaction walkthrough with UI mockups | 1920×1080 (16:9) | 30–60s |
| `FeatureHighlight` | Single feature spotlight with annotations | 1920×1080 (16:9) | 15–30s |
| `DSShowcase` | Design system before/after animation | 1920×1080 (16:9) | 20–40s |
| `PromoReel` | Social media promo / YouTube B-roll | 1080×1920 (9:16) or 1920×1080 | 15–60s |

### Workflow

1. **Phase 1**: Extract design tokens from `DESIGN.md` → `remotion/tokens/design-tokens.ts`
2. **Phase 2**: Scaffold Remotion project in `remotion/` (skip if already set up)
3. **Phase 3**: Generate composition, render via `npx remotion render`, compress via `video-compress`

### Output

Video file at `outputs/motion-forge/{date}/{name}.mp4` with render log.

### Execution

Read and follow the `remotion-motion-forge` skill (`.cursor/skills/standalone/remotion-motion-forge/SKILL.md`).
