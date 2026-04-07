---
description: "Tailor the response to a specific audience's knowledge level, vocabulary, and concerns"
argument-hint: "<audience> <topic or question>"
---

# Audience-Adapted Response

Adapt vocabulary, depth, examples, framing, and action items to match a specific audience's knowledge level and concerns.

## Usage

```
/audience beginner How does Kubernetes work?
/audience executive Why should we invest in observability?
/audience investor Q3 revenue growth from AI features
/audience engineer Trade-offs of event-driven vs request-driven architecture
/audience non-technical What does our CI/CD pipeline do?
/audience student 머신러닝에서 편향-분산 트레이드오프란?
/audience designer Why does our API need pagination?
```

## Your Task

User input: $ARGUMENTS

### Workflow

1. **Parse audience** — Extract the audience type from the first token of `$ARGUMENTS`
2. **Parse topic** — Everything after the audience token is the topic or question
3. **Calibrate response:**
   - **Vocabulary** — Match the audience's technical fluency
   - **Depth** — Shallow overview vs. deep dive
   - **Examples** — Relatable to the audience's daily work
   - **Framing** — What this audience cares about (cost? usability? correctness? risk?)
   - **Action items** — What this audience should do with this information
4. **Generate response** — Consistent with the calibrated parameters
5. **Add audience-specific takeaway** — One sentence: "What this means for you as a [audience]"

### Audience Calibration

| Audience | Vocabulary | Depth | Cares About |
|----------|-----------|-------|-------------|
| `beginner` | No jargon, analogies | Surface | Getting started, not breaking things |
| `intermediate` | Some jargon, defined | Medium | Best practices, common pitfalls |
| `expert` | Full jargon | Deep | Edge cases, trade-offs, internals |
| `executive` | Business terms | High-level | ROI, risk, timeline, competitive advantage |
| `child` | Simple words, stories | Very surface | Fun, curiosity |
| `non-technical` | Zero jargon, metaphors | Surface | Impact on their work |
| `investor` | Financial terms | Medium | Growth, unit economics, moat |
| `engineer` | Technical terms | Deep | Implementation, performance, reliability |
| `designer` | Design terms | Medium | User experience, accessibility, consistency |
| `student` | Academic terms | Medium-deep | Understanding concepts, exam readiness |

### Constraints

- Never use jargon above the audience's level without immediately defining it
- For `executive` and `investor`: lead with the bottom line, then support
- For `beginner` and `child`: max 3 new concepts per response
- For `engineer`: include code or architecture diagrams when relevant
- If the topic genuinely requires more expertise than the audience has, bridge the gap explicitly
