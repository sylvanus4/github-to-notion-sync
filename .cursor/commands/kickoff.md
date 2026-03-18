---
description: Auto-generates a project kickoff package: Notion project page, stakeholder map, initial risk register, and kick-off meeting agenda.
argument-hint: "<project-name> [--desc <description>] [--leads <team-leads>]"
---

# /kickoff

Generates a complete project kickoff package: Notion project page from template, stakeholder map, initial risk register, kick-off meeting agenda, calendar event, and Slack notification.

## What This Command Does

Collects project name, description, and team leads, creates a Notion project page from template, generates a stakeholder map and initial risk register, drafts a kick-off meeting agenda, creates a calendar event via gws-calendar, and notifies the team via Slack.

## Required Input

- **Project name** — Name of the project.
- **Description** (optional) — Brief project description.
- **Team leads** (optional) — Comma-separated list of team lead names.

## Execution Steps

1. **Collect project name, description, team leads** — Parse from command args or prompt user.
2. **Create Notion project page from template** — Use md-to-notion with project template structure.
3. **Generate stakeholder map** — Invoke pm-execution for stakeholder mapping.
4. **Create initial risk register** — Use kwp-operations-risk-assessment for initial risks.
5. **Draft kick-off meeting agenda** — Generate agenda via pm-execution or kwp-product-management-feature-spec.
6. **Create calendar event via gws-calendar** — Schedule kick-off meeting.
7. **Notify team via Slack** — Post kickoff summary to `#효정-할일` or specified channel.

## Output

- Notion project page
- Stakeholder map (visual)
- Risk register (markdown/Notion)
- Kick-off meeting agenda
- Calendar event
- Slack notification

## Skills Used

- pm-execution: Stakeholder map, agenda
- kwp-product-management-feature-spec: Project structure
- md-to-notion: Notion publishing
- gws-calendar: Calendar event creation
- visual-explainer: Stakeholder map diagram

## Example Usage

```
/kickoff AI Platform v2
/kickoff New Feature X --desc "Enterprise SSO integration" --leads "효정, 승우"
```
