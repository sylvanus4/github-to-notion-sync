---
name: selective-external-github-to-project-skills
description: >-
  Discover and selectively adopt skills from multiple sources: GitHub
  repositories, skills.sh directory, and well-known skill endpoints. Evaluates
  candidates on value, overlap, maintenance cost, and trigger collision risk
  before creating or updating SKILL.md files. Supports unified search across
  all sources in one command. Use when the user asks to "evaluate this repo
  for skills", "selective adopt", "search skills.sh", "discover skills", "find
  skills for X", "unified skill search", "well-known skills", "좋은 것만 반영", "외부
  깃헙 스킬 선별", "cherry-pick skills from repo",
  "selective-external-github-to-project-skills", "외부 레포 분석 후 선별 반영", "스킬 검색",
  "스킬 허브 검색", or shares an external GitHub URL, skills.sh query, or well-known
  endpoint URL with intent to adopt patterns selectively. Do NOT use for
  wholesale repo-to-skill conversion without selection (use skill-seekers). Do
  NOT use for syncing Anthropic KWP upstream (use kwp-sync). Do NOT use for
  .cursor/ asset sync across own repos (use cursor-sync). Do NOT use for
  creating a skill from scratch without an external source (use create-skill).
disable-model-invocation: true
---

# Selective External GitHub to Project Skills

Discover and selectively adopt skills from multiple sources into `.cursor/skills/`. Supports three discovery channels: GitHub repos, skills.sh directory, and well-known skill endpoints. Merge only justified pieces after scoring and de-duplication.

## Input

The user provides one of:
1. **GitHub URL** or repo identifier to evaluate
2. **skills.sh search query** — a keyword or phrase to search the skills.sh directory (e.g., "search skills.sh for code review", "skills.sh: deployment")
3. **Well-known endpoint URL** — a base URL to probe for `/.well-known/skills/index.json` (e.g., "check skills at https://example.com")
4. **Unified search query** — a keyword to search across ALL sources simultaneously (e.g., "find skills for testing", "unified search: observability")

Plus optional:
- **Intent** — "adopt all good patterns", "check if X is useful", specific area of interest
- **Scope** — skills only, rules only, both, or specific subdirectories

## Workflow

### Step 1: Source Discovery

Route based on input type:

#### 1A: GitHub Repository (default)
1. Clone or fetch the repo (read-only)
2. Summarize: purpose, license, scope, maintenance status, last commit date
3. Inventory artifacts: SKILL.md files, rules, commands, scripts, docs

#### 1B: skills.sh Directory Search
1. Query `https://skills.sh/api/search?q={query}` via WebFetch
2. If the API is unavailable, fall back to `WebSearch("site:skills.sh {query}")`
3. Parse results: extract skill name, description, source URL, author, install count
4. For each promising result, fetch the full skill definition from the listed source URL
5. Proceed to Step 2 with fetched skill definitions as artifacts

#### 1C: Well-Known Endpoint Discovery
1. Probe `{base_url}/.well-known/skills/index.json` via WebFetch
2. If the index exists, parse it: extract skill entries with name, description, version, download URL
3. For each entry, fetch the full SKILL.md content from the download URL
4. If `/.well-known/skills/index.json` returns 404, report "No skill index found at this endpoint" and stop
5. Proceed to Step 2 with fetched skill definitions as artifacts

#### 1D: Unified Search (all sources)
1. Run Steps 1A, 1B, and 1C in parallel:
   - 1A: `gh search repos "{query}" --limit 10` for GitHub repos containing SKILL.md files
   - 1B: skills.sh API search as described above
   - 1C: Probe a configurable list of well-known endpoints (default: empty; user can pass `--endpoints url1,url2`)
2. Deduplicate results by skill name across all sources
3. Merge into a unified candidate list with source attribution (GitHub / skills.sh / well-known)
4. Proceed to Step 2 with the merged list

### Step 2: Map to Local Needs

For each artifact, classify as:
- **New SKILL.md** — fills a documented gap in the local ecosystem
- **Update to existing skill** — strengthens triggers, adds patterns, or fixes gaps
- **Doc-only note** — useful reference but not a skill
- **Skip** — duplicates existing capability or out of scope

### Step 3: Score Candidates

| Dimension | Weight | Criteria |
|---|---|---|
| Value | 30% | Does it fill a real gap? Does it address a user correction pattern? |
| Overlap | 25% | Trigger collision risk with existing skills (check via Grep on descriptions) |
| Maintenance | 20% | Will it stay current? Does it depend on external APIs or tools we don't use? |
| Quality | 25% | Does it meet skill-upgrade-validator patterns? Is the prompt well-structured? |

Score each candidate 1-10 on each dimension. Weighted score >= 6.0 → recommend adoption.

### Step 4: Present Recommendations

Present a ranked table to the user:

```
| # | Artifact | Action | Score | Rationale |
|---|----------|--------|-------|-----------|
| 1 | skill-x  | ADD    | 8.2   | Fills gap in ... |
| 2 | skill-y  | UPDATE | 7.1   | Strengthens ... |
| 3 | skill-z  | SKIP   | 4.3   | Duplicates ... |
```

Wait for user approval before proceeding.

### Step 5: Apply Approved Items

1. For ADD: create SKILL.md using `create-skill` patterns, adapting to project conventions
2. For UPDATE: merge triggers/constraints into existing skill via `StrReplace`
3. Record skipped items with one-line rationale

### Step 6: Post-Adoption Quality Check

Run `skill-optimizer` audit on all touched skills to verify quality standards.

## Constraints

- Never adopt wholesale without evaluation — the default is selective
- De-duplicate triggers against all existing skills before adding
- Respect project rules: English SKILL bodies, explicit exports, no secrets
- Preserve the upstream license attribution in skill metadata if applicable
- Max 10 skills per adoption batch to keep review manageable

## Error Handling

| Error | Recovery |
|---|---|
| Repo inaccessible | Report URL issue, ask for alternative |
| License incompatible | Flag and skip affected artifacts |
| Trigger collision detected | Present conflict and ask user to resolve |
| Quality score below threshold | Skip with explanation, offer manual override |
| skills.sh API unreachable | Fall back to `WebSearch("site:skills.sh {query}")` |
| Well-known endpoint 404 | Report "No skill index found", suggest GitHub or skills.sh search |
| Unified search partial failure | Continue with sources that responded, note which failed |

## Examples

### Example 1: Evaluate an agent framework repo

User says: "이 레포에서 좋은 것들만 반영해줘: https://github.com/example/agent-skills"

Actions:
1. Clone and survey: 15 skills, MIT license, active maintenance
2. Map: 3 fill gaps, 2 overlap with existing, 10 out of scope
3. Score top 5, present ranked table
4. After approval, create 3 new SKILL.md files and update 1 existing

Result: 3 new skills added, 1 updated, 11 skipped with rationale

### Example 2: Cherry-pick specific patterns

User says: "이 레포의 eval 패턴만 우리 skill-optimizer에 반영할 수 있을지 봐줘"

Actions:
1. Focus on eval-related files only
2. Diff against existing skill-optimizer and skill-upgrade-validator
3. Identify 2 complementary patterns, score them
4. Merge approved patterns into existing skill

Result: 2 patterns merged into skill-upgrade-validator, quality verified

### Example 3: skills.sh directory search

User says: "skills.sh에서 code review 관련 스킬 찾아봐"

Actions:
1. Query `https://skills.sh/api/search?q=code+review` via WebFetch
2. Parse 6 results, fetch full definitions for top 4
3. Score against existing deep-review, simplify, code-review-all
4. 1 fills a gap (PR size analysis), 3 overlap
5. Present ranked table, adopt 1 after approval

Result: 1 new skill adopted from skills.sh, 3 skipped as redundant

### Example 4: Well-known endpoint discovery

User says: "check skills at https://acme-corp.dev"

Actions:
1. Probe `https://acme-corp.dev/.well-known/skills/index.json`
2. Index returns 8 skills, fetch full SKILL.md for each
3. Score: 2 relevant, 6 out of scope
4. Present candidates, adopt 1 after approval

Result: 1 skill adopted from well-known endpoint

### Example 5: Unified search

User says: "find skills for observability"

Actions:
1. Parallel search: GitHub repos (3 results), skills.sh (5 results), no well-known endpoints configured
2. Deduplicate: 2 appear in both GitHub and skills.sh
3. Score 6 unique candidates against existing monitoring-specialist, sre-devops-expert
4. 2 fill gaps, present ranked table

Result: 2 skills adopted from unified search (1 GitHub, 1 skills.sh)
