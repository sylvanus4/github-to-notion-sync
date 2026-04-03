## Video Script Generator

Generate structured video scripts with hooks, content sections, pacing marks, B-roll cues, and CTAs — optimized for YouTube, Shorts, TikTok, Reels, and educational content.

### Usage

```
# YouTube explainer
/video-script "Why AI agents will replace SaaS" --platform youtube --duration 10min

# TikTok short
/video-script "3-second rule in presentations" --platform tiktok --duration 55s

# Educational series
/video-script "Python 기초 - 리스트와 딕셔너리" --platform educational --duration 8min

# From existing content
/video-script "outputs/papers/review.md" --platform shorts --duration 60s
```

### Workflow

1. **Brief** — Collect topic, platform, duration, audience, tone, source material
2. **Format** — Select platform-specific structure and constraints
3. **Generate** — Write each section with spoken script, visual direction, and pacing notes
4. **Hook** — Construct platform-optimized opening (2s for TikTok, 30s for YouTube)
5. **Validate** — Check timing against target duration ±10%

### Output

Full script with metadata, per-section script/visual/pacing blocks, and production notes (B-roll list, graphics needed, music suggestions, thumbnail concept).

### Execution

Read and follow the `video-script-generator` skill (`.cursor/skills/standalone/video-script-generator/SKILL.md`).
