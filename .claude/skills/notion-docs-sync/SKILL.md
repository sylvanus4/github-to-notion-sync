---
name: notion-docs-sync
description: >-
  Markdown 문서를 Notion 페이지/DB에 동기화합니다. Notion 동기화, .notion-sync.yaml 설정, 문서를
  Notion에 올려줘, Notion 연동, 문서 동기화 요청 시 사용합니다. Do NOT use for 화면 기획서
  작성(screen-description), GitHub 이슈/PR 관리(github-workflow-automation).
disable-model-invocation: true
---

# Notion document sync

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Prerequisites

If the project has no `.notion-sync.yaml`, confirm the target folder with the user (default: repo root), then run `init.sh`:

```bash
SKILL_DIR/scripts/init.sh <target-dir>
```

Why `init.sh` matters:

- Copies the `.notion-sync.yaml` template and `NOTION-SYNC.md` (Notion authoring constraints) into the project. Without them the agent cannot follow sync config and writing rules.
- Creates `spec/` and `guide/` (or equivalent) so markdown has a home.
- Runs `npm install` once for sync script dependencies; without it `sync.mjs` fails.

Requirements: Node.js 18+.

`sync.mjs` stays under the skill directory (not copied into the project). Paths in `.notion-sync.yaml` are relative to the YAML file location.

## Sync behavior

- Sync markdown under `docs/` (or paths declared in YAML) to Notion via `sync.mjs`.
- Metadata lives in `.notion-sync.yaml`.
- Each run typically clears page body (`erase_content`) then re-adds blocks.
- Two modes:
  - **`databases`** — Rows in a Notion database. Find or create by `Sync ID`.
  - **`pages`** — Standalone pages. Target by `page_id`.

### `.notion-sync.yaml` shape

```yaml
databases:
  - database_id: "<Notion DB ID>"
    pages:
      - file: spec/api-design.md
        title: "API design guidelines"
        Sync ID: spec-api-design
        Parent: ""

pages:
  - file: guide/quickstart.md
    page_id: "<Notion Page ID>"
```

Fields:

- `file` — Path relative to the doc root configured in YAML (often `docs/`).
- `title` — Notion page title (required); updated on sync.
- `Sync ID` — Stable key, e.g. `spec-api-design`, `guide-setup`.
- `Parent` — Parent row’s `Sync ID`; empty string = top level.
- `page_id` — For `pages` mode only.

Sample: [templates/.notion-sync.yaml](templates/.notion-sync.yaml)

### Run sync

`SKILL_DIR` = this skill’s directory.

Requires `NOTION_TOKEN`. If unset, ask the user for an integration token.

```bash
# Full sync (when CWD contains .notion-sync.yaml)
node SKILL_DIR/scripts/sync.mjs

# Explicit YAML path
node SKILL_DIR/scripts/sync.mjs path/to/.notion-sync.yaml

# Specific files only
node SKILL_DIR/scripts/sync.mjs .notion-sync.yaml spec/api-design.md guide/setup.md
```

### Database schema minimum

The Notion database needs:

- One **title** property (name auto-detected).
- `Sync ID` — rich_text.
- `Parent` — self-referential relation.

Extra columns in YAML are mapped when types are supported: rich_text, select, multi_select, number, checkbox, people, relation, date, url, email, phone_number.

## Authoring rules

After `init.sh`, follow `NOTION-SYNC.md` in the project for folder layout, headings, filenames, body rules, and attachments.

## Examples

### Example 1: First-time setup + full sync

User: "Sync this project’s docs to Notion"

1. Ensure `.notion-sync.yaml` exists → else run `init.sh`.
2. Collect `NOTION_TOKEN` and database ID from the user.
3. Register files in `.notion-sync.yaml`.
4. Run `node SKILL_DIR/scripts/sync.mjs`.

### Example 2: One doc only

User: "Upload only the API design doc"

1. Confirm path in YAML (e.g. `spec/api-design.md`).
2. `node SKILL_DIR/scripts/sync.mjs .notion-sync.yaml spec/api-design.md`

## Troubleshooting

### `MODULE_NOT_FOUND` running `sync.mjs`

Cause: dependencies not installed.
Fix: `SKILL_DIR/scripts/init.sh <target-dir>`, retry.

### Notion API 401

Cause: missing or expired `NOTION_TOKEN`.
Fix: Rotate token in Notion integration settings, `export NOTION_TOKEN=...`.
