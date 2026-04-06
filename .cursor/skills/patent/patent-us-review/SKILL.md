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
  patent-us-oa-response). Korean triggers: "미국 특허 검토", "101 분석",
  "Alice 분석", "112 검토", "특허 품질 검토".
metadata:
  version: "1.0.0"
  category: "review"
  author: "thaki"
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
- Identify any claim limitations that invoke 112(f)
- Verify corresponding structure in specification
- Flag unintended 112(f) invocations

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

Severity levels:
- **CRITICAL**: Near-certain rejection; must fix before filing
- **HIGH**: Likely rejection; strongly recommend fixing
- **MEDIUM**: Possible issue; consider addressing
- **LOW**: Minor risk; optional improvement

### Step 8: Claim Scorecard

| Claim | 101 | 102 | 103 | 112(a) | 112(b) | Overall |
|-------|-----|-----|-----|--------|--------|---------|
| 1 | A/B/C/D/F | A/B/C/D/F | ... | ... | ... | [grade] |

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
