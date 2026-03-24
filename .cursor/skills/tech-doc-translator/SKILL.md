---
name: tech-doc-translator
description: >-
  API·아키텍처·클라우드·코드 주석 등 기술 문서를 기획자·디자이너·운영·경영진이 이해할 수 있게 번역·해설한다.
  Use when the user asks to "explain this technical doc", "translate tech spec for planners",
  "기술 문서 쉽게 설명", "API 문서 기획자용으로", "기술 스펙 해석", "비개발자용 설명",
  "기술 용어 풀어줘", "기술 문서 설명해줘", "tech context", "tech-doc-translator",
  "non-tech explanation", "explain technical docs for planners", or needs planning implications
  and constraints/opportunities from technical material.
  Do NOT use for authoring new technical documentation (use technical-writer).
  Do NOT use for code review or reverse spec from code (use deep-review or code-to-spec).
  Do NOT use for cloud feasibility studies without translation focus (use cloud-requirements-analyst).
  Do NOT use for meeting notes (use meeting-digest).
  Do NOT use for pure natural-language translation unrelated to technical docs (translate directly).
metadata:
  author: thaki
  version: "2.0.1"
  category: generation
---

# Tech Doc Translator

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

Transforms **API docs**, **architecture / system design**, **cloud service docs**, and **code comments** into audience-specific Korean narratives. Preserves technical accuracy while surfacing **planning implications**, **constraints**, **opportunities**, **states**, **exceptions**, and **decision points**.

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| `<document>` | Yes | Path, URL, Notion page, pasted text, or GitHub reference |
| `--audience` | No | `planner` \| `pm` \| `designer` \| `ops` \| `executive` \| `all` (default: `planner`) |
| `--depth` | No | `summary` \| `standard` \| `detailed` (default: `standard`; aliases: `overview`→summary, `deep-dive`→detailed) |
| `--keep-terms` | No | Keep original terms in parentheses (default: true) |
| `--glossary` | No | Project glossary file path for consistent wording |
| `--focus` | No | Narrow to API, section, or question |

## Document acquisition

| Source | Method |
|--------|--------|
| Web URL | `defuddle` or WebFetch for clean markdown |
| Notion | Notion MCP |
| GitHub | GitHub MCP or raw fetch |
| Local file | Read tool |

**CRITICAL:** If length > ~5000 characters, outline first, then segment (Type 1 context gap — do not skip sections silently).

## Workflow

```
Phase 1  Parse      — Classify doc type, map structure
Phase 2  Identify  — Terms, patterns, states, constraints
Phase 3  Transform — Audience-specific rewrite
Phase 4  Implications — Planning frame + decisions + opportunities/risks
Phase 5  Enrich    — Analogies, FAQ, glossary, optional diagrams
Phase 6  Deliver   — Final markdown (+ optional Notion / Slack)
```

### Phase 1 — Parse

Classify as one or more: **API**, **system design**, **technical spec / protocol**, **infra / ops**, **incident / postmortem**, **code comments only**, **cloud product doc**.

### Phase 2 — Identify

Extract:

- Concepts, acronyms, endpoints, status codes, limits  
- Dependencies, costs, SLAs, security/compliance hooks  

Apply [references/state-extraction-guide.md](references/state-extraction-guide.md) for **states**, **exceptions**, and **constraints** → map to planning impact.

Load [references/audience-profiles.md](references/audience-profiles.md) for the selected audience.

### Phase 3 — Transform

Apply [references/simplification-rules.md](references/simplification-rules.md) and [references/analogy-patterns.md](references/analogy-patterns.md):

- **Planner**: user-visible behavior, limits, schedule/data implications  
- **Designer**: UI states, latency feel, field limits, error surfaces  
- **Ops**: customer impact, comms, where to verify  
- **Executive**: cost, risk, timeline, strategic tradeoffs  

### Phase 4 — Planning implications

Run the decision lens:

| Lens | Deliver |
|------|---------|
| Scope | New capabilities vs must-drop |
| UX | Speed, failure, empty states |
| Business | Usage-based cost, pricing fit |
| Schedule | Dependency / complexity |
| Risk | Severe failure modes |

List **decision points**: what to decide, options, tradeoffs, technical hint, planning note.

### Phase 5 — Enrich

- Minimum **3 FAQ** pairs  
- **Glossary**: at least 3 terms with non-expert Korean explanations + planning impact (extend with [references/tech-glossary.md](references/tech-glossary.md))  
- Optional Mermaid / ASCII for flows  
- **So-what line**: one sentence per major change (use natural Korean heading in deliverable)  

### Phase 6 — Deliver

Default structure (full narrative in [references/output-template.md](references/output-template.md)):

Deliver in Korean with sections analogous to: title with audience tag; TL;DR (≤3 lines); why this doc matters; core content (transformed body); planning implications / constraints / opportunities; so-what summary; FAQ; glossary; source references.

`--audience all`: emit **Planner + Designer + Executive** bundles (fold Ops into Planner/Ops subsection where useful).

## Output contract (quality gate)

1. **Accuracy** — no factual distortion  
2. **Glossary** — ≥3 terms with planning impact  
3. **TL;DR** — ≤3 lines  
4. **FAQ** — ≥3 Q&As  
5. **So-what** — ≥1 explicit impact sentence  
6. **`--keep-terms`** — originals in parentheses when true  

## Skill chain

| Need | Skill |
|------|-------|
| Publish | `md-to-notion` |
| Canvas / thread | `md-to-slack-canvas` / Slack MCP |
| Doc QA on output | `doc-quality-gate` |
| Deck narrative | `presentation-strategist` |
| Visual overview | `visual-explainer` |

## Examples

**API doc → planner** — Map endpoints to user actions; translate 429/5xx to UX policy.  
**Architecture → executive** — Microservices → release speed vs cost.  
**Cloud IAM doc → ops** — Who gets locked out when roles misconfigured.  
**Inline code comments → designer** — Derive allowed states for a screen.

## Error handling

| Situation | Action |
|-----------|--------|
| URL blocked | Ask for paste or alternate path |
| Non-KO/EN source | Keep technical terms; explain in Korean |
| Huge doc | Section picks + rolling summary |
| Missing audience | Default `planner` |
| Regulated domain | Flag expert review |
| Poor source quality | Suggest `doc-quality-gate` on source first |

## Evolution / eval hooks (binary)

| ID | Check |
|----|--------|
| E1 | Audience calibration (tone/depth matches profile) |
| E2 | ≥2 planning implications (scope/UX/cost/schedule/risk) |
| E3 | ≥1 decision point with options |
| E4 | ≥1 sound analogy |
| E5 | Glossary ≥3 + optional term parentheses |
| E6 | States/constraints extracted when doc implies them (or explicit N/A) |

**Autoimprove test inputs:** REST API doc, microservice architecture, AWS Lambda overview, schema migration notes, OAuth2 summary.
