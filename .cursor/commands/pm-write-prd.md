---
description: Create a comprehensive Product Requirements Document from a feature idea or problem statement
argument-hint: "<feature or problem statement>"
---

# Product Requirements Document

Write a structured PRD that aligns stakeholders and guides development. Accepts any input from vague ideas to detailed briefs.

## Usage
```
/pm-write-prd SSO support for enterprise customers
/pm-write-prd Users are dropping off at onboarding step 3 — needs fixing
/pm-write-prd 기업 고객을 위한 SSO 지원 PRD 작성
```

## Workflow

### Step 1: Understand the Feature
Accept: feature names, problem statements, user requests, vague ideas, uploaded documents.

### Step 2: Gather Context
Conversationally ask about: user problem (who, severity), target users (segment, size), success metrics, constraints, prior art, scope preference. If documents provided, extract context and only ask about gaps.

### Step 3: Generate PRD
Read and apply pm-execution skill, invoking **create-prd** sub-skill. Create 8-section document: Summary, Background & Context, Objectives & Success Metrics, Target Users, User Stories & Requirements (P0/P1/P2), Solution Overview, Open Questions, Timeline & Phasing.

### Step 4: Review and Iterate
Suggest: scope narrowing, pre-mortem, user story decomposition, stakeholder update.

Save as markdown file.

## Notes
- Narrow PRDs beat comprehensive vague ones
- Non-goals are as important as goals — they prevent scope creep
- Success metrics must be specific: "improve NPS" is bad, "raise NPS from 32 to 45 within 90 days post-launch" is good
