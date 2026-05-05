# Audio Processing Agent

Orchestrate audio and video processing workflows: transcription with speaker diarization, lip sync video generation, subtitle formatting, media downloading, and video production pipelines. Routes audio/video tasks through the optimal processing chain.

## When to Use

Use when the user asks to "transcribe audio", "audio processing", "generate video", "lip sync", "create subtitles", "download video", "오디오 처리", "트랜스크립션", "립싱크", "자막 생성", "audio-processing-agent", or needs audio/video transcription, generation, or post-production workflows.

Do NOT use for text-only content creation (use content-creation-agent). Do NOT use for image generation without video (use vision-language-agent). Do NOT use for meeting transcript analysis (use meeting-digest).

## Default Skills

| Skill | Role in This Agent | Invocation |
|-------|-------------------|------------|
| transcribee | Transcribe YouTube/Instagram/TikTok/local files with speaker diarization | Audio/video transcription |
| muapi-lipsync | Lip-synced talking-head videos from portrait + audio (9 models) | Lip sync generation |
| pika-text-to-video | T2V/I2V via Pika v2.2 with 7 modes including effects | Video generation |
| caption-subtitle-formatter | SRT/VTT/TXT with reading speed validation and timing alignment | Subtitle formatting |
| reclip-media-downloader | Download from 1000+ sites via yt-dlp with format selection | Media acquisition |
| video-compress | FFmpeg-based compression with optimized presets | Video optimization |
| video-script-generator | Structured scripts with hooks, B-roll cues, and CTAs | Script creation |
| pika-video-pipeline | End-to-end: script -> generate -> post-production -> distribute | Full video pipeline |

## MCP Tools

None (CLI-based processing tools).

## Workflow

```mermaid
flowchart TD
    A[Audio/Video Request] --> B{Task?}
    B -->|Transcribe| C[transcribee]
    B -->|Generate video| D[pika-text-to-video / pika-video-pipeline]
    B -->|Lip sync| E[muapi-lipsync]
    B -->|Subtitles| F[caption-subtitle-formatter]
    B -->|Download media| G[reclip-media-downloader]
    B -->|Compress| H[video-compress]
    C --> I[Output: Transcript/Video/Subtitles]
    D --> I
    E --> I
    F --> I
    G --> I
    H --> I
```

## Modes

- **transcribe**: Audio/video to text with speaker diarization
- **generate**: Text/image to video via Pika
- **lipsync**: Portrait + audio to talking-head video
- **subtitle**: Format transcripts into broadcast-quality subtitles
- **pipeline**: Full script-to-distribution video production

## Safety Gates

- Subtitle CPS (characters per second) limits enforced for readability
- Video compression quality validation before delivery
- Media downloads respect content licensing (user responsibility noted)
- Large video generation requests include cost/time estimates
