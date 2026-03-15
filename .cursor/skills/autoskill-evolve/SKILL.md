---
name: autoskill-evolve
description: >-
  End-to-end skill evolution pipeline: extract candidates from agent transcripts,
  judge each against existing skills, apply add/merge/discard. Use when the user
  asks to "evolve skills", "run autoskill evolution", "mine sessions for skills",
  "autoskill evolve", "스킬 진화", "세션 기반 스킬 진화", "transcripts to skills",
  or when triggered by /autoskill-evolve. Do NOT use for creating skills
  manually (use create-skill), auditing skills (use skill-optimizer), or
  recalling session context (use recall).
metadata:
  author: thaki
  version: "0.2.0"
  category: self-improvement
---

# AutoSkill Evolve

End-to-end skill evolution pipeline that extracts reusable skill candidates from agent transcripts, judges each against the existing skill ecosystem, and applies add/merge/discard decisions. Optionally mines workflow patterns, composes workflow-type skills, validates security, and tracks intent alignment. Orchestrates autoskill-extractor, autoskill-judge, autoskill-merger, workflow-miner, skill-composer, semantic-guard, and intent-alignment-tracker.

## Instructions

### Pipeline Overview

```
Transcripts → [Mine Patterns] → Extract → Judge → [Compose/Merge] → Guard → Report (+IA)
```

### Step 1: Scope Selection

Determine which transcripts to process based on the `--scope` flag:

- `recent` (default): Process the 5 most recent transcripts not yet indexed
- `all`: Process all unindexed transcripts (use with caution)
- `session <uuid>`: Process a specific session transcript

Track processed transcripts in `.cursor/hooks/state/autoskill-evolution.json`:
```json
{
  "last_processed": "2026-03-14T10:00:00Z",
  "processed_transcripts": ["uuid1", "uuid2"],
  "evolution_count": 42,
  "skills_created": 12,
  "skills_merged": 28,
  "skills_discarded": 15
}
```

### Step 1.5: Pattern Discovery (workflow-miner, optional)

When `--with-mining` is set:
1. Read `.cursor/skills/workflow-miner/SKILL.md` and run mining on the same transcript scope
2. Collect discovered frequent tool-call patterns (frequency >= 3)
3. Pass patterns as extraction hints to Step 2 via `--hint "workflow patterns: ..."`
4. This helps autoskill-extractor identify multi-step workflow candidates that pure text analysis might miss

### Step 2: Extract (autoskill-extractor)

For each transcript in scope:
1. Read the SKILL.md at `.cursor/skills/autoskill-extractor/SKILL.md`
2. Run extraction following the instructions
3. Collect all candidates with confidence >= 0.6
4. Maximum 2 candidates per transcript

### Step 3: Judge (autoskill-judge)

For each extracted candidate:
1. Read the SKILL.md at `.cursor/skills/autoskill-judge/SKILL.md`
2. Search existing skills for similarity using hybrid retrieval
3. Apply decision logic: add, merge, or discard
4. Record decision with reasoning

### Step 4: Apply Decisions

For `add` decisions:
1. **Classify candidate type**: Check if the candidate describes a multi-step workflow
   (3+ sequential skill/tool references, trigger conditions like "whenever/after/before")
2. **If workflow type**: Read `.cursor/skills/skill-composer/SKILL.md` and use it to generate
   a proper workflow skill with sequential/parallel patterns, input/output contracts, and
   error recovery — instead of a plain SKILL.md
3. **If single skill type**: Create a new skill directory in `.cursor/skills/<name>/` and
   write SKILL.md with proper frontmatter and body
4. Optionally run `skill-optimizer` audit on the new skill

For `merge` decisions:
1. Read the SKILL.md at `.cursor/skills/autoskill-merger/SKILL.md`
2. Perform the merge following merger instructions
3. Bump version in the target skill
4. Record merge changelog

For `discard` decisions:
1. Log the discard reason
2. No file changes

### Step 4.5: Security Validation (semantic-guard)

Before writing any new or merged skill to `.cursor/skills/`:
1. Read `.cursor/skills/semantic-guard/SKILL.md` and scan the candidate content
2. Check for: prompt injection patterns, sensitive data, unsafe instructions
3. **SAFE**: Proceed with writing
4. **WARNING**: Log warning in evolution report, proceed with caution flag
5. **BLOCKED**: Do NOT write the skill. Log in discarded candidates with reason "security-blocked"

### Step 5: Generate Evolution Report

Create a markdown report at `outputs/autoskill-reports/<date>-evolution.md`:

```markdown
# Skill Evolution Report — YYYY-MM-DD

## Summary
- Transcripts processed: N
- Candidates extracted: M
- Skills added: A (workflow-type: W, single-type: S)
- Skills merged (updated): U
- Skills discarded: D
- Security blocked: B

## Added Skills
| Name | Type | Description | Confidence | Source |
|------|------|-------------|------------|--------|

## Merged Skills
| Target Skill | Version Change | Changes | Source |
|-------------|----------------|---------|--------|

## Discarded Candidates
| Name | Reason | Confidence |
|------|--------|------------|

## Security Validation Results
| Skill | Status | Details |
|-------|--------|---------|

## Intent Alignment Feedback
- Sessions with lowest IA scores (candidates for next evolution run)
- Newly created skills: IA baseline = "pending first use"
- Skills merged this run: previous IA score → mark for re-evaluation
```

When `--ia-priority` is set, sort transcripts by associated IA score (lowest first)
so the evolution focuses on improving the weakest skills.

### Step 6 (Optional): Post to Slack

If `--slack` flag is set, post the evolution summary to `#효정-할일` channel.

### Flags

- `--scope recent|all|session <uuid>`: Transcript selection (default: recent)
- `--dry-run`: Show what would happen without making changes
- `--auto-optimize`: Run `skill-optimizer` audit on all created/merged skills
- `--slack`: Post summary to Slack
- `--hint "focus"`: Pass extraction hint to `autoskill-extractor`
- `--with-mining`: Run workflow-miner pattern discovery before extraction (Step 1.5)
- `--ia-priority`: Sort transcripts by IA score (lowest first) to focus on weakest skills

### Safety Guards

- Never process the same transcript twice (tracked in state file)
- Maximum 2 candidates per transcript (prevents skill spam)
- Minimum confidence 0.6 for extraction
- Human review flag for merge conflicts
- Dry-run mode for previewing changes
