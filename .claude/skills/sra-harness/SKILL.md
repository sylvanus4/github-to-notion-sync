---
name: sra-harness
description: >-
  SRA (Skill Retrieval Augmentation) 3-stage pipeline orchestrator with BM25
  index-backed retrieval via Python helper scripts. Task -> Retrieval ->
  Incorporation -> Application. Addresses skill-loading hallucination, zero
  need-awareness, and noise interference. Use when the user asks "SRA",
  "sra-harness", "스킬 검색 증강", "어떤 스킬을 써야 해?", "best skill for
  this task", "스킬 찾아줘", "SRA pipeline", "auto-find and use skills",
  "SRA orchestrate", "자동 스킬 파이프라인", "SRA 오케스트레이터",
  "스킬 자동 검색 + 실행", "find the right skill and run it", or when a complex
  task requires finding the optimal skill from 1000+ candidates. Do NOT use for
  direct skill invocation when the user already named the skill. Do NOT use for
  skill creation (use write-a-skill or anthropic-skill-creator). Do NOT use for
  skill index management only (use sra-skill-indexer). Do NOT use for skill
  search without execution (use sra-retriever). Do NOT use for SRA quality
  benchmarking (use sra-bench).
metadata:
  version: "2.0"
  category: workflow
  tags: [sra, orchestrator, pipeline, skill-retrieval-augmentation, harness]
---

# SRA Harness -- Skill Retrieval Augmentation Orchestrator

3-stage pipeline that finds, validates, and applies the right skill for a task.
Implements the SRA paradigm (arXiv:2604.24594) with BM25 index-backed retrieval.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   User Task                         │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  Stage 0: Index Check                               │
│  - Verify outputs/sra/skill_index.json exists       │
│  - If missing/stale → python scripts/sra/build_index.py │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  Stage 1: Skill Retrieval (sra-retriever)           │
│  - BM25 search via python scripts/sra/retrieve.py   │
│  - Return top-k candidates with scores              │
│  - Deduplicated by skill name                       │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  Stage 2: Skill Incorporation (sra-incorporator)    │
│  - Need-awareness check                             │
│  - Noise filter (Do-NOT-use exclusions)             │
│  - Strategy: Full Injection / LLM Selection /       │
│    Progressive Disclosure (based on token budget)    │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  Stage 3: Skill Application                         │
│  - Load verified skill → Execute → Evaluate         │
│  - Persist results to outputs/sra/runs/             │
└─────────────────────────────────────────────────────┘
```

## Sub-Skills

| Skill | Role |
|-------|------|
| `sra-skill-indexer` | Stage 0: Build BM25 index from all SKILL.md files |
| `sra-retriever` | Stage 1: Query-based top-k skill retrieval |
| `sra-incorporator` | Stage 2: Incorporation strategy selection |

## Stage 0: Index Freshness Check

```bash
ls -la outputs/sra/skill_index.json
```

If missing or older than 24h, rebuild:
```bash
python scripts/sra/build_index.py
```

## Stage 1: Retrieval (BM25 -> Top-K)

### 1a. BM25 Retrieval

```bash
python scripts/sra/retrieve.py "<USER_TASK_DESCRIPTION>" --top-k 7 --json
```

Parse JSON output. Results are deduplicated by skill name and sorted by BM25 score.

### 1b. Need-Awareness Check

Before proceeding, answer:

> "Can I complete this task using only native tools (Read, Edit, Bash, Grep, Agent)
> without any skill-specific workflow guidance?"

- **YES** -> Report: "Native reasoning sufficient. No skill needed." STOP.
- **NO** -> Continue to Stage 2.
- **UNSURE** -> List what the task requires that exceeds native capability. If empty, treat as YES.

## Stage 2: Incorporation (Refine / Adapt)

### 2a. Noise Filtering

For each candidate from Stage 1:
1. Read the skill's `Do NOT use for` section
2. Check if the current task falls under any exclusion
3. Check if the skill requires prerequisites not met (CLI tools, MCP servers)
4. Remove disqualified candidates

### 2b. Incorporation Strategy

Select based on token budget and candidate count:

| Condition | Strategy |
|-----------|----------|
| 1-2 candidates, budget ample | **Full Injection**: load complete SKILL.md |
| 3-5 candidates, budget moderate | **LLM Selection**: read descriptions, pick best 1-2 |
| 5+ candidates or tight budget | **Progressive Disclosure**: description-only -> load on demand |

### 2c. Progressive Disclosure Table

Present filtered candidates to the user:

```markdown
| Rank | Skill | BM25 Score | Why |
|------|-------|------------|-----|
| 1 | skill-name | 12.34 | [one-line reason] |
| 2 | skill-name | 8.21 | [one-line reason] |
```

If only 1 candidate with score >= 5.0, proceed automatically.

## Stage 3: Application (Reasoning & Acting)

### 3a. Load Skill

Invoke the selected skill via the Skill tool. Do NOT read SKILL.md directly.

### 3b. Execute

Follow the loaded skill's instructions exactly. The skill is now in control.

### 3c. Post-Execution Evaluation

| Criterion | Score (1-5) |
|-----------|-------------|
| Was the skill necessary? (vs native reasoning) | |
| Did the skill improve output quality? | |
| Were there unused skill sections? (noise) | |

If "Was the skill necessary?" scores 1-2, log as potential hallucination.

## Skill Gap Detection

When retrieval returns poor matches (all scores < 2.0):
1. Report: "No existing skill covers [specific capability]"
2. Suggest: "Consider creating a new skill with create-skill"
3. Log the gap query to `outputs/sra/gaps.log`

## Error Recovery

| Failure | Action |
|---------|--------|
| No candidates found | Ask user to rephrase, or offer create-skill |
| Index missing/stale | Run `python scripts/sra/build_index.py` |
| Selected skill fails to load | Fall back to next candidate |
| Skill prerequisites not met | Report missing dependencies, offer manual workflow |
| User rejects all candidates | Proceed with native reasoning |

## Constraints

- Maximum 3 full skill loads per pipeline run (token budget guard)
- If no skill scores above 2.0, report "no strong match" and suggest manual search
- Never skip Stage 2 -- even if only 1 skill is retrieved, run incorporation
- Persist pipeline execution log to `outputs/sra/runs/`

## Output Format

```
## SRA Pipeline Report

**Task**: <user's original task>

### Stage 1: Retrieval
| Rank | Skill | Score |
|------|-------|-------|
| 1 | skill-name | 12.34 |
| 2 | skill-name | 8.21 |

### Stage 2: Incorporation
- Strategy: LLM Selection
- Loaded: skill-name (full), skill-name (description-only)
- Token budget used: ~2500

### Stage 3: Application
<Skill execution output>

### Gaps Detected
- None / <description of missing capability>
```

## Integration

- **sra-skill-indexer**: Prerequisite -- builds the BM25 index
- **sra-retriever**: Sub-skill for Stage 1 query execution
- **sra-incorporator**: Sub-skill for Stage 2 strategy decision
- **sra-bench**: Quality evaluation of retrieval accuracy
- **skill-recommender**: Stack-aware pre-filtering before SRA retrieval
- **skill-guide**: Interactive human-driven discovery; SRA is automated
- **token-diet**: SRA reduces token waste by loading only verified skills
- **engineering-harness**: SRA can be Stage 0 of any harness
