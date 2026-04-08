---
name: muapi-lipsync
description: >-
  Generate lip-synced talking-head videos from a portrait image or existing video
  plus an audio file via the Muapi.ai gateway. Supports 9 models including Infinite Talk,
  Hallo3, LetsTalk, SadTalker, Sonic, MuseTalk, and Wav2Lip with resolution control
  (480p-1080p). Two input modes: portrait-to-video and video-to-video lipsync.
  Use when the user asks to "lip sync", "talking head", "make this face talk",
  "audio to video", "lipsync", "muapi-lipsync", "portrait to speech video",
  "Infinite Talk", "Hallo3", "LetsTalk", "SadTalker", "립싱크", "말하는 영상",
  "초상화 영상", "오디오 립싱크", "립싱크 비디오", or any request to generate
  audio-driven talking videos from still images or existing video.
  Do NOT use for general video generation without lip sync (use pika-text-to-video).
  Do NOT use for image generation (use muapi-image-studio).
  Do NOT use for video editing or post-production (use video-editing-planner).
  Do NOT use for video transcription (use transcribee).
---

# Muapi Lip Sync Studio

Generate audio-driven talking-head videos from portrait images or existing videos through the Muapi.ai gateway.

## Prerequisites

| Requirement | Check |
|---|---|
| `MUAPI_API_KEY` in environment | `echo $MUAPI_API_KEY` |
| Python packages: `httpx`, `pydantic` | `pip list \| grep -E 'httpx\|pydantic'` |
| Muapi service module | `python -c "from app.services.muapi import muapi_client"` (from `backend/`) |
| Audio file (WAV, MP3, or M4A) | User-provided |
| Portrait image OR source video | User-provided |

## Input Modes

### Mode 1: Portrait Image + Audio → Talking Video

Takes a still portrait photograph and an audio file, generates a video of the portrait speaking with lip movements synchronized to the audio.

**Best for:** Product spokesperson videos, AI avatars, educational content, podcast visualizations.

### Mode 2: Source Video + Audio → Re-dubbed Video

Takes an existing video of a person and a new audio file, re-synchronizes the lip movements in the video to match the new audio.

**Best for:** Video dubbing, language localization, voiceover replacement, content repurposing.

## Available Models

| Model | Endpoint | Category | Best For |
|---|---|---|---|
| Infinite Talk | `infinitetalk-image-to-video` | Portrait→Video | High quality, natural motion |
| Hallo3 | `hallo3` | Portrait→Video | Fast, good expressions |
| LetsTalk | `letstalk` | Portrait→Video | Diverse angles |
| SadTalker | `sadtalker` | Portrait→Video | Classic, reliable |
| Sonic | `sonic` | Portrait→Video | Quick generation |
| MuseTalk RealTime | `musetalk-realtime` | Portrait→Video | Low latency |
| Wav2Lip | `wav2lip` | Video→Video | Video re-dubbing |
| Video Retalking | `video-retalking` | Video→Video | High fidelity re-dub |
| Infinite Talk V2V | `infinitetalk-video-to-video` | Video→Video | Premium re-dubbing |

## Resolution Options

| Resolution | Recommended Use |
|---|---|
| `480p` | Quick preview, social media stories |
| `720p` | Standard web content |
| `1080p` | Professional / broadcast quality |

## Workflow

```
1. User provides portrait image (or video) + audio file
2. Select input mode: portrait (image+audio) or video (video+audio)
3. Choose model based on quality/speed needs
4. Upload files to Muapi → get hosted URLs
5. Submit lipsync request → receive request_id
6. Poll for completion (2s intervals, up to 30 min)
7. Return video URL and metadata
```

## Usage

### Portrait-to-Video lip sync

```python
import asyncio
from app.services.muapi import muapi_client

async def lipsync_portrait():
    # Upload portrait and audio
    portrait = await muapi_client.upload_file("portrait.png")
    audio = await muapi_client.upload_file("speech.wav")

    result = await muapi_client.lipsync(
        endpoint="infinitetalk-image-to-video",
        audio_url=audio.url,
        image_url=portrait.url,
        resolution="720p",
    )
    print(f"Video URL: {result.output_url}")

asyncio.run(lipsync_portrait())
```

### Video re-dubbing

```python
async def redub_video():
    video = await muapi_client.upload_file("original_video.mp4")
    new_audio = await muapi_client.upload_file("korean_voiceover.wav")

    result = await muapi_client.lipsync(
        endpoint="wav2lip",
        audio_url=new_audio.url,
        video_url=video.url,
        resolution="1080p",
    )
    print(f"Re-dubbed video: {result.output_url}")
```

### Model selection helper

```python
from app.services.muapi.models import get_models_by_category, ModelCategory, LipsyncInputMode

lipsync_models = get_models_by_category(ModelCategory.LIPSYNC)

portrait_models = [m for m in lipsync_models if "image" in m.endpoint or m.endpoint in [
    "hallo3", "letstalk", "sadtalker", "sonic", "musetalk-realtime"
]]
video_models = [m for m in lipsync_models if "video-to-video" in m.endpoint or m.endpoint in [
    "wav2lip", "video-retalking"
]]

print("Portrait → Video models:")
for m in portrait_models:
    print(f"  {m.name}: {m.endpoint}")
print("Video → Video models:")
for m in video_models:
    print(f"  {m.name}: {m.endpoint}")
```

## Quality Tips

1. **Portrait images**: Front-facing, well-lit, neutral expression, minimum 512x512px
2. **Audio quality**: Clean speech, minimal background noise, WAV preferred
3. **Model selection**:
   - Infinite Talk: Best overall quality, slower
   - Hallo3: Good balance of quality and speed
   - SadTalker: Most reliable for diverse faces
   - Wav2Lip: Best for video re-dubbing specifically
4. **Resolution**: Start with 480p for testing, upgrade to 720p/1080p for final output

## Error Handling

| Error | Cause | Resolution |
|---|---|---|
| `MuapiError` | API returned non-2xx | Check API key, file URLs |
| `MuapiTimeoutError` | Generation took too long | 1080p can take 10+ minutes; increase max attempts |
| `MuapiJobFailedError` | Model rejected input | Check image/audio format, try different model |
| Upload failure | File too large or unsupported format | Convert to supported format, reduce file size |

## Integration with Other Skills

- **transcribee**: Transcribe source audio before lip sync to verify content
- **video-compress**: Compress output video for distribution
- **caption-subtitle-formatter**: Add subtitles to the generated video
- **content-repurposing-engine**: Create platform-specific variants of the talking-head video
- **muapi-media-orchestrator**: Chain lip sync as part of a larger media production pipeline
- **pika-video-pipeline**: Use lip sync output as input for further video processing

## Environment Variables

Same as muapi-image-studio (shared Muapi service configuration).
