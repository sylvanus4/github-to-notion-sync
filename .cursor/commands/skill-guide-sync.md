## Skill Guide Sync

Scan all installed skills, identify undocumented ones, generate guide documentation following the standard template, and update the README index.

### Usage

```
/skill-guide-sync                    # full sync (scan + generate + update README)
/skill-guide-sync --dry-run          # gap analysis only, no file changes
/skill-guide-sync --scope tab-*      # only document skills matching prefix
/skill-guide-sync --scope role-*     # only document role-* skills
/skill-guide-sync --readme-only      # only update README.md counts and tables
```

### Workflow

1. **Inventory** — Glob installed skills and grep documented skills from guides
2. **Gap analysis** — Cross-reference to find undocumented skills
3. **Categorize** — Map each to existing guide or propose new guide file
4. **Generate** — Write guide sections following `docs/skill-guides/00-template.md`
5. **README update** — Update counts, tables, mermaid diagram in README.md
6. **Report** — Summary of changes made

### Execution

Read and follow the `skill-guide-generator` skill (`.cursor/skills/skill-guide-generator/SKILL.md`) for the full pipeline, category mapping rules, and error handling.

### Examples

Full documentation sync:
```
/skill-guide-sync
```

Check what's missing without making changes:
```
/skill-guide-sync --dry-run
```

Document only trading skills:
```
/skill-guide-sync --scope trading-*
```

Just refresh README counts:
```
/skill-guide-sync --readme-only
```
