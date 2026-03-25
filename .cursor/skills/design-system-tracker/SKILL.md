---
name: design-system-tracker
description: >-
  Figma·코드·Git 기반 디자인 시스템 변경을 감지하고, 체인지로그·영향 분석·Notion 기록·Slack 알림까지 수행한다.
  Code Connect 매핑 커버리지를 추적하고 search_design_system으로 퍼블리시된 DS 인벤토리를 조회한다.
  Use when the user asks to "track design system changes", "디자인 시스템 변경 추적", "디자인 변경 추적",
  "디자인 시스템 변경 이력", "디자인 토큰 변경", "컴포넌트 변경 이력", "디자인 변경 감지",
  "design system changelog", "design token tracking", "component changelog", "Figma 변경 이력",
  "디자인 체인지로그", "컴포넌트 변경 영향 분석", "design change", "track design change",
  "디자인 시스템 싱크", "디자인 변경 영향 분석", "Code Connect 커버리지", "코드 커넥트 추적",
  or needs end-to-end DS evolution tracking.
  Do NOT use for implementing tokens in code (use figma-dev-pipeline).
  Do NOT use for casual Figma browsing without tracking intent (use Figma MCP only).
  Do NOT use for creating new design components (manual design work).
  Do NOT use for code-only refactors with no design implications (use code-reviewer).
  Do NOT use for Code Connect mapping setup (use figma-code-connect-components plugin skill via figma-dev-pipeline).
metadata:
  author: thaki
  version: "2.1.0"
  category: tracking
---

# Design System Tracker

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

Unified skill for **change detection**, **structured changelogs**, **impact analysis**, **Notion logging**, and **Slack notifications** across Figma, local code, and Git history.

## Configuration

| Key | Value |
|-----|-------|
| Figma MCP | `plugin-figma-figma` (or `user-Figma` per workspace) |
| Notion MCP | `plugin-notion-workspace-notion` |
| Slack MCP | `plugin-slack-slack` |
| Default output dir | `output/design-system/` |

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| `<source>` | Yes | Figma URL, component name, git range (`HEAD~N`, paths), or free-text change description |
| `--scope` | No | `all` \| `tokens` \| `components` \| comma-separated names |
| `--type` | No | `token` \| `component` \| `pattern` \| `layout` (default: auto) |
| `--baseline` | No | Prior snapshot date, commit SHA, or `latest` for last known state |
| `--severity` | No | `breaking` \| `major` \| `minor` \| `patch` (default: auto via references) |
| `--notion-parent` | No | Notion parent page or DB for history entries |
| `--notify` | No | Slack channel IDs (comma-separated); omit with `--no-notify` |
| `--no-notify` | No | Skip Slack |

## Source mode detection

| Mode | Detect | Action |
|------|--------|--------|
| **Figma URL** | `figma.com` in input | Figma MCP: file/component data |
| **Component name** | PascalCase token, no spaces (e.g. `Button`) | Ripgrep codebase for imports/usages |
| **Git diff** | Paths or revision range | Diff design-touched files only |
| **Plain text** | Else | Parse user description into structured change list |

**Design-touched file patterns (Git / code):** `*.css`, `*.scss`, `tailwind.config.*`, `tokens.*`, `**/components/**`, `**/ui/**`, `*theme*`, `*design-system*`.

## Workflow (sequential)

```
Phase 1  Collect & classify   → current state + change type
Phase 2  Diff / detect       → vs baseline snapshot (or establish first snapshot)
Phase 3  Impact analysis     → code, screens, docs, policy, teams
Phase 4  Changelog           → Keep a Changelog + Korean DS history template
Phase 5  Publish             → Notion + Slack + new baseline snapshot
```

### Phase 1 — Change detection & classification

- **Figma (DS-aware discovery)**: Use `search_design_system` with `includeComponents: true`, `includeVariables: true`, `includeStyles: true` to get the authoritative published DS inventory from linked Figma libraries. This replaces generic `get_figma_data` / `get_file` calls for DS-level tracking and provides the canonical list of components, variables, and styles.
- **Figma (file-level)**: For changes in specific files (not library-level), use `get_design_context` / `get_metadata` per frame/node.
- **Code / Git**: filter diffs to design paths; map edits to tokens/components.
- **Code Connect audit**: Call `get_code_connect_suggestions` to identify which published DS components have Code Connect mappings and which don't. Track Code Connect coverage as a dimension alongside token/component changes. (Requires Org/Enterprise plan; skip if unavailable.)
- **Classification** (default severity hints): see [references/change-categories.md](references/change-categories.md) and [references/breaking-change-criteria.md](references/breaking-change-criteria.md).

Snapshot structure: [references/design-token-schema.md](references/design-token-schema.md).

### Phase 2 — Diff against baseline

Compare current extract to baseline:

| Bucket | Meaning |
|--------|---------|
| Added | New components, tokens, variants |
| Modified | Value/structure/name changes |
| Removed | Gone from baseline |
| Renamed | >~80% structural match, different name (flag confidence) |

Changelog-style severity: **Breaking** / **Visual** / **Additive** / **Internal** (see changelog skill legacy behavior — Breaking = removed/renamed API, Visual = value changes, etc.).

If **no baseline**: save current state as baseline; report initial snapshot only (Korean copy in deliverable).

### Phase 3 — Impact analysis

Use [references/change-impact-matrix.md](references/change-impact-matrix.md), [references/component-taxonomy.md](references/component-taxonomy.md), and team matrix:

- Direct/indirect code usage (grep + composition).
- Screen / feature mapping table.
- Doc & policy touchpoints (brand, a11y).
- Team actions: planning / design / development / QA (localized labels in Korean output).
- **Code Connect breakage detection**: When code components are renamed, moved, or deleted, flag potential Code Connect mapping breakage. Cross-reference `get_code_connect_suggestions` results against the changed components.

If PRD provided: run [references/review-checklist.md](references/review-checklist.md).

### Phase 4 — Changelog generation

Produce **both**:

1. **Keep a Changelog**-style block (Breaking / Visual / Additions / Internal) for engineering & design ops.
2. **Korean change history** for stakeholders: include summary (date, type, impact, author), before/after detail, affected screens/components matrix, migration guide when needed, and links (Figma, PR, policy). Use Korean headings per output rule.

**Code Connect coverage report** (appended to changelog when available):
- Total published DS components (from `search_design_system`).
- Components with Code Connect mappings vs without.
- Code Connect coverage % (mapped / total).
- Newly broken mappings (from Phase 3 breakage detection).

### Phase 5 — Publish & notify

- **Notion**: create child page or DB row; title pattern per team convention (Korean category + artifact + date).
- **Slack**: parent message (severity + counts + Code Connect coverage %) + threads (detail + team action items).
- **Baseline**: store new snapshot path or commit note under `output/design-system/snapshots/` (or team convention).

**Large files (>500 components):** batch by 100; report progress. **Rate limits:** backoff and retry.

### GitHub / component-level tracking

- For **history without Figma**: `git log --follow` on token/component paths; attribute by commit message and touched files.
- Cross-link commits to changelog entries (SHA, author, date).
- Optional: align with repo practices (e.g. Conventional Commits for `fix(ui):` / `feat(ds):`).

## References (progressive disclosure)

| Topic | File |
|-------|------|
| Token snapshot & diff schema | [references/design-token-schema.md](references/design-token-schema.md) |
| Change taxonomy & escalation | [references/change-categories.md](references/change-categories.md) |
| Breaking vs non-breaking | [references/breaking-change-criteria.md](references/breaking-change-criteria.md) |
| Component & token categories | [references/component-taxonomy.md](references/component-taxonomy.md) |
| Impact matrices | [references/change-impact-matrix.md](references/change-impact-matrix.md) |
| PRD ↔ DS review | [references/review-checklist.md](references/review-checklist.md) |
| Figma automation limits | [references/figma-automation-boundaries.md](references/figma-automation-boundaries.md) |

## Skill chain

| Step | Skill / tool | Role |
|------|--------------|------|
| DS inventory | `search_design_system` (Figma MCP) | Authoritative published component/variable/style list |
| Code Connect audit | `get_code_connect_suggestions` (Figma MCP) | Map coverage tracking (Org/Enterprise) |
| Publish MD | `md-to-notion` | Long-form changelog pages |
| Canvas | `md-to-slack-canvas` | Slack Canvas optional |
| Post-breaking | `cross-domain-sync-checker` | SSoT drift check |
| Doc quality | `doc-quality-gate` | If linked specs must be revalidated |
| Code Connect setup | `figma-code-connect-components` (plugin) | When new mappings needed |

## Examples

**Example 1 — Figma component change**  
User shares Button Figma URL → MCP fetch → grep `Button` usages → impact matrix → Notion + Slack.

**Example 2 — Token / primary color**  
User asks primary color impact → search `brand-600`, theme files → migration notes in Korean.

**Example 3 — Weekly DS scan**  
Scan library vs last week snapshot → counts of breaking/visual/additive → changelog + `#design-system` post.

## Error handling

| Error | Recovery |
|-------|----------|
| Figma MCP auth | Run `mcp_auth`; stop until connected |
| File/node not found | Verify URL and permissions |
| Component not in code | Confirm naming; suggest similar symbols |
| No baseline | First-snapshot mode |
| Notion failure | Save markdown locally; report error |
| Slack failure | Verify channel IDs; deliver local artifact |
| Rename uncertainty | Mark "possible rename" + confidence; ask user |
| Code Connect unavailable | Skip coverage tracking; note plan limitation in report |
| `search_design_system` empty | No published libraries; fall back to file-level MCP + Git heuristics |
