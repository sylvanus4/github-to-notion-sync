# Anthropic Best Practices for SKILL.md Files

Condensed from "The Complete Guide to Building Skills for Claude" (Anthropic, 2025). Use for this workspace's `.cursor/skills/` tree.

## 1. Frontmatter Rules

### Required Fields
- `name`: kebab-case, matches folder name (e.g., `doc-quality-gate`)
- `description`: Under 1024 characters. No XML angle brackets (`<`, `>`). Must include what, when, and negative triggers.

### Recommended Fields
```yaml
metadata:
  version: "1.0.0"
  category: execution | review | generation | orchestrator | self-improvement
```

### Description Formula
```
[What it does — 1 sentence] +
[When to use — trigger phrases with "Use when..."] +
[Do NOT use for — negative triggers pointing to other skills]
```

### Frontmatter Security
- **No angle brackets** (`<`, `>`) anywhere in YAML frontmatter — they break XML-based parsers.
- Use plain text for argument hints and examples.

## 2. Progressive Disclosure (3 Levels)

| Level | Location | What Goes Here | Token Cost |
|-------|----------|---------------|------------|
| 1 | YAML frontmatter | name, description, metadata | Always loaded |
| 2 | SKILL.md body | Instructions, workflow, examples | Loaded on trigger |
| 3 | `references/` files | Large tables, templates, registries | Loaded on demand |

### When to Move Content to references/
- Tables with 10+ rows
- Multi-step bash command blocks (20+ lines)
- Template files or boilerplate
- Service registries or inventories
- Any content that is consulted but not needed for every invocation

### Linking Pattern
Keep a 1-2 line summary inline, then link:
```markdown
For the full audit checklist, see [references/audit-checklist.md](references/audit-checklist.md).
```

## 3. Required Sections in SKILL.md Body

1. **Title** (H1) — matches skill name
2. **When to Use** — brief trigger context (or ensure triggers live in frontmatter `description`)
3. **Workflow / Instructions** — step-by-step, numbered
4. **Output Format** — expected output structure
5. **Examples** — at least 1, format: `User says / Actions / Result`
6. **Troubleshooting** — at least 1, format: `Cause / Solution`

## 4. Composability Rules

### Negative Triggers
When two skills have overlapping trigger zones, BOTH skills must include `Do NOT use for...` clauses that point to the other skill.

### Example Overlap Pairs (planning automation)
- `meeting-digest` ↔ `pm-execution` (simple summary vs full PM workflow)
- `prd-research-factory` ↔ `pm-execution` (research PRD vs simple PRD)
- `code-to-spec` (unified reverse spec) ↔ `code-spec-comparator` (Notion spec vs code gaps)
- `doc-quality-gate` (unified: weighted scoring + A–D grade + approve/reject gate + checklists)
- `policy-text-generator` ↔ `ux-writing-agent` (policy compliance vs tone/voice / UX copy)

### Independence
Skills must be self-contained — no skill should require another skill to function. Multi-skill flows are orchestrated via `.cursor/rules/skill-orchestration.mdc` and user commands (e.g. `/prd-from-meeting`), not by hard dependencies inside a single SKILL.md.

## 5. Design Patterns

### Pattern 1: Sequential Workflow Orchestration
Steps execute in fixed order. Each step's output feeds the next.
Best for: meeting → PRD → quality gate pipelines.

### Pattern 2: Multi-MCP Coordination
Skill coordinates multiple MCP servers or tools for a single task.
Best for: Notion + Slack, Figma + GitHub.

### Pattern 3: Iterative Refinement
Audit → fix → re-validate loop. Repeats until quality threshold met.
Best for: Document review, skill optimization.

### Pattern 4: Context-aware Tool Selection
Skill selects different tools/approaches based on runtime context.
Best for: Diagnostics, environment-dependent tasks.

### Pattern 5: Domain-specific Intelligence
Skill encodes expert knowledge for a specific domain.
Best for: UX writing policy, design system tracking, PRD structure.

## 6. Category Assignment

| Category | Meaning | Examples (this repo) |
|----------|---------|----------------------|
| execution | Modifies code, state, or files | md-to-notion, prd-cascade-sync (when applying) |
| review | Read-only analysis | doc-quality-gate, cross-domain-sync-checker, skill-optimizer |
| generation | Creates new artifacts | prd-auto-generator, policy-text-generator |
| orchestrator | Coordinates other skills | dev-planning-bridge (orchestrates pipeline) |
| self-improvement | Meta-skills | skill-autoimprove, autoskill-evolve |

## 7. Folder Structure

```
.cursor/skills/<skill-name>/
  SKILL.md              # Main skill file (REQUIRED, case-sensitive)
  references/           # Linked reference documents
  scripts/              # Executable scripts (optional)
  assets/               # Static assets (optional)
```

### Naming Rules
- Folder: kebab-case, no spaces/underscores/capitals
- Main file: Exactly `SKILL.md` (not `skill.md`, `Skill.md`, or `README.md`)
- References: Descriptive kebab-case names (e.g., `quality-checklist.md`)

## 8. Size Guidelines

| Element | Target | Hard Limit |
|---------|--------|------------|
| Description | 200-500 chars | 1024 chars |
| SKILL.md body | Under 150 lines | 200 lines (team may allow up to 500 for legacy — prefer extraction) |
| SKILL.md word count | Under 2000 words | 5000 words |
| Single reference file | Under 500 lines | No hard limit |

## 9. Portability

Skills should work identically across:
- Claude.ai (Projects)
- Claude Code (CLI)
- Cursor IDE
- Google ADK (via `load_skill_from_dir()`)
- API integrations

Avoid IDE-specific commands or paths. Use relative paths for all file references within the skill.

## 10. Content Design Patterns

Five content design patterns complement the infrastructure patterns in Section 5. While infrastructure patterns describe _how skills orchestrate work_, content design patterns describe _how skills structure their internal knowledge and interaction logic_.

### Pattern A: Tool Wrapper

Provides on-demand context for a specific library, API, or coding standard. Instead of hardcoding rules in the system prompt, the skill loads focused reference files when triggered.

**Structure:**
```
skill-name/
  SKILL.md            # Trigger logic + "read references/X when..."
  references/
    api-rules.md      # Library-specific constraints
```

### Pattern B: Generator

Separates output templates from style/formatting rules for consistent artifact creation.

**Structure:**
```
skill-name/
  SKILL.md            # Generation workflow
  assets/
    templates/        # Output structure templates
  references/
    style-guide.md    # Formatting rules, tone, conventions
```

### Pattern C: Reviewer

Separates "what to check" (swappable review criteria) from "how to check" (review infrastructure).

**Structure:**
```
skill-name/
  SKILL.md            # Review workflow + aggregation logic
  references/
    review-checklist.md  # Swappable criteria
```

### Pattern D: Inversion

Agent interviews the user before producing output. Explicit gate conditions prevent premature generation from incomplete context.

**Implementation:**
```markdown
## HARD-GATE
Do NOT produce any output until ALL of the following are confirmed:
1. [Required context item 1]
2. [Required context item 2]
If any requirement is missing, ASK — do not assume.
```

### Pattern E: Pipeline

Enforces step-by-step execution with checkpoint verification between phases. Each phase loads only the reference files it needs.

**Implementation:**
```markdown
### Phase 1: [Name]
Read `references/phase-1-context.md`. Execute steps. Verify output.

### Phase 1½: Quality Gate
Before proceeding, verify: [criteria]. If ANY fails, STOP.
```

### Pattern Combinations

Patterns are composable:
- **Pipeline + Reviewer**: Add a Reviewer checkpoint stage within a Pipeline
- **Generator + Inversion**: Interview for requirements before generating from templates
- **Tool Wrapper + Reviewer**: Load domain rules, then review code against them
- **Pipeline + Inversion**: Interview at pipeline start, checkpoints throughout
