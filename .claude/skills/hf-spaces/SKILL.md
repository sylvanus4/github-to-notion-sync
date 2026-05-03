---
name: hf-spaces
description: >-
  Discover, inspect, and develop Hugging Face Spaces (Gradio, Streamlit,
  Docker apps) via the hf CLI. Use when the user asks to search for Spaces,
  get Space info, enable dev mode for live development, or hot-reload code
  changes on a running Space. Do NOT use for Inference Endpoints (use
  hf-endpoints), model serving (use hf-endpoints), repo management (use
  hf-repos), or compute jobs (use hf-jobs). Korean triggers: "HF 스페이스", "스페이스
  검색", "스페이스 개발", "Gradio 앱".
---

# Hugging Face Spaces

> **Prerequisites**: `hf` CLI installed and authenticated. See `hf-hub` skill.

## Quick Commands

### Search Spaces

```bash
hf spaces ls --search "chatbot" --sort trending --limit 10
hf spaces ls --author gradio --format json
hf spaces ls -q  # Space IDs only
```

| Flag | Required | Description |
|------|----------|-------------|
| `--search TEXT` | No | Search query |
| `--author TEXT` | No | Filter by author/org |
| `--sort` | No | `created_at`, `downloads`, `last_modified`, `likes`, `trending_score` |
| `--limit INTEGER` | No | Number of results (default: 10) |
| `--format [table\|json]` | No | Output format |
| `-q, --quiet` | No | Print Space IDs only |

### Get Space Info

```bash
hf spaces info SPACE_ID
hf spaces info SPACE_ID --format json
```

### Dev Mode

Enable dev mode for live development without rebuilding:

```bash
hf spaces dev-mode SPACE_ID --enable
hf spaces dev-mode SPACE_ID --disable
```

> **Write command** — changes the Space's runtime mode.

When dev mode is enabled, code changes are applied without triggering a full rebuild.

### Hot Reload

Push a single file change to a running Space instantly:

```bash
hf spaces hot-reload SPACE_ID --file app.py
```

> **Write command** — modifies the running Space code.

This updates the specified file on the running Space without restarting.

## Common Patterns

```bash
# Find trending Gradio demos
hf spaces ls --search "gradio" --sort trending --limit 10

# Discover Spaces by a specific organization
hf spaces ls --author huggingface --sort likes --limit 20

# Get runtime status of a Space
hf spaces info my-org/my-space --format json

# Live development workflow
hf spaces dev-mode my-org/my-space --enable
# ... edit app.py locally ...
hf spaces hot-reload my-org/my-space --file app.py
# ... test changes ...
hf spaces dev-mode my-org/my-space --disable

# Find Spaces using a specific model (search by model name)
hf spaces ls --search "meta-llama/Llama-3.2" --sort trending
```

## Examples

### Example 1: Browse and inspect Spaces

**User says:** "Find popular text-to-image Spaces"

**Actions:**
1. Search: `hf spaces ls --search "text-to-image" --sort trending --limit 10`
2. Inspect top result: `hf spaces info SPACE_ID --format json`
3. Report Space URL, SDK type, and hardware info

### Example 2: Develop a Space

**User says:** "I want to iterate on my Space without full rebuilds"

**Actions:**
1. Enable dev mode: `hf spaces dev-mode my-org/my-space --enable`
2. Make changes locally to `app.py`
3. Hot reload: `hf spaces hot-reload my-org/my-space --file app.py`
4. Test at the Space URL
5. When done: `hf spaces dev-mode my-org/my-space --disable`

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Space not found | Verify Space ID and check if it's private |
| Dev mode not available | Ensure you own the Space and it uses a supported SDK |
| Hot reload failed | Check that the file path is correct relative to Space root |
| Space crashed after reload | Check Space logs via HF dashboard; disable dev mode and rebuild |
| Permission denied | Verify token has write access to the Space repo |
