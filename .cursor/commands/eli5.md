---
description: "Explain any topic in the simplest possible terms, as if to a 5-year-old — no jargon, only analogies and short sentences"
argument-hint: "<topic or text to simplify>"
---

# Explain Like I'm 5

Translate complex ideas into language a young child could understand. Strip all jargon, use everyday analogies, and keep sentences short.

## Usage

```
/eli5 How does HTTPS work?
/eli5 Kubernetes pod scheduling
/eli5 블록체인이 뭐야?
/eli5 What is a transformer model in machine learning?
/eli5 --visual How does DNS resolution work?
```

## Your Task

User input: $ARGUMENTS

### Mode Selection

Parse `$ARGUMENTS` for flags:

- **No flags** — Standard ELI5 explanation (default)
- `--visual` — Include an ASCII or Mermaid analogy diagram alongside the explanation
- `--compare` — Explain by comparing to something familiar (e.g., "it's like a library card...")
- `--story` — Frame the explanation as a short story with characters

### Workflow

1. **Parse topic** — Extract the concept to explain from `$ARGUMENTS`
2. **Identify complexity** — Determine which parts are hardest to simplify
3. **Strip jargon** — Replace every technical term with a plain-language equivalent
4. **Build analogy** — Find a concrete, physical-world analogy the concept maps onto (kitchen, playground, school, toys)
5. **Draft explanation** — Write in short sentences (max 12 words each), active voice, present tense
6. **Validate simplicity** — Re-read and remove any word a 5-year-old wouldn't know; if unavoidable, define it inline with "that means..."
7. **Add visual** (if `--visual`) — Create a simple ASCII diagram or Mermaid flowchart using the analogy
8. **Deliver** — Present the explanation in 2-3 short paragraphs max

### Output Format

```
## [Topic] — Like You're 5

[Analogy-based explanation in 2-3 paragraphs]

### The Simple Version
[One-sentence summary a child could repeat]
```

If `--visual` is set, append:
```
### Picture It
[ASCII or Mermaid diagram using analogy objects]
```

### Constraints

- No sentence longer than 15 words
- No technical terms without an inline "that means..." definition
- No acronyms
- Use "you" and "your" to keep it personal
- Prefer concrete nouns (box, pipe, letter) over abstract ones (protocol, architecture, layer)

### Execution

For complex technical topics, optionally reference the `adaptive-tutor` skill (`.cursor/skills/standalone/adaptive-tutor/SKILL.md`) using its Visual Thinking teaching mode for diagram generation.
