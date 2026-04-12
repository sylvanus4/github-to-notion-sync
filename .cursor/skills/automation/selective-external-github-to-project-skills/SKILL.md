---
name: selective-external-github-to-project-skills
description: >-
  Evaluate external GitHub repositories for skills, patterns, or agent
  frameworks and selectively adopt only high-value items into the local skill
  ecosystem. Scores each candidate on value, overlap, maintenance cost, and
  trigger collision risk before creating or updating SKILL.md files. Use when
  the user asks to "evaluate this repo for skills", "selective adopt", "좋은
  것만 반영", "외부 깃헙 스킬 선별", "cherry-pick skills from repo",
  "selective-external-github-to-project-skills", "외부 레포 분석 후 선별
  반영", or shares an external GitHub URL with intent to adopt patterns
  selectively. Do NOT use for wholesale repo-to-skill conversion without
  selection (use skill-seekers). Do NOT use for syncing Anthropic KWP upstream
  (use kwp-sync). Do NOT use for .cursor/ asset sync across own repos (use
  cursor-sync). Do NOT use for creating a skill from scratch without an
  external source (use create-skill).
metadata:
  author: "autoskill-evolve"
  version: "1.0.0"
  category: "automation"
tags:
  - skills
  - governance
  - import
  - github
composes:
  - skill-optimizer
  - skill-upgrade-validator
  - create-skill
---

# Selective External GitHub to Project Skills

Assess external repositories (skills, agent platforms, tooling) for patterns worth adopting into `.cursor/skills/`, and merge only justified pieces after scoring and de-duplication.

## Input

The user provides:
1. **GitHub URL** or repo identifier to evaluate
2. **Intent** (optional) — "adopt all good patterns", "check if X is useful", specific area of interest
3. **Scope** (optional) — skills only, rules only, both, or specific subdirectories

## Workflow

### Step 1: Upstream Survey

1. Clone or fetch the repo (read-only)
2. Summarize: purpose, license, scope, maintenance status, last commit date
3. Inventory artifacts: SKILL.md files, rules, commands, scripts, docs

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
