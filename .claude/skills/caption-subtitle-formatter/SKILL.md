---
name: caption-subtitle-formatter
description: >-
  Format transcripts into proper subtitle files (SRT, VTT, TXT) with
  line-break optimization, reading speed validation (CPS limits), timing
  alignment, safe-area compliance, and multi-language support. Takes raw
  transcripts (from transcribee, defuddle, or pasted text) and produces
  broadcast-quality subtitle files. Use when the user asks to "create
  subtitles", "format SRT", "generate VTT", "make captions", "자막 만들어줘", "SRT
  파일", "VTT 생성", "자막 포맷", "subtitle formatting", "caption-subtitle-formatter",
  or wants properly formatted subtitle files from a transcript. Do NOT use for
  transcription (use transcribee). Do NOT use for social media captions/copy
  (use marketing-podcast-ops or content-repurposing-engine). Do NOT use for
  YouTube transcript extraction (use defuddle). Do NOT use for video script
  writing (use video-script-generator).
---

# Caption & Subtitle Formatter

Transform raw transcripts into broadcast-quality subtitle files with proper timing, line breaks, and accessibility compliance.

## When to Use

- A transcript (from transcribee, defuddle, or manual) needs to become subtitle files
- Existing SRT/VTT files need reformatting for compliance
- Video content needs captions for accessibility (WCAG, FCC, or platform requirements)
- Multi-language subtitles need consistent formatting
- Subtitle timing needs adjustment to match audio

## Workflow

### Step 1: Ingest Transcript

Accept input as:
- **transcribee output** — Timestamped transcript with speaker diarization
- **defuddle YouTube output** — Transcript with timestamps and chapters
- **Raw SRT/VTT file** — Existing subtitle file for reformatting
- **Plain text + timing info** — Text with approximate timestamps or video duration
- **Plain text only** — Text without timing (will generate estimated timing)

### Step 2: Configure Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| **Format** | SRT | Output format: SRT, VTT, or both |
| **Max CPS** | 20 | Maximum characters per second (reading speed limit) |
| **Max CPL** | 42 | Maximum characters per line |
| **Max lines** | 2 | Maximum lines per subtitle block |
| **Min duration** | 1.0s | Minimum display time per block |
| **Max duration** | 7.0s | Maximum display time per block |
| **Gap** | 0.08s | Minimum gap between consecutive blocks |
| **Language** | Auto-detect | Primary language of the content |
| **Speaker labels** | Off | Include speaker identification (for diarized input) |

### Step 3: Segment and Format

#### 3a: Text Segmentation

Split the transcript into subtitle blocks following these rules:

1. **Sentence boundaries** — Prefer breaking at sentence ends
2. **Clause boundaries** — If a sentence is too long, break at commas, conjunctions, or natural pauses
3. **Line length** — Each line ≤ Max CPL characters
4. **Lines per block** — Each block ≤ Max lines
5. **Semantic unity** — Keep related words together (don't split noun phrases, verb phrases)

**Line break hierarchy** (prefer higher over lower):
1. Period, question mark, exclamation mark
2. Comma, semicolon, colon
3. Conjunction (and, but, or / 그리고, 하지만)
4. Preposition phrase boundary
5. After 35+ characters if no other break point

#### 3b: Korean-Specific Rules

- Break AFTER particles, not before
- Keep subject + particle together on the same line
- Honorific endings stay with their verb
- Spacing rules per Korean orthography

#### 3c: Timing Assignment

If input has timestamps:
- Map text segments to existing timestamps
- Adjust boundaries to avoid mid-word cuts
- Ensure subtitle appears slightly before the audio (50-100ms lead)

If input has no timestamps:
- Estimate using speaking rate (~150 words/min EN, ~200 syllables/min KO)
- Distribute timing evenly with natural pauses at sentence boundaries
- Mark output as "ESTIMATED TIMING — sync with audio before use"

### Step 4: Validation

Run these checks on every subtitle block:

| Check | Rule | Action on Fail |
|-------|------|----------------|
| **Reading speed** | CPS ≤ Max CPS | Split block or extend duration |
| **Line length** | CPL ≤ Max CPL | Re-break the line |
| **Display duration** | Min ≤ duration ≤ Max | Adjust timing |
| **Overlap** | No temporal overlap between blocks | Add gap or adjust end time |
| **Gap** | Gap between blocks ≥ Min gap | Adjust timing |
| **Empty blocks** | No blank subtitle blocks | Remove empty blocks |
| **Numbering** | Sequential, starting from 1 | Renumber |

Report validation results:
```
## Validation Report
- Total blocks: [N]
- CPS violations fixed: [N]
- Line breaks adjusted: [N]
- Timing overlaps resolved: [N]
- Average CPS: [N]
- Max CPS: [N] (block #[N])
```

### Step 5: Output

Generate the subtitle file(s):

**SRT format:**
```
1
00:00:01,000 --> 00:00:04,500
First line of subtitle text
Second line if needed

2
00:00:04,600 --> 00:00:07,800
Next subtitle block

```

**VTT format:**
```
WEBVTT

00:00:01.000 --> 00:00:04.500
First line of subtitle text
Second line if needed

00:00:04.600 --> 00:00:07.800
Next subtitle block

```

Write the output file(s) to:
- Same directory as input file with `.srt` / `.vtt` extension, OR
- `outputs/subtitles/[source-name].[format]` if no input file path

Include a summary:

```markdown
## Subtitle Generation Summary

- **Source**: [input path or "pasted text"]
- **Format**: [SRT / VTT / both]
- **Language**: [detected language]
- **Total blocks**: [N]
- **Total duration**: [HH:MM:SS]
- **Average CPS**: [N]
- **Output file(s)**: [path(s)]
- **Timing**: [synced / estimated]

### Validation
- All checks passed: [Yes / No — details if No]
```

## Examples

### Example 1: Transcribee output to SRT

User: "이 transcribee 출력을 SRT 자막 파일로 만들어줘" + [transcript file]

Read the timestamped transcript, segment into 2-line blocks following Korean line-break rules, validate CPS at 20 max, generate sequential SRT with proper `HH:MM:SS,mmm` formatting, write to `outputs/subtitles/`.

### Example 2: YouTube transcript to VTT

User: "Convert this YouTube transcript to VTT format"

Use the defuddle-extracted timestamps, reformat into VTT with proper `HH:MM:SS.mmm` timing, apply 42 CPL line breaks, validate reading speed, output `.vtt` file.

### Example 3: Plain text to estimated-timing SRT

User: "I have this script text, create subtitles for a 3-minute video"

Calculate speaking rate from word count / 180 seconds, distribute timing across sentence boundaries, generate SRT with estimated timestamps, flag as "ESTIMATED TIMING" in output.

### Example 4: Reformat existing SRT

User: "This SRT file has lines that are too long and CPS is too high, fix it"

Read the existing SRT, re-segment long lines, split fast blocks into shorter ones, maintain original timing alignment, output corrected SRT with validation report showing before/after metrics.

## Error Handling

| Scenario | Action |
|----------|--------|
| Input has no timing information | Generate estimated timing based on word count and target duration; warn user |
| CPS cannot be reduced below max without changing content | Flag the block and suggest the speaker talks too fast in that segment |
| Input language not detected | Ask: "What language is this transcript in?" |
| Extremely long transcript (>60 min) | Process in chunks; maintain sequential numbering across chunks |
| Mixed languages in transcript | Apply the dominant language's rules; flag code-switched segments |
| Corrupt or malformed input SRT/VTT | Attempt recovery; report which blocks could not be parsed |

## Composability

- **reclip-media-downloader** — Download video files from URLs, then transcribe and format as subtitles
- **transcribee** — Transcribe audio/video first, then format as subtitles
- **defuddle** — Extract YouTube transcripts, then format as proper SRT/VTT
- **video-script-generator** — Generate script, then pre-generate subtitles from the script
- **video-editing-planner** — Include subtitle specifications in the editing plan
- **sentence-polisher** — Polish subtitle text before formatting (fix grammar in captions)
