---
name: prd-research-factory
description: >-
  End-to-end pipeline that takes a meeting URL or customer interview,
  auto-researches market context, verifies facts against source material,
  and writes a complete PRD with competitive analysis, market sizing, and
  confidence-scored sections. Includes 3-layer distortion prevention:
  source verification, fidelity monitoring, and human review checkpoints.
  Use when the user asks to "PRD from meeting", "research PRD", "미팅 기반
  PRD", "requirements to PRD", "prd-research-factory", "미팅에서 PRD 만들어",
  "회의 기반 기획서", "PRD 자동 생성", or shares a meeting URL for PRD
  generation. Do NOT use for simple PRD without research (use pm-execution
  create-prd). Do NOT use for meeting digest only (use meeting-digest).
  Do NOT use for feature spec refinement only (use
  kwp-product-management-feature-spec). Do NOT use for document quality
  inspection only (use doc-quality-gate).
metadata:
  author: thaki
  version: "2.0.1"
  category: "execution"
  content_pattern: "sequential-research-prd"
---

# PRD Research Factory

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

Transforms meeting content or customer interviews into a fully researched
product requirements document. Verifies every claim against source material,
scores confidence per section, and provides human review checkpoints to
prevent distortion from AI-generated meeting summaries.

## Configuration

| Key | Value |
|-----|-------|
| Output Directory | `output/prd/` |
| Language | Korean |
| MCP Server (Notion) | `plugin-notion-workspace-notion` |
| MCP Server (Slack) | `plugin-slack-slack` |
| Default Trust Level | `low` (all 3 gates active) |

## Input Modes

| Mode | Detection | Handling |
|------|-----------|----------|
| **Notion URL/ID** | Contains `notion.so` or 32-char hex ID | Fetch via Notion MCP |
| **Local file** | `--file <path>` or valid file path | Read from disk |
| **Raw text** | `--raw` or inline text | Parse directly |

## Pipeline Overview

```
Phase 1: Ingest & Verify   → Fetch content, detect AI summary, source verification
Phase 2: Fact Extraction    → Extract claims with provenance tracking
Phase 3: Research           → Market context, competitive landscape (parallel)
Phase 4: PRD Draft          → Generate PRD with confidence scores
Phase 5: Fidelity Check     → Distortion monitoring report
Phase 6: Quality Gate       → doc-quality-gate + human review
Phase 7: Deliver            → Local files + Notion + optional DOCX/Slack
```

**Pattern**: Sequential with Parallel at Phase 3. Human review gates at
Phases 1, 5, and 7 (configurable via `--trust-level`).

## Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--trust-level low\|medium\|high` | Human review checkpoint intensity | `low` |
| `--no-research` | Skip market research (Phase 3) | false |
| `--notion-parent <id>` | Notion parent page for output | required |
| `--docx` | Generate Word document | false |
| `--slack` | Post summary to Slack | false |
| `--no-notion` | Skip Notion upload | false |

Trust level behavior:
- `low` (default): All 3 gates active — safest for Notion AI summaries
- `medium`: Gate 1 auto-pass, Gates 2+3 active
- `high`: Gates 1+2 auto-pass, Gate 3 only for sections with confidence < 70

---

## Phase 1: Content Ingestion & Source Verification

### 1.1 Fetch Content

Same detection logic as meeting-digest:
- **Notion URL**: Extract page ID, fetch via `notion-fetch` MCP
- **Local file**: Read with Read tool
- **Raw text**: Use directly

### 1.2 Source Type Detection

**CRITICAL**: Distinguish between AI-generated summaries and raw transcripts.

Check for AI summary indicators:
- Notion AI summary markers (`Summary by Notion AI`, structured bullet points
  without speaker attribution, uniform formatting)
- Absence of speaker names, timestamps, or conversational markers
- Suspiciously clean structure without hesitations or topic jumps

Tag the source:

| Source Type | Tag | Reliability |
|-------------|-----|-------------|
| Raw transcript with speaker names | `[RAW_TRANSCRIPT]` (use Korean tag in deliverable) | High |
| Meeting recording transcript | `[RECORDING_TRANSCRIPT]` (Korean tag in deliverable) | High |
| Human-written meeting notes | `[HUMAN_NOTES]` (Korean tag in deliverable) | Medium |
| AI-generated summary | `[AI_SUMMARY_VERIFY]` (Korean tag in deliverable) | Low |
| Mixed (AI summary + raw notes) | `[MIXED_SOURCE]` (Korean tag in deliverable) | Medium |

### 1.3 Gate 1: Source Verification Checkpoint

**Active when**: `--trust-level low` (default)

Present source type, reliability level, and 3-5 bullet content summary.
If AI summary detected, show warning. User can continue, provide
corrections, or abort. For display template, see
[references/gate-protocols.md](references/gate-protocols.md).

If `--trust-level medium|high`, auto-pass with source tag preserved.

Save normalized content to `output/prd/raw/{sanitized-title}.md`.

---

## Phase 2: Fact Extraction with Provenance

### 2.1 Extract Claims

Parse meeting content and extract structured facts:

| Category | Extraction Target |
|----------|-------------------|
| Requirements | Feature requests, user needs, business rules |
| Decisions | Agreed-upon choices with rationale |
| Constraints | Technical limits, budget, timeline, policy rules |
| Stakeholders | Names, roles, ownership assignments |
| Assumptions | Unstated beliefs underlying decisions |
| Open Questions | Unresolved items needing follow-up |

### 2.2 Provenance Tracking

For every extracted fact, record the source location:

```
Fact: "User authentication will use OAuth 2.0"
Source: [Source: meeting notes L23–L25, speaker: Alex Kim]
Confidence: 95 (direct quote)
```
(In Korean deliverables, render fact text and source line in Korean as appropriate.)

Confidence scoring per fact:
- **90-100**: Direct quote from identified speaker in raw transcript
- **70-89**: Paraphrased from clear discussion context
- **50-69**: Inferred from surrounding discussion, not explicitly stated
- **0-49**: Not found in source material — flag as `[NO_SOURCE_EVIDENCE]` (Korean tag in deliverable)

### 2.3 Cross-Reference Check

If Notion project/backlog DBs are accessible:

1. Query Notion for existing project pages related to the meeting topic
2. Compare extracted facts against existing documentation
3. Flag contradictions: `[CONFLICT: doc says X, meeting says Y]` (Korean wording in deliverable)
4. Flag missing context: `[NEEDS_DOC_REF: related PRD exists]` (Korean wording in deliverable)

---

## Phase 3: Market Research (Parallel)

**Skip if**: `--no-research` flag is set.

Launch up to 3 parallel subagents:

### 3.1 Market Context (parallel agent 1)

Read `.cursor/skills/parallel-deep-research/SKILL.md` or use WebSearch:
- Industry trends related to the meeting topic
- Relevant market data and benchmarks
- Technology landscape

### 3.2 Competitive Analysis (parallel agent 2)

Read `.cursor/skills/pm-market-research/SKILL.md`, route to
competitive analysis:
- Competitor feature comparison
- Market positioning analysis
- Differentiation opportunities

### 3.3 Opportunity Discovery (parallel agent 3)

Read `.cursor/skills/pm-product-discovery/SKILL.md`, route to
assumption identification:
- Opportunity Solution Tree from meeting context
- Key assumptions to validate
- Suggested experiments

Aggregate all research results into `output/prd/{date}/research-context.md`.

---

## Phase 4: PRD Draft Generation

### 4.1 Generate PRD

Read `.cursor/skills/pm-execution/SKILL.md`, route to `create-prd`.
Provide as input:
- Extracted facts from Phase 2 (with provenance)
- Research context from Phase 3
- Source reliability tag from Phase 1

PRD structure (Korean section titles in the file):

- Title: `[Product/Feature Name] PRD`
- Document metadata — date, source meeting, source type tag, overall confidence
- Sections 1–8: background, problem, goals/metrics, user stories, requirements (functional / non-functional), constraints/dependencies, timeline, risks/mitigations — each with `[confidence: XX]` as needed
- Appendices A–C: market research summary, competitive analysis, source traceability table

### 4.2 Section-Level Confidence

Calculate confidence per section as weighted average of contained facts:

```
Section confidence = Σ(fact_confidence × fact_weight) / Σ(fact_weight)
```

Weight by importance: requirements (1.5x), decisions (1.3x), constraints
(1.0x), assumptions (0.8x).

### 4.3 Source Traceability Table (Appendix C)

Generate a table mapping every PRD claim to its source (Korean column headers in deliverable):

| PRD section | Claim | Source location | Speaker | Confidence |
|-------------|-------|-----------------|---------|------------|
| 2. Problem | Legacy auth latency | L12–L15 | Alex Kim | 92 |
| 5.1 Functional | OAuth 2.0 adoption | L23–L25 | Alex Kim | 95 |
| 7. Timeline | Q3 launch target | L45 | Jordan Park | 78 |

Save PRD draft to `output/prd/{date}/prd-draft.md`.

---

## Phase 5: Fidelity Check (Distortion Monitoring)

### 5.1 Generate Fidelity Report

Compare the PRD draft against the original meeting content across three
dimensions: **Missing** (in meeting but absent from PRD), **Hallucinated** (in PRD but not in meeting), **Distorted** (meaning changed).

For the full report template and scoring rules, see
[references/fidelity-report-template.md](references/fidelity-report-template.md).

### 5.2 Confidence Heatmap

If `visual-explainer` is available, generate an HTML heatmap showing
section-level confidence:
- Green (90+): High confidence, source-verified
- Yellow (70-89): Moderate confidence, context-inferred
- Orange (50-69): Low confidence, needs review
- Red (<50): No source basis, likely hallucinated

Save to `output/prd/{date}/fidelity-report.md` and optionally
`output/prd/{date}/confidence-heatmap.html`.

### 5.3 Gate 2: Fact Verification Checkpoint

**Active when**: `--trust-level low` or `--trust-level medium`

Present Fidelity Report summary and confidence scores to user. Highlight
sections with confidence < 70. User can continue, provide corrections
(re-run fidelity on modified sections only), or abort.

For gate display templates and protocols, see
[references/gate-protocols.md](references/gate-protocols.md).

---

## Phase 6: Quality Gate

### 6.1 Automated Quality Inspection

Read `.cursor/skills/doc-quality-gate/SKILL.md` and run inspection
on the PRD draft. Evaluate across 7 dimensions (Korean labels in report):
completeness, consistency, policy alignment, state coverage, edge cases, terminology, cross-references

### 6.2 Feature Spec Refinement

If PRD contains detailed feature requirements, optionally read
`.cursor/skills/kwp-product-management-feature-spec/SKILL.md` and
refine the requirements section with structured acceptance criteria.

### 6.3 Auto-Fix Low-Confidence Sections

For sections with confidence < 50:
- If `--trust-level low`: Remove the section and add to "Open Questions"
- If `--trust-level medium|high`: Keep with `[NEEDS_VERIFICATION]` tag (Korean in deliverable)

For sections with confidence 50-69:
- Add `[REVIEW_RECOMMENDED]` tag regardless of trust level (Korean in deliverable)

Save final PRD to `output/prd/{date}/prd-final.md`.

---

## Phase 7: Output Delivery

### 7.1 Gate 3: Final Approval Checkpoint

**Active when**: `--trust-level low`, `medium`, or `high` with
low-confidence sections

Present quality inspection results, final confidence score, and file list.
User chooses: upload to Notion, provide final corrections, or keep local only.

For gate display templates, see
[references/gate-protocols.md](references/gate-protocols.md).

### 7.2 Local Files (always)

```
output/prd/{date}/
├── raw/                    # Phase 1: normalized source
│   └── {title}.md
├── research-context.md     # Phase 3: research output
├── prd-draft.md           # Phase 4: draft with confidence scores
├── fidelity-report.md     # Phase 5: fidelity / drift report
├── confidence-heatmap.html # Phase 5: optional heatmap
├── quality-report.md      # Phase 6: quality gate output
└── prd-final.md           # Phase 7: final PRD
```

### 7.3 Notion Upload (default, unless --no-notion)

Create a temporary directory, run table conversion, create Notion sub-pages,
and clean up:

```bash
TMPDIR=$(mktemp -d /tmp/notion-upload-XXXXXX)

python .cursor/skills/md-to-notion/scripts/convert_tables.py \
  --outdir "$TMPDIR" \
  output/prd/{date}/prd-final.md \
  output/prd/{date}/fidelity-report.md
```

Upload JSON files from `$TMPDIR/notion_page_N.json` via Notion MCP.
After upload verification, clean up: `rm -rf "$TMPDIR"`.

Create 3 sub-pages under `--notion-parent`:
1. `[{date}] {title} PRD` — Final PRD
2. `[{date}] fidelity / fact-check report` — Korean title in deliverable
3. `[{date}] market research` — Research context if Phase 3 ran (Korean title in deliverable)

### 7.4 DOCX Generation (--docx flag)

Read `.cursor/skills/anthropic-docx/SKILL.md` and generate formatted
Word document from the final PRD.

### 7.5 Slack Notification (--slack flag)

Post to specified channel:
- Main message: PRD title + confidence score + Notion link
- Thread: Key decisions + action items
- Thread: Fidelity report summary

### 7.6 Drift Log Update

Append to the configured Notion drift-monitoring log page (if any) a row with: date, meeting title, source type, overall confidence, source match rate, distortion count, missing count. Use Korean column headers in the live table.

This enables trend tracking across PRD generations.

---

## Examples

### Example 1: Meeting URL with low trust (default)

User: `/prd-research-factory https://notion.so/meeting-123 --notion-parent abc123`

Actions:
1. Fetch Notion page, detect AI summary → tag `[AI_SUMMARY_VERIFY]`
2. **Gate 1**: Show summary, user confirms with corrections
3. Extract 23 facts with provenance, 4 flagged as low confidence
4. Run 3 parallel research agents
5. Generate PRD draft, average confidence 78/100
6. Fidelity report: 2 missing items, 1 hallucinated claim
7. **Gate 2**: User reviews, removes hallucinated claim, adds missing context
8. doc-quality-gate: 82/100
9. **Gate 3**: User approves Notion upload
10. Create 3 Notion sub-pages + local files

### Example 2: Local transcript with high trust

User: `/prd-research-factory --file meeting.md --trust-level high --docx`

Actions:
1. Read local file, detect raw transcript → tag `[RAW_TRANSCRIPT]`
2. Gate 1 auto-passed (high trust)
3. Extract 31 facts, all high confidence (raw transcript)
4. Research phase runs
5. PRD draft, confidence 91/100
6. Gate 2 auto-passed (high trust, all sections > 70)
7. doc-quality-gate: 88/100
8. **Gate 3**: Only 1 section at 68, user reviews
9. Generate DOCX + upload to Notion

### Example 3: Quick PRD without research

User: `Create PRD from meeting --no-research --trust-level medium`

Actions:
1. User provides raw text
2. Gate 1 auto-passed (medium trust)
3. Extract facts, generate PRD without research appendix
4. **Gate 2**: User reviews confidence scores
5. **Gate 3**: User approves
6. Upload to Notion

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Notion MCP not authenticated | Instruct user to authorize |
| Meeting content empty | Report and exit |
| All sections below confidence 50 | Warn: source material insufficient for PRD |
| Research agents fail | Continue without research, note in PRD |
| doc-quality-gate score < 50 | Flag for major revision, do not auto-upload |
| Notion upload fails | Save locally, report failure |
| Gate timeout (user unresponsive) | Save current state, resume on next invocation |
| Cross-reference DB not found | Skip cross-reference, note in fidelity report |

---

## Distortion Prevention Summary

For teams frequently encountering Notion AI meeting summary distortion:

1. **Always use `--trust-level low`** when the source is an AI-generated
   summary. This activates all 3 human review gates.
2. **Check the Fidelity Report** — the Missing/Hallucinated/Distorted
   breakdown tells you exactly where the PRD diverges from source.
3. **Track drift over time** — the Notion drift log page shows accuracy
   trends. If distortion rates increase, consider switching to raw
   transcript sources.
4. **Confidence scores are per-section** — you don't need to review the
   entire PRD. Focus review time on sections scoring below 70.
5. **Cross-reference check** catches contradictions with existing docs
   that pure meeting analysis would miss.
