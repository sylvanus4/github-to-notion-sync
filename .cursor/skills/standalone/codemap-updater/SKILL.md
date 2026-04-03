---
name: codemap-updater
version: 1.0.0
description: "Generate and maintain a structured codebase map (CODEMAP.md) that gives agents quick navigation context — directory tree, entry points, architecture layers, module dependencies, and hot-file index."
---

# Codemap Updater

Generate and maintain `CODEMAP.md` at the project root — a compact, up-to-date navigation reference that helps agents (and humans) orient quickly in the codebase without reading every file.

## Trigger Phrases

- "update codemap", "codemap", "codebase map", "refresh codemap"
- "코드맵 업데이트", "코드맵", "코드베이스 맵"
- `/codemap` command

## Do NOT Use For

- General code review (use `deep-review` or `simplify`)
- Dependency graph visualization only (use `dependency-radar` or `visual-explainer`)
- Git history ownership analysis only (use `codebase-archaeologist`)
- Documentation writing (use `technical-writer`)

## Modes

| Mode | Flag | Description |
|------|------|-------------|
| **refresh** | `--refresh` | Full rebuild from scratch — scan entire project |
| **diff** | `--diff` | Show what changed since the last CODEMAP.md update |
| **display** | (default) | Display the current CODEMAP.md contents |

## Output: CODEMAP.md Sections

The generated `CODEMAP.md` follows this structure (keep under 500 lines total):

### 1. Architecture Overview
- High-level description of project layers (backend, frontend, scripts, config, docs)
- Primary tech stack summary

### 2. Entry Points
- Main application entry files (e.g., `backend/app/main.py`, CLI scripts)
- Configuration entry files (e.g., `.env`, `settings.py`)
- CI/CD entry files (e.g., `.github/workflows/`)

### 3. Directory Map
- Top-level directory tree (depth 2) with one-line purpose annotations
- Only include directories with substantive code (skip `node_modules`, `__pycache__`, `.git`)

### 4. Module Index
- Key modules/packages with their public interfaces
- Group by domain (backend services, frontend components, scripts, skills)

### 5. Hot Files (Most Changed)
- Top 15 most-frequently-modified files from `git log --format='' --name-only | sort | uniq -c | sort -rn | head -15`
- Indicates where active development is concentrated

### 6. Dependency Overview
- Internal module dependency direction (which modules import which)
- External dependency summary (major packages and their roles)

## Workflow

### Step 1: Gather Data
Use these tools in parallel:
- `Glob` to scan project structure (depth 2-3)
- `Shell` to run `git log --format='' --name-only --since='3 months ago' | sort | uniq -c | sort -rn | head -20` for hot files
- `SemanticSearch` or `Grep` to identify entry points and key exports

### Step 2: Analyze Architecture
- Classify directories into layers (backend, frontend, scripts, config, docs, tests, outputs)
- Identify primary entry points per layer
- Map internal import relationships between top-level modules

### Step 3: Generate CODEMAP.md
- Write the structured document following the sections above
- Keep descriptions concise (one line per item where possible)
- Total file MUST stay under 500 lines

### Step 4: Verify
- Confirm all referenced files/directories exist
- Check that hot files list is current
- Validate the architecture description matches reality

## When to Update

- After completing a multi-file feature (>5 files changed)
- After directory restructuring or new module creation
- At the start of a new work session when the codebase is unfamiliar
- After major dependency changes
- When invoked via `/codemap --refresh`

## Examples

### Example 1: Full Refresh
```
User: "Update the codemap"
Agent: Scans project → Generates CODEMAP.md → Reports summary
```

### Example 2: Diff Mode
```
User: "/codemap --diff"
Agent: Compares current CODEMAP.md against actual project state → Reports additions/removals/renames
```

### Example 3: Quick Reference
```
User: "/codemap"
Agent: Displays current CODEMAP.md contents (or generates if missing)
```

## Error Handling

- If `CODEMAP.md` doesn't exist and mode is `display`, automatically switch to `refresh`
- If git history is unavailable (new repo), skip the Hot Files section
- If the project is very large (>2000 files), increase summarization level and reduce depth
