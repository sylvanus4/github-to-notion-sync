---
description: "Team Wiki — manage domain-specific team knowledge scoped by role"
---

# Team Wiki

## Skill Reference

Read and follow the skill at `.cursor/skills/knowledge-base/wiki-team/SKILL.md`.

## Your Task

User input: $ARGUMENTS

Manage team/domain-specific wiki content. Parse `$ARGUMENTS` to determine the mode:

| Input | Mode | Description |
|---|---|---|
| `ingest --role {domain} --topic {topic} {url/path}` | ingest | Add content to a team topic |
| `compile [--role {domain}] [--topic {topic}]` | compile | Build team wiki articles |
| `query --role {domain} {question}` | query | Search team wiki by domain |
| `lint [--role {domain}] [--topic {topic}]` | lint | Team wiki health check |
| `status [--role {domain}]` | status | Team wiki overview |
| `flag-promote --topic {topic} --article {path}` | flag-promote | Mark content for company promotion |

### Valid Domains

sales, marketing, product-management, engineering, data-analytics, design-ux,
finance, human-resources, operations, customer-support, executive, devops-sre,
research, trading, enterprise-productivity, cross-team

### Examples

```
/wiki-team status --role engineering
/wiki-team query --role sales "Who are our main competitors?"
/wiki-team ingest --role research --topic ai-research https://arxiv.org/abs/2401.12345
/wiki-team compile --role marketing
/wiki-team lint --role product-management
/wiki-team flag-promote --topic incident-history --article wiki/post-mortems/2026-q1.md
```

If `$ARGUMENTS` is empty or unclear, ask the user to specify the domain and mode.
If `--role` is omitted but `--topic` is provided, auto-detect the domain from
`knowledge-bases/_wiki-registry.json`.
