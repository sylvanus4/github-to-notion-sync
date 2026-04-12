---
name: kb-daily-report
description: >-
  Synthesize daily KB collection and compilation results into a consolidated
  Korean intelligence report with cross-role trend detection, KB health
  snapshot, connection delta tracking, and automated decision item extraction.
  Generates a professional DOCX via anthropic-docx, uploads to Google Drive
  via gws-drive, and posts a structured Slack thread with the Drive link
  to #효정-의사결정.
  Reads newly ingested raw files and compiled wiki articles, extracts key
  findings per role (Sales, Marketing, PM, Engineering, Design, Finance,
  Research), detects entities/themes spanning 3+ roles and promotes them
  as Cross-Role Signals, includes a KB Health Snapshot with freshness scores
  from kb-lint, reports new connections/ documents from today's compile,
  and auto-tags decision-worthy findings using keyword detection.
  Triggered automatically as Phase 6-7 of kb-daily-build-orchestrator.
  Use when the user asks to "generate KB report", "KB 일일 리포트",
  "위키 리포트", "KB intelligence report", "kb-daily-report",
  "cross-role trends", "KB health snapshot", "connection delta",
  or when invoked by kb-daily-build-orchestrator Phase 6.
  Do NOT use for general Slack messaging (use kwp-slack-slack-messaging).
  Do NOT use for the today pipeline stock report (use today).
  Korean triggers: "KB 리포트", "위키 리포트", "일일 지식 리포트",
  "크로스롤 트렌드", "KB 건강 스냅샷", "커넥션 델타".
metadata:
  author: "thaki"
  version: "3.0.0"
  category: "report"
  tags: ["knowledge-base", "report", "slack", "daily-pipeline", "intelligence", "docx", "google-drive", "cross-role", "freshness", "connections"]
---

# KB Daily Report — Wiki Intelligence Digest

Generate a consolidated Korean intelligence report from the day's KB collection and compilation results, produce a professional DOCX uploaded to Google Drive, and post a structured Slack thread with the Drive link to `#효정-의사결정`.

## Slack Target

| Channel | ID |
|---|---|
| `#효정-의사결정` | `C0ANBST3KDE` |

## Prerequisites

- KB daily build pipeline has run (collection + compile completed)
- Slack MCP server connected
- `outputs/kb-daily-build/{DATE}/collection-summary.md` exists
- `knowledge-bases/*/wiki/` directories contain compiled articles
- `gws` CLI installed and authenticated (`gws auth status` passes) — for Google Drive upload
- `knowledge-bases/_config/drive-upload.yaml` with `kb_report_folder_id` — for Google Drive upload
- `anthropic-docx` skill available — for DOCX generation

## Input

The report skill receives context from the orchestrator:

```
DATE=YYYY-MM-DD
collection_summary_path=outputs/kb-daily-build/{DATE}/collection-summary.md
topics_updated=[list of KB topic names that had new raw files today]
dedup_stats={files_removed: N, topics_affected: M}   # from Phase 3.5
```

If invoked manually, scan for today's collection summary automatically.

## Workflow

### Step 1: Gather Intelligence Sources

1. Read `outputs/kb-daily-build/{DATE}/collection-summary.md` for stats
2. For each updated topic, read the wiki `_summary.md` for topic overview
3. For each updated topic, scan `raw/` for files created today (`{DATE}` in filename or mtime)
4. For each updated topic, scan `wiki/concepts/` and `wiki/references/` for recently compiled articles (check frontmatter `compiled_date` or file mtime)

### Step 2: Extract Key Findings Per Role

For each role domain, extract up to 3 key findings from today's new content:

| Role | KB Topics | Finding Focus |
|---|---|---|
| Sales | competitive-intel, sales-playbook | New competitor moves, pricing changes, win/loss patterns |
| Marketing | brand-guidelines, marketing-playbook, content-library | Content trends, brand positioning changes, campaign insights |
| PM | product-strategy, prd-library | Feature gaps, user feedback signals, roadmap implications |
| Engineering | engineering-standards, system-architecture | Architecture decisions, tech debt signals, dependency risks |
| Design | design-patterns | Design system changes, UX pattern updates |
| Finance | finance-policies | Pricing model changes, cost signals, compliance updates |
| Research | (from kb-collect-research output) | Hot papers, trending models, tech breakthroughs |

For each finding, produce:
- **제목**: 1-line Korean title
- **요약**: 2-3 sentence Korean summary
- **시사점**: What this means for ThakiCloud (1 sentence)
- **긴급도**: HIGH / MEDIUM / LOW

### Step 2b: Cross-Role Signal Detection

After collecting per-role findings, detect entities and themes that appear across **3+ roles**. These cross-cutting signals indicate high strategic importance.

1. Extract named entities (companies, technologies, products, market terms) from all role findings
2. Build a frequency map: `entity → [roles that mention it]`
3. Filter entities appearing in 3+ role domains
4. For each cross-role entity, produce a synthesis:
   - **시그널**: Entity name
   - **관련 역할**: List of roles mentioning this entity
   - **종합 해석**: 2-3 sentence Korean synthesis combining perspectives from each role
   - **전략적 의미**: What this cross-role convergence implies for ThakiCloud
   - **긴급도**: HIGH (all 7 roles) / MEDIUM (4-6 roles) / LOW (3 roles)

These are promoted to the **"크로스롤 시그널"** section at the TOP of the report, before per-role details.

### Step 2c: KB Health Snapshot (Freshness Summary)

Include a "KB 건강 스냅샷" section showing topic-level health:

1. For each of the 68 topics, check:
   - Was this topic updated today? (new raw files or recompiled articles)
   - `last_compiled` date from most recent wiki article
   - Count of wiki articles with `staleness_flag: true` or missing `last_compiled`
2. Classify each topic:
   - 🟢 **FRESH**: Updated today or compiled within 7 days
   - 🟡 **AGING**: Last compiled 8-30 days ago
   - 🔴 **STALE**: Last compiled 30+ days ago or no wiki articles
3. Produce a summary table:

```
## KB 건강 스냅샷

| 상태 | 토픽 수 | 비율 |
|---|---|---|
| 🟢 FRESH | 12 | 18% |
| 🟡 AGING | 38 | 56% |
| 🔴 STALE | 18 | 26% |

*오늘 업데이트된 토픽*: competitive-intel, sales-playbook, product-strategy
*주의 필요 (🔴 30일+ 미갱신)*: design-patterns, finance-policies, ...
```

If `kb-lint` has run with Unified Freshness Score, include topic-average scores.

### Step 2d: Connection Delta

Report new `connections/` documents created during today's compile:

1. Scan `knowledge-bases/*/wiki/connections/` for files with today's date in mtime or `compiled_date` frontmatter
2. For each new connection document:
   - **연결 문서**: Filename
   - **연결 개념**: The two (or more) concepts linked
   - **토픽**: Which KB topic
   - **유형**: comparison / causal / composition / temporal (inferred from filename or content)
3. Produce a summary:

```
## 신규 커넥션 (오늘 발견)

| 토픽 | 연결 문서 | 연결 개념 | 유형 |
|---|---|---|---|
| competitive-intel | conn-gpu-pricing-vs-serverless.md | GPU 가격 ↔ 서버리스 전환 | comparison |
| product-strategy | conn-agent-platform-enables-mlops.md | Agent Platform → MLOps | causal |

*총 {N}건의 신규 개념 연결 발견*
```

If no new connections were created, note "오늘 신규 커넥션 없음" and skip this section in Slack.

### Step 3: Identify Decision Items (Auto-Extraction Enhanced)

Scan findings for items that require human decision or action using **two methods**:

**Method 1: Pattern-based triggers** (existing):
- Competitor pricing change requiring response
- New competitor feature threatening differentiation
- Compliance or regulatory change requiring policy update
- Technology shift requiring architecture evaluation
- Market opportunity requiring strategic pivot discussion

**Method 2: Language-based auto-detection** (new):
Scan all finding text (제목, 요약, 시사점) for decision-indicating keywords:
- Korean: "해야 할", "검토 필요", "대응 필요", "기회", "위험", "리스크", "선택해야", "결정 필요", "전략 변경", "긴급"
- English: "should we", "recommend", "risk of", "opportunity to", "requires decision", "must decide", "evaluate whether", "consider switching"

Any finding matching 2+ keywords is auto-promoted to a decision item. Single-keyword matches are flagged as `decision_candidate: true` for human review.

Tag each decision item with:
- `scope`: personal | team
- `urgency`: HIGH | MEDIUM
- `action`: Recommended next step
- `auto_detected`: true/false (whether it was auto-extracted vs manually identified)

### Step 4: Persist Markdown Report

Save the full report to `outputs/kb-daily-build/{DATE}/intelligence-report.md` with:
- Full Korean markdown content
- Structured data (findings array, decision items array)
- Dedup stats from Phase 3.5 (if available)

### Step 5: Generate DOCX Report

Generate a professional Word document using the `anthropic-docx` skill:

1. Read `outputs/kb-daily-build/{DATE}/intelligence-report.md`
2. Generate DOCX with the following sections:
   - **표지**: KB 일일 인텔리전스 리포트 + date
   - **Executive Summary**: Overall stats, HIGH urgency items, cross-role signal count, dedup stats
   - **크로스롤 시그널**: Cross-role entities/themes spanning 3+ roles with synthesis (from Step 2b)
   - **KB 건강 스냅샷**: Topic freshness breakdown (🟢/🟡/🔴 counts, stale topics list) (from Step 2c)
   - **역할별 주요 발견**: One section per role with findings table (제목, 요약, 시사점, 긴급도)
   - **신규 커넥션**: New connections discovered today with linked concepts (from Step 2d)
   - **의사결정 필요 항목**: Decision items (including auto-detected) with scope, urgency, action, auto_detected flag
   - **부록**: Source list, collection stats, dedup stats (files removed, topics affected)
3. Save to `outputs/kb-daily-build/{DATE}/kb-intelligence-report-{DATE}.docx`
4. If DOCX generation fails, log warning and continue without DOCX

### Step 6: Upload to Google Drive

Upload the DOCX report using the `gws-drive` skill:

1. Read folder ID from `knowledge-bases/_config/drive-upload.yaml` (key: `kb_report_folder_id`)
2. Upload `outputs/kb-daily-build/{DATE}/kb-intelligence-report-{DATE}.docx` to the target folder:
   ```bash
   gws drive upload outputs/kb-daily-build/{DATE}/kb-intelligence-report-{DATE}.docx --parent {folder_id}
   ```
3. Capture the shareable link from the upload response
4. If `gws` CLI is unavailable or upload fails, log a warning and continue without the link

### Step 7: Format Slack Report

Build a 4-message Slack thread:

**Message 1 (Main Post):**

```
*KB 일일 인텔리전스 리포트* — {DATE}

*수집 현황*
- 신규 raw 파일: {N}건
- 업데이트된 토픽: {topics_updated 목록}
- 새 위키 문서: {N}건 (컨셉 {N}, 레퍼런스 {N}, 커넥션 {N})
- 중복 제거: {dedup_stats.files_removed}건 ({dedup_stats.topics_affected}개 토픽)

*크로스롤 시그널 ({signal_count}건)*
{For each cross-role signal: 시그널 + 관련 역할 list + 종합 해석, 1-2 lines}

*즉시 주목 ({HIGH count}건)*
{HIGH urgency findings, 1 line each}

*참고 사항 ({MEDIUM count}건)*
{MEDIUM urgency findings, 1 line each}

*KB 건강*: 🟢 {fresh_count} | 🟡 {aging_count} | 🔴 {stale_count}
*신규 커넥션*: {connection_count}건

*상세 리포트*: {Google Drive link or "(업로드 실패)"}
```

**Message 2 (Thread -- Role Details):**

```
*역할별 주요 발견*

*Sales & Competitive Intel*
{Sales findings with 시사점}

*Marketing*
{Marketing findings with 시사점}

*Product Management*
{PM findings with 시사점}

*Engineering*
{Engineering findings with 시사점}

*Design*
{Design findings with 시사점}

*Finance*
{Finance findings with 시사점}

*Research*
{Research findings with 시사점}
```

**Message 3 (Thread -- KB Health & Connections):**

```
*KB 건강 스냅샷*
- 🟢 FRESH ({fresh_count}): {topic list}
- 🟡 AGING ({aging_count}): {topic list, truncated if >10}
- 🔴 STALE ({stale_count}): {topic list}

*신규 커넥션 ({connection_count}건)*
{For each new connection: 토픽 | 연결 문서 | 연결 개념 | 유형}
```

Only post Message 3 if there are stale topics (🔴 > 0) or new connections.

**Message 4 (Thread -- Decision Items):**

Only if decision items exist.

```
*의사결정 필요 항목*

{For each decision item:}
> *{제목}* {auto_detected ? "🤖" : ""}
> 긴급도: {urgency} | 스코프: {scope}
> 시사점: {description}
> 권장 조치: {action}
```

Auto-detected items are marked with 🤖 emoji for transparency.

### Step 8: Post to Slack

1. Post Message 1 to `#효정-의사결정` (`C0ANBST3KDE`)
2. Reply with Message 2 in thread (using `thread_ts` from Message 1)
3. Reply with Message 3 in thread (if stale topics exist or new connections found)
4. Reply with Message 4 in thread (if decision items exist)

## Output Artifacts

| File | Description |
|---|---|
| `outputs/kb-daily-build/{DATE}/intelligence-report.md` | Full report markdown |
| `outputs/kb-daily-build/{DATE}/kb-intelligence-report-{DATE}.docx` | Professional DOCX report |
| Google Drive link | Shareable link to the uploaded DOCX |
| Slack thread in `#효정-의사결정` | 4-message intelligence digest with Drive link (main + roles + health/connections + decisions) |

## Empty Day Handling

If no new raw files were collected today (all collectors returned 0 files):

Post a single message:
```
*KB 일일 인텔리전스 리포트* — {DATE}
오늘 신규 수집 데이터 없음. 모든 토픽 최신 상태 유지 중.
```

Do NOT generate DOCX, upload to Drive, or post thread replies for empty days.

## Error Handling

- If collection summary is missing, scan `knowledge-bases/*/raw/` for today's files directly
- If DOCX generation fails, continue to Slack posting without DOCX/Drive link
- If `gws` CLI is unavailable or Drive upload fails, continue to Slack without Drive link
- If Slack MCP is unavailable, save report to file only and log warning
- If a topic's wiki is empty, skip that role's findings section

## Gotchas

- **Symptom:** Spurious cross-topic trends. **Root cause:** Same URL ingested into multiple topics. **Correct approach:** Deduplicate by URL before trend scoring.
- **Symptom:** Truncated or incomplete DOCX. **Root cause:** anthropic-docx limits on very long output (~50+ pages). **Correct approach:** Split into volumes or shorten sections when daily output exceeds safe length.
- **Symptom:** False decision routes to Slack. **Root cause:** Keywords like "결정" match historical narrative. **Correct approach:** Check temporal context (today vs past) before posting to `#효정-의사결정`.

## Examples

### Example 1: Standard daily report

**User says:** "KB 일일 리포트 생성해줘"

**Actions:**
1. Scan all topic `raw/` for files ingested today.
2. Run cross-topic trend detection on new articles (after URL dedup).
3. Compute per-topic freshness summary.
4. Generate DOCX, upload to Drive.
5. Post the 4-message Slack thread to `#효정-의사결정`.

### Example 2: Focused topic report

**User says:** "오늘 engineering-standards KB에 추가된 내용 리포트"

**Actions:**
1. Limit scope to `engineering-standards` only.
2. Summarize new `raw/` and same-day `wiki/` changes.
3. Emit a single-topic intelligence report (markdown + optional DOCX).

## Constraints

- Expects **kb-daily-build-orchestrator** (or equivalent) to have populated `raw/` and summaries for the report date.
- DOCX path needs **anthropic-docx** available in the session.
- Drive upload needs **gws-drive** auth; Slack needs `SLACK_USER_TOKEN` (or working Slack MCP).
- Reports are date-bound; past dates need archived `raw/` and artifacts, not invented backfill.

## Composability

- **kb-daily-build-orchestrator** — invokes this skill in Phases 6–7 after collection/compile.
- **anthropic-docx** — builds the Korean DOCX deliverable.
- **gws-drive** — uploads DOCX and returns the share link.
- **decision-router** — optional follow-on routing for extracted decision items.
- **kb-lint** — freshness metrics feed the KB Health Snapshot section.

## Output Discipline

- Quiet days: say **변동 없음** per topic; no generic filler paragraphs.
- Each insight appears once in its best section; no copy-paste across sections.
- Length tracks actual delta; short input yields a short report.

## Honest Reporting

- List topics with zero change explicitly; do not omit them for optics.
- DOCX or Drive failures must appear in Slack (e.g. "(업로드 실패)"), not silent drops.
- Trends below the promotion threshold are still noted as "below threshold," not omitted.
