---
description: Decompose features into user stories, job stories, or WWA backlog items
argument-hint: "[user|job|wwa] <feature or epic description>"
---

# PM Write Stories

Decompose features or epics into backlog items in three formats: user stories (As a… I want… So that…), job stories (When… I want to… So I can…), or WWA (What, Why, Acceptance). Uses pm-execution skill with user-stories, job-stories, wwas sub-skills.

## Usage
```
/pm-write-stories user Convert this feature to user stories
/pm-write-stories 사용자 스토리로 분해해줘
/pm-write-stories job Breaking down the onboarding flow
/pm-write-stories 온보딩 플로우 잡 스토리로
/pm-write-stories wwa WWA format for search filters
/pm-write-stories WWA 형식으로 백로그 만들어줘
```

## Workflow

### Step 1: Choose Format
- **user**: As a [role], I want [action], so that [benefit]
- **job**: When [situation], I want to [action], so I can [outcome]
- **wwa**: What / Why / Acceptance criteria
- Default to user if argument omitted

### Step 2: Decompose Feature
- Break feature into smallest valuable increments (vertical slices)
- One user-facing outcome per story
- Avoid technical implementation stories unless they're explicit deliverables

### Step 3: Enrich Each Item
- **Acceptance criteria**: Given/When/Then or checklist format
- **Priority**: P0/P1/P2 or MoSCoW (Must/Should/Could/Won't)
- **Dependencies**: Blocked by, blocks, relates to

### Step 4: Output
- Structured list or table: Story ID, Title, Format, AC, Priority, Dependencies
- Optional: export-ready format (Markdown, CSV for Jira/Linear)

## Notes
- Job stories emphasize situation/context; better for complex workflows
- WWA is concise; good for teams that prefer minimal ceremony
- Acceptance criteria should be testable — avoid vague language like "works well"
