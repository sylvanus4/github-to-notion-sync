---
description: "Convert any plan, analysis, or answer into an executable checklist with checkboxes, grouping, and priority"
argument-hint: "<content to convert into checklist>"
---

# Actionable Checklist

Transform any content into a structured, executable checklist with checkboxes, grouped by phase or category.

## Usage

```
/checklist Deploy a new microservice to production
/checklist [paste meeting notes here]
/checklist --prioritized Migrate database from MySQL to PostgreSQL
/checklist --with-owners Sprint planning tasks for the auth team
/checklist 신규 기능 출시 전 점검 사항 정리해줘
```

## Your Task

User input: $ARGUMENTS

### Mode Selection

Parse `$ARGUMENTS` for flags:

- **No flags** — Grouped checklist with checkboxes (default)
- `--prioritized` — Add P0/P1/P2 priority labels to each item
- `--with-owners` — Add `@owner` placeholder after each item
- `--with-deadlines` — Add deadline placeholders `(by: YYYY-MM-DD)`
- `--flat` — No grouping, single flat list

### Workflow

1. **Parse input** — Accept pasted text, a topic description, or a file reference
2. **Extract actionable items** — Identify every discrete task or verification step
3. **De-duplicate** — Merge overlapping items
4. **Order by dependency** — Ensure prerequisites come before dependent items
5. **Group by phase/category** — Organize into logical sections (e.g., Preparation, Execution, Verification, Cleanup)
6. **Format as checkboxes** — Use `- [ ]` markdown format
7. **Add metadata** — Apply priority, owner, or deadline labels based on selected flags

### Output Format

```
## Checklist: [Title]

### Phase 1: [Category Name]
- [ ] [Action item 1]
- [ ] [Action item 2]

### Phase 2: [Category Name]
- [ ] [Action item 3]
- [ ] [Action item 4]

### Verification
- [ ] [Verification step]
```

### Constraints

- Each item must start with an action verb (Create, Verify, Run, Configure, etc.)
- Each item must be completable by one person in one sitting
- If an item is too broad, split it into sub-items using nested `- [ ]`
- Never include vague items like "Think about X" — make them concrete
