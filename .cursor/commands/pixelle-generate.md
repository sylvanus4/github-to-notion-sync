## Pixelle Generate

Generate a short-form video from a topic or script using the Pixelle-Video engine.

### Usage

```
# Generate from a topic (AI writes the script)
/pixelle-generate "Why AI agents are the future of software development"

# Generate from a topic with specific settings
/pixelle-generate "Topic here" --scenes 5 --voice en-US-AriaNeural --template 1080x1920/static_default.html

# Generate from a pre-written script (fixed mode)
/pixelle-generate --mode fixed --script "Line 1.\nLine 2.\nLine 3."

# Korean video with Korean TTS
/pixelle-generate "AI 에이전트가 소프트웨어 개발의 미래인 이유" --voice ko-KR-SunHiNeural

# Quick text-only video (no ComfyUI needed)
/pixelle-generate "Your topic" --template 1080x1920/static_default.html

# Widescreen cinematic video (requires ComfyUI)
/pixelle-generate "Your topic" --template 1920x1080/image_film.html
```

### Parameters

| Flag | Default | Description |
|------|---------|-------------|
| `--mode` | `generate` | `generate` (AI script) or `fixed` (use provided text) |
| `--scenes` | `5` | Number of scenes (generate mode only) |
| `--voice` | `en-US-AriaNeural` | Edge-TTS voice name |
| `--speed` | `1.2` | TTS speech speed |
| `--template` | `1080x1920/static_default.html` | HTML frame template |
| `--bgm-volume` | `0.2` | Background music volume (0.0-1.0) |
| `--output` | auto | Output directory path |

### Execution

Read and follow the `pixelle-generate` skill (`.cursor/skills/pixelle/pixelle-generate/SKILL.md`).

### Examples

Quick test video (text-only, no ComfyUI):
```
/pixelle-generate "The rise of agentic AI" --scenes 3 --template 1080x1920/static_default.html
```

Korean educational video:
```
/pixelle-generate "쿠버네티스 오토스케일링의 이해" --voice ko-KR-InJoonNeural --scenes 5
```
