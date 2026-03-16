# Sync Target Projects

## Table of Contents

1. [Target Registry](#target-registry)
2. [Per-Project Notes](#per-project-notes)
3. [Managing Targets](#managing-targets)

## Target Registry

| Alias | Repo | Path (회사) | Path (집) |
|-------|------|-------------|-----------|
| `github-to-notion-sync` | `thakicloud/github-to-notion-sync` | `/Users/hanhyojung/work/thakicloud/github-to-notion-sync` | `/Users/hanhyojung/thaki/github-to-notion-sync` |
| `ai-platform-webui` | `thakicloud/ai-platform-webui` | `/Users/hanhyojung/work/thakicloud/ai-platform-webui` | `/Users/hanhyojung/thaki/ai-platform-webui` |
| `ai-model-event-stock-analytics` | `thakicloud/ai-model-event-stock-analytics` | `/Users/hanhyojung/work/thakicloud/ai-model-event-stock-analytics` | `/Users/hanhyojung/thaki/ai-model-event-stock-analytics` |
| `ai-template` | `thakicloud/ai-template` | `/Users/hanhyojung/work/thakicloud/ai-template` | `/Users/hanhyojung/thaki/ai-template` |

The alias is used with `--targets` flag: `/cursor-sync --targets ai-template`.
The repo identifier is used with `--repo` flag: `/cursor-sync --repo thakicloud/ai-template`.

**Path resolution**: Each target has two possible paths (회사/집). At runtime, try each path in order and use the first one that exists. If neither exists, skip the target with a warning.

## Per-Project Notes

### github-to-notion-sync

- Has 60+ commands (many shared with source)
- Project-specific rules: `ACT_GUIDE.mdc`, `PRD.mdc`
- No project-specific skills

### ai-platform-webui

- Has project-specific skills: `ux-expert`, `frontend-expert`, `e2e-testing`, `backend-expert`, `overlay-layout-patterns`, `notion-docs-sync`
- Has project-specific commands: `ux-review`, `test-plan`, `release-prep`, `full-quality-audit`, `feature-pipeline`
- Has nested `.cursor/` in `ai-platform/backend/go/` (not affected by sync)

### ai-model-event-stock-analytics

- Has project-specific skills: `stock-csv-downloader`, `daily-stock-check`, `weekly-stock-update`
- Has project-specific commands: `weekly-stock-update`, `daily-stock-check`, `stock-csv-download`, `dev-start`, `dev-stop`, `dev-status`
- Has many sp-* (skill-pipeline) skills and commands

### ai-template

- Template repository — intended to have the most complete set of shared assets
- Has project-specific skills: `kwp-sync`, `i18n-sync`
- Has domain-specific rules: `sales.mdc`, `product-management.mdc`, `marketing.mdc`, etc.

## Extra Sync Directories

Beyond `.cursor/{commands,skills,rules}`, additional directories can be synced with per-target path mappings.

| Scope Key | Source Path (this repo) | Target Alias | Target Path | Direction |
|-----------|------------------------|--------------|-------------|-----------|
| `skill-guides` | `docs/skill-guides/` | `ai-template` | `skill-guides/` | bidirectional |
| `skill-guides` | `docs/skill-guides/` | `ai-platform-webui` | `docs/skill-guides/` | bidirectional |

**Bidirectional sync**: push (source → target) first, then pull (target → source). Both directions run without `--delete`, so files unique to either side are preserved.

## Managing Targets

### Adding a new target

1. Add a row to the Target Registry table above (include the `Repo` column with the `org/repo` identifier)
2. Ensure the project directory exists with a `.cursor/` subdirectory
3. Run `/cursor-sync --targets <alias> --dry-run` or `/cursor-sync --repo <org/repo> --dry-run` to preview

### Removing a target

1. Remove the row from the Target Registry table
2. Files already synced to the target remain (no cleanup needed)
