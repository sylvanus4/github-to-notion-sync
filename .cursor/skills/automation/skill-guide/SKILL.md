---
name: skill-guide
description: >-
  Interactive skill and agent team discovery guide: scans the local skills library
  and agent-teams registry, matches user intent to available skills or multi-agent
  teams, suggests chains, and gives copy-paste invocation patterns.
  Korean triggers: "어떤 스킬 써야 해?", "스킬 찾기", "스킬 추천", "스킬 가이드",
  "스택 기반 추천", "기술 스택 맞는 스킬".
  English triggers: "skill guide", "find skill", "which skill", "help me choose",
  "recommend a skill", "skill picker", "what skill for", "stack-aware skills".
  Do NOT use for creating new skills (use create-skill), auditing skill quality
  (use skill-optimizer), or transcript-based skill mining (use autoskill-extractor).
metadata:
  version: "1.0.2"
  category: meta
  author: thaki
---

# Skill Guide (Interactive Discovery)

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Purpose

Help the user pick the **right** skill from `.cursor/skills/` by intent, surface **when not to use** a skill (from each skill’s description), and propose **short chains** (e.g. meeting → digest → md-to-notion).

## Prerequisites

- Workspace root is the **ai-model-event-stock-analytics** repository (stock analytics, event study, trading pipelines).
- Skills live under `.cursor/skills/<skill-name>/SKILL.md`.

## Repository conventions (ai-model-event-stock-analytics)

When **authoring** skills or explaining how this repo expects agents to behave:

| Topic | Convention |
|-------|------------|
| SKILL.md body | English (workflows, headings, technical steps). |
| User-facing deliverables | Korean (한국어) unless the user explicitly asks otherwise. |
| Korean triggers | Keep in YAML `description` / trigger lists; do not strip in favor of English-only. |
| Domain | Prioritize **financial data analysis**, **trading / screening**, **pipeline automation** (`today`, `daily-stock-check`, DB sync, FastAPI tabs) when intent is ambiguous. |
| UI guidance | **Tailwind CSS + Radix UI** per local rules; do not default to Thaki Cloud **TDS** or **Figma** as mandatory. |
| Integrations | Prefer **Notion MCP**, **Slack MCP**, and **Google Workspace CLI (`gws`)** when the task is publishing or notify workflows—aligned with `AGENTS.md`. |

Use this block when the user asks for “skills in English but outputs in Korean”, or when routing tasks tied to stock reports, Slack trading channels, or stakeholder documentation.

### Tier-aware recommendations

1. Read [docs/policies/skill-assessment-matrix.md](../../../docs/policies/skill-assessment-matrix.md) for **tier classification** (A–E).
2. **Exclude Tier D** skills from default recommendations for this project (not applicable here unless the user explicitly names a Tier D use case).
3. **Prioritize** trading and financial analysis skills (e.g. `today`, `daily-stock-check`, `weekly-stock-update`, `tab-*`, `trading-*`, `alphaear-*`) when intent matches markets or portfolio workflows.
4. When a skill includes **Project-Specific Overrides** (bottom of its SKILL.md) or points to [.cursor/skills/references/project-overrides/](../references/project-overrides/README.md), **say so** in the rationale so the user knows policy-aligned context is available.

## Modes

### Default Mode (intent-based)

Standard interactive discovery matching user intent to available skills.

### Stack-Aware Mode (`--stack-aware`)

Pre-filters skills by detected project tech stack before intent matching.
Activated when the user says "스택 기반 추천", "stack-aware", "기술 스택 맞는 스킬",
or when the user's request implies project-specific technology context.

**Stack-Aware Procedure:**

1. Run `python scripts/skill_recommender.py --top=30` to get the ranked skill list
2. Use the ranked output as the candidate pool instead of scanning all skills
3. Continue with the standard Procedure below, but only match against the pre-filtered set
4. In the output, add a "🔧 Detected Stack" summary line showing which technologies were found

This mode reduces noise from 700+ skills to the ~30 most stack-relevant candidates,
making recommendations more precise for project-specific tasks.

## Agent Team Discovery

When the user's intent maps to a **multi-step collaborative workflow** (not a single skill),
check `.cursor/skills/agent-teams/team-registry.md` for a matching agent team.

| Intent Signal | Recommend Team Instead of Skill |
|---------------|-------------------------------|
| "deep research with report", "연구 리포트" | Research & Report Team |
| "create content", "콘텐츠 제작" | Content Production Team |
| "strategic analysis", "전략 분석" | Strategic Intelligence Team |
| "incident response", "장애 대응" | Incident Response Team |
| "ship code", "코드 출시" | Code Ship Team |
| "build knowledge base", "KB 구축" | Knowledge Builder Team |
| "analyze meeting", "회의 분석" | Meeting Intelligence Team |
| "prepare deal package", "딜 준비" | Sales Deal Team |

**When to recommend a team over a single skill:**
- The task requires 3+ sequential or parallel sub-tasks
- Quality review / iteration is expected
- Multiple perspectives or expertise domains are needed
- The user asks for "end-to-end", "전체 파이프라인", or "팀으로"

**How to invoke a team:** Read the coordinator SKILL.md and follow its protocol:
```
Read: .cursor/skills/agent-teams/{team}/coordinator/SKILL.md
```

## Procedure

1. **Capture intent** — Task type (meeting, PRD, code reverse, doc quality, GTM, design sync, etc.), constraints (Notion-only, no code access, deadline), and desired artifact (Slack post, Notion page, local markdown).

2. **Inventory skills** — List directories under `.cursor/skills/`. For each `SKILL.md`, read YAML `name`, `description` (first ~400 chars), and `metadata.category` if present. Build a table: `skill-name` | one-line capability | category.

3. **Conditional filter** — For each candidate from Step 2, check `metadata.requires_mcp`, `metadata.fallback_for_mcp`, and `metadata.platforms` fields (see `skill-prompt-patterns.mdc` Conditional Activation Metadata). Remove skills whose conditions are not met by the current session (e.g., missing MCP server, wrong OS). Skills without these fields pass unconditionally.

4. **Match** — Score candidates against intent using: trigger phrases in `description`, explicit “Use when” / “Korean triggers”, and negation clauses (“Do NOT use for …”). Prefer **one primary** skill; list **2 alternates** with one-line rationale. **Filter out Tier D** skills unless the user explicitly needs them (see `skill-assessment-matrix.md`). **Boost** financial / trading / data-pipeline skills when intent involves stocks, signals, backtests, or `outputs/` reports.

5. **Recommend usage** — For the primary skill, output:
   - **Invocation hint**: natural-language prompt the user can paste (Korean).
   - **Inputs to prepare**: URLs, file paths, DB names, channels.
   - **Chain recipe** (optional): ordered list of skills + handoff artifact between steps.

6. **Integrations** — If the task needs publishing: mention **Notion MCP** (pages/DB), **Slack MCP** (channel/thread), or **Google Workspace CLI** (`gws`) only when the recommended skill’s workflow expects them; do not assume credentials are configured.

7. **Gap handling** — If no skill fits, say so clearly and suggest the closest 2 skills plus what human work remains.

8. **Registry cross-check (optional)** — If the repository maintains a skill registry under `.cursor/rules/`, mention only **in-repo** references when the user asks for slash-commands or orchestration maps. Never invent commands that are not documented locally.

9. **Safety** — Do not expose secrets, tokens, or private URLs from skill files. Redact if encountered.

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

- **Intent**: Daily stock pipeline / screener / report → Recommend `today` or `daily-stock-check`; chain `daily-db-sync` when persisting `outputs/` to PostgreSQL.

## Quality checklist (before responding)

- Primary recommendation has **one** clear owner skill (not a vague list).
- Alternates explain **trade-offs**, not duplicates.
- User-facing prompt is **paste-ready** Korean.
- “Do NOT use” conflicts are explicitly called out when relevant.
- **Tier D** skills are not recommended unless the user asked for that tier explicitly.

## Error handling

- **Missing `.cursor/skills/`**: Report path missing; ask user to confirm workspace root.
- **Unreadable SKILL.md**: Skip file; list it under “Files excluded from scan”.
- **Ambiguous intent**: Ask up to **3** clarifying questions (source system, final destination, code vs doc only).

---

## Project-Specific Overrides

Applies only in **ai-model-event-stock-analytics**.

| Override | Path |
|----------|------|
| SSOT / repo facts | [.cursor/skills/references/project-overrides/project-ssot.md](../references/project-overrides/project-ssot.md) |
| Terminology (POL-001) | [.cursor/skills/references/project-overrides/project-terminology-glossary.md](../references/project-overrides/project-terminology-glossary.md) |

**Constraints:** **Exclude Tier D** from default picks; **prioritize** trading / financial analysis skills; **note** when recommended skills ship **Project-Specific Overrides**; use [docs/policies/skill-assessment-matrix.md](../../../docs/policies/skill-assessment-matrix.md) for tier labels.
