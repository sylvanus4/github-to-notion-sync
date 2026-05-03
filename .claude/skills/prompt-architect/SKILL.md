---
name: prompt-architect
description: Analyze and restructure prompts using 8 research-backed frameworks — CO-STAR, RISEN, RISE-IE, RISE-IX, TIDD-EC, RTF, Chain of Thought, Chain of Density.
arguments: [prompt_text]
---

Analyze and optimize the prompt: `$prompt_text`.

## Frameworks

| Framework | Best For |
|-----------|----------|
| CO-STAR | General-purpose structured prompts |
| RISEN | Role-based task execution |
| RISE-IE | Information extraction |
| RISE-IX | Index and classification |
| TIDD-EC | Complex multi-step reasoning |
| RTF | Role-Task-Format simple prompts |
| CoT | Step-by-step reasoning |
| CoD | Progressive summarization |

## Process

1. **Analyze**: Score current prompt quality (1-10) across clarity, specificity, structure
2. **Recommend**: Suggest best framework based on task type
3. **Clarify**: Ask targeted questions to fill gaps
4. **Restructure**: Apply selected framework
5. **Score**: Compare before/after quality

## Output

```markdown
## Prompt Analysis
- Current Score: [X/10]
- Recommended Framework: [name]
- Key Improvements: [list]

## Optimized Prompt
[Restructured prompt text]

## Quality Comparison
| Dimension | Before | After |
|-----------|--------|-------|
| Clarity | X/10 | Y/10 |
| Specificity | X/10 | Y/10 |
| Structure | X/10 | Y/10 |
```
