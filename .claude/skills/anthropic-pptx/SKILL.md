---
name: anthropic-pptx
description: Create, read, edit PowerPoint presentations (.pptx) with layouts, speaker notes, and visual formatting.
disable-model-invocation: true
arguments: [operation, file_path]
---

Work with PowerPoint presentations: `$operation` on `$file_path`.

## Operations

| Operation | Description |
|-----------|-------------|
| create | Create new presentation |
| read | Extract content from existing .pptx |
| edit | Modify slides, content, or layout |
| merge | Combine multiple presentations |

## Slide Design Guidelines

- Max 6 bullets per slide
- One key message per slide
- Consistent color scheme throughout
- Speaker notes for every content slide
- Data visualization over text where possible

## Rules

- Use python-pptx for programmatic generation
- Include speaker notes in Korean
- Practical demos over abstractions
- Steve Jobs style for keynotes
- Include slide numbers
