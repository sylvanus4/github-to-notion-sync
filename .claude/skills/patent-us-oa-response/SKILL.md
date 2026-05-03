---
name: patent-us-oa-response
description: >-
  Draft responses to USPTO office actions: analyze rejections
  (101/102/103/112), generate claim amendments with markup, draft traversal
  arguments with case law citations, suggest interview strategies, and produce
  response packages. Handles non-final and final office actions, restriction
  requirements, and election of species. Use when the user asks to "respond to
  office action", "answer rejection", "OA response", "amend claims", "traverse
  103 rejection", or "office action strategy". Do NOT use for Korean OA
  responses (use patent-kr-oa-response). Do NOT use for pre-filing review (use
  patent-us-review). Do NOT use for initial drafting (use patent-us-drafting).
  Korean triggers: "미국 거절이유 대응", "OA 답변", "의견서 작성 (미국)", "거절 극복", "보정안 (미국)".
---

# US Office Action Response — Rejection Traversal & Amendments

## Role

Expert US patent prosecutor who analyzes USPTO office action rejections,
crafts claim amendments with proper markup, and drafts persuasive traversal
arguments supported by case law, all aimed at overcoming rejections while
preserving maximum claim scope.

## Prerequisites

- Office action document (uploaded or pasted)
- Current claims and specification
- Prior art references cited by the examiner
- Write tool for persisting output to `outputs/patent-us-oa/{date}/`

## Workflow

### Step 0: Input Validation

Do not begin drafting amendments or remarks until inputs are verified.

| Requirement | Rule |
|-------------|------|
| **(a) Office action document** | Full text of the OA (or complete upload). **If the OA is not provided, STOP** — do not fabricate rejections. |
| **(b) Current claims and specification** | Current claim text **and** specification needed to support amendments. **If claims are missing, do not draft amendments** — request claims first. |
| **(c) Response deadline** | Confirm the **response deadline** (statutory date and any extension strategy). **If the deadline is within 1 month, flag URGENCY** prominently in the output header and summary. |

### Step 1: Office Action Analysis

Parse the office action to extract:

| Section | Extract |
|---------|---------|
| OA type | Non-Final / Final / Advisory / Restriction |
| Response deadline | Statutory (3/6 months) + extensions |
| Rejections | Per-claim: statute, grounds, cited art |
| Objections | Formality issues (drawings, abstract, spec) |
| Examiner notes | Reasons for allowance (if any claims allowed) |

Build a rejection matrix:

| Claim | Rejection Type | Statute | Cited Art | Key Issue |
|-------|---------------|---------|-----------|-----------|
| 1 | Anticipation | 102(a)(1) | Smith (US 10,xxx) | [element overlap] |
| 1 | Obviousness | 103 | Smith + Jones | [combination] |
| 1 | Eligibility | 101 | Alice | [abstract idea] |
| 3 | Indefiniteness | 112(b) | — | [unclear term] |

### Step 2: Response Strategy

For each rejection, determine the strategy:

**101 Rejection Strategy Options**:
- Amend to strengthen practical application integration
- Argue technical improvement under Prong 2
- Add hardware/specific technical elements
- Cite analogous favorable decisions

**102 Rejection Strategy Options**:
- Distinguish over cited reference (element-by-element)
- Argue cited reference teaches away
- Challenge reference qualification (date, public availability)
- Amend to add distinguishing limitations

**103 Rejection Strategy Options**:
- Attack motivation to combine
- Argue teaching away in one or more references
- Present secondary considerations (commercial success, long-felt need)
- Amend to add differentiating dependent claim features
- Challenge number of references needed (>3 = weak case)

**112 Rejection Strategy Options**:
- Amend claim language for clarity
- Point to specification support
- Add definitions to specification (if non-final)
- Argue that PHOSITA would understand term

### Step 3: Draft Claim Amendments

Use standard patent amendment markup:

```
1. (Currently Amended) A method [for/of achieving X], comprising:
   [step A]ing [first action];
   [step B]ing [second action], [[wherein [new limitation added
   to distinguish over Smith]--]]; and
   [step C]ing [third action] [[based on [new element]--]].
```

Notation:
- `[[text--]]` = added text (double brackets with dash-dash)
- `[[--deleted text--]]` = deleted text (strikethrough equivalent)
- Underline new matter, strikethrough removed matter

<!-- M1: 보정 마크업 일관성 게이트 -->
**Markup Consistency Gate:** All claims in the response package MUST use the **identical** markup convention above. Before proceeding to Step 4, scan every amended claim and confirm: (a) additions use `[[...--]]` only, (b) deletions use `[[--...--]]` only, (c) no mixed or ad-hoc markup styles appear. If inconsistency is found, fix before continuing.

Rules:
- Every amendment must find support in the original specification
<!-- M2: 명세 단락 인용 완전성 게이트 -->
- Cite the specification paragraph supporting each added limitation — **every** `[[...--]]` addition MUST be immediately followed by a parenthetical spec citation `(Support: ¶[xxxx])`. An amendment line lacking a spec citation is incomplete and must not be included in the final package.
- Minimize scope reduction — add only what is necessary to overcome
- Preserve independent claim breadth; narrow via dependent claims first

### Step 4: Draft Arguments (Remarks)

Structure the Remarks section:

**I. Status of the Claims**
- List of amendments: claims amended, added, canceled
- Claims pending after amendment

**II. Claim Rejections Under 35 USC [section]**

For each rejection ground:

**A. Summary of the Rejection**
- Brief, accurate restatement of the examiner's position

**B. Response**
- Element-by-element traversal showing where cited art fails to teach/suggest
- For 103: attack motivation to combine, show teaching away, or present
  secondary considerations
- For 101: emphasize technical improvement, cite favorable decisions
- For 112: point to specification support or amend for clarity

<!-- M3: 거절별 차별화된 논증 필수 게이트 -->
**Differentiation Gate:** Each rejection ground (101, 102, 103, 112) MUST receive a **unique primary argument** tailored to that specific ground. Cross-check before finalizing: if two rejections share the same core argument verbatim, rewrite one with a distinct traversal angle. Copy-pasting the same argument across different rejections is prohibited.

<!-- M4: 103 결합 동기 논증 필수 게이트 -->
**103 Motivation-to-Combine Gate:** For **every** 103 rejection, the Remarks section MUST include a dedicated subsection titled "No Motivation to Combine" that: (a) identifies the specific teaching the Examiner relies on for combination, (b) argues why a PHOSITA would NOT have combined the references (e.g., teaching away, different problem solved, incompatible architectures), and (c) cites at least one supporting case (e.g., KSR, Kahn, Cheese v. Molinaro). Omitting this subsection for any 103 rejection is a blocking deficiency.

**C. Conclusion**
- Respectfully request withdrawal of the rejection

**III. Interview Request** (if applicable)
- Propose interview topics
- Suggest claim amendments for discussion

### Step 5: Case Law Citations

Include relevant case law to support arguments:

| Issue | Favorable Cases |
|-------|----------------|
| 101 - Technical improvement | Enfish, DDR Holdings, Core Wireless |
| 101 - Specific implementation | Bascom, Berkheimer |
| 103 - No motivation to combine | KSR (limits), Unigene |
| 103 - Teaching away | In re Gurley |
| 103 - Secondary considerations | Graham v. John Deere |
| 112(a) - Written description | Ariad v. Eli Lilly |
| 112(b) - Definiteness | Nautilus v. Biosig |

### Step 6: Final OA Considerations

If responding to a FINAL office action:
- Consider After Final Consideration Pilot (AFCP 2.0)
- Consider Request for Continued Examination (RCE)
- Consider appeal to PTAB
- Consider interview before filing response
- Note: amendments in response to final OA are limited to those placing
  the application in condition for allowance

### Step 7: Response Package

Assemble the complete response:

1. Transmittal letter
2. Claim amendments (marked up)
3. Remarks/Arguments
4. Clean claim set (after amendments)
5. Declaration/affidavit (if submitting 103 evidence)

### Step 8: Persist Output

Write to `outputs/patent-us-oa/{date}/`:
- `oa-analysis.md` — rejection matrix and strategy
- `amended-claims.md` — claims with amendment markup
- `remarks.md` — full arguments/remarks section
- `clean-claims.md` — clean claim set after amendments
- `response-summary.json` — structured summary

## Anti-Patterns (DO NOT)

1. **DO NOT** argue every rejection point exhaustively — identify the **2–3 strongest** lines of attack and **focus** remarks on those (plus any claim amendments that must be defended).
2. **DO NOT** amend claims without citing the **specific specification paragraph(s)** that support each added limitation.
3. **DO NOT** use amendment markup inconsistently — **additions:** bracket inserted text per one convention (e.g. `[[added--]]` … or `[[...new language...--]]` as in the worked example); **deletions:** `[[--deleted--]]` for removed text; use the **same** style for all claims in the package.
4. **DO NOT** draft arguments that **merely disagree** with the examiner — tie traversal to **record evidence** (spec, declaration, affidavit, or undisputed claim construction).
5. **DO NOT** suggest an examiner interview without **specific topics** (e.g., claim 1 vs. Smith reference, motivation to combine A+B, 112(b) term scope).

## Worked Example: Claim Amendment Entry (Test Invention)

**Context:** LLM Agent Orchestration Platform — DAG execution and resource-aware model tier selection.

**Example amendment line:**

> **Claim 1 (Currently Amended):** … selecting, for each node in the directed acyclic graph, a language model tier from a plurality of available tiers [[based on a complexity signal derived from an analysis of input token count, required reasoning depth, and historical execution latency for similar tasks--]]; **(Support: Specification ¶[0052]–[0054])**

(Replace paragraph numbers with the actual supporting paragraphs of the application.)

### Step 9: Pre-Delivery Check

Before delivering the response package, confirm **all** of the following:

1. **Per-rejection strategy:** Every rejection in the OA has a **named response strategy** (amend + argue, argue only, interview first, etc.) in `oa-analysis.md` or the summary.
2. **Spec support for amendments:** Every amended limitation cites **at least one specification paragraph** (or states clearly if support is being added via declaration with basis in spec).
3. **Clean claim consistency:** `clean-claims.md` matches the **final** amended claim text and is **internally consistent** (dependencies, antecedent basis, numbering).

<!-- M5: clean-claims.md 일치 검증 게이트 -->
   **Clean-Claims Verification Gate:** After generating `clean-claims.md`, perform a **line-by-line comparison** against `amended-claims.md` (with all markup stripped). Every claim in `clean-claims.md` must exactly reproduce the final intended claim language — no markup residue (`[[`, `--]]`), no stale pre-amendment text, and no missing claims. If any discrepancy is found, regenerate `clean-claims.md` before delivering the package.
4. **Deadline:** Response **deadline** is **prominently noted** in the transmittal/summary (and **URGENCY** if the deadline is less than one month away).
5. **Case law:** Cited cases are **correctly named**, **on point** for the statute argued, and not overstated beyond their holdings.

## Output Artifacts

| Artifact | Path | Format |
|----------|------|--------|
| OA analysis | `outputs/patent-us-oa/{date}/oa-analysis.md` | Markdown |
| Amended claims | `outputs/patent-us-oa/{date}/amended-claims.md` | Markdown |
| Remarks | `outputs/patent-us-oa/{date}/remarks.md` | Markdown |
| Clean claims | `outputs/patent-us-oa/{date}/clean-claims.md` | Markdown |
| Summary | `outputs/patent-us-oa/{date}/response-summary.json` | JSON |

## Constraints

- AI-generated OA responses require attorney review before filing
- Amendments must find support in original specification — cite paragraphs
- Do not introduce new matter through amendments
- Response deadlines are strict — always note the deadline prominently
- Case law citations should be checked for current validity

## Gotchas

- Final OA amendments are severely limited — consider RCE or appeal early
- AFCP 2.0 provides additional examiner time for after-final amendments
- Examiner interviews can resolve issues faster than written arguments
- 103 arguments must address motivation to combine, not just individual
  reference deficiencies
- Adding claims via amendment has fee implications
- Restriction requirements and election of species affect which claims
  can be pursued in the current application vs. divisionals
