---
name: autoskill-merger
description: >-
  스킬 후보를 기존 스킬에 semantic union 또는 token-efficient patch로 병합. 제약, 트리거, 태그를 의미
  기반으로 통합하고 패치 버전을 범프. autoskill-judge의 merge 결정을 실행. Patch 모드는 단순 추가(트리거, 제약,
  태그)에 old_string/new_string 최소 편집을 적용하여 토큰 사용량을 절감. Use when autoskill-judge
  returns a merge decision, "스킬 병합", "autoskill merge", "merge skill
  candidate", "기존 스킬에 새 제약 추가", "스킬 업데이트 병합", "patch merge", "패치 병합". Do NOT
  use for creating new skills (use create-skill), skill quality auditing (use
  skill-optimizer), or manual skill editing (edit directly).
---

# AutoSkill Merger

Merge a skill candidate into an existing skill to produce an improved version. Unify constraints, triggers, and tags by **semantic union** while preserving the existing skill’s identity.

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Input

- Path to existing SKILL.md (`target_skill_id` from `autoskill-judge`)
- Candidate JSON from `autoskill-extractor`

## Workflow

### Step 1: Read existing skill

Parse target SKILL.md into frontmatter + body.

### Step 2: Select merge mode

Evaluate the candidate and choose the appropriate merge strategy:

| Criteria | Mode | When to use |
|----------|------|-------------|
| Appending triggers, constraints, tags, or examples only | `patch` | Candidate adds to existing sections without structural changes |
| Extending or restructuring workflow, adding new sections | `full` | Candidate modifies skill logic, resolves conflicts, or broadens scope |
| Contradictions or scope changes detected | `full` | Conflict resolution requires semantic judgment |

**Default**: `patch` — use `full` only when patch cannot express the change.

### Step 3: Apply merge (mode-dependent)

#### 3a: Full mode — semantic union

Apply these merge principles:

- **Shared intent**: Preserve core capability identity
- **Diff-aware**: Take only unique, non-conflicting constraints from the candidate
- **Semantic union**: Merge by meaning, not string concatenation
- **Recency guard**: On conflict, prefer the candidate’s recent intent
- **Anti-duplication**: No duplicate section headers, bullets, or blocks

Field-level merge rules:

| Field | Strategy |
|-------|----------|
| `name` | Change only if the candidate is clearly more specific |
| `description` | Keep existing shape; extend if the candidate broadens scope |
| Body | Semantic union of Goal, Constraints, Workflow sections |
| `triggers` | Union, dedupe, cap at 8 |
| `tags` | Union, dedupe, cap at 8 |
| `examples` | Append new examples, max 5 total additions |

#### 3b: Patch mode — minimal StrReplace edits

Apply the candidate's additions as targeted `StrReplace` operations:

1. **Identify insertion points**: Find the exact section header or list boundary where new content belongs
2. **Construct minimal edits**: Each edit uses `old_string` (existing anchor text) and `new_string` (anchor + appended content)
3. **Scope limit**: Max 3 StrReplace operations per patch merge; if more are needed, escalate to full mode
4. **No structural changes**: Patch mode must NOT reorder sections, rename headers, or modify existing content — append only

Patch mode examples:

- **Add trigger**: Extend the last trigger in the description with the new trigger appended
- **Add constraint bullet**: Append after the last bullet in the Constraints section
- **Add tag**: Extend the tags array in frontmatter

**Escalation rule**: If patch mode would require modifying existing text (not just appending), switch to full mode automatically.

### Step 4: Version bump

Bump patch in frontmatter:
- Missing version → set `1.0.0`
- Existing → increment patch: `1.0.N` → `1.0.N+1`

### Step 5: Change log

Append a comment at the bottom of SKILL.md:

```
<!-- autoskill-merge v1.0.N+1 | YYYY-MM-DD | Merged from candidate: <name> -->
```

### Step 6: Conflict resolution

- Candidate contradicts existing constraint → flag human review
- Candidate narrows scope → include
- Candidate greatly expands scope → flag review

### Step 7: Post-merge policy verification (mandatory)

After writing the merged `SKILL.md`, validate:

1. **POL-001 / terminology** — Scan body for forbidden or deprecated product terms per `docs/policies/01-product-identity.md` and [.cursor/skills/references/project-overrides/project-terminology-glossary.md](../references/project-overrides/project-terminology-glossary.md). If new violations appear, **revert** the merge or patch before completing.
2. **Design system references** — Instructions must point to **Tailwind CSS + Radix UI** and local conventions (see [.cursor/skills/references/project-overrides/project-design-conventions.md](../references/project-overrides/project-design-conventions.md)). **Fail** if the merged skill **requires** Thaki **TDS** or **Figma** as mandatory for this app.
3. **Project-Specific Overrides** — If the target skill already had a **Project-Specific Overrides** section, **preserve** it; merge candidate content around it without deleting override links.

Record pass/fail in the merge report JSON under `policy_verification`.

## Output

- Updated SKILL.md in place
- Merge report JSON: `outputs/autoskill-merges/<date>-<skill-name>.json`

```json
{
  "target_skill": "skill-name",
  "previous_version": "1.0.5",
  "new_version": "1.0.6",
  "merge_mode": "patch",
  "changes": {
    "triggers_added": ["new trigger"],
    "constraints_added": ["new constraint"],
    "conflicts_flagged": [],
    "strreplace_ops": 2
  },
  "source_candidate": "candidate-name",
  "merge_date": "2026-03-24",
  "policy_verification": {
    "pol_001_ok": true,
    "tailwind_radix_only": true,
    "overrides_section_preserved": true
  }
}
```

## Integration

- Receive `merge` decisions from `autoskill-judge`
- Modify files under `.cursor/skills/`
- Optionally trigger `skill-optimizer` after merge

## Examples

### Example 1: Trigger merge

Existing: `policy-text-generator` (8 triggers)
Candidate: 2 new Korean triggers + 1 tone constraint

Result:
- Triggers: remove 1 duplicate from existing 8, add 2 new → trim to 8 by priority
- Constraints: add to tone guideline section
- Version: 1.0.0 → 1.0.1

### Example 2: Workflow extension merge

Existing: `doc-quality-gate` (unified 7 dimensions)
Candidate: add “accessibility” dimension

Result:
- Add dimension or extend an existing dimension (by scope)
- No conflict → auto-merge
- Version: 1.0.0 → 1.0.1

## Error Handling

| Error | Response |
|-------|----------|
| Target skill missing | Verify path; re-check autoskill-judge decision |
| Candidate JSON parse error | Validate format; suggest re-running autoskill-extractor |
| Body exceeds 500 lines after merge | Move large blocks to `references/` |
| Unresolvable conflict | Flag human review; preserve both versions for review |
| Post-merge policy check fails | Revert or fix SKILL.md; do not mark merge complete |

---

## Project-Specific Overrides

Applies only in **ai-model-event-stock-analytics**.

| Override | Path |
|----------|------|
| Terminology (POL-001) | [.cursor/skills/references/project-overrides/project-terminology-glossary.md](../references/project-overrides/project-terminology-glossary.md) |
| Design / UI stack | [.cursor/skills/references/project-overrides/project-design-conventions.md](../references/project-overrides/project-design-conventions.md) |

**Constraints:** Run **post-merge validation** against POL-001 terminology; ensure design system references are **Tailwind+Radix**, not TDS; **preserve** the **Project-Specific Overrides** section when present.
