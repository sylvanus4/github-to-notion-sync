---
name: patent-pipeline
description: >-
  End-to-end patent filing package pipeline: prior art search → patentability
  scan → technical drawings → claim drafting → specification → review → quality
  gate → output packaging. Orchestrates 6-8 patent skills sequentially with
  intermediate file persistence at each phase. Supports US-only, KR-only, or
  dual-jurisdiction modes. Use when the user asks to "run full patent pipeline",
  "end-to-end patent", "complete filing package", "특허 출원 전체 프로세스",
  "전체 파이프라인", "filing-ready package", or wants automated patent
  application generation from idea to filing documents. Do NOT use for
  individual patent tasks (use the specific patent-* skill). Do NOT use for
  OA response workflows (use patent-us-oa-response or patent-kr-oa-response).
  Korean triggers: "특허 전체 파이프라인", "출원 패키지", "전체 프로세스",
  "파이프라인 실행".
metadata:
  version: "1.0.0"
  category: "pipeline"
  author: "thaki"
---

# Patent Filing Pipeline — End-to-End Package Generation

## Role

Master pipeline orchestrator that chains patent skills into a complete filing
package workflow, persisting intermediate results at each phase for resumability,
auditability, and human review gates.

## Prerequisites

- Invention description (technical document, code, or natural language)
- Target jurisdiction(s): US, KR, or both
- Write tool for persisting all intermediate and final outputs

## Phase 0: Pre-Flight

Before starting Phase 1, run these checks:

(a) **Invention description**: Must exist and be **substantive** (more than **100 words** of technical content, or equivalent structured detail). If too thin, ask the user to expand embodiments, architecture, and differentiation before Discovery.

(b) **Target jurisdiction(s)**: Confirm **US**, **KR**, or **both** explicitly.

(c) **Existing search results**: If **recent** `patent-search` outputs exist for the same invention (e.g. under `_workspace/patent-pipeline/{date}/` or user-provided paths), **skip Phase 1.1** or merge into a delta search per user instruction.

(d) **Existing diagrams**: If **recent** `patent-diagrams` outputs exist for the same invention, **skip Phase 2.1** or run an update pass only.

(e) **Resume**: If `_workspace/patent-pipeline/{date}/` contains artifacts from a **prior run**, detect the **last completed phase** from persisted files and **offer** to resume from the next phase instead of restarting from Phase 1.

## Pipeline Architecture

```
Phase 1: Discovery
  ├── patent-search (prior art)
  └── patent-scanner (patentability assessment)
       └── GATE: patentability score >= 6/10 to proceed

Phase 2: Preparation
  ├── patent-diagrams (technical drawings)
  └── patent-claim-chart (if prior art found — differentiation map)

Phase 3: Drafting (jurisdiction-dependent)
  ├── US: patent-us-drafting
  └── KR: patent-kr-drafting

Phase 4: Review (jurisdiction-dependent)
  ├── US: patent-us-review
  ├── KR: patent-kr-review
  └── KR+AI: patent-kr-ai-invention (if AI/SW invention)
       └── GATE: no CRITICAL issues remaining

Phase 5: Revision
  └── Apply review fixes → re-draft → re-review (max 2 iterations)

Phase 6: Packaging
  └── Assemble filing-ready document set
```

## Workflow

### Anti-Patterns (Patent Pipeline)

1. **DO NOT** proceed past **Quality Gate 1** if patentability score **< 6/10** without **explicit user approval** to continue.
2. **DO NOT** skip **intermediate file persistence** — every phase must write to `_workspace/patent-pipeline/{date}/` before the next phase consumes inputs.
3. **DO NOT** run **more than 2 revision iterations** in Phase 5 — escalate remaining issues to **human review**.
4. **DO NOT** skip **`patent-kr-ai-invention`** for any **KR** filing of **software/AI** inventions when that skill applies.
5. **DO NOT** generate the **final package** (Phase 6) without completing **all** preceding phases for the selected jurisdiction(s).
6. **DO NOT** mix **`_workspace/`** (working state) with **`outputs/`** (final deliverables) — keep paths and purpose distinct in documentation and on disk.

### Worked Example: Phase 1 Output (LLM Orchestration Platform)

Illustrative Discovery summary for an invention such as: *LLM Agent Orchestration Platform with semantic skill routing, DAG execution ordering, and resource-aware model selection.*

- **Phase 1.1 Search:** 23 results across 6 databases (US: 8, KR: 5, WO: 4, EP: 3, Academic: 3); **2 blocking references** identified (relevance 8+); **key gap:** no prior art shown combining **semantic routing + DAG execution + model tier selection** in a **single orchestration framework** as claimed.
- **Phase 1.2 Scan:** Composite score **8.2/10**; top candidates: (1) Semantic skill routing **PAT-001:** 8.5, (2) DAG executor with checkpoints **PAT-002:** 7.8, (3) Model tier selector **PAT-003:** 7.2.
- **Quality Gate 1:** **PASS** (8.2 >= 6.0) → proceed to Phase 2.

### Phase 1: Discovery

**Step 1.1: Prior Art Search**

Invoke `patent-search` with the invention description.
- Persist results to `_workspace/patent-pipeline/{date}/phase1-search.md`
- Extract: top 5 closest references, novelty gaps

**Step 1.2: Patentability Scan**

Invoke `patent-scanner` with the invention and search results.
- Persist results to `_workspace/patent-pipeline/{date}/phase1-scan.json`
- Extract: patentability score, claim angles, risk assessment

**Quality Gate 1**: If patentability score < 6/10, STOP and report:
- "Patentability score is X/10. Proceeding is not recommended."
- Provide specific reasons and suggest pivots
- Ask user whether to proceed anyway

### Phase 2: Preparation

**Step 2.1: Technical Drawings**

Invoke `patent-diagrams` with the invention description and scan results.
- Persist to `_workspace/patent-pipeline/{date}/phase2-diagrams.md`
- Generate: system diagram, flowcharts, data flow diagrams

**Step 2.2: Claim Chart** (conditional)

If prior art references were found, invoke `patent-claim-chart`:
- Map invention elements against top 3 prior art references
- Persist to `_workspace/patent-pipeline/{date}/phase2-chart.md`
- Purpose: inform drafting by highlighting differentiating features

### Phase 3: Drafting

**US Track** (if US jurisdiction selected):

Invoke `patent-us-drafting` with:
- Invention description
- Prior art analysis from Phase 1
- Drawings from Phase 2
- Claim chart differentiation points
- Persist to `_workspace/patent-pipeline/{date}/phase3-us-draft/`

**KR Track** (if KR jurisdiction selected):

Invoke `patent-kr-drafting` with same inputs.
- Persist to `_workspace/patent-pipeline/{date}/phase3-kr-draft/`

### Phase 4: Review

**US Track**:

Invoke `patent-us-review` on the US draft.
- Persist to `_workspace/patent-pipeline/{date}/phase4-us-review/`

**KR Track**:

Invoke `patent-kr-review` on the KR draft.
- Persist to `_workspace/patent-pipeline/{date}/phase4-kr-review/`

If AI/SW invention, also invoke `patent-kr-ai-invention`:
- Persist to `_workspace/patent-pipeline/{date}/phase4-kr-ai/`

**Quality Gate 2**: If CRITICAL issues found:
- List all critical issues
- Do NOT proceed to packaging until resolved

### Phase 5: Revision (Evaluator-Optimizer Loop)

For each CRITICAL/HIGH issue from review:
1. Apply the suggested fix to the draft
2. Re-run the relevant review skill on the amended section
3. Verify the issue is resolved
4. Max 2 iterations per issue — escalate unresolved items

Persist revision log to `_workspace/patent-pipeline/{date}/phase5-revisions.md`

### Phase 6: Packaging

Assemble the final filing package:

**US Filing Package** (`outputs/patent-pipeline/{date}/us/`):

| Document | File | Description |
|----------|------|-------------|
| Title | `title.md` | Invention title |
| Abstract | `abstract.md` | 150-word abstract |
| Claims | `claims.md` | Independent + dependent claims |
| Specification | `specification.md` | Background, summary, detailed description |
| Drawings | `drawings.md` | Mermaid/SVG diagrams with descriptions |
| Review report | `review-report.md` | Quality assessment |
| Prior art summary | `prior-art-summary.md` | Search results |
| Filing checklist | `checklist.md` | Pre-filing verification |

**KR Filing Package** (`outputs/patent-pipeline/{date}/kr/`):

| Document | File | Description |
|----------|------|-------------|
| 발명의 명칭 | `title-kr.md` | 한국어 제목 |
| 요약서 | `abstract-kr.md` | 요약서 |
| 특허청구범위 | `claims-kr.md` | 청구항 (뒷받침 주석 포함) |
| 발명의 설명 | `specification-kr.md` | 상세한 설명 |
| 도면의 간단한 설명 | `drawings-desc-kr.md` | 도면 설명 |
| 도면 | `drawings-kr.md` | 기술 도면 |
| 뒷받침 매트릭스 | `support-matrix-kr.md` | 청구항-명세서 대응표 |
| 검토 보고서 | `review-report-kr.md` | 품질 평가 |
| 선행기술 요약 | `prior-art-summary-kr.md` | 조사 결과 |
| 출원 체크리스트 | `checklist-kr.md` | 출원 전 확인 사항 |

**Pipeline Summary** (`outputs/patent-pipeline/{date}/`):

Write `pipeline-summary.json`:
```json
{
  "date": "YYYY-MM-DD",
  "jurisdiction": ["US", "KR"],
  "invention_title": "...",
  "patentability_score": 8,
  "claims_count": {"independent": 3, "dependent": 12},
  "review_issues": {"critical": 0, "high": 1, "medium": 3},
  "phases_completed": [1, 2, 3, 4, 5, 6],
  "output_paths": {"us": "...", "kr": "..."}
}
```

### Phase 6.5: Pre-Delivery Check

Before declaring the pipeline complete:

(a) **All 6 phases** completed for the selected jurisdiction(s) — verify `_workspace/patent-pipeline/{date}/` contains expected outputs per phase (phase1–phase5, phase6 assembly notes if used).

(b) **`pipeline-summary.json`** reflects **accurate** counts (scores, issue counts, phases_completed, paths).

(c) **Final package** under `outputs/patent-pipeline/{date}/` includes **every** document listed in the Phase 6 tables for each active jurisdiction.

(d) **No unresolved CRITICAL** review issues remain — or user has explicitly accepted residual risk in writing.

(e) **`_workspace/`** and **`outputs/`** files are **both** present where expected and **consistent** (titles, claim counts, jurisdiction flags match summary).

## Intermediate Persistence Map

| Phase | Output Path | Purpose |
|-------|------------|---------|
| 1 | `_workspace/patent-pipeline/{date}/phase1-*` | Search + scan |
| 2 | `_workspace/patent-pipeline/{date}/phase2-*` | Diagrams + chart |
| 3 | `_workspace/patent-pipeline/{date}/phase3-*-draft/` | Drafts |
| 4 | `_workspace/patent-pipeline/{date}/phase4-*-review/` | Reviews |
| 5 | `_workspace/patent-pipeline/{date}/phase5-revisions.md` | Revision log |
| 6 | `outputs/patent-pipeline/{date}/` | Final package |

## Constraints

- Each phase must complete before the next begins
- Quality gates are mandatory — do not skip
- All intermediate files must be persisted before proceeding
- Human review recommended between Phase 4 and Phase 5
- Final output is a draft requiring attorney review, not a legal filing

## Gotchas

- Phase 3 (drafting) is the most token-intensive phase — consider
  subagents for US and KR tracks
- Quality Gate 1 prevents wasted effort on non-patentable inventions
- The revision loop (Phase 5) is capped at 2 iterations to prevent
  infinite cycles — escalate remaining issues
- KR drafting takes longer due to support-basis anchoring at every claim
- For dual-jurisdiction, KR draft should reference US draft for consistency
  but must independently satisfy KIPO requirements
- _workspace files are working state; outputs/ files are the deliverables
