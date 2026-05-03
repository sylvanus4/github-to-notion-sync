---
name: notion-template-library
description: >-
  Manage standardized Notion page templates for PRDs, policies, meetings,
  design specs, and retrospectives: select templates, apply structure to new
  pages, track template versions, and keep planning document shapes consistent
  via Notion MCP. Korean triggers: "노션 템플릿", "템플릿 적용", "문서 템플릿", "표준 템플릿".
  English triggers: "notion template", "notion template library", "apply
  template", "standard planning template Notion". Do NOT use for bulk markdown
  repo sync (use notion-docs-sync), meeting content analysis (use
  meeting-digest), or arbitrary database schema migrations without user
  approval.
---

# Notion Template Library

**All outputs MUST be in Korean (한국어). Technical terms may remain in English.**

## Purpose

Operate a **catalog of Notion templates** for planning artifacts, **apply** them when creating pages, and **track versions** so teams do not drift across PRDs, policies, meetings, design specs, and retros.

## Prerequisites

- **Notion MCP** with permission to duplicate/create pages under agreed parents.
- Canonical **template pages** in Notion (one per doc type) or user-provided template IDs.

## Procedure

1. **Catalog** — Maintain a logical registry (in the agent response or a user-managed Notion DB) with columns: `template_key`, `title`, `notion_url`, `version`, `owner`, `intended_use`, `last_reviewed`.

2. **Template keys (defaults)** — `prd`, `policy`, `meeting_notes`, `design_spec`, `retro`, `decision_log`. Map each to a **source template page** in Notion.

3. **Apply template** — For a new document request:
   - Resolve `template_key` from user intent
   - Use **Notion MCP** to **duplicate** the template page under the target parent, or create page and **insert** structured blocks matching the template outline
   - Set title per team convention (category + document name + `YYYY-MM-DD`) **in Korean** when requested

4. **Populate placeholders** — Replace `{{owner}}`, `{{feature}}`, `{{date}}`, etc., with user-supplied values; list any **unfilled** placeholders explicitly in Korean.

5. **Version control** — When template structure changes:
   - Bump `version` (semver)
   - Append **changelog** bullet list (what sections added/removed)
   - Notify via **Slack MCP** (short summary + Notion template link)

6. **Consistency audit** — Sample recent child pages: verify required headings exist; report drift score as low / medium / high **using Korean labels** in the output with fix suggestions (do not mass-edit without confirmation).

7. **Optional calendar hook** — For meeting templates, pull today’s events with **`gws` calendar** to pre-fill time/attendees fields when user opts in.

8. **Access model** — Confirm parent page permissions so the duplicated page is visible to intended teams; if uncertain, note permissions need verification **in Korean** in the output.

## Notion MCP operations

- **Duplicate template page** under the target parent when the template is a full page with formatting the team wants preserved.
- **Create from outline** when templates are simple: insert heading blocks (H1–H3), to-do blocks, and callouts mirroring the standard structure.
- Record returned **page URL** and **page id** in the Korean summary for traceability.

## Template versioning rules

- **Patch**: wording, examples, non-structural tweaks.
- **Minor**: new required sections, new properties in related DBs (if applicable).
- **Major**: renamed core sections that break downstream automations or review rubrics.

## Slack MCP announcements

- Notify on **major** and **minor** template updates; optional for **patch** unless user requests always-on notices.
- Include: template key, old→new version, Notion template URL, effective date.

## Output structure (sections must be written in Korean)

1. Selected template and version
2. Created Notion page URL
3. Filled fields vs remaining placeholders
4. If auditing: drift summary and recommended fixes

## Examples

- **New PRD** — Duplicate `prd` template → fill problem, goals, metrics sections → link related decision log.

- **Retro** — Duplicate `retro` template → pre-fill attendees from calendar when opted in → leave action items as unchecked todos.

## Quality checklist

- Template key is explicit; no silent defaults when ambiguity exists.
- Placeholders are visible and tracked until cleared.
- Changelog entries are **specific** (which section changed).

## Error handling

- **Template not found**: List available keys; ask user to pick or supply URL.
- **MCP duplicate fails**: Fall back to manual checklist: paste section headings for user to copy.
- **Permission denied**: Output exact failure; suggest workspace admin + integration scopes.
- **Ambiguous doc type**: Ask one question; default to `prd` only if user explicitly allows.
