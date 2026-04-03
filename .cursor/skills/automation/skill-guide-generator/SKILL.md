---
name: skill-guide-generator
description: >-
  Scan all installed skills, identify undocumented ones, generate guide
  documentation following the standard template, and update the README index.
  Use when the user asks to "document skills", "sync skill guides",
  "skill-guide-sync", "find undocumented skills", "update skill docs",
  "스킬 문서화", "스킬 가이드 동기화", "문서화 안 된 스킬", or wants to ensure
  all skills have corresponding guide entries. Do NOT use for creating new
  skills from scratch (use create-skill), optimizing skill quality (use
  skill-optimizer), or writing general documentation (use technical-writer).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
---
# Skill Guide Generator

Automate the full skill documentation lifecycle: inventory installed skills, identify gaps, generate guide sections, and update the README index.

## Usage

```
/skill-guide-sync                    # full sync (scan + generate + update README)
/skill-guide-sync --dry-run          # gap analysis only, no file changes
/skill-guide-sync --scope tab-*      # only document skills matching prefix
/skill-guide-sync --readme-only      # only update README.md counts and tables
```

## Pipeline Overview

```
Phase 1: Inventory
  ├─ Glob .cursor/skills/*/SKILL.md → installed skills list
  └─ Grep docs/skill-guides/*.md → documented skills set

    ↓

Phase 2: Gap Analysis
  ├─ Cross-reference → undocumented skills list
  └─ Categorize → existing guide vs new guide file

    ↓

Phase 3: Generation (parallel, max 4 subagents)
  ├─ New guide files → create numbered .md files
  └─ Existing guides → append sections + update summary tables

    ↓

Phase 4: README Update
  ├─ Add/update rows in core skills table
  ├─ Update skill counts and header total
  └─ Update mermaid diagram and workflow commands

    ↓

Phase 5: Report
  └─ Summary of files created, updated, skills documented
```

## Workflow

### Phase 1 — Inventory

1. **Discover installed skills**:

```bash
find .cursor/skills -maxdepth 2 -name "SKILL.md" -type f | sort
```

Record each skill name (parent directory name) and path.

Exclude skills from external locations (only `.cursor/skills/` within the workspace).

2. **Discover documented skills**:

For each file in `docs/skill-guides/*.md` (excluding `00-template.md` and `README.md`), grep for skill section headers (`## <skill-name>` or backtick references in summary tables).

Build a set of `{skill-name → guide-file}` mappings.

### Phase 2 — Gap Analysis

1. Compute the difference: `installed_skills - documented_skills = undocumented_skills`.

2. For each undocumented skill, determine its target guide file using the category mapping in [references/category-mapping.md](references/category-mapping.md). The mapping uses prefix matching and keyword rules.

3. Group results:
   - **Existing guide additions**: skills that belong in an existing numbered guide
   - **New guide files**: skills that need a new category file (when 3+ unrelated skills share no existing category)

4. If `--dry-run` is set, present the gap analysis report and stop.

5. If `--scope <pattern>` is set, filter undocumented skills to only those matching the glob pattern.

### Phase 3 — Generation

For each undocumented skill:

1. **Read source**: Read `.cursor/skills/<name>/SKILL.md` to extract:
   - Description and trigger conditions (from frontmatter)
   - Key features and workflow (from body)
   - Anti-patterns / "Do NOT use" clauses
   - Related skills

2. **Generate guide section** following the template in [docs/skill-guides/00-template.md](docs/skill-guides/00-template.md):
   - Overview (description, skill file path, type)
   - Key features (3-5 bullets)
   - Trigger methods (slash command, natural language, auto-activation)
   - When NOT to use (with alternative skill references)
   - 5 usage examples (situation, prompt, expected result)
   - Related skills table
   - Tips and caveats

3. **Write to target**:
   - For new guide files: create `docs/skill-guides/NN-category-name.md` with header, summary table, and all sections
   - For existing guides: append new sections and update the summary table skill count

4. All documentation must be in Korean following existing guide conventions.

5. Use parallel subagents (max 4) when generating 2+ new guide files simultaneously.

### Phase 4 — README Update

Update [docs/skill-guides/README.md](docs/skill-guides/README.md):

1. **Header**: Update the total skill count (e.g., "400개+" → "410개+")

2. **Mermaid diagram**: Add new category nodes to the `coreSkills` subgraph if new guide files were created. Add corresponding edges from `MC`.

3. **Workflow commands table**: Add rows for any new slash commands discovered in the newly documented skills.

4. **Decision flowchart**: Add branches for new categories if applicable.

5. **Core skills table**: Add new rows for new guide files. Update skill counts in modified existing rows.

If `--readme-only` is set, skip Phases 1-3 and recount all skills from existing guide files to update counts.

### Phase 5 — Report

Present a summary:

```
Skill Guide Sync Report
========================
Installed skills:  [N]
Previously documented: [N]
Newly documented: [N]
Remaining undocumented: [N]

Files created:  [list]
Files updated:  [list]

Per-category breakdown:
  [guide-file]: +[N] skills ([skill names])
```

## Scoping Rules

When `--scope <pattern>` is provided:
- Only process skills whose names match the glob pattern
- Still perform the full inventory for accurate gap counting
- Only generate docs for matching skills
- Only update README entries related to the matching category

## Error Handling

| Error | Action |
|-------|--------|
| No undocumented skills found | Report "All skills are documented" and exit |
| Source SKILL.md missing frontmatter | Skip skill, log warning |
| Guide file write conflict | Show diff, ask user to resolve |
| Category not found in mapping | Propose a new category name, ask user to confirm |
| README.md parse error | Show the problematic section, suggest manual fix |

## Examples

### Example 1: Full documentation sync

User says: "문서화 안 된 스킬들 모두 문서화해줘"

Actions:
1. Inventory: 415 installed skills, 400 documented
2. Gap: 15 undocumented skills across 3 categories
3. Generate: 1 new guide file + 2 existing guide updates
4. README: add 1 row, update 2 counts
5. Report: 15 skills documented, 3 files modified

### Example 2: Dry-run gap analysis

User says: "/skill-guide-sync --dry-run"

Actions:
1. Inventory and gap analysis only
2. Present: "Found 8 undocumented skills: [list] → would go in [guide files]"
3. No files modified

### Example 3: Scoped documentation

User says: "/skill-guide-sync --scope role-*"

Actions:
1. Filter to role-* skills only
2. Document any undocumented role-* skills
3. Update only the role-based-analysis guide and README

### Example 4: README-only update

User says: "/skill-guide-sync --readme-only"

Actions:
1. Recount all skills from existing guide files
2. Update README counts, mermaid diagram, and table
3. No guide content generated

### Example 5: New category discovery

User says: "/skill-guide-sync" (and 5 new `calendar-*` skills exist)

Actions:
1. Gap analysis finds 5 `calendar-*` skills with no matching guide
2. Propose new category: "31-calendar-integration.md"
3. User confirms → generate new guide file with all 5 skills
4. Update README with new row and diagram node

## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
