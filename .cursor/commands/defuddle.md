## Defuddle

Extract clean markdown content from any web page or YouTube video transcript, stripping ads, sidebars, and UI noise. For YouTube URLs, returns full transcripts with timestamps, chapters, and speaker diarization.

### Usage

```
<url> [action]
```

### Actions

| Action | Description |
|--------|-------------|
| _(none)_ | Extract and display the markdown content (or transcript for YouTube) |
| `save <path>` | Extract and save to a local file |
| `summarize` | Extract and summarize the content in Korean |
| `compare <url2>` | Extract two pages and compare key points |
| `transcript` | (YouTube only) Extract and display the full transcript with timestamps |

### Execution

Read and follow the `defuddle` skill (`.cursor/skills/defuddle/SKILL.md`) for the full workflow, API details, and error handling.

For standalone YouTube transcript workflows with Slack posting, see the `/youtube-transcript` command.

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

# Extract YouTube transcript
/defuddle https://youtube.com/watch?v=abc123 transcript

# Save YouTube transcript for research
/defuddle https://youtu.be/xyz789 save output/transcripts/talk.md

# Summarize a YouTube video in Korean
/defuddle https://youtube.com/watch?v=abc123 summarize
```
