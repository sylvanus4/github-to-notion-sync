---
name: pm-execution
description: >-
  Orchestrate product execution workflows: PRDs, OKRs, roadmaps, sprint
  planning, retrospectives, release notes, stakeholder mapping, user stories,
  job stories, pre-mortems, test scenarios, and prioritization frameworks. Based
  on phuryn/pm-skills. Use when the user asks for "write PRD", "plan OKRs",
  "sprint plan", "retrospective", "release notes", "stakeholder map", "user
  stories", "pre-mortem", "test scenarios", "prioritization", "outcome roadmap",
  "meeting summary", or "dummy dataset". Do NOT use for product discovery (use
  pm-product-discovery), product strategy (use pm-product-strategy), or general
  feature spec (use kwp-product-management-feature-spec). Korean triggers:
  "테스트", "계획", "워크플로우", "릴리즈".
metadata:
  author: "thaki"
  version: "1.0.0"
  upstream: "https://github.com/phuryn/pm-skills"
  category: "product"
---
# PM Execution

Product execution skill orchestrator. Routes user requests to 15 sub-skills for planning, documentation, backlog management, and delivery. Read the matching reference file and follow its instructions.

## Sub-Skill Index

| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| brainstorm-okrs | Quarterly OKRs, team goals aligned with company strategy | [references/brainstorm-okrs.md](references/brainstorm-okrs.md) |
| create-prd | PRD, product requirements, feature spec | [references/create-prd.md](references/create-prd.md) |
| dummy-dataset | Test data, mock datasets, sample data | [references/dummy-dataset.md](references/dummy-dataset.md) |
| job-stories | JTBD-style backlog items, situations and motivations | [references/job-stories.md](references/job-stories.md) |
| outcome-roadmap | Output→outcome roadmap transformation | [references/outcome-roadmap.md](references/outcome-roadmap.md) |
| pre-mortem | Launch risk analysis, Tigers/Paper Tigers/Elephants | [references/pre-mortem.md](references/pre-mortem.md) |
| prioritization-frameworks | RICE, ICE, Kano, MoSCoW, framework selection | [references/prioritization-frameworks.md](references/prioritization-frameworks.md) |
| release-notes | Changelogs, user-facing release notes | [references/release-notes.md](references/release-notes.md) |
| retro | Sprint retrospective, action items | [references/retro.md](references/retro.md) |
| sprint-plan | Sprint capacity, story selection, dependencies | [references/sprint-plan.md](references/sprint-plan.md) |
| stakeholder-map | Power/interest grid, communication plan | [references/stakeholder-map.md](references/stakeholder-map.md) |
| summarize-meeting | Meeting transcripts → structured notes | [references/summarize-meeting.md](references/summarize-meeting.md) |
| test-scenarios | QA test cases from user stories | [references/test-scenarios.md](references/test-scenarios.md) |
| user-stories | User stories, 3 C's, INVEST | [references/user-stories.md](references/user-stories.md) |
| wwas | Why-What-Acceptance backlog items | [references/wwas.md](references/wwas.md) |

## Workflow

1. **Route**: Match user intent to one sub-skill from the index.
2. **Read**: Load `references/<sub-skill>.md` and follow its instructions.
3. **Execute**: Produce output per reference template; save markdown when substantial.

## Examples

| User Request | Sub-Skill |
|--------------|-----------|
| "Draft OKRs for Q3 for our onboarding team" | brainstorm-okrs |
| "Write a PRD for the new search feature" | create-prd |
| "Run a pre-mortem on our launch plan" | pre-mortem |

## Error Handling

| Situation | Action |
|-----------|--------|
| Ambiguous request | Ask which sub-skill applies (e.g., user stories vs job stories vs WWA). |
| Missing context | Ask for PRD, roadmap, transcript, or backlog before proceeding. |
| No matching sub-skill | Suggest closest sub-skill or recommend pm-product-discovery / pm-product-strategy. |
