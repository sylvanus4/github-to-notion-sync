---
name: sprint-retro-to-issues
description: >-
  End-to-end pipeline that fetches a sprint retrospective from Notion, runs
  multi-perspective PM analysis, extracts structured action items, applies
  adversarial quality critique, creates GitHub issues with full Project #5
  field setup, and posts a Korean summary to Slack. Use when the user asks to
  "create issues from retro", "sprint retro to issues", "스프린트 회고에서 이슈 생성", "회고
  이슈화", "retro to github", "스프린트 액션 아이템 이슈화", "회고록 이슈 생성", "sprint
  retrospective to GitHub issues", "sprint-retro-to-issues", or shares a
  Notion sprint retro URL with intent to convert action items into tracked
  GitHub issues. Do NOT use for general meeting digest without issue creation
  (use meeting-digest). Do NOT use for creating issues from git commits (use
  commit-to-issue). Do NOT use for sprint triage of existing issues (use
  sprint-orchestrator). Do NOT use for simple meeting notes without retro
  context (use pm-execution summarize-meeting).
disable-model-invocation: true
---

# Sprint Retro-to-Issues Pipeline

## Output Language

All outputs MUST be in Korean (한국어). Technical terms and GitHub field values may remain in English.

## Role

Orchestrator that converts sprint retrospective meetings into tracked GitHub work items. Operates as a 6-phase sequential pipeline with file-first persistence and an adversarial quality gate before issue creation.

## Configuration

| Key | Value |
|-----|-------|
| Output Directory | `outputs/sprint-retro-to-issues/{date}/` |
| Language | Korean |
| MCP Server (Notion) | `plugin-notion-workspace-notion` |
| MCP Server (Slack) | `plugin-slack-slack` |
| GitHub CLI | `gh` (direct CLI, not MCP) |
| GitHub Project | ThakiCloud Project #5 (`PVT_kwDODHOnas4A9FHM`) |
| Default Assignee | `sylvanus4` |
| Default Sprint | `26-04-Sprint3` |
| Default Slack Channel | `#효정-할일` (`C0AA8NT4T8T`) |
| Templates | `references/` directory |

### Owner-to-GitHub Mapping

When extracting action items, resolve `owner_mentioned` to a GitHub username using this table. Unmapped or generic entries (e.g. "팀원(미지정)") fall back to `sylvanus4`.

| 이름 (Korean) | GitHub Username |
|---------------|-----------------|
| 량경님 | `ryangkyung-thaki` |
| 혜림 | `haerimmm` |
| 민기님 | `lapidix` |
| 재훈님 | `jaehoonkim` |
| 종민님 | `jongmin-kim-thakicloud` |
| 윤재님 | `yunjae-park1111` |
| 약교님 | `thaki-yakhyo` |
| 효정님 | `sylvanus4` |
| 재호님 팀 | `sylvanus4` (fallback) |
| 은재님 | `sylvanus4` (fallback) |
| 재우님 | `sylvanus4` (fallback) |
| 상윤 | `sylvanus4` (fallback) |
| 팀원(미지정) | `sylvanus4` (fallback) |

> If `gh issue create --assignee` fails for a username (not a collaborator), retry without `--assignee` and note the intended owner in the issue body metadata.

## Prerequisites

- `gh` CLI authenticated with `repo` and `project` scopes
- Notion MCP server authenticated (`mcp_auth` for `plugin-notion-workspace-notion`)
- Slack MCP server available (`plugin-slack-slack`)
- Access to ThakiCloud GitHub org and Project #5

## Output Artifacts

| Phase | Stage Name | Output File | Skip Flag |
|-------|-----------|-------------|-----------|
| 1 | Collect | `outputs/sprint-retro-to-issues/{date}/phase-1-collect.json` | — |
| 2 | Analyze | `outputs/sprint-retro-to-issues/{date}/phase-2-analyze.json` | `--skip-analysis` |
| 3 | Extract | `outputs/sprint-retro-to-issues/{date}/phase-3-extract.json` | — |
| 4 | Critique | `outputs/sprint-retro-to-issues/{date}/phase-4-critique.json` | `--skip-critique` |
| 5 | Create Issues | `outputs/sprint-retro-to-issues/{date}/phase-5-issues.json` | `--dry-run` |
| 6 | Report | `outputs/sprint-retro-to-issues/{date}/phase-6-report.json` | — |
| — | Summary report | `outputs/sprint-retro-to-issues/{date}/report.md` | — |
| — | Action items | `outputs/sprint-retro-to-issues/{date}/action-items.md` | — |
| — | Run manifest | `outputs/sprint-retro-to-issues/{date}/manifest.json` | — |

## Pipeline Initialization

Before Phase 1, execute once per run:

1. Set `{date}` to the run date in `YYYY-MM-DD`.
2. Create the output directory: `mkdir -p outputs/sprint-retro-to-issues/{date}/`
3. Write an initial `manifest.json`:
   ```json
   {
     "pipeline": "sprint-retro-to-issues",
     "date": "{date}",
     "notion_url": "{input-url}",
     "started_at": "{ISO-8601}",
     "completed_at": null,
     "phases": [],
     "overall_status": "running",
     "warnings": [],
     "flags": {}
   }
   ```

## Subagent Return Contract

Any Task/subagent invoked MUST return only:

```json
{
  "status": "success | skipped | failed",
  "file": "path to written artifact or null",
  "summary": "one short paragraph"
}
```

The parent reads content from `file`, never from the subagent's chat transcript.

---

## Phase 1: Collect (Notion Fetch)

**Goal**: Fetch the full Notion sprint retro page including transcript.

### Steps

1. Authenticate Notion MCP if needed:
   ```
   CallMcpTool(server="plugin-notion-workspace-notion", toolName="mcp_auth")
   ```

2. Fetch the page with transcript:
   ```
   CallMcpTool(
     server="plugin-notion-workspace-notion",
     toolName="notion-fetch",
     arguments={"id": "{notion-url}", "include_transcript": true}
   )
   ```

3. From the response, extract and separate:
   - **Meeting summary** (structured content from the page body)
   - **Full transcript** (from `include_transcript`)
   - **Retro table** (personal sprint retrospective entries)

4. Write extracted content to `phase-1-collect.json`:
   ```json
   {
     "phase": 1,
     "label": "collect",
     "status": "success",
     "meeting_title": "{title}",
     "summary_text": "{extracted summary}",
     "transcript_text": "{full transcript}",
     "retro_table": [{...}],
     "participant_count": N,
     "content_size_kb": N
   }
   ```

5. Update `manifest.json` phases array.

### Error Handling

- If Notion MCP auth fails: report and abort.
- If page not found: report URL and abort.
- If transcript is empty: warn but continue with summary content only.

---

## Phase 2: Analyze (Multi-Perspective PM Analysis)

**Goal**: Run meeting-digest-style analysis on the collected content.

### Steps

1. Read `phase-1-collect.json` from disk.

2. Launch a **generalPurpose** subagent with the meeting-digest analysis methodology:

   **Subagent prompt**: Read the meeting-digest skill at `.cursor/skills/pipeline/meeting-digest/SKILL.md`. Using the collected meeting content from `{phase-1 file path}`, perform:

   a. **Meeting type classification**: Classify as `sprint-retro` type.

   b. **PM analysis activation**: Run the following PM sub-skills relevant to sprint retrospectives:
      - `pm-execution retrospective`: What went well, what didn't, improvements
      - `pm-execution test-scenarios`: Identify process gaps from retro discussion
      - If product strategy is discussed: `pm-product-strategy` analysis

   c. **Cross-cutting analysis**:
      - Technical debt items mentioned
      - Process improvement opportunities
      - Team capacity and velocity observations
      - External dependencies and blockers

   Write results to `phase-2-analyze.json` with:
   ```json
   {
     "phase": 2,
     "label": "analyze",
     "status": "success",
     "meeting_type": "sprint-retro",
     "pm_analyses": ["retrospective", "test-scenarios"],
     "key_findings": [...],
     "improvement_areas": [...],
     "tech_debt_items": [...],
     "process_gaps": [...]
   }
   ```

3. Update `manifest.json`.

### Skip Condition

If `--skip-analysis` flag is set, copy relevant fields from Phase 1 directly and mark as `skipped`.

---

## Phase 3: Extract (Structured Action Items)

**Goal**: Extract structured, assignable action items from the analysis.

### Steps

1. Read `phase-1-collect.json` and `phase-2-analyze.json` from disk.

2. Read the action item template at `references/action-item-template.md`.

3. Extract action items from ALL sources:
   - Meeting summary action items
   - Transcript-derived commitments (look for "I will", "we need to", "let's", "해야 합니다", "할게요")
   - Retro table improvement ideas that are actionable
   - PM analysis findings that require follow-up
   - Technical debt items needing resolution

4. For EACH action item, produce a structured record following the template:
   - `title` MUST be entirely in Korean (한국어). Use an imperative verb form.
   - `description` MUST include expanded background context: why this matters, what the current state is, and what success looks like. Minimum 100 characters.
   - `assignee_github` MUST be resolved from the Owner-to-GitHub Mapping table in Configuration. If the owner cannot be mapped, use `sylvanus4` as fallback.

   ```json
   {
     "id": "SRI-001",
     "title": "{한국어 제목 — 반드시 한국어로, 동사형으로 시작}",
     "description": "{상세 한국어 설명: 배경, 현재 상태, 성공 기준 포함. 최소 100자}",
     "assignee_github": "{resolved GitHub username from owner mapping}",
     "priority": "P0|P1|P2",
     "size": "XS|S|M|L|XL",
     "estimate": 1,
     "category": "bug|feature|improvement|tech-debt|process|documentation",
     "source": "summary|transcript|retro-table|pm-analysis",
     "source_quote": "{relevant quote or reference}",
     "acceptance_criteria": ["{criterion 1}", "{criterion 2}"],
     "dependencies": ["SRI-XXX"],
     "sprint_target": "current|next"
   }
   ```

5. Auto-size rules (AI-driven development, 1 story point = 8h = 1 sprint):
   - XS: < 1h → estimate 0.1
   - S: 1-2h → estimate 0.25
   - M: 2-4h → estimate 0.5
   - L: 4-8h → estimate 1
   - XL: > 8h → 분해 필수; 불가피한 경우 최대 2
   > 웬만해서는 estimate 1을 초과하지 않도록 한다. XL 항목은 더 작은 단위로 분해한다.

6. Write all items to `phase-3-extract.json` and `action-items.md`.

7. Update `manifest.json`.

---

## Phase 4: Critique (Quality Gate)

**Goal**: Adversarial review of extracted action items before issue creation.

### Steps

1. Read `phase-3-extract.json` from disk.

2. Read the critique rubric at `references/critique-rubric.md`.

3. Score EACH action item on 5 dimensions (1-5 scale):

   | Dimension | Checks |
   |-----------|--------|
   | **Completeness** | Has title, description, acceptance criteria, size, priority? |
   | **Clarity** | Would a developer understand what to do without asking questions? |
   | **Actionability** | Is this a concrete task, not a vague wish? Can it be done in one sprint? |
   | **Traceability** | Does source_quote link back to the retro discussion? |
   | **Feasibility** | Is the size/estimate realistic? Are dependencies identified? |

4. **Adversarial checks** (flag issues):
   - Items with no acceptance criteria → FAIL
   - Items with vague descriptions (< 20 characters) → FAIL
   - Items that duplicate another item → MERGE candidate
   - Items with P0 priority but XL size → FLAG (scope too large for urgent)
   - Items missing source attribution → WARN

5. **Gap detection**:
   - Compare extracted items against the original retro topics
   - Flag any discussed topic with NO corresponding action item
   - Check if all retro table "improvement ideas" are captured

6. For items scoring below 3.0 average: rewrite them with improved clarity.

7. Write results to `phase-4-critique.json`:
   ```json
   {
     "phase": 4,
     "label": "critique",
     "status": "success",
     "total_items": N,
     "passed": N,
     "rewritten": N,
     "merged": N,
     "flagged": N,
     "gap_warnings": [...],
     "final_items": [{...}],
     "average_score": 4.2
   }
   ```

8. Update `manifest.json`.

### Skip Condition

If `--skip-critique` flag is set, pass Phase 3 items through unchanged.

---

## Phase 5: Create Issues (GitHub)

**Goal**: Create GitHub issues and set Project #5 fields.

### Steps

1. Read `phase-4-critique.json` from disk (use `final_items`).

2. Read the issue body template at `references/github-issue-body-template.md`.

3. For EACH final action item:

   a. **Create the GitHub issue**:
      ```bash
      gh issue create \
        --repo ThakiCloud/ai-platform-strategy \
        --title "{item.title}" \
        --body "$(cat <<'EOF'
      {rendered issue body from template — all sections in Korean per github-issue-body-template.md}
      EOF
      )" \
        --assignee "{item.assignee_github}" \
        --label "sprint-retro"
      ```

   b. **Get the issue number** from the command output.

   c. **Add to Project #5 and set fields** using GraphQL:

      ```bash
      # Get project item ID
      ITEM_ID=$(gh project item-add 5 \
        --owner ThakiCloud \
        --url "https://github.com/ThakiCloud/ai-platform-strategy/issues/{N}" \
        --format json | jq -r '.id')

      # Set Status → Backlog
      gh project item-edit \
        --project-id PVT_kwDODHOnas4A9FHM \
        --id "$ITEM_ID" \
        --field-id PVTSSF_lADODHOnas4A9FHMzgw46Tk \
        --single-select-option-id {status_option_id}

      # Set Priority
      gh project item-edit \
        --project-id PVT_kwDODHOnas4A9FHM \
        --id "$ITEM_ID" \
        --field-id PVTSSF_lADODHOnas4A9FHMzgw46qc \
        --single-select-option-id {priority_option_id}

      # Set Size
      gh project item-edit \
        --project-id PVT_kwDODHOnas4A9FHM \
        --id "$ITEM_ID" \
        --field-id PVTSSF_lADODHOnas4A9FHMzgw46qg \
        --single-select-option-id {size_option_id}

      # Set Estimate
      gh project item-edit \
        --project-id PVT_kwDODHOnas4A9FHM \
        --id "$ITEM_ID" \
        --field-id PVTF_lADODHOnas4A9FHMzgw46qk \
        --number {estimate}

      # Set Sprint (current)
      gh project item-edit \
        --project-id PVT_kwDODHOnas4A9FHM \
        --id "$ITEM_ID" \
        --field-id PVTIF_lADODHOnas4A9FHMzgw46qo \
        --iteration-id {current_sprint_id}
      ```

   d. Record the created issue URL and project item ID.

4. **Priority → Option ID mapping** (from project-config.md):

   | Priority | Option ID |
   |----------|-----------|
   | P0 (Critical) | `15f21a51` |
   | P1 (High) | `87367794` |
   | P2 (Medium) | `473ded73` |

   > Note: Project #5 has P0-P2 only. Map P3 items to P2.

   | Size | Option ID |
   |------|-----------|
   | XS | `84ca859b` |
   | S | `434b26a1` |
   | M | `ba4bcc7c` |
   | L | `f38a3a9e` |
   | XL | `2f3f024c` |

   | Status | Option ID |
   |--------|-----------|
   | Todo | `f75ad846` |
   | In Progress | `47fc9ee4` |
   | Done | `98236657` |

5. Write results to `phase-5-issues.json`:
   ```json
   {
     "phase": 5,
     "label": "create-issues",
     "status": "success",
     "created_count": N,
     "failed_count": 0,
     "issues": [
       {
         "action_id": "SRI-001",
         "issue_number": 123,
         "issue_url": "https://github.com/ThakiCloud/ai-platform-strategy/issues/123",
         "project_item_id": "...",
         "fields_set": ["status", "priority", "size", "estimate", "sprint"]
       }
     ]
   }
   ```

6. Update `manifest.json`.

### Dry Run Mode

If `--dry-run` flag is set:
- Render all issue bodies to `outputs/sprint-retro-to-issues/{date}/dry-run/` as individual markdown files
- Do NOT call `gh issue create`
- Report what WOULD be created

### Error Handling

- If `gh issue create` fails due to invalid assignee: retry without `--assignee`, add `> 의도된 담당자: {assignee_github}` to the issue body, and continue.
- If `gh issue create` fails for other reasons: log error, continue with remaining items, record in `failed_count`.
- If project field setting fails: log warning but don't fail the issue (issue is still created).
- Get current sprint ID dynamically:
  ```bash
  gh project field-list 5 --owner ThakiCloud --format json | \
    jq -r '.fields[] | select(.name == "Sprint") | .configuration.iterations[0].id'
  ```

---

## Phase 6: Report (Summary & Distribution)

**Goal**: Generate a Korean summary report and post to Slack.

### Steps

1. Read all phase JSON files from disk.

2. Read the report template at `references/report-template.md`.

3. Generate `report.md` with:
   - Pipeline execution summary (phases, timing, counts)
   - Meeting overview (title, participants, topics)
   - Action items summary table (ID, title, priority, issue link)
   - Quality critique results (scores, rewrites, gaps found)
   - Created issues list with direct GitHub links

4. Read the Slack post template at `references/slack-post-template.md`.

5. Post to Slack `#효정-할일` (`C0AA8NT4T8T`):

   **Main message**:
   ```
   🔄 스프린트 회고 → GitHub 이슈 변환 완료

   📋 {meeting_title}
   📊 생성된 이슈: {N}개 | 우선순위: P0({n}) P1({n}) P2({n})
   📎 프로젝트: ThakiCloud Project #5
   ```

   **Thread reply 1** — Issue list:
   ```
   📌 생성된 이슈 목록:
   • #{issue_number}: {title} (P{n}, {size})
   • ...
   ```

   **Thread reply 2** — Quality report:
   ```
   🔍 품질 검사 결과:
   • 총 항목: {N} | 통과: {N} | 보완: {N} | 병합: {N}
   • 평균 품질 점수: {score}/5.0
   • 갭 경고: {N}건
   ```

6. Write `phase-6-report.json` and update `manifest.json` with `completed_at` and `overall_status: "success"`.

---

## Constraints

- NEVER create issues without running the quality gate (Phase 4) unless `--skip-critique` is explicitly set.
- Assign to the `assignee_github` resolved from the Owner-to-GitHub Mapping. If `--assignee` fails (user not a collaborator), retry without `--assignee` and note the intended owner in issue body metadata. Default fallback: `sylvanus4`.
- NEVER skip file persistence between phases.
- All action item descriptions must be in Korean with sufficient detail for a developer to start work.
- All GitHub issue bodies must follow the template with acceptance criteria.
- Size and estimate must be consistent (auto-size rules in Phase 3).

## Gotchas

- Notion MCP requires `mcp_auth` before first use in a session.
- GitHub Project field IDs are org-specific; the IDs in Phase 5 are for ThakiCloud Project #5 only.
- Sprint iteration ID changes each sprint; always fetch dynamically.
- The `gh project item-add` command returns the item ID needed for field edits.
- Slack `slack_send_message` may reject raw `---` horizontal rules; avoid them.
- Large transcripts (>100KB) may need chunking for PM analysis subagents.

## Verification

After execution, verify:
- [ ] All phase JSON files exist in `outputs/sprint-retro-to-issues/{date}/`
- [ ] `manifest.json` shows `overall_status: "success"`
- [ ] Each created issue has all 5 project fields set (Status, Priority, Size, Estimate, Sprint)
- [ ] `report.md` contains clickable GitHub issue links
- [ ] Slack message posted with thread replies
- [ ] No action items from the retro were missed (check gap warnings)

## Error Recovery

| Failure Point | Recovery |
|--------------|----------|
| Phase 1 (Notion fetch) | Check URL validity and Notion MCP auth |
| Phase 2 (Analysis) | Re-run with `--skip-analysis` to use raw content |
| Phase 3 (Extraction) | Check Phase 1 output; ensure transcript is present |
| Phase 4 (Critique) | Re-run with `--skip-critique` to bypass quality gate |
| Phase 5 (GitHub) | Check `gh auth status`; partial creates are recorded in phase-5-issues.json |
| Phase 6 (Report) | Manual: read phase-5-issues.json for issue links |
