## YouTube Transcript

Extract a YouTube video transcript as clean markdown with timestamps,
chapters, and speaker diarization via Defuddle.

### Usage

```
<youtube-url> [action]
```

### Actions

| Action | Description |
|--------|-------------|
| _(none)_ | Extract and display the transcript |
| save `<path>` | Extract and save to a local file |
| summarize | Extract and produce a Korean summary with key takeaways |
| to-slack `#channel` | Extract, summarize, and post to Slack (x-to-slack pipeline) |

### Examples

```
/youtube-transcript https://youtube.com/watch?v=abc123
/youtube-transcript https://youtu.be/abc123 save output/transcripts/talk.md
/youtube-transcript https://youtube.com/watch?v=abc123 summarize
/youtube-transcript https://youtube.com/watch?v=abc123 to-slack #research
```

### How It Works

This command delegates to the `defuddle` skill for transcript extraction
via `curl -s "https://defuddle.md/{youtube_url_without_protocol}"`.

For the `to-slack` action, it chains to the `x-to-slack` skill's
YouTube handler (Handler C) which uses the Defuddle-extracted transcript
to produce a rich 3-message Slack thread with timestamped key points.

### Supported URL Formats

- `https://youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://m.youtube.com/watch?v=VIDEO_ID`
- `https://www.youtube.com/watch?v=VIDEO_ID`

### Limitations

- Only works with YouTube URLs (for local files, use `transcribee`)
- Transcript availability depends on the video having captions enabled
- Speaker diarization quality is "pretty good" but not word-level accurate
- Chapter markers depend on the uploader setting them
