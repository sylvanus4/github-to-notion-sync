## Doc Coauthor

Structured co-authoring workflow for documents — proposals, technical specs, decision docs, and reports with iterative refinement.

### Usage

```
/doc-coauthor "architecture decision record"   # start co-authoring
/doc-coauthor --refine draft.md                # refine an existing draft
/doc-coauthor --type proposal                  # specific document type
```

### Workflow

1. **Context transfer** — Gather document goals, audience, and constraints
2. **Structure** — Create document outline with sections and key points
3. **Draft** — Write initial content section by section
4. **Iterate** — Refine through feedback cycles: clarity, completeness, tone
5. **Verify** — Ensure the document works for its intended readers

### Execution

Read and follow the `anthropic-doc-coauthoring` skill (`.cursor/skills/anthropic/anthropic-doc-coauthoring/SKILL.md`) for the structured co-authoring workflow with iterative refinement.

### Examples

Co-author an ADR:
```
/doc-coauthor "ADR: choosing between PostgreSQL and CockroachDB"
```

Refine an existing draft:
```
/doc-coauthor --refine docs/proposals/caching-strategy.md
```
