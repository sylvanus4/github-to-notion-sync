---
name: autoskill-merger
description: >-
  Merge a skill candidate into an existing skill with semantic union of
  constraints, triggers, and tags. Use when autoskill-judge returns a merge
  decision, when the user asks to "merge skill candidate", "update skill with
  new constraints", "스킬 병합", "autoskill merge", or when invoked by
  autoskill-evolve. Do NOT use for creating new skills (use create-skill),
  skill quality auditing (use skill-optimizer), or manual skill editing.
metadata:
  author: thaki
  version: "0.1.0"
  category: self-improvement
---

# AutoSkill Merger

Merge a skill candidate into an existing skill, producing an improved version with a patch version bump. Performs semantic union of constraints, triggers, and tags while preserving the existing skill's identity. Adapts AutoSkill's P_merge methodology for the Cursor SKILL.md format.

## Instructions

### Input

- The existing SKILL.md file path (from `autoskill-judge` decision's `target_skill_id`)
- The skill candidate JSON (from `autoskill-extractor`)

### Merge Process

1. **Read Existing Skill**: Parse the target SKILL.md file including frontmatter metadata and body content.

2. **Apply Merge Principles**:

   - **Shared Intent**: Preserve the existing skill's core capability identity
   - **Diff-Aware**: Import only unique, non-conflicting constraints from the candidate
   - **Semantic Union**: Combine constraints by meaning, not raw concatenation
   - **Recency Guard**: When conflicts arise, prefer the candidate's recent-topic intent
   - **Anti-Duplication**: Never duplicate section headers, bullets, or blocks

3. **Field-Level Merge Rules**:

   | Field | Merge Strategy |
   |-------|---------------|
   | `name` | Keep existing unless candidate is clearly more specific |
   | `description` | Keep existing structure, add new scope if candidate expands usage |
   | `prompt` / body | Semantic union of Goal, Constraints, Workflow sections |
   | `triggers` | Union + deduplicate, max 8 |
   | `tags` | Union + deduplicate, max 8 |
   | `examples` | Append new examples, max 5 total |

4. **Version Bump**: Increment the patch version in the SKILL.md frontmatter:
   - If no version exists, set `v0.1.0`
   - Otherwise increment: `v0.1.N` → `v0.1.N+1`

5. **Changelog Entry**: Add a brief changelog comment at the bottom of the SKILL.md:
   ```
   <!-- autoskill-merge v0.1.N+1 | YYYY-MM-DD | Merged from candidate: <name> -->
   ```

6. **Conflict Resolution**:
   - If candidate contradicts an existing constraint, flag for human review
   - If candidate adds a constraint that narrows existing scope, include it
   - If candidate adds a constraint that broadens scope significantly, flag for review

### Output

- Updated SKILL.md file written in place
- Merge report JSON to `outputs/autoskill-merges/<date>-<skill-name>.json`:

```json
{
  "target_skill": "skill-name",
  "previous_version": "v0.1.5",
  "new_version": "v0.1.6",
  "changes": {
    "triggers_added": ["new trigger"],
    "constraints_added": ["new constraint"],
    "conflicts_flagged": []
  },
  "source_candidate": "candidate-name",
  "merge_date": "2026-03-14"
}
```

### Reference Prompts

See `references/merge-prompt.md` for the full adapted merge prompt template.

### Integration

- Receives `merge` decisions from `autoskill-judge`
- Modifies existing files in `.cursor/skills/`
- Invoked by `autoskill-evolve` orchestrator
- Optionally triggers `skill-optimizer` audit after merge

### SEFO Integration (CRDT Merge)

Replace heuristic field-level merging with deterministic CRDT semantics from the FSE module:

1. **Version vector check**: Before merging, retrieve the existing skill's SEFO representation via `GET /api/v1/sefo/skills?search=<skill_name>`. Compare version vectors to determine merge strategy (accept, keep, LWW, or fork).
2. **CRDT merge via gossip**: If both skills exist in SEFO, POST the candidate as a `GossipMessage` to `POST /api/v1/sefo/fse/gossip` with `skill_name`, `skill_data`, and `version_vector`. The FSE module handles deterministic merge or fork creation.
3. **Fork resolution**: If the merge results in a fork (conflicting grammar rules), retrieve the fork via `GET /api/v1/sefo/fse/status` and resolve via `POST /api/v1/sefo/fse/forks/{fork_id}/resolve`.
4. **Sign merged skill**: After successful merge, sign the updated skill via `POST /api/v1/sefo/tsg/sign` to establish provenance chain continuity.
5. **Fallback**: If the SEFO backend is unavailable, fall back to the existing heuristic merge process. Log a warning for later reconciliation.
