---
name: spec-quality-gate
description: >-
  기획서의 완성도, 일관성, 정책 정합성을 자동 검증하고 품질 리포트를
  생성합니다. 7개 검증 항목(필수 섹션, 상태 커버리지, 예외 상황, 정책 정합성,
  용어 일관성, API 정합성, 디자인 참조)을 점검합니다. Use when the user asks to
  "기획서 점검", "기획서 리뷰", "스펙 검증", "문서 품질 검사", "spec quality
  check", "review spec", "validate spec", "기획서 품질", "문서 완성도 확인",
  "spec-quality-gate", or wants to verify that planning documents meet quality
  standards before handoff. Do NOT use for generating specs from code (use
  code-to-spec). Do NOT use for code review (use code review tools). Do NOT use for
  general document editing (use technical-writer). Do NOT use for skill file
  auditing (use skill-optimizer). Korean triggers: "기획서 점검", "기획서 리뷰",
  "스펙 검증", "문서 품질", "품질 게이트".
metadata:
  author: "thaki"
  version: "1.0.1"
  category: "review"
---
# Spec Quality Gate — Planning document quality check

Validate completeness and consistency across seven dimensions and emit a structured quality report.

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Input

| Input | Required | Notes |
|------|----------|------|
| **Spec path** | **Yes** | `.md` file or directory (recursive if directory) |
| Policy doc path | Optional | For policy alignment checks |
| API spec path | Optional | Swagger/OpenAPI for API alignment |
| Glossary path | Optional | Default: [references/terminology-guide.md](references/terminology-guide.md) |

---

## Workflow

### Step 1: Load specs

1. Discover spec files under the target path
2. Parse structure (headings, sections, tables, checklists)
3. Note linked artifacts (policy, API, design)

### Step 2: Run seven checks

Details: [references/quality-checklist.md](references/quality-checklist.md)

#### 2.1 Required sections

| Required section | Severity |
|-----------------|----------|
| Screen overview | Critical |
| Feature list | Critical |
| Per-state UI | Critical |
| Exception handling | High |
| User flow | High |
| API integration | Medium |
| Changelog | Medium |

- Verify equivalent headings exist
- Empty shells → classify as “heading only” (High)

#### 2.2 State coverage

For every data screen:
- loading defined?
- error defined?
- empty defined?
- success defined?

**Verdict:**
- 4/4 → PASS
- 3/4 → Medium (name missing state)
- ≤2/4 → High

#### 2.3 Exception documentation

- Exceptions table present?
- Each row: trigger, handling, user-facing message?
- At least three documented exceptions?

**Verdict:**
- ≥3 complete → PASS
- ≥3 incomplete → Medium
- <3 → High

#### 2.4 Policy alignment

Only if policy doc provided:
- Copy/behavior matches policy
- Policy rules reflected in spec
- List conflicts

#### 2.5 Terminology

Against [references/terminology-guide.md](references/terminology-guide.md):
- Same concept, different labels (e.g. mixed terms for “order”)
- Raw framework jargon in planner-facing text
- Drift from agreed team terms

#### 2.6 API alignment

Only if API spec provided:
- Endpoints in spec vs OpenAPI
- Method/param mismatches
- Implemented APIs missing from spec
- Spec-only APIs not implemented

#### 2.7 Design references

- Figma or design file link
- Design-system component usage called out
- Layout description present

### Step 3: Quality report

```markdown
## Spec Quality Report

### Summary
- **Target**: [path]
- **Date**: YYYY-MM-DD
- **Verdict**: PASS / FAIL (PASS if Critical = 0)

| Severity | Count |
|----------|-------|
| Critical | [N] |
| High | [N] |
| Medium | [N] |
| Low | [N] |

### Critical issues
1. **[Check] Title**
   - Location: ...
   - Current: ...
   - Expected: ...
   - Fix: ...

### High issues
...

### Passed checks
- [Item] ✅ ...

### Coverage matrix
| Check | Result | Notes |
|-------|--------|-------|
| Required sections | PASS/FAIL | ... |
| State coverage | PASS/FAIL | ... |
| Exceptions | PASS/FAIL | ... |
| Policy | PASS/FAIL/SKIP | ... |
| Terminology | PASS/FAIL | ... |
| API | PASS/FAIL/SKIP | ... |
| Design refs | PASS/FAIL | ... |
```

### Step 4: Auto-fix (optional)

If the user says “fix it” or passes `--fix`:
1. Fix Critical first
2. Empty sections → template with TODO placeholders
3. Missing states → add rows with `{TODO}`
4. Terminology → replace per glossary
5. Re-run validation

---

## Examples

### Example 1: Directory scan

User: "Check specs under docs/specs/orders/"

Actions: load 3 files, run 7 checks, report Critical/High/Medium counts and FAIL if Critical > 0.

### Example 2: Fix mode

User: "Check the spec and fix it --fix"

Actions: insert state table template, re-run, PASS when Critical cleared.

### Example 3: Policy + API cross-check

User: "Check this spec against policy and API"

Actions: load all three; report APIs present in code but missing from spec.

Result: Detailed report including cross-check findings.

---

## Error Handling

| Error | Response |
|-------|----------|
| Spec file missing | Reconfirm path |
| Unparseable format | Check recognizable sections only; SKIP rest |
| No policy doc | SKIP policy alignment |
| No API spec | SKIP API alignment |
| Very large spec | Split validation by section |

## Troubleshooting

- **High false positives**: Tune glossary for the project
- **Too strict**: Reserve Critical for missing required sections and undefined states
- **Design ref always fails**: Early-phase specs may lack design — downgrade to Medium
