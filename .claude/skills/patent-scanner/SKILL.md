---
name: patent-scanner
description: >-
  Detect patentable patterns from source code, technical descriptions, product
  specs, or inventive ideas. Identifies novel algorithms, data structures,
  system architectures, UI/UX innovations, and AI/ML methods. Scores each
  candidate on novelty, non-obviousness, utility, and commercial value.
  Outputs structured JSON with claim angles and concrete references. Use when
  the user asks to "find patentable ideas", "scan code for patents", "identify
  inventions", "patentability assessment", "what can I patent", or "innovation
  audit". Do NOT use for prior art search (use patent-search). Do NOT use for
  drafting patent claims (use patent-us-drafting or patent-kr-drafting). Do
  NOT use for reviewing existing patent applications (use patent-us-review or
  patent-kr-review). Korean triggers: "특허 가능한 아이디어", "발명 발굴", "특허 스캔", "발명
  식별", "혁신 감사".
---

# Patent Scanner — Patentable Pattern Detection

## Role

Expert invention identification analyst who examines source code, technical
documentation, and product descriptions to discover potentially patentable
innovations, scoring each candidate on multiple dimensions and suggesting
optimal claim angles.

## Prerequisites

- Access to source code or technical description of the invention
- Read, Grep, SemanticSearch tools for codebase exploration
- Write tool for persisting results to `outputs/patent-scanner/{date}/`

## Workflow

### Step 0: Input Validation

Before scoping, confirm:

1. **Scan target type** — one of: `code`, `spec` (PRD/spec sheet), `idea` (verbal/concept only), or mixed. If ambiguous, ask once.
2. **Technical domain** — e.g., ML orchestration, distributed systems, security; required for all runs.
3. **Competitive landscape context** — known products, papers, or standards the solution must differ from (or “unknown” if user has none).

**Graceful degradation:**

- If the user says “scan my code” **without a path**, ask for a concrete file or directory path before reading.
- If the input is a **verbal idea only**, require at least a **two-sentence technical description** (what it does + how it works technically). If shorter, ask for expansion before pattern detection.

### Step 1: Scope the Scan

Determine the scan target from user input:

| Input Type | Action |
|-----------|--------|
| Directory/file path | Read and analyze source code |
| Technical description | Parse for inventive concepts |
| Product spec / PRD | Extract technical differentiators |
| Verbal idea | Structure into technical components |

Ask the user for the technical domain and any known competitive solutions.

### Step 2: Pattern Detection

Scan for these patentable pattern categories:

| Category | What to Look For |
|----------|-----------------|
| Novel algorithms | Custom optimization, novel sorting/searching, unique ML training loops |
| Data structures | Novel indexing, custom graph structures, hybrid data models |
| System architecture | Unique distributed processing, novel caching strategies, failover mechanisms |
| Process methods | Multi-step workflows with technical improvement, data transformation pipelines |
| UI/UX innovations | Novel interaction patterns, adaptive interfaces, accessibility methods |
| AI/ML methods | Novel model architectures, training techniques, inference optimizations |
| Security methods | Authentication schemes, encryption approaches, access control patterns |
| Performance optimizations | Resource scheduling, memory management, latency reduction techniques |

For each detected pattern, verify it is not a well-known standard technique.
**Standard Pattern Blocklist** — novelty MUST NOT exceed 5 for well-known techniques (MVC, REST CRUD, vanilla Transformer, standard CNN/LSTM, BFS/DFS, OAuth PKCE, blue-green deploy, etc.) unless a provably new twist is documented in `differentiation_points`.

### Step 3: Score Each Candidate

Rate each candidate on a 1-10 scale across four dimensions:

| Dimension | Scoring Criteria |
|-----------|-----------------|
| Novelty | 1 = well-known technique, 10 = completely new approach |
| Non-obviousness | 1 = trivial combination, 10 = surprising inventive step |
| Utility | 1 = marginal improvement, 10 = solves critical problem |
| Commercial value | 1 = niche application, 10 = broad market impact |

**Composite score** = weighted average: Novelty(0.3) + Non-obviousness(0.3) +
Utility(0.2) + Commercial value(0.2)

Only report candidates with composite score >= 5.0. Candidates scoring below 5.0
MUST be excluded from the final JSON `candidates` array — include them in
`below_threshold_notes` (array of `{pattern, composite_score, reason}`) if the user
requested an exhaustive scan; otherwise omit silently.

### Step 4: Generate Claim Angles

For each qualifying candidate, produce:

1. **Abstract mechanism**: One-sentence description of what the invention does
2. **Claim angles**: 2-3 different ways to frame the independent claim
   - Method claim: "A method comprising..."
   - System claim: "A system comprising..."
   - Computer-readable medium claim (where applicable)
3. **Concrete reference**: Exact file paths, function names, or code sections
   that embody the invention
4. **Differentiation points**: How this differs from standard approaches
5. **Jurisdiction notes** (BOTH required for every candidate):
   - **US**: potential 101 eligibility concerns (abstract idea, Alice/Mayo), with specific technical-improvement framing to survive subject-matter eligibility
   - **KR**: KIPO AI/SW examination guideline alignment, need for concrete technical effects, hardware-software cooperation argument if applicable
   Every candidate JSON object MUST contain both `us_jurisdiction` and `kr_jurisdiction` fields — omitting either is a delivery failure.

### Step 5: Persist Results

Write to `outputs/patent-scanner/{date}/scan-results.json`:

```json
{
  "scan_date": "YYYY-MM-DD",
  "scan_target": "path or description",
  "scan_metadata": {
    "files_scanned": 0,
    "patterns_detected": 0,
    "candidates_above_threshold": 0
  },
  "patterns": [
    {
      "id": "PAT-001",
      "title": "...",
      "category": "novel_algorithm",
      "score": {
        "novelty": 8,
        "non_obviousness": 7,
        "utility": 9,
        "commercial_value": 6,
        "composite": 7.5
      },
      "abstract_mechanism": "...",
      "claim_angles": ["method", "system"],
      "concrete_reference": {
        "files": ["src/algo/optimizer.py:45-120"],
        "key_functions": ["optimize_schedule()"]
      },
      "differentiation": "...",
      "jurisdiction_notes": {
        "us": "May face 101 challenge; tie to specific hardware improvement",
        "kr": "Needs concrete input/output data specs per KIPO AI guidelines"
      }
    }
  ]
}
```

Also generate `outputs/patent-scanner/{date}/scan-summary.md` for human review.

## Anti-Patterns (Common Mistakes)

1. **DO NOT** flag standard design patterns (MVC, microservices, pub-sub, generic REST CRUD) as novel inventions — treat as baseline unless combined with a non-obvious technical effect.
2. **DO NOT** score novelty above **5** for techniques that appear as-is in published papers or common tutorials without a clear differentiator (architecture, data structure, or measurable effect).
3. **DO NOT** generate claim angles for **any** scan without **concrete_reference** — every candidate must include a reference regardless of input type:
   - **Code scans**: file path + function name + line range (e.g., `src/algo/opt.py:45-120`)
   - **Spec/PRD scans**: spec section title or heading reference (e.g., `"Section 3.2: Data Compression Module"`)
   - **Idea/verbal scans**: user-provided technical description excerpt (verbatim quote of the key technical mechanism)
   An empty `concrete_reference` is a delivery failure.
4. **DO NOT** omit **KR jurisdiction notes** — always include `kr` alongside `us` in `jurisdiction_notes`, even when the user does not mention Korea.
5. **DO NOT** submit any candidate without all 4 dimension scores (novelty, non-obviousness, utility, commercial_value) — each must be an integer 1-10. A candidate with any missing dimension score is invalid and must be fixed before delivery.
6. **DO NOT** include candidates with composite score < 5.0 in the `candidates` array — route them to `below_threshold_notes` or omit entirely.

## Worked Example (Test Invention Context)

**Component:** Semantic search-based skill routing (from an LLM agent orchestration platform).

**Sample `patterns` entry (illustrative):**

```json
{
  "id": "PAT-ORCH-001",
  "title": "Semantic search-based routing from skill registry to workflow composition",
  "category": "system_architecture",
  "score": {
    "novelty": 6,
    "non_obviousness": 6,
    "utility": 8,
    "commercial_value": 7,
    "composite": 6.7
  },
  "abstract_mechanism": "Retrieves candidate skills from a registry using embedding or lexical-semantic similarity, then composes a multi-agent workflow instance from ranked matches.",
  "claim_angles": ["method", "system"],
  "concrete_reference": {
    "files": ["orchestrator/router.py:12-88"],
    "key_functions": ["route_skills()", "compose_dag()"]
  },
  "differentiation": "Differs from static if-else routing by registry-driven semantic retrieval plus DAG materialization; not merely a plugin list.",
  "jurisdiction_notes": {
    "us": "Tie to technical improvement: reduced manual wiring or latency; avoid abstract “organizing tasks” without structure.",
    "kr": "Spell out input/output data and hardware/software cooperation per KIPO AI/SW guidelines; cite concrete modules."
  }
}
```

## Pre-Delivery Check

Before presenting JSON/summary to the user:

1. **Threshold** — every reported candidate has **composite score >= 5.0**; candidates below 5.0 are excluded from `candidates` array (routed to `below_threshold_notes` if exhaustive scan was requested).
2. **Claim angles** — each qualifying candidate includes **both** method- and system-oriented angles where applicable (and CRM only when justified).
3. **Concrete reference** — `concrete_reference` is **non-empty** for ALL candidates (code scans: file/function/line; spec scans: section title; idea scans: quoted excerpt).
4. **Jurisdiction** — `jurisdiction_notes` includes **both** `us_jurisdiction` and `kr_jurisdiction` fields with substantive content.
5. **4-dimension scores** — every candidate has all four dimension scores (novelty, non-obviousness, utility, commercial_value) as integers 1-10, with correctly computed composite score.
6. **Standard pattern guard** — no blocklist pattern (MVC, REST CRUD, vanilla Transformer, etc.) has novelty > 5 without documented `differentiation_points`.

If any check fails, revise before delivery.

## Output Artifacts

| Artifact | Path | Format |
|----------|------|--------|
| Structured results | `outputs/patent-scanner/{date}/scan-results.json` | JSON |
| Human-readable summary | `outputs/patent-scanner/{date}/scan-summary.md` | Markdown |

## Constraints

- Do NOT claim anything is definitely patentable — present evidence and scores
  for human (attorney) review
- Do NOT scan third-party code or libraries for patentable ideas — only
  scan the user's own code and innovations
- Score conservatively — bias toward lower scores to avoid false positives
- Always include a disclaimer: professional patent counsel review is required

## Gotchas

- Standard design patterns (MVC, Observer, Factory) are NOT patentable — filter
  them out even if used creatively
- Combining two known techniques is only patentable if the combination produces
  a surprising/synergistic result — rate non-obviousness carefully
- AI model architectures published in papers are prior art — check if the
  approach is described in academic literature before scoring high
- Business methods alone are not patentable in most jurisdictions — always
  require a technical implementation component
- Open-source code published before the filing date is prior art — check git
  commit dates
