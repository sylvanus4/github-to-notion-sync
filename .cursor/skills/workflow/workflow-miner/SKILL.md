---
name: workflow-miner
description: >-
  Mine agent transcript files (.jsonl) to discover frequent workflow patterns
  using Sequential Pattern Mining (SPM). Use when the user asks to "mine
  workflows", "discover patterns", "workflow miner", "transcript mining",
  "워크플로우 마이닝", "패턴 발견", "세션 분석", "autoskill patterns", or wants to
  auto-synthesize optimized workflows from interaction traces. Do NOT use for
  creating skills from scratch (use create-skill), transcript reading for
  context recall (use recall), or general code review.
metadata:
  author: thaki
  version: "0.1.0"
  category: self-improvement
---

# Workflow Miner

Mines agent transcript files (.jsonl) to discover frequent workflow patterns using Sequential Pattern Mining (SPM). Based on AgentOS paper's concept of mining interaction traces to auto-synthesize optimized workflows.

## Instructions

### 1. Parse Agent Transcripts

- Source: transcript JSONL files under `/Users/hanhyojung/.cursor/projects/*/agent-transcripts/**/*.jsonl`
- Each line is a JSON object with `role` ("user" | "assistant") and `message.content` (array of blocks)
- Group events by session (one JSONL file per session)

### 2. Extract Tool-Call Sequences

- For each assistant message, iterate `message.content` and collect items with `type === "tool_use"`
- Extract `name` field (e.g. Read, Grep, WebSearch, StrReplace, Shell) to build ordered sequences
- Preserve order within a turn; concatenate across turns in temporal order
- Result: one sequence of tool names per session (e.g. `["Read","Read","Grep","StrReplace","Read"]`)

### 3. Find Frequent Subsequences (Simplified PrefixSpan)

- Use a sliding-window approach (no external SPM library)
- For window sizes 2..N (default N=6), enumerate all contiguous substrings from each session sequence
- Count frequency of each unique subsequence across all sessions
- A subsequence is frequent if its count ≥ minimum support (default: 3)
- See `references/mining-methodology.md` for algorithm details

### 4. Filter by Minimum Support

- Default `min_support = 3` (appears in at least 3 sessions)
- Configurable via `--min-support N`

### 5. Rank Patterns

- Score = frequency × avg_session_value
- Session value: 1.0 if session appears to complete (no abrupt end, reasonable length); 0.5 otherwise
- Heuristic: sessions with ≥5 tool calls and last turn from assistant → more likely successful
- Sort by score descending

### 6. Present Discovered Patterns

- Output a Markdown table with columns: Pattern (tool chain), Frequency, Example Session IDs, Suggested Workflow Name
- Suggest workflow name from pattern semantics (e.g. "Read → Grep → StrReplace" → "code-search-and-replace")

### 7. Optional: Create Workflow Definitions

- If user confirms patterns, optionally emit workflow definitions or skill compositions
- Output to `.cursor/skills/workflow-miner/outputs/` or suggest edits to existing workflow rules

## Output Format

```markdown
## Discovered Workflow Patterns

| Pattern | Frequency | Example Sessions | Suggested Workflow Name |
|---------|-----------|------------------|-------------------------|
| Read → Grep → StrReplace | 12 | abc-123, def-456 | code-search-and-replace |
| WebSearch → Read → anthropic-docx | 5 | ghi-789 | research-to-doc |
```

## Triggers

- "mine workflows"
- "discover patterns"
- "workflow miner"
- "transcript mining"
- "워크플로우 마이닝"
- "패턴 발견"
- "세션 분석"
- "autoskill patterns"

## Do NOT Use For

- Creating skills from scratch (use create-skill)
- Transcript reading for context recall (use recall)
- General code review
