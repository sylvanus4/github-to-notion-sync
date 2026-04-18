## Ubiquitous Language

Extract a DDD-style ubiquitous language glossary from the codebase or current conversation, ensuring the team shares the same terms.

### Usage

```
/ubiquitous-language                   # extract from current codebase
/ubiquitous-language src/domain/       # extract from specific directory
/ubiquitous-language --conversation    # extract from current conversation context
```

### Workflow

1. **Scan** — Identify domain terms, entity names, and ambiguous vocabulary
2. **Define** — Write precise definitions for each term
3. **Detect conflicts** — Find terms used with different meanings across modules
4. **Generate glossary** — Output a structured glossary markdown document
5. **Recommend** — Suggest term unifications and naming improvements

### Execution

Read and follow the `terminology-guardian` skill (`.cursor/skills/planning/terminology-guardian/SKILL.md`) for glossary maintenance, term drift detection, and consistency enforcement across PRDs, code, designs, and policies.

### Examples

Extract glossary from codebase:
```
/ubiquitous-language
```

Extract from a specific domain module:
```
/ubiquitous-language src/entities/billing/
```
