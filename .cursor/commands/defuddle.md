## Defuddle

Extract clean markdown content from any web page, stripping ads, sidebars, and UI noise.

### Usage

```
<url> [action]
```

### Actions

| Action | Description |
|--------|-------------|
| _(none)_ | Extract and display the markdown content |
| `save <path>` | Extract and save to a local file |
| `summarize` | Extract and summarize the content |
| `compare <url2>` | Extract two pages and compare key points |

### Execution

Read and follow the `defuddle` skill (`.cursor/skills/defuddle/SKILL.md`) for the full workflow, API details, and error handling.

### Examples

```bash
# Extract a blog post
/defuddle https://stephango.com/file-over-app

# Save documentation as markdown
/defuddle https://docs.example.com/guide save docs/guide.md

# Extract and summarize in Korean
/defuddle https://openai.com/blog/some-post summarize

# Compare two articles
/defuddle https://blog.a.com/post compare https://blog.b.com/post
```
