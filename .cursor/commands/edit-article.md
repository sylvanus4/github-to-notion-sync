## Edit Article

Deep-edit articles by restructuring sections, cutting filler, sharpening arguments, and improving flow — far beyond grammar cleanup.

### Usage

```
/edit-article docs/blog/my-draft.md
/edit-article --cut-target 30% docs/posts/verbose-post.md
/edit-article "paste article text here"
```

### Workflow

1. **Diagnose** — Read the full article and score structure, density, clarity, and tone
2. **Restructure** — Propose section reordering, merges, and removals
3. **Tighten** — Cut filler, sharpen each paragraph's point, fix transitions
4. **Polish** — Verify thesis clarity, heading accuracy, and produce a change summary

### Execution

Read and follow the `edit-article` skill (`.cursor/skills/standalone/edit-article/SKILL.md`) for the full 4-phase editing workflow.

### Examples

Edit a blog draft:
```
/edit-article docs/blog/ai-platform-launch.md
```

Cut an article by 30%:
```
/edit-article --cut-target 30% docs/posts/long-technical-guide.md
```
