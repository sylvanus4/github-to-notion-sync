---
name: skill-seekers
description: "Convert documentation sites, GitHub repos, PDFs, and videos into structured Cursor skill files with conflict detection. Use when converting external docs/repos into skills, scraping documentation for skill creation, building skills from existing sources, or detecting conflicts with installed skills. Do NOT use for creating skills from scratch (use anthropic-skill-creator or create-skill). Do NOT use for discovering pre-built skills from a registry (use find-skills)."
metadata:
  upstream: "https://github.com/yusufkaraaslan/Skill_Seekers"
  version: 3.2.0
  license: MIT
---

# Skill Seekers — Documentation-to-Skill Converter

Convert any documentation source into a structured Cursor skill file. Supports doc sites (with llms.txt), GitHub repos, PDFs, videos, and local directories.

## Prerequisites

Install the CLI (one-time):

```bash
pip install skill-seekers[all]
```

For MCP integration only:

```bash
pip install skill-seekers[mcp]
```

Verify installation:

```bash
skill-seekers --version
```

## Workflow

### 1. Choose a Source

| Source type | Command |
|-------------|---------|
| Documentation URL | `skill-seekers create https://docs.react.dev/` |
| GitHub repo | `skill-seekers create facebook/react` |
| Local directory | `skill-seekers create ./my-project` |
| PDF file | `skill-seekers create manual.pdf` |
| Video (YouTube) | `skill-seekers video --url <youtube-url> --name <name>` |
| Config preset | `skill-seekers scrape --config configs/react.json` |

### 2. Package for Cursor

```bash
skill-seekers package output/<name> --target cursor
```

This produces a SKILL.md and supporting files in the Cursor-compatible format.

### 3. Install to Cursor

```bash
skill-seekers install-agent output/<name>/ --agent cursor
```

Or manually copy the output directory into `.cursor/skills/<name>/`.

### 4. Detect Conflicts

Before installing, check for conflicts with existing skills:

```bash
skill-seekers detect-conflicts output/<name>/ --skills-dir .cursor/skills/
```

This compares the new skill's trigger phrases and capabilities against all installed skills and reports overlaps.

## Key CLI Commands

```bash
# One-shot: fetch, scrape, enhance, package, install
skill-seekers install --config <name>

# List available config presets
skill-seekers list-configs

# Quick scrape without a config file
skill-seekers scrape --url <url> --name <name>

# GitHub repo scraping (three-stream: code, docs, insights)
skill-seekers github --repo owner/repo

# PDF extraction
skill-seekers pdf --pdf <file> --name <name>

# Multi-source unified scrape
skill-seekers unified --config configs/<name>_unified.json

# Enhance with additional analysis
skill-seekers enhance output/<name>/ --preset security-focus

# Merge multiple scraped sources
skill-seekers merge output/source1 output/source2 --output output/merged
```

## Config Presets

List available presets:

```bash
skill-seekers list-configs
```

Common presets: `react`, `vue`, `angular`, `django`, `fastapi`, `docker`, `godot`, `claude-code`.

Generate a custom config:

```bash
skill-seekers generate-config --url https://docs.example.com --name example
```

## MCP Server Integration

Skill Seekers provides 26 MCP tools. To use as an MCP server in Cursor:

**Option A: HTTP transport (recommended for Cursor)**

```bash
python -m skill_seekers.mcp.server_fastmcp --transport http --port 8765
```

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "skill-seekers": {
      "url": "http://localhost:8765/sse"
    }
  }
}
```

**Option B: stdio transport**

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "skill-seekers": {
      "command": "python",
      "args": ["-m", "skill_seekers.mcp.server_fastmcp"],
      "cwd": "/path/to/Skill_Seekers"
    }
  }
}
```

### MCP Tool Categories

- **Core (9):** `list_configs`, `generate_config`, `validate_config`, `estimate_pages`, `scrape_docs`, `package_skill`, `upload_skill`, `enhance_skill`, `install_skill`
- **Extended (10):** `scrape_github`, `scrape_pdf`, `unified_scrape`, `merge_sources`, `detect_conflicts`, `add_config_source`, `fetch_config`, and more
- **Vector DB (4):** `export_to_chroma`, `export_to_weaviate`, `export_to_faiss`, `export_to_qdrant`
- **Cloud (3):** `cloud_upload`, `cloud_download`, `cloud_list`

## Cursor-Specific Packaging

When packaging for Cursor, Skill Seekers generates:

1. **`SKILL.md`** with YAML frontmatter (`name`, `description`, `metadata`)
2. **`references/`** directory with scraped documentation split into progressive-disclosure files
3. Descriptions optimized for Cursor's skill triggering (WHAT + WHEN + DO NOT USE)

### Post-Processing Checklist

After `skill-seekers package ... --target cursor`:

- [ ] Verify SKILL.md frontmatter has `name` (max 64 chars, lowercase, hyphens)
- [ ] Verify `description` includes trigger scenarios and exclusions
- [ ] Confirm SKILL.md is under 500 lines; move excess to `references/`
- [ ] Run `detect-conflicts` against `.cursor/skills/`
- [ ] Copy output to `.cursor/skills/<name>/`

## Enhancement Presets

```bash
skill-seekers workflows list           # List available presets
skill-seekers enhance output/<name>/ --preset <preset>
```

Common presets: `security-focus`, `architecture-comprehensive`, `api-deep-dive`.

## Detailed Reference

For full CLI reference, see [references/cli-commands.md](references/cli-commands.md).
For MCP server setup details, see [references/mcp-setup.md](references/mcp-setup.md).
For config preset details, see [references/presets.md](references/presets.md).
