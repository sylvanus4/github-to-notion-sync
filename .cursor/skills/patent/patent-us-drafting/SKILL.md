---
name: patent-us-drafting
description: >-
  Draft US patent application documents: independent/dependent claims (method,
  system, CRM), detailed specification, abstract, and title. Uses broad-first
  claim drafting style with functional language, means-plus-function
  alternatives, and Alice/Mayo-compliant technical improvement framing. Outputs
  filing-ready markdown documents. Integrates with patent-diagrams for figure
  references and patent-search for prior art differentiation. Use when the user
  asks to "draft US patent claims", "write a patent application", "US patent
  draft", "claim drafting", "specification drafting", or "write claims". Do NOT
  use for Korean patent drafting (use patent-kr-drafting). Do NOT use for
  reviewing existing applications (use patent-us-review). Do NOT use for office
  action responses (use patent-us-oa-response). Korean triggers: "미국 특허
  출원", "미국 청구항 작성", "US 특허 초안".
metadata:
  version: "1.1.0"
  category: "drafting"
  author: "thaki"
---

# US Patent Drafting — Claims & Specification

## Role

Expert US patent drafter who produces prosecution-ready patent application
documents following USPTO practice, emphasizing broad independent claims with
strategic dependent claim narrowing, Alice/Mayo-compliant framing, and
specification detail sufficient to support claim scope under 35 USC 112.

## Prerequisites

- Invention description (from patent-scanner output or user input)
- Prior art search results (from patent-search, optional but recommended)
- Patent diagrams (from patent-diagrams, optional)
- Write tool for persisting output to `outputs/patent-us/{date}/`

## Workflow

### Step 0: Input Validation

Before Step 1, confirm the following inputs are present and usable:

1. **Invention description**: Minimum **100 words** of technical disclosure, **or** structured output from `patent-scanner` (if provided, extract problem, solution, and novelty directly from that output rather than asking the user to repeat it).
2. **Prior art differentiation points**: Explicit bullets or narrative explaining how the invention differs from known solutions (may reference `patent-search` results).
3. **AI/SW invention flag**: Whether the invention is primarily software/AI-driven (if yes, **Alice/Mayo** analysis is mandatory in later steps).

**If the invention description is too vague** (missing concrete technical effect, data flows, or structure): stop and ask the user for specifics on **(a)** the technical problem, **(b)** the technical solution, and **(c)** how the solution differs from prior art. Do not draft claims until these are answerable from the input.

**If `patent-scanner` output is provided**: treat it as authoritative for invention disclosure; pull claim candidates, elements, and differentiators from it before expanding prose.

### Step 1: Invention Analysis

From the input, extract:
1. Core technical problem being solved
2. Technical solution and its novel aspects
3. Key differentiators over prior art
4. Commercial embodiments and variations
5. Whether the invention touches abstract ideas (triggers Alice analysis)

### Step 2: Claim Strategy

Design the claim tree:

**Independent Claims** (MANDATORY minimum 3 categories — drafts missing any of these three MUST be revised before delivery):
- Claim 1: **Method** claim — "A method comprising..."
- Claim N: **System** claim — "A system comprising: a processor; a memory
  storing instructions that, when executed by the processor, cause the
  processor to..."
- Claim M: **Non-transitory computer-readable medium (CRM)** claim — "A non-transitory
  computer-readable medium storing instructions..."

If the invention is purely hardware with no software component, replace CRM with an **apparatus** claim and document the substitution rationale.

**Broadest claim first**: Start with the minimum elements needed to distinguish
over the prior art. Each word constrains scope — remove anything not essential.

**Dependent claims**: Add narrowing limitations progressively:
- Preferred embodiment details
- Specific parameter ranges or thresholds
- Alternative implementations
- Performance characteristics
- Integration with other components

Aim for 15-20 total claims (standard USPTO filing).

### Step 3: Draft Independent Claims

For each independent claim, follow this structure:

```
1. A method [for/of achieving X], comprising:
   [step A]ing [first action with broad functional language];
   [step B]ing [second action], wherein [key technical constraint];
   [step C]ing [third action] based on [result of step B]; and
   [step D]ing [output/result action].
```

**Language rules**:
- Use "comprising" (open-ended) unless closed claim is strategically needed
- Gerund form for method steps: "receiving", "determining", "generating"
- Avoid unnecessary specificity: "a computing device" not "a server running
  Linux"
- Include "wherein" clauses for essential technical relationships
- For AI/software: tie abstract concepts to technical improvements
  (speed, accuracy, resource usage, specific technical effect)

**Alice/Mayo compliance** (35 USC 101):
- Frame the invention as a technical improvement, NOT a business method
- Include at least one step tied to specific hardware/technical operation
- Emphasize concrete technical effect: "thereby reducing computational
  complexity from O(n²) to O(n log n)" or "improving prediction accuracy
  by at least X%"
- Avoid pure data manipulation — connect to real-world technical outcome

### Anti-Patterns (Independent Claims & Specification)

1. **DO NOT** draft claims using implementation-specific language — use technology-neutral terms. **Blocklist** (non-exhaustive): Python, Java, JavaScript, TypeScript, Go, Rust, C++, PostgreSQL, MySQL, MongoDB, Redis, Docker, Kubernetes, AWS, Azure, GCP, React, TensorFlow, PyTorch, Linux, Windows, macOS, REST, GraphQL, gRPC. Replace with functional equivalents (e.g., "a processor", "a data store", "a containerized execution environment", "a cloud computing platform"). Run a final text scan of all claims against this blocklist before delivery.
2. **DO NOT** write more than **five** substantive limitations/steps in a single independent claim — overly complex independent claims invite **35 USC 112** clarity/enablement rejections; split into dependents instead. After drafting each independent claim, count the substantive steps/elements; if > 5, factor the excess into dependent claims.
3. **DO NOT** use "means for …" language unless **112(f)** interpretation is intentional and tied to corresponding structure in the specification.
4. **DO NOT** draft **CRM** (computer-readable medium) claims without the **"non-transitory"** qualifier.
5. **DO NOT** write specification paragraphs that **merely repeat** claim language — each claim element needs **concrete implementation detail**, examples, and alternatives in the detailed description.
6. **DO NOT** skip the **Alice self-check** (Step 6) even when the invention appears hardware-heavy — software-adjacent elements may still trigger abstract-idea analysis.

### Worked Example: LLM Agent Orchestration Platform

**Test invention context**: An LLM agent orchestration platform that dynamically composes multi-agent workflows from a skill registry using semantic-search-based routing, DAG-based execution ordering, and resource-aware model selection.

**Example independent method claim** (illustrative breadth; narrow with real prior art):

```
1. A computer-implemented method for orchestrating multi-agent workflows, comprising:
   receiving, by a processor, a task description specifying a computational objective;
   performing a semantic search over a skill registry to identify a set of candidate agent skills based on embedding similarity between the task description and skill metadata;
   constructing a directed acyclic graph representing an execution order for the identified candidate agent skills based on inter-skill dependency relationships;
   selecting, for each node in the directed acyclic graph, a language model tier from a plurality of available tiers based on a complexity signal derived from the task description; and
   executing the directed acyclic graph by dispatching each agent skill to the selected language model tier, wherein execution results are persisted at checkpoint nodes to enable failure recovery.
```

Use this as a structural template only — align terminology with the final specification and claim chart.

### Step 4: Draft Dependent Claims

Build a claim tree:

```
Claim 1 (Independent - Method)
├── Claim 2: [specific algorithm or technique]
├── Claim 3: [data type or format constraint]
├── Claim 4: [threshold or parameter range]
│   └── Claim 5: [further narrowing of Claim 4]
├── Claim 6: [integration with external system]
└── Claim 7: [error handling or fallback]

Claim 8 (Independent - System)
├── Claim 9: [hardware specification]
├── Claim 10: [mirrors Claim 2 in system form]
...
```

### Step 5: Draft Specification

Structure the specification:

1. **Title**: Concise, descriptive (no marketing language)
2. **Cross-Reference to Related Applications**: Placeholder for priority claims
3. **Field of the Invention**: One paragraph, broad technology area
4. **Background of the Invention**: 2-3 paragraphs identifying the technical
   problem WITHOUT disparaging prior art
5. **Summary of the Invention**: Brief overview of the solution; may mirror
   broadest claim language
6. **Brief Description of the Drawings**: One line per figure referencing
   patent-diagrams output
7. **Detailed Description of Preferred Embodiments**:
   - Walk through each figure with reference numerals
   - Describe every claim element with at least one concrete example
   - Include alternative embodiments for key elements
   - Use "In some embodiments..." and "In another embodiment..." phrasing
   - Describe any algorithm or process with sufficient detail for a PHOSITA
     to reproduce
8. **Abstract**: ≤ 150 words summarizing the technical disclosure. Count the words in the abstract before finalizing `draft-abstract.md`; if over 150, compress by removing dependent-claim-level detail

**Critical**: The specification MUST support every claim limitation. For each
claim element, verify at least one paragraph in the detailed description
explains it with concrete specificity.

**MANDATORY — Claim-to-Specification Traceability Table**: After completing the detailed description, produce a table mapping every claim limitation to its supporting specification paragraph. This table must be included in `draft-specification.md` as an appendix:

| Claim # | Limitation | Spec ¶ # | Summary of Support |
|---------|-----------|---------|-------------------|
| 1 | step A: receiving a task description | ¶ 0032 | Describes task input parsing |
| 1 | step B: performing semantic search | ¶ 0035-0037 | Embedding similarity algorithm |

If any limitation lacks a specification paragraph, STOP and add the missing description before finalizing.

### Step 6: Alice/Mayo Self-Check

Before finalizing, verify each independent claim passes the two-step Alice
framework:

| Step | Question | Required Answer |
|------|----------|----------------|
| Step 1 | Is the claim directed to an abstract idea? | If yes, proceed to Step 2 |
| Step 2A-Prong 1 | Does it recite a judicial exception? | Identify the exception |
| Step 2A-Prong 2 | Is the exception integrated into a practical application? | Must be YES |
| Step 2B | Does it recite significantly more? | Should be YES (safety net) |

If any claim fails, restructure to emphasize the technical improvement.

**MANDATORY — Persist as `alice-check.md`**: The Alice/Mayo analysis MUST be written to `outputs/patent-us/{date}/alice-check.md` as a separate artifact. Do NOT embed it only in `draft-specification.md`. The file must contain the full table above completed for every independent claim, with a PASS/FAIL verdict and remediation notes for any failures.

### Step 7: Persist Output

Write to `outputs/patent-us/{date}/`:
- `draft-claims.md` — all claims in standard format
- `draft-specification.md` — full specification
- `draft-abstract.md` — abstract
- `claim-tree.md` — visual claim dependency tree
- `alice-check.md` — Alice/Mayo compliance analysis

### Step 8: Pre-Delivery Check

After Step 7 (persist output), perform this **pre-delivery self-verification** before handing off to the user or counsel:

| # | Check | Requirement |
|---|--------|----------------|
| (a) | Independent claim set | At least **three** independent claims present: **method**, **system**, and **CRM** (non-transitory). |
| (b) | Specification support | Every claim element has **explicit support** in the specification — cite the supporting **paragraph number** (or ¶ ID) next to each element in a traceability table or inline notes. |
| (c) | Alice self-check | Step 6 (Alice/Mayo) completed for **every** independent claim; failures resolved or documented. |
| (d) | Claim count | Total claims **15–20** (adjust dependents to hit band unless user specifies otherwise). |
| (e) | Terminology | Consistent terms for the same components across claims and specification (glossary alignment). |
| (f) | Abstract length | Abstract **≤ 150 words**. |

If any check fails, revise the draft and re-run this checklist.

## Output Artifacts

| Artifact | Path | Format |
|----------|------|--------|
| Claims | `outputs/patent-us/{date}/draft-claims.md` | Markdown |
| Specification | `outputs/patent-us/{date}/draft-specification.md` | Markdown |
| Abstract | `outputs/patent-us/{date}/draft-abstract.md` | Markdown |
| Claim tree | `outputs/patent-us/{date}/claim-tree.md` | Markdown |
| Alice check | `outputs/patent-us/{date}/alice-check.md` | Markdown |

## Constraints

- AI-generated drafts require attorney review before filing — include
  a disclaimer
- No attorney-client privilege is created by using this tool
- Aim for broadest defensible scope — not broadest imaginable scope
- Every claim term must find explicit support in the specification
- Use consistent terminology — same component = same term throughout

## Gotchas

- "Comprising" vs "consisting of": default to "comprising" unless the
  invention requires a closed set
- Means-plus-function (112(f)): avoid unless intentional — triggers narrow
  construction limited to specification embodiments + equivalents
- Functional claim language must be tied to structure for 112(f) avoidance:
  "a processor configured to" is better than "means for processing"
- Provisional applications: can be less formal but still need full disclosure
  to establish priority date for all claimed subject matter
- CRM claims: always specify "non-transitory" to avoid rejection under
  In re Nuijten
- Specification must enable the FULL scope of claims, not just one embodiment
