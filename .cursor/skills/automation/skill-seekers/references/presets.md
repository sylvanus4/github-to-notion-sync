# Skill Seekers Config Presets

## Listing Presets

```bash
skill-seekers list-configs
```

## Available Presets

Presets are JSON config files that define scraping targets, page limits, and output format for common frameworks and tools.

### Frontend Frameworks

| Preset | Source |
|--------|--------|
| `react` | React documentation (react.dev) |
| `vue` | Vue.js documentation (vuejs.org) |
| `angular` | Angular documentation (angular.dev) |

### Backend Frameworks

| Preset | Source |
|--------|--------|
| `django` | Django documentation |
| `fastapi` | FastAPI documentation |

### Game Engines

| Preset | Source |
|--------|--------|
| `godot` | Godot Engine documentation |
| `godot_unified` | Godot (multi-source: docs + GitHub) |

### DevOps / Infra

| Preset | Source |
|--------|--------|
| `docker` | Docker documentation |

### AI / LLM

| Preset | Source |
|--------|--------|
| `claude-code` | Claude Code documentation |

### Other

| Preset | Source |
|--------|--------|
| `httpx_comprehensive` | HTTPX Python HTTP client |
| `blender-unified` | Blender 3D (multi-source) |
| `medusa-mercurjs` | MedusaJS / MercurJS |
| `astrovalley_unified` | AstroValley (multi-source) |

## Generating Custom Configs

```bash
skill-seekers generate-config --url https://docs.example.com --name my-project
```

This generates a JSON config file with default settings you can customize before scraping.

## Enhancement Presets

Enhancement presets modify how scraped content is analyzed and structured:

```bash
skill-seekers workflows list
```

Common enhancement presets:
- `security-focus` — Emphasize security patterns and vulnerabilities
- `architecture-comprehensive` — Deep architecture analysis
- `api-deep-dive` — Detailed API reference extraction
