---
name: pixelle-setup
description: >-
  Install, configure, and verify Pixelle-Video for local short-form video
  generation. Use when the user asks to "install pixelle", "setup pixelle",
  "pixelle-setup", "configure pixelle video", "Pixelle 설치", "Pixelle 설정",
  "check pixelle health", "pixelle health check", or needs to prepare the
  Pixelle-Video environment before generating videos. Do NOT use for video
  generation (use pixelle-generate). Do NOT use for template browsing (use
  pixelle-template). Do NOT use for the full production pipeline (use
  pixelle-video-pipeline).
disable-model-invocation: true
---

# pixelle-setup

Install, configure, and health-check the Pixelle-Video short-form video engine.

## When to Use

- First-time setup of Pixelle-Video
- Reconfiguring LLM or ComfyUI settings
- Diagnosing why video generation fails
- Verifying prerequisites after system updates

## Prerequisites

| Tool | Check Command | Install |
|------|--------------|---------|
| Python 3.11+ | `python3 --version` | `brew install python@3.12` |
| uv | `uv --version` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| ffmpeg | `ffmpeg -version` | `brew install ffmpeg` |
| Ollama (optional) | `ollama list` | `brew install ollama` |

## Setup Steps

### 1. Clone or Update Repository

```bash
# First time
cd /Users/hanhyojung/thaki/ai-platform-strategy
git clone https://github.com/AIDC-AI/Pixelle-Video.git vendor/Pixelle-Video

# Update existing
cd vendor/Pixelle-Video && git pull origin main
```

### 2. Install Dependencies

```bash
cd vendor/Pixelle-Video
uv sync
```

### 3. Configure `config.yaml`

Copy the example and fill in your settings:

```bash
cp config.example.yaml config.yaml
```

**Minimal config for local Ollama (no ComfyUI, text-only videos):**

```yaml
project_name: Pixelle-Video

llm:
  api_key: "ollama"
  base_url: "http://localhost:11434/v1"
  model: "qwen2.5:7b"

comfyui:
  comfyui_url: http://127.0.0.1:8188
  tts:
    default_workflow: selfhost/tts_edge.json
  image:
    default_workflow: runninghub/image_flux.json
  video:
    default_workflow: runninghub/video_wan2.1_fusionx.json

template:
  default_template: "1080x1920/static_default.html"
```

**LLM Presets:**

| Provider | `base_url` | `model` |
|----------|-----------|---------|
| Ollama (local) | `http://localhost:11434/v1` | `qwen2.5:7b` |
| OpenAI | `https://api.openai.com/v1` | `gpt-4o` |
| DeepSeek | `https://api.deepseek.com` | `deepseek-chat` |
| Qwen Max | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-max` |

### 4. Health Check

```bash
cd vendor/Pixelle-Video

# Verify Python API imports
uv run python -c "
from pixelle_video import PixelleVideoCore, config_manager
print('Import OK')
print(f'Config loaded: {config_manager.config.project_name}')
print(f'LLM config: {config_manager.config.to_dict().get(\"llm\", {})}')
"

# Test LLM connectivity (Ollama)
curl -s http://localhost:11434/v1/models | python3 -m json.tool

# Test ffmpeg
ffmpeg -version 2>&1 | head -1
```

## Known Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError: pixelle_video.cli` | CLI module not yet implemented upstream | Use Python API directly via `PixelleVideoCore` |
| `config_manager.get('llm.model')` returns `None` | `get()` only supports top-level keys | Access nested keys via `config_manager.config.to_dict()['llm']['model']` |
| Template warning on startup | Configured template path doesn't exist | Check `templates/` directory; use `static_default.html` for text-only |

## File Locations

| File | Path |
|------|------|
| Repo root | `vendor/Pixelle-Video/` |
| Config | `vendor/Pixelle-Video/config.yaml` |
| Config example | `vendor/Pixelle-Video/config.example.yaml` |
| Templates | `vendor/Pixelle-Video/templates/` |
| Output | `vendor/Pixelle-Video/output/` |
| Streamlit UI | `vendor/Pixelle-Video/web/app.py` |

## Quick Verification Script

```python
import asyncio
from pixelle_video import PixelleVideoCore

async def verify():
    core = PixelleVideoCore()
    await core.initialize()
    cfg = core.config
    print(f"Project: {cfg.get('project_name')}")
    llm = cfg.get('llm', {})
    print(f"LLM: {llm.get('model')} @ {llm.get('base_url')}")
    print(f"Pipelines: {list(core.pipelines.keys())}")
    print("Health check PASSED")

asyncio.run(verify())
```

Run with: `cd vendor/Pixelle-Video && uv run python -c "$(cat above_script)"`

## Examples

**User:** "pixelle 설치해줘" / "setup pixelle"
→ Run prerequisites check, clone repo, configure config.yaml with Ollama, run health check

**User:** "pixelle health check" / "pixelle 상태 확인"
→ Run the Quick Verification Script section, report pass/fail per component

**User:** "reconfigure pixelle to use OpenAI"
→ Update config.yaml LLM section with OpenAI base_url and model, re-run health check
