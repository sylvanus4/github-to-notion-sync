---
description: "Rewrite text in a specified style while preserving the original meaning — formal, casual, academic, journalistic, and more"
argument-hint: "<style> <text to rewrite>"
---

# Style Rewriter

Rewrite any text in a target style while preserving the original meaning. Includes a before/after comparison to verify no meaning drift.

## Usage

```
/rewrite-as formal Hey, the deploy broke again lol, can someone check?
/rewrite-as academic This study shows AI is getting better at coding
/rewrite-as casual The quarterly earnings exceeded analyst expectations by 12%
/rewrite-as journalistic Our platform processed 10M requests yesterday
/rewrite-as marketing We reduced latency by 40% through cache optimization
/rewrite-as legal 사용자 데이터를 서버에 저장합니다
/rewrite-as minimalist [paste verbose paragraph]
```

## Your Task

User input: $ARGUMENTS

### Workflow

1. **Parse style** — Extract the target style from the first token of `$ARGUMENTS`
2. **Extract source text** — Everything after the style token is the text to rewrite
3. **Analyze original** — Identify core meaning, key facts, and tone
4. **Apply style transformation** — Rewrite with the target style's vocabulary, sentence structure, and conventions
5. **Verify meaning preservation** — Compare original and rewritten versions; flag any meaning changes
6. **Polish** — Apply sentence-level refinements for natural flow

### Supported Styles

| Style | Characteristics |
|-------|----------------|
| `formal` | Professional, no contractions, complete sentences, passive voice acceptable |
| `casual` | Conversational, contractions, shorter sentences, direct address |
| `academic` | Scholarly, citations-ready, hedging language, passive constructions |
| `journalistic` | Inverted pyramid, lead with the news, active voice, quotes-ready |
| `poetic` | Metaphorical, rhythmic, evocative imagery |
| `technical` | Precise terminology, specification-like, unambiguous |
| `legal` | Defined terms, conditional clauses, liability-aware |
| `marketing` | Benefit-focused, action-oriented, emotional hooks |
| `conversational` | Friendly, first-person, question-and-answer flow |
| `dramatic` | High stakes, tension, vivid descriptions |
| `minimalist` | Shortest possible form, every word essential |
| `executive` | Bottom-line first, metrics-driven, action items |

### Output Format

```
## Rewritten ([style])

[Rewritten text]

### Meaning Check
- **Preserved:** [Core facts/meaning retained]
- **Changed:** [Any tone or nuance shifts — "None" if perfect preservation]
```

### Constraints

- Never alter factual content (numbers, names, dates, technical specifics)
- If the style conflicts with accuracy (e.g., marketing exaggeration), prioritize accuracy
- Preserve the original language (Korean input → Korean output, English → English)
- If the source text is a single sentence, output a single sentence

### Execution

Reference `prompt-transformer` (`.cursor/skills/standalone/prompt-transformer/SKILL.md`) for structural transformation patterns. Reference `sentence-polisher` (`.cursor/skills/standalone/sentence-polisher/SKILL.md`) for final-stage grammar and flow refinement.
