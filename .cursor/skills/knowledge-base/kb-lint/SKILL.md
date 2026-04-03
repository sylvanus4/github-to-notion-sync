---
name: kb-lint
description: >-
  Run health checks over an LLM Knowledge Base wiki to find inconsistencies,
  stale data, broken links, missing coverage, imputable gaps, and interesting
  connection candidates. Generates an actionable report with severity-ranked
  issues and auto-fix suggestions. Optionally performs web searches to
  impute missing data. Use when the user asks to "lint the KB", "health
  check knowledge base", "kb lint", "check wiki consistency", "find gaps
  in KB", "improve wiki quality", or wants to incrementally enhance the
  wiki's data integrity.
  Do NOT use for compiling the wiki (use kb-compile).
  Do NOT use for querying the KB (use kb-query).
  Do NOT use for rebuilding indexes (use kb-index).
  Korean triggers: "KB 린트", "위키 건강 점검", "지식베이스 점검",
  "KB 일관성 검사", "위키 품질 검사".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
  tags: ["knowledge-base", "lint", "quality", "health-check"]
---

# KB Lint — Wiki Health Checker

Run comprehensive health checks over a Knowledge Base wiki to detect issues, suggest improvements, and incrementally enhance data quality. Inspired by Karpathy's approach of running LLM "health checks" to clean up and enhance the wiki.

## Health Check Dimensions

| Dimension | What It Checks | Severity |
|-----------|---------------|----------|
| **Consistency** | Contradictory claims across articles | High |
| **Completeness** | Missing coverage of important subtopics | Medium |
| **Freshness** | Stale data, outdated references | Medium |
| **Links** | Broken `[[wikilinks]]`, orphan articles | High |
| **Structure** | Missing frontmatter, inconsistent formatting | Low |
| **Connections** | Missed cross-references, isolated concepts | Low |
| **Accuracy** | Verifiable claims that may be wrong | High |
| **Redundancy** | Duplicate or near-duplicate content | Medium |

## Workflow

### Step 1: Scan Wiki

Read all articles and index files from `knowledge-bases/{topic}/wiki/`.

### Step 2: Run Checks

#### Check 1: Broken Links

Scan for `[[wikilink]]` references that point to nonexistent files:

```
⚠ BROKEN LINK: [[attention-heads]] referenced in concepts/transformer.md
  → No file: wiki/concepts/attention-heads.md
  Suggestion: Create article or fix link to [[multi-head-attention]]
```

#### Check 2: Orphan Articles

Find articles not referenced by any other article or the index:

```
⚠ ORPHAN: wiki/concepts/layer-normalization.md
  → Not referenced by any other article
  Suggestion: Add backlinks from [[transformer-block]], [[training-stability]]
```

#### Check 3: Consistency

Compare claims across articles for contradictions:

```
⚠ INCONSISTENCY:
  wiki/concepts/bert.md says: "BERT uses 12 attention heads"
  wiki/concepts/transformer-sizes.md says: "BERT-base has 8 heads"
  Suggestion: Verify against raw source and correct
```

#### Check 4: Completeness

Identify concepts mentioned but never given their own article:

```
ℹ MISSING ARTICLE: "dropout regularization"
  → Mentioned in 4 articles but has no dedicated concept page
  Suggestion: Create wiki/concepts/dropout-regularization.md
```

#### Check 5: Stale Data

Check `last_compiled` dates and source publication dates:

```
ℹ STALE: wiki/concepts/gpt-architecture.md
  → Last compiled: 2025-06-15 (10 months ago)
  → Newer raw sources exist: raw/gpt4o-paper.md (2026-03-01)
  Suggestion: Recompile with latest sources
```

#### Check 6: Missing Connections

Identify articles that likely should cross-reference but don't:

```
ℹ SUGGESTED CONNECTION: 
  [[positional-encoding]] and [[rotary-embeddings]]
  → Both discuss position representation but don't reference each other
  Suggestion: Add cross-reference or create connection article
```

#### Check 7: Frontmatter Quality

Check for missing or incomplete YAML frontmatter:

```
⚠ MISSING FRONTMATTER: wiki/concepts/beam-search.md
  → No YAML frontmatter found
  Suggestion: Add title, category, related, sources, word_count
```

#### Check 8: Imputable Gaps (with web search)

If `--impute` flag is set, use WebSearch to find data that could fill gaps:

```
ℹ IMPUTABLE GAP: "Latest benchmark results for {model}"
  → KB discusses {model} but benchmark data is from 2025
  → Web search found: updated benchmarks from {date}
  Suggestion: kb-ingest the source, then kb-compile to update
```

### Step 3: Generate Report

Write the full report to `knowledge-bases/{topic}/outputs/lint-report-{date}.md`:

```markdown
# KB Lint Report: {topic}

**Date:** {date}
**Articles scanned:** {N}
**Issues found:** {total}

## Summary

| Severity | Count |
|----------|-------|
| 🔴 High | {N} |
| 🟡 Medium | {N} |
| 🔵 Low | {N} |

## High Priority

### 1. [BROKEN LINK] ...
### 2. [INCONSISTENCY] ...

## Medium Priority

### 3. [COMPLETENESS] ...

## Low Priority

### 4. [CONNECTION] ...

## Suggested New Articles

1. **dropout-regularization** — mentioned 4 times, no article
2. **gradient-clipping** — mentioned 3 times, no article

## Suggested Connections

1. [[positional-encoding]] ↔ [[rotary-embeddings]]
2. [[attention-mechanism]] ↔ [[flash-attention]]

## Further Questions to Explore

1. "How do recent sparse attention methods compare to standard attention?"
2. "What are the memory-efficiency tradeoffs of different positional encodings?"
```

### Step 4: Auto-Fix (Optional)

If `--fix` is specified, automatically fix trivial issues:
- Add missing frontmatter (inferred from content)
- Fix broken links where the correct target is obvious
- Add missing backlinks
- Update stale word counts

### Step 5: Report to User

```
✓ KB Lint complete: {topic}
  Issues: {high} high, {medium} medium, {low} low
  Report: knowledge-bases/{topic}/outputs/lint-report-{date}.md
  
  Top actions:
  1. Fix {N} broken links
  2. Create {N} missing articles
  3. Resolve {N} inconsistencies
```

## Examples

### Example 1: Basic lint

**User says:** "Lint my ML knowledge base"

**Actions:**
1. Scan all wiki articles
2. Run all 8 checks
3. Generate report
4. Present summary with top actions

### Example 2: Lint with auto-fix

**User says:** "Lint the KB and fix what you can"

**Actions:**
1. Run all checks
2. Auto-fix trivial issues (frontmatter, backlinks, word counts)
3. Report what was fixed and what needs manual attention

### Example 3: Lint with gap imputation

**User says:** "Check my KB for gaps and search the web for missing info"

**Actions:**
1. Run all checks including Check 8 (imputable gaps)
2. Use WebSearch for each gap
3. Suggest specific sources to ingest
4. Report findings

## Error Handling

| Error | Symptom | Action |
|-------|---------|--------|
| No wiki | Empty wiki/ directory | Prompt to run kb-compile first |
| Very large KB | > 200 articles | Process in batches, summarize checks |
| Web search fails | API unavailable for --impute | Skip imputation, note in report |
