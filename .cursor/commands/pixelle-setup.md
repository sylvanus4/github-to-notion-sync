## Pixelle Setup

Install, configure, and verify the Pixelle-Video short-form video engine for local video generation.

### Usage

```
# Full setup (clone, install, configure, health check)
/pixelle-setup

# Health check only (verify existing installation)
/pixelle-setup --health-check

# Reconfigure LLM provider
/pixelle-setup --reconfigure

# Update to latest version
/pixelle-setup --update
```

### Workflow

1. **Prerequisites** — Verify Python 3.11+, uv, ffmpeg, optionally Ollama
2. **Clone/Update** — Clone or pull `vendor/Pixelle-Video/`
3. **Install** — Run `uv sync` for dependencies
4. **Configure** — Generate `config.yaml` with LLM and ComfyUI settings
5. **Health Check** — Verify Python API imports, LLM connectivity, and pipeline availability

### Execution

Read and follow the `pixelle-setup` skill (`.cursor/skills/pixelle/pixelle-setup/SKILL.md`).

### Examples

First-time setup with Ollama:
```
/pixelle-setup
```

Verify existing installation works:
```
/pixelle-setup --health-check
```

Switch LLM from Ollama to OpenAI:
```
/pixelle-setup --reconfigure
```
