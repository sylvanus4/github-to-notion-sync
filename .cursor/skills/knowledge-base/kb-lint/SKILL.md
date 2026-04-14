---
name: kb-lint
description: >-
  Run health checks over an LLM Knowledge Base wiki to find inconsistencies,
  stale data, broken links, missing coverage, imputable gaps, evidence
  timeline issues, cross-topic gaps, and interesting connection candidates.
  Computes Unified Freshness Score (0-100) per article and topic-level
  freshness summaries. Validates evidence diversity and compiled truth
  completeness. Detects cross-topic entity gaps, coverage asymmetry, and
  contradictory claims across topics. Generates an actionable report with
  severity-ranked issues and auto-fix suggestions. Optionally performs web
  searches to impute missing data. Use when the user asks to "lint the KB",
  "health check knowledge base", "kb lint", "check wiki consistency",
  "find gaps in KB", "improve wiki quality", "freshness score", "evidence
  validation", "cross-topic gaps", or wants to incrementally enhance the
  wiki's data integrity.
  Do NOT use for compiling the wiki (use kb-compile).
  Do NOT use for querying the KB (use kb-query).
  Do NOT use for rebuilding indexes (use kb-index).
  Korean triggers: "KB 린트", "위키 건강 점검", "지식베이스 점검",
  "KB 일관성 검사", "위키 품질 검사", "신선도 점수", "증거 검증",
  "크로스토픽 갭".
metadata:
  author: "thaki"
  version: "2.0.0"
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

#### Check 5: Stale Data + Unified Freshness Score

Check `last_compiled` dates and source publication dates. Compute a **Unified Freshness Score (0-100)** for each article:

**Score formula** (weighted average):

| Factor | Weight | Scoring |
|--------|--------|---------|
| `ingested_at` age | 40% | 100 if < 7 days, 80 if < 30, 60 if < 90, 30 if < 180, 0 if > 180 |
| `last_compiled` age | 30% | 100 if < 14 days, 70 if < 60, 40 if < 120, 0 if > 120 |
| Source date spread | 20% | 100 if newest source < 30 days, linear decay to 0 at 365 days |
| `staleness_flag` | 10% | 100 if absent or "fresh", 50 if "review", 0 if "stale" |

**Article-level output:**
```
ℹ FRESHNESS: wiki/concepts/gpt-architecture.md
  → Score: 42/100 (🟡 MEDIUM)
  → ingested_at: 2025-06-15 (10 months ago) → 0/100
  → last_compiled: 2026-01-10 (3 months ago) → 40/100
  → Newest source: 2026-03-01 (41 days ago) → 89/100
  → staleness_flag: absent → 100/100
  Suggestion: Recompile with latest sources
```

**Topic-level freshness summary** (appended to lint report):
```
## Freshness Summary

| Bracket | Count | % |
|---------|-------|---|
| 🟢 Fresh (80-100) | 12 | 55% |
| 🟡 Aging (50-79) | 6 | 27% |
| 🔴 Stale (0-49) | 4 | 18% |

Average freshness: 67/100
Bottom 5 stalest articles: ...
```

#### Check 5b: Evidence Timeline Validation

Consume the `evidence_diversity` and orphan evidence data from `kb-compile` output and validate:

1. **Orphan Evidence Detection** — for each concept article, verify every `## Evidence Timeline` entry has at least one corresponding claim in `## Compiled Truth`. Flag entries that exist in the timeline but are never synthesized:

```
⚠ ORPHAN EVIDENCE: wiki/concepts/gpu-inference-cost.md
  → Evidence Timeline entry [2026-02-14] "NVIDIA H200 pricing at $3.50/hr"
  → Not reflected in any Compiled Truth paragraph
  → Severity: Medium
  Suggestion: Either incorporate into Compiled Truth or mark as superseded
```

2. **Evidence Diversity Validation** — flag articles with `evidence_diversity: low` that rely on a single source or narrow date window:

```
ℹ LOW DIVERSITY: wiki/concepts/model-distillation.md
  → evidence_diversity: low
  → 1 unique source, 1-day date spread, 1 source type
  → Severity: Medium
  Suggestion: Ingest additional sources via kb-ingest to diversify evidence
```

3. **Source-Claim Ratio** — flag articles where the Evidence Timeline has > 2x entries compared to Compiled Truth paragraphs (evidence accumulation without synthesis):

```
ℹ SYNTHESIS GAP: wiki/concepts/rlhf-alignment.md
  → 14 Evidence Timeline entries, 3 Compiled Truth paragraphs
  → Ratio: 4.7:1 (threshold: 2.0:1)
  → Severity: Low
  Suggestion: Recompile to synthesize accumulated evidence
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

#### Check 9: Cross-Topic Gap Detection

When linting with `--all-topics` or when multiple topics are specified, scan across topic boundaries:

1. **Shared Entity, Missing Cross-Reference** — identify entities (company names, model names, technical terms) that appear in 2+ topics but have no `connections/` document or frontmatter `related` link bridging them:

```
ℹ CROSS-TOPIC GAP: Entity "NVIDIA H100"
  → Appears in topics: gpu-infrastructure (5 articles), competitive-intel (3 articles), finance-policies (1 article)
  → No cross-topic connections/ document exists
  → Severity: Medium
  Suggestion: Create a connection article in the most relevant topic, or add cross-topic related links
```

2. **Topic Coverage Asymmetry** — detect when a concept is deeply covered in one topic but only superficially mentioned in another where it should have depth:

```
ℹ COVERAGE ASYMMETRY: "inference cost optimization"
  → Deep coverage in gpu-infrastructure (4 concept articles, 12 raw sources)
  → Shallow mention in finance-policies (1 passing reference, 0 dedicated articles)
  → Severity: Low
  Suggestion: Create dedicated article in finance-policies or add reference link to gpu-infrastructure
```

3. **Contradictory Claims Across Topics** — extend Check 3 (Consistency) across topic boundaries:

```
⚠ CROSS-TOPIC INCONSISTENCY:
  → Topic "competitive-intel" says: "AWS GPU market share is 45%"
  → Topic "finance-policies" says: "AWS GPU market share is 38%"
  → Different source dates: 2026-01 vs 2025-09
  → Severity: High
  Suggestion: Reconcile using the more recent source
```

#### Check 10: Orphan Entity References (MemKraft-inspired)

Scan all wiki articles for entity mentions (bold terms, `[[wikilinks]]`, frontmatter `related` entries) that have no corresponding concept article, connection document, or glossary entry anywhere in the wiki. Unlike Check 4 (Completeness) which looks for frequently-mentioned missing articles, this check focuses on *any* entity reference — including one-off mentions — that resolves to nothing:

```
⚠ ORPHAN ENTITY REF: "LoRA adapter"
  → Referenced in wiki/concepts/fine-tuning-methods.md (bold mention)
  → No article, connection, or glossary entry exists
  → Severity: Medium
  Suggestion: Create wiki/concepts/lora-adapter.md or add to glossary
```

Inspired by MemKraft's entity-integrity assertions that ensure every referenced memory node is reachable in the graph.

**Difference from Check 4:**
- Check 4 uses frequency (mentioned N times) to suggest new articles.
- Check 10 checks every resolvable reference for existence, catching even single-mention orphans that indicate broken knowledge graph edges.

#### Check 11: Unresolved Conflicts (MemKraft-inspired)

Scan `knowledge-bases/{topic}/conflicts/` directories for JSON files where `"resolved": false`. These conflict records are generated by `kb-compile`'s conflict detection (P2) when an article's Compiled Truth is overwritten with materially different facts:

```
⚠ UNRESOLVED CONFLICT: competitive-intel/cloud-pricing-2026-04-14.json
  → Entity: "AWS GPU hourly rate"
  → Old fact: "$3.50/hr for p5.48xlarge"
  → New fact: "$3.20/hr for p5.48xlarge"
  → Detected: 2026-04-14
  → Severity: High
  Suggestion: Review conflict, verify correct value, mark resolved: true
```

Inspired by MemKraft's conflict detection mechanism that flags contradictory facts across memory nodes and requires explicit resolution.

**Aggregation:**
```
ℹ CONFLICT SUMMARY for topic "competitive-intel":
  → Total conflict files: 8
  → Unresolved: 3 (HIGH if > 0)
  → Oldest unresolved: 2026-03-28 (17 days ago)
  Suggestion: Review and resolve conflicts before next compilation
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

## Freshness Summary

| Bracket | Count | % |
|---------|-------|---|
| 🟢 Fresh (80-100) | {N} | {P}% |
| 🟡 Aging (50-79) | {N} | {P}% |
| 🔴 Stale (0-49) | {N} | {P}% |

Average freshness: {score}/100
Bottom 5 stalest: ...

## Evidence Timeline Health

- Orphan evidence entries: {N}
- Low-diversity articles: {N}
- Synthesis gaps (ratio > 2:1): {N}

## Cross-Topic Gaps

- Shared entities without cross-references: {N}
- Coverage asymmetries: {N}
- Cross-topic inconsistencies: {N}

## Suggested New Articles

1. **dropout-regularization** — mentioned 4 times, no article
2. **gradient-clipping** — mentioned 3 times, no article

## Suggested Connections

1. [[positional-encoding]] ↔ [[rotary-embeddings]]
2. [[attention-mechanism]] ↔ [[flash-attention]]

## Orphan Entity References

| Entity | File | Reference Type |
|--------|------|---------------|
| {entity} | {file} | {bold/wikilink/frontmatter} |

Total orphan refs: {N}

## Unresolved Conflicts

| Conflict File | Entity | Age (days) |
|---------------|--------|------------|
| {file} | {entity} | {days} |

Total conflicts: {N}, Unresolved: {M}, Oldest: {date}

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

## CI Mode (`--ci`)

When invoked with `--ci` flag, output a machine-readable JSON object instead of the human-readable markdown report. Designed for GitHub Actions and automated pipelines.

```json
{
  "topic": "ai-knowledge-bases",
  "timestamp": "2026-04-04T12:00:00Z",
  "articles_scanned": 11,
  "issues": {
    "high": 0,
    "medium": 2,
    "low": 3,
    "total": 5
  },
  "orphan_entity_refs": {
    "count": 3,
    "entities": ["LoRA adapter", "speculative decoding", "RLHF"]
  },
  "unresolved_conflicts": {
    "count": 2,
    "oldest_days": 17,
    "files": ["cloud-pricing-2026-04-14.json", "gpu-specs-2026-04-10.json"]
  },
  "pass": true,
  "findings": [
    {
      "severity": "medium",
      "check": "completeness",
      "message": "Missing dedicated article for 'dropout regularization'",
      "file": null,
      "suggestion": "Create wiki/concepts/dropout-regularization.md"
    },
    {
      "severity": "medium",
      "check": "orphan_entity_refs",
      "message": "Entity 'LoRA adapter' referenced but has no article or glossary entry",
      "file": "wiki/concepts/fine-tuning-methods.md",
      "suggestion": "Create wiki/concepts/lora-adapter.md or add to glossary"
    },
    {
      "severity": "high",
      "check": "unresolved_conflicts",
      "message": "Unresolved conflict for 'AWS GPU hourly rate' (17 days old)",
      "file": "conflicts/cloud-pricing-2026-04-14.json",
      "suggestion": "Review conflict, verify correct value, mark resolved: true"
    }
  ]
}
```

`pass` is `true` when `high == 0`. CI pipelines can gate on `jq '.pass'` to fail the build on critical issues.

The CLI wrapper supports this via: `python scripts/kb_cli.py lint-report {topic} --ci`

## Error Handling

| Error | Symptom | Action |
|-------|---------|--------|
| No wiki | Empty wiki/ directory | Prompt to run kb-compile first |
| Very large KB | > 200 articles | Process in batches, summarize checks |
| Web search fails | API unavailable for --impute | Skip imputation, note in report |

## Gotchas

- **Symptom:** Flood of cross-topic "gaps" (Check 9). **Root cause:** Same entity, intentional different angles per topic. **Correct approach:** Verify missing coverage vs deliberate separation before acting.
- **Symptom:** Reference articles (glossaries) drag freshness down. **Root cause:** Unified score treats age uniformly. **Correct approach:** Exclude or down-weight frontmatter-marked evergreen articles when interpreting scores.
- **Symptom:** "Low diversity" on one comprehensive source. **Root cause:** Timeline rule counts entries, not depth. **Correct approach:** Use manual review for single-source-but-thorough articles.

## Constraints

- Lint reads compiled `wiki/` only; run **kb-compile** first.
- Check 9 needs at least two topics; single-topic runs skip or no-op cross-topic detection.
- Freshness decays over calendar time by design to prompt review, not only on edits.
- Lint outputs diagnostics and suggestions; it does not auto-mutate `wiki/` unless an explicit `--fix` path is documented and invoked.

## Composability

- **kb-compile** — must produce `wiki/` before lint.
- **kb-coverage-dashboard** — ingests lint outputs (freshness, links) for rollups.
- **kb-daily-report** — cites lint/freshness in KB Health sections.
- **kb-orchestrator** — runs lint in `enhance` (and related) workflows.

## Output Discipline

- Report every check's findings; do not trim long lists to save tokens.
- Severity is qualitative: one Critical outweighs many Low items; do not rank by count alone.
- Do not suggest fixes that require editing `raw/`; lint scope is `wiki/` (ingest/compile handles raw).

## Honest Reporting

- Use exact counts (e.g. 47 broken links), not rounded approximations.
- If all checks pass, state zero-issue clearly; do not fabricate findings.
- A topic-level freshness score of 0 is critical; surface it explicitly, not buried in averages.
