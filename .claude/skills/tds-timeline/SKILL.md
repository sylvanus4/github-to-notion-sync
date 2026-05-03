---
name: tds-timeline
description: >-
  GitHub 커밋 이력 기반으로 TDS(Thaki Design System) 컴포넌트 변경 타임라인을 생성하고 정기 리포트를 발행한다.
  누가, 언제, 어떤 컴포넌트를, 어떤 의도로 수정했는지 타임라인 형태로 시각화하여 Notion·Slack에 공유한다. Use when
  the user asks to "TDS 변경 이력", "디자인 시스템 타임라인", "컴포넌트 변경 추적", "TDS changelog",
  "디자인 시스템 변경 리포트", "tds-timeline", "TDS 리포트", "디자인 시스템 히스토리", "컴포넌트 수정 내역",
  "TDS 주간 리포트", "디자인 변경 타임라인", or any request to track and visualize design
  system component changes over time. Do NOT use for code-level PR review (use
  deep-review or code-reviewer). Do NOT use for general git log viewing (use
  Shell directly). Do NOT use for design token generation (use
  visual-explainer). Korean triggers: "TDS 타임라인", "디자인 시스템 이력", "컴포넌트 변경 추적",
  "TDS 변경 리포트", "디자인 시스템 변경 내역".
---

# TDS Timeline

Build a component change timeline from GitHub commit history for design, planning, and engineering visibility. Works with any component-based frontend — TDS (`@thakicloud/shared`), Radix + Tailwind, shadcn/ui, or custom component libraries.

## Scope adaptation

| Project type | `--path` default | Component detection |
|---|---|---|
| TDS (`@thakicloud/shared`) | `src/shared/ui/` or `packages/shared/` | TDS component registry |
| Radix + Tailwind (e.g. `ai-model-event-stock-analytics`) | `frontend/src/components/` | Directory-based (1st child = component name) |
| shadcn/ui | `src/components/ui/` | File-based (each `.tsx` = component) |
| Custom | User-specified | Directory or file-based |

When the project does **not** use `@thakicloud/shared`, omit TDS-specific token/design-system language in the output and use generic "component change timeline" framing.

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Input

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--repo` | Yes | — | GitHub repo (`owner/repo`) |
| `--path` | No | `src/components/` | Root path for TDS components |
| `--since` | No | 7 days ago | Start date (`YYYY-MM-DD`) |
| `--until` | No | today | End date (`YYYY-MM-DD`) |
| `--authors` | No | all | Comma-separated author filter |
| `--output` | No | `markdown` | `markdown`, `notion`, `slack`, `html` |
| `--group-by` | No | `component` | `component`, `author`, `date` |
| `--parent` | No | — | Notion parent page ID (required for `notion`) |
| `--channel` | No | — | Slack channel ID (required for `slack`) |

## Workflow

```
Phase 1: Collect  → Commits via GitHub MCP
Phase 2: Classify → Per-component change typing + intent
Phase 3: Render   → Timeline markdown (Korean summaries in deliverables)
Phase 4: Deliver  → Notion / Slack / file / HTML
```

### Phase 1: Collect

1. `list_commits` for the window
2. `get_commit` per SHA with diffs when needed
3. Keep files under `--path`; derive component names from paths (e.g. `.../Button/Button.tsx` → `Button`)
4. Apply date and author filters

### Phase 2: Classify

**Change types**:

| Type | Rule |
|------|------|
| `new` | File added |
| `change` | File modified |
| `remove` | File deleted |
| `refactor` | Message/diff signals refactor |
| `style` | Style-only edits |
| `a11y` | Accessibility-related keywords |

**Intent line**: One-line **Korean** summary for stakeholders (per output rule).
Details: [references/classification-rules.md](references/classification-rules.md).

### Phase 3: Render

Group by `--group-by`. Render tables and summaries in Korean (date, author, change type, one-line description, rollup stats).

### Phase 4: Deliver

- **`markdown`**: `outputs/tds-timeline/tds-timeline-YYYY-MM-DD.md`
- **`notion`**: `md-to-notion` / Notion MCP create-pages pattern with `--parent`
- **`slack`**: Main post + thread details (Korean)
- **`html`**: `visual-explainer`-style standalone HTML

## Periodic reports (`--schedule`)

| Cadence | Window |
|---------|--------|
| `weekly` | Last 7 days (e.g. Monday run) |
| `biweekly` | Last 14 days |
| `monthly` | Last 30 days |

Default: publish to Notion + Slack together.

## Examples

```
/tds-timeline --repo org/design-system --since 2026-03-17 --output notion --parent <page-id>
/tds-timeline --repo org/design-system --authors designer-a --group-by date
/tds-timeline --repo org/design-system --output slack --channel C0123...
/tds-timeline --repo org/design-system --output html --group-by component
```

## Error handling

| Issue | Resolution |
|-------|------------|
| No repo access | Verify auth (`get_me`) |
| Empty `--path` | Warn; suggest repo layout |
| >100 commits | Paginate (cap e.g. 5 pages) |
| Missing Notion parent / Slack channel | Require IDs |
| No changes in range | Return “no TDS changes” message |
| Empty commit message | Infer from diff |
| Rate limit | Backoff and retry |
