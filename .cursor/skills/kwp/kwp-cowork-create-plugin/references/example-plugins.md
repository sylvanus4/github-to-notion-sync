# Example Plugin Structures

Three complete plugin examples at different complexity levels: minimal, standard, and advanced.

---

## Example 1: Minimal Plugin (Single Skill)

A plugin that adds domain knowledge for a specific function. No commands, no MCP, no hooks.

### Structure

```
meeting-notes/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── meeting-notes/
│       └── SKILL.md
└── README.md
```

### `.claude-plugin/plugin.json`

```json
{
  "name": "meeting-notes",
  "version": "0.1.0",
  "description": "Structured meeting notes with action items and decisions",
  "author": {
    "name": "Your Name"
  }
}
```

### `skills/meeting-notes/SKILL.md`

```markdown
---
name: meeting-notes
description: >
  Create structured meeting notes from transcripts, raw notes, or live
  dictation. Extracts decisions, action items, and key discussion points.
  Trigger with "write up meeting notes", "summarize this meeting",
  "extract action items from meeting", or "meeting recap".
metadata:
  version: 1.0.0
---

# Meeting Notes

Transform raw meeting input into structured, actionable notes.

## Output Format

### [Meeting Title] — [Date]

**Attendees:** [Names]
**Duration:** [Time]
**Type:** [Stand-up / Planning / Review / Decision / Brainstorm]

#### Decisions Made
- [Decision 1] — Owner: [Name]
- [Decision 2] — Owner: [Name]

#### Action Items
| # | Action | Owner | Due |
|---|--------|-------|-----|
| 1 | [Task] | [Name] | [Date] |

#### Discussion Summary
[2-3 paragraph summary of key topics discussed]

#### Parking Lot
- [Items deferred to future discussion]

## Guidelines

- Lead with decisions and action items — they're why meetings exist
- Keep discussion summary to key points, not a transcript
- Flag items without a clear owner or due date
- If input is messy, ask one clarifying question before structuring
```

### `README.md`

```markdown
# Meeting Notes Plugin

Turns raw meeting notes, transcripts, or dictation into structured
documents with decisions, action items, and summaries.

## Usage

Just describe or paste your meeting notes and ask Claude to structure them.
```

---

## Example 2: Standard Plugin (Skills + Commands)

A plugin for weekly reporting with both knowledge and interactive commands.

### Structure

```
weekly-report/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── weekly-status.md
│   └── team-standup.md
├── skills/
│   └── reporting/
│       ├── SKILL.md
│       └── references/
│           └── report-templates.md
└── README.md
```

### `.claude-plugin/plugin.json`

```json
{
  "name": "weekly-report",
  "version": "0.2.0",
  "description": "Generate weekly status reports and team standups",
  "author": {
    "name": "Your Name"
  },
  "keywords": ["reporting", "status", "standup"]
}
```

### `commands/weekly-status.md`

```markdown
---
name: weekly-status
description: Generate a weekly status report from recent activity
---

# Weekly Status Report

Generate a weekly status report by reviewing recent work.

## Steps

1. Check available sources for this week's activity:
   - Git commits (if available)
   - Task tracker updates
   - Chat messages and decisions
   - Documents created or modified

2. Organize findings into:

   ## Weekly Status — Week of [Date]

   ### Completed
   - [Items shipped or finished this week]

   ### In Progress
   - [Active work with current status]

   ### Blocked
   - [Items stuck and what's needed to unblock]

   ### Next Week
   - [Planned priorities]

   ### Highlights
   - [Notable wins, learnings, or decisions]

3. Load the **reporting** skill for formatting guidance.

4. Ask: "Want me to adjust the level of detail or send this somewhere?"
```

### `commands/team-standup.md`

```markdown
---
name: team-standup
description: Run an async team standup and compile updates
---

# Team Standup

Compile team standup updates into a single digest.

## Steps

1. Ask: "Paste the standup updates from your team, or tell me where to find them."

2. For each person's update, extract:
   - What they completed
   - What they're working on
   - Any blockers

3. Compile into a team digest:

   ## Team Standup — [Date]

   | Person | Completed | Working On | Blocked |
   |--------|-----------|------------|---------|
   | [Name] | [Items] | [Items] | [Items or None] |

   ### Blockers Needing Attention
   - [Blocker] — [Person] — [What's needed]

4. Ask: "Want me to post this to your team channel?"
```

---

## Example 3: Advanced Plugin (Skills + Commands + MCP)

A plugin for sales teams with external tool integration.

### Structure

```
sales-assistant/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── prep-call.md
│   ├── log-activity.md
│   └── pipeline-check.md
├── skills/
│   └── sales-methodology/
│       ├── SKILL.md
│       └── references/
│           ├── qualification-frameworks.md
│           └── objection-handling.md
├── .mcp.json
├── CONNECTORS.md
└── README.md
```

### `.claude-plugin/plugin.json`

```json
{
  "name": "sales-assistant",
  "version": "0.3.0",
  "description": "Sales call prep, activity logging, and pipeline management",
  "author": {
    "name": "Your Name"
  },
  "keywords": ["sales", "CRM", "pipeline"]
}
```

### `.mcp.json`

```json
{
  "mcpServers": {
    "crm": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-hubspot"],
      "env": {
        "HUBSPOT_ACCESS_TOKEN": "${HUBSPOT_ACCESS_TOKEN}"
      }
    }
  }
}
```

### `CONNECTORS.md`

```markdown
# Connectors

## Connectors for this plugin

| Category | Placeholder | Options |
|----------|-------------|---------|
| CRM | `~~CRM` | HubSpot, Salesforce, Pipedrive |
| Calendar | `~~calendar` | Google Calendar, Outlook Calendar |
| Email | `~~email` | Gmail, Outlook |
```

### `commands/prep-call.md`

```markdown
---
name: prep-call
description: Prepare for a sales call with account research and agenda
arguments:
  - name: company
    description: Company name or domain to research
    required: true
---

# Call Prep

Prepare a sales call brief for the specified company.

## Steps

1. Search ~~CRM for the account matching the company name.
   Pull: contacts, deal stage, recent activities, notes.

2. Web search for recent news about the company.

3. Load the **sales-methodology** skill for qualification
   framework guidance.

4. Generate a call prep brief:

   ## Call Prep: [Company]

   ### Account Snapshot
   | Field | Value |
   |-------|-------|
   | Stage | [From CRM] |
   | Deal Size | [From CRM] |
   | Last Touch | [Date and summary] |

   ### Attendees
   [Research each attendee]

   ### Suggested Agenda
   1. [Opening — reference recent interaction]
   2. [Key discussion topic]
   3. [Next steps proposal]

   ### Discovery Questions
   - [Based on gaps in CRM data]

5. Ask: "Want me to adjust the agenda or research anyone specific?"
```

### `skills/sales-methodology/SKILL.md`

```markdown
---
name: sales-methodology
description: >
  Sales qualification frameworks (MEDDPICC, BANT, SPICED), objection
  handling patterns, and deal progression guidance. Trigger with
  "qualify this deal", "how should I handle this objection",
  "what stage is this deal", or "help me progress this opportunity".
metadata:
  version: 1.0.0
---

# Sales Methodology

Frameworks for qualifying deals, handling objections, and
progressing opportunities through the pipeline.

## MEDDPICC Qualification

| Element | Question | What Good Looks Like |
|---------|----------|---------------------|
| Metrics | What business outcomes do they measure? | Specific, quantified goals |
| Economic Buyer | Who signs the check? | Identified and engaged |
| Decision Criteria | How will they evaluate? | Mapped to our strengths |
| Decision Process | What are the steps to yes? | Timeline with milestones |
| Paper Process | What does procurement require? | Legal, security, procurement mapped |
| Identify Pain | What problem are we solving? | Confirmed by multiple stakeholders |
| Champion | Who is selling internally for us? | Has power, access, and motivation |
| Competition | Who else are they evaluating? | Known, with differentiation plan |

## Reference Files

- **`references/qualification-frameworks.md`** — BANT, SPICED,
  and Challenger Sale frameworks in detail
- **`references/objection-handling.md`** — Common objections by
  category with response patterns
```

---

## Plugin Complexity Guide

| Complexity | When to Use | Components |
|------------|------------|------------|
| **Minimal** | Adding domain knowledge for a role | 1 skill |
| **Standard** | Interactive workflows with structured output | Skills + commands |
| **Advanced** | External tool integration and multi-step automation | Skills + commands + MCP |

Start minimal. Add complexity only when the user's workflow requires it.
