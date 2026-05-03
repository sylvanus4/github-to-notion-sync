---
name: skill-curator
description: >-
  Skill lifecycle curator: tracks usage analytics, manages active/stale/archived
  states, consolidates overlapping skills, and cleans up unused ones. Runs
  manually via "skill-curator", "스킬 큐레이션", "스킬 정리", "curator run",
  "skill cleanup", "스킬 통합", or on a scheduled cadence. Skips pinned,
  bundled, and externally installed skills. Only curates agent-created and
  user-written skills. Do NOT use for skill creation (write-a-skill), evolution
  (hermes-skill-evolver), or single-skill optimization (skill-autoimprove).
---

# Skill Curator

Lifecycle management for agent-created and user-written skills. Prevents skill sprawl by tracking usage, transitioning unused skills through `active -> stale -> archived`, and consolidating overlapping skills.

## When to Use

- `skill-curator run` or `스킬 큐레이션` -- full curation pass
- `skill-curator status` -- dashboard of skill health
- `skill-curator scan` -- dry-run analysis without changes
- `skill-curator pin <skill>` -- protect a skill from curation
- `skill-curator unpin <skill>` -- remove pin protection
- `skill-curator restore <skill>` -- recover from archive
- `skill-curator consolidate <skill1> <skill2> ...` -- merge specified skills

## Do NOT Use

- Skill creation from scratch -> `write-a-skill`
- Population-based evolution -> `hermes-skill-evolver`
- Single-mutation optimization -> `skill-autoimprove`
- Static quality audit -> `skill-guide`

---

## Architecture

```
.claude/skills/
  ├── .curator/
  │   ├── registry.json      # Usage analytics + lifecycle state per skill
  │   ├── config.json         # Curation thresholds + settings
  │   └── last-run.json       # Timestamp + summary of last curator run
  ├── .archive/               # Archived skills (recoverable)
  │   └── {skill-name}/
  └── {skill-name}/
      └── SKILL.md
```

## Lifecycle FSM

```
  ┌──────────┐     stale_after_days     ┌──────────┐    archive_after_days    ┌──────────┐
  │  active   │ ──────────────────────> │  stale    │ ──────────────────────> │ archived  │
  └──────────┘                          └──────────┘                          └──────────┘
       ^                                     │                                     │
       │                                     │  (used again)                       │  (restore)
       │                                     v                                     v
       └─────────────────────────────── reactivated ◄──────────────────────── recovered
```

### States

| State | Meaning | Registry `state` |
|-------|---------|------------------|
| **active** | Used within `stale_after_days` | `active` |
| **stale** | Not used for `stale_after_days` (default 30d) | `stale` |
| **archived** | Not used for `archive_after_days` (default 90d), moved to `.archive/` | `archived` |
| **pinned** | Explicitly protected from all curation | `pinned` |

### Transition Rules

- `active -> stale`: automatic when `days_since_last_use > stale_after_days`
- `stale -> archived`: automatic when `days_since_last_use > archive_after_days`
- `stale -> active`: automatic when skill is used again
- `archived -> active`: manual via `skill-curator restore <skill>`
- `pinned`: manual via `skill-curator pin/unpin`. Pinned skills skip ALL transitions.

---

## Registry Schema

`registry.json` -- one entry per skill:

```json
{
  "skill-name": {
    "state": "active|stale|archived|pinned",
    "origin": "agent|user|bundled|external",
    "created_at": "2026-01-15",
    "last_modified": "2026-03-20",
    "last_used": "2026-04-28",
    "use_count": 12,
    "tags": ["research", "analysis"],
    "size_bytes": 4200,
    "consolidation_group": null,
    "notes": ""
  }
}
```

### Origin Classification

| Origin | Criteria | Curated? |
|--------|----------|----------|
| `bundled` | Shipped with repo, present in initial commit | NO |
| `external` | Installed from hub/marketplace | NO |
| `agent` | Created by agent (skill-autoimprove, write-a-skill, hermes-skill-evolver) | YES |
| `user` | Created manually by user | YES |

Only `agent` and `user` origin skills are subject to curation.

---

## Config Schema

`.curator/config.json`:

```json
{
  "enabled": true,
  "stale_after_days": 30,
  "archive_after_days": 90,
  "auto_run_interval_days": 7,
  "max_consolidation_batch": 5,
  "min_similarity_for_consolidation": 0.7,
  "protect_patterns": ["hermes-*", "omc-*"],
  "dry_run": false
}
```

---

## Curation Pass Workflow

### Phase 1: Registry Sync (deterministic, no LLM)

1. Scan `.claude/skills/` for all skill directories with SKILL.md
2. For each skill NOT in registry -> add with `origin: "user"`, `state: "active"`, `use_count: 0`
3. For each registry entry whose skill directory is missing -> mark `state: "archived"` (orphan cleanup)
4. Update `size_bytes` and `last_modified` from filesystem

### Phase 2: Lifecycle Transitions (deterministic, no LLM)

For each curated skill (`origin` in `[agent, user]` AND `state` != `pinned`):

1. Calculate `days_since_last_use = today - last_used`
2. If `state == "active"` AND `days_since_last_use > stale_after_days`:
   - Transition to `stale`
   - Log: `"{skill} -> stale (unused {N} days)"`
3. If `state == "stale"` AND `days_since_last_use > archive_after_days`:
   - Move skill directory to `.archive/{skill-name}/`
   - Transition to `archived`
   - Log: `"{skill} -> archived (unused {N} days)"`

### Phase 3: Consolidation Analysis (LLM-assisted)

Spawn a single haiku-model subagent to analyze curated skills:

1. Read SKILL.md for all `active` + `stale` curated skills
2. Identify consolidation candidates:
   - **Overlapping scope**: Two skills that solve similar problems
   - **Subset relationship**: Skill A is a strict subset of Skill B
   - **Fragmented workflow**: Multiple small skills that form a single logical workflow
3. For each candidate group, propose ONE of:
   - **Merge**: Combine into a single skill, archive the others
   - **Absorb**: Fold the smaller skill into the larger one as a sub-section
   - **Reference**: Convert the narrow skill into a template/script referenced by the broader skill
   - **Keep**: Skills are distinct enough to remain separate

Output: consolidation proposals as structured list.

### Phase 4: User Review

Present findings to user:

```markdown
# Skill Curator Report

## Lifecycle Changes
| Skill | Previous | New | Reason |
|-------|----------|-----|--------|

## Consolidation Proposals
| Group | Skills | Action | Rationale |
|-------|--------|--------|-----------|

## Health Summary
- Total skills: {N}
- Active: {N} | Stale: {N} | Archived: {N} | Pinned: {N}
- Bundled (skipped): {N} | External (skipped): {N}
- Avg use count: {N}
- Top 10 most used: ...
- Bottom 10 least used: ...
```

### Phase 5: Execute (user-approved only)

- Apply lifecycle transitions (Phase 2 always applies unless `dry_run: true`)
- Execute approved consolidations from Phase 4
- Update registry.json
- Write `last-run.json` with timestamp + summary

---

## Commands

### `skill-curator run`

Full curation pass (Phase 1-5).

```bash
# Execute
Bash: Run registry sync + lifecycle transitions

# Analysis
Agent(model: haiku): Read curated skills, propose consolidations

# Report
Output: Curator Report to user

# Execute approved changes
Edit/Bash: Apply consolidations, update registry
```

### `skill-curator status`

Dashboard only, no changes.

1. Read `registry.json`
2. Calculate current lifecycle states (without transitioning)
3. Output health summary

### `skill-curator scan`

Dry-run: show what WOULD happen without making changes.

1. Run Phase 1-3
2. Output report with `[DRY RUN]` prefix
3. No filesystem or registry changes

### `skill-curator pin <skill-name>`

1. Set `state: "pinned"` in registry
2. Confirm: `"{skill} pinned -- curator will skip this skill"`

### `skill-curator unpin <skill-name>`

1. Set `state: "active"` in registry, reset `last_used` to today
2. Confirm: `"{skill} unpinned -- now subject to curation"`

### `skill-curator restore <skill-name>`

1. Move `.archive/{skill-name}/` back to `.claude/skills/{skill-name}/`
2. Set `state: "active"`, `last_used: today` in registry
3. Confirm: `"{skill} restored from archive"`

### `skill-curator consolidate <skill1> <skill2> [...]`

Manual consolidation of specified skills:

1. Read all specified SKILL.md files
2. Agent(model: sonnet): Generate merged SKILL.md
3. Present diff to user for approval
4. On approval: write merged skill, archive source skills, update registry

---

## Usage Tracking

Usage is tracked by updating `registry.json` when skills are invoked.

### How to Record Usage

When any skill is loaded via the Skill tool, the curator registry should be updated:

```
After Skill tool invocation:
  1. Read .curator/registry.json
  2. Find entry for invoked skill
  3. Increment use_count
  4. Set last_used = today
  5. If state == "stale" -> set state = "active" (reactivation)
  6. Write registry.json
```

This is a convention -- the agent should update the registry after invoking skills when the curator is enabled. Not enforced by a hook.

---

## Consolidation Heuristics

The haiku subagent uses these heuristics to propose consolidations:

### Signal: Name Similarity
Skills with similar prefixes or shared domain keywords.
Example: `agency-frontend-developer` + `agency-ui-designer` + `agency-ux-researcher`

### Signal: Description Overlap
SKILL.md descriptions that reference the same tools, workflows, or outputs.

### Signal: Trigger Phrase Collision
Multiple skills triggered by similar user requests.

### Signal: Size Anomaly
Very small skills (<500 bytes) that could be sections of a larger skill.

### Signal: Inverse Relationship
Skills whose "Do NOT use for" section points at each other -- often siblings that should share a parent.

### Anti-Signal: Different Domains
Skills in different domains (finance vs. devops) should NOT be consolidated even if structurally similar.

### Anti-Signal: Different Complexity Tiers
A simple lookup skill and a multi-agent orchestrator should NOT merge.

---

## Safety Guarantees

1. **Never auto-delete**: Worst case is archival to `.archive/`, always recoverable
2. **Never touch pinned**: Pinned skills are completely invisible to curation
3. **Never touch bundled/external**: Only `agent` and `user` origin skills
4. **User approval for consolidations**: Phase 3 proposals require explicit approval
5. **Lifecycle transitions are automatic but reversible**: stale -> active on next use
6. **Dry-run mode**: `scan` command or `dry_run: true` in config
7. **Checkpoint before bulk changes**: If 10+ skills affected, suggest `hermes-checkpoint-rollback` first

---

## Integration with Jarvis

Jarvis includes `skill-curator` in Post-flight when:
- Session used 10+ different skills
- Session created new skills via `write-a-skill` or `hermes-skill-evolver`
- Last curator run was 7+ days ago

---

## Registry Bootstrap

First run initializes the registry by scanning all existing skills:

```bash
# For each skill directory in .claude/skills/:
#   1. Read SKILL.md frontmatter
#   2. Check git log for creation date: git log --diff-filter=A --format=%aI -- .claude/skills/{name}/SKILL.md
#   3. Check git log for last modified: git log -1 --format=%aI -- .claude/skills/{name}/SKILL.md
#   4. Classify origin:
#      - If in initial commit -> bundled
#      - If has marketplace/hub metadata -> external
#      - If commit message contains "autoimprove\|write-a-skill\|hermes" -> agent
#      - Else -> user
#   5. Set state: active, use_count: 0, last_used: last_modified
```

Run: `skill-curator bootstrap` to initialize.

---

## Scheduled Execution

Use `/schedule` to set up recurring curation:

```
/schedule skill-curator run -- every Monday at 9am
```

Or configure `auto_run_interval_days` in config.json for convention-based triggering (agent checks on session start if interval has elapsed).
