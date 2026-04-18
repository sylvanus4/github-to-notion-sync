## Image Gen

Generate images via AI — text-to-image, image-to-image, and local generation with 100+ models.

### Usage

```
/image-gen "a futuristic data center at sunset"      # text-to-image
/image-gen --local "minimalist icon set"             # local generation
/image-gen --style "photorealistic" "team photo"     # style-specific
```

### Workflow

1. **Prompt** — Craft a detailed visual prompt with style, composition, lighting cues
2. **Select model** — Choose from Flux, SDXL, Midjourney-style, or local generation
3. **Generate** — Run generation with aspect ratio and quality settings
4. **Iterate** — Refine prompt or parameters based on output
5. **Export** — Save final images to the project outputs directory

### Execution

Read and follow the `muapi-image-studio` skill (`.cursor/skills/pika/muapi-image-studio/SKILL.md`) for Muapi gateway-based generation with 100+ models. For local generation without API dependencies, use `nano-banana` (`.cursor/skills/standalone/nano-banana/SKILL.md`).

### Examples

Generate via Muapi:
```
/image-gen "isometric view of a Kubernetes cluster with glowing nodes"
```

Generate locally:
```
/image-gen --local "flat design icon for cloud storage"
```
