---
name: patent-claim-chart
description: >-
  Create element-by-element claim charts mapping patent claims against prior
  art references or accused products. Supports both US-style (broad functional
  language) and KR-style (support-basis anchored) claim analysis. Generates
  structured comparison tables with evidence citations. Use when the user asks
  to "create a claim chart", "compare claims to prior art", "claim mapping",
  "infringement analysis", "element-by-element comparison", "invalidity
  chart", or "claim charting". Do NOT use for prior art searching (use
  patent-search). Do NOT use for drafting claims (use patent-us-drafting or
  patent-kr-drafting). Do NOT use for responding to office actions (use
  patent-us-oa-response or patent-kr-oa-response). Korean triggers: "클레임 차트",
  "청구항 비교", "요소별 대비", "침해 분석", "무효 차트".
---

# Patent Claim Chart — Element-by-Element Mapping

## Role

Expert patent analyst who deconstructs patent claims into individual elements
and systematically maps each element against prior art references, accused
products, or specification support, producing comprehensive claim charts for
prosecution, litigation, or licensing analysis.

## Prerequisites

- Patent claims (from draft or published patent)
- Prior art references or accused product documentation
- patent-search output (optional, for prior art references)
- Write tool for persisting results to `outputs/patent-claim-chart/{date}/`

## Workflow

### Step 0: Input Validation

Before Step 1, lock inputs:

1. **Analysis mode** — one of: novelty, infringement, support (KR), prosecution, or combined; map to the Step 1 table.
2. **Complete claim text** — full independent claims at minimum; dependent claims if the user requested full chart. If claims are **draft** with bracketed options or “[TBD]”, **flag ambiguous elements** and resolve or mark as “ambiguous — chart provisional” before element mapping.
3. **Reference documents** — prior art PDFs/URLs, accused product spec, or specification for support mode. If **prior art is missing** for novelty/validity, suggest running **patent-search** first and pause until references exist or user accepts a gap analysis.

**Graceful degradation:** If only claim fragments exist, chart only what is provided and list **assumptions** explicitly in the summary JSON.

### Step 1: Identify Analysis Mode

| Mode | Purpose | Input |
|------|---------|-------|
| Novelty/Validity | Compare claims against prior art | Claims + prior art refs |
| Infringement | Compare claims against accused product | Claims + product docs |
| Support basis (KR) | Map claims to specification support | Claims + specification |
| Prosecution | Distinguish claims over cited art | Claims + examiner citations |

### Step 2: Deconstruct Claims

Parse each independent claim into discrete elements:

1. **Preamble**: The introductory clause establishing the context — **ALWAYS chart as row P**. Even when the preamble is non-limiting (US) or has minimal scope, it MUST appear as the first row in the chart. Omitting the preamble row is a **hard error**.
2. **Transitional phrase**: "comprising" (open) / "consisting of" (closed) /
   "consisting essentially of" (semi-closed)
3. **Body elements**: Each distinct limitation, numbered sequentially

For dependent claims, identify:
- Parent claim reference
- Additional limitations added
- Narrowing of parent claim elements

### Step 3: Build the Claim Chart

For each claim element, analyze the reference/product:

**US-Style Chart (novelty/infringement)**:

| # | Claim Element | Reference Disclosure | Assessment |
|---|---------------|---------------------|------------|
| P | [Preamble] | [Reference section/page] | Met / Not Met / Partially Met |
| 1 | [Element 1] | [Exact quote or description] | Met / Not Met / Partially Met |
| 2 | [Element 2] | [Exact quote or description] | Met / Not Met / Partially Met |

Assessment values:
- **Met**: Element clearly disclosed/present with citation — **MUST** include at least one of: page number, paragraph number (e.g., para. [0042]), figure reference (e.g., FIG. 3), or spec ¶ number. A bare "Met" without a specific locator is **invalid**.
- **Not Met**: Element absent — **MUST** state specifically what is missing in the reference/product (e.g., "Reference discloses X but lacks Y feature"). A bare "Not Met" or "absent" without a concrete gap description is **invalid**.
- **Partially Met**: Element partially disclosed — identify the gap with citation to what IS present and description of what is MISSING

**KR-Style Chart (support basis)**:

| # | 청구항 요소 | 명세서 근거 | 도면 참조 | 평가 |
|---|------------|-----------|----------|------|
| P | [전제부] | [단락 번호] | [도면 번호] | 충분 / 불충분 / 부분적 |
| 1 | [구성요소 1] | [단락 번호, 인용문] | [도면 번호, 부호] | 충분 / 불충분 / 부분적 |

For KR support basis charts, every claim element MUST map to:
- Specific specification paragraph numbers
- Drawing reference numerals where applicable
- Concrete implementation detail (not just abstract description)

### Step 4: Summarize Findings

Produce a summary table:

| Claim | Total Elements | Met | Not Met | Partial | Overall |
|-------|---------------|-----|---------|---------|---------|
| Claim 1 (Ind.) | N | X | Y | Z | Anticipated / Novel / Partially Novel |
| Claim 2 (Dep.) | N | X | Y | Z | ... |

For prosecution mode, highlight:
- Elements NOT found in any single reference (novelty arguments)
- Elements requiring combination of references (non-obviousness arguments)
- Motivation to combine analysis (or lack thereof)

### Step 5: Persist Results

Write to `outputs/patent-claim-chart/{date}/`:
- `claim-chart.md` — full claim chart in markdown table format
- `claim-chart-summary.json` — structured summary with element counts

## Anti-Patterns (Common Mistakes)

1. **DO NOT** mark **Met** without an **exact citation** (page, paragraph, figure number, or claim/spec paragraph for patent refs).
2. **DO NOT** skip **preamble analysis** — in KR practice preambles can be limiting; chart preamble row explicitly.
3. **DO NOT** chart **dependent** claims before **all independent** claims in the same family are complete for the chosen reference set. **Independent-First Gate:** Before starting ANY dependent claim chart, verify all independent claims are fully charted with all rows (P + body elements) populated. If any independent claim chart is incomplete, STOP and complete it first.
4. **DO NOT** mix **US-style** and **KR-style** chart formats in a single table — use one format per artifact section (separate sections if both are needed).

## Worked Example (Test Invention Context)

**Element:** “ordering execution of the plurality of sub-tasks according to a directed acyclic graph (DAG).”

**Hypothetical prior art:** US Patent Doc. X, FIGS. 2–3, para. [0042]–[0045].

| # | Claim Element | Reference Disclosure | Assessment |
|---|----------------|---------------------|------------|
| 3 | … wherein the processor orders execution of the plurality of sub-tasks according to a DAG | Doc. X, FIG. 3: tasks A→B→C with no back-edges; para. [0043]: “execution order follows dependency edges.” | Met — cite figure node IDs and paragraph |

**Not Met example:** If Doc. X only discloses linear pipelines without acyclic graph structure, state: **Not Met** — “Reference teaches sequential queues only; no directed acyclic graph or cycle prevention.”

## Pre-Delivery Check

Before delivering charts or files:

1. **Met citations** — every **Met** row has page/paragraph/figure (or spec ¶) citation, not a vague section name alone.
2. **Not Met** — every **Not Met** has a **specific gap** (what is missing in the reference/product).
3. **Independents** — chart covers **all independent** claims requested; dependents follow after independents per anti-pattern #3.
4. **Summary totals** — summary table Met/Not Met/Partial counts **match** the detailed chart rows. **Arithmetic Verification Procedure:** Count every row in the detailed chart by assessment value (Met / Not Met / Partially Met). Compare each count against the summary table. If ANY count differs, fix the summary table before delivery. This is a blocking check — do NOT deliver if counts mismatch.
5. **Preamble row** — every claim chart starts with row "P" for the preamble. If missing, add it.

If any check fails, correct before handoff.

## Output Artifacts

| Artifact | Path | Format |
|----------|------|--------|
| Full claim chart | `outputs/patent-claim-chart/{date}/claim-chart.md` | Markdown |
| Structured summary | `outputs/patent-claim-chart/{date}/claim-chart-summary.json` | JSON |

## Constraints

- Do NOT make legal conclusions about infringement or validity — present the
  element-by-element mapping for attorney review
- Always cite exact locations in prior art (page, paragraph, figure number)
- For KR support basis charts, every "불충분" finding must include a specific
  suggestion for what specification detail to add
- When an element is "Not Met", explicitly state what would need to be present

## Gotchas

- Preamble limitations: in US practice, preambles are not always limiting —
  note this when relevant; in KR practice, preambles carry more weight
- Transitional phrases: "comprising" (US: open-ended, allows additional
  elements) vs KR "포함하는" — similar but examine carefully
- Means-plus-function elements (US 35 USC 112(f)): must map to specification
  structure + equivalents, not just function
- Dependent claim analysis: if an independent claim is anticipated, dependent
  claims may still distinguish — always chart dependents too
- Multiple prior art combination: for 103/non-obviousness analysis, track which
  references cover which elements and identify the "gap" elements
