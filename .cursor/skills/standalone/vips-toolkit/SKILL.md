# vips-toolkit

High-performance image processing via the libvips CLI (`vips`, `vipsthumbnail`). Streaming architecture processes images with constant memory regardless of input size -- 10-50x faster than ImageMagick for common operations, using ~1/10th the RAM. Supports 300+ formats including HEIF, AVIF, WebP, TIFF, SVG, PDF, and OpenSlide whole-slide images.

Use when the user asks to "resize images fast", "batch convert to WebP", "thumbnail generation", "vips", "vipsthumbnail", "libvips", "high-performance image processing", "low-memory image resize", "AVIF convert", "image pipeline", "streaming image processing", "ICC profile convert", "smart crop", "watermark image", "composite images", "이미지 고속 처리", "이미지 배치 변환", "썸네일 생성", "이미지 파이프라인", "저메모리 이미지 처리", "WebP 변환", "AVIF 변환", "vips-toolkit", or any task requiring fast, memory-efficient image manipulation via CLI.

Do NOT use for video processing (use ffmpeg-toolkit). Do NOT use for complex pixel-level algorithms or computer vision (use opencv-toolkit). Do NOT use for metadata-only operations without pixel manipulation (use exiftool-toolkit). Do NOT use for Python-scripted image generation with drawing/text (use pillow-toolkit). Do NOT use for non-programmatic photo editing with layers/masks (use manual tools like GIMP/Photoshop).

## Installation

```bash
# macOS (Homebrew)
brew install vips

# Verify
vips --version
vipsthumbnail --vips-version
```

Key build dependencies auto-installed: libjpeg-turbo, libpng, libwebp, libheif, libtiff, librsvg, poppler, OpenEXR, cgif.

## Step 0: Probe Input (Always Start Here)

Before any operation, inspect the source image to understand dimensions, color space, bit depth, and embedded ICC profile.

```bash
# Full header dump (format, width, height, bands, interpretation, etc.)
vips header "input.jpg"

# Specific field extraction
vips header -f width "input.jpg"
vips header -f height "input.jpg"
vips header -f bands "input.jpg"          # 3=RGB, 4=RGBA, 1=grayscale
vips header -f interpretation "input.jpg" # srgb, cmyk, b-w, etc.
vips header -f coding "input.jpg"         # none, labq, rad
vips header -f format "input.jpg"         # uchar, ushort, float, etc.

# Check ICC profile presence
vips header -f icc-profile-data "input.jpg" 2>/dev/null && echo "ICC: yes" || echo "ICC: no"

# Batch probe all images in a directory
for f in *.jpg; do printf "%-30s %sx%s %s\n" "$f" "$(vips header -f width "$f")" "$(vips header -f height "$f")" "$(vips header -f interpretation "$f")"; done
```

## Operation Categories

### Category 1: Resize & Thumbnail

The fastest resize path in any image toolkit. `vipsthumbnail` uses shrink-on-load for JPEG/WebP/TIFF (reads only the pixels needed).

```bash
# Quick thumbnail (auto-detects best shrink method)
vipsthumbnail "input.jpg" -s 320x240 -o "thumb_%s.jpg"

# Exact width, auto height (preserve aspect ratio)
vipsthumbnail "input.jpg" -s 800x -o "resized_%s.jpg"

# Exact height, auto width
vipsthumbnail "input.jpg" -s x600 -o "resized_%s.jpg"

# Force exact dimensions (may distort)
vipsthumbnail "input.jpg" -s 800x600! -o "exact_%s.jpg"

# Smart crop to exact dimensions (attention-based center detection)
vipsthumbnail "input.jpg" -s 800x600 --smartcrop attention -o "smart_%s.jpg"

# Smart crop variants
vipsthumbnail "input.jpg" -s 400x400 --smartcrop entropy -o "entropy_%s.jpg"
vipsthumbnail "input.jpg" -s 400x400 --smartcrop centre -o "centre_%s.jpg"

# Resize with specific interpolation kernel
vips resize "input.jpg" "output.jpg" 0.5                    # 50% scale, default bicubic
vips resize "input.jpg" "output.jpg" 2.0 --kernel lanczos3  # 2x upscale, Lanczos
vips resize "input.jpg" "output.jpg" 0.25 --kernel nearest  # 25%, pixel-art safe

# Batch thumbnails (multiple sizes for responsive web)
for w in 320 640 1024 1920; do
  vipsthumbnail "hero.jpg" -s "${w}x" -o "hero-${w}.webp[Q=80]"
done
```

**Quality control for output:**

```bash
# JPEG quality (default 75)
vipsthumbnail "input.jpg" -s 800x -o "out.jpg[Q=85]"

# WebP quality
vipsthumbnail "input.jpg" -s 800x -o "out.webp[Q=80]"

# PNG compression level (0-9, higher = smaller + slower)
vipsthumbnail "input.png" -s 800x -o "out.png[compression=6]"

# Strip metadata on output (smaller files)
vipsthumbnail "input.jpg" -s 800x --delete -o "out.jpg[Q=85]"
```

### Category 2: Format Conversion

```bash
# JPEG → WebP (lossy)
vips copy "input.jpg" "output.webp[Q=80]"

# JPEG → WebP (lossless)
vips copy "input.jpg" "output.webp[lossless=true]"

# JPEG → AVIF (smallest modern format, slower encode)
vips copy "input.jpg" "output.avif[Q=50,speed=4]"
# Q: 1-63 (lower=better quality), speed: 0-9 (higher=faster, lower quality)

# JPEG → HEIF/HEIC
vips copy "input.jpg" "output.heif[Q=50]"

# PNG → JPEG (strips alpha, adds white background)
vips flatten "input.png" "output.jpg[Q=90]" --background "255 255 255"

# TIFF → JPEG (handles multi-page: extracts page 0)
vips copy "input.tiff[page=0]" "output.jpg[Q=90]"

# SVG → PNG (rasterize at specific DPI)
vips copy "input.svg[dpi=300]" "output.png"

# PDF page → PNG (high DPI for print)
vips copy "input.pdf[dpi=300,page=0]" "page0.png"

# Animated GIF → WebP (preserves animation)
vips copy "input.gif" "output.webp[Q=75]"

# Batch convert directory (JPEG → WebP)
for f in *.jpg; do
  vips copy "$f" "${f%.jpg}.webp[Q=80]"
done
```

### Category 3: Crop & Extract

```bash
# Extract region: left, top, width, height
vips extract_area "input.jpg" "cropped.jpg" 100 50 800 600

# Smart crop (attention-based, keeps most interesting region)
vips smartcrop "input.jpg" "smart.jpg" 800 600 --interesting attention

# Extract specific band (e.g., red channel from RGB)
vips extract_band "input.jpg" "red_channel.png" 0    # 0=R, 1=G, 2=B
vips extract_band "input.jpg" "alpha.png" 3           # alpha channel if RGBA

# Trim whitespace/border (auto-detect threshold)
vips find_trim "input.png"
# Returns: left top width height — use with extract_area

# Gravity-based crop (like CSS object-fit: cover)
vipsthumbnail "input.jpg" -s 1200x630 --smartcrop attention -o "og-image.jpg[Q=85]"
```

### Category 4: Color Space & ICC Profiles

```bash
# Convert to sRGB with ICC profile transform
vips icc_transform "input.tiff" "output.jpg" "srgb"

# Import profile then export to sRGB
vips icc_import "cmyk.tiff" "temp.v" --input-profile "USWebCoatedSWOP.icc"
vips icc_export "temp.v" "output.jpg" --output-profile "sRGB.icc"

# Convert to grayscale (perceptual luminance)
vips colourspace "input.jpg" "gray.jpg" b-w

# Convert to Lab color space (for perceptual operations)
vips colourspace "input.jpg" "lab.v" lab

# Embed ICC profile
vips copy "input.jpg" "profiled.jpg"
# (profile is preserved from source automatically)

# Strip ICC profile
vips copy "input.jpg" "stripped.jpg[profile=none]"
```

### Category 5: Sharpen, Blur & Filters

```bash
# Unsharp mask (sigma, x1=flat, y2=jagged, y3=threshold)
vips sharpen "input.jpg" "sharp.jpg" --sigma 1.5 --x1 2 --y2 10 --y3 0

# Gaussian blur
vips gaussblur "input.jpg" "blurred.jpg" 3.0   # sigma=3.0

# Box blur (uniform, fast)
vips linear "input.jpg" "temp.v" 1 0
vips conv "temp.v" "box_blurred.jpg" "vips_kernel_3x3.mat"

# Median filter (salt-and-pepper noise removal)
vips median "input.jpg" "denoised.jpg" 3   # 3x3 window

# Emboss effect
vips conv "input.jpg" "emboss.jpg" "3 3 -2 -1 0 -1 1 1 0 1 2"

# Custom convolution kernel (3x3 sharpen)
echo "3 3 0 -1 0 -1 5 -1 0 -1 0" > /tmp/sharpen.mat
vips conv "input.jpg" "custom_sharp.jpg" /tmp/sharpen.mat
```

### Category 6: Composite & Watermark

```bash
# Overlay watermark (bottom-right with padding)
vips composite2 "base.jpg" "watermark.png" "composited.jpg" over \
  --x $(($(vips header -f width "base.jpg") - $(vips header -f width "watermark.png") - 20)) \
  --y $(($(vips header -f height "base.jpg") - $(vips header -f height "watermark.png") - 20))

# Semi-transparent overlay (blend mode)
vips linear "watermark.png" "faded.v" 0.3 0  # reduce to 30% opacity
vips composite2 "base.jpg" "faded.v" "watermarked.jpg" over --x 50 --y 50

# Tile watermark across entire image
vips replicate "watermark.png" "tiled.v" \
  $(($(vips header -f width "base.jpg") / $(vips header -f width "watermark.png") + 1)) \
  $(($(vips header -f height "base.jpg") / $(vips header -f height "watermark.png") + 1))
vips crop "tiled.v" "tiled_crop.v" 0 0 $(vips header -f width "base.jpg") $(vips header -f height "base.jpg")
vips composite2 "base.jpg" "tiled_crop.v" "tiled_watermark.jpg" over

# Side-by-side join (horizontal)
vips arrayjoin "left.jpg right.jpg" "sidebyside.jpg" --across 2

# Vertical stack
vips arrayjoin "top.jpg bottom.jpg" "stacked.jpg" --across 1

# Grid layout (2x2)
vips arrayjoin "a.jpg b.jpg c.jpg d.jpg" "grid.jpg" --across 2
```

### Category 7: Rotate & Transform

```bash
# Auto-rotate based on EXIF orientation (ESSENTIAL for camera photos)
vips autorot "input.jpg" "rotated.jpg"

# Rotate by exact angle (bilinear interpolation, expand canvas)
vips rotate "input.jpg" "rotated.jpg" 45

# Rotate 90/180/270 (lossless, no interpolation)
vips rot "input.jpg" "rot90.jpg" d90
vips rot "input.jpg" "rot180.jpg" d180
vips rot "input.jpg" "rot270.jpg" d270

# Flip horizontal / vertical
vips flip "input.jpg" "flipped_h.jpg" horizontal
vips flip "input.jpg" "flipped_v.jpg" vertical

# Affine transform (scale + rotate + translate)
vips affine "input.jpg" "transformed.jpg" "1.2 0.1 -0.1 1.2" \
  --interpolate "bicubic" --oarea "0 0 1000 800"
```

### Category 8: Adjustment & Histogram

```bash
# Brightness/contrast (linear: output = input * a + b)
vips linear "input.jpg" "bright.jpg" 1.2 10     # 20% brighter + offset
vips linear "input.jpg" "contrast.jpg" 1.5 -50   # more contrast

# Gamma correction
vips gamma "input.jpg" "gamma.jpg" --exponent 0.8   # brighten darks
vips gamma "input.jpg" "gamma.jpg" --exponent 1.5   # darken

# Histogram equalization (auto-contrast)
vips hist_equal "input.jpg" "equalized.jpg"

# Normalize (stretch histogram to full range)
vips hist_norm "input.jpg" "normalized.v"

# Invert
vips invert "input.jpg" "inverted.jpg"

# Per-channel statistics
vips stats "input.jpg"
# Returns: min, max, sum, sum^2, mean, deviation per band

# Generate histogram plot
vips hist_find "input.jpg" "hist.v"
vips hist_plot "hist.v" "histogram.png"
```

### Category 9: Alpha Channel & Transparency

```bash
# Add alpha channel (fully opaque)
vips bandjoin "input.jpg temp_alpha.v" "rgba.png"

# Remove alpha channel (flatten to white)
vips flatten "input.png" "no_alpha.jpg" --background "255 255 255"

# Premultiply alpha (required before many compositing operations)
vips premultiply "input.png" "premultiplied.v"

# Unpremultiply (after compositing, before saving)
vips unpremultiply "composited.v" "output.png"

# Extract alpha as grayscale mask
vips extract_band "input.png" "alpha_mask.png" 3

# Check if image has alpha
bands=$(vips header -f bands "input.png")
interp=$(vips header -f interpretation "input.png")
if [ "$bands" -eq 4 ] && [ "$interp" = "srgb" ]; then echo "Has alpha"; fi
```

### Category 10: Batch Processing Pipelines

```bash
# Responsive image set for web (JPEG source → WebP + AVIF at 3 sizes)
generate_responsive() {
  local src="$1" name="${1%.*}"
  for w in 640 1024 1920; do
    vipsthumbnail "$src" -s "${w}x" --delete -o "${name}-${w}.webp[Q=80]" &
    vipsthumbnail "$src" -s "${w}x" --delete -o "${name}-${w}.avif[Q=50,speed=6]" &
  done
  wait
}
generate_responsive "hero.jpg"

# Directory batch: resize + strip + convert
process_dir() {
  local indir="$1" outdir="$2" max_width="${3:-1920}"
  mkdir -p "$outdir"
  for f in "$indir"/*.{jpg,jpeg,png,tiff}; do
    [ -f "$f" ] || continue
    local base=$(basename "${f%.*}")
    vipsthumbnail "$f" -s "${max_width}x" --delete \
      -o "${outdir}/${base}.webp[Q=80]"
  done
}
process_dir "originals" "optimized" 1920

# Parallel batch with GNU parallel
find originals/ -name '*.jpg' | parallel -j$(nproc) \
  'vipsthumbnail {} -s 1200x --delete -o output/{/.}.webp[Q=80]'

# E-commerce product pipeline: resize + pad to square + white bg
square_pad() {
  local src="$1" size="${2:-1000}" out="$3"
  vipsthumbnail "$src" -s "${size}x${size}" -o "/tmp/_thumb.png"
  vips gravity "/tmp/_thumb.png" "$out" centre "$size" "$size" \
    --extend background --background "255 255 255"
}
square_pad "product.jpg" 1000 "product_square.jpg"
```

### Category 11: Large Image & Scientific Imaging

```bash
# Open extremely large images (TIFF pyramids, OpenSlide)
# libvips streams — never loads full image into RAM
vips header "gigapixel.tiff"   # works even on 100GB files

# Extract region from large image without loading whole file
vips extract_area "huge.tiff" "region.jpg" 10000 10000 2000 2000

# Generate Deep Zoom (DZI) pyramid for web viewers
vips dzsave "large.jpg" "output_dzi" --suffix ".jpg[Q=80]" --tile-size 256

# Generate Google Maps-style tiles
vips dzsave "large.jpg" "tiles" --layout google --suffix ".png" --tile-size 256

# TIFF pyramid creation (for GIS/medical imaging)
vips tiffsave "input.tiff" "pyramid.tiff" \
  --pyramid --compression jpeg --Q 85 --tile --tile-width 256 --tile-height 256

# 16-bit / 32-bit float processing (HDR, scientific)
vips cast "input_16bit.tiff" "float.v" float
vips linear "float.v" "processed.v" 1.5 0
vips cast "processed.v" "output_16bit.tiff" ushort

# OpenSlide whole-slide image (WSI) processing
# vips uses openslide loader for .svs, .mrxs, .ndpi, .vms, .scn
vips header "slide.svs"                        # read metadata without RAM spike
vips extract_area "slide.svs" "roi.png" 40000 30000 2048 2048
# Extract 2048x2048 region at (40000, 30000) — zero full-image load

# Multi-resolution pyramid for IIIF/DZI web viewer
vips dzsave "slide.svs" "iiif_output" --layout iiif \
  --suffix ".jpg[Q=80]" --tile-size 512

# Memory profiling: measure peak RSS for a pipeline
/usr/bin/time -l vipsthumbnail "huge.tiff" -s 1200x -o /dev/null 2>&1 | \
  grep "maximum resident"
# Typical result for 2GB TIFF: ~80MB peak (vs 2GB+ for full-load tools)

# Environment variable tuning for constrained systems
export VIPS_CONCURRENCY=2          # limit threads (default: nproc)
export VIPS_DISC_THRESHOLD=30m     # switch to disk-backed at 30MB
export VIPS_PROGRESS=1             # show progress bar on stderr
```

### Category 12: Text & Annotation (via Pango)

```bash
# Render text to image (requires Pango support)
vips text "Hello World" "text.png" --font "Arial 48" --dpi 300

# White text on transparent background
vips text "Watermark" "wm.png" --font "Helvetica Bold 24" --rgba true

# Overlay text on image
vips text "© 2026" "/tmp/copyright.png" --font "Arial 16" --rgba true
vips composite2 "photo.jpg" "/tmp/copyright.png" "stamped.jpg" over \
  --x 20 --y $(($(vips header -f height "photo.jpg") - 40))
```

## Performance Comparison

| Operation | vips (1000 JPEG, 4000x3000) | ImageMagick | speedup |
|-----------|---------------------------|-------------|---------|
| Resize to 800x | 12s | 85s | ~7x |
| Convert to WebP | 18s | 120s | ~6.5x |
| Thumbnail 320x | 6s | 62s | ~10x |
| Sharpen | 15s | 95s | ~6x |

Memory: vips uses ~50MB constant regardless of image count; ImageMagick scales linearly.

## Chaining Operations (Pipeline Pattern)

vips operations chain via intermediate `.v` (VIPS format) files that stay in memory:

```bash
# Multi-step pipeline: resize → sharpen → convert → strip metadata
vipsthumbnail "input.jpg" -s 1200x -o "/tmp/step1.v"
vips sharpen "/tmp/step1.v" "/tmp/step2.v" --sigma 1.0
vips copy "/tmp/step2.v" "final.webp[Q=80,strip=true]"

# Or use vipsthumbnail's built-in sharpen
vipsthumbnail "input.jpg" -s 1200x --sharpen mild --delete -o "final.webp[Q=80]"
# --sharpen options: none, mild (default for downsize), medium, heavy
```

## Load/Save Options Reference

| Format | Key Options | Example |
|--------|------------|---------|
| JPEG | `Q` (1-100), `optimize-coding`, `interlace`, `subsample-mode` | `[Q=85,optimize-coding=true,interlace=true]` |
| WebP | `Q` (0-100), `lossless`, `smart-subsample`, `effort` (0-6) | `[Q=80,smart-subsample=true]` |
| AVIF | `Q` (1-63), `speed` (0-9), `lossless` | `[Q=50,speed=4]` |
| PNG | `compression` (0-9), `interlace`, `palette`, `bitdepth` | `[compression=6,palette=true]` |
| TIFF | `compression` (none/jpeg/deflate/lzw), `Q`, `tile`, `pyramid` | `[compression=deflate,tile=true]` |
| HEIF | `Q` (1-100), `lossless`, `compression` (hevc/av1/avc) | `[Q=50,compression=av1]` |
| GIF | (via cgif) `effort`, `bitdepth` | `[effort=7]` |

## Error Handling & Troubleshooting

| Error Message | Root Cause | Fix |
|---|---|---|
| `VipsForeignLoad: ... is not a known file format` | Missing loader (heif, avif, pdf) | `brew install vips` with `--with-heif` or rebuild; `vips --vips-config \| grep heif` to verify |
| `VipsForeignSave: ... does not support ...` | Saving to format that lacks encoder | Check `vips list classes \| grep Save`; install `libcgif` for GIF, `libaom` for AVIF |
| `vips_image_write: ... No space left on device` | Temp dir full (vips uses `/tmp` for large images) | `export VIPS_TMPDIR=/path/to/big/disk`; increase `VIPS_DISC_THRESHOLD` |
| `out of order read` | Sequential access mode violated by random-access op | Insert `vips copy input.v tmp.v` (forces random access) before the failing step |
| `killed (signal 9)` / OOM | Image too large for available RAM | Lower `VIPS_CONCURRENCY`; set `VIPS_DISC_THRESHOLD=10m`; use `--vips-leak` to trace |
| `Profile not found` | ICC profile path missing | Install `icc-profiles-free` or point `VIPS_ICC_DIR` to profiles directory |

```bash
# Debug any failing pipeline
VIPS_TRACE=1 vips sharpen input.jpg output.jpg --sigma 1.5 2>&1 | head -50
# Shows every operation vips performs — find the failing step

# Verify vips build capabilities
vips --vips-config   # full build flags
vips list classes | grep -iE "(heif|avif|webp|pdf|svg)"  # available loaders/savers

# Memory leak detection
VIPS_LEAK=1 vipsthumbnail huge.tiff -s 800x -o /dev/null
# Prints unreferenced images at exit — non-zero means leak in your pipeline
```

## Gotchas

- **EXIF auto-rotation**: Camera JPEGs often have orientation tags. Use `vips autorot` or `vipsthumbnail` (auto-rotates by default) before any pixel operations. Raw `vips resize` does NOT auto-rotate.
- **Alpha premultiplication**: When compositing RGBA images, premultiply before blending and unpremultiply before saving to avoid dark fringing artifacts.
- **CMYK input**: Always convert CMYK to sRGB via `vips icc_transform` before operations that assume RGB. Skipping this produces inverted colors.
- **Intermediate format**: Use `.v` (VIPS native) for pipeline intermediates. Using JPEG between steps accumulates compression artifacts. `.v` files are uncompressed and fast.
- **Thread safety**: vips is fully thread-safe and auto-parallelizes. Set `VIPS_CONCURRENCY` to control thread count (default: CPU count). Reduce when running many parallel vips processes to avoid oversubscription.
- **Memory limit**: Set `VIPS_DISC_THRESHOLD` (default 100MB) to control when vips switches from RAM to disk-backed temp files. For batch jobs on constrained systems: `export VIPS_DISC_THRESHOLD=50m`.
- **PDF/SVG rasterization**: Requires `--dpi` specification. Default is 72 DPI which is too low for print. Use 300 for print, 150 for screen.
- **Animated formats**: `vips copy "anim.gif" "out.webp"` preserves animation. But resize/crop on animated images operates on all frames, which is slow. Extract single frames with `[page=N]` for preview.
