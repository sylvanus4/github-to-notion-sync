---
name: content-graph-audit
description: >-
  Health check for the Content Skill Graph — scans all nodes for completeness,
  freshness, wikilink integrity, voice calibration, platform coverage,
  repurpose chain validity, and cross-node consistency. Produces a
  severity-ranked report with auto-fix suggestions. Use when the user asks to
  "audit content graph", "check graph health", "graph audit", "content audit",
  "validate my content graph", "콘텐츠 그래프 점검", "그래프 건강 점검",
  "content-graph-audit", "check content skill graph", "is my graph complete",
  "fix broken links", or wants to verify and improve the Content Skill Graph's
  structural integrity. Do NOT use for setting up a new graph (use
  content-graph-setup). Do NOT use for producing content (use
  content-graph-produce). Do NOT use for calibrating voice (use
  content-graph-voice). Do NOT use for evolving the graph based on performance
  data (use content-graph-evolve).
---

# Content Graph Audit

Scan the Content Skill Graph for structural integrity, completeness, and quality across 7 dimensions. Produce a severity-ranked health report with actionable fix suggestions.

## Role

You are a knowledge graph quality inspector. You methodically verify every node, link, and relationship in the Content Skill Graph, treating it as a production system where broken links or stale data directly degrade content output quality.

## Prerequisites

- `content-skill-graph/` directory must exist with populated files

## Constraints

- Do NOT modify any files unless the user explicitly approves fixes
- Do NOT report false positives — verify each issue before flagging
- Do NOT skip any dimension in the 7-dimension check
- Classify all issues as CRITICAL, WARNING, or INFO

## Workflow

### Phase 1: Inventory Scan

Walk the `content-skill-graph/` directory tree and catalog every `.md` file:

1. List all files with their paths
2. Record file sizes (empty files = immediate CRITICAL)
3. Record last-modified dates
4. Count total nodes

Expected minimum structure:

```
content-skill-graph/
├── index.md
├── audience/
│   ├── segments.md
│   └── pain-points.md
├── voice/
│   ├── brand-voice.md
│   └── platform-tone.md
├── platforms/
│   └── {at least one platform}.md
└── engine/
    ├── repurpose.md
    ├── hooks.md
    ├── content-types.md
    ├── goals.md
    └── schedule.md
```

### Phase 2: Seven-Dimension Health Check

#### Dimension 1: Completeness

Check every expected file exists and is non-empty:

| File | Required | Status |
|------|----------|--------|
| `index.md` | Yes | ✅/❌ |
| `audience/segments.md` | Yes | ✅/❌ |
| `audience/pain-points.md` | Yes | ✅/❌ |
| `voice/brand-voice.md` | Yes | ✅/❌ |
| `voice/platform-tone.md` | Yes | ✅/❌ |
| `engine/repurpose.md` | Yes | ✅/❌ |
| `engine/hooks.md` | Yes | ✅/❌ |
| `engine/content-types.md` | Yes | ✅/❌ |
| `engine/goals.md` | Yes | ✅/❌ |
| `engine/schedule.md` | Optional | ✅/❌/➖ |
| `platforms/*.md` | At least 1 | ✅/❌ |

Missing required files = CRITICAL.

#### Dimension 2: Wikilink Integrity

For every `[[wikilink]]` found in every file:

1. Extract the target path
2. Verify the target file exists
3. Report broken links with source file, line, and target

Broken wikilinks = WARNING (content-graph-produce will silently miss context).

#### Dimension 3: Voice Calibration

Read `voice/brand-voice.md` and check:

- Contains a "Voice DNA" or "Linguistic Fingerprint" section (not just wizard placeholder text)
- Has "Calibration Source" section with a date
- Lists at least 3 personality adjectives
- Has "Always" and "Never" sections

Uncalibrated voice = WARNING with suggestion to run `content-graph-voice`.

#### Dimension 4: Platform Coverage

For each platform file in `platforms/`:

1. Verify it contains format rules (character limits, formatting style)
2. Verify it has a corresponding entry in `voice/platform-tone.md`
3. Verify it appears in the repurpose chain in `engine/repurpose.md`

Platform without tone mapping = WARNING.
Platform not in repurpose chain = INFO.

#### Dimension 5: Repurpose Chain Validity

Read `engine/repurpose.md` and verify:

1. A chain order is defined (numbered or sequential list)
2. Every platform in the chain exists as `platforms/{name}.md`
3. No duplicate platforms in the chain
4. Chain starts with the longest-form platform

Invalid chain = CRITICAL (content-graph-produce cannot run).

#### Dimension 6: Freshness

Check last-modified dates on all files:

| Age | Classification |
|-----|---------------|
| < 30 days | Fresh ✅ |
| 30-90 days | Aging ⚠️ |
| > 90 days | Stale 🔴 |

Stale core files (`index.md`, `voice/brand-voice.md`) = WARNING.
Stale engine files = INFO.

#### Dimension 7: Cross-Node Consistency

Verify consistency across connected nodes:

1. Platforms listed in `index.md` match files in `platforms/`
2. Audience segments referenced in `engine/goals.md` exist in `audience/segments.md`
3. Content types in `engine/content-types.md` are referenced by at least one platform
4. Hook formulas in `engine/hooks.md` reference valid platform names

Mismatches = WARNING.

### Phase 3: Health Report

Compile all findings into a structured report:

```markdown
# Content Skill Graph Health Report — {date}

## Score: {composite}/100

| Dimension | Score | Issues |
|-----------|-------|--------|
| Completeness | {score}/100 | {count} |
| Wikilink Integrity | {score}/100 | {count} |
| Voice Calibration | {score}/100 | {count} |
| Platform Coverage | {score}/100 | {count} |
| Repurpose Chain | {score}/100 | {count} |
| Freshness | {score}/100 | {count} |
| Cross-Node Consistency | {score}/100 | {count} |

## Issues by Severity

### CRITICAL ({count})
{List with file, line, description, suggested fix}

### WARNING ({count})
{List with file, line, description, suggested fix}

### INFO ({count})
{List with file, line, description, suggested fix}

## Suggested Actions
1. {Highest priority fix}
2. {Second priority fix}
...
```

Scoring:
- CRITICAL issue: -15 points from that dimension
- WARNING issue: -5 points from that dimension
- INFO issue: -1 point from that dimension
- Each dimension starts at 100

### Phase 4: Auto-Fix Offer

For fixable issues, offer batch repair:

1. **Broken wikilinks**: Suggest correct targets based on fuzzy filename matching
2. **Missing files**: Offer to create stub files with TODO markers
3. **Stale files**: No auto-fix, suggest re-running relevant setup/voice skill
4. **Missing platform-tone entries**: Offer to generate default entries

Use `AskQuestion` to confirm before applying any fixes:
- "Apply {N} auto-fixes? (broken links: {n1}, stubs: {n2}, tone entries: {n3})"

### Phase 5: Summary

```
📊 Content Skill Graph Audit Complete

Score: {composite}/100
📁 Nodes scanned: {N}
🔗 Wikilinks checked: {N}
🔴 CRITICAL: {N}
🟡 WARNING: {N}
🔵 INFO: {N}
🔧 Auto-fixes applied: {N} (if any)

Status: {HEALTHY | NEEDS ATTENTION | CRITICAL ISSUES}
```

## Verification

Before reporting complete:

1. Confirm all 7 dimensions were checked
2. Confirm every `.md` file in the graph was scanned
3. Confirm every wikilink was resolved or flagged
4. Confirm the composite score calculation is consistent
5. Confirm no auto-fixes were applied without user consent

```
VERDICT: PASS — Graph audited across 7 dimensions, {N} nodes, score {S}/100
```

## Error Recovery

| Error | Recovery |
|-------|----------|
| `content-skill-graph/` not found | Direct user to `content-graph-setup` |
| Directory exists but is empty | Report as CRITICAL completeness failure; suggest re-running `content-graph-setup` |
| Permission errors reading files | Report affected files; suggest checking filesystem permissions |
| Very large graph (100+ nodes) | Process in batches of 20; report progress |
