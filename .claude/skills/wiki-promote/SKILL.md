---
name: wiki-promote
description: >-
  Promotion pipeline that moves validated team knowledge to the company wiki
  tier. Runs a multi-gate validation (lint, evidence check, cross-team
  relevance assessment, reviewer approval) before re-ingesting team articles
  into company topics with upgraded provenance. Manages the promotion queue,
  tracks promotion history, and handles rejection with feedback. Use when the
  user asks to "promote team content", "upgrade to company wiki", "wiki
  promote", "promote article", "팀 지식 승격", "회사 위키로 승격", "위키 프로모트",
  "wiki-promote", "promotion review", "승격 리뷰", "promotion queue", "승격 큐", or
  any request to move team-tier content to the company-tier wiki. Do NOT use
  for company wiki CRUD (use wiki-company). Do NOT use for team wiki CRUD (use
  wiki-team). Do NOT use for personal memory operations (use memkraft skills).
  Korean triggers: "팀 지식 승격", "회사 위키로 승격", "승격 큐", "승격 리뷰", "위키 프로모트".
---

# Wiki Promotion Pipeline

Moves validated team-tier knowledge to the company-tier wiki through a
structured review and quality gate process. Enforces the promotion rules
defined in `_wiki-registry.json`.

## Architecture Context

```
wiki-team                          wiki-company
(flag-promote)                     (ingest as company)
     │                                   ▲
     ▼                                   │
┌──────────────────────────────────────────┐
│              wiki-promote                │
│              (this skill)                │
│                                          │
│  ┌─────────┐  ┌──────────┐  ┌────────┐  │
│  │ Gate 1  │→ │ Gate 2   │→ │ Gate 3 │  │
│  │ Lint    │  │ Evidence │  │ Review │  │
│  │ Quality │  │ + Scope  │  │ Approval│  │
│  └─────────┘  └──────────┘  └────────┘  │
└──────────────────────────────────────────┘
```

## Modes

### 1. `review` — Run promotion gates on a candidate

```
wiki-promote review --topic <topic> --article <article-path>
```

Runs the full 3-gate validation pipeline:

**Gate 1: Quality Check (automated)**
1. Run `kb-lint` on the article with company-tier thresholds
2. Check frontmatter completeness: `tier`, `domain`, `promotion_candidate`
3. Verify zero critical lint issues
4. Check evidence diversity ≥ 3 (company standard)
5. Result: PASS / FAIL with details

**Gate 2: Scope & Relevance (automated + LLM)**
1. Check if the content is relevant across 2+ teams (cross-team utility)
2. Verify it is not time-sensitive data that will become stale
3. Confirm it is not personal opinion or in-progress content
4. Check against `_wiki-registry.json` `promotion_rules.prohibited` list
5. Score cross-team relevance (0-10); require ≥ 6 to pass
6. Result: PASS / FAIL with relevance score and reasoning

**Gate 3: Reviewer Approval (human-in-the-loop)**
1. Present Gate 1 + Gate 2 results to the user
2. Request explicit approval with reviewer name
3. If approved: proceed to promotion execution
4. If rejected: log rejection reason and mark article as `promotion_rejected`

### 2. `execute` — Perform the promotion

```
wiki-promote execute --topic <topic> --article <article-path> --reviewer <name>
```

Only runs after all 3 gates pass:

1. Determine the target company topic:
   - If `<topic>` is already a company topic, ingest directly
   - If it's a team topic, map to the closest company topic or create a
     new company topic if justified
2. Copy the article to `knowledge-bases/<company-topic>/raw/` with
   updated frontmatter:
   - `tier: company` (upgraded from `team`)
   - `promoted_from: <original-domain>/<original-topic>`
   - `promoted_date: <ISO date>`
   - `promoted_by: <reviewer>`
   - `reviewed_by: <reviewer>`
3. Run `wiki-company compile --topic <company-topic>` to recompile
4. Update `_promotion-queue.json`: mark entry as `promoted`
5. Update the original team article: add `promoted_to: <company-topic>`
   reference (the team copy remains as a domain-scoped view)

### 3. `queue` — View pending promotion candidates

```
wiki-promote queue [--role <domain>]
```

1. Read `knowledge-bases/_promotion-queue.json`
2. List all pending candidates with:
   - Source topic and domain
   - Date flagged
   - Promotion reason
   - Gate status (if review has been run)
3. If `--role` specified, filter to that domain's candidates

### 4. `history` — View promotion history

```
wiki-promote history [--since <date>]
```

1. Read `_promotion-queue.json` for entries with status `promoted` or `rejected`
2. Show: article, source domain, target company topic, reviewer, date, outcome
3. Useful for audit trail and tracking knowledge flow

### 5. `reject` — Explicitly reject a candidate

```
wiki-promote reject --topic <topic> --article <article-path> --reason <text>
```

1. Mark the article's `promotion_candidate` as `false`
2. Add `promotion_rejected: true`, `rejection_reason`, `rejection_date`
3. Update `_promotion-queue.json` with `rejected` status
4. Provide feedback to the team on what would need to change for
   future promotion (e.g., more evidence, broader relevance)

## Promotion Queue File

`knowledge-bases/_promotion-queue.json`:

```json
{
  "version": "1.0.0",
  "candidates": [
    {
      "id": "uuid",
      "source_domain": "engineering",
      "source_topic": "incident-history",
      "article_path": "wiki/post-mortems/2026-q1-outage.md",
      "flagged_date": "2026-04-15",
      "reason": "Cross-team relevance: affects ops, engineering, and support",
      "status": "pending",
      "gate1_result": null,
      "gate2_result": null,
      "gate3_reviewer": null,
      "promoted_to": null,
      "promoted_date": null,
      "rejection_reason": null
    }
  ]
}
```

## Promotion Rules Reference

From `_wiki-registry.json`:

**Requirements:**
- Content must be validated by at least 2 team members
- Must pass kb-lint with zero critical issues
- Must be relevant across 2+ teams or organization-wide
- Approval from a domain lead or wiki-promote review gate

**Prohibited:**
- In-progress or unverified content
- Personal opinions or preferences
- Time-sensitive data that will become stale

## Provenance Rules

- Promoted content receives `[OFFICIAL]` tag (upgraded from `[TEAM]`)
- Promotion lineage is preserved: `promoted_from` metadata tracks origin
- The team copy is annotated but NOT deleted — it serves as a
  domain-scoped reference pointing to the company article
- If the company article is later updated, the team reference should
  link to the latest company version

## Error Handling

| Error | Action |
|-------|--------|
| Article fails Gate 1 (lint) | Show lint report, block promotion |
| Article fails Gate 2 (scope) | Show relevance score, suggest improvements |
| Gate 3 rejected by reviewer | Log rejection, provide feedback |
| Target company topic unclear | Suggest closest match or propose new topic |
| Article already promoted | Skip with dedup notice |
| Promotion queue file missing | Create with empty candidates array |

## Integration Points

- **wiki-team**: Flags candidates via `flag-promote` mode
- **wiki-company**: Receives promoted content via `ingest` mode
- **kb-lint**: Quality gate for Gate 1
- **ai-context-router**: Uses promotion metadata to track knowledge lineage
- **kb-daily-build-orchestrator**: Can trigger batch promotion reviews
