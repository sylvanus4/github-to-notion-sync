---
name: docs-tutor-setup
description: >-
  Transform the project's docs/ markdown files into an Obsidian StudyVault
  with structured concept notes, practice questions, dashboards, and
  interlinking. Use when the user asks to "generate a study vault", "create
  study notes from docs", "docs-tutor-setup", or wants to learn the platform
  documentation systematically. Do NOT use for interactive quizzing (use
  docs-tutor) or for general documentation writing (use technical-writer).
  Korean triggers: "학습 노트", "StudyVault 생성".
---

# Docs Tutor Setup — Markdown Docs to Obsidian StudyVault

## Scope

Converts markdown files under `docs/` into a structured Obsidian StudyVault at the project root (`StudyVault/`). The vault contains concept notes, practice questions with active recall, a dashboard with MOC, and full interlinking.

## Allowed Tools

Read, Write, Glob, Grep, Shell (for directory listing only), AskQuestion

## Boundary Rules

1. **Source**: Only read from `docs/` and its subdirectories.
2. **Output**: Only write to `StudyVault/` at the project root.
3. **No modifications** to source `docs/` files.
4. **Skip**: `docs/tasks/`, `docs/ai/`, `.git/`, `node_modules/`, any `.tsv` files.

## Selective Scope

The user may specify a target subdirectory. If provided, only process that subdirectory:

```
/docs-tutor-setup                           # all of docs/
/docs-tutor-setup docs/platform-overview    # single section
/docs-tutor-setup docs/infrastructure docs/on-call  # multiple sections
```

If no argument, scan all of `docs/` and present the discovered sections for user confirmation before proceeding.

---

## Phase D1: Source Discovery

1. **Glob** `docs/**/*.md` to find all markdown files.
2. **Group by top-level subdirectory** under `docs/` — each becomes a "section."
   - Nested subdirectories (e.g., `docs/planned/agent-sandbox-platform/`) are treated as a single section with subtopics.
3. **Build section inventory table**:

   | Section | Files | Description |
   |---------|-------|-------------|
   | platform-overview | 8 | Platform architecture and security |
   | infrastructure | 12 | Deployment and infra docs |
   | ... | ... | ... |

4. **Present to user** for confirmation. Ask if any sections should be excluded.
5. **Read each file** — understand scope, structure, depth. For large sections (50+ files), read the README or index file first, then sample 5-10 representative files.

### Source Content Mapping (MANDATORY)

- Read the README/index of every section to understand its scope.
- Build verified mapping: `{ section → actual_topics → file_list }`.
- Flag non-documentation files (meeting notes, scratch files) for exclusion.
- Present mapping to user for verification before proceeding.

## Phase D2: Content Analysis

1. **Identify topic hierarchy** — sections, subsections, domain divisions.
2. **Separate** concept content vs. operational procedures vs. specifications.
3. **Map dependencies** between topics (e.g., infrastructure depends on platform-overview).
4. **Identify key patterns** — architecture diagrams, API specs, decision records, runbooks.
5. **Full topic checklist (MANDATORY)** — every topic/subtopic listed. This drives all subsequent phases.

### Equal Depth Rule

Even a briefly mentioned subtopic MUST get a full dedicated note supplemented with the source material and contextual knowledge about the platform.

### Content Classification

Classify each topic into one of:
- **Architecture** — system design, component boundaries, data flow
- **API/Interface** — endpoints, contracts, request/response formats
- **Infrastructure** — deployment, Kubernetes, networking, CI/CD
- **Operations** — runbooks, incident response, monitoring, alerting
- **Feature Spec** — PRDs, planned features, requirements
- **Security** — auth, RBAC, secrets, compliance
- **Testing** — QA scenarios, test strategies, E2E patterns

## Phase D3: Tag Standard

Define tag vocabulary before creating notes:

- **Format**: English, lowercase, kebab-case (e.g., `#arch-microservice`, `#ops-incident`)
- **Categories**:
  - `#arch-*` — architecture concepts
  - `#infra-*` — infrastructure and deployment
  - `#api-*` — API endpoints and contracts
  - `#ops-*` — operational procedures
  - `#security-*` — security and compliance
  - `#feature-*` — feature specifications
  - `#test-*` — testing strategies
  - `#admin-*` — admin portal features
- **Registry**: Only registered tags allowed. Detail tags co-attach parent category tag.
- **Present registry** to user for approval before proceeding.

## Phase D4: Vault Structure

Create `StudyVault/` at project root with numbered folders:

```
StudyVault/
  00-Dashboard/           # MOC + Quick Reference
  01-<Section1>/          # Concept notes per domain
  02-<Section2>/
  ...
  NN-<SectionN>/
```

Per [templates.md](references/templates.md) folder structure. Group 3-5 related concepts per file when topics are small.

## Phase D5: Dashboard Creation

Create `00-Dashboard/`: MOC, Quick Reference. See [templates.md](references/templates.md).

### MOC (Map of Content)

- **Section Map**: Table of all sections with purpose + links to concept notes
- **Practice Notes**: Links to all practice question files
- **Study Tools**: Links to Quick Reference
- **Tag Index**: Tag registry with hierarchy rules
- **Weak Areas**: Placeholder for areas needing review (populated by tutor skill)
- **Learning Path**: Recommended reading order for platform newcomers

### Quick Reference

- Every section heading includes `→ [[Concept Note]]` link
- One-line summary table per key concept/term
- Grouped by domain category
- Key architecture patterns and infrastructure commands
- "Must-know concepts" section at bottom with `→ [[Note]]` links

## Phase D6: Concept Notes

Create concept notes per [templates.md](references/templates.md). Key rules:

- **YAML frontmatter**: `source_docs` (list of source file paths), `section`, `keywords` (MANDATORY)
- **source_docs MUST match verified Phase D1 mapping** — never guess from filenames
- `[[wiki-links]]` for cross-references
- Callouts: `> [!tip]`, `> [!important]`, `> [!warning]`
- **Comparison tables over prose** — always prefer structured tables
- **ASCII diagrams** for architecture flows, data pipelines, request paths
- **Simplification-with-exceptions**: general statements must note edge cases
- Content language matches source (Korean docs → Korean notes, English → English)
- Tags always in English

## Phase D7: Practice Questions

Create practice questions per [templates.md](references/templates.md). Key rules:

- Every section folder MUST have a practice file (8+ questions)
- **Active recall**: answers use `> [!answer]- 정답 보기` fold callout
- Patterns use `> [!hint]-` / `> [!summary]-` fold callouts
- **Question type diversity**: tag `[recall]`, `[application]`, `[analysis]`, `[troubleshooting]` in heading
  - ≥40% recall, ≥20% application, ≥2 analysis, ≥2 troubleshooting per file
- `## Related Concepts` with `[[wiki-links]]`

### Platform-Specific Question Types

- **Architecture decisions**: "Why does the platform use X pattern instead of Y?"
- **Operational scenarios**: "What is the incident response procedure when X occurs?"
- **Configuration**: "How would you configure X for production deployment?"
- **Troubleshooting**: "Given symptom X in the logs, what is the most likely root cause?"
- **API behavior**: "What HTTP status code is returned when X happens?"
- **Security**: "What RBAC role is required to perform X action?"

## Phase D8: Interlinking

1. `## Related Notes` on every concept note.
2. MOC links to every concept + practice note.
3. Cross-link concept ↔ practice; siblings reference each other.
4. Quick Reference sections → `[[Concept Note]]` links.
5. Weak Areas → relevant note links.
6. Cross-section links where topics depend on each other (e.g., infrastructure notes link to architecture notes).

## Phase D9: Self-Review (MANDATORY)

Verify against [quality-checklist.md](references/quality-checklist.md). Fix and re-verify until all checks pass.

Report completion with:
- Number of sections processed
- Number of concept notes created
- Number of practice questions generated
- Any sections skipped and why

---

## Language

- **Content**: Match source material language (Korean source → Korean notes, English → English)
- **Tags/keywords**: ALWAYS English kebab-case
- **Dashboard labels**: Korean (정답 보기, 핵심 패턴, 패턴 요약)
- **Fold callout labels**: Korean (정답 보기, 클릭하여 보기)

## Examples

### Example 1: Standard usage
**User says:** "docs tutor setup" or request matching the skill triggers
**Actions:** Execute the skill workflow as specified. Verify output quality.
**Result:** Task completed with expected output format.

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Unexpected input format | Validate input before processing; ask user for clarification |
| External service unavailable | Retry with exponential backoff; report failure if persistent |
| Output quality below threshold | Review inputs, adjust parameters, and re-run the workflow |
