---
name: icarus-memory-fabric
description: >-
  Cross-session shared memory with decision-quality tagging and training data
  extraction. Write, recall, and search entries in a flat-file fabric
  directory with tiered quality labels (high/normal/low training_value).
  Auto-capture high-value decisions during sessions and export training pairs
  for model fine-tuning. Use when the user asks to "write to fabric", "recall
  from fabric", "search memory", "tag decision", "export training data",
  "fabric write", "fabric recall", "decision memory", "training pairs",
  "session memory", "패브릭 저장", "패브릭 검색", "결정 기록", "학습 데이터 추출", "세션 메모리",
  "icarus-memory-fabric", or wants shared memory with quality-tagged entries
  for training data extraction. Do NOT use for personal tiered memory (use
  memkraft). Do NOT use for company/team wiki (use wiki-company or wiki-team).
  Do NOT use for knowledge graph operations (use cognee). Do NOT use for
  session transcript search (use recall). Do NOT use for model training
  execution (use agent-succession-pipeline). Korean triggers: "패브릭", "결정 메모리",
  "학습 데이터", "세션 메모리", "품질 태깅".
---

# Icarus Memory Fabric — Decision-Quality Shared Memory

A flat-file shared memory system where every entry carries a quality tag for
potential use as training data. Agents write decisions, corrections, reviews,
and learnings; a retriever surfaces relevant entries; and an extractor produces
fine-tuning pairs.

Adapted from [esaradev/icarus-plugin](https://github.com/esaradev/icarus-plugin)'s
fabric memory system.

---

## Why Fabric

Existing memory systems (`recall`, `memkraft`, `cognee`) optimize for retrieval.
Fabric optimizes for **training data generation** — every entry is a potential
fine-tuning example. The key insight from Icarus: agents that tag their own
decision quality produce better training data than post-hoc annotation.

---

## Fabric Directory

```
~/fabric/
├── 2026-04-22-decision-rbac-casbin.md
├── 2026-04-22-correction-error-handling.md
├── 2026-04-21-review-api-design.md
├── 2026-04-21-learning-helm-override.md
├── 2026-04-20-note-meeting-summary.md
└── ...
```

Each entry is a markdown file with YAML frontmatter. The directory is set via
`FABRIC_DIR` environment variable (defaults to `~/fabric/`).

---

## Entry Schema

```yaml
---
type: decision          # decision | correction | review | learning | note | ticket
summary: "Chose Casbin for RBAC policy engine over OPA"
status: active          # active | superseded | archived
outcome: success        # success | failure | pending | mixed
training_value: high    # high | normal | low
verified: true          # human-verified entry
platform: cursor        # cursor | cli | api
agent: opus-4           # model that created the entry
project: ai-platform
tags: [rbac, architecture, backend]
review_of: ""           # links to entry being reviewed
revises: ""             # links to entry being superseded
created: 2026-04-22T09:30:00Z
session_id: "abc-123"
---

## Context
We needed a policy engine for fine-grained RBAC on the AI Platform API.

## Decision
Chose Casbin over OPA because:
1. Native Go library — no sidecar required
2. Built-in PostgreSQL adapter for policy storage
3. Simpler policy language for our team's experience level

## Alternatives Considered
- OPA/Rego: More powerful but steeper learning curve
- Custom middleware: Too fragile, no audit trail

## Consequences
- Need to add Casbin as a Go dependency
- Policy files live in `configs/rbac/`
- Must write adapter for our existing user/role tables
```

---

## Operations

### Write

Create a new fabric entry:

1. Determine entry type from context
2. Auto-detect `training_value`:
   - **high**: Contains a decision with clear alternatives considered, or a correction
     that prevented a real mistake
   - **normal**: Standard observations, notes, or learnings
   - **low**: Routine notes, session metadata, or uncertain entries
3. Write markdown file with YAML frontmatter
4. Return the file path

Decision detection heuristics (from Icarus):
- Text contains: "decided", "resolved", "completed", "fixed", "deployed",
  "shipped", "reviewed", "approved", "rejected"
- Entry links to another entry via `review_of` or `revises`

### Recall

Retrieve relevant entries for a query:

1. Parse query into tokens
2. Two-pass scoring:
   - **Pass 1**: Score ALL entries on keyword match, project, agent, recency, tier, type
   - **Pass 2**: Re-score top candidates with reference chain bonus
3. Return top-N entries within token budget

Scoring signals (weights from Icarus):
- Keyword match: 0.35
- Project match: 0.20
- Agent match: 0.10
- Recency (exponential decay, half-life 14 days): 0.15
- Tier (high > normal > low): 0.10
- Type (decision > correction > review > learning > note): 0.05
- Reference chain (links to/from other high-value entries): 0.05

### Search

Full-text search across all entries with optional filters:

```
fabric search "casbin policy" --type=decision --project=ai-platform --limit=5
```

### Auto-Capture

During sessions, automatically capture high-value decisions:

1. After each significant agent action, check if the response contains
   decision indicators (keywords from the detection heuristic)
2. If detected, extract the decision context and create a fabric entry
3. Default `training_value` to `normal`; promote to `high` if the decision
   involves architecture, data model, or security choices

### Session Scoring

At session end, evaluate the session's fabric contributions:

- Count entries written
- Average training_value
- Decision-to-note ratio
- Quality threshold: sessions with < 0.3 average value get a "low-value session" flag

---

## Training Data Extraction

The primary differentiator: fabric entries become fine-tuning pairs.

### Export Modes

| Mode | Filter | Use Case |
|------|--------|----------|
| `high-precision` | `training_value=high` AND `verified=true` | SFT with high-quality data |
| `normal` | `training_value` in (high, normal) | General fine-tuning |
| `high-volume` | All entries except `training_value=low` | Large-scale training |

### Pair Extraction

Each entry generates one or more training pairs:

- **Decision entries** → `(context + alternatives, chosen decision + reasoning)`
- **Correction entries** → `(original mistake, corrected approach)`
- **Review entries** → `(code/artifact, review feedback)`
- **Learning entries** → `(question/problem, discovered pattern)`

### Export Formats

```bash
# OpenAI format
fabric export --mode=high-precision --format=openai > training.jsonl

# HuggingFace format
fabric export --mode=normal --format=huggingface > dataset.jsonl

# Raw JSON (for custom pipelines)
fabric export --mode=high-volume --format=raw > raw.json
```

OpenAI format output:
```json
{"messages": [
  {"role": "user", "content": "We need a policy engine for RBAC. Options: Casbin, OPA, custom middleware. Evaluate."},
  {"role": "assistant", "content": "Chose Casbin over OPA because: 1. Native Go library — no sidecar required..."}
]}
```

---

## Integration with Other Skills

| Skill | Integration |
|---|---|
| `maestro-conductor` | Mission learnings and corrections stored in fabric |
| `agent-behavioral-principles` | Principle violations become correction entries |
| `agent-succession-pipeline` | Reads exported training pairs for fine-tuning |
| `memkraft` | Fabric entries can be promoted to MemKraft personal memory |
| `recall` | Fabric search complements transcript-based recall |
| `kb-ingest` | High-value entries can be ingested into team KB |

---

## Commands

| Command | Action |
|---------|--------|
| `fabric write` | Create a new fabric entry interactively |
| `fabric recall {query}` | Retrieve relevant entries |
| `fabric search {query}` | Full-text search with filters |
| `fabric export` | Export training pairs |
| `fabric stats` | Show fabric health metrics |
| `fabric verify {id}` | Mark an entry as human-verified |
| `fabric supersede {id}` | Mark an entry as superseded by a new one |
