# Quality Checklist — Self-Review

Before reporting completion, verify every item. Fix and re-verify if any check fails.

---

## Source Traceability

- [ ] Every section's content verified by reading README/index + representative files
- [ ] Source content mapping table built and verified in Phase D1
- [ ] Every `source_docs` frontmatter matches verified mapping — no guesses from filenames
- [ ] Non-documentation files excluded and documented
- [ ] Excluded sections documented in MOC

## Coverage

- [ ] Every topic from Phase D2 checklist has a concept note
- [ ] No source topic missing or underrepresented
- [ ] Equal depth rule followed — briefly mentioned subtopics still get full notes
- [ ] Content classification applied (Architecture / API / Infrastructure / Operations / Feature Spec / Security / Testing)

## Tags

- [ ] All tags: English kebab-case, from registry only
- [ ] Tag Index in MOC includes hierarchy rules
- [ ] Detail tags co-attached with parent category tags
- [ ] No unregistered tags used

## Structure & Formatting

- [ ] Every note has YAML frontmatter: `source_docs`, `section`, `keywords`
- [ ] Every concept note has overview table + related notes section
- [ ] Architecture/flow topics have ASCII diagrams
- [ ] Notes are concise (tables over prose)
- [ ] Simplified statements include exception caveats (`> [!warning]`)
- [ ] Content language matches source material language
- [ ] Tags and keywords are always English

## Dashboard

- [ ] MOC: Section Map + Practice Notes + Study Tools + Tag Index + Weak Areas + Learning Path
- [ ] MOC links to every concept note AND practice note
- [ ] Weak Areas section exists (placeholder for tutor skill updates)
- [ ] Learning Path provides recommended reading order

## Quick Reference

- [ ] Key concepts per section included
- [ ] Every section heading links to concept note via `→ [[Note]]`
- [ ] Architecture patterns table present
- [ ] Must-know concepts summary at bottom

## Practice — Active Recall

- [ ] Every section folder has practice file (8+ questions)
- [ ] All answers use `> [!answer]- 정답 보기` fold — never immediately visible
- [ ] Key Patterns: `> [!hint]-` fold; Pattern Summary: `> [!summary]-` fold
- [ ] `## Related Concepts` with backlinks in every practice file
- [ ] Question type diversity: ≥40% recall, ≥20% application, ≥2 analysis, ≥2 troubleshooting per file
- [ ] Platform-specific question types included (architecture decisions, operational scenarios, configuration, troubleshooting)

## Interlinking

- [ ] Every concept note has `## Related Notes`
- [ ] `[[wiki-links]]` for all cross-references
- [ ] Siblings reference each other; concept ↔ practice cross-linked
- [ ] Cross-section links exist where topics depend on each other
- [ ] MOC links to all concept and practice notes
- [ ] Quick Reference sections link to concept notes

## Boundary Compliance

- [ ] Source files read only from `docs/` and subdirectories
- [ ] Output files written only to `StudyVault/`
- [ ] No modifications to source `docs/` files
- [ ] No absolute file paths in notes or frontmatter
- [ ] `docs/tasks/`, `docs/ai/`, `.tsv` files excluded
