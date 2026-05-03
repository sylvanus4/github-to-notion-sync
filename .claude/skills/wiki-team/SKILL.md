---
name: wiki-team
description: >-
  Team/domain wiki manager for domain-specific knowledge scoped by role.
  Manages team-specific raw sources, compiles team wikis, queries content
  filtered by domain, and flags validated content for company promotion.
  Supports a --role parameter (sales, engineering, marketing, etc.) to filter
  operations by domain as defined in _wiki-registry.json and
  _role-registry.json. Handles both confirmed team knowledge (in KB wiki) and
  tracks in-progress team context. Use when the user asks to "add to team
  wiki", "team knowledge base", "sales wiki", "engineering wiki", "team wiki
  query", "domain wiki", "팀 위키", "팀 지식", "영업 위키", "마케팅 위키", "엔지니어링 위키",
  "wiki-team", "팀 위키 추가", "도메인 위키", or any team/domain-scoped wiki operation.
  Do NOT use for company-wide official wiki operations (use wiki-company). Do
  NOT use for promoting content to company tier (use wiki-promote). Do NOT use
  for personal memory operations (use memkraft skills). Korean triggers: "팀
  위키", "도메인 위키", "팀 지식", "영업 위키", "마케팅 위키", "엔지니어링 위키", "팀 위키 빌드".
---

# Team/Domain Wiki Manager

Manages the **team tier** of the LLM Wiki — domain-specific knowledge owned
by functional teams (sales, engineering, marketing, etc.). Scopes all
operations by role/domain using `_wiki-registry.json` and `_role-registry.json`.

## Architecture Context

```
_wiki-registry.json        _role-registry.json
  (topic→tier)               (role→topics+skills)
       │                          │
       └──────────┬───────────────┘
                  ▼
          ┌───────────────┐
          │   wiki-team   │──── --role sales
          │  (this skill) │──── --role engineering
          └───────┬───────┘──── --role marketing
                  │                 ...
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
kb-ingest    kb-compile     kb-lint
 + team       + team        + team
  tags        quality       checks
```

## Parameters

| Param | Required | Description |
|-------|----------|-------------|
| `--role` | Recommended | Domain filter: sales, marketing, engineering, etc. |
| `--topic` | For targeted ops | Specific topic within the domain |
| `--promote` | Flag | Mark content as ready for company promotion review |

## Modes

### 1. `ingest` — Add content to a team topic

```
wiki-team ingest --role <domain> --topic <topic> --source <url|path>
```

1. Validate `<topic>` exists under the specified domain in `_wiki-registry.json`
2. If `--role` omitted, infer domain from topic via registry lookup
3. Run `kb-ingest` on the source
4. Tag raw file frontmatter with `tier: team`, `domain: <domain>`
5. No reviewer gate required (team-level trust)

### 2. `compile` — Build team wiki articles

```
wiki-team compile [--role <domain>] [--topic <topic>]
```

1. If `--role` specified, compile all topics for that domain
2. If `--topic` specified, compile only that topic
3. If neither, compile all team-tier topics
4. Invoke `kb-compile` with team-tier quality settings:
   - Evidence diversity ≥ 2 (relaxed vs company tier)
   - WIP markers allowed but flagged in compile output
   - Cross-references within domain topics encouraged
5. Run `kb-lint` on compiled topics with team-tier thresholds

### 3. `query` — Search team wiki by domain

```
wiki-team query --role <domain> "<question>"
```

1. Load topic list for the domain from `_wiki-registry.json`
2. Also check `_role-registry.json` for supplementary topic associations
3. Scope `kb-search` / `kb-query` to only those topics
4. Return results tagged with `[TEAM:<domain>]` provenance
5. If results are insufficient, suggest broadening to company wiki

### 4. `lint` — Team wiki health check

```
wiki-team lint [--role <domain>] [--topic <topic>]
```

1. Run `kb-lint` with team-tier thresholds:
   - Freshness: articles older than 14 days flagged as WARNING
   - Freshness: articles older than 60 days flagged as CRITICAL
   - Broken wikilinks within domain: CRITICAL
   - Cross-domain broken links: WARNING
2. Check team-specific policies:
   - Articles should have `tier: team` and `domain` in frontmatter
   - Flag articles with no updates in 30+ days as candidates for archival
3. Identify promotion candidates: articles referenced by 3+ other articles
   or cited by company-tier topics

### 5. `status` — Team wiki overview

```
wiki-team status [--role <domain>]
```

1. List topics for the domain with article counts and freshness
2. Show promotion candidates (articles flagged via `--promote` or auto-detected)
3. Show coverage gaps: topics with zero or very few articles
4. Compare against `_role-registry.json` recommended topics

### 6. `flag-promote` — Mark content for company promotion

```
wiki-team flag-promote --topic <topic> --article <article-path> [--reason <text>]
```

1. Validate the article exists and passes `kb-lint` with zero critical issues
2. Add `promotion_candidate: true` and `promotion_reason` to article frontmatter
3. Log to a promotion queue file: `knowledge-bases/_promotion-queue.json`
4. Notify that `wiki-promote` should be run to complete the promotion

## Domain Resolution

When `--role` is provided, the skill resolves topics via this priority:

1. `_wiki-registry.json` → `team.domains.<role>.topics` (canonical)
2. `_role-registry.json` → `<role>.topics` (supplementary, may include
   company topics for read access)
3. Union of both, deduplicated

When `--role` is omitted but `--topic` is provided, reverse-lookup the
domain from the registry.

## Provenance Rules

- All team wiki content carries `[TEAM:<domain>]` provenance tag
- Team content has medium trust level — suitable for domain operations
  but not authoritative for cross-team decisions
- When team content conflicts with company wiki, company wiki takes
  precedence (flag the conflict for resolution)
- Promotion to company tier requires explicit `wiki-promote` execution

## In-Progress Team Knowledge

Team wikis may contain WIP content that is not yet validated:

- WIP articles should include a `status: draft` or `status: review`
  frontmatter field
- WIP content is excluded from promotion candidates
- WIP content is included in team queries but tagged with `[DRAFT]`
  provenance to distinguish from confirmed knowledge

## Error Handling

| Error | Action |
|-------|--------|
| Topic not in team tier | Check if it's a company topic, suggest `wiki-company` |
| Role not recognized | List valid domains from registry |
| Topic not in specified domain | List topics for that domain |
| Article fails lint for promotion | Block promotion, show lint report |

## Integration Points

- **wiki-company**: Sibling skill for company-tier operations
- **wiki-promote**: Receives promotion flags and executes the promotion pipeline
- **ai-context-router**: Queries team wiki as the domain knowledge layer
- **_role-registry.json**: Maps roles to topics and recommended skills
- **kb-daily-build-orchestrator**: Can trigger team wiki compilation per domain
