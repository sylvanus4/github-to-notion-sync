---
description: Sprint lifecycle — plan, retro, or release-notes modes
argument-hint: "[plan|retro|release-notes] <context>"
---

# PM Sprint

Manage sprint lifecycle in three modes: plan (capacity, stories, risks), retro (Start/Stop/Continue, 4Ls, Sailboat), or release-notes (technical → user-facing). Uses pm-execution skill with sprint-plan, retro, release-notes sub-skills.

## Usage
```
/pm-sprint plan for 2-week sprint with 5 engineers
/pm-sprint 스프린트 계획 2주 5명으로
/pm-sprint retro using 4Ls framework
/pm-sprint 회고 4Ls 프레임워크로
/pm-sprint release-notes from these PRs and commits
/pm-sprint 릴리즈 노트 작성해줘
```

## Workflow

### Mode: Plan
1. **Capacity estimation**: Get team size, sprint length, holidays, PTO. Calculate available story points or days
2. **Story selection**: Prioritize backlog items against capacity. Flag dependencies and blockers
3. **Risk identification**: List technical risks, scope creep risks, external dependencies. Suggest mitigation

### Mode: Retro
1. **Choose framework**: Start/Stop/Continue, 4Ls (Loved/Learned/Lacked/Longed for), or Sailboat (wind/anchors/rocks/island)
2. **Gather input**: If transcript or notes provided, extract themes. Otherwise provide template for team to fill
3. **Synthesize**: Group related items, highlight top 3–5 actionable improvements, assign owners for follow-up

### Mode: Release-notes
1. **Ingest artifacts**: PRs, commits, Jira tickets, changelog fragments
2. **Translate technical → user-facing**: Rewrite in plain language. Group by feature area or user benefit
3. **Structure**: Sections (e.g., New Features, Improvements, Fixes), ordered by impact. Add upgrade/migration notes if needed

## Notes
- Default to plan mode if no mode specified — ask user to confirm
- For retros, 4Ls works well for learning-focused teams; Sailboat for visual/creative teams
- Release-notes: avoid jargon; write for end users, not engineers
