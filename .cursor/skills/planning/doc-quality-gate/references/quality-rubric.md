# Document Quality Rubric (Unified)

Reference for `doc-quality-gate` v2: seven weighted dimensions, legacy six binary lenses, and document-type specifics. **Skill outputs are Korean; this file may mix EN/KR for precision.**

## Part A — Seven dimensions (primary scoring)

### 1. Required sections (20%)

**Passing (high score):** All required sections for the document type exist, are non-empty, and avoid placeholders (TBD/TODO without owners).

**Include checks from legacy “Completeness + Clarity + Actionability”:**

- Requirements use testable language; prefer RFC 2119 style (MUST/SHOULD/MAY) where appropriate.
- Red-flag vague phrasing: see [ambiguity-patterns.md](ambiguity-patterns.md) and Clarity red flags in Part B.
- PRD: problem, goals, users, functional + non-functional requirements, success metrics, constraints, timeline/milestones.
- Feature spec / execution spec: feature overview, screens/flows, states, edge cases, interactions, data requirements.
- Policy: purpose, scope, rules, enforcement, effective date, exceptions, ownership.

**Per-type tables:** [completeness-checklist.md](completeness-checklist.md), [checklist.md](checklist.md), [quality-checklists/](quality-checklists/).

### 2. State coverage (20%)

For each major screen/flow/component, verify defined UX/system behavior for:

| State | Required |
|-------|----------|
| Normal / default | Yes |
| Loading | Yes |
| Error | Yes |
| Empty | Yes |
| Disabled / unavailable | When applicable |
| Success (completion) | When applicable |

Also check: permission variants (logged out / role), and transition conditions where stated.

**Extended checklist (12-state model, use subset per feature):** default, loading, empty, partial data, success, validation error, network error, server error, auth error, timeout, permission denied, disabled.

### 3. Edge cases (15%)

Categories: input (empty, max length, format, special chars), network (offline, timeout, slow, duplicate submit), concurrency, permissions (session expiry, role change), data (null, type mismatch, large volume), environment (i18n, dark mode, a11y, low-end devices).

Standard list (15): empty input, max-length input, special characters, concurrent requests, double submit, back button, refresh, session timeout, large dataset, no data → first data, deleted reference, timezone, offline transition, permission change mid-session, multi-device sync.

### 4. Policy compliance (15%)

When a policy document is supplied:

- UI copy vs policy (errors, consent, collection notices).
- Data practices vs privacy/terms alignment.
- Contradictions and missing citations (policy IDs/links).

**If no policy supplied:** dimension = **N/A** (exclude from denominator; state in report).

Qualitative scale (from inspector rubric): 10 = fully reflected; 7 = minor gaps; 5 = incomplete; 1 = ignored.

### 5. Terminology consistency (10%)

Detect synonym mixing, feature name drift, state label drift, acronym inconsistency. Examples: 사용자/유저/고객, 로딩/처리 중, error/에러/오류.

Scoring aid: `max(0, 10 - 2 × inconsistency_cluster_count)` scaled to 0–100 as needed.

### 6. API alignment (10%)

- APIs/endpoints referenced or specified; request/response and error codes where relevant.
- Alignment between narrative spec and any schema/field tables.
- Versioning and traceability to technical doc links.

### 7. Design references (10%)

- Figma or design file links; design system / component references.
- Links to related PRDs, specs, ADRs, test/QA docs.
- Decision rationale and change/version history when expected by org template.

**Org template reminder:** title format `[카테고리] 문서명 — YYYY-MM-DD`, metadata (author, date, status, version) when applicable.

---

## Part B — Legacy six binary lenses (supporting signals)

Use these as **PASS/FAIL hints** inside narrative scoring; they do not replace the seven dimensions.

### 1. Completeness

**Pass:** Required sections for type present and non-empty.  
**Fail:** Missing or placeholder-only sections.

| Document Type | Required Sections (minimum) |
|---------------|------------------------------|
| PRD | Problem Statement, User Stories/Requirements, Success Metrics, Scope, Timeline |
| Spec | Overview, Requirements (functional + non-functional), Constraints, Acceptance Criteria |
| Policy | Purpose, Scope, Rules/Guidelines, Enforcement, Effective Date |
| Guideline | Purpose, When to Apply, Instructions, Examples, Exceptions |
| Postmortem | Incident Summary, Timeline, Root Cause, Impact, Action Items |
| Research | Objective, Methodology, Findings, Implications, Limitations |

### 2. Clarity

**Pass:** Unambiguous language; terms defined; no passive-voice mush in requirements.  
**Fail:** Vague terms, undefined acronyms, agentless requirements.

Red flags: "적절한/appropriate" (undefined), "필요 시/if necessary" (no condition), "등/etc." in requirements, "가능한/as possible" (no constraint), "일반적으로/generally" in rules.

### 3. Consistency

**Pass:** One term per concept; no cross-section contradictions.  
**Fail:** Synonym drift; conflicting numbers/dates/status values.

### 4. Actionability

**Pass:** Action items have owner, deadline, measurable outcome; stories have acceptance criteria.  
**Fail:** Floating tasks; unmeasurable outcomes.

### 5. Traceability

**Pass:** Links to related docs; decision context; change history where appropriate.  
**Fail:** Isolated doc; broken links.

### 6. Compliance

**Pass:** Follows template, naming, metadata, language rules (Korean body, English technical terms).  
**Fail:** Template/metadata violations.

**Legacy binary score:** `Total = sum of six PASS (1) / FAIL (0)` → max 6. Optional diagnostic only; map results into dimensions 1, 5, 6, 7.

---

## Part C — Inspector numeric rubric (optional deep scoring)

Categories from the former inspector `quality-rubric.md` can inform dimension scores:

1. **Structure completeness** — section coverage × quality of structure.  
2. **State coverage** — mean coverage across features × 10 (scale to 0–100).  
3. **Edge cases** — addressed / applicable × 10.  
4. **Policy reflection** — qualitative 1–10 scale → map to dimension 4.  
5. **Terminology** — `10 - 2 × inconsistency_count`, cap 0–10 → map to dimension 5.  
6. **Testability** — testable requirements / total → maps into dimensions 1 and 3.

---

## Failure prioritization (legacy gate)

| Priority | Focus | Rationale |
|----------|--------|-----------|
| 1 | Required sections | Missing sections = missing intent |
| 2 | Clarity inside sections | Ambiguity → wrong build |
| 3 | Actionability | No owners → no delivery |
| 4 | Consistency | Contradictions → rework |
| 5 | Traceability | Context loss |
| 6 | Template compliance | Discoverability |

---

## Severity of findings

| Severity | Meaning | Example |
|----------|---------|---------|
| Critical | Blocks purpose | No requirements in a PRD |
| High | Likely wrong implementation | No error states; policy conflict |
| Medium | Understandable but weak | Term drift; partial TBD |
| Low | Polish | Format; minor link issues |
