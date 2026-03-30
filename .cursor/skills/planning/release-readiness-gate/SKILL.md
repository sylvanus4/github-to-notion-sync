---
name: release-readiness-gate
description: >-
  Pre-release comprehensive check: specs updated, designs aligned with implementation,
  tests green, policies reflected, docs current, UX copy reviewed, design QA complete.
  Aggregates signals from doc-quality-gate, cross-domain-sync-checker, ux-copy-audit,
  spec-state-validator, and feature-coverage-matrix into one go/no-go report.
  Korean triggers: "릴리스 준비", "출시 점검", "릴리스 게이트".
  English triggers: "release readiness", "release gate", "go/no-go", "release-readiness-gate".
  Do NOT use for post-incident review (use incident workflows) or CI-only checks without planning artifacts.
metadata:
  version: "1.0.1"
  category: review
  author: thaki
---

# Release Readiness Gate

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Purpose

Produce a **single go/no-go decision packet** for a release candidate by **orchestrating** planning-quality and sync skills, then **synthesizing** outcomes into an executive-ready Korean report with **blockers**, **risks**, and **explicit next steps**.

## Prerequisites

- **Release identifier**: version tag, branch name, or date-bound scope.
- **Artifact locations**: Notion PRD/spec pages, Figma links (if applicable), repo root, test commands.
- **Notion MCP** (optional): publish the final report page.
- **Slack MCP** (optional): notify release channel with verdict summary.

## Referenced skill roles (run or simulate from prior outputs)

| Signal source | What it must answer |
|---------------|---------------------|
| doc-quality-gate | Are planning docs complete and consistent? |
| cross-domain-sync-checker | Policy / design / code / PRD alignment |
| ux-copy-audit | UI string policy and tone compliance |
| spec-state-validator | Spec states and edges covered in code |
| feature-coverage-matrix | Spec → design → code → tests coverage |

When full runs are not available, accept **user-supplied prior reports** and **ingest summaries** instead of re-executing every skill.

## Procedure

1. **Charter** — Confirm release scope, freeze criteria, and **go/no-go owner** (role name). List mandatory gates for this release tier (hotfix vs major).

2. **Collect inputs** — Gather latest results from the five sources above (fresh invocations or pasted conclusions). Normalize to a common **pass / fail / waived / unknown** scale.

3. **Gate matrix** — Build a table: Gate name, Result, Evidence link, Owner, Due date for remediation (if fail).

4. **Critical path** — Identify **hard blockers** (any fail in tier-mandatory gate) vs **conditional waivers** (documented risk acceptance).

5. **Verdict** — Output **GO**, **NO-GO**, or **GO with conditions** with explicit conditions in Korean.

6. **Publish** — Create **Notion** page under agreed parent via **Notion MCP**; title and headings per team naming (Korean).

7. **Slack** — Post short Korean summary: verdict, blocker count, link to Notion; use thread for gate table screenshot or bullet list.

8. **Follow-ups** — Emit a checklist of **remaining tasks** with suggested owners (names if known from context).

## Notion MCP usage

- Create structured page: Verdict, Gate matrix, Risks, Waivers, Links to evidence.
- Link related PRD / decision log pages if IDs are provided.

## Slack MCP usage

- One main message; details in thread to reduce noise.
- Mention **@channel** or specific groups only if user requests.

## Google Workspace CLI (`gws`)

- Optional: attach **Calendar** milestone or release review meeting to the report (event link) when scheduling is part of the workflow.

## Output structure

Deliver in Korean: verdict (GO / NO-GO / conditional GO); gate result matrix; blocker list; residual risks and mitigations; evidence links.

## Error handling

- Missing any input source → mark **unknown** for that gate; **do not infer pass**.
- Conflicting results between two gates → call out **conflict** and recommend reconciliation owner.

## Examples

- Major launch: **NO-GO** due to spec-state-validator failing on payment edge states.
- Patch: **GO** with waiver on design QA for non-UI change, documented in report.

## Guardrails

- Waivers require **written rationale** in the Korean report; silent skips are forbidden.
- Keep evidence links **internal** (Notion, repo); redact customer-specific data in Slack posts.
