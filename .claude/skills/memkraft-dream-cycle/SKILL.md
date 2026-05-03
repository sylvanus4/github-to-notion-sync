---
name: memkraft-dream-cycle
description: >-
  Nightly MemKraft maintenance: consolidate sessions into topics, decay stale
  entries, resolve orphan entities, promote repeated patterns to preferences,
  and archive COLD-tier entries. Uses existing attention_decay.py and
  extract-sessions.py.
---

# MemKraft Dream Cycle — Nightly Maintenance

## Purpose

The Dream Cycle is MemKraft's nightly maintenance routine. Inspired by memory
consolidation during sleep, it processes the day's accumulated memories: extracting
sessions, consolidating topics, decaying stale entries, resolving orphans, promoting
patterns, and archiving dead entries.

## When to Run

- **Scheduled**: Daily at 23:00 (configured in `memory/memkraft.json`)
- **Manual**: When the user asks to "run dream cycle", "clean up memory", "consolidate memories"
- **Pipeline**: Triggered as final phase of `daily-pm-orchestrator`

## 6-Phase Pipeline

### Phase 1: Session Extraction

Extract new session transcripts into structured memory entries.

```bash
python scripts/memory/extract-sessions.py --incremental
```

- Reads new `.jsonl` transcripts from agent-transcripts/
- Extracts high-signal items (decisions, corrections, discoveries)
- Writes structured summaries to `memory/sessions/`
- Skips already-processed transcripts (tracked in `.cache/`)

### Phase 2: Topic Consolidation

Merge session findings into existing topic files.

**Process**:
1. Read all new session entries from Phase 1
2. Match each entry to existing topics in `memory/topics/` by keyword/entity overlap
3. For matching topics: append new findings with `[RECENT]` tag and today's date
4. For non-matching entries: create new topic file if signal is strong enough (≥2 mentions)
5. Deduplicate within each topic file

### Phase 3: Attention Decay

Apply time-based score decay to all memory entries.

```bash
python scripts/memory/attention_decay.py --apply
```

- Apply `daily_rate` decay (default: -0.02/day) from `memkraft.json`
- Transition entries between tiers when crossing thresholds:
  - HOT → WARM when score drops below 0.7
  - WARM → COLD when score drops below 0.3
  - COLD → archive when score drops below `archive_below` (0.1)
- Boost accessed entries by `boost_on_access` (+0.15)
- Never decay below `min_score` (0.05) to prevent total loss

### Phase 4: Orphan Resolution

Find and process unresolved items that may now have answers.

**Process**:
1. Read all files in `memory/unresolved/`
2. For each open item, search recent sessions and topics for potential answers
3. If a resolution is found: update status to `resolved`, move to `memory/archive/resolved/`
4. If partially answered: update with new evidence, keep status `investigating`
5. Flag items older than 14 days as `stale` for user review

### Phase 5: Preference Promotion

Detect repeated patterns in sessions and promote to explicit preferences.

**Process**:
1. Scan recent sessions for repeated user corrections or consistent behavior patterns
2. Check `promotion.repeat_threshold` (default: 3 occurrences)
3. Check `promotion.confidence_min` (default: 0.8)
4. If both thresholds met and `auto_promote_preferences` is true:
   - Create or update the matching preference file in `memory/preferences/`
   - Tag with `[PREFERENCE]` provenance
5. Report promoted items in the Dream Cycle log

### Phase 6: Archive Sweep

Move COLD-tier entries below archive threshold to `memory/archive/`.

**Process**:
1. Scan all memory files for entries with score < `archive_below` (0.1)
2. Move to `memory/archive/` with date stamp and `[ARCHIVED]` tag
3. Preserve original path in archive metadata for potential retrieval
4. Update `memory/index.md` if entry counts changed significantly

## Output

Each Dream Cycle run produces a log file at `memory/dream-cycle/{date}-dream-cycle.md`:

```markdown
# Dream Cycle — {date}

## Summary
- Sessions extracted: {n}
- Topics consolidated: {n}
- Entries decayed: {n} (avg score change: -{x})
- Tier transitions: {n} (HOT→WARM: {a}, WARM→COLD: {b}, COLD→archive: {c})
- Orphans resolved: {n}/{total}
- Preferences promoted: {n}
- Items archived: {n}

## Details
### Tier Transitions
- `topics/trading-stack.md`: HOT → WARM (0.72 → 0.68)
...

### Promoted Preferences
- "User prefers Korean error messages" → preferences/communication.md
...

### Resolved Items
- `unresolved/2026-04-10-api-timeout.md` → resolved (found fix in session 2026-04-14)
...
```

## Script Integration

The Dream Cycle orchestrates these existing and new scripts:

| Script | Phase | Purpose |
|--------|-------|---------|
| `scripts/memory/extract-sessions.py` | 1 | Session transcript extraction |
| `scripts/memory/attention_decay.py` | 3 | Score decay and tier transitions |
| `scripts/memory/build-index.py` | Post | Rebuild search index after changes |
| `scripts/memory/dream_cycle.py` | All | Consolidated runner (Phase 2c) |

## Configuration

All parameters are in `memory/memkraft.json`:

- `decay.daily_rate`: Score reduction per day (default: 0.02)
- `decay.boost_on_access`: Score boost when accessed (default: 0.15)
- `decay.archive_below`: Archive threshold (default: 0.1)
- `dream_cycle.max_duration_minutes`: Safety timeout (default: 15)
- `promotion.repeat_threshold`: Occurrences before auto-promote (default: 3)
