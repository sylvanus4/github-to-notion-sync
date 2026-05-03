---
name: content-graph-evolve
description: >-
  Evolve the Content Skill Graph based on production performance data.
  Analyzes content output scores, engagement feedback, and production patterns
  to propose targeted graph updates — new nodes, refined voice parameters,
  adjusted hook formulas, and updated platform rules. Use when the user asks
  to "evolve content graph", "improve my content graph", "update graph from
  performance", "graph evolution", "adapt content engine", "refine voice from
  results", "콘텐츠 그래프 진화", "그래프 업데이트", "성과 기반 개선", "content-graph-evolve",
  "learn from content results", "update hooks", "optimize my content system",
  or wants the Content Skill Graph to improve based on real-world content
  performance. Do NOT use for initial graph setup (use content-graph-setup).
  Do NOT use for content production (use content-graph-produce). Do NOT use
  for graph health checks without performance data (use content-graph-audit).
  Do NOT use for one-time voice calibration from samples (use
  content-graph-voice).
---

# Content Graph Evolve

Continuously improve the Content Skill Graph by feeding production results back into the graph. Detects patterns in quality scores, identifies underperforming dimensions, and proposes targeted graph node updates.

## Role

You are a content systems optimizer. You read production output data, detect patterns that reveal graph weaknesses, and propose precise surgical updates to specific graph nodes — never wholesale rewrites.

## Prerequisites

- `content-skill-graph/` directory must exist with populated files
- At least 3 production runs exist in `outputs/content-graph/` (need pattern data)
- Production outputs include quality scores from `content-graph-produce` Phase 6

## Constraints

- Do NOT modify graph files without explicit user approval
- Do NOT propose changes without citing specific performance data as evidence
- Do NOT rewrite entire files — propose targeted insertions, updates, or deletions
- Do NOT delete existing nodes unless they are demonstrably unused
- Always present changes as diffs (before/after) for user review
- Maximum 5 proposals per evolution cycle (prevent overwhelming changes)

## Workflow

### Phase 1: Performance Data Collection

Scan all production output directories:

1. Read all `outputs/content-graph/*/06-final-scored.md` files
2. Extract per-platform scores across all runs:
   - Voice Fidelity scores
   - Platform Native scores
   - Hook Strength scores
   - Audience Fit scores
   - Goal Alignment scores
3. Build a performance matrix:

```markdown
| Date | Platform | Voice | Native | Hook | Audience | Goal | Composite |
|------|----------|-------|--------|------|----------|------|-----------|
| ... | ... | ... | ... | ... | ... | ... | ... |
```

4. Calculate averages, trends, and standard deviations per dimension per platform
5. Write the performance analysis to `outputs/content-graph/evolution-{date}.md`

### Phase 2: Pattern Detection

Analyze the performance matrix for actionable patterns:

#### Pattern A: Consistently Weak Dimensions
- Dimension averaging < 7.0 across all platforms → graph-wide issue
- Dimension averaging < 7.0 on a specific platform → platform-specific issue

#### Pattern B: Declining Trends
- Dimension score dropping over 3+ consecutive runs → something is stale or misaligned

#### Pattern C: Platform Outliers
- One platform consistently 2+ points below others → platform node needs update

#### Pattern D: Hook Performance
- Hook scores consistently low → `engine/hooks.md` needs new formulas
- Hook scores vary wildly → hook selection logic may need refinement

#### Pattern E: Voice Drift
- Voice Fidelity scores declining → voice DNA may need recalibration
- Voice Fidelity inconsistent across platforms → `voice/platform-tone.md` gaps

### Phase 3: Proposal Generation

For each detected pattern, generate a specific proposal:

```markdown
## Proposal {N}: {Title}

**Pattern**: {Which pattern from Phase 2}
**Evidence**: {Specific scores, dates, platforms}
**Affected Node**: `{path/to/file.md}`
**Change Type**: INSERT | UPDATE | DELETE

### Current Content
{Exact section being changed}

### Proposed Content
{New content to replace/insert}

### Expected Impact
{Which dimension should improve, by how much}
```

Rules for proposals:
1. Each proposal targets exactly ONE graph node
2. Each proposal cites at least 2 data points as evidence
3. Each proposal predicts the dimension it should improve
4. Maximum 5 proposals per cycle

### Phase 4: New Node Suggestions

Beyond updating existing nodes, detect if entirely new nodes would help:

1. **Missing audience segment**: Production outputs frequently address a persona not in `audience/segments.md`
2. **Missing content type**: Certain posts don't match any type in `engine/content-types.md`
3. **Missing platform**: User is producing content for a platform with no `platforms/{name}.md`
4. **Missing hook category**: Hooks that work well don't match any formula in `engine/hooks.md`

For each new node suggestion:

```markdown
## New Node Suggestion: {filename}

**Location**: `content-skill-graph/{path}/{filename}.md`
**Rationale**: {Why this node is needed, with evidence}
**Draft Content**: {Proposed initial content}
**Connections**: {Which existing nodes should wikilink to this}
```

### Phase 5: User Review

Present all proposals and new node suggestions to the user:

1. Use `AskQuestion` to let the user select which proposals to apply
2. Options: Apply All, Apply Selected, Skip All, Review One-by-One

For each approved proposal:
1. Read the target file
2. Apply the specific change (insert/update/delete)
3. Verify wikilinks still resolve after the change
4. Log the change with date and evidence to `outputs/content-graph/evolution-{date}.md`

### Phase 6: Evolution Report

```markdown
# Content Skill Graph Evolution Report — {date}

## Data Analyzed
- Production runs: {N}
- Date range: {earliest} to {latest}
- Total posts scored: {N}

## Patterns Detected
1. {Pattern description} — Severity: {HIGH|MEDIUM|LOW}
2. ...

## Proposals
| # | Target Node | Change | Status | Expected Impact |
|---|-------------|--------|--------|-----------------|
| 1 | `voice/brand-voice.md` | UPDATE | ✅ Applied | Voice Fidelity +1.5 |
| 2 | `engine/hooks.md` | INSERT | ⏭️ Skipped | — |
| ... | | | | |

## New Nodes Created
- `{path}` — {rationale}

## Next Steps
- Re-run `content-graph-audit` to verify integrity after changes
- Monitor next 3 production runs for score improvement
- Schedule next evolution cycle after 5+ new runs
```

## Verification

Before reporting complete:

1. Confirm at least 3 production output directories were analyzed
2. Confirm all 5 pattern types were checked
3. Confirm no graph files were modified without user approval
4. Confirm evolution report was written to outputs
5. Confirm wikilink integrity after any applied changes

```
VERDICT: PASS — Analyzed {N} runs, detected {P} patterns, proposed {Q} changes, applied {A}
```

## Error Recovery

| Error | Recovery |
|-------|----------|
| `outputs/content-graph/` empty or missing | Need at least 3 production runs first; suggest `content-graph-produce` |
| Score files missing or malformed | Skip that run; warn user; continue with available data |
| Insufficient data (< 3 runs) | Report what patterns are visible; recommend running more production cycles |
| Conflicting patterns | Present both with evidence; let user decide priority |
| Applied change breaks wikilinks | Auto-revert the change; report the issue; suggest manual fix |
