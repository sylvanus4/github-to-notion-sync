## Caption & Subtitle Formatter

Format transcripts into proper subtitle files (SRT, VTT) with line-break optimization, reading speed validation, timing alignment, and accessibility compliance.

### Usage

```
# From transcribee output
/subtitles "outputs/transcripts/interview.txt" --format srt

# From YouTube transcript
/subtitles "outputs/transcripts/youtube-defuddle.md" --format vtt

# Reformat existing SRT
/subtitles "existing-captions.srt" --max-cps 18 --max-cpl 38

# Plain text with duration
/subtitles "script.txt" --duration 180s --format both
```

### Workflow

1. **Ingest** — Accept transcript (timestamped, raw SRT/VTT, or plain text)
2. **Configure** — Set format, max CPS (20), max CPL (42), max lines (2), timing parameters
3. **Segment** — Split into subtitle blocks following sentence/clause/semantic boundaries
4. **Validate** — Check reading speed, line length, overlap, gaps, numbering
5. **Output** — Generate SRT/VTT file(s) with validation report

### Output

Subtitle file(s) in SRT/VTT format with generation summary (block count, duration, average CPS, validation results).

### Execution

Read and follow the `caption-subtitle-formatter` skill (`.cursor/skills/standalone/caption-subtitle-formatter/SKILL.md`).
