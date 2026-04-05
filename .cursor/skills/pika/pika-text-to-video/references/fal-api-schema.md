# fal.ai Pika API Reference

Source: https://fal.ai/models/fal-ai/pika/v2.2/text-to-video/api

## Endpoints

| Mode | Endpoint ID | Description |
|------|------------|-------------|
| text-to-video | `fal-ai/pika/v2.2/text-to-video` | Text prompt → video |
| image-to-video | `fal-ai/pika/v2.2/image-to-video` | Image + prompt → video |
| pikascenes | `fal-ai/pika/v2.2/pikascenes` | Multiple images → combined video |
| pikaframes | `fal-ai/pika/v2.2/pikaframes` | Keyframe images → transition video |
| pikaffects | `fal-ai/pika/v2.2/pikaffects` | Image + effect → video |
| pikaswaps | `fal-ai/pika/v2.2/pikaswaps` | Video + swap instructions → modified video |
| pikadditions | `fal-ai/pika/v2.2/pikadditions` | Video + image → video with added element |

## Common Parameters

- `prompt` (string): Text description
- `negative_prompt` (string): What to avoid, default "ugly, bad, terrible"
- `seed` (integer): Reproducibility seed
- `aspect_ratio`: 16:9, 9:16, 1:1, 4:5, 5:4, 3:2, 2:3
- `resolution`: 480p, 720p, 1080p
- `duration`: 5 or 10 seconds

## Pikaffect Effects

Cake-ify, Crumble, Crush, Decapitate, Deflate, Dissolve, Explode, Eye-pop,
Inflate, Levitate, Melt, Peel, Poke, Squish, Ta-da, Tear

## Pricing

~$0.40 per video generation (varies by resolution/duration)

## Authentication

Set `FAL_KEY` environment variable.
