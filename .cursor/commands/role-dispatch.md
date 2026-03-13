## Role Dispatch

Dispatch a business topic to 10 role-perspective analyzer skills, synthesize a CEO executive briefing, and post to Slack.

### Usage

```
/role-dispatch {topic}                          # analyze topic from all 10 roles
/role-dispatch {topic} --roles cto,pm,security  # analyze from specific roles only
/role-dispatch {topic} --skip hr,finance        # skip specific roles
/role-dispatch {topic} --no-slack               # skip Slack posting
/role-dispatch {topic} --dry-run                # show relevance scores only
```

### Workflow

1. **Parse input** — Extract topic, optional role filters
2. **Fan-out** — Dispatch to 10 role skills in 3 parallel batches (max 4 concurrent)
   - Batch 1: CEO, CTO, PM, Developer
   - Batch 2: UX Designer, Security Engineer, CSO, Sales
   - Batch 3: HR, Finance
3. **Filter** — Only roles with relevance score >= 5 produce full analysis
4. **Synthesize** — Invoke `executive-briefing` to create CEO summary report
5. **Deliver** — Post main summary + per-role thread replies to Slack `#효정-할일`
6. **Report** — Output files, participation stats, Slack links

### Execution

Read and follow the `role-dispatcher` skill (`.cursor/skills/role-dispatcher/SKILL.md`) for orchestration steps, subagent prompts, and error handling.

### Examples

Full cross-role analysis:
```
/role-dispatch New GPU inference service launch for enterprise customers
```

Technical roles only:
```
/role-dispatch API authentication refactor --roles cto,developer,security
```

Skip non-technical roles:
```
/role-dispatch Kubernetes cluster migration --skip hr,sales,finance
```

Preview relevance scores:
```
/role-dispatch Company rebranding initiative --dry-run
```
