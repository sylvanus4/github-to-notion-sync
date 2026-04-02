---
name: github-sprint-digest
description: >-
  Fetch overnight GitHub activity (issues, PRs, reviews, comments) per user
  across multiple projects, generate a Korean summary, and post structured
  digests to Notion sub-pages and Slack. Use when the user asks to "summarize
  GitHub activity", "sprint digest", "GitHub 스프린트 요약", "깃헙 활동 정리",
  "밤새 PR 정리", "github-sprint-digest", or wants a daily development activity
  summary across projects. Do NOT use for creating GitHub issues from commits
  (use commit-to-issue), PR review (use pr-review-captain), or full CI pipeline
  checks (use ci-quality-gate).
metadata:
  author: "thaki"
  version: "1.1.0"
  category: "sprint-management"
---
# github-sprint-digest

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

Fetch overnight GitHub activity per user across multiple projects and distribute Korean summaries.

## Workflow

**Init:** Create `outputs/github-sprint-digest/{date}/` and write initial `manifest.json` (all phases `pending`). See **Pipeline Output Protocol (File-First)**.

1. **Fetch activity** — Use `gh` CLI to pull last 24h of GitHub events across configured repositories: new issues, PR opens/merges/reviews, review comments, CI status changes. **Persist & manifest:** Write `phase-1-fetch.json`; set manifest phase 1 to `complete` (or `failed`/`skipped`) and bump `updatedAt`.

2. **Per-user aggregation** — Read `phase-1-fetch.json`. Group activity by contributor: what each person worked on, PRs awaiting review, blocked items, completed items. **Persist & manifest:** Write `phase-2-aggregate.json`; update manifest phase 2.

3. **Sprint context** — Read `phase-2-aggregate.json`. Cross-reference with current sprint milestones and project board status. **Persist & manifest:** Write `phase-3-sprint-context.json`; update manifest phase 3.

4. **Generate digest** — Read `phase-3-sprint-context.json`. Produce Korean summary per user with: completed items, in-progress items, blocked items, items needing feedback. **Persist & manifest:** Write `phase-4-generate-digest.json`; update manifest phase 4.

5. **Distribute** — Read **only** `manifest.json` (for phase status) and `phase-4-generate-digest.json` (and prior phase files if a field is missing—always prefer on-disk JSON over memory). Create Notion sub-pages per user under the sprint parent page; post team-level summary to Slack sprint channel; flag items needing immediate feedback. **Persist & manifest:** Write `phase-5-distribute.json` (Notion URLs, Slack timestamp, flags); update manifest phase 5 and final `updatedAt`.

## Composed Skills

- GitHub CLI (`gh`) — Issue/PR/review data fetching
- Notion MCP — Sub-page creation for per-user digests
- Slack MCP — Team-level summary posting

## Configuration

Target repositories (default — update per project):

```yaml
repositories:
  - ThakiCloud/ai-platform-webui
  - ThakiCloud/tkai-deploy
  - ThakiCloud/tkai-agents
  - ThakiCloud/research
  - ThakiCloud/ai-template
```

## Pipeline Output Protocol (File-First)

All multi-phase work MUST persist to disk under a date-stamped run directory. Do not rely on chat context to carry data between phases.

### Output directory

- **Root:** `outputs/github-sprint-digest/{date}/`
- **`{date}`:** Run date in `YYYY-MM-DD` (KST or the timezone used for the digest window).

### Phase files

Each phase writes exactly one JSON artifact:

| Phase | Label | File |
| ----- | ----- | ---- |
| 1 | fetch | `phase-1-fetch.json` |
| 2 | aggregate | `phase-2-aggregate.json` |
| 3 | sprint-context | `phase-3-sprint-context.json` |
| 4 | generate-digest | `phase-4-generate-digest.json` |
| 5 | distribute | `phase-5-distribute.json` |

### Manifest

- **Path:** `outputs/github-sprint-digest/{date}/manifest.json`
- The manifest is created at initialization and updated after each phase completes (status + paths).

#### `manifest.json` schema

```json
{
  "skill": "github-sprint-digest",
  "date": "YYYY-MM-DD",
  "outputDir": "outputs/github-sprint-digest/YYYY-MM-DD/",
  "startedAt": "ISO8601",
  "updatedAt": "ISO8601",
  "phases": [
    {
      "id": 1,
      "label": "fetch",
      "outputFile": "phase-1-fetch.json",
      "status": "pending|complete|failed|skipped",
      "updatedAt": "ISO8601"
    }
  ]
}
```

- **`status`:** `complete` when the phase file is written and validated; `failed` on error (with error summary in the phase file or a sibling `phase-N-*.error.txt` if needed); `skipped` when intentionally bypassed.

### Subagent Return Contract

When a subagent executes a phase, it MUST return **only** this object (no large payloads in prose):

```json
{
  "status": "complete|failed|skipped",
  "file": "outputs/github-sprint-digest/{date}/phase-N-{label}.json",
  "summary": "One short sentence for the operator log."
}
```

### Final aggregation rule

Phases that produce the **team summary, Notion body, or Slack post** MUST read inputs **only** from:

- `phase-1-fetch.json` through `phase-4-generate-digest.json` (as required), and
- `manifest.json` for ordering and completion status.

They MUST NOT reconstruct narrative from prior in-context memory alone. If context was compacted, re-read the JSON files from disk.

### Initialization (before Phase 1)

1. Resolve `{date}` for the run.
2. Create the directory `outputs/github-sprint-digest/{date}/` (mkdir -p or equivalent).
3. Write `manifest.json` with all five phases listed and `status: "pending"`, `startedAt` set, `updatedAt` matching `startedAt`.

## Error Handling

| Error | Action |
|-------|--------|
| `gh` CLI not authenticated | Prompt user to run `gh auth login` |
| Repository access denied | Skip inaccessible repo, note in summary, continue with remaining |
| No activity in last 24h for a repo | Report "No activity" for that repo, don't create empty Notion page |
| Notion MCP unavailable | Fall back to Slack-only distribution |
| GitHub API rate limit | Reduce scope to last 12h or most-active repos first |

**Recovery:** If a phase fails, the last valid `phase-*.json` on disk is the resume point. Fix the issue, then re-run from the failed phase after reading that file and `manifest.json`. Do not rely on prior chat context for partial data.

## Examples

```
User: "Summarize GitHub activity from last night to now"
→ Init outputs/github-sprint-digest/{date}/ + manifest.json → phase-1-fetch … phase-5-distribute on disk → Notion/Slack from phase files only

User: "github-sprint-digest"
→ Full pipeline: fetch → aggregate → sprint-context → generate-digest → distribute (each step persists JSON + updates manifest)
```


## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
