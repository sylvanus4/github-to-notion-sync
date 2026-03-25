---
name: autoskill-judge
description: >-
  autoskill-extractor가 생성한 스킬 후보를 평가하여 add(신규 추가),
  merge(기존 스킬에 병합), discard(폐기) 결정. 기존 스킬과의 capability
  identity를 비교하여 중복 방지.
  Use when processing extracted candidates, "스킬 후보 평가", "autoskill judge",
  "evaluate skill candidate", "스킬 후보 판정", "add or merge decision".
  Do NOT use for skill quality auditing (use skill-optimizer), creating skills
  from scratch (use create-skill), or general code review.
metadata:
  author: thaki
  version: "1.0.1"
  category: self-improvement
---

# AutoSkill Judge

Evaluate skill candidates from `autoskill-extractor` and decide add, merge into an existing skill, or discard. Compare **capability identity** against existing skills to avoid duplicates.

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Input

- Candidate JSON from `outputs/autoskill-candidates/`
- Existing skills under `.cursor/skills/`

## Workflow

### Step 1: Find similar skills

Find the top 3 existing skills most similar to the candidate:
- Search using candidate name, description, triggers
- Compare to each skill’s SKILL.md frontmatter

### Step 2: Capability identity test

For each similar skill, score on four axes:

| Axis | Question |
|------|----------|
| **Job-to-be-done** | Do both solve the same core problem? |
| **Deliverable type** | Do both produce the same kind of output? |
| **Hard constraints** | Do both enforce similar quality rules? |
| **Required tools/workflow** | Do both use a similar tool chain? |

If 3+ axes align → treat as **same capability**.

### Step 3: Apply decision logic

**Policy-based judgment (this repository — ai-model-event-stock-analytics):** Before finalizing `add` / `merge`, score the candidate against **financial analytics** relevance (signals, data pipelines, trading ops, stock UI). **DISCARD** if the candidate **introduces POL-001 forbidden terms** or **requires** Thaki Cloud **TDS** (`@thakicloud/shared`), **Figma**, or **Thaki Cloud platform** runtime as mandatory (this app is React + FastAPI + Tailwind + Radix). Prefer candidates that align with `docs/policies/01-product-identity.md` and [.cursor/skills/references/project-overrides/project-terminology-glossary.md](../references/project-overrides/project-terminology-glossary.md).

**DISCARD** when:
- Captures a generic, non-portable task
- confidence < 0.6
- Duplicates an existing skill with no new constraints
- Conflicts with project conventions without user confirmation
- Scope is too narrow (single file/module only)
- **Policy**: Introduces disallowed terminology (POL-001) or mandates TDS/Figma/Thaki Cloud product stack for this repo
- **Domain**: Near-zero financial/stock relevance when the candidate purports to be a product workflow for this codebase

**MERGE** when:
- Same capability as an existing skill (same job-to-be-done)
- Candidate adds constraints, triggers, or improvements to that skill
- After removing instance details, both serve the same purpose
- Merge strengthens the existing identity without breaking it

**ADD** when:
- No existing skill covers this capability family
- Genuinely new workflow or preference pattern
- Deliverable type or target audience differs materially from existing skills

### Step 4: Hard rules

- Same capability → **forbid** `add` (must be `merge` or `discard`)
- Name collision after normalization → **forbid** `add`
- Primary deliverable class differs → different capability → `add` OK
- Intended audience differs materially → different capability → `add` OK
- **Forbid** `add`/`merge` that would embed **TDS / Figma / Thaki Cloud** as the default design or deployment SSOT for this project; those outcomes must be **discard** or rewritten first

## Output

```json
{
  "action": "add|merge|discard",
  "target_skill_id": "existing-skill-name or null",
  "confidence": 0.85,
  "reason": "Concise explanation of the decision",
  "similar_skills": [
    {"name": "skill-name", "similarity": 0.82, "same_capability": true}
  ]
}
```

Persist decisions to `outputs/autoskill-decisions/<date>-<candidate-name>.json`.

## Integration

- Receive candidates from `autoskill-extractor`
- On `merge` → hand off to `autoskill-merger`
- On `add` → hand off to skill creation flow

## Examples

### Example 1: Merge

Candidate: "korean-friendly-tone" (keep Korean-friendly tone)  
Similar: "policy-text-generator" (includes tone/voice guidelines)

Decision: **MERGE** — same job-to-be-done (copy generation); candidate adds tone constraints.

### Example 2: Add

Candidate: "api-changelog-generator" (auto API changelogs)  
Similar: "technical-writer" (similarity 0.45)

Decision: **ADD** — deliverable type (changelog vs general docs) and workflow differ.

### Example 3: Discard

Candidate: "fix-typo-in-readme" (fix README typo)

Decision: **DISCARD** — one-off task, not reusable.

## Error Handling

| Error | Response |
|-------|----------|
| Missing candidate file | Verify path; suggest running autoskill-extractor |
| Cannot list existing skills | Verify directory path |
| Ambiguous capability | Lower confidence; flag human review |
| Multiple merge targets | Pick highest similarity; log alternatives |

---

## Project-Specific Overrides

Applies only in **ai-model-event-stock-analytics**.

| Override | Path |
|----------|------|
| Terminology / POL-001 | [.cursor/skills/references/project-overrides/project-terminology-glossary.md](../references/project-overrides/project-terminology-glossary.md) |
| UI stack (Tailwind + Radix) | [.cursor/skills/references/project-overrides/project-design-conventions.md](../references/project-overrides/project-design-conventions.md) |

**Constraints:** Judge candidates against **POL-001** forbidden terms; **reject** skills that **require** TDS, Figma, or Thaki Cloud platform assumptions; include **financial domain relevance** in the rationale when the candidate is workflow-oriented.
