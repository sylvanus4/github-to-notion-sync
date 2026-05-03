---
name: pm-execution
description: >-
  Orchestrate product execution workflows: PRDs, OKRs, roadmaps, sprint planning,
  retrospectives, release notes, stakeholder mapping, user stories, job stories,
  pre-mortems, test scenarios, prioritization frameworks, and vertical-slice issue
  decomposition. Based on phuryn/pm-skills frameworks.
disable-model-invocation: true
arguments: [action, topic]
---

# PM Execution — Product Management Workflows

Comprehensive product execution toolbox. Specify an action and topic to generate structured PM artifacts.

## Usage

```
/pm-execution create-prd "User authentication system"
/pm-execution okrs "Q3 platform goals"
/pm-execution sprint-plan
/pm-execution retro
/pm-execution user-stories "File upload feature"
/pm-execution to-issues docs/plans/auth-spec.md
```

## Available Actions

### Document Generation

| Action | Output |
|--------|--------|
| `create-prd` | Full PRD with problem statement, scope, user journeys, requirements |
| `okrs` | OKRs with measurable key results |
| `roadmap` | Outcome-based roadmap with Now/Next/Later format |
| `release-notes` | User-facing release notes from recent commits/PRs |
| `stakeholder-map` | Stakeholder matrix with influence/interest levels |

### Planning & Analysis

| Action | Output |
|--------|--------|
| `sprint-plan` | Sprint plan with prioritized backlog and capacity |
| `retro` | Retrospective facilitation (What worked / What didn't / Actions) |
| `pre-mortem` | Pre-mortem risk analysis before launch |
| `prioritize` | Prioritization using RICE, ICE, or MoSCoW framework |
| `test-scenarios` | Test scenarios with edge cases and acceptance criteria |

### Story & Requirements

| Action | Output |
|--------|--------|
| `user-stories` | User stories with acceptance criteria |
| `job-stories` | Job stories (When... I want to... So I can...) |
| `summarize-meeting` | Meeting summary with decisions and action items |
| `dummy-data` | Realistic dummy dataset for prototyping |

### Issue Decomposition

| Action | Output |
|--------|--------|
| `to-issues` | Break a plan/spec/PRD into vertical-slice GitHub issues |

`to-issues` workflow:
1. Read the input document (PRD, spec, plan)
2. Decompose into independently-grabbable vertical slices (tracer bullets)
3. For each slice: title, description, acceptance criteria, dependencies, size estimate
4. Order by dependency graph — foundational slices first
5. Present the issue list for approval before creating

## PRD Template

When `create-prd`:

```markdown
# [Feature Name] PRD

## Problem Statement
[What problem are we solving and for whom?]

## Target Users
[Primary and secondary user segments]

## Goals
[Measurable success criteria]

## Non-Goals
[Explicitly out of scope]

## User Journeys
[Step-by-step flows for key scenarios]

## Functional Requirements
[Prioritized feature requirements]

## Non-Functional Requirements
[Performance, security, scalability, accessibility]

## Technical Considerations
[Architecture impact, dependencies, risks]

## Open Questions
[Unresolved items requiring stakeholder input]
```

## Output Rules

- All output in Korean unless explicitly requested otherwise
- Include uncertainty levels for estimates
- Reference existing project docs where applicable
- Flag assumptions that need stakeholder validation

## Test Invocation

```
/pm-execution create-prd "GPU quota management for multi-tenant platform"
/pm-execution to-issues docs/plans/kueue-localqueue.md
/pm-execution sprint-plan
/pm-execution retro
```
