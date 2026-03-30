# Sync Target Projects

## Table of Contents

1. [Target Registry](#target-registry)
2. [Skill Group Whitelist](#skill-group-whitelist)
3. [Per-Project Notes](#per-project-notes)
4. [Managing Targets](#managing-targets)

## Target Registry

| Alias | Repo | Full Path | Bidirectional |
|-------|------|-----------|---------------|
| `github-to-notion-sync` | `thakicloud/github-to-notion-sync` | `/Users/hanhyojung/thaki/github-to-notion-sync` | **yes** |
| `ai-platform-webui` | `thakicloud/ai-platform-webui` | `/Users/hanhyojung/thaki/ai-platform-webui` | **yes** |
| `ai-model-event-stock-analytics` | `thakicloud/ai-model-event-stock-analytics` | `/Users/hanhyojung/thaki/ai-model-event-stock-analytics` | **yes** |
| `ai-template` | `thakicloud/ai-template` | `/Users/hanhyojung/thaki/ai-template` | **yes** |

The alias is used with `--targets` flag: `/cursor-sync --targets ai-template`.
The repo identifier is used with `--repo` flag: `/cursor-sync --repo thakicloud/ai-template`.

## Skill Group Whitelist

Skills are organized into subdirectories under `.cursor/skills/`. During push, only the whitelisted groups are synced to each target. `all` means every group is included.

| Alias | Skill Groups |
|-------|-------------|
| `ai-model-event-stock-analytics` | `all` |
| `ai-platform-webui` | `review`, `infra`, `frontend`, `workflow`, `ce`, `ecc`, `anthropic`, `standalone` |
| `github-to-notion-sync` | `gws`, `nlm`, `pipeline`, `workflow`, `anthropic`, `standalone` |
| `ai-template` | `workflow`, `anthropic`, `ce`, `ecc`, `standalone` |

### Available Skill Groups (23 total)

| Group | Description | Skill Count |
|-------|------------|-------------|
| `trading` | Stock analysis, Toss Securities, MiroFish, screener tabs | 66 |
| `agency` | AI specialist agent personas | 69 |
| `kwp` | Anthropic Knowledge Work Plugins | 95 |
| `planning` | PRD, spec, policy, planning docs | 35 |
| `automation` | Autoskill, skill management, setup, sync | 34 |
| `pipeline` | Daily orchestrators, morning/EOD, meeting, portfolio | 33 |
| `review` | Code review, testing, shipping, CI | 31 |
| `frontend` | FSD, Figma, design, screen implementation | 21 |
| `hf` | HuggingFace Hub operations (customized) | 15 |
| `infra` | Helm, Terraform, K8s, SRE, IaC | 15 |
| `ce` | Context Engineering theory/methodology | 15 |
| `gws` | Google Workspace (Gmail, Calendar, Drive, Sheets) | 14 |
| `role` | Cross-role perspective analysis (CEO, CTO, PM, etc.) | 14 |
| `nlm` | NotebookLM notebooks, slides, video, research | 11 |
| `ecc` | Everything Claude Code patterns | 10 |
| `workflow` | Workflow patterns, orchestration, planning | 10 |
| `alphaear` | AlphaEar financial intelligence suite | 9 |
| `pm` | PM skills (phuryn-based) | 9 |
| `research` | Paper review, auto-research, paper archive | 9 |
| `anthropic` | Document tools (DOCX, PPTX, PDF, templates) | 7 |
| `notion` | Notion publishing, sync, templates | 7 |
| `omc` | Oh-My-ClaudeCode skills | 5 |
| `standalone` | Miscellaneous skills without a clear group | 50 |

### Rationale for Per-Repo Selection

- **ai-model-event-stock-analytics**: Main project — needs every group
- **ai-platform-webui**: K8s platform — needs review (code quality), infra (Helm/K8s), frontend (React/FSD), workflow (orchestration), ce/ecc (agent patterns), anthropic (doc generation), standalone (utilities)
- **github-to-notion-sync**: Notion automation — needs gws (Google Workspace), nlm (NotebookLM), pipeline (orchestration), workflow (patterns), anthropic (doc generation), standalone (utilities)
- **ai-template**: Template repo — needs only generic, project-agnostic groups: workflow, anthropic, ce, ecc, standalone

### Overriding at Runtime

Use `--skill-groups` to override the whitelist for a specific run:

```bash
/cursor-sync --targets ai-platform-webui --skill-groups review,infra,trading
```

Use `--all-skills` to push all groups regardless of whitelist:

```bash
/cursor-sync --all-skills
```

**Bidirectional = yes** means the target is also treated as a pull source during `cursor-sync`. Research pulls new/updated assets from ALL targets first (newest-wins via `-u` flag), then pushes the merged result back to all targets. This keeps research as the canonical merge hub: any change in any of the 5 repos eventually reaches every other repo in one `/cursor-sync` run.

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

## Managing Targets

### Adding a new target

1. Add a row to the Target Registry table above (include the `Repo` column with the `org/repo` identifier)
2. Set `Bidirectional` to `yes` if research should also pull from this project, `no` otherwise
3. Add a row to the Skill Group Whitelist table with the relevant groups (or `all`)
4. Ensure the project directory exists with a `.cursor/` subdirectory
5. Run `/cursor-sync --targets <alias> --dry-run` or `/cursor-sync --repo <org/repo> --dry-run` to preview

### Removing a target

1. Remove the row from the Target Registry table
2. Remove the row from the Skill Group Whitelist table
3. Files already synced to the target remain (no cleanup needed)

### Making a target bidirectional

1. Change the `Bidirectional` column value to `yes`
2. Research will pull from that project at the start of every `cursor-sync` run
3. Any skills/rules in the target but not in research will be merged into research before the outbound push

### Updating skill group whitelist

1. Edit the Skill Group Whitelist table to add/remove groups for a target
2. New groups will be synced on next `/cursor-sync` run
3. Removed groups will NOT be deleted from the target (no `--delete` flag) — they simply stop receiving updates
4. To add a new skill group, create the subdirectory under `.cursor/skills/` and add it to the Available Skill Groups table
