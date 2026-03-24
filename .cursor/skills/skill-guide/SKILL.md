---
name: skill-guide
description: >-
  Interactive skill discovery and usage guide: scans the local skills library,
  matches user intent to available skills, suggests chains, and gives copy-paste
  invocation patterns without opening every SKILL.md manually.
  Korean triggers: "어떤 스킬 써야 해?", "스킬 찾기", "스킬 추천", "스킬 가이드".
  English triggers: "skill guide", "find skill", "which skill", "help me choose",
  "recommend a skill", "skill picker", "what skill for".
  Do NOT use for creating new skills (use create-skill), auditing skill quality
  (use skill-optimizer), or transcript-based skill mining (use autoskill-extractor).
metadata:
  version: "1.0.1"
  category: meta
  author: thaki
---

# Skill Guide (Interactive Discovery)

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Purpose

Help the user pick the **right** skill from `.cursor/skills/` by intent, surface **when not to use** a skill (from each skill’s description), and propose **short chains** (e.g. meeting → digest → md-to-notion).

## Prerequisites

- Workspace root is the planning automation repository.
- Skills live under `.cursor/skills/<skill-name>/SKILL.md`.

## Procedure

1. **Capture intent** — Task type (meeting, PRD, code reverse, doc quality, GTM, design sync, etc.), constraints (Notion-only, no code access, deadline), and desired artifact (Slack post, Notion page, local markdown).

2. **Inventory skills** — List directories under `.cursor/skills/`. For each `SKILL.md`, read YAML `name`, `description` (first ~400 chars), and `metadata.category` if present. Build a table: `skill-name` | one-line capability | category.

3. **Match** — Score candidates against intent using: trigger phrases in `description`, explicit “Use when” / “Korean triggers”, and negation clauses (“Do NOT use for …”). Prefer **one primary** skill; list **2 alternates** with one-line rationale.

4. **Recommend usage** — For the primary skill, output:
   - **Invocation hint**: natural-language prompt the user can paste (Korean).
   - **Inputs to prepare**: URLs, file paths, DB names, channels.
   - **Chain recipe** (optional): ordered list of skills + handoff artifact between steps.

5. **Integrations** — If the task needs publishing: mention **Notion MCP** (pages/DB), **Slack MCP** (channel/thread), or **Google Workspace CLI** (`gws`) only when the recommended skill’s workflow expects them; do not assume credentials are configured.

6. **Gap handling** — If no skill fits, say so clearly and suggest the closest 2 skills plus what human work remains.

7. **Registry cross-check (optional)** — If the repository maintains a skill registry under `.cursor/rules/`, mention only **in-repo** references when the user asks for slash-commands or orchestration maps. Never invent commands that are not documented locally.

8. **Safety** — Do not expose secrets, tokens, or private URLs from skill files. Redact if encountered.

## Tooling

- **Discovery**: Enumerate `.cursor/skills/*/` directories; open each `SKILL.md` frontmatter first (fast path).
- **Deep match**: When two skills overlap, compare their **negative triggers** (“Do NOT use”) to avoid wrong routing.
- **Notion MCP**: Recommend when the user’s source of truth is a Notion page/DB and live fetch is required.
- **Slack MCP**: Recommend when the deliverable is a team broadcast or threaded decision log.
- **Google Workspace CLI (`gws`)**: Recommend when the workflow depends on Calendar, Gmail, Drive, or Sheets automation in the terminal.

## Output structure (sections must be written in Korean)

1. Recommended skill (one primary + two alternates)
2. Rationale (intent and constraints mapping)
3. How to run (paste-ready Korean prompt + required inputs)
4. Optional skill-chain recipe
5. Skills to avoid (when relevant)

## Examples

- **Intent**: Meeting notes → action items → Notion publish → Recommend `meeting-digest` or `notion-meeting-sync` by source; chain `md-to-notion` if the intermediate artifact is local Markdown.

- **Intent**: PRD quality scoring + gate only → Recommend `doc-quality-gate`; avoid `doc-review-orchestrator` if orchestration is out of scope.

- **Intent**: Code-only reverse spec → Recommend `code-to-spec`; if diffing against a canonical Notion spec, add `code-spec-comparator`.

- **Intent**: Today’s work summary to Slack → Recommend `planning-daily-briefing` when Notion + Calendar are in scope; otherwise Slack-only summary with explicit data gaps.

## Quality checklist (before responding)

- Primary recommendation has **one** clear owner skill (not a vague list).
- Alternates explain **trade-offs**, not duplicates.
- User-facing prompt is **paste-ready** Korean.
- “Do NOT use” conflicts are explicitly called out when relevant.

## Error handling

- **Missing `.cursor/skills/`**: Report path missing; ask user to confirm workspace root.
- **Unreadable SKILL.md**: Skip file; list it under “Files excluded from scan”.
- **Ambiguous intent**: Ask up to **3** clarifying questions (source system, final destination, code vs doc only).
