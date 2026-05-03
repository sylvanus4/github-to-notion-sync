---
name: ai-brief
description: >-
  Morning briefing with provenance-tagged context from MemKraft (personal
  memory) and LLM Wiki (official knowledge). Extends ai-chief-of-staff with
  personal-first context assembly via ai-context-router. Produces structured
  briefings separating official policy from personal preferences and recent
  history. Use when the user asks for "ai brief", "ai briefing", "personal
  briefing", "morning brief with context", "ai-brief", "AI 브리핑", "개인 맞춤 브리핑",
  "맥락 포함 아침 브리핑", "AI 아침 브리핑", or wants a morning overview that blends
  personal memory with organizational knowledge. Do NOT use for Google
  Workspace-only briefing without MemKraft (use ai-chief-of-staff). Do NOT use
  for stock analysis briefing (use today or toss-morning-briefing). Do NOT use
  for general recall without briefing structure (use ai-recall). Do NOT use
  for calendar-only briefing (use calendar-daily-briefing).
---

# ai-brief — Personal Morning Briefing

Generates a provenance-tagged morning briefing that combines personal memory
(MemKraft) with official knowledge (LLM Wiki) and live data sources (Calendar,
Email). Every piece of information carries its source tag so the user can
distinguish personal context from organizational fact.

## Output Language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Architecture

```
ai-brief
  │
  ├─→ ai-context-router (query: "today's priorities and context")
  │     ├─ MemKraft: recent sessions, preferences, unresolved items
  │     └─ Wiki: relevant policies, runbooks, team knowledge
  │
  ├─→ calendar-daily-briefing (today's schedule)
  │
  ├─→ gmail-daily-triage (unread summary, if available)
  │
  └─→ Assemble provenance-tagged briefing
```

## Workflow

### Step 1: Context Assembly

Invoke `ai-context-router` with query: "today's priorities, recent decisions,
pending items, and relevant policies" with `--recency-boost true`.

### Step 2: Calendar & Email

Run `calendar-daily-briefing` for today's schedule.
Optionally check email via `gws-gmail` for unread count and urgent items.

### Step 3: Briefing Assembly

Assemble results into the standard provenance-tagged format:

```markdown
## 📋 오늘의 브리핑 — {YYYY-MM-DD}

### Official Knowledge (LLM Wiki)
- [COMPANY] <relevant company policies for today's meetings>
- [TEAM:engineering] <sprint deadlines, architecture decisions>

### Personal Context (MemKraft)
- [RECENT] <yesterday's key decisions and outcomes>
- [PREFERENCE] <working style preferences relevant to today>
- [UNRESOLVED] <open items carrying over from previous days>

### 일정
- {calendar events with preparation notes}

### 이메일 요약
- {urgent/important email count and highlights}

### Recommendation
Based on official priorities and your personal context:
1. {top priority with reasoning}
2. {second priority}
3. {items to defer}
```

## Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| Full | `ai-brief` (default) | Calendar + Email + MemKraft + Wiki |
| Quick | `ai-brief --quick` | MemKraft unresolved + Calendar only |
| Deep | `ai-brief --deep` | Full + gbrain/Cognee entity context |

## Integration

- **Upstream**: User invocation or `daily-am-orchestrator`
- **Core dependency**: `ai-context-router` for provenance-tagged context assembly
- **Downstream skills**: `calendar-daily-briefing`, `gmail-daily-triage`, `memkraft`
- **Output**: Structured Korean briefing with provenance tags
