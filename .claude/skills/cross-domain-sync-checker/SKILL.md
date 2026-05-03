---
name: cross-domain-sync-checker
description: >-
  SSoT 매핑 테이블과 Notion 정책·Figma 디자인·GitHub 코드·PRD 기획서에 대한 병렬 스캔으로 드리프트를 탐지하고,
  크로스 매트릭스로 상태/엣지/정책 정합성을 비교하며, 팀별 액션 아이템과 Slack 알림까지 제공. Use when the user
  asks to "check sync status", "cross-domain sync", "크로스체크", "싱크 확인", "기획 디자인
  개발 싱크", "도메인 간 싱크 확인", "정책-디자인-코드 싱크", "PRD vs 코드", "디자인 코드 싱크", "design-dev
  sync", "sync check", "cross-team sync", "SSoT 검증", "드리프트 감지", "산출물 정합성", "정책
  반영 확인", "싱크 점검", "디자인 코드 비교", "기획 구현 비교". Do NOT use for design-system
  changelog only (use design-system-tracker or tds-timeline). Do NOT use for
  document quality scoring only (use doc-quality-gate). Do NOT use for
  code-only review (use deep-review or code-reviewer). Do NOT use for reverse
  spec from code only (use code-to-spec).
---

# Cross-Domain Sync Checker

Unified sync verification across **policy (Notion)**, **design (Figma)**,
**code (GitHub / local)**, and **PRD / specs (Notion or files)**. Combines:

1. **SSoT mapping + parallel domain scans** — drift, staleness, cascade updates
2. **Cross-matrix comparison** — normalized elements across 2+ artifacts
3. **Six-axis gap analysis** — design ↔ code ↔ spec ↔ policy (when sources exist)
4. **Team action items + Slack alerts** — structured handoffs

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Configuration

| Key | Typical value |
|-----|----------------|
| Notion MCP | `plugin-notion-workspace-notion` or `user-Notion` |
| Figma MCP | `plugin-figma-figma` or `user-Figma` |
| GitHub MCP | `user-GitHub` |
| Slack MCP | `plugin-slack-slack` |
| Report path | `output/sync-reports/{date}-{feature-slug}/sync-report.md` |

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| `mode` | No | `ssot` \| `matrix` \| `full` (default: infer from inputs) |
| `--mapping` | For `ssot` / `full` | Path to mapping table or `auto` → default [references/ssot-mapping-schema.md](references/ssot-mapping-schema.md) |
| `--prd` | For `matrix` | Notion URL/ID or file path |
| `--design` | Optional | Figma URL |
| `--code` | Optional | Path, folder, or PR URL |
| `--policy` | Optional | Notion URL/ID or file path |
| `--spec` | Optional | Alias for PRD/planning doc (Notion/file) |
| `--focus` | No | `state` / `edge` / `policy` / `all` (default: `all`) |
| `--scope` | No | `full` / `feature` / `component` (for gap severity context) |
| `--notify` | No | Slack channel for summary + thread |
| `--no-notion` | No | Skip uploading report to Notion |

**Minimum:** either a valid **mapping** for SSoT mode, or **at least two** of
`--prd`, `--design`, `--code`, `--policy` / `--spec` for matrix mode.

### Figma-absent projects

When the project does not use Figma (no `--design` provided and no Figma MCP configured):

- Skip all Figma-related scan steps (Phase B1 Figma node fetch, Phase B2 design extraction).
- Omit design-axis columns from the sync matrix and six-axis gap table.
- Recalculate weighted scores with design weight redistributed proportionally to remaining axes.
- Note in the report header: "디자인 도구(Figma) 미사용 프로젝트 — 디자인 축 제외됨."
- Focus on **PRD ↔ code**, **PRD ↔ policy**, and **code ↔ policy** axes instead.

### Single-product simplified workflow

When the project is a single-product repository with file-based PRDs (`.md` specs in `docs/` or `specs/`) and no Notion/Figma integration:

1. **Skip SSoT mapping table** — treat each local `.md` spec file as the single source of truth for its domain.
2. **Reduce scan axes** to 3: PRD ↔ code, PRD ↔ policy, code ↔ policy.
3. **Use `git diff` for change detection** instead of Notion timestamp comparison.
4. **Simplify gap table** to a flat list: `| Spec file | Code path | Status | Gap description |`.
5. **Skip cross-team Slack notifications** — output the sync report as a local `.md` file only.
6. Auto-detect this mode when: no `--notion` flag, no `--design` flag, and `docs/**/*.md` or `specs/**/*.md` files exist in the repo.
7. Note in report header: "단일 제품 파일 기반 PRD 모드 — Notion/Figma 축 제외됨."

## Mode selection

| Mode | When to use |
|------|-------------|
| `ssot` | Maintain [references/ssot-mapping-schema.md](references/ssot-mapping-schema.md); parallel Notion/Figma/code scans; drift types + cascade |
| `matrix` | Explicit PRD/design/code/policy inputs; normalization [references/normalization-schema.md](references/normalization-schema.md); sync score |
| `full` | Run SSoT phases **and** matrix comparison when both mapping and artifact URLs are available |

## Workflow overview

```
Intake → (A) SSoT load/discover → (B) Parallel scans / artifact ingest
      → (C) Normalize → (D) Cross-matrix + six-axis gaps
      → (E) Drift + cascade (SSoT) → (F) Korean report + Notion + Slack
```

**Pattern:** Sequential overall; Phase B may fan out per source (max 4 parallel agents).

---

## Phase A: SSoT mapping

1. Load mapping table format from [references/ssot-mapping-schema.md](references/ssot-mapping-schema.md).
2. If missing: **discovery mode** — search Notion for policy/guide pages (use workspace keywords in Korean or English as appropriate), scan Figma file structure, scan repo tokens/components; propose rows; confirm with user.
3. Each row links **Concept → Policy / Design / Code** with **SSoT owner** and **Last Synced**.

---

## Phase B1: Parallel domain scan (SSoT)

For each mapped row:

- **Notion:** fetch page; extract modified time; hash key rules/constraints.
- **Figma:** fetch node/component; extract properties vs baseline.
- **Code / GitHub:** read mapped paths; extract values (tokens, props, copy).

---

## Phase B2: Artifact ingestion (matrix)

Minimum two sources. Extract comparable elements:

- **PRD/spec:** features, states, edge cases, flows, business rules
- **Design:** screens, variants, error/empty/loading, text layers
- **Code:** enums, branches, APIs, validation, errors
- **Policy:** mandatory rules, prohibitions, legal/consent, data rules

Use Notion/Figma/GitHub MCP tools as available; fall back to local reads.

---

## Phase C: Normalization

Convert to shared records per [references/normalization-schema.md](references/normalization-schema.md).

---

## Phase D: Cross-matrix and sync score

1. Join on `element_id` (or best-effort fuzzy match with confidence note).

| Verdict | Definition | Typical severity |
|---------|------------|------------------|
| Match | Aligned across sources | — |
| Partial | Wording differs, intent same | Low |
| Mismatch | Conflicting definitions | High |
| Missing | Present in some sources only | Medium–High |
| Extra | Implemented/planned beyond spec | Medium |

2. **Matrix template:** render a sync matrix table in Korean with columns for spec element, PRD, design, code, policy, and verdict.

3. **Weighted score (when matrix applies):**

| Dimension | Weight |
|-----------|--------|
| State sync | 30% |
| Edge-case sync | 25% |
| Business-rule sync | 25% |
| Policy reflection | 20% |

| Score | Label |
|-------|--------|
| 90–100% | SYNCED |
| 70–89% | DRIFT |
| 0–69% | MISALIGNED |

4. **Six-axis gap table** (only for axes with both ends): use
[references/artifact-comparison-criteria.md](references/artifact-comparison-criteria.md).

Severity for gaps: **CRITICAL** (behavior conflict), **HIGH** (UX/policy mismatch),
**MEDIUM** (minor inconsistency), **LOW** (documentation gap).

---

## Phase E: Drift detection and cascade (SSoT)

| Drift type | Detection | Severity |
|------------|-----------|----------|
| Value mismatch | Same concept, different values | High |
| Missing artifact | Concept in one domain only | Medium |
| Stale sync | Last synced old | Low |
| Unidirectional update | One domain changed, others not | High |
| Orphan | Mapped but missing live | Medium |

For each drift: identify **source of truth** from SSoT owner; outline **cascade**
(what to update in Policy / Design / Code / PRD).

---

## Phase F: Report, Notion, Slack

### Report sections

Deliver in Korean: executive summary (scope, drift/mismatch counts, SYNCED/DRIFT/MISALIGNED); SSoT drift detail by severity; sync matrix; per-axis gap summary; team action items (planning, design, development, policy/ops); recommended cascade order; updated mapping draft with last-synced timestamps.

### Slack

- **Parent:** Korean headline with feature/area, summary, score/label (per team format).
- **Thread:** Critical/High items + team action bullets.

### Notion

Publish via `md-to-notion` unless `--no-notion`.

---

## Skill chain

| Step | Skill / tool | Purpose |
|------|----------------|---------|
| 1 | Notion MCP | PRD, policy pages |
| 2 | Figma MCP | Components, tokens |
| 3 | GitHub / filesystem | Code |
| 4 | (self) | Matrix + drift |
| 5 | `doc-quality-gate` | Optional: validate updated docs |
| 6 | `spec-state-validator` | Optional: code vs spec after fixes |
| 7 | `md-to-notion` | Publish |
| 8 | Slack MCP | Notify |

---

## Examples

### Example 1: SSoT full scan

User: "Run policy–design–code sync check"

Actions: Load mapping → parallel scans → drifts + cascade → Korean report → Slack.

### Example 2: PRD vs code only

User: "Compare payment PRD to code" + URLs/paths

Actions: `matrix` mode → normalize → matrix → score → actions.

### Example 3: Four-way cross-check

User: PRD + Figma + code + policy.

Actions: `full` → matrix + six-axis + optional SSoT overlap → consolidated report.

---

## Error handling

| Issue | Action |
|-------|--------|
| Only one artifact source | Request at least one more or switch to SSoT-only with mapping |
| Mapping missing | Discovery mode; do not assume mappings without confirmation |
| MCP unavailable | Continue partial scan; label gaps in report |
| Mapped artifact deleted | Orphan row; suggest mapping cleanup |
| >50 drifts | Top 10 detail + grouped summary |
| No drifts | Report all clear (Korean message) + checked-at timestamp |
