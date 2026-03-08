## Paperclip Costs

View cost summary, manage budgets, and track token spend across agents and projects.

### Usage

```
/paperclip-costs                           # overall cost summary
/paperclip-costs summary                   # total spend overview
/paperclip-costs by-agent                  # costs grouped by agent
/paperclip-costs by-project                # costs grouped by project
/paperclip-costs budget company <amount>   # set company monthly budget (cents)
/paperclip-costs budget agent <id> <amount>  # set agent monthly budget (cents)
```

### Workflow

1. **Parse scope** — determine view from `$ARGUMENTS` (default: summary)
2. **Fetch data** — cost summary, by-agent, or by-project via REST
3. **Present** — formatted table with spend, budget, and utilization percentage
4. **Budget action** — update budgets if requested

### Execution

Read and follow the `paperclip-control` skill (`.cursor/skills/paperclip-control/SKILL.md`) for cost and budget endpoints.

### Examples

View all costs by agent:
```
/paperclip-costs by-agent
```

Set agent budget to $50/month:
```
/paperclip-costs budget agent frontend-dev 5000
```
