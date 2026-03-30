# Output Structure

## Table of Contents

- [Directory Layout](#directory-layout)
- [transcript.txt](#transcripttxt)
- [metadata.json](#metadatajson)
- [transcript-raw.json](#transcript-rawjson---raw-flag-only)

## Directory Layout

Transcripts are saved to `~/Documents/transcripts/` in a self-organizing structure:

```
~/Documents/transcripts/
├── ai-research/
│   ├── ilya-sutskever-interview-2026-03-01/
│   │   ├── transcript.txt
│   │   └── metadata.json
│   └── anthropic-constitutional-ai-2026-02-15/
│       ├── transcript.txt
│       └── metadata.json
├── startups/
│   └── ycombinator-how-to-get-users-2026-01-20/
│       ├── transcript.txt
│       └── metadata.json
└── health/
    └── huberman-sleep-optimization-2026-02-10/
        ├── transcript.txt
        └── metadata.json
```

Categories are single-level, kebab-case folders. Claude analyzes existing categories and reuses them when semantically appropriate, or creates new ones.

## transcript.txt

Speaker-labeled dialogue format:

```
speaker_0: Welcome to the show. Today we're discussing...
speaker_1: Thanks for having me. I think the key insight is...
speaker_0: That's interesting. Can you elaborate on...
```

Speakers are identified by `speaker_0`, `speaker_1`, etc. via ElevenLabs diarization.

## metadata.json

```json
{
  "sourceUrl": "https://youtube.com/watch?v=...",
  "title": "Original Video Title",
  "date": "2026-03-01",
  "source": {
    "extractor": "youtube",
    "channel": "Channel Name",
    "uploader": "Uploader Name",
    "duration": 3600,
    "duration_string": "1:00:00",
    "description": "Video description...",
    "like_count": 12345,
    "comment_count": 678,
    "view_count": 98765,
    "thumbnail": "https://...",
    "upload_date": "20260301",
    "webpage_url": "https://..."
  },
  "theme": {
    "primaryTheme": "ai-research",
    "subTheme": "video-title-sanitized",
    "folderName": "ai-research",
    "confidence": "high",
    "summary": "Reasoning for category classification"
  },
  "transcription": {
    "language": "en",
    "confidence": 0.98,
    "wordsDetected": 15432
  }
}
```

### Source Fields by Input Type

| Field | URL Source | Local File |
|-------|-----------|------------|
| `extractor` | `youtube`, `instagram`, etc. | `local` |
| `channel` | Channel name | — |
| `duration` | From yt-dlp | From ffprobe |
| `view_count` | From yt-dlp | — |
| `webpage_url` | Original URL | `file://...` |

## transcript-raw.json (--raw flag only)

Full ElevenLabs API response including word-level data:

```json
{
  "words": [
    {
      "text": "Welcome",
      "start": 0.0,
      "end": 0.5,
      "type": "word",
      "speaker_id": "speaker_0"
    }
  ],
  "language_code": "en",
  "language_probability": 0.98
}
```

Each word includes start/end timestamps (seconds), type (`word`, `spacing`, `punctuation`), and speaker ID.
