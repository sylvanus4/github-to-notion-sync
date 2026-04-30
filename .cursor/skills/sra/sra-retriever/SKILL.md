---
name: sra-retriever
description: Retrieve the top-k most relevant skills from the BM25 index for a given natural-language task description. Supports re-ranking and relevance scoring. Implements SRA Stage 1 (Skill Retrieval).
metadata:
  version: "1.0"
  category: automation
  tags: [sra, retrieval, bm25, skill-search]
---

# SRA Skill Retriever

Implements **Stage 1 (Skill Retrieval)** of the SRA paradigm (arXiv:2604.24594).

## Role

You are a skill retrieval engine. Given a user's task description or problem statement,
you query the BM25 skill index and return the most relevant skills ranked by score.
Optionally apply LLM-based re-ranking to improve precision.

## When to Use

Use when the user asks to "find skills for task", "retrieve skills", "SRA retrieve",
"sra-retriever", "which skill should I use for", "스킬 검색", "SRA 리트리버",
"적합한 스킬 찾기", "skill search for task", or when sra-orchestrator delegates retrieval.

Do NOT use for building/rebuilding the index (use sra-skill-indexer).
Do NOT use for interactive skill browsing without a task query (use skill-guide).
Do NOT use for deciding how to incorporate skills (use sra-incorporator).

## Constraints

- Requires `outputs/sra/skill_index.json` to exist (run sra-skill-indexer first if missing)
- Default top-k is 5; configurable via `--top-k`
- BM25 parameters: k1=1.2, b=0.75 (standard values)
- Re-ranking is optional and adds latency

## Workflow

### Basic Retrieval

```bash
python scripts/sra/retrieve.py "deploy a GPU workload on Kubernetes" --top-k 5
```

### JSON Output (for piping to sra-incorporator)

```bash
python scripts/sra/retrieve.py "deploy a GPU workload on Kubernetes" --top-k 5 --json
```

### LLM Re-ranking (optional, within this skill's judgment)

After BM25 retrieval returns top-k candidates, optionally re-rank by:
1. Reading each candidate's description
2. Scoring relevance to the original query on a 1-5 scale
3. Re-ordering by relevance score

Use re-ranking when:
- BM25 top-1 score is < 3.0 (weak signal)
- Multiple candidates have similar BM25 scores (ambiguous)
- The query uses domain-specific terminology that BM25 may not capture

## Output Format

**Table mode** (default): Human-readable ranked list with scores
**JSON mode** (`--json`): Machine-readable array for pipeline consumption

```json
[
  {
    "id": "k8s-deployment-creator",
    "name": "k8s-deployment-creator",
    "path": "/path/to/SKILL.md",
    "description": "Generate production-grade Kubernetes workload manifests...",
    "score": 12.34
  }
]
```

## Verification

- At least 1 result returned for non-trivial queries
- Results are sorted by descending score
- Each result has valid `id`, `path`, and `score > 0`
