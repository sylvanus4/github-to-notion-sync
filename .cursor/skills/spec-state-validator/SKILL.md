---
name: spec-state-validator
description: >-
  Validate that code implementation covers all states, transitions, and edge
  cases defined in a PRD or spec document. Cross-references spec definitions
  against actual code to find coverage gaps. Use when the user asks to "validate
  spec coverage", "check state implementation", "스펙-코드 검증", "상태값 구현
  확인", "엣지케이스 커버리지", "spec validation", "기획서 대비 구현 확인",
  "누락 상태 검사", or needs to verify code matches its specification. Do NOT
  use for reverse-engineering specs from code (use code-to-spec), general
  code review (use code-reviewer), or document quality scoring (use
  doc-quality-gate).
metadata:
  author: thaki
  version: "1.0.1"
  category: review
---

# Spec-State Validator

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

Cross-reference product specifications against code implementation to detect coverage gaps: missing states, unhandled transitions, unimplemented edge cases, and policy violations. Produces a coverage report with specific file locations and remediation guidance.

## Input

The user provides:
1. **Spec source** — PRD/spec file path, Notion page URL, or inline spec content
2. **Code scope** — Directory path or file list to validate against
3. **Focus area** — Optional: `states`, `transitions`, `edge-cases`, `policies`, `all` (default: `all`)

## Workflow

### Step 1: Parse Specification

Extract testable artifacts from the spec document:

1. **State definitions** — All explicitly named states, statuses, or modes
2. **Transitions** — State-to-state transitions with trigger conditions
3. **Edge cases** — Explicitly documented edge cases and expected behaviors
4. **Business rules** — Conditional logic requirements
5. **Error scenarios** — Expected error states and handling requirements
6. **Policy constraints** — Compliance rules that must be enforced in code

Parse into a structured checklist. See [references/state-coverage-checklist.md](references/state-coverage-checklist.md) for the checklist format.

```
Spec Artifact: [name]
Type: state | transition | edge-case | rule | error | policy
Description: [what the spec says]
Expected in code: [what to look for]
```

### Step 2: Scan Code

For each spec artifact, search the code scope:

| Artifact Type | Search Strategy |
|---------------|-----------------|
| State | Grep for enum values, string literals, status constants matching spec state names |
| Transition | Find conditional blocks that change state; verify trigger matches spec |
| Edge case | Search for guard clauses, null checks, boundary validations matching spec scenarios |
| Business rule | Find conditional logic with domain constants matching spec rules |
| Error scenario | Search catch blocks, error handlers matching spec error states |
| Policy constraint | Find validation logic, permission checks matching spec policies |

For each artifact, record:
- **Found**: Yes/No
- **Location**: File path + line number
- **Implementation match**: Full/Partial/None
- **Notes**: Any deviation from spec

### Step 3: Gap Analysis

Classify findings into coverage categories:

| Category | Definition | Severity |
|----------|------------|----------|
| Covered | Spec artifact fully implemented in code | OK |
| Partially covered | Implementation exists but incomplete or deviating | Medium |
| Missing | Spec artifact has no corresponding code implementation | High |
| Extra | Code handles states/cases not mentioned in spec | Info |
| Contradicting | Code behavior contradicts spec requirement | Critical |

### Step 4: Generate Coverage Report

```markdown
# Spec-State Validation Report

## Summary
- Spec: [document title]
- Code scope: [directory/files]
- Coverage: [N]% ([covered]/[total] artifacts)
- Gaps: [N] missing, [N] partial, [N] contradicting

## Coverage Matrix

### States
| State | In Spec | In Code | Location | Status |
|-------|---------|---------|----------|--------|
| PENDING | Yes | Yes | order.ts:15 | Covered |
| PROCESSING | Yes | No | — | MISSING |

### Transitions
| From | To | Trigger | In Code | Location | Status |
|------|-----|---------|---------|----------|--------|
| PENDING | CONFIRMED | payment_success | Yes | order.ts:42 | Covered |
| PENDING | CANCELLED | timeout_24h | No | — | MISSING |

### Edge Cases
| # | Scenario | In Code | Location | Status |
|---|----------|---------|----------|--------|
| 1 | Empty cart checkout | Yes | cart.ts:88 | Covered |
| 2 | Concurrent edit | No | — | MISSING |

### Policy Constraints
| Policy | Required Behavior | In Code | Status |
|--------|-------------------|---------|--------|
| Max retry 3x | Retry counter with 3 limit | Yes | Covered |
| PII masking | Log sanitization | No | MISSING |

## Extra Coverage (in code, not in spec)
[Items found in code that have no corresponding spec entry]

## Remediation Plan
[Ordered list of items to implement, grouped by severity]
```

## Skill Chain

| Step | Skill | Purpose |
|------|-------|---------|
| 1 | Notion MCP | Fetch spec from Notion if URL provided |
| 2 | (self) | Parse spec + scan code + gap analysis |
| 3 | code-to-spec | Generate spec for "extra" items found only in code |
| 4 | md-to-notion | Publish coverage report to Notion |
| 5 | cross-domain-sync-checker | Feed gaps back into sync tracking |

## Examples

### Example 1: PRD vs implementation validation

User says: "Validate code against this PRD — PRD: [URL], code: src/features/checkout/"

Actions:
1. Fetch PRD, extract 8 states, 12 transitions, 15 edge cases
2. Scan `src/features/checkout/` for each artifact
3. Result: 85% coverage — 2 missing states, 3 unhandled edge cases
4. Generate report with specific file locations for covered items and remediation plan for gaps

Result: Coverage report showing PROCESSING and PARTIAL_REFUND states missing from implementation

### Example 2: Policy compliance check

User says: "Validate code against our privacy policy"

Actions:
1. Parse privacy policy: PII masking, retention limits, consent requirements
2. Scan codebase for logging, storage, and consent logic
3. Find: consent check missing in 2 API endpoints, log sanitization missing in 1 file
4. Generate policy compliance gap report

Result: 3 policy violations identified with exact file locations and fix instructions

## Error Handling

| Error | Action |
|-------|--------|
| Spec document not found | Ask user for correct path or URL |
| Spec has no testable artifacts | Report that no states, transitions, or rules were found; suggest using `code-to-spec` instead |
| Code scope too large (>100 files) | Ask user to narrow scope; or process in batches with progress reports |
| Ambiguous spec language | Flag as "untestable" with explanation; suggest clarifying the spec |
| Code in unsupported language | Report limitation; process supported files and skip others |
| No gaps found | Report 100% coverage with congratulatory summary |
