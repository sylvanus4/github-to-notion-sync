---
name: context-engineer
description: >-
  Manage project knowledge architecture — MEMORY.md lifecycle, domain glossary
  maintenance, context packages per analysis type, knowledge graph updates, and
  AI agent context window optimization. Ensures AI agents always have full
  understanding of the stock analytics domain without re-explaining. Use when
  the user asks to "update context", "refresh MEMORY.md", "build context
  package", "optimize agent context", "context engineer", "컨텍스트 관리",
  "MEMORY 업데이트", "지식 아키텍처", or wants to improve how AI agents
  understand the project.
  Do NOT use for general MEMORY.md updates during task completion (follow
  done-checklist rule directly). Do NOT use for creating new skills (use
  anthropic-skill-creator or create-skill). Do NOT use for prompt optimization
  (use prompt-architect or prompt-transformer).
metadata:
  author: thaki
  version: 1.0.0
  category: generation
---

# Context Engineer

Manage the knowledge architecture that makes AI agents effective collaborators in this stock analytics project. Context engineering ensures every AI interaction starts with the right domain knowledge, project state, and historical context -- eliminating the need to re-explain.

## Meta-Orchestration

### Prompt router (representative user phrases)

| # | Example prompt | This skill? | Delegation order (numbered) | Output merge strategy | User overrides |
|---|----------------|-------------|------------------------------|------------------------|----------------|
| 1 | AI 리포트 품질을 자동 평가해줘 | No | 1) `ai-quality-evaluator` | — | — |
| 2 | 데일리 파이프라인을 설계해줘 | No | 1) `ai-workflow-integrator` / `today` | — | — |
| 3 | 이 프로세스를 자동화할지 결정해줘 | No | 1) `automation-strategist` | — | — |
| 4 | 시스템 데이터 흐름을 분석해줘 | No | 1) `system-thinker` | — | — |
| 5 | 프로젝트 컨텍스트를 업데이트해줘 | Yes | 1) Choose mode (MEMORY refresh vs context package vs glossary vs optimization) → 2) Parallel gather (git log, tasks, lessons, skills) → 3) Apply edits → 4) Run quality checks table | **Merged** updates: MEMORY.md sections + optional new `references/*-context.md` + summary bullet for user | `PRUNE_DAYS` (default 30); `MODE=1|2|3|4`; target domain name for packages |

### Error recovery

| Failure mode | Retry | Fallback | Abort |
|--------------|-------|----------|-------|
| MEMORY.md conflict/stale | — | Re-read file; merge sections; never delete [decision] without user OK | — |
| Oversized skill | — | Extract to `references/`; leave stub workflow | — |
| Missing domain for package | — | Ask user to name domain | — |

### Output aggregation

After updates, emit **one** user-facing summary listing: files touched, pruned count, open gaps, and **next recommended skill** if work continues (e.g. `skill-guide-sync`).

## Knowledge Architecture

The project's context is organized in three tiers:

### Tier 1: Working Memory (always loaded)

| Source | Path | Content |
|--------|------|---------|
| MEMORY.md | `MEMORY.md` | Decisions, tasks, issues, session context |
| Rules | `.cursor/rules/*.mdc` | Persistent behavior rules |
| Skill descriptions | `.cursor/skills/*/SKILL.md` frontmatter | Skill registry (description field only) |

### Tier 2: Domain Knowledge (loaded on demand)

| Source | Path | Content |
|--------|------|---------|
| Skill bodies | `.cursor/skills/*/SKILL.md` | Full skill instructions |
| Skill references | `.cursor/skills/*/references/*.md` | Detailed reference docs |
| Task tracking | `tasks/todo.md` | Current and completed tasks |
| Lessons learned | `tasks/lessons.md` | Patterns from past corrections |
| Known issues | `KNOWN_ISSUES.md` | Documented bugs and patterns |

### Tier 3: Project Knowledge (searchable)

| Source | Path | Content |
|--------|------|---------|
| Product docs | `docs/` | PRDs, ADRs, architecture docs |
| API schemas | `backend/app/api/` | Endpoint definitions |
| DB models | `backend/app/models/` | Data schema |
| Constants | `backend/app/core/constants.py` | Ticker maps, categories |
| Config | `.env.example`, `docker-compose.yml` | Infrastructure config |

## Workflow

### Mode 1: MEMORY.md Refresh

Update MEMORY.md with current project state.

**Step 1 — Audit current MEMORY.md:**

Read `MEMORY.md` and identify:
- Stale entries (decisions that have been superseded)
- Missing entries (recent work not captured)
- Incorrect entries (facts that changed)

**Step 2 — Gather fresh context:**

Run these in parallel:
1. `git log --oneline -20` — recent commits
2. Read `tasks/todo.md` — current task state
3. Read `tasks/lessons.md` — recent lessons
4. Scan `.cursor/skills/` — any new or removed skills
5. Check `backend/app/core/constants.py` — ticker changes

**Step 3 — Update MEMORY.md:**

Apply the MEMORY.md protocol from `.cursor/rules/self-improvement.mdc`:

```markdown
## [decision] Title (YYYY-MM-DD)
- Context: why this decision was made
- Choice: what was decided
- Alternatives considered: what was rejected and why

## [task] Title (YYYY-MM-DD)
- Status: completed/in-progress/blocked
- Key artifacts: file paths created or modified

## [issue] Title (YYYY-MM-DD)
- Symptom: what went wrong
- Resolution: how it was fixed
```

Remove entries older than 30 days unless they contain architectural decisions.

### Mode 2: Context Package Creation

Build a reusable context package for a specific analysis domain.

**Step 1 — Define the domain:**

Identify what the context package covers:
- Stock analysis (Turtle, Bollinger, Oscillators)
- Data pipeline operations
- Report generation
- Market research (news, sentiment)

**Step 2 — Assemble context:**

For the target domain, collect:

1. **Glossary**: Domain-specific terms and their meanings in this project
2. **Architecture**: Relevant file paths, data flows, and dependencies
3. **Conventions**: Naming patterns, data formats, API contracts
4. **Examples**: Sample inputs/outputs from actual runs
5. **Constraints**: Known limitations, gotchas, edge cases

**Step 3 — Write the context package:**

Create a focused reference document at `.cursor/skills/ce/context-engineer/references/{domain}-context.md`:

```markdown
# {Domain} Context Package

## Glossary
- **Term**: Definition in project context

## Architecture
- Key files and their roles
- Data flow diagram (text-based)

## Conventions
- Naming patterns
- Data formats

## Examples
- Sample input/output

## Constraints
- Known limitations
```

### Mode 3: Domain Glossary Maintenance

Keep the project's domain-specific terminology current.

**Step 1 — Scan for undefined terms:**

Search the codebase for financial and technical terms used without definition:
- Check `backend/app/services/technical_indicator_service.py` for indicator names
- Check `backend/app/core/constants.py` for category names
- Check `.cursor/skills/trading/daily-stock-check/SKILL.md` for signal terminology

**Step 2 — Cross-reference with existing glossary:**

Read the frontend glossary data (if available) at `frontend/src/` for i18n terms.

**Step 3 — Update or create glossary:**

Add missing terms to the appropriate context package. Each entry:
- **Term**: The canonical name
- **Definition**: What it means in this project
- **Used in**: File paths where it appears
- **Related**: Other terms it connects to

### Mode 4: Agent Context Optimization

Optimize how AI agents receive context for this project.

**Step 1 — Identify context bottlenecks:**

Check for:
- Skills over 500 lines (should extract to `references/`)
- MEMORY.md over 200 lines (should prune old entries)
- Redundant context (same info in multiple places)
- Missing negative triggers (skills triggering incorrectly)

**Step 2 — Apply progressive disclosure:**

For each oversized skill:
1. Keep essential workflow in SKILL.md (under 500 lines)
2. Extract detailed references to `references/` subdirectory
3. Add links from SKILL.md to reference files

**Step 3 — Optimize rule loading:**

Check `.cursor/rules/`:
- `always_applied` rules: Must be concise (loaded every turn)
- `agent_requestable` rules: Can be longer (loaded on demand)
- Move verbose always-applied rules to agent-requestable where possible

**Step 4 — Verify context chain:**

Ensure the context loading order is correct:
1. Rules fire first → set behavior
2. Skill description triggers → skill body loads
3. Skill references load → on explicit read
4. MEMORY.md and tasks/ → loaded when relevant

## Quality Checks

After any context update, verify:

| Check | Criteria |
|-------|----------|
| MEMORY.md size | Under 200 lines |
| No stale entries | All entries less than 30 days old (except architectural decisions) |
| No contradictions | Recent entries don't conflict with rules or skill descriptions |
| Glossary coverage | All signal types (BUY/SELL/NEUTRAL) and indicator names defined |
| Progressive disclosure | No skill body over 500 lines |

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| MEMORY.md over 200 lines | Not pruned regularly | Remove entries older than 30 days (keep architectural decisions) |
| Stale context package | Domain changed but package not updated | Re-run Mode 2 for the affected domain |
| Skill over 500 lines | Content not extracted | Extract tables, schemas, and examples to `references/` |
| Agent lacks ticker context | MEMORY.md missing ticker info | Run Mode 1 refresh, ensure constants.py is captured |
| Contradicting entries | Old decisions superseded by new ones | Remove old entry, add new [decision] with context |

## Examples

### Example 1: Post-feature MEMORY.md refresh

User says: "Update MEMORY.md with today's work"

Actions:
1. Audit current MEMORY.md
2. Check git log for recent commits
3. Read tasks/todo.md for completed items
4. Add [task] and [decision] entries
5. Prune entries older than 30 days

### Example 2: Create analysis context package

User says: "Build a context package for the technical analysis domain"

Actions:
1. Scan indicator service for terms (RSI, MACD, SMA, etc.)
2. Map data flow: DB → daily_stock_check.py → JSON → reporter
3. Document signal scoring rules
4. Save to `references/technical-analysis-context.md`

### Example 3: Optimize slow agent responses

User says: "Agent seems to lack context about our tickers"

Actions:
1. Check if MEMORY.md mentions current ticker list
2. Verify constants.py is referenced in relevant skills
3. Add ticker context to the stock analysis context package
4. Update MEMORY.md with current ticker count and categories

## Integration

- **MEMORY.md**: `MEMORY.md` (project root)
- **Rules**: `.cursor/rules/self-improvement.mdc`, `.cursor/rules/context-architecture.mdc`
- **Task tracking**: `tasks/todo.md`, `tasks/lessons.md`
- **Skills**: `.cursor/skills/*/SKILL.md`
- **Related skills**: `prompt-architect` (prompt optimization), `anthropic-skill-creator` (skill creation), `skill-optimizer` (skill quality)
