---
name: gbrain-briefing
description: >-
  Generate entity-aware morning briefing from gbrain — active deals, recent meetings,
  people in play, and upcoming timelines. Posts a structured Slack thread to
  #효정-할일 as part of the morning pipeline. Use when the user asks to "gbrain
  briefing", "entity briefing", "who's in play", "active deals", "gbrain morning",
  "gbrain-briefing", "엔티티 브리핑", "gbrain 아침", "인맥 브리핑", "활성 딜",
  or wants an entity-centric morning overview. Do NOT use for daily stock analysis
  (use today). Do NOT use for general web search (use parallel-web-search).
  Do NOT use for Cognee knowledge graph queries (use cognee).
metadata:
  version: "2.0.0"
  category: "pipeline"
  author: "thaki"
  composable_with:
    - daily-am-orchestrator
    - unified-knowledge-search
    - gbrain-bridge
    - gbrain-maintain
---
# gbrain Briefing — Entity-Aware Morning Intelligence (v0.10)

Generate a structured entity briefing from gbrain's people, companies, deals, and meetings data. Includes brain health score (0-100), feature availability, autopilot daemon status, and stale compiled truth detection. Designed to run as Phase 8.5 of `daily-am-orchestrator`.

## Prerequisites

- `gbrain` CLI at `~/.local/bin/gbrain`
- PostgreSQL running with gbrain schema initialized
- gbrain MCP server registered in `.cursor/mcp.json`

## Skip Conditions

Set status to `"skipped"` and exit gracefully when:
- `gbrain` CLI not found at `~/.local/bin/gbrain`
- `gbrain doctor --json` fails (PostgreSQL unreachable)
- gbrain has < 5 total pages (insufficient data for meaningful briefing)

## Procedure

### Step 1: Health Check & Brain Status

Run the full v0.10 diagnostic suite. All three commands are independent; run in parallel when possible.

#### 1a. Doctor (connectivity + schema)

```bash
~/.local/bin/gbrain doctor --json
```

Parse output to confirm connectivity and page count. If `pages < 5`, skip with reason.

#### 1b. Health Score (composite 0-100)

```bash
~/.local/bin/gbrain health --json
```

Captures the composite brain health score across dimensions: freshness, link density, embedding coverage, compiled truth ratio, citation density, and filing compliance. Store the `score` and per-dimension breakdown for the briefing.

#### 1c. Features Check

```bash
~/.local/bin/gbrain features --json
```

Returns enabled/disabled status for each v0.10 capability (e.g. `signal_detection`, `brain_first_lookup`, `citation_enforcement`, `filing_protocol`, `autopilot`, `webhook_transforms`, `cron_scheduler`, `acl`). Store the full feature map.

#### 1d. Autopilot Status

```bash
~/.local/bin/gbrain autopilot status --json
```

Check if the persistent autopilot daemon is running. Capture `running` (bool), `pid`, `last_sync`, `last_extract`, `last_embed`, and `uptime`. If the command fails or returns `running: false`, flag as `autopilot_down` for the briefing alert section.

#### 1e. Stale Compiled Truths

```bash
~/.local/bin/gbrain search "compiled-truth" --limit 50 --json
```

For each compiled truth page, compare the `updated_at` timestamp against the `updated_at` of its source pages (linked via backlinks). A compiled truth is **stale** if any source page was updated after the compiled truth's last update. Collect stale items for the briefing alert.

### Step 2: Gather Entity Intelligence

Query gbrain for entity-centric intelligence using the following CLI commands:

#### 2a. Recent Activity (last 7 days)

```bash
~/.local/bin/gbrain search "updated recently" --limit 20 --json
```

#### 2b. People in Play

```bash
~/.local/bin/gbrain search "people" --limit 10 --json
```

Filter results to `people/` namespace pages. Extract names, roles, companies, last interaction dates.

#### 2c. Active Deals / Companies

```bash
~/.local/bin/gbrain search "companies deals active" --limit 10 --json
```

Filter results to `companies/` and `deals/` namespace pages.

#### 2d. Recent Meetings

```bash
~/.local/bin/gbrain search "meetings" --limit 5 --json
```

Filter to `meetings/` namespace pages.

#### 2e. Ideas / Decisions

```bash
~/.local/bin/gbrain search "ideas decisions" --limit 5 --json
```

Filter to `ideas/` namespace pages.

### Step 3: Synthesize Briefing

Compile the gathered data into a structured Korean briefing:

```markdown
## gbrain 엔티티 브리핑 (YYYY-MM-DD)

### 주요 인물 (People in Play)
| 이름 | 소속 | 최근 컨텍스트 | 마지막 접점 |
|------|------|------------|-----------|
| {name} | {company} | {context} | {date} |

### 활성 회사/딜
| 회사 | 상태 | 최근 변경 |
|------|------|----------|
| {company} | {status} | {date} |

### 최근 미팅
- {meeting title} ({date}) — {key takeaway}

### 주요 아이디어/의사결정
- {idea/decision title} — {summary}

### 🧠 Brain Health
- **종합 점수**: {score}/100 {🟢 ≥80 | 🟡 50-79 | 🔴 <50}
- 신선도: {freshness}/100 | 링크 밀도: {link_density}/100
- 임베딩 커버리지: {embedding_coverage}/100 | 인용 밀도: {citation_density}/100
- 컴파일 진실 비율: {compiled_truth_ratio}/100 | 파일링 준수: {filing_compliance}/100

### ⚙️ Features (v0.10)
| 기능 | 상태 |
|------|------|
| signal_detection | ✅/❌ |
| brain_first_lookup | ✅/❌ |
| citation_enforcement | ✅/❌ |
| filing_protocol | ✅/❌ |
| autopilot | ✅/❌ |
| webhook_transforms | ✅/❌ |
| cron_scheduler | ✅/❌ |
| acl | ✅/❌ |

### 🤖 Autopilot
- 상태: {🟢 Running | 🔴 Stopped}
- 마지막 동기화: {last_sync} | 마지막 추출: {last_extract} | 마지막 임베딩: {last_embed}
- 가동 시간: {uptime}

### ⚠️ Alerts
- 오래된 컴파일 진실: {N}건 (소스 갱신 후 미반영)
  - {stale_truth_1}: 소스 {source_page} ({source_updated}) > 컴파일 ({compiled_updated})
- Autopilot 다운: {yes/no}
- 비활성 기능: {disabled_features list}

### 통계
- 총 엔티티: {N}페이지
- 최근 7일 업데이트: {N}건
- 임베딩 대기: {N}건
```

### Step 4: Distribute

If invoked as part of `daily-am-orchestrator`:
- Post as a **thread reply** to the Phase 8 main message in `#효정-할일`
- Include the briefing as a formatted Slack mrkdwn message

If invoked standalone:
- Post to `#효정-할일` as a new message with thread replies for each section

### Step 5: Persist

Write output to `outputs/daily-am/{date}/phase-8.5-gbrain-briefing.json`:

```json
{
  "status": "success",
  "date": "YYYY-MM-DD",
  "stats": {
    "total_pages": N,
    "recently_updated": N,
    "people_found": N,
    "companies_found": N,
    "meetings_found": N,
    "ideas_found": N,
    "stale_embeddings": N
  },
  "brain_health": {
    "composite_score": 85,
    "freshness": 90,
    "link_density": 80,
    "embedding_coverage": 95,
    "citation_density": 70,
    "compiled_truth_ratio": 85,
    "filing_compliance": 88
  },
  "features": {"signal_detection": true, "brain_first_lookup": true, "...": "..."},
  "autopilot": {"running": true, "uptime": "3d 12h", "last_sync": "...", "last_extract": "...", "last_embed": "..."},
  "alerts": {
    "stale_compiled_truths": 2,
    "autopilot_down": false,
    "disabled_features": []
  },
  "briefing_markdown": "...",
  "slack_posted": true,
  "slack_ts": "..."
}
```

## Error Handling

| Error | Action |
|-------|--------|
| gbrain CLI not found | Skip with reason `"gbrain CLI not installed"` |
| PostgreSQL unreachable | Skip with reason `"database unreachable"` |
| gbrain search returns 0 results | Generate minimal briefing noting empty state |
| Slack post fails | Log error, persist briefing to file only |
| Timeout (>60s per query) | Use partial results, note incomplete data |

## Non-Blocking Guarantee

This phase is **non-blocking**. Failures in gbrain briefing:
- Do NOT affect `overall_status` of the morning pipeline
- Do NOT prevent Phase 8 consolidated briefing from completing
- Are logged in `phase-8.5-gbrain-briefing.json` with `status: "failed"` and error details
