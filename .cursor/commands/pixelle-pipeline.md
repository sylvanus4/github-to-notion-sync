## Pixelle Pipeline

Run the full 4-phase short-form video production pipeline: scripting, generation, post-production, and distribution.

### Usage

```
# Full pipeline from topic
/pixelle-pipeline "Why AI agents are the future of software development"

# Full pipeline with platform target
/pixelle-pipeline "Your topic" --platform youtube-shorts

# Skip distribution phase
/pixelle-pipeline "Your topic" --skip-distribute

# Korean content for TikTok
/pixelle-pipeline "AI 플랫폼 전략" --platform tiktok --lang ko

# Minimal pipeline (generate + compress only)
/pixelle-pipeline "Your topic" --minimal
```

### Phases

| Phase | Skills Used | Output |
|-------|-------------|--------|
| 1. Script & Hook | `video-script-generator`, `hook-generator` | Structured script with opening hook |
| 2. Generate Video | `pixelle-template`, `pixelle-generate` | Raw video (`.mp4`) |
| 3. Post-Production | `video-compress`, `caption-subtitle-formatter` | Compressed video + subtitles |
| 4. Distribution | `content-repurposing-engine`, `video-editing-planner` | Multi-platform content + editing plan |

### Platform Presets

| Platform | Aspect | Scenes | Speed |
|----------|--------|--------|-------|
| `youtube-shorts` | 9:16 | 4 | 1.3 |
| `tiktok` | 9:16 | 5 | 1.2 |
| `instagram-reels` | 9:16 | 3 | 1.2 |
| `linkedin` | 1:1 | 6 | 1.0 |
| `youtube` | 16:9 | 8 | 1.0 |

### Execution

Read and follow the `pixelle-video-pipeline` skill (`.cursor/skills/pixelle/pixelle-video-pipeline/SKILL.md`).

### Examples

YouTube Shorts from topic:
```
/pixelle-pipeline "3 reasons to adopt AI agents today" --platform youtube-shorts
```

Full pipeline with Korean TikTok target:
```
/pixelle-pipeline "클라우드 네이티브 AI의 미래" --platform tiktok --lang ko
```

Quick generation without distribution:
```
/pixelle-pipeline "Your topic" --minimal
```
