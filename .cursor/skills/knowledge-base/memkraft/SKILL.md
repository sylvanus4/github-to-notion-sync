---
name: memkraft
description: >-
  Personal memory orchestrator: read, write, query, and manage tiered personal memory
  (HOT/WARM/COLD) with provenance tags, session continuity, and unresolved item tracking.
  Wraps existing `recall` skill with MemKraft semantics.
triggers:
  - memkraft
  - personal memory
  - memory status
  - memory query
  - tier status
  - 개인 메모리
  - 메모리 상태
  - 메모리 조회
  - MemKraft
  - 메모리 티어
do_not_use_for:
  - LLM Wiki operations (use wiki-company or wiki-team)
  - Dream Cycle maintenance (use memkraft-dream-cycle)
  - Writing new memories (use memkraft-ingest for explicit ingest)
  - General web search (use WebSearch)
  - Code review (use deep-review)
---

# MemKraft — Personal Memory Orchestrator

## Purpose

MemKraft is the personal memory layer of the knowledge system. It manages dynamic,
recency-sensitive, provenance-tagged personal context — distinct from the LLM Wiki
(`knowledge-bases/`) which holds organizational/team knowledge.

MemKraft wraps the existing `recall` skill with tiered memory semantics, attention
decay, unresolved item tracking, and per-domain preference management.

## Architecture

```
┌─────────────────────────────────────────┐
│              MemKraft                   │
│  ┌──────────┬──────────┬──────────┐    │
│  │   HOT    │   WARM   │   COLD   │    │
│  │  ≥ 0.7   │ 0.3–0.7  │  < 0.3   │    │
│  │ Active   │Background│ Archive  │    │
│  └──────────┴──────────┴──────────┘    │
│  ┌─────────┐ ┌───────────┐ ┌────────┐ │
│  │Sessions │ │Preferences│ │Unresolvd│ │
│  └─────────┘ └───────────┘ └────────┘ │
└─────────────────────────────────────────┘
```

Configuration: `memory/memkraft.json`

## Modes

### 1. `query` (default)

Search personal memory with MemKraft-first retrieval.

**Input**: Natural language query or topic keyword
**Process**:
1. Search `memory/topics/` for matching topic files (HOT tier first)
2. Search `memory/preferences/` for relevant domain preferences
3. Search `memory/unresolved/` for related open items
4. Search `memory/sessions/` via `recall` skill for session history
5. Tag all results with provenance: `[PERSONAL]`, `[PREFERENCE]`, `[RECENT]`, `[UNRESOLVED]`
6. Rank by recency × relevance × tier score

**Output**: Provenance-tagged memory context

### 2. `status`

Report MemKraft health and statistics.

**Process**:
1. Read `memory/memkraft.json` for configuration
2. Count entries per tier (HOT/WARM/COLD) from topic file frontmatter
3. Count unresolved items and their priorities
4. Count preference domains
5. Report last Dream Cycle run from `memory/dream-cycle/`
6. Compute overall freshness score

**Output**: Health dashboard with tier distribution, staleness warnings, unresolved count

### 3. `tier-report`

Detailed breakdown of all memory entries by tier.

**Process**:
1. Read all files in `memory/topics/`, `memory/preferences/`, `memory/unresolved/`
2. Classify each by attention score into HOT/WARM/COLD
3. Flag entries approaching tier boundaries (within 0.05 of threshold)

**Output**: Per-file tier assignment with scores and transition warnings

### 4. `boost`

Manually boost a memory entry's attention score (triggers on access).

**Input**: File path or topic name
**Process**:
1. Locate the memory file
2. Apply `boost_on_access` (default: +0.15) from `memkraft.json`
3. Cap at 1.0
4. Update the file's frontmatter score

### 5. `archive`

Manually move a COLD-tier entry to archive.

**Input**: File path or topic name
**Process**:
1. Verify entry is COLD tier (score < 0.3)
2. Move to `memory/archive/` with `[ARCHIVED]` provenance
3. Update index

## Provenance Tags

Every MemKraft response includes provenance:

| Tag | Meaning |
|-----|---------|
| `[PERSONAL]` | Session-derived facts, decisions, context |
| `[PREFERENCE]` | User preferences and conventions |
| `[RECENT]` | Entries from the last 48 hours |
| `[UNRESOLVED]` | Open questions awaiting resolution |
| `[ARCHIVED]` | Moved to COLD tier, available via search |

## File Locations

| Directory | Content |
|-----------|---------|
| `memory/topics/` | Structured topic files (Layer 2) |
| `memory/preferences/` | Per-domain preference files |
| `memory/unresolved/` | Pending issues and open questions |
| `memory/sessions/` | Auto-extracted session transcripts |
| `memory/dream-cycle/` | Dream Cycle maintenance logs |
| `memory/archive/` | COLD tier archived entries |
| `memory/memkraft.json` | Configuration (tiers, decay, schedule) |

## Integration

- **Upstream**: Fed by `memkraft-ingest` (explicit writes) and `extract-sessions.py` (auto-extraction)
- **Downstream**: Consumed by `ai-context-router` for personal-first retrieval in `ai-*` skills
- **Maintenance**: `memkraft-dream-cycle` runs nightly decay, consolidation, and archival
- **Fallback**: Wraps `recall` skill for backward-compatible session search
