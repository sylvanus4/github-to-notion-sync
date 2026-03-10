## Notion Meeting Sync

Sync meeting notes from Notion, analyze with PM skills, generate comprehensive Korean summaries with detailed action items, and create a PowerPoint presentation.

### Usage

```
/notion-meeting-sync              # Sync all new meetings since last sync
/notion-meeting-sync latest       # Sync only the latest meeting
/notion-meeting-sync 2026-03-10   # Sync meetings from a specific date
/notion-meeting-sync full         # Re-sync all meetings (ignore sync state)
```

### Workflow

1. Read the notion-meeting-sync skill at `.cursor/skills/notion-meeting-sync/SKILL.md`
2. Execute the 5-phase sequential pipeline:

**Phase 1 — Notion Sync:**

- Authenticate Notion MCP (`plugin-notion-workspace-notion`)
- Query meeting database (`22c9eddc34e680d5beb9d2cf6c8403b4`)
- Compare with local sync state (`output/meetings/.sync-state.json`)
- Fetch new/updated page content and save as markdown

**Phase 2 — Meeting Analysis (parallel per meeting, max 4):**

- Read `.cursor/skills/pm-execution/SKILL.md` → route to `summarize-meeting` sub-skill
- Read `.cursor/skills/pm-execution/references/summarize-meeting.md` and follow its template
- Apply secondary PM skills based on content signals (stakeholder-map, sprint-plan, retro, etc.)

**Phase 3 — Summary Generation:**

- Produce comprehensive Korean summary covering all discussion topics, decisions, and open questions
- Save to `output/meetings/YYYY-MM-DD/summary.md`

**Phase 4 — Action Items:**

- Extract all explicit and implicit action items with owners, due dates, priorities, and dependencies
- Save to `output/meetings/YYYY-MM-DD/action-items.md`

**Phase 5 — PPTX Generation:**

- Read `.cursor/skills/anthropic-pptx/SKILL.md` → follow "Creating from Scratch" path
- Read `.cursor/skills/anthropic-theme-factory/SKILL.md` → apply professional theme
- Run content QA + visual QA with fix-and-verify loop
- Save to `output/meetings/YYYY-MM-DD/meeting-summary.pptx`

### Output

```
output/meetings/YYYY-MM-DD/
├── summary.md              # Comprehensive Korean meeting summary
├── action-items.md         # Detailed action items with priorities
└── meeting-summary.pptx    # Professional PowerPoint deck
```

### Execution

Read and follow `.cursor/skills/notion-meeting-sync/SKILL.md`

### Examples

Sync all new meetings and generate reports:
```
/notion-meeting-sync
```

Quick digest of the latest meeting only:
```
/notion-meeting-sync latest
```

Re-process all historical meetings:
```
/notion-meeting-sync full
```
