---
name: ai-learn
description: >-
  Knowledge ingestion router that classifies new information and routes it to
  MemKraft (personal memory) or LLM Wiki (team/company knowledge) based on
  content type, audience, and trust level. Ensures every piece of learned
  information is stored in the correct layer with proper provenance. Use when
  the user asks "ai learn", "remember this", "store this knowledge", "save
  this as policy", "learn this", "ai-learn", "AI 학습", "이거 기억해", "지식 저장", "이거
  정책으로", "배운 것 저장", "이거 팀 위키에", or wants to route new information to the
  appropriate knowledge layer. Do NOT use for session transcript extraction
  (use extract-sessions.py). Do NOT use for KB raw source ingestion (use
  kb-ingest). Do NOT use for bulk Wiki compilation (use kb-compile). Do NOT
  use for MemKraft Dream Cycle maintenance (use memkraft-dream-cycle).
---

# ai-learn — Knowledge Ingestion Router

Classifies incoming information and routes it to the correct knowledge layer:
- **Personal fact/preference/decision** → MemKraft (via `memkraft-ingest`)
- **Team-level knowledge** → Team Wiki (via `wiki-team`)
- **Company-wide policy** → Company Wiki (via `wiki-company`, requires approval)

## Output Language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Architecture

```
ai-learn (new information)
  │
  ├─→ Classification Engine
  │     ├─ Personal? → MemKraft (memkraft-ingest)
  │     ├─ Team?     → Team Wiki (wiki-team)
  │     └─ Company?  → Company Wiki (wiki-company, gated)
  │
  ├─→ Deduplication Check (ai-context-router search)
  │
  └─→ Confirmation + Provenance Tag Assignment
```

## Workflow

### Step 1: Content Classification

Classify the incoming information:

| Signal | Classification | Target |
|--------|---------------|--------|
| "I prefer", "my habit", "I decided" | Personal | MemKraft |
| "remember that I", past decision context | Personal | MemKraft |
| "our team does", domain-specific practice | Team | Team Wiki |
| "company policy", org-wide rule | Company | Company Wiki |
| Ambiguous | Ask user | — |

### Step 2: Deduplication

Search existing stores via `ai-context-router` to detect near-duplicates:
- If exact match exists: report and skip
- If partial overlap: present diff and ask user to merge or create new
- If no match: proceed to ingestion

### Step 3: Route to Target

**MemKraft route**:
```
memkraft-ingest --type <preference|decision|fact|unresolved>
  --content "<information>"
  --provenance "user-stated"
  --tier HOT
```

**Team Wiki route**:
```
wiki-team --domain <engineering|product|design|...>
  --action add
  --content "<information>"
```

**Company Wiki route** (requires confirmation):
```
wiki-company --action propose
  --content "<information>"
  --requires-approval true
```

### Step 4: Confirmation

```markdown
## ✅ 학습 완료

### 저장 위치
- **Layer**: {MemKraft | Team Wiki | Company Wiki}
- **Provenance**: {[PERSONAL] | [TEAM:<domain>] | [COMPANY]}
- **Type**: {preference | decision | fact | policy | unresolved}

### 저장된 내용
{stored content summary}

### 관련 기존 지식
- {any related entries found during dedup check}
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `content` | (required) | Information to store |
| `--target` | auto | Force target: `personal`, `team`, `company` |
| `--type` | auto | Content type: preference, decision, fact, policy, unresolved |
| `--domain` | auto | Team domain for team-tier routing |

## Integration

- **Upstream**: User invocation or other `ai-*` skills
- **Downstream**: `memkraft-ingest`, `wiki-team`, `wiki-company`
- **Dedup via**: `ai-context-router` search
- **Output**: Confirmation with provenance tag and storage location
