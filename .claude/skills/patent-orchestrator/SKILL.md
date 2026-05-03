---
name: patent-orchestrator
description: >-
  Intelligent router that classifies patent tasks by jurisdiction (US/KR/both)
  and task type (search, scan, draft, review, OA response, strategy), then
  dispatches to the appropriate patent-* skill. Handles ambiguous requests by
  asking clarifying questions. Acts as the single entry point for all patent
  work. Use when the user asks for general patent help without specifying
  jurisdiction or task type, e.g. "patent this idea", "특허 도와줘", "help with
  patent", "analyze this for patentability", "patent workflow", "특허 출원 절차", or
  any broad patent request. Do NOT use when the user already specifies a
  jurisdiction and task (route to the specific skill directly). Korean
  triggers: "특허", "특허 도와줘", "특허 출원", "발명 보호", "patent".
---

# Patent Orchestrator — Intelligent Task Router

## Role

Single entry point for all patent-related requests. Classifies the user's
intent by jurisdiction (US, KR, or both) and task type, then delegates to
the appropriate specialist skill.

## Routing Table

| Task Type | US Skill | KR Skill |
|-----------|----------|----------|
| Prior art search | patent-search | patent-search |
| Patentability scan | patent-scanner | patent-scanner |
| Claim chart | patent-claim-chart | patent-claim-chart |
| Technical drawings | patent-diagrams | patent-diagrams |
| Application drafting | patent-us-drafting | patent-kr-drafting |
| Draft review | patent-us-review | patent-kr-review |
| AI/SW invention review | patent-us-review (Alice focus) | patent-kr-ai-invention |
| Office action response | patent-us-oa-response | patent-kr-oa-response |
| Portfolio/strategy | patent-us-portfolio | patent-kr-strategy |

Jurisdiction-agnostic skills (patent-search, patent-scanner, patent-claim-chart,
patent-diagrams) handle both US and KR via internal parameters.

## Edge Case Handling (Before Classification)

Apply explicit routing rules when the input matches these patterns:

(a) **URL to an existing patent or application** (USPTO, KIPO, Espacenet, Google Patents, etc.): Classify as **review** (specification/claims review) or **claim-chart** (if user asks for comparison to another reference). Do not default to drafting.

(b) **Code snippet or repository excerpt** provided as the main input: Classify as **scan** (`patent-scanner`) unless the user explicitly asks for drafting or diagrams.

(c) User says only **"특허"** or equivalent with **no** task or jurisdiction: Present the **full clarification menu** from Step 2 (both jurisdiction and task type).

(d) **Office action / rejection document** pasted or uploaded: Classify as **oa-response**. Detect **jurisdiction** from document language and citations (e.g., USPTO form paragraphs, KIPO 의견제출통지서 양식) — do not rely on the user’s chat language alone.

## Workflow

### Step 1: Intent Classification

Analyze the user's request along two axes:

**Jurisdiction Detection**:

| Signal | Jurisdiction |
|--------|-------------|
| "USPTO", "US patent", "American", "35 USC", "Alice", "continuation" | US |
| "KIPO", "한국", "국내", "특허법", "뒷받침", "분할출원", "진보성" | KR |
| "PCT", "international", "both", "양국", "미국과 한국" | Both |
| Ambiguous / no signal | Ask user |

**Task Type Detection**:

| Signal | Task |
|--------|------|
| "search", "prior art", "선행기술", "찾아줘" | search |
| "patentable", "can I patent", "특허 가능", "발명 발굴" | scan |
| "claim chart", "대비표", "비교" | claim-chart |
| "drawings", "diagrams", "도면" | diagrams |
| "draft", "write", "작성", "출원서" | drafting |
| "review", "check", "검토", "점검" | review |
| "AI patent", "SW patent", "인공지능 발명" | ai-review (KR) or review (US) |
| "office action", "rejection", "거절", "의견서" | oa-response |
| "strategy", "portfolio", "전략", "분할", "계속출원" | strategy |

**Classification Output Gate:** After completing Step 1 analysis, output the following two lines verbatim before proceeding:
```
JURISDICTION: [US|KR|BOTH|AMBIGUOUS]
TASK_TYPE: [search|scan|chart|diagrams|drafting|review|ai-review|oa-response|strategy|AMBIGUOUS]
```
If either value is `AMBIGUOUS`, proceed to Step 2. If both are resolved, skip to Step 3. Omitting this block is a routing violation.

### Step 2: Clarification (if needed)

If jurisdiction or task type is ambiguous, ask **exactly ONE** focused question. **Ambiguity Gate:** If jurisdiction is AMBIGUOUS but task type is resolved, ask only about jurisdiction. If task type is AMBIGUOUS but jurisdiction is resolved, ask only about task type. If both are AMBIGUOUS, present the combined menu below but count it as ONE question. Never ask two separate follow-up messages.

```
특허 관련 도움을 드리겠습니다.

1. 어느 국가를 대상으로 하시나요?
   - 🇺🇸 미국 (USPTO)
   - 🇰🇷 한국 (KIPO)
   - 🌐 양국 모두

2. 어떤 작업이 필요하신가요?
   - 선행기술 조사
   - 특허 가능성 분석
   - 출원서 작성
   - 기존 출원 검토
   - 거절이유 대응
   - 출원 전략 수립
```

### Step 3: Dispatch

Once jurisdiction and task are determined:

1. Read the target skill's SKILL.md
2. Follow its workflow exactly
3. If dispatching to both US and KR skills, run them sequentially:
   US skill first, then KR skill, with a comparison summary

### Step 4: Multi-Jurisdiction Workflow

When both US and KR are requested:

```
Phase 1: Shared Steps
  └── patent-search (multi-jurisdiction mode)
  └── patent-scanner (jurisdiction-agnostic)

Phase 2: US Track          Phase 3: KR Track
  └── patent-us-drafting     └── patent-kr-drafting
  └── patent-us-review       └── patent-kr-review
                              └── patent-kr-ai-invention (if AI/SW)

Phase 4: Cross-Jurisdiction Summary
  └── Comparison of US vs KR claim strategies
  └── Timeline alignment for both jurisdictions
  └── Cost summary for dual filing
```

### Step 5: Output Consolidation

When multiple skills are invoked, produce a consolidated summary:

| Jurisdiction | Skill Used | Key Output | Status |
|-------------|-----------|------------|--------|
| US | patent-us-drafting | 15 claims drafted | Complete |
| KR | patent-kr-drafting | 15 claims + support matrix | Complete |

Write consolidated summary to `outputs/patent-orchestrator/{date}/routing-log.json`.

### Anti-Patterns (Orchestrator)

1. **DO NOT** perform patent search, drafting, review, or OA work **inline** — **always** delegate to the specific `patent-*` skill and follow that skill’s workflow.
2. **DO NOT** assume **jurisdiction** from evidence-free cues — **Korean user text alone** does not prove KIPO filing intent; the user may want **US** filing described in Korean. Confirm jurisdiction when ambiguous.
3. **DO NOT** dispatch to **multiple** skills in parallel for **multi-jurisdiction** work **without** confirming **execution order** and dependencies with the user when order matters.
4. **DO NOT** skip the **routing log** — every dispatch must be **recorded** in `outputs/patent-orchestrator/{date}/routing-log.json`.
5. **DO NOT** classify **"review my patent"** as **drafting** — always distinguish **review** (existing document) from **creation** (new draft).

**Delegation Enforcement Gate:** After Step 3 dispatch, verify that the actual action taken was a **skill invocation** (e.g., `Invoke patent-us-drafting`, `Read SKILL.md`, `Task tool`) — NOT inline generation of claims, prior art tables, or review checklists. If the agent produced patent content directly instead of delegating, flag `DELEGATION VIOLATION` in the routing log and re-route to the correct skill.

### Worked Example: Classification (Dual Jurisdiction + Drafting)

**Input:** `이 LLM 오케스트레이션 플랫폼을 한국과 미국 양국에 특허 출원하고 싶습니다`

- **Jurisdiction:** Both (US + KR) — Signal: `양국`
- **Task:** drafting — Signal: `출원`
- **Suggested dispatch (sequential phases; confirm with user before running):**
  - Phase 1: `patent-search` (multi-jurisdiction prior art)
  - Phase 2: `patent-scanner`
  - Phase 3a: `patent-us-drafting`
  - Phase 3b: `patent-kr-drafting`
  - Phase 4: Cross-jurisdiction summary (claim scope, timeline, cost)

### Pre-Delivery Check

Before reporting the orchestration run complete:

(a) **Routing log** is written to `outputs/patent-orchestrator/{date}/routing-log.json` with each skill invoked, inputs summary, and outcome status.
(b) All dispatched skills **completed** or their **failures** are reported with next steps.
(c) For **multi-jurisdiction** work, a **comparison summary** (US vs KR approach, timeline, cost) is produced when both tracks were requested.

**Routing Log Completeness Gate:** Verify `routing-log.json` contains at least: `timestamp`, `user_request` (original text), `classified_jurisdiction`, `classified_task_type`, `dispatched_skill`, and `outcome` (success/failure + summary). If any field is missing, populate it before declaring orchestration complete.
(d) The **user’s original intent** (task type + jurisdiction + constraints) is **fully addressed** or explicitly listed as blocked/pending.

## Constraints

- Always route to the specific skill — never attempt patent work inline
- If the user's request maps to multiple skills, execute sequentially
- For dual-jurisdiction work, always note differences in approach
- Maintain a routing log for audit purposes

## Gotchas

- "Patent this" without context is a scan task, not a drafting task
- AI/SW inventions need different treatment in US (Alice/Mayo) vs KR
  (HW-SW cooperation) — always flag this difference
- "Review" can mean pre-filing review OR OA response review — clarify
- Korean users may say "특허" for any patent task — always classify
- PCT does not replace national filings — it delays them
