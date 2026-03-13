---
name: notion-meeting-sync
description: >-
  Sync meeting notes from a Notion database, analyze with PM skills, generate
  comprehensive Korean summaries with detailed action items, produce a
  PowerPoint deck, and post the final digest to Slack. Use when the user asks
  to "sync meetings from Notion", "notion meeting sync", "회의록 동기화",
  "회의 요약", "노션 회의록", "meeting digest", "meeting to PPTX",
  "meeting summary from Notion", "노션 회의 요약", or any request to pull Notion
  meeting data, analyze it, and produce summaries or presentations. Do NOT use
  for summarizing a meeting transcript without Notion source (use pm-execution
  summarize-meeting). Do NOT use for syncing markdown docs to Notion (use
  notion-docs-sync). Do NOT use for GitHub-to-Notion project sync (use the
  project's sync scripts). Do NOT use for ad-hoc PPTX creation without Notion
  source (use anthropic-pptx).
metadata:
  author: "thaki"
  version: "1.1.0"
  category: "execution"
---
# Notion Meeting Sync

Pull meeting notes from a Notion database, analyze them with PM skills,
generate comprehensive Korean summaries with detailed action items,
produce a PowerPoint presentation, and post the final digest to Slack
— all in a single sequential pipeline.

## Configuration

| Key | Value |
|-----|-------|
| Notion Database ID | `22c9eddc34e680d5beb9d2cf6c8403b4` |
| Notion View URL | `https://www.notion.so/thakicloud/22c9eddc34e680d5beb9d2cf6c8403b4?v=22c9eddc34e6805a8b50000c969ed362` |
| Output Directory | `output/meetings/` |
| Sync State File | `output/meetings/.sync-state.json` |
| Language | Korean |
| MCP Server (Notion) | `plugin-notion-workspace-notion` |
| MCP Server (Slack) | `plugin-slack-slack` |
| Slack Channel | `#ai-platform-chapter-기획` (ID: `C0AL6D32Z7W`) |

## Scoping Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **all** | `/notion-meeting-sync` | Sync all new/updated meetings since last sync |
| **latest** | `/notion-meeting-sync latest` | Sync only the most recently edited meeting |
| **date** | `/notion-meeting-sync 2026-03-10` | Sync meetings from a specific date |
| **full** | `/notion-meeting-sync full` | Re-sync all meetings (ignore sync state) |

## Pipeline Overview

```
Phase 1: Notion Sync     → Fetch meeting data from Notion DB
Phase 2: Meeting Analysis → Analyze with PM sub-skills
Phase 3: Summary          → Generate comprehensive Korean summary
Phase 4: Action Items     → Extract and document detailed action items
Phase 5: PPTX Generation  → Create PowerPoint presentation
Phase 6: Slack Post       → Post summary & action items to Slack (no file uploads)
```

**Pattern**: Sequential (Phase 1 → 2 → 3 → 4 → 5 → 6).
When multiple meetings are fetched, Phase 2 runs parallel subagents
(one per meeting, max 4 concurrent).

---

## Phase 1: Notion Data Sync

### 1.1 Authenticate Notion MCP

Before any Notion operations, ensure the MCP server is authenticated:

```
CallMcpTool(server="plugin-notion-workspace-notion", toolName="mcp_auth", arguments={})
```

If authentication fails, instruct the user to authorize via the Notion
integration settings.

### 1.2 Query the Meeting Database

Use the Notion MCP to query the database. The plugin-notion-workspace-notion
server provides tools dynamically after authentication. Use whichever
query/search tool is available:

1. **Search for the database** using the database ID `22c9eddc34e680d5beb9d2cf6c8403b4`
2. **Query all pages** from the database, sorted by last edited time (descending)
3. For each page, extract:
   - Page ID
   - Title (meeting name)
   - Last edited time
   - Any date/status/participant properties

Alternatively, use the Notion workspace plugin skills if MCP tools are
unavailable. The `database-query` skill is provided by the
`cursor-public/notion-workspace` Cursor plugin (not a project-local skill).
To use it, read its SKILL.md from the plugin cache and follow its
instructions to query the meeting database.

### 1.3 Compare with Local Sync State

Read `output/meetings/.sync-state.json`. If it does not exist, treat all
pages as new.

For each page from Notion:
- If `page_id` is NOT in `.sync-state.json` → mark as **new**
- If `page_id` exists but `last_edited` is newer → mark as **updated**
- Otherwise → skip

Apply scoping mode:
- `latest`: Keep only the single most recently edited page
- `date`: Keep only pages with matching date
- `full`: Mark all pages as new (ignore sync state)

### 1.4 Fetch Page Content

For each new/updated page:

1. Fetch the full page content (all blocks, including nested children)
2. Convert block content to markdown
3. Save to `output/meetings/raw/{sanitized-title}.md`

### 1.5 Update Sync State

After fetching, update `output/meetings/.sync-state.json`:

```json
{
  "database_id": "22c9eddc34e680d5beb9d2cf6c8403b4",
  "last_synced": "2026-03-10T14:30:00Z",
  "pages": {
    "<page-id>": {
      "title": "Weekly Standup 2026-03-10",
      "last_edited": "2026-03-10T14:00:00Z",
      "synced_at": "2026-03-10T14:30:00Z"
    }
  }
}
```

---

## Phase 2: Meeting Analysis

For each synced meeting, run analysis using PM sub-skills. When multiple
meetings are synced, use parallel Task subagents (max 4 concurrent).

### 2.1 Primary Analysis — Summarize Meeting

Read `.cursor/skills/pm-execution/SKILL.md` and route to the
`summarize-meeting` sub-skill.

Read the reference file at `.cursor/skills/pm-execution/references/summarize-meeting.md`
and follow its instructions with the raw meeting content as input.

Extract:
- Date, time, participants
- Main topic / agenda
- Key discussion points (every topic discussed — miss nothing)
- Decisions made
- Action items with owners and due dates
- Open questions and blockers
- Disagreements or concerns raised

### 2.2 Secondary Analysis — Contextual Skills

Based on meeting content, apply additional analysis where relevant:

| Content Signal | Skill to Apply | Reference |
|---------------|----------------|-----------|
| Stakeholders mentioned | `pm-execution` → `stakeholder-map` | `.cursor/skills/pm-execution/references/stakeholder-map.md` |
| Sprint/backlog discussed | `pm-execution` → `sprint-plan` | `.cursor/skills/pm-execution/references/sprint-plan.md` |
| Retrospective items | `pm-execution` → `retro` | `.cursor/skills/pm-execution/references/retro.md` |
| Feature specs discussed | `kwp-product-management-feature-spec` | `.cursor/skills/kwp-product-management-feature-spec/SKILL.md` |
| OKRs/goals mentioned | `pm-execution` → `brainstorm-okrs` | `.cursor/skills/pm-execution/references/brainstorm-okrs.md` |
| Prioritization needed | `pm-execution` → `prioritization-frameworks` | `.cursor/skills/pm-execution/references/prioritization-frameworks.md` |

Only apply secondary skills when the meeting content clearly matches
the signal. Do not force-apply irrelevant skills.

### 2.3 Cross-Meeting Synthesis

If multiple meetings were synced in one run, identify:
- Recurring topics across meetings
- Action items that appear in multiple meetings (potentially stalled)
- Evolving decisions (changed between meetings)

---

## Phase 3: Summary Generation

Combine Phase 2 analysis into a comprehensive Korean summary document.

### Output Format

Save to `output/meetings/{date}/summary.md` where `{date}` is today's
date in `YYYY-MM-DD` format.

```markdown
# 회의 요약 보고서

**생성일**: YYYY-MM-DD
**동기화 범위**: [all/latest/date/full]
**분석된 회의 수**: N

---

## 1. 회의 개요

### 회의 1: [제목]

**일시**: [날짜 및 시간]
**참석자**: [이름 및 역할]
**주제**: [한 줄 요약]

---

## 2. 핵심 논의 사항

### [주제 1]
- **논의 내용**: [상세 설명]
- **결론**: [결정된 사항]
- **관련 참석자**: [이름]

### [주제 2]
...

---

## 3. 주요 결정 사항

| # | 결정 사항 | 결정 배경 | 영향 범위 | 담당자 |
|---|----------|----------|----------|--------|
| 1 | ... | ... | ... | ... |

---

## 4. 미해결 이슈 / 오픈 질문

| # | 이슈 | 관련 담당자 | 예상 해결 시점 |
|---|------|-----------|-------------|
| 1 | ... | ... | ... |

---

## 5. 액션 아이템 요약

[Phase 4에서 상세 문서 생성 — 여기서는 요약만]

| 우선순위 | 담당자 | 액션 | 기한 |
|---------|--------|------|------|
| 높음 | ... | ... | ... |

---

## 6. 다음 단계

- [구체적인 후속 조치 1]
- [구체적인 후속 조치 2]
```

### Quality Checklist

Before proceeding to Phase 4, verify the summary:
- [ ] Every discussion topic from every meeting is captured
- [ ] All decisions are listed with context
- [ ] All participants are mentioned
- [ ] No action items are missing
- [ ] Open questions are documented
- [ ] Language is clear, accessible Korean

---

## Phase 4: Action Items Document

Generate a detailed, standalone action items document.

### Output Format

Save to `output/meetings/{date}/action-items.md`:

```markdown
# 액션 아이템 상세 문서

**생성일**: YYYY-MM-DD
**출처 회의**: [회의 제목 목록]

---

## 우선순위: 긴급 (높음)

### AI-001: [액션 제목]

- **담당자**: [이름]
- **기한**: [YYYY-MM-DD]
- **우선순위**: 긴급
- **상태**: 미시작
- **관련 회의**: [회의 제목]
- **배경**: [왜 이 액션이 필요한지 2-3문장]
- **상세 내용**:
  1. [구체적 실행 단계 1]
  2. [구체적 실행 단계 2]
  3. [구체적 실행 단계 3]
- **성공 기준**: [완료 판단 기준]
- **의존성**: [선행 조건이나 관련 액션]
- **비고**: [추가 참고 사항]

---

## 우선순위: 보통 (중간)

### AI-002: [액션 제목]
...

---

## 우선순위: 낮음

### AI-003: [액션 제목]
...

---

## 액션 아이템 대시보드

| ID | 액션 | 담당자 | 기한 | 우선순위 | 상태 | 의존성 |
|----|------|--------|------|---------|------|--------|
| AI-001 | ... | ... | ... | 긴급 | 미시작 | - |
| AI-002 | ... | ... | ... | 보통 | 미시작 | AI-001 |
```

### Action Item Extraction Rules

1. **Explicit items**: Anything stated as "we need to", "someone should",
   "let's", "will do", "by next week" → extract as action item
2. **Implicit items**: Decisions that require follow-up work even if not
   explicitly assigned → extract and flag for assignment
3. **Blocked items**: Items dependent on external input or other teams →
   mark dependencies clearly
4. **Recurring items**: Items that appeared in previous meetings without
   resolution → flag as recurring and escalate priority

---

## Phase 5: PPTX Generation

Create a professional PowerPoint presentation from the summary.

### 5.1 Read the PPTX Skill

Read `.cursor/skills/anthropic-pptx/SKILL.md` and follow the
"Creating from Scratch" path (read `pptxgenjs.md`).

### 5.2 Slide Structure

Design the deck with these slides (adjust count based on content volume):

| # | Slide | Content |
|---|-------|---------|
| 1 | 표지 | 회의 요약 보고서 + 날짜 + 팀명 |
| 2 | 목차 | 주요 섹션 overview |
| 3 | 회의 개요 | 참석자, 일시, 주제 요약 |
| 4-N | 핵심 논의 사항 | 각 주제별 1슬라이드 (핵심 포인트 + 결론) |
| N+1 | 주요 결정 사항 | 결정 테이블 or 카드 레이아웃 |
| N+2 | 액션 아이템 | 우선순위별 액션 테이블 |
| N+3 | 미해결 이슈 | 오픈 질문 + 예상 해결 시점 |
| N+4 | 다음 단계 | 후속 조치 + 타임라인 |

### 5.3 Apply Theme

Read `.cursor/skills/anthropic-theme-factory/SKILL.md`.

Select a theme appropriate for business meeting summaries:
- **Recommended**: "Modern Minimalist" or "Ocean Depths" for professional tone
- If the user has a preference, apply their chosen theme

### 5.4 Design Guidelines

Follow the anthropic-pptx design rules:
- Bold, content-informed color palette
- Every slide has a visual element (icons, charts, shapes)
- Vary layouts across slides (two-column, cards, tables, callouts)
- Large stat callouts for key metrics
- 0.5" minimum margins, consistent spacing
- No accent lines under titles
- Korean text throughout

### 5.5 QA Check

Run the QA process from anthropic-pptx:
1. Content QA: `python -m markitdown output/meetings/{date}/meeting-summary.pptx` — verify all content present
2. Visual QA: Convert to images → inspect with a subagent for overlaps,
   overflow, contrast issues
3. Fix-and-verify loop until clean

### 5.6 Save Output

Save to `output/meetings/{date}/meeting-summary.pptx`

---

## Phase 6: Slack Post

Post the meeting digest to `#ai-platform-chapter-기획` using the Slack MCP.
PPTX files are NOT uploaded — only text-based summaries are posted.

### 6.1 Main Message

Send the first message to channel `C0AL6D32Z7W` with a high-level digest:

```
CallMcpTool(
  server="plugin-slack-slack",
  toolName="slack_send_message",
  arguments={
    "channel_id": "C0AL6D32Z7W",
    "message": "<constructed message>"
  }
)
```

**Message format** (adapt content from `summary.md`):

```markdown
📋 *회의 요약 보고서* — {date}

*동기화 범위*: {scope} | *분석된 회의 수*: {count}

---

*📌 회의 목록*
{for each meeting}
• *{title}* — {date/time}, 참석: {participants}
{end for}

---

*🔑 주요 결정 사항*
{numbered list of key decisions}

---

*⚠️ 미해결 이슈*
{numbered list of open issues, if any}

> 상세 내용은 쓰레드를 확인해 주세요.
```

Keep this message under 4000 characters. If the summary is too long,
truncate discussion details and refer to the thread.

### 6.2 Thread: Detailed Discussion Points

Reply in-thread (`thread_ts` = main message timestamp) with the detailed
discussion points from `summary.md` Section 2 ("핵심 논의 사항"):

```markdown
💬 *핵심 논의 사항*

*[주제 1]*
• 논의 내용: ...
• 결론: ...

*[주제 2]*
• 논의 내용: ...
• 결론: ...
```

Split into multiple thread messages if content exceeds 4000 characters.

### 6.3 Thread: Action Items

Reply in-thread with the action items from `action-items.md`:

```markdown
✅ *액션 아이템* ({total_count}건)

*🔴 긴급*
• `AI-001` {action} — 담당: {owner}, 기한: {due_date}
• `AI-002` ...

*🟡 보통*
• `AI-003` {action} — 담당: {owner}, 기한: {due_date}

*🟢 낮음*
• `AI-004` ...
```

### 6.4 Thread: Next Steps

Reply in-thread with the next steps from `summary.md` Section 6:

```markdown
🚀 *다음 단계*
1. {next step 1}
2. {next step 2}
3. ...
```

### 6.5 Slack Post Rules

1. **No file uploads**: Do NOT upload PPTX, markdown files, or any
   attachments. All content is posted as formatted Slack messages.
2. **Thread structure**: Main message + 3 thread replies (discussion,
   action items, next steps). This keeps the channel clean.
3. **Character limit**: Each Slack message must be under 5000 characters.
   Split into multiple messages if needed.
4. **Formatting**: Use Slack mrkdwn syntax (`*bold*`, `_italic_`,
   `` `code` ``, `~strikethrough~`, `>` for quotes).
5. **Cross-meeting synthesis**: If multiple meetings were analyzed,
   add a synthesis thread reply between discussion and action items.

---

## Output Structure

```
output/meetings/
├── .sync-state.json                  # Sync state tracking
├── raw/                              # Raw Notion content (markdown)
│   ├── weekly-standup-2026-03-10.md
│   └── product-review-2026-03-09.md
├── 2026-03-10/                       # Date-stamped output
│   ├── summary.md                    # Comprehensive Korean summary
│   ├── action-items.md               # Detailed action items
│   └── meeting-summary.pptx          # PowerPoint deck
└── 2026-03-09/
    └── ...
```

---

## Examples

### Example 1: Sync all new meetings

User says: `/notion-meeting-sync`

Actions:
1. Query Notion DB → find 3 new meetings since last sync
2. Fetch content for all 3, save to `output/meetings/raw/`
3. Analyze each with pm-execution summarize-meeting (parallel, 3 subagents)
4. Generate `output/meetings/2026-03-10/summary.md` (Korean)
5. Generate `output/meetings/2026-03-10/action-items.md` with 12 action items
6. Create `output/meetings/2026-03-10/meeting-summary.pptx` (10 slides)
7. Post digest to `#ai-platform-chapter-기획`: main message + 3 thread replies

Result: Complete meeting digest package in `output/meetings/2026-03-10/`
and Slack thread in `#ai-platform-chapter-기획`

### Example 2: Latest meeting only

User says: `/notion-meeting-sync latest`

Actions:
1. Query Notion DB → fetch only the most recently edited meeting
2. Single meeting analysis (no parallel subagents needed)
3. Generate summary, action items, and PPTX for that one meeting
4. Post digest to `#ai-platform-chapter-기획`

Result: Focused output for the single latest meeting, posted to Slack

### Example 3: Full re-sync

User says: `/notion-meeting-sync full`

Actions:
1. Ignore `.sync-state.json` → treat all DB pages as new
2. Re-fetch and re-analyze all meetings
3. Generate comprehensive cross-meeting synthesis
4. Post full digest with cross-meeting insights to `#ai-platform-chapter-기획`

Result: Complete refresh of all meeting data with cross-meeting insights,
posted to Slack

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Notion MCP not authenticated | Call `mcp_auth`, then retry |
| Notion API rate limited | Wait and retry with exponential backoff |
| Database ID not found | Verify database ID, prompt user to check Notion integration permissions |
| Empty meeting content | Skip the meeting, log warning, continue with others |
| PPTX generation fails | Fall back to summary.md + action-items.md as deliverables; Slack post still proceeds |
| No new meetings to sync | Report "No new meetings found since last sync" and exit |
| Slack message too long | Split into multiple thread replies, each under 5000 chars |
| Slack MCP fails | Save all outputs locally, report Slack posting failure, do not block pipeline |
| Slack channel not found | Verify channel ID `C0AL6D32Z7W`, search by name `ai-platform-chapter-기획` |

## Integration Notes

- This skill reads from Notion (pull direction) — it does NOT write back
- The sync state file prevents re-processing already-synced meetings
- Raw meeting content is preserved in `output/meetings/raw/` for audit trail
- Each run produces a date-stamped output folder
- The skill is designed to be idempotent — running it twice on the same
  data produces the same output
- Slack posting is the final phase — local file generation always completes
  first, so partial Slack failures do not lose data
- PPTX files are generated locally but NOT uploaded to Slack; only
  text-based summaries and action items are posted as Slack messages
