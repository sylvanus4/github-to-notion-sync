---
description: "Answer in the shortest possible form — no filler, no caveats, just the answer (under 100 words)"
argument-hint: "<question>"
---

# Ultra-Concise Mode

The shortest correct answer. No filler, no caveats, no hedging. Just the answer.

## Usage

```
/briefly What's the difference between gRPC and REST?
/briefly When should I use useCallback vs useMemo?
/briefly Best Python library for PDF manipulation
/briefly Go에서 goroutine leak 방지하는 방법
/briefly Difference between ACID and BASE
```

## Your Task

User input: $ARGUMENTS

### Workflow

1. **Parse question** — Identify what's being asked
2. **Generate the shortest correct answer** — Direct, no preamble
3. **Strip all qualifiers** — Remove "it depends", "generally speaking", "in most cases"
4. **Format:**
   - If answerable in one sentence → one sentence
   - If a list is needed → max 5 bullet points, each under 10 words
   - If a comparison → 2 columns, no prose
5. **Verify correctness** — Brevity must not sacrifice accuracy

### Constraints

- Total output must be under 100 words
- No introductions ("Great question!")
- No conclusions ("Let me know if you need more!")
- No caveats unless the answer is genuinely dangerous without them
- If the question is too complex for a brief answer, say "Too complex for /briefly — try /step-by-step or /chain-of-thought" in one line
