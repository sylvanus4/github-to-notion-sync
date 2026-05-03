---
name: ai-recall
description: >-
  Enhanced cross-session recall with MemKraft-first search and Wiki fallback.
  Replaces direct recall usage with provenance-tagged results that clearly
  separate personal memory from official knowledge. Uses ai-context-router for
  weighted RRF merging across all knowledge layers. Use when the user asks "ai
  recall", "remember with context", "what did I decide", "recall with
  provenance", "ai-recall", "AI 리콜", "맥락 포함 회상", "이전 결정 확인", "프로비넌스 포함 검색",
  "뭐였더라", "이전에 어떻게 했지", or wants to search personal and official memory with
  source attribution. Do NOT use for raw session transcript search without
  provenance (use recall). Do NOT use for Wiki-only search (use kb-query or
  kb-search). Do NOT use for web search (use WebSearch or
  parallel-web-search). Do NOT use for codebase search (use Grep or
  SemanticSearch).
---

# ai-recall — Provenance-Tagged Memory Search

Enhanced recall that searches MemKraft first (personal memory, preferences,
unresolved items) then falls back to LLM Wiki (official knowledge), merging
results with provenance tags so the user can distinguish "what I decided" from
"what the company policy says."

## Output Language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Architecture

```
ai-recall (query)
  │
  └─→ ai-context-router
        ├─ MemKraft (1.5× weight): topics, preferences, unresolved, sessions
        ├─ Wiki (1.0× weight): company-tier, team-tier
        └─ Deep backends (0.8× weight, optional): gbrain, Cognee
        │
        ▼
      Provenance-tagged results with RRF ranking
```

## Workflow

### Step 1: Query Enhancement

Enhance the user's query for better recall coverage:
- Extract key entities and time references
- Identify whether the query is personal, factual, or hybrid
- Add temporal context if the user references "yesterday", "last week", etc.

### Step 2: Context Assembly

Invoke `ai-context-router` with the enhanced query.
Default settings: `--recency-boost true`, `--top-n 10`.

For personal-only queries (e.g., "what did I decide"), add `--personal-only`.
For policy lookups, let the router handle both layers.

### Step 3: Result Presentation

Present results in the standard provenance-tagged format:

```markdown
## 🔍 검색 결과: "{original query}"

### Official Knowledge (LLM Wiki)
- [COMPANY] <matching company wiki content>
- [TEAM:<domain>] <matching team wiki content>

### Personal Context (MemKraft)
- [RECENT] <matching session history>
- [PREFERENCE] <relevant personal preferences>
- [UNRESOLVED] <related open questions>

### Sources
- MemKraft: N results (HOT: X, WARM: Y)
- Wiki: N results (company: X, team: Y)

### Recommendation
Based on the retrieved context:
- <synthesis of what was found, highlighting any conflicts between
  personal decisions and official policy>
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `query` | (required) | Natural language recall query |
| `--personal-only` | false | MemKraft only, skip Wiki |
| `--wiki-only` | false | Wiki only, skip MemKraft |
| `--deep` | false | Include gbrain/Cognee |
| `--time-range` | all | Filter by recency (24h, 7d, 30d, all) |

## Integration

- **Upstream**: User invocation or other `ai-*` skills
- **Core dependency**: `ai-context-router` for provenance-tagged search
- **Wraps**: `recall` (session search), `kb-search` (wiki search), `memkraft` (personal memory)
- **Output**: Provenance-tagged Korean results with source attribution
