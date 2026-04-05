---
name: pika-text-to-video
description: |
  Generate videos from text prompts, images, keyframes, or apply special effects using Pika v2.2 via fal.ai API. Supports 7 modes: text-to-video, image-to-video, pikascenes (multi-image composition), pikaframes (keyframe transitions), pikaffects (16 special effects), pikaswaps (element replacement in video), and pikadditions (add elements to video). Up to 1080p resolution, 5-10s duration, 7 aspect ratios. Use when the user asks to "generate a video", "create video from text", "animate this image", "text to video", "image to video", "pika video", "비디오 생성", "텍스트 투 비디오", "이미지 투 비디오", "영상 만들어줘", "AI 비디오", "pika-text-to-video", "pikascenes", "pikaframes", "pikaffects", "영상 이펙트", "키프레임 비디오", "영상 특수효과", or any request to generate video content using AI. Do NOT use for live video meeting participation (use pikastream-video-meeting). Do NOT use for video compression or encoding (use video-compress). Do NOT use for video editing plans (use video-editing-planner). Do NOT use for video transcription (use transcribee). Do NOT use for NotebookLM video explainers (use nlm-video). Do NOT use for Remotion programmatic videos (use remotion-motion-forge).
metadata:
  author: thakicloud
  version: 0.1.0
  category: pika
  license: Apache-2.0
  cost: ~$0.40/video
---

# Pika Text-to-Video

Generate videos via 7 Pika v2.2 modes through fal.ai.

Script directory: `SKILL_DIR=.cursor/skills/pika/pika-text-to-video`

## Prerequisites

- Python 3.10+
- `FAL_KEY` environment variable set (get one at https://fal.ai/dashboard/keys)

## First-Time Setup

```bash
pip install -r $SKILL_DIR/requirements.txt
```

## Modes

### 1. Text-to-Video

Generate video from a text prompt.

```bash
python $SKILL_DIR/scripts/pika_video_generate.py text-to-video \
  --prompt "A golden retriever running through autumn leaves in slow motion" \
  --resolution 1080p --duration 5 --aspect-ratio 16:9 \
  --output outputs/pika/my-video.mp4
```

### 2. Image-to-Video

Animate a static image with a motion prompt.

```bash
python $SKILL_DIR/scripts/pika_video_generate.py image-to-video \
  --image path/to/photo.jpg \
  --prompt "Camera slowly zooms in, leaves gently blowing in the wind" \
  --resolution 720p --duration 5 \
  --output outputs/pika/animated.mp4
```

### 3. Pikascenes

Combine multiple images into one video with AI composition.

```bash
python $SKILL_DIR/scripts/pika_video_generate.py pikascenes \
  --images img1.jpg img2.jpg img3.jpg \
  --prompt "A cinematic montage transitioning between scenes" \
  --ingredients-mode creative --resolution 1080p \
  --output outputs/pika/scenes.mp4
```

### 4. Pikaframes

Create smooth transitions between 2-5 keyframe images.

```bash
python $SKILL_DIR/scripts/pika_video_generate.py pikaframes \
  --images keyframe1.jpg keyframe2.jpg keyframe3.jpg \
  --prompt "Smooth morphing transition between each frame" \
  --resolution 720p \
  --output outputs/pika/frames.mp4
```

### 5. Pikaffects

Apply one of 16 special effects to an image.

Available effects: Cake-ify, Crumble, Crush, Decapitate, Deflate, Dissolve, Explode, Eye-pop, Inflate, Levitate, Melt, Peel, Poke, Squish, Ta-da, Tear

```bash
python $SKILL_DIR/scripts/pika_video_generate.py pikaffects \
  --image photo.jpg --effect Explode \
  --prompt "Dramatic explosion with particles" \
  --output outputs/pika/effect.mp4
```

### 6. Pikaswaps

Replace or modify elements within an existing video.

```bash
python $SKILL_DIR/scripts/pika_video_generate.py pikaswaps \
  --video-url "https://example.com/video.mp4" \
  --image replacement.jpg \
  --modify-region "the hat on the person" \
  --prompt "Replace with a cowboy hat" \
  --output outputs/pika/swapped.mp4
```

### 7. Pikadditions

Add new elements to an existing video.

```bash
python $SKILL_DIR/scripts/pika_video_generate.py pikadditions \
  --video-url "https://example.com/video.mp4" \
  --image element.png \
  --prompt "Add a flying butterfly near the flowers" \
  --output outputs/pika/added.mp4
```

## Workflow

### Step 1 — Choose mode

Based on user intent:
- Has only text → `text-to-video`
- Has one image + wants animation → `image-to-video`
- Has multiple images + wants composition → `pikascenes`
- Has multiple images + wants transitions → `pikaframes`
- Has one image + wants effect → `pikaffects`
- Has existing video + wants to replace something → `pikaswaps`
- Has existing video + wants to add something → `pikadditions`

### Step 2 — Prepare inputs

1. If the user provides a local image file, the script auto-uploads it to fal.ai storage.
2. For `--images`, pass all paths space-separated.
3. Ensure `outputs/pika/` directory exists: `mkdir -p outputs/pika`

### Step 3 — Run generation

Execute the appropriate command from the Modes section above. The script:
- Uploads local files to fal.ai storage
- Submits the generation request via queue
- Polls for completion with log streaming
- Downloads the result to `--output` path (if specified)
- Prints JSON result to stdout

### Step 4 — Present result

Show the user:
- The local file path (if `--output` was used)
- The remote video URL from the JSON output
- Generation parameters used

## Error Handling

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Success | Video URL in stdout JSON |
| 1 | General error | Check stderr for details |
| 2 | Invalid arguments | Check required args for the chosen mode |
| 3 | API error | Check FAL_KEY validity, network, or API status |
| 4 | Missing FAL_KEY | Set FAL_KEY environment variable |

## Cross-Skill References

- For live video meeting avatar: use `pikastream-video-meeting`
- For video compression after generation: use `video-compress`
- For post-production editing plans: use `video-editing-planner`
- For subtitles on generated video: use `caption-subtitle-formatter`
- For video script writing before generation: use `video-script-generator`
- For publishing video content: use `content-repurposing-engine`
