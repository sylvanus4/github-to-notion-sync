# Skill Seekers CLI Reference

## Global Options

```
--version    Show version
--help       Show help
--verbose    Enable verbose output
--quiet      Suppress non-essential output
```

## Commands

### `create` — One-shot skill creation

```bash
skill-seekers create <source>
```

Source can be a URL, GitHub `owner/repo`, local path, or PDF file. Automatically detects source type and runs the full pipeline: scrape, build, enhance.

### `scrape` — Scrape documentation

```bash
skill-seekers scrape --url <url> --name <name>
skill-seekers scrape --config configs/<name>.json
```

Options:
- `--url` — Documentation site URL
- `--name` — Output directory name
- `--config` — Config file path
- `--max-pages` — Limit pages scraped
- `--follow-links` — Follow cross-domain links (default: false)

### `github` — GitHub repository scraping

```bash
skill-seekers github --repo owner/repo
skill-seekers github --repo owner/repo --token $GITHUB_TOKEN
```

Three-stream analysis: Code structure, Documentation, Repository insights.

Options:
- `--repo` — GitHub repository (owner/repo format)
- `--token` — GitHub personal access token (for private repos or rate limits)
- `--branch` — Target branch (default: main)

### `pdf` — PDF extraction

```bash
skill-seekers pdf --pdf <file> --name <name>
```

### `video` — Video extraction

```bash
skill-seekers video --url <youtube-url> --name <name>
```

Requires `[video]` or `[video-full]` extras. Uses Whisper for transcription.

### `unified` — Multi-source scrape

```bash
skill-seekers unified --config configs/<name>_unified.json
```

Scrapes from multiple sources defined in a unified config file.

### `enhance` — Enhancement pass

```bash
skill-seekers enhance output/<name>/
skill-seekers enhance output/<name>/ --preset security-focus
skill-seekers enhance output/<name>/ --preset architecture-comprehensive
```

### `package` — Package for target platform

```bash
skill-seekers package output/<name> --target cursor
skill-seekers package output/<name> --target claude
skill-seekers package output/<name> --target langchain
skill-seekers package output/<name> --target markdown
```

Targets: `claude`, `gemini`, `openai`, `langchain`, `llama-index`, `cursor`, `markdown`.

### `install` — Full pipeline

```bash
skill-seekers install --config <name>
```

Runs: fetch config → scrape → enhance → package → upload.

### `install-agent` — Install to AI agent

```bash
skill-seekers install-agent output/<name>/ --agent cursor
skill-seekers install-agent output/<name>/ --agent claude
```

### `detect-conflicts` — Conflict detection

```bash
skill-seekers detect-conflicts output/<name>/ --skills-dir .cursor/skills/
```

Compares trigger phrases, capabilities, and description overlap.

### `merge` — Merge sources

```bash
skill-seekers merge output/source1 output/source2 --output output/merged
```

### `list-configs` — List presets

```bash
skill-seekers list-configs
```

### `generate-config` — Generate config

```bash
skill-seekers generate-config --url <url> --name <name>
```

### `workflows` — Enhancement workflow management

```bash
skill-seekers workflows list
skill-seekers workflows show <name>
skill-seekers workflows copy <name> <dest>
skill-seekers workflows add <file>
skill-seekers workflows remove <name>
skill-seekers workflows validate <file>
```
