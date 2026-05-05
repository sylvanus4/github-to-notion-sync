---
name: imagemagick-toolkit
description: >-
  Comprehensive ImageMagick 7.x CLI toolkit for image manipulation, conversion, and batch processing.
  ALWAYS invoke when the user asks to "convert image format", "resize image", "crop image",
  "rotate image", "add text to image", "watermark image", "create montage", "create contact sheet",
  "create animated gif", "optimize gif", "split gif frames", "images to pdf", "pdf to images",
  "compare images", "image diff", "composite images", "overlay images", "batch resize",
  "batch convert", "strip metadata", "auto-orient", "trim whitespace", "image border",
  "color adjust", "brightness contrast", "histogram stretch", "sepia tone", "grayscale",
  "emboss", "charcoal effect", "oil paint effect", "blur image magick", "sharpen image magick",
  "unsharp mask", "perspective distort", "barrel distort", "arc text", "annotate image",
  "montage grid", "sprite sheet", "tile images", "mogrify", "identify image",
  "image metadata", "EXIF data", "ICC profile", "imagemagick-toolkit", "magick convert",
  "이미지 변환", "이미지 리사이즈", "이미지 크롭", "이미지 회전", "텍스트 삽입",
  "워터마크", "몽타주", "GIF 생성", "GIF 분할", "PDF 변환", "이미지 비교",
  "이미지 합성", "배치 변환", "메타데이터 제거", "이미지 효과", "이미지 필터",
  "이미지 보정", "밝기 대비", "그레이스케일", "세피아", "이미지 정보",
  "이미지 테두리", "이미지 트림", "모자이크", "스프라이트 시트", "이미지 타일",
  "원근 왜곡", "배럴 왜곡", "이미지 주석", "배치 리사이즈".
  Do NOT use for OpenCV/Python computer vision operations (use opencv-toolkit).
  Do NOT use for video operations (use ffmpeg-toolkit).
  Do NOT use for web image optimization only (use image-optimizer).
  Do NOT use for AI image generation (use muapi-image-studio or nano-banana).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
  platforms: [darwin, linux]
  tags: [imagemagick, magick, convert, identify, composite, mogrify, montage, compare, image, transform, filter, resize, crop, annotate, batch, metadata, pdf, gif, sprite]
---

# imagemagick-toolkit

Comprehensive CLI toolkit wrapping ImageMagick 7.x (`magick`) for image manipulation, format conversion, compositing, and batch processing. Exposes the full parameter surface through structured workflows covering 15 operation categories.

## Quick Reference

| I want to... | Category | Key Flag |
|---|---|---|
| Change format (PNG to JPEG) | 1: Format Conversion | `magick in.png out.jpg` |
| Resize an image | 2: Resize & Scale | `-resize WxH` |
| Cut a region from image | 3: Crop & Trim | `-crop WxH+X+Y` |
| Rotate or flip | 4: Rotate & Flip | `-rotate`, `-flip`, `-flop` |
| Adjust colors, brightness | 5: Color Operations | `-modulate`, `-level` |
| Blur, sharpen, effects | 6: Filters & Effects | `-blur`, `-unsharp`, `-charcoal` |
| Add text, shapes | 7: Drawing & Annotation | `-annotate`, `-draw` |
| Overlay, watermark | 8: Compositing | `magick composite`, `-compose` |
| Create thumbnail grid | 9: Montage & Tiling | `magick montage` |
| Create/edit animated GIF | 10: GIF Animation | `-delay`, `-loop` |
| Convert PDF to images | 11: PDF Operations | `-density 300 in.pdf out.png` |
| Get image info, compare | 12: Info & Comparison | `magick identify`, `magick compare` |
| Strip/edit metadata | 13: Metadata & Profiles | `-strip`, `-set` |
| Process many files at once | 14: Batch Processing | `magick mogrify -path out/` |
| Distort, pixel math | 15: Advanced | `-distort`, `-fx` |

## Constraints

- Every `magick` command uses validated parameters; never pass unfiltered user prose
- Always validate input files exist before building commands
- Prefer `magick` (v7) over legacy `convert` (v6 compatibility alias)
- Never overwrite the original source file; `mogrify` exception: always use `-path` for output
- Output naming: `{stem}_{operation}.{ext}`
- For commands expected to run >30s, use `block_until_ms: 0` to background
- Never commit output image files to git
- Set resource limits for large images: `-limit memory 2GiB -limit disk 4GiB`
- Always quote file paths containing spaces with double quotes

## Prerequisites

- ImageMagick >= 7.0 (verified: `magick --version`)
- macOS: `brew install imagemagick`; Linux: `apt install imagemagick` or build from source
- For PDF operations: Ghostscript required (`gs --version`)
- For SVG: librsvg recommended for better rendering
- Security policy: check `/etc/ImageMagick-7/policy.xml` or `/opt/homebrew/etc/ImageMagick-7/policy.xml` if PDF/SVG operations fail (common: `<policy domain="coder" rights="none" pattern="PDF" />` blocks PDF)

## Workflow

### Step 0: Identify Input

```bash
magick identify -verbose "input.jpg" | head -30
```

Extract: format, dimensions, colorspace, depth, filesize, compression, EXIF orientation.

Quick check: `magick identify -format "%wx%h %m %[size]" "input.jpg"`

### Step 1: Select Operation Category

Match user request to one of the 15 categories below.

### Step 2: Build Command

Construct the `magick` command from validated parameters.

### Step 3: Execute

Run the command. For large batch operations (>30s), background it.

### Step 4: Verify Output

```bash
magick identify -format "%wx%h %m %Q %[size]" "output.jpg"
```

Report: input size, output size, dimensions, format.

## Operation Categories

### Category 1: Format Conversion

```bash
magick "input.png" "output.jpg"                    # PNG to JPEG
magick "input.jpg" -quality 85 "output.webp"       # JPEG to WebP
magick -density 300 "input.svg" "output.png"       # SVG to PNG at 300dpi
magick "input.tiff" -compress zip "output.tiff"    # Recompress TIFF
```

| Parameter | Description | Example |
|---|---|---|
| `-quality N` | Output quality (JPEG: 1-100, WebP: 0-100, PNG: 0-9 compression) | `-quality 85` |
| `-density N` | DPI for vector input (SVG, PDF) | `-density 300` |
| `-depth N` | Bit depth | `-depth 8` |
| `-colorspace` | Force colorspace | `-colorspace sRGB` |
| `-define webp:lossless=true` | WebP lossless mode | |

**Modern format conversion recipes (WebP/AVIF):**

```bash
# JPEG to WebP (lossy, quality 80, fast)
magick "input.jpg" -quality 80 "output.webp"

# JPEG to WebP (lossless, larger file but bit-perfect)
magick "input.jpg" -define webp:lossless=true "output.webp"

# JPEG to AVIF (smaller than WebP, slower encode)
magick "input.jpg" -quality 60 "output.avif"

# Batch JPEG → WebP for web (keep originals)
mkdir -p webp_out
magick mogrify -path webp_out -format webp -quality 80 *.jpg

# Responsive set: 3 widths + WebP format
for w in 640 1024 1920; do
  magick "hero.jpg" -resize "${w}x" -quality 80 "hero-${w}.webp"
done
```

AVIF requires ImageMagick compiled with `libheif` + `libaom`. Check: `magick -list format | grep AVIF`.

### Category 2: Resize & Scale

| Flag | Behavior | Example |
|---|---|---|
| `-resize WxH` | Fit within bounds (preserve aspect) | `-resize 800x600` |
| `-resize WxH!` | Exact size (ignore aspect) | `-resize 800x600!` |
| `-resize WxH^` | Fill bounds (crop may be needed) | `-resize 800x600^` |
| `-resize WxH>` | Shrink only (skip if smaller) | `-resize 800x600>` |
| `-resize WxH<` | Enlarge only (skip if larger) | `-resize 800x600<` |
| `-resize N%` | Percentage scale | `-resize 50%` |
| `-thumbnail WxH` | Resize + strip metadata (fastest) | `-thumbnail 200x200` |
| `-sample WxH` | Nearest-neighbor (pixelated, fast) | `-sample 400x300` |

```bash
magick "input.jpg" -resize 1280x720 -quality 85 "output_resized.jpg"
```

### Category 3: Crop & Trim

| Operation | Command |
|---|---|
| Crop region | `magick in.jpg -crop 400x300+100+50 +repage out.jpg` |
| Tile crop | `magick in.jpg -crop 200x200 +repage tile_%02d.jpg` |
| Auto-trim whitespace | `magick in.png -trim +repage out.png` |
| Trim with fuzz | `magick in.png -fuzz 10% -trim +repage out.png` |
| Shave borders | `magick in.jpg -shave 20x20 out.jpg` |
| Gravity crop (center) | `magick in.jpg -gravity Center -crop 500x500+0+0 +repage out.jpg` |

`+repage` resets the virtual canvas after crop. Always include it.

### Category 4: Rotate & Flip

| Operation | Command |
|---|---|
| Rotate 90 CW | `magick in.jpg -rotate 90 out.jpg` |
| Rotate with fill | `magick in.jpg -background white -rotate 15 out.jpg` |
| Conditional rotate | `magick in.jpg -rotate "90>" out.jpg` (only if taller than wide) |
| Flip (vertical) | `magick in.jpg -flip out.jpg` |
| Flop (horizontal) | `magick in.jpg -flop out.jpg` |
| Transpose | `magick in.jpg -transpose out.jpg` (flip + rotate 90) |
| Auto-orient (EXIF) | `magick in.jpg -auto-orient out.jpg` |

### Category 5: Color Operations

| Operation | Command |
|---|---|
| Grayscale | `magick in.jpg -colorspace Gray out.jpg` |
| Sepia | `magick in.jpg -sepia-tone 80% out.jpg` |
| Negate/invert | `magick in.jpg -negate out.jpg` |
| Modulate (B,S,H) | `magick in.jpg -modulate 110,120,100 out.jpg` |
| Brightness-contrast | `magick in.jpg -brightness-contrast 10x20 out.jpg` |
| Level stretch | `magick in.jpg -level 10%,90% out.jpg` |
| Auto-level | `magick in.jpg -auto-level out.jpg` |
| Normalize | `magick in.jpg -normalize out.jpg` |
| Colorize | `magick in.jpg -fill blue -colorize 30% out.jpg` |
| Channel separate | `magick in.jpg -channel R -separate out_red.jpg` |

`-modulate` format: `brightness,saturation,hue` (100=unchanged for each).

### Category 6: Filters & Effects

| Effect | Command |
|---|---|
| Gaussian blur | `magick in.jpg -blur 0x3 out.jpg` |
| Sharpen | `magick in.jpg -sharpen 0x1 out.jpg` |
| Unsharp mask | `magick in.jpg -unsharp 0x5+1.5+0.02 out.jpg` |
| Emboss | `magick in.jpg -emboss 1 out.jpg` |
| Edge detect | `magick in.jpg -edge 1 out.jpg` |
| Charcoal | `magick in.jpg -charcoal 2 out.jpg` |
| Sketch | `magick in.jpg -sketch 0x20+120 out.jpg` |
| Oil paint | `magick in.jpg -paint 4 out.jpg` |
| Despeckle | `magick in.jpg -despeckle out.jpg` |
| Noise reduction | `magick in.jpg -enhance out.jpg` |
| Morphology erode | `magick in.png -morphology Erode Diamond out.png` |
| Morphology dilate | `magick in.png -morphology Dilate Disk:2 out.png` |

`-unsharp` format: `radiusxsigma+amount+threshold`. Amount >1 amplifies; threshold prevents sharpening noise.

### Category 7: Drawing & Annotation

```bash
# Text annotation
magick in.jpg -gravity South -pointsize 36 -fill white -stroke black \
  -strokewidth 1 -annotate +0+20 "Caption text" out.jpg

# Draw rectangle
magick in.jpg -fill none -stroke red -strokewidth 2 \
  -draw "rectangle 50,50 200,150" out.jpg

# Draw circle
magick in.jpg -fill "rgba(255,0,0,0.3)" -draw "circle 100,100 150,100" out.jpg
```

| Parameter | Description |
|---|---|
| `-font` | Font name or path (`-font Arial`, `-font /path/to/font.ttf`) |
| `-pointsize N` | Text size in points |
| `-fill` | Fill color (names, hex `#FF0000`, `rgba(R,G,B,A)`) |
| `-stroke` | Outline color |
| `-strokewidth` | Outline thickness |
| `-gravity` | Anchor point: `NorthWest`, `North`, `NorthEast`, `West`, `Center`, `East`, `SouthWest`, `South`, `SouthEast` |
| `-annotate +X+Y` | Text at offset from gravity |

### Category 8: Compositing & Overlay

```bash
# Watermark overlay (bottom-right, 50% opacity)
magick "base.jpg" "watermark.png" -gravity SouthEast -geometry +10+10 \
  -compose Dissolve -define compose:args=50 -composite "output.jpg"

# Simple overlay
magick composite -gravity Center "overlay.png" "base.jpg" "output.jpg"
```

| Compose Mode | Effect |
|---|---|
| `Over` | Standard overlay (default) |
| `Multiply` | Darken blend |
| `Screen` | Lighten blend |
| `Dissolve` | Opacity-controlled (use `-define compose:args=N`) |
| `Difference` | Pixel difference |
| `Overlay` | Contrast-preserving blend |

Alpha management: `-alpha Set`, `-alpha Remove`, `-alpha Off`, `-background white -flatten` (remove alpha).

### Category 9: Montage & Tiling

```bash
# 4x3 thumbnail grid
magick montage *.jpg -tile 4x3 -geometry 200x200+5+5 -shadow montage.jpg

# Contact sheet with labels
magick montage *.jpg -tile 5x -geometry 150x150+2+2 \
  -label "%f\n%wx%h" -pointsize 10 -title "Contact Sheet" sheet.jpg
```

| Parameter | Description |
|---|---|
| `-tile NxM` | Grid layout (Nx0 = auto rows, 0xM = auto cols) |
| `-geometry WxH+border` | Thumbnail size + spacing |
| `-frame N` | Frame around each thumbnail |
| `-shadow` | Drop shadow effect |
| `-label "%f"` | Label with filename (`%w`=width, `%h`=height) |
| `-title` | Sheet title |
| `-background` | Background color |

### Category 10: GIF Animation

```bash
# Create GIF from images
magick -delay 10 -loop 0 frame_*.png animation.gif

# Optimize GIF
magick animation.gif -coalesce -layers optimize optimized.gif

# Extract frames
magick animation.gif frame_%03d.png

# Specific frame
magick "animation.gif[3]" frame3.png

# Resize GIF
magick animation.gif -coalesce -resize 320x240 -layers optimize small.gif
```

| Parameter | Description |
|---|---|
| `-delay N` | Frame delay in centiseconds (10 = 100ms) |
| `-loop N` | Loop count (0 = infinite) |
| `-dispose Background` | Clear frame before next |
| `-coalesce` | Expand optimized frames to full |
| `-layers optimize` | Optimize for smaller file |

**GIF edit pipeline (coalesce-first pattern):**

```bash
# WRONG: editing without coalesce corrupts optimized GIFs
magick animation.gif -resize 320x240 small.gif

# CORRECT: always coalesce → edit → optimize
magick animation.gif -coalesce -resize 320x240 -layers optimize small.gif

# Bounce loop (forward + reverse)
magick animation.gif -coalesce \( -clone 0--1 -reverse \) \
  -layers optimize bounce.gif

# Speed up 2x (halve delay)
magick animation.gif -coalesce -set delay 5 -layers optimize fast.gif

# Add crossfade between frames
magick animation.gif -coalesce -morph 5 -layers optimize smooth.gif
```

### Category 11: PDF Operations

```bash
# PDF to images (one per page)
magick -density 300 "input.pdf" "page_%03d.png"

# Specific page
magick -density 300 "input.pdf[0]" "first_page.png"

# Page range
magick -density 300 "input.pdf[2-5]" "page_%03d.png"

# Images to PDF
magick *.jpg -compress JPEG -quality 85 "output.pdf"
```

Gotcha: If PDF operations fail with "not authorized", edit `policy.xml` to allow PDF coder: `<policy domain="coder" rights="read|write" pattern="PDF" />`.

**High-quality PDF pipeline:**

```bash
# Print-quality extraction (300 DPI + trimmed whitespace)
magick -density 300 "input.pdf[0]" -trim +repage -quality 95 "page_hq.png"

# Merge images into multi-page PDF with consistent sizing
magick *.jpg -resize 2480x3508^ -gravity center -extent 2480x3508 \
  -units PixelsPerInch -density 300 -compress JPEG -quality 85 "output.pdf"

# PDF thumbnail strip (first 4 pages side by side)
magick -density 150 "input.pdf[0-3]" +append -resize x200 "preview_strip.png"
```

### Category 12: Image Information & Comparison

```bash
# Basic info
magick identify "input.jpg"

# Detailed info
magick identify -verbose "input.jpg"

# Custom format
magick identify -format "%wx%h %m %Q %[size] %[colorspace]" "input.jpg"

# Compare images (SSIM)
magick compare -metric SSIM "img1.jpg" "img2.jpg" diff.png

# Compare (pixel count)
magick compare -metric AE -fuzz 5% "img1.jpg" "img2.jpg" null: 2>&1
```

| Format Token | Meaning |
|---|---|
| `%w` / `%h` | Width / Height |
| `%m` | Format (JPEG, PNG...) |
| `%Q` | Compression quality |
| `%[size]` | File size |
| `%[EXIF:*]` | All EXIF tags |
| `%[colorspace]` | Color space |

| Metric | Meaning |
|---|---|
| `AE` | Absolute error (pixel count) |
| `RMSE` | Root mean square error |
| `SSIM` | Structural similarity (1.0 = identical) |
| `PHASH` | Perceptual hash distance |

### Category 13: Metadata & Profiles

| Operation | Command |
|---|---|
| Strip all metadata | `magick in.jpg -strip out.jpg` |
| Read EXIF | `magick identify -format "%[EXIF:*]" in.jpg` |
| Set comment | `magick in.jpg -set comment "My Photo" out.jpg` |
| Auto-orient (EXIF) | `magick in.jpg -auto-orient out.jpg` |
| Remove ICC profile | `magick in.jpg +profile icc out.jpg` |
| Assign sRGB profile | `magick in.jpg -profile sRGB.icc out.jpg` |
| Fast metadata only | `magick identify -ping "in.jpg"` |

### Category 14: Batch Processing

```bash
# Batch resize to 800px wide (output to resized/ directory)
mkdir -p resized
magick mogrify -path resized -resize 800x -quality 85 *.jpg

# Batch convert PNG to JPEG
magick mogrify -path converted -format jpg -quality 90 *.png

# Shell loop (more control)
for f in *.jpg; do
  magick "$f" -resize 1200x -quality 85 "output/${f%.jpg}_web.jpg"
done

# Parallel batch (GNU parallel)
find . -name "*.png" | parallel -j4 'magick {} -resize 800x -quality 85 resized/{/.}.jpg'
```

`mogrify` without `-path` overwrites originals. **Always use `-path`** for safe batch.

### Category 15: Advanced Operations

| Operation | Command |
|---|---|
| Perspective distort | `magick in.jpg -distort Perspective "0,0,10,20 W,0,W-10,30 0,H,15,H-10 W,H,W-5,H-20" out.jpg` |
| Barrel distort | `magick in.jpg -distort Barrel "0.0 0.0 -0.03 1.03" out.jpg` |
| Arc text | `magick -size 300x300 xc:white -font Arial -pointsize 24 -draw "text 0,0 'Hello'" -distort Arc 120 out.png` |
| Pixel formula | `magick in.jpg -fx "intensity" out.jpg` (grayscale via fx) |
| Evaluate (add) | `magick in.jpg -evaluate Add 20% out.jpg` |
| Flatten layers | `magick in.psd -flatten out.png` |
| Connected comp. | `magick in.png -connected-components 4 -auto-level out.png` |

`-fx` is a per-pixel formula engine: `p` = current pixel, `u` = first image, `v` = second image, `i`/`j` = x/y coords, `w`/`h` = dimensions.

## Error Handling

| Error | Symptom | Recovery |
|---|---|---|
| Policy blocks format | `not authorized` | Edit `policy.xml`: set `rights="read\|write"` for the blocked coder |
| Delegate missing | `no decode delegate for this image format` | Install Ghostscript (PDF), librsvg (SVG), libwebp (WebP) |
| Memory exceeded | `cache resources exhausted` | Add `-limit memory 2GiB -limit disk 4GiB` |
| File not found | `unable to open image` | Verify path with `ls -la`; check spaces in filename |
| Format not supported | `unrecognized image format` | Check `magick -list format \| grep <FMT>` |
| Mogrify overwrites | Original files lost | Always use `mogrify -path <dir>` |

## Gotchas

- **v6 vs v7**: In ImageMagick 7, use `magick` as the primary command. `convert` is a legacy v6 alias that may behave differently. Always prefer `magick in.jpg [ops] out.jpg`.
- **`policy.xml`**: Default security policies may block PDF, SVG, PS, EPS processing. Check `/opt/homebrew/etc/ImageMagick-7/policy.xml` (macOS) or `/etc/ImageMagick-7/policy.xml` (Linux). Common fixes:

```xml
<!-- Allow PDF read/write (requires Ghostscript) -->
<policy domain="coder" rights="read|write" pattern="PDF" />
<!-- Allow SVG (requires librsvg or internal renderer) -->
<policy domain="coder" rights="read|write" pattern="SVG" />
<!-- Raise memory limits for large images -->
<policy domain="resource" name="memory" value="2GiB" />
<policy domain="resource" name="disk" value="8GiB" />
```
- **`mogrify` overwrites**: Without `-path`, `mogrify` modifies files in-place. Always specify `-path output_dir/`. Safe pattern: `mkdir -p safe_out && magick mogrify -path safe_out -resize 800x -quality 85 *.jpg`. If you must edit in-place, back up first: `cp -r originals/ backup/ && magick mogrify -resize 800x originals/*.jpg`.
- **Geometry `+repage`**: After `-crop`, the virtual canvas retains original dimensions. Add `+repage` to reset.
- **`-resize` aspect ratio**: By default, `-resize WxH` preserves aspect ratio (fits within). Use `!` suffix for exact, `^` for fill.
- **GIF optimization**: Always `-coalesce` before resizing or modifying GIF frames, then `-layers optimize` after.
- **PDF density**: Without `-density`, PDF rasterizes at 72 DPI (blurry). Use `-density 300` for print quality.
- **Color profiles**: Converting between colorspaces without explicit profile assignment can shift colors. Use `-profile sRGB.icc` for web output.
- **Parentheses in complex commands**: Use `\( ... \)` (escaped) for sub-image processing within a single command.

## Anti-Example

> "Here's how to resize your image:
> `convert input.jpg -resize 800 output.jpg`"

This fails because: uses legacy `convert` instead of `magick`, `-resize 800` is ambiguous (800 what? width only without height preserves aspect but unclear), no quality parameter (JPEG defaults to 92 which may be too high), no input validation, no output naming convention. Every magick command must use explicit format, quality, and validated parameters.

## See Also

- **opencv-toolkit** -- Python-based computer vision (detection, segmentation, feature matching)
- **image-optimizer** -- Web-optimized compression (WebP/AVIF conversion, responsive sets)
- **ffmpeg-toolkit** -- Video/audio multimedia operations
- **video-compress** -- Simple video compression presets
- **nano-banana** -- AI image generation via Google GenAI
- **muapi-image-studio** -- AI image generation via Muapi gateway
