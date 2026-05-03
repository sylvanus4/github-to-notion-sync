---
name: patent-us-review
description: >-
  Review US patent application drafts for compliance with 35 USC 101
  (subject-matter eligibility, Alice/Mayo), 102 (novelty), 103
  (non-obviousness), and 112 (written description, enablement, definiteness).
  Produces a severity-ranked issue report with specific fix suggestions and
  claim-by-claim scoring. Use when the user asks to "review US patent draft",
  "check patent compliance", "101 analysis", "Alice review", "112 check",
  "patent quality review", or "pre-filing review". Do NOT use for Korean
  patent review (use patent-kr-review). Do NOT use for drafting (use
  patent-us-drafting). Do NOT use for office action responses (use
  patent-us-oa-response). Korean triggers: "미국 특허 검토", "101 분석", "Alice 분석",
  "112 검토", "특허 품질 검토".
---

# US Patent Review — Statutory Compliance Analysis

## Role

Expert US patent examiner-perspective reviewer who analyzes patent application
drafts against all four statutory requirements, identifies prosecution risks
before filing, and suggests concrete revisions to strengthen the application.

## Prerequisites

- US patent draft (claims + specification from patent-us-drafting or user input)
- Prior art references (from patent-search, optional)
- Write tool for persisting results to `outputs/patent-us-review/{date}/`

## Workflow

### Step 0: Input Validation

Before any statutory analysis, verify inputs. If validation fails, stop or document limitations explicitly in the report.

| Requirement | Rule |
|-------------|------|
| **(a) Complete claim set** | Require the full claim set (all pending claims). **Reject or halt** if only partial/incomplete claims are provided; request the complete set before proceeding. |
| **(b) Specification text** | Require specification text (at least the portions supporting the claims). |
| **(c) Known prior art** | Collect any prior art references the user or drafter has identified. |

**If specification is missing:** Proceed only with user acknowledgment; **warn prominently** that **112(a)/112(b)/written description and enablement analysis will be limited** and support for amendments cannot be fully assessed.

**If prior art is missing:** **Skip 102 and 103 analysis** (or mark those columns as "N/A — prior art not provided") and **note explicitly** in the report that novelty and non-obviousness were not evaluated against references.

### Step 1: Claim Parsing

Parse each claim into structured elements:
- Claim number, type (independent/dependent), category (method/system/CRM)
- Preamble, transitional phrase, body elements
- Dependency chain for dependent claims

### Step 2: 35 USC 101 — Subject-Matter Eligibility

Apply the Alice/Mayo two-step framework to each independent claim:

**Step 2A — Prong 1: Judicial Exception?**
Does the claim recite:
- Abstract idea (mathematical concept, mental process, method of organizing
  human activity)?
- Law of nature?
- Natural phenomenon?

**Step 2A — Prong 2: Practical Application?**
If judicial exception found, does the claim integrate it into a practical
application by:
- Improving computer/technology functionality?
- Applying the exception with a particular machine?
- Transforming an article to a different state/thing?
- Applying in a meaningful way beyond "apply it"?

**Step 2B: Inventive Concept?**
Does the claim recite additional elements that amount to significantly more
than the judicial exception, individually or in combination?

Score each independent claim:

| Claim | Judicial Exception | Practical Application | Inventive Concept | Risk Level |
|-------|-------------------|----------------------|-------------------|------------|
| 1 | [Type or None] | [Yes/No + reason] | [Yes/No + reason] | Low/Medium/High |

**Alice Completeness Gate (mandatory before proceeding to Step 3):**
1. List ALL independent claim numbers parsed in Step 1.
2. Verify each independent claim has a completed row in the table above with all four columns filled.
3. If any independent claim is missing, add its analysis now — do NOT proceed with a gap.

**Anti-Software-Bias Self-Check:** For every independent claim scored Medium or High risk, re-read Anti-Pattern #1 and confirm the risk rating is based on the full 2A/2B analysis, not on the mere fact that the claim involves software or an algorithm.

### Step 3: 35 USC 102 — Novelty

For each independent claim, assess against known prior art:
- Is every element disclosed in a single prior art reference?
- Identify the closest single reference
- If anticipated, identify which elements are disclosed and which are novel

### Step 4: 35 USC 103 — Non-Obviousness

For each independent claim:
- Identify the closest prior art combination (max 3 references)
- Assess motivation to combine
- Check for teaching away
- Evaluate secondary considerations (commercial success, long-felt need,
  failure of others, unexpected results)

### Step 5: 35 USC 112 — Disclosure Requirements

**112(a) Written Description**:
- Does the specification describe the claimed invention in sufficient detail
  that a PHOSITA would recognize the inventor had possession?
- Are all claim terms adequately described?

**112(a) Enablement**:
- Can a PHOSITA make and use the full scope of the claimed invention without
  undue experimentation?
- Wands factors assessment where applicable

**112(b) Definiteness**:
- Are claim terms clear and definite?
- Any terms of degree without clear standard?
- Antecedent basis for all "said" / "the" references?
- Means-plus-function elements identified and properly supported?

**112(f) Interpretation Check**:
- Scan ALL claims for the following trigger expressions that may invoke 112(f):
  - "means for …", "step for …"
  - "configured to …", "adapted to …", "operable to …"
  - "module for …", "mechanism for …", "unit for …"
  - Any nonce word + functional language pattern (e.g., "widget for processing")
- For each detected trigger expression: determine if 112(f) is invoked, verify corresponding structure in specification, and flag unintended invocations
- If NO trigger expressions are detected, explicitly state "No 112(f) trigger expressions found" — do not silently skip this section

### Step 6: Cross-Cutting Issues

Check for:
- Claim dependency errors (referencing non-existent claims)
- Terminology inconsistency between claims and specification
- Missing claim support in specification (any claim element not described)
- Double patenting risk (if related applications known)
- Restriction/election risk (multiple independent inventions)

### Step 7: Generate Review Report

Produce a severity-ranked issue list:

| # | Severity | Statute | Claim(s) | Issue | Suggested Fix |
|---|----------|---------|----------|-------|---------------|
| 1 | CRITICAL | 101 | 1, 8, 15 | [description] | [fix] |
| 2 | HIGH | 112(b) | 3 | [description] | [fix] |
| 3 | MEDIUM | 103 | 1 | [description] | [fix] |
| 4 | LOW | 112(a) | 5 | [description] | [fix] |

**CRITICAL Issue Completeness Rule:** Every row marked **CRITICAL** MUST contain all three of:
1. **Statutory basis** — the specific statute subsection (e.g., "101 Step 2A Prong 2")
2. **Concrete example** — why this claim would likely be rejected, citing specific claim language or missing disclosure
3. **Actionable fix** — a specific revision (e.g., "add limitation X from spec ¶Y" or "recite the specific data transformation step"), never vague suggestions like "strengthen" or "clarify"

If any CRITICAL row lacks one of these three, downgrade to HIGH or add the missing component before delivery.

Severity levels:
- **CRITICAL**: Near-certain rejection; must fix before filing
- **HIGH**: Likely rejection; strongly recommend fixing
- **MEDIUM**: Possible issue; consider addressing
- **LOW**: Minor risk; optional improvement

### Step 8: Claim Scorecard

| Claim | 101 | 102 | 103 | 112(a) | 112(b) | Overall |
|-------|-----|-----|-----|--------|--------|---------|
| 1 | A/B/C/D/F | A/B/C/D/F | ... | ... | ... | [grade] |

**Scorecard Completeness Gate:** The table MUST include one row for EVERY claim in the pending claim set (from Step 1). If the claim set has N claims, the scorecard must have exactly N rows — omission of any claim is a blocking defect. For 102/103 columns: if prior art was not provided, mark "N/A" rather than omitting the row.

### Step 9: Persist Output

Write to `outputs/patent-us-review/{date}/`:
- `review-report.md` — full severity-ranked issue report
- `claim-scorecard.md` — per-claim grading table
- `101-analysis.md` — detailed Alice/Mayo analysis
- `review-summary.json` — structured summary

## Anti-Patterns (DO NOT)

1. **DO NOT** mark a claim as "failing 101" merely because it involves software — perform the **full Alice two-step** analysis (including practical application / inventive concept where applicable).
2. **DO NOT** assign **CRITICAL** severity without a **specific statutory basis** (e.g., 101, 102, 103, 112) **and** a **concrete example** of why the claim would likely be rejected or is fatally defective.
3. **DO NOT** skip **112(f)** analysis for claims using **"configured to"** or other means-style language — analyze whether **corresponding structure** is adequately disclosed or whether 112(f) is unintentionally invoked.
4. **DO NOT** provide vague fix suggestions such as "strengthen the claim" — every fix must be **specific and actionable** (e.g., add limitation X from spec ¶Y, or replace term Z with antecedent-supported language).
5. **DO NOT** rate all claims the same grade — **differentiate** independent vs. dependent claim strength and reflect different risk profiles where supported.

## Worked Example: 101 Analysis Entry (Test Invention)

**Test invention context:** LLM Agent Orchestration Platform that dynamically composes multi-agent workflows from a skill registry using semantic-search-based routing, DAG-based execution ordering, and resource-aware model selection.

**Example 101 analysis row (illustrative):**

> Claim 1 recites "performing a semantic search… constructing a DAG… selecting a language model tier" — **Step 2A Prong 1:** may recite abstract ideas (e.g., mathematical/graph concepts and data comparison). **Step 2A Prong 2:** integrated into a **practical application** — the claim specifies dispatching agent skills to selected model tiers and persisting results at checkpoints for failure recovery, which can be framed as **specific technical improvements** to multi-agent system reliability and execution control. **RISK: LOW** (fact-specific; tie each element to spec support in the actual review).

### Step 10: Pre-Delivery Check

Before delivering the review package to the user, confirm **all** of the following:

1. **Scorecard completeness:** Every claim in the pending set has at least one row/grade in the claim scorecard (no omitted claims).
2. **CRITICAL issues:** Every **CRITICAL** finding includes a **specific, actionable fix** and, where applicable, a **specification paragraph reference** (or explicit "add new paragraph" instruction if support is missing).
3. **101 coverage:** **Alice/Mayo (Step 2A/2B) analysis is completed for every independent claim** — no independent claim left without eligibility analysis.
4. **Severity distribution:** Severity counts are **not artificially uniform** — if every issue is CRITICAL or every issue is LOW, re-check whether differentiation is justified; independent vs. dependent claim strength should differ where the record supports it.

## Output Artifacts

| Artifact | Path | Format |
|----------|------|--------|
| Review report | `outputs/patent-us-review/{date}/review-report.md` | Markdown |
| Claim scorecard | `outputs/patent-us-review/{date}/claim-scorecard.md` | Markdown |
| 101 analysis | `outputs/patent-us-review/{date}/101-analysis.md` | Markdown |
| Structured summary | `outputs/patent-us-review/{date}/review-summary.json` | JSON |

## Constraints

- This is a pre-filing risk assessment, NOT legal advice
- Always recommend attorney review for CRITICAL and HIGH issues
- Do not make definitive patentability conclusions
- Review is based on publicly available prior art only

## Gotchas

- Abstract idea categories keep evolving via Federal Circuit decisions
- "Improvements to computer functionality" is the strongest 101 argument
  for software patents
- Specification amendments are limited after filing — catch 112 issues NOW
- 103 analysis requires articulating motivation to combine, not just finding
  elements across references
- Functional claiming at the point of novelty invites 112 challenges
