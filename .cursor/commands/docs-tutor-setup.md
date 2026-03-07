## Docs Tutor Setup

Transform `docs/` markdown files into an Obsidian-compatible StudyVault with concept notes, practice questions, dashboards, and full interlinking.

### Usage

```
# Generate StudyVault from all docs
/docs-tutor-setup

# Target specific sections
/docs-tutor-setup docs/platform-overview
/docs-tutor-setup docs/infrastructure docs/on-call

# Regenerate a section (overwrites existing)
/docs-tutor-setup docs/admin-portal --force
```

### Workflow

1. **Source Discovery** — Scan `docs/` for markdown files, group by subdirectory as sections
2. **Content Analysis** — Identify topic hierarchy, dependencies, and content classification
3. **Tag Standard** — Define English kebab-case tag registry (`#arch-*`, `#infra-*`, `#ops-*`, etc.)
4. **Vault Structure** — Create `StudyVault/` with numbered section folders
5. **Dashboard** — Generate MOC (section map, practice links, tag index, learning path) + Quick Reference
6. **Concept Notes** — Structured notes with YAML frontmatter, comparison tables, ASCII diagrams
7. **Practice Questions** — 8+ questions per section with fold callout answers (recall/application/analysis/troubleshooting)
8. **Interlinking** — Cross-reference all notes with `[[wiki-links]]`
9. **Self-Review** — Verify against quality checklist, fix issues

### Output

```
StudyVault/
  00-Dashboard/          # MOC + Quick Reference
  01-<Section1>/         # Concept notes + practice questions
  02-<Section2>/
  ...
```

### Execution

Read and follow the `docs-tutor-setup` skill (`.cursor/skills/docs-tutor-setup/SKILL.md`) for phase details, templates, and quality checklist.
