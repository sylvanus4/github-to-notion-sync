---
name: sefo-plan-router
description: >-
  Run SEFO skill retrieval and DAG composition for plan-aware skill routing.
  Discovers the best skills for a task and generates execution phases with
  dependency ordering.
disable-model-invocation: true
---

# SEFO Plan Router

Run the SEFO (Skill Evolution and Federated Orchestration) plan router to discover the most relevant skills for a given task and automatically generate a dependency-ordered execution plan (DAG). Uses BM25 or Hybrid (BM25 + Dense) retrieval against the local `skill_corpus.json`, then builds a CompositionGraph from `composable_skills` edges to determine parallel execution phases.

## Prerequisites

- Python 3.11+ with `PyYAML` installed (`pip install pyyaml`)
- Optional: `rank_bm25` for optimized BM25 scoring (`pip install rank-bm25`); falls back to built-in TF-IDF if absent
- Corpus cached at `scripts/data/skill_corpus.json` (auto-built on first run with `--rebuild`)

## Workflow

### Step 1: Formulate the Task Query

Convert the user's request into a concise task description. This is the search query against the skill corpus.

Good queries:
- "daily stock analysis pipeline with report generation and Slack posting"
- "review PR, run security scan, and prepare release"
- "create PRD from meeting notes and publish to Notion"

Bad queries (too vague):
- "help me"
- "do something"

### Step 2: Run the Router

```bash
python scripts/sefo_plan_router.py "<task_description>" --top-k 10
```

**Options:**
| Flag | Default | Description |
|------|---------|-------------|
| `--top-k N` | 10 | Number of skills to return |
| `--method bm25\|hybrid` | hybrid | Retrieval method |
| `--rebuild` | false | Force rebuild `skill_corpus.json` from SKILL.md files |
| `--no-rebuild` | false | Use cached corpus only |
| `--corpus PATH` | auto | Custom corpus path |
| `--skills-dir PATH` | auto | Custom skills directory |
| `-v` | false | Verbose debug logging |

### Step 3: Interpret the Output

The script outputs JSON to stdout:

```json
{
  "query": "daily stock analysis pipeline",
  "corpus_size": 350,
  "results": [
    {
      "rank": 1,
      "skill_id": "today",
      "skill_name": "today",
      "score_method": "hybrid",
      "category": "pipeline",
      "composable_skills": ["weekly-stock-update", "daily-stock-check", "alphaear-news"],
      "description": "Run the daily data sync..."
    }
  ],
  "dag": {
    "phases": [
      {"phase": 1, "skills": ["weekly-stock-update", "alphaear-news"], "parallel": true},
      {"phase": 2, "skills": ["daily-stock-check"], "parallel": false},
      {"phase": 3, "skills": ["today"], "parallel": false}
    ],
    "mermaid": "graph TD\n    ...",
    "node_count": 4,
    "edge_count": 3
  }
}
```

**Key fields:**
- `results`: Skills ranked by relevance (higher rank = more relevant)
- `dag.phases`: Execution order — skills in the same phase can run in parallel
- `dag.mermaid`: Copy-pasteable Mermaid diagram for visual plans

### Step 4: Build the Plan

Use the SEFO output to structure a plan:

1. **Phase-ordered steps**: Each DAG phase becomes a plan step. Parallel skills within a phase can be delegated to concurrent subagents.
2. **Skill descriptions**: Use the `description` field to inform what each step does.
3. **Composable edges**: The `composable_skills` field shows known dependencies — if skill A lists skill B, A likely produces input that B consumes.
4. **Mermaid diagram**: Include in the plan for stakeholder visibility.

### Step 5: Present to User

Show the user:
1. The ranked skill list with brief descriptions
2. The Mermaid DAG diagram
3. The proposed phase-ordered execution plan
4. Ask for confirmation or adjustments

## Example Usage

```bash
# Default hybrid retrieval, top 10 skills
python scripts/sefo_plan_router.py "create a comprehensive code review with security and performance analysis"

# BM25 only, top 5 skills
python scripts/sefo_plan_router.py --method bm25 --top-k 5 "deploy Helm charts with validation"

# Force corpus rebuild after adding new skills
python scripts/sefo_plan_router.py --rebuild "morning pipeline with email triage and stock analysis"
```

## Constraints

- The router is **advisory** — the user always has final say on skill selection
- Anti-trigger filtering removes skills whose exclusion patterns match the query
- DAG edges come only from `composable_skills` declared in SKILL.md files; undeclared dependencies are not captured
- Dense retrieval falls back to Jaccard similarity if `sentence-transformers` is not installed
- The corpus must be rebuilt (`--rebuild`) after adding, removing, or modifying SKILL.md files

## Do NOT Use For

- Federation sync between SEFO instances (use `sefo-federation`)
- Trust/governance operations on skills (use `sefo-governance`)
- Full SADO API-based orchestration with the backend server (use `sefo-orchestrator`)
- Creating new skills (use `create-skill`)
- Optimizing existing skills (use `skill-optimizer`)
