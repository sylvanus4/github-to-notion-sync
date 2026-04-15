---
description: "LLM Wiki — manage company and team knowledge wikis with tier-based governance"
---

# Wiki

## Skill Reference

Parse `$ARGUMENTS` to determine which skill to invoke:

- **Company operations** → Read and follow `.cursor/skills/knowledge-base/wiki-company/SKILL.md`
- **Team operations** → Read and follow `.cursor/skills/knowledge-base/wiki-team/SKILL.md`
- **Promotion operations** → Read and follow `.cursor/skills/knowledge-base/wiki-promote/SKILL.md`

## Your Task

User input: $ARGUMENTS

Manage the LLM Wiki system (company + team tiers). Parse `$ARGUMENTS` to determine the target tier and mode:

### Company Wiki (default when no tier specified)

| Input | Mode | Skill |
|---|---|---|
| `company ingest {topic} {url/path}` | Ingest verified content | wiki-company |
| `company compile [topic]` | Compile company wiki | wiki-company |
| `company lint [topic]` | Policy compliance check | wiki-company |
| `company status` | Company wiki health overview | wiki-company |
| `company list` | List company topics | wiki-company |

### Team Wiki

| Input | Mode | Skill |
|---|---|---|
| `team ingest --role {domain} --topic {topic} {url/path}` | Add team content | wiki-team |
| `team compile [--role {domain}]` | Compile team wiki | wiki-team |
| `team query --role {domain} {question}` | Query team wiki | wiki-team |
| `team lint [--role {domain}]` | Team health check | wiki-team |
| `team status [--role {domain}]` | Team wiki overview | wiki-team |
| `team flag-promote --topic {topic} --article {path}` | Flag for promotion | wiki-team |

### Promotion

| Input | Mode | Skill |
|---|---|---|
| `promote review --topic {topic} --article {path}` | Run promotion gates | wiki-promote |
| `promote execute --topic {topic} --article {path}` | Execute promotion | wiki-promote |
| `promote queue [--role {domain}]` | View pending promotions | wiki-promote |
| `promote history [--since {date}]` | View promotion history | wiki-promote |
| `promote reject --topic {topic} --article {path}` | Reject candidate | wiki-promote |

### Shortcuts

| Input | Mode | Skill |
|---|---|---|
| `ingest {topic} {url/path}` | Ingest (auto-detect tier) | wiki-company or wiki-team |
| `status` | Full wiki status (both tiers) | wiki-company + wiki-team |
| `lint` | Lint all topics | wiki-company + wiki-team |

### Routing Logic

1. If `$ARGUMENTS` starts with `company`, `team`, or `promote` → route to that tier
2. If `$ARGUMENTS` starts with a mode keyword (`ingest`, `compile`, etc.) without a tier prefix:
   - Look up the topic in `knowledge-bases/_wiki-registry.json`
   - If company tier → delegate to `wiki-company`
   - If team tier → delegate to `wiki-team`
   - If ambiguous → ask the user
3. If `$ARGUMENTS` is empty → show available modes and ask for input

### Examples

```
/wiki company status
/wiki team query --role sales "What is the latest competitive analysis?"
/wiki promote queue
/wiki ingest engineering-standards https://example.com/new-standard
/wiki status
```
