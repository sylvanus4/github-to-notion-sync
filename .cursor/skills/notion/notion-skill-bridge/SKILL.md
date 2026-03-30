---
name: notion-skill-bridge
description: >-
  Compare Notion MCP-first workflows versus SKILL.md-first agent workflows for a
  given task; deliver a decision matrix (freshness, cost, reusability, constraint
  strength, collaboration, output stability) and a clear recommendation.
  Korean triggers: "노션 스킬 비교", "어떤 방식이 나아?", "노션 대 스킬".
  English triggers: "Notion vs Skill", "notion-skill-bridge", "MCP vs Skill.md",
  "workflow approach comparison", "Notion automation vs skill".
  Do NOT use for implementing integrations (write code/MCP config), arbitrary app
  comparisons unrelated to Notion or skills, or choosing unrelated tools (e.g. Jira).
metadata:
  version: "1.0.0"
  category: meta
  author: thaki
---

# Notion–Skill Bridge (Decision Guide)

**All outputs MUST be in Korean (한국어). Technical terms may remain in English.**

## Purpose

For a **specific workflow**, help choose between:
- **Notion MCP–centric**: live read/write of pages/DB as the system of record.
- **SKILL.md–centric**: encode procedure, rubrics, and guardrails in-repo; tools invoked as needed.

## Prerequisites

- Clear **user goal** (e.g. recurring digest, one-off analysis, governance gate).
- Awareness that **Notion MCP** needs connectivity; **Slack MCP** / **gws** are optional context.

## Procedure

1. **Define the workflow** — Inputs, actors, frequency (adhoc / daily / on-event), and outputs (Notion page, Slack, email, file).

2. **Score both approaches** (0–5 each; document assumptions in Korean):

   | Criterion | Notion MCP–first | SKILL.md–first |
   |-----------|------------------|----------------|
   | **Freshness** | High if always reading live pages | Medium unless skill mandates refresh step |
   | **Cost** | Higher token/tool use per run | Lower per run after skill is stable |
   | **Reusability** | Medium (prompt + MCP calls) | High (repeatable procedure) |
   | **Constraint strength** | Medium (depends on prompt discipline) | High (explicit MUST/ MUST NOT) |
   | **Collaboration** | Strong (SSoT in Notion) | Weaker unless skill links to Notion |
   | **Output stability** | Variable with live data | More stable rubric-driven outputs |

3. **Hybrid pattern** — If scores tie, recommend **SKILL.md orchestrating Notion MCP** (procedure in repo, state in Notion): best constraint strength + collaboration.

4. **Decision** — State **primary** recommendation, **when to switch** (e.g. policy changes weekly → bias Notion; rigid QA rubric → bias skill).

5. **Integration note** — If calendar/email matters, mention **Google Workspace CLI (`gws`)** as auxiliary, not a replacement for Notion SSOT.

6. **Cost model (qualitative)** — Notion MCP-heavy flows increase tool calls and tokens per run; SKILL.md-heavy flows shift cost to maintenance and review. State this trade-off explicitly in Korean.

7. **Governance** — If constraints must survive prompt drift, prefer SKILL.md + optional Notion SSOT for data; if constraints change weekly, prefer Notion MCP reads with a thin skill wrapper.

## When to choose Notion MCP–first

- The page/DB is the **authoritative** source and changes frequently.
- Multiple humans edit the same artifact and expect **live** fidelity.
- You need structured properties (status, owner, dates) without duplicating them into git.

## When to choose SKILL.md–first

- You need **stable** procedures, rubrics, or gates across many tasks.
- The workflow is repeated with similar shape (checklists, scoring, mandatory order).
- You want reviewability in PRs like normal code.

## Hybrid pattern (recommended default)

- SKILL.md defines **steps, guardrails, and output shape**.
- Notion MCP supplies **current records** (pages, DB rows).
- Slack MCP publishes **human-facing summaries** when broadcast is required.

## Output structure (sections must be written in Korean)

1. Workflow summary
2. Criterion score table (Notion-first vs skill-first vs hybrid)
3. Final recommendation + rationale
4. Risks and mitigations
5. Optional implementation checklist (MCP calls, skill placement, approval gates)
6. One-sentence decision summary

## Examples

- **Daily status digest** → Hybrid: SKILL defines steps; Notion MCP pulls project DB; Slack MCP posts.

- **One-off page edit** → Notion MCP–first; no new skill unless repetition ≥3.

- **Recurring compliance review** → SKILL.md–first with embedded checklist; link to Notion policy page as SSOT.

## Quality checklist

- Matrix uses the same 0–5 scale for both columns or explains any N/A cells.
- Recommendation names **who maintains** the skill vs the Notion source (roles, not individuals, unless user supplied).
- Risks include **failure modes** (stale Notion, over-long skills, MCP outages).

## Error handling

- **Insufficient workflow detail**: Ask up to **3** targeted questions (frequency, owners, canonical data location).
- **No Notion access assumed**: Recommend SKILL.md with manual paste path, or gating step “human exports from Notion”.
- **Conflicting SSOT**: Explicitly flag; recommend resolving ownership before automation.
