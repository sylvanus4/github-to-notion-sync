---
name: weekly-planning-digest
description: >-
  Weekly digest of planning team activities: aggregate Notion project DB
  changes, completed and in-progress work, new blockers, key decisions,
  upcoming deadlines; compare to prior week for trends; publish to Slack and
  Notion archive; optional PPTX summary via anthropic-pptx orchestration.
  Korean triggers: "주간 기획 다이제스트", "기획팀 주간 보고", "주간 정리". English triggers:
  "weekly planning digest", "planning weekly", "weekly-planning-digest". Do
  NOT use for company-wide executive rollups (use executive-briefing) or
  GitHub-only sprint digests (use github-sprint-digest).
---

# Weekly Planning Digest

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Purpose

Summarize **one week** of **planning-team** motion: what moved, what stalled, what was decided, and what is due soon—then **publish** to **Slack** and a **Notion archive** page, with optional **PPTX** for stakeholder readouts.

## Prerequisites

- **Week boundaries** (timezone-aware Monday–Sunday or org standard).
- **Notion MCP**: project and/or task databases; optional decision log.
- **Slack MCP**: target channel for the digest.
- Prior week digest page URL or pasted summary for **trend compare** (if unavailable, note **no baseline**).

## Procedure

1. **Frame** — Confirm date range, databases, Slack channel, and whether to include **PPTX**.

2. **Notion: completed** — Query items moved to Done/Closed in the window. Capture title, project, owner.

3. **Notion: in progress** — Query active statuses; group by project or pillar. Highlight **age** if “in progress” exceeded N days (N from user or default 14).

4. **Notion: blockers** — New or updated blocker flags, comments, or status notes. Deduplicate by work item.

5. **Notion: decisions** — Pull from Decision Log or meeting pages if integrated; else infer from comment deltas only with a **low confidence** label (Korean phrasing in the deliverable).

6. **Deadlines** — Next-week and two-week horizon due dates from task properties.

7. **Trends** — Compare counts vs prior week: completed (↑/↓), new blockers, WIP. Narrate in Korean without inventing causes.

8. **Draft digest** — Sections: Highlights, Shipped, In flight, Blockers & risks, Decisions, Upcoming deadlines, Data gaps.

9. **Notion publish** — Create archive child page: `[Digest] Planning weekly — YYYY-MM-DD` via **Notion MCP**; link prior digest.

10. **Slack publish** — Post Korean executive summary; thread with bullet details and Notion link.

11. **PPTX (optional)** — If requested, use **anthropic-pptx** skill: agenda slide, metric slides, risks slide, next week slide. Attach file path in the final Korean delivery note.

## Notion MCP usage

- Use `database-query` with **created time** and **last edited time** filters where schema supports it.
- If only manual status changes exist, rely on **edited_time** and verify with titles.

## Slack MCP usage

- Main: 5–7 lines max.
- Thread: tables as monospace or bullet lists; include **Notion** URL first in thread.

## Google Workspace CLI (`gws`)

- Optional: summarize **Calendar** planning meetings held in the week (titles + outcomes) via `gws` calendar commands when authenticated.

## Output structure

Deliver in Korean: week-at-a-glance (3 bullets); shipped items; in-flight by project; new/persistent blockers; decisions; upcoming deadlines; week-over-week deltas when measurable; data limitations.

## Error handling

- Missing database permissions → output **partial digest** with explicit gaps.
- No prior week baseline → omit comparison section or mark comparison unavailable (Korean label in deliverable).

## Examples

- Blockers doubled week-over-week → call out **risk trend** and suggest review meeting (no automatic scheduling unless asked).

## Guardrails

- Do not disclose confidential names or customer data in Slack; use roles if sensitivity is unknown.
- Numeric claims must tie to **query results** or be qualified as estimates.
