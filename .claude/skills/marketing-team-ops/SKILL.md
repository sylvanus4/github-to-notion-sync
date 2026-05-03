---
name: marketing-team-ops
description: >-
  Marketing team operations — Elon Algorithm 5-step performance audit with
  stack ranking, and meeting intelligence that extracts actions, decisions,
  and commitments from transcripts.
disable-model-invocation: true
---

# Marketing Team Ops

Team performance management using the Elon Algorithm 5-step framework and meeting intelligence. Audits team output with stack ranking and extracts actionable items from meeting transcripts.

## Triggers

Use when the user asks to:
- "team performance audit", "Elon algorithm", "meeting action extraction"
- "stack ranking", "team audit", "performance review"
- "팀 성과 감사", "엘론 알고리즘", "회의 액션 추출"

## Do NOT Use

- For meeting digest with PM analysis → use `meeting-digest`
- For daily standup summary → use `standup-digest`
- For HR org planning → use `kwp-human-resources-org-planning`
- For meeting action tracking and Slack DM reminders → use `meeting-action-tracker`

## Prerequisites

- Python 3.10+
- `pip install anthropic openai`
- Environment: `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`
- Optional: `HUBSPOT_API_KEY` (for task creation)

## Execution Steps

### Step 1: Team Performance Audit
Run `scripts/team_performance_audit.py --input team_data.json --output report.md`. Applies the Elon Algorithm: (1) Eliminate unnecessary requirements, (2) Delete parts/processes, (3) Simplify and optimize, (4) Accelerate cycle time, (5) Automate.

### Step 2: Meeting Action Extraction
Run `scripts/meeting_action_extractor.py --transcript <file> --format markdown`. Extracts: action items with owners and deadlines, key decisions, commitments, and open questions.

### Step 3: Optional HubSpot Integration
With `HUBSPOT_API_KEY`, automatically creates tasks from extracted action items.

## Examples

### Example 1: Run a team performance audit

User: "Audit our marketing team's performance using the Elon Algorithm"

1. Run `scripts/team_performance_audit.py --input team_metrics.json --output audit_report.md`

Result: 5-step analysis with stack ranking, unnecessary requirements flagged, and automation opportunities.

### Example 2: Extract meeting actions

User: "Pull action items from today's marketing standup"

1. Run `scripts/meeting_action_extractor.py --transcript standup_2026-04-03.txt --format markdown`

Result: Structured list of action items with owners, deadlines, key decisions, and open questions.

## Error Handling

| Error | Action |
|-------|--------|
| ANTHROPIC_API_KEY / OPENAI_API_KEY not set | At least one LLM API key required |
| Team data format error | Expects JSON with `name`, `role`, `metrics` fields |
| Transcript too short | Minimum 500 words for meaningful extraction |
| HubSpot task creation failed | Check API key permissions; tasks are saved locally as fallback |

## Output

- Performance audit report with stack ranking
- Improvement recommendations per team member
- Extracted meeting actions (markdown or JSON)
- Optional: HubSpot tasks from meeting items
