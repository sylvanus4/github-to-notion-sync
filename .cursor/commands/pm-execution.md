---
description: PM execution workflows — PRDs, OKRs, roadmaps, sprint planning, retrospectives, release notes, user stories, pre-mortems
argument-hint: "<product or feature to plan>"
---

## PM Execution

Product execution workflows: PRDs, OKRs, roadmaps, sprint planning, retrospectives, release notes, stakeholder mapping, user stories, pre-mortems, test scenarios, and prioritization frameworks.

### Usage

```
<sub-skill> [context]
```

### Sub-Skills

| Sub-Skill | Shorthand | What it does |
|-----------|-----------|--------------|
| create-prd | `prd` | Create PRD with 8-section template |
| brainstorm-okrs | `okrs` | Draft team OKRs aligned with company objectives |
| outcome-roadmap | `roadmap` | Transform feature roadmap into outcome-focused roadmap |
| sprint-plan | `sprint` | Sprint planning: capacity, story selection, dependencies |
| retro | `retro` | Facilitate sprint retrospective |
| release-notes | `release` | Draft user-facing release notes |
| stakeholder-map | `stakeholders` | Power x Interest grid with communication plan |
| user-stories | `stories` | User stories following 3 C's and INVEST |
| job-stories | `jobs` | JTBD-style backlog items |
| wwas | `wwa` | Why-What-Acceptance backlog items |
| pre-mortem | `premortem` | Pre-mortem risk analysis (Tigers/Paper Tigers/Elephants) |
| prioritization-frameworks | `prioritize` | Guide to 9 frameworks (RICE, ICE, Kano, MoSCoW, etc.) |
| test-scenarios | `tests` | Generate test scenarios from user stories |
| summarize-meeting | `meeting` | Meeting transcript to structured notes |
| dummy-dataset | `data` | Create realistic dummy datasets (CSV, JSON, SQL) |

### Execution

Read and follow the `pm-execution` skill (`.cursor/skills/pm-execution/SKILL.md`) for the full workflow, sub-skill selection, and error handling.

### Examples

```bash
# Write a PRD
/pm-execution prd -- PRD for the new search feature

# Plan OKRs
/pm-execution okrs -- Q3 OKRs for the onboarding team

# Sprint planning
/pm-execution sprint -- plan next sprint for the checkout team

# Pre-mortem on launch
/pm-execution premortem -- risk analysis for our v2.0 launch plan

# Transform roadmap
/pm-execution roadmap -- convert our feature list to outcome-focused roadmap

# Generate user stories
/pm-execution stories -- break down the payment integration feature

# Retrospective
/pm-execution retro -- facilitate retro from this sprint's transcript
```
