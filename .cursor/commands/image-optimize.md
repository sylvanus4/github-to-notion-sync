## Image Optimizer

Resize, compress, and convert images to modern web formats (WebP, AVIF) for fast page loads.

### Usage

```
/image-optimize src/assets/
/image-optimize --format avif public/images/hero.png
/image-optimize --responsive src/assets/banner.png
```

### Workflow

1. **Audit** — Scan directory for images, report sizes, flag files over 200KB/500KB thresholds
2. **Plan** — Recommend target format and quality settings per image based on type (photo, graphic, thumbnail)
3. **Execute** — Run conversion commands via sharp-cli, cwebp, or ImageMagick
4. **Verify** — Compare before/after sizes, calculate total savings, generate `<picture>` fallback snippets

### Execution

Read and follow the `image-optimizer` skill (`.cursor/skills/standalone/image-optimizer/SKILL.md`) for the full 4-phase optimization workflow.

### Examples

Optimize an entire assets directory:
```
/image-optimize src/assets/
```

Convert a hero image to AVIF with responsive variants:
```
/image-optimize --format avif --responsive public/images/hero.png
```
