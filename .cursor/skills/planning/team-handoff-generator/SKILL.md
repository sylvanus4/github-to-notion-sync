---
name: team-handoff-generator
description: >-
  Generate structured handoff documents for cross-team transitions: planning→design,
  design→development, development→QA. Includes context, requirements checklist, design
  decisions, open questions, acceptance criteria, timeline, dependencies; formatted for
  Notion; Slack notify to receiving team.
  Korean triggers: "핸드오프", "인수인계", "팀 전달", "핸드오프 문서".
  English triggers: "handoff generator", "team handoff", "team-handoff-generator".
  Do NOT use for external vendor SOW (use legal/procurement workflows) or code-only README handoffs without planning context.
metadata:
  version: "1.0.1"
  category: generation
  author: thaki
---

# Team Handoff Generator

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Purpose

Produce a **paste-ready Notion page** (markdown structure) that **reduces rework** between phases: **planning → design**, **design → development**, or **development → QA**, and **ping the receiving team** on **Slack** with the essentials.

## Prerequisites

- **Handoff type** (one of the three above) and **feature or initiative name**.
- Source context: PRD links, Figma links, tech notes, open threads—provided by user.
- **Notion MCP** for page creation when parent page ID is supplied.
- **Slack MCP** for team channel notification.

## Standard sections (deliver section titles and body in Korean)

1. **One-line summary** — Outcome and handoff intent.
2. **Background and goals** — Problem, user value, success metrics.
3. **Requirements checklist** — Must-have vs nice-to-have with trace IDs to spec sections.
4. **Design decisions** — Tokens, patterns, exceptions (for design→dev); collapse N/A for other types.
5. **Open questions** — Suggested owner per item.
6. **Acceptance criteria** — Testable bullets.
7. **Timeline and milestones** — Dates or phases; highlight dependencies.
8. **Dependencies** — Other teams, APIs, data, legal/policy gates.
9. **Reference links** — Notion, Figma, repo, dashboards.
10. **Next actions** — What the receiving team should do within 48h.

## Procedure

1. **Classify handoff** — Confirm direction (planning→design, etc.) and **depth** (MVP vs full).

2. **Extract** — From user materials, pull decisions, constraints, and **non-goals**. Mark anything unclear as **open question** rather than guessing.

3. **Map roles** — Label **sending** and **receiving** teams (e.g. planning, design, development, QA). Do not fabricate individual names unless provided.

4. **Draft** — Fill the standard sections. Use **tables** for checklists when they improve scanability.

5. **Notion** — Create page via **Notion MCP** under the given parent; use title pattern aligned with workspace rules (Korean title per output rule).

6. **Slack** — Post Korean summary: handoff type, top 3 requirements, top 3 risks/questions, **Notion URL**, request acknowledgment in thread.

7. **Closure** — Return the full markdown body in chat for local backup and diff review.

## Notion MCP usage

- Prefer **create-page** with structured blocks; split long checklists into toggles if the workspace style prefers it.
- Link **related database items** (project, epic) when IDs are supplied.

## Slack MCP usage

- Channel message stays under ~8 lines; details in thread.
- Use emoji sparingly; one status emoji for urgency if the user wants (optional).

## Google Workspace CLI (`gws`)

- Optional: if the user requests a **Calendar** handoff meeting, create or propose a slot with attendees listed (user must confirm emails).

## Output structure

Deliver in Korean: complete Notion page body; Slack summary for copy-paste; short acknowledgment request for the receiving team.

## Error handling

- Missing Figma for design→dev → state **design assets pending** and list required screens.
- Conflicting requirements → surface **conflict table** with sources.

## Examples

- Planning→design: emphasize user journeys and metrics; design decisions section minimal.
- Dev→QA: emphasize test data, feature flags, known defects, regression scope.

## Guardrails

- Do not commit to delivery dates not present in source material.
- Flag **policy-sensitive** items for review with **policy-text-generator** or legal if indicated by user.

## Project-Specific Overrides (AI Stock Analytics)

This skill operates under project-specific policies:

- `.cursor/skills/references/project-overrides/project-ssot.md` (POL-005 — artifact locations, not-used systems)
- `.cursor/skills/references/project-overrides/project-document-standards.md` (POL-004 — quality gate, grading, report standards)

Key constraints:

- Cite POL-005 SSoT mapping for where PRDs, policies, and code live; handoffs should point to repo paths, not assumed Notion parents.
- Design references = `.cursor/rules/design-system.mdc` (no Figma handoff pack).
- Specs and requirements = local markdown (`docs/`, `tasks/`, etc.) unless the user explicitly provides external links.
