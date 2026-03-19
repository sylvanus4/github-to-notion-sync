# Anthropic Best Practices for SKILL.md Files

Condensed from "The Complete Guide to Building Skills for Claude" (Anthropic, 2025).

## 1. Frontmatter Rules

### Required Fields
- `name`: kebab-case, matches folder name (e.g., `backend-expert`)
- `description`: Under 1024 characters. No XML angle brackets (`<`, `>`). Must include what, when, and negative triggers.

### Recommended Fields
```yaml
metadata:
  version: "1.0.0"
  category: execution | review | generation | orchestrator
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
2. **When to Use** — brief trigger context
3. **Workflow / Instructions** — step-by-step, numbered
4. **Output Format** — expected output structure
5. **Examples** — at least 1, format: `User says / Actions / Result`
6. **Troubleshooting** — at least 1, format: `Cause / Solution`

## 4. Composability Rules

### Negative Triggers
When two skills have overlapping trigger zones, BOTH skills must include `Do NOT use for...` clauses that point to the other skill.

### Known Overlap Pairs
- `ux-expert` ↔ `web-design-guidelines` ↔ `frontend-design`
- `frontend-expert` ↔ `frontend-design`
- `backend-expert` ↔ `db-expert`
- `qa-test-expert` ↔ `e2e-testing`
- `security-expert` ↔ `compliance-governance`
- `local-dev-runner` ↔ `service-health-doctor`
- `pr-review-captain` ↔ `domain-commit`
- `technical-writer` ↔ `prompt-transformer`

### Independence
Skills must be self-contained — no skill should require another skill to function. Orchestration is handled by `mission-control`, not by individual skills.

## 5. Design Patterns

### Pattern 1: Sequential Workflow Orchestration
Steps execute in fixed order. Each step's output feeds the next.
Best for: CI pipelines, deployment workflows, commit workflows.

### Pattern 2: Multi-MCP Coordination
Skill coordinates multiple MCP servers or tools for a single task.
Best for: Cross-platform operations (GitHub + Slack, Figma + code).

### Pattern 3: Iterative Refinement
Audit → fix → re-validate loop. Repeats until quality threshold met.
Best for: Code review, optimization, quality checks.

### Pattern 4: Context-aware Tool Selection
Skill selects different tools/approaches based on runtime context.
Best for: Debugging, diagnostics, environment-dependent tasks.

### Pattern 5: Domain-specific Intelligence
Skill encodes expert knowledge for a specific domain.
Best for: Security review, UX audit, performance profiling.

## 6. Category Assignment

| Category | Meaning | Skills |
|----------|---------|--------|
| execution | Modifies code, state, or files | domain-commit, ci-quality-gate, e2e-testing, local-dev-runner, service-health-doctor, dependency-auditor, i18n-sync |
| review | Read-only analysis | backend-expert, frontend-expert, db-expert, security-expert, compliance-governance, ux-expert, sre-devops-expert, qa-test-expert, pr-review-captain, performance-profiler, web-design-guidelines |
| generation | Creates new artifacts | technical-writer, frontend-design, ui-ux-pro-max, prompt-transformer, skill-optimizer |
| orchestrator | Coordinates other skills | mission-control |

## 7. Folder Structure

```
.cursor/skills/<skill-name>/
  SKILL.md              # Main skill file (REQUIRED, case-sensitive)
  references/           # Linked reference documents
    reference.md        # Detailed reference material
    templates.md        # Template files
  scripts/              # Executable scripts (optional)
  assets/               # Static assets (optional)
```

### Naming Rules
- Folder: kebab-case, no spaces/underscores/capitals
- Main file: Exactly `SKILL.md` (not `skill.md`, `Skill.md`, or `README.md`)
- References: Descriptive kebab-case names (e.g., `service-inventory.md`)

## 8. Size Guidelines

| Element | Target | Hard Limit |
|---------|--------|------------|
| Description | 200-500 chars | 1024 chars |
| SKILL.md body | Under 150 lines | 200 lines |
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
    coding-guide.md   # Team coding standards
```

**Key principle:** The `references/` files are the value — SKILL.md is just the loader. Swapping reference files changes the domain expertise without modifying the skill.

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

**Key principle:** Templates define _what_ gets produced; style guides define _how_ it looks. Both are swappable independently.

### Pattern C: Reviewer

Separates "what to check" (swappable review criteria) from "how to check" (review infrastructure).

**Structure:**
```
skill-name/
  SKILL.md            # Review workflow + aggregation logic
  references/
    review-checklist.md  # Swappable criteria
    agent-prompts.md     # Domain-specific reviewer instructions
```

**Key principle:** Replacing `review-checklist.md` (e.g., Python style to OWASP security) transforms the review domain while reusing the same infrastructure.

### Pattern D: Inversion

Agent interviews the user before producing output. Explicit gate conditions prevent premature generation from incomplete context.

**Implementation:**
```markdown
## HARD-GATE
Do NOT produce any output until ALL of the following are confirmed:
1. [Required context item 1]
2. [Required context item 2]
3. User has approved the approach
If any requirement is missing, ASK — do not assume.
```

**Key principle:** The gate forces context completeness. Without it, agents tend to generate from partial information, producing plausible but wrong output.

### Pattern E: Pipeline

Enforces step-by-step execution with checkpoint verification between phases. Each phase loads only the reference files it needs.

**Implementation:**
```markdown
### Phase 1: [Name]
Read `references/phase-1-context.md`. Execute steps. Verify output.

### Phase 1½: Quality Gate
Before proceeding, verify: [criteria]. If ANY fails, STOP.

### Phase 2: [Name]
Read `references/phase-2-context.md`. Execute steps.
```

**Key principle:** Diamond gate conditions between phases prevent step-skipping. Phase-specific reference loading conserves context window tokens.

### Pattern Combinations

Patterns are composable:
- **Pipeline + Reviewer**: Add a Reviewer checkpoint stage within a Pipeline
- **Generator + Inversion**: Interview for requirements before generating from templates
- **Tool Wrapper + Reviewer**: Load domain rules, then review code against them
- **Pipeline + Inversion**: Interview at pipeline start, checkpoints throughout
