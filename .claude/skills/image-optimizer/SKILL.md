---
name: image-optimizer
description: >-
  Audit, resize, compress, and convert images to modern formats (WebP, AVIF)
  for fast web performance with quality-aware compression and responsive image
  set generation. Use when the user asks to "optimize images", "compress
  images", "convert to WebP", "resize images", "responsive image set", "reduce
  image size", "audit image sizes", "Core Web Vitals images", "batch image
  optimize", "이미지 최적화", "이미지 압축", "WebP 변환", "이미지 리사이즈", "반응형 이미지", "이미지 용량
  줄이기", or has oversized images hurting page load. Do NOT use for AI image
  generation (use nano-banana or muapi-image-studio), creative image editing
  or design (use canvas-design), SVG optimization (use svgo directly), or
  video compression (use video-compress).
disable-model-invocation: true
---

# Image Optimizer

Resize, compress, and convert images to modern web formats (WebP, AVIF) for optimal loading performance, with quality-aware compression and responsive image set generation.

## When to Use

- Optimizing images before deployment to reduce page load time
- Converting PNG/JPEG assets to WebP or AVIF
- Generating responsive image sets (1x, 2x, 3x) from high-res sources
- Batch-optimizing an entire directory of images
- Auditing a project for oversized images that hurt Core Web Vitals

## When NOT to Use

- AI image generation (use `nano-banana`, `muapi-image-studio`, or `image-gen`)
- Design or creative image editing (use `canvas-design`)
- Icon or SVG optimization (use svgo directly)
- Video compression (use `video-compress`)

## Workflow

### Phase 1: Audit

1. Scan the target directory for image files (`.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.tiff`)
2. Report per-file: dimensions, file size, format, estimated savings
3. Flag images over threshold:
   - **Critical**: > 500KB (likely unoptimized photos)
   - **Warning**: > 200KB (worth compressing)
   - **OK**: < 200KB

### Phase 2: Optimization Plan

Based on each image's characteristics, recommend:

| Source Format | Target Format | When |
|--------------|--------------|------|
| PNG (photo) | WebP | Photos incorrectly saved as PNG |
| PNG (graphics/transparency) | WebP (lossless) | Graphics needing alpha channel |
| JPEG | WebP | Standard photo optimization |
| Any | AVIF | Maximum compression, modern browsers |
| GIF (animated) | WebP (animated) | Animated content |

Propose quality settings:
- **Photos**: WebP quality 80-85 (visually lossless)
- **Graphics**: WebP lossless
- **Thumbnails**: WebP quality 70-75 (smaller is fine)
- **Hero images**: WebP quality 85-90 (quality matters)

### Phase 3: Execute

For each image, generate the shell commands:

```bash
# Single image conversion (requires sharp-cli, imagemagick, or cwebp)
npx sharp-cli -i input.png -o output.webp --webp '{"quality": 82}'

# Or using cwebp
cwebp -q 82 input.png -o output.webp

# Or using ImageMagick
magick input.png -quality 82 output.webp

# Batch conversion
npx sharp-cli -i 'src/assets/**/*.{png,jpg}' -o dist/assets/ -f webp --webp '{"quality": 82}'
```

For responsive sets:
```bash
# Generate 1x, 2x, 3x variants
npx sharp-cli -i hero.png -o hero-sm.webp --resize 640 --webp '{"quality": 82}'
npx sharp-cli -i hero.png -o hero-md.webp --resize 1280 --webp '{"quality": 82}'
npx sharp-cli -i hero.png -o hero-lg.webp --resize 1920 --webp '{"quality": 85}'
```

### Phase 4: Verification

1. Compare file sizes before and after
2. Calculate total savings (bytes and percentage)
3. Verify no visible quality degradation for critical images
4. Generate an HTML `<picture>` snippet with fallbacks:
   ```html
   <picture>
     <source srcset="image.avif" type="image/avif">
     <source srcset="image.webp" type="image/webp">
     <img src="image.jpg" alt="..." loading="lazy" width="800" height="600">
   </picture>
   ```

## Output Format

```markdown
## Image Optimization Report

### Summary
| Metric | Before | After | Savings |
|--------|--------|-------|---------|
| Total size | X MB | Y MB | Z% |
| File count | N | N | - |
| Avg file size | X KB | Y KB | Z% |

### Per-File Results
| File | Original | Optimized | Format | Savings |
|------|----------|-----------|--------|---------|
| hero.png | 1.2 MB | 180 KB | WebP | 85% |
| ... | ... | ... | ... | ... |

### Commands Used
(reproducible commands for CI integration)
```

## Gotchas

1. **Quality 80 != quality 80 across tools.** WebP quality 80 in `sharp` produces a different result than quality 80 in `cwebp`. Always test visually on 2-3 representative images before batch-processing.
2. **AVIF encoding is slow.** A single large image can take 10+ seconds. Don't default to AVIF for batch jobs unless the user explicitly requests it and accepts the encoding time.
3. **Transparent PNGs → JPEG = data loss.** Never convert a PNG with an alpha channel to JPEG. The transparency is silently destroyed and replaced with a white or black background.
4. **Responsive sets without `srcset` are useless.** Generating 3 sizes means nothing if the HTML doesn't use `<picture>` or `srcset`. Always provide the HTML snippet alongside the generated files.

## Verification

After completing all phases:
1. Confirm original files are untouched — optimized files are in a separate directory or have different extensions
2. Verify total savings percentage is reported with before/after sizes
3. Spot-check at least one image visually (open in browser) to confirm no visible quality loss
4. Confirm all generated `<img>` / `<picture>` tags include `width`, `height`, and `loading="lazy"`
5. Verify tools were checked for availability before running commands

## Anti-Example

```bash
# BAD: Overwrites originals with no backup
cwebp -q 50 hero.png -o hero.png  # Original destroyed forever

# BAD: JPEG for transparent images
magick logo-with-alpha.png logo.jpg  # Alpha channel silently lost

# BAD: AVIF everywhere without checking browser support
<img src="photo.avif" alt="...">  # No fallback for Safari < 16
# Should use <picture> with WebP and JPEG fallbacks
```

## Constraints

- Never delete original files — always output to a separate directory or with a different extension
- Default to WebP for broad compatibility; use AVIF only when explicitly requested or for maximum savings
- Preserve aspect ratio during resize unless explicitly told otherwise
- Always include `width` and `height` attributes in generated `<img>` tags to prevent CLS
- For transparency, use WebP lossless or PNG — never JPEG
- Check that tools are installed before running commands; suggest installation if missing
- Do NOT optimize SVGs — use svgo for that; this skill handles raster images only
