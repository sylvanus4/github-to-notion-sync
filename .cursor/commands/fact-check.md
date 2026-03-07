## Fact Check

Verify the factual accuracy of a document against the actual codebase, correct inaccuracies in place, and add a verification summary.

### Usage

```
/fact-check <file-path>          # verify specific file (.html, .md, or any text)
/fact-check                      # verify most recent HTML in ~/.agent/diagrams/
```

### Workflow

1. **Determine target** — Use the provided file path, or find the most recently modified `.html` file in `~/.agent/diagrams/`
2. **Auto-detect document type** — HTML review pages, plan/spec documents, or any document with code claims
3. **Phase 1: Extract claims** — Read the file and extract every verifiable factual claim:
   - Quantitative (line counts, file counts, function counts)
   - Naming (function names, type names, file paths)
   - Behavioral (what code does, before/after comparisons)
   - Structural (architecture claims, dependency relationships)
   - Temporal (git history claims, commit attributions)
4. **Phase 2: Verify** — For each claim, go to the source:
   - Re-read every referenced file, check signatures and behavior
   - Re-run git commands and compare against document's numbers
   - Classify each claim: Confirmed / Corrected / Unverifiable
5. **Phase 3: Correct in place** — Fix incorrect numbers, names, paths, behavior descriptions. Preserve layout, CSS, and structure.
6. **Phase 4: Add verification summary** — Insert summary (total checked, confirmed, corrected, unverifiable) matching the document's existing styling
7. **Phase 5: Report** — Tell user what was checked and corrected

This is a fact-checker, not a re-review. It does not second-guess analysis or design judgments — it verifies data matches reality.

### Execution

Read and follow the `visual-explainer` skill (`.cursor/skills/visual-explainer/SKILL.md`) for CSS patterns when styling the verification summary in HTML documents.

### Examples

Verify a diff review:
```
/fact-check ~/.agent/diagrams/auth-diff-review.html
```

Verify a plan document:
```
/fact-check docs/plans/migration-spec.md
```

Verify the latest output:
```
/fact-check
```
