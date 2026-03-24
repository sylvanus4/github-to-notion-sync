---
name: feature-coverage-matrix
description: >-
  Track feature implementation coverage across the pipeline: spec → design → code → tests.
  Scan Notion for specs, Figma for designs, Git for code, and test files for coverage;
  build a matrix of completion per feature per stage and highlight gaps.
  Korean triggers: "기능 커버리지", "feature coverage", "커버리지 매트릭스",
  "feature tracking", "구현 현황", "feature coverage matrix", "단계별 현황". Do NOT use for
  single-artifact code review (use code-reviewer), design QA only (use design-qa-checklist),
  or formal test plan execution (use pm-execution test scenarios).
metadata:
  author: thaki
  version: "1.0.0"
  category: tracking
---

# Feature Coverage Matrix

**All outputs MUST be in Korean (한국어). Technical terms may remain in English.**

## Purpose

Give planning and engineering a single sheet-style view of where each feature stands from idea to verification. Surfaces bottlenecks (designed but not built, built but untested).

## Prerequisites

- Notion database or list that defines **features** with stable IDs or slugs.
- Repository and test roots the user authorizes for search.
- Matching rules or examples mapping Notion titles to code paths (even heuristic).

## Success criteria

- Matrix has **no blank mystery rows**: each cell is a defined status or `Unknown` with reason.
- Bottlenecks name **one next action** (e.g., link design, add e2e file).
- Timestamp shows when Git/test signals were collected.

## Inputs

1. **Feature list** — Notion database filter, epic list, or explicit feature IDs/names.
2. **Sources** — Notion spec parent, Figma file/project, Git repo roots, test root paths (unit/e2e).
3. **Matching rules** — How features map across tools: naming convention, shared slug, Jira/Notion ID in branch names, etc.
4. **Time window** — Optional; limit Git/test signals to recent activity for delta reports.

## Procedure

1. **Ingest features** — Load rows from Notion MCP (name, status, owner, links to design/spec).
2. **Spec stage** — Mark `Present` if linked PRD/spec page exists and is non-empty; `Draft` if stub; `Missing` otherwise.
3. **Design stage** — `Linked` if Figma or Notion design URL on row; `Partial` if only wireframe; `Missing` if none. Use Figma MCP when available to confirm key frames exist.
4. **Code stage** — Search repo for feature slug, route segments, flags, or module names; classify `Not started` | `In progress` | `Shipped` using recent commits and main-branch presence.
5. **Test stage** — Grep test paths and titles for feature slug; classify `None` | `Partial` | `Adequate` using file count and critical-path hints (smoke vs deep).
6. **Score** — Optional RAG status per row: `Green` all stages ≥ threshold; `Yellow` one weak stage; `Red` any `Missing` critical stage.
7. **Synthesis** — Sort by risk: high user impact + weak test coverage first.
8. **Publish** — Korean matrix table with legend and bottleneck callouts.

### Workflow notes

- When a feature spans **multiple repos**, add a column or footnote per repo slice.
- Treat **feature flags** as code signals only when flag keys are discoverable from names or comments.
- For tests, prefer **e2e** titles for user journeys; unit tests alone may justify only `Partial`.

## Integrations

- **Notion MCP** — Read/update feature database; add a rollup property or comment with latest matrix link.
- **Figma MCP** — Verify design presence when links exist.
- **GitHub MCP** — Summarize recent PRs touching feature paths.
- **Slack MCP** — Weekly snapshot post with trend deltas if run periodically.
- **Google Workspace CLI (`gws`)** — Optional Sheets export via copy-paste friendly TSV in chat.

### Publishing checklist

1. Write the matrix to a Notion page or database rollup comment with link.
2. Slack weekly snapshot: delta since last run (optional second table).
3. Optional TSV block for Sheets import.

## Output Structure

- Legend for stage statuses and colors.
- Matrix: Feature | Spec | Design | Code | Tests | Overall | Notes.
- Bottleneck section: top five blocked features with suggested next action.
- Data freshness timestamp per source.

## Examples

- **Input:** "Matrix for all rows in Notion Features DB this quarter." **Output:** Korean table with 20 rows and 6 yellow items lacking tests.
- **Input:** "Where is onboarding stuck?" **Output:** Filtered matrix showing design done, code partial, tests missing.
- **Input:** "Coverage for Q1 epics only, tests in `e2e/`." **Output:** Filtered matrix with test stage from e2e filenames.

## Boundaries

- **Heuristic** code/test matching can misclassify; owners should confirm borderline rows.
- Does **not** measure **code coverage %** from Istanbul; tracks presence of meaningful tests by naming/path heuristics unless user supplies metrics.

## Error Handling

- **Alias mismatch** — List unmapped features; request slug alignment.
- **Private Figma** — Mark design stage `Unknown` with explanation.
- **Forked branches only** — Do not mark `Shipped` unless merged to agreed default branch.
- **Flaky test signal** — Treat test stage as `Partial` if only skipped or quarantined tests match.
- **Empty Notion filter** — Stop and ask for scope; do not invent features.
- **Monorepo noise** — Narrow with path prefixes from the user to keep signals meaningful.
