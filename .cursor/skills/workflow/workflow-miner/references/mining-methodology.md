# Workflow Mining Methodology

Reference for the workflow-miner skill: Sequential Pattern Mining (SPM) adapted for LLM-based mining of Cursor agent transcripts.

---

## 1. SPM Algorithm Overview

### PrefixSpan (Simplified for LLM-Based Mining)

PrefixSpan discovers frequent sequential patterns without candidate generation. For in-prompt implementation without external libraries:

1. **Project**: For each frequent item, project the database to suffixes after that item
2. **Grow**: Extend patterns by appending items that appear in projected suffixes
3. **Prune**: Discard patterns with support below threshold

### Simplified Sliding-Window Approach

Since we cannot run true PrefixSpan in-prompt, use a practical approximation:

1. **Extract sequences** from each transcript (tool-call chains)
2. **Enumerate contiguous substrings** for window sizes 2..N (e.g. N=6)
3. **Count** each unique subsequence across sessions
4. **Filter** by minimum support
5. **Rank** by frequency × session value heuristic

**Example**: Sequence `[Read, Grep, StrReplace, Read]` produces:
- Length 2: `Read→Grep`, `Grep→StrReplace`, `StrReplace→Read`
- Length 3: `Read→Grep→StrReplace`, `Grep→StrReplace→Read`
- Length 4: `Read→Grep→StrReplace→Read`

---

## 2. Transcript JSONL Format

### Structure

Each line is a JSON object:

```json
{"role":"user","message":{"content":[{"type":"text","text":"<user_query>...</user_query>"}]}}
```

```json
{"role":"assistant","message":{"content":[
  {"type":"text","text":"..."},
  {"type":"tool_use","name":"Read","input":{"path":"/path/to/file"}},
  {"type":"tool_use","name":"Grep","input":{"pattern":"..."}}
]}}
```

### Fields

| Field | Description |
|-------|-------------|
| `role` | `"user"` or `"assistant"` |
| `message.content` | Array of content blocks |
| `content[].type` | `"text"` or `"tool_use"` |
| `content[].name` | Tool name when `type` is `"tool_use"` |
| `content[].input` | Tool arguments (optional for sequence extraction) |

### File Layout

```
~/.cursor/projects/<project-id>/agent-transcripts/<session-uuid>/<session-uuid>.jsonl
```

One JSONL file per session; each line is one message/event.

---

## 3. Tool-Call Sequence Extraction Logic

```python
def extract_tool_sequence(transcript_path: str) -> list[str]:
    sequence = []
    with open(transcript_path) as f:
        for line in f:
            obj = json.loads(line)
            if obj.get("role") != "assistant":
                continue
            for block in obj.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    sequence.append(block.get("name", "?"))
    return sequence
```

### Notes

- Preserve chronological order (first tool in session → last)
- Tools invoked in parallel within a turn appear in array order
- Empty sessions produce `[]`; skip or count as failed
- Unknown tool names: use `"?"` or the literal name if present

---

## 4. Support and Confidence Metrics

### Support

- **Definition**: Number of sessions containing the pattern (as a contiguous subsequence)
- **Minimum support**: Default 3 — pattern must appear in ≥3 sessions
- **Formula**: `support(P) = |{s ∈ S : P ⊑ sᴛᵢₘ}|` where `S` = sessions, `sᴛᵢₘ` = tool sequence of `s`, `⊑` = contiguous subsequence

### Confidence (Optional)

- **Definition**: For pattern `A → B`, confidence = P(B follows A in sessions containing A)
- **Use**: Filter spurious patterns; lower confidence may indicate noise
- **Formula**: `confidence(A→B) = support(A→B) / support(A)`

### Session Value (Heuristic)

- **1.0**: Session has ≥5 tool calls; last turn is assistant; no obvious error markers
- **0.5**: Shorter session or ambiguous completion
- **0.0**: Empty or malformed
- **Use**: Weight pattern score by avg session value of sessions containing it

---

## 5. Example Patterns and Interpretations

| Pattern | Interpretation | Suggested Workflow |
|---------|----------------|-------------------|
| `Read → Grep → StrReplace` | Code search and replace | code-search-and-replace |
| `WebSearch → Read → anthropic-docx` | Research and document | research-to-doc |
| `Grep → SemanticSearch → Read` | Locate then inspect | locate-and-inspect |
| `Read → StrReplace → ReadLints` | Edit and validate | edit-and-lint |
| `SemanticSearch → Grep → Read` | Semantic then exact search | semantic-then-exact |
| `Read → TodoWrite → Shell` | Plan then execute | plan-and-run |

### Pattern Naming Conventions

- Use kebab-case for workflow names
- Reflect the logical flow: `<action1>-<action2>-<result>`
- Prefer verbs that describe the step (read, search, replace, run)

### Filtering Low-Value Patterns

- Single-tool patterns (e.g. `Read` only): Usually too generic; consider excluding or raising min_support
- Very long patterns (>6 tools): Often session-specific; may split into sub-patterns
- Patterns dominated by one session: Check if one user/session skews results; consider per-user or per-project mining
