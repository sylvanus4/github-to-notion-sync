# pillow-toolkit

Python-native image processing via Pillow (PIL fork). The standard library for programmatic image manipulation in Python scripts, Jupyter notebooks, and data pipelines. Covers image I/O for 30+ formats, pixel-level manipulation, drawing and text rendering, geometric transforms, color space operations, filtering, compositing, animated GIF/WebP creation, batch automation, and integration with NumPy/OpenCV/ML frameworks. Pillow is the default choice when image operations need to live inside Python code rather than CLI one-liners.

Use when the user asks to "process images in Python", "Pillow", "PIL", "create thumbnail Python", "draw text on image", "image watermark Python", "Python image resize", "animated GIF Python", "image filter Python", "batch image processing Python", "create image from scratch", "pixel manipulation Python", "image composite Python", "Python screenshot processing", "convert image format Python", "image to numpy", "numpy to image", "pillow-toolkit", "이미지 Python 처리", "Python 이미지 리사이즈", "Python 썸네일", "Python 워터마크", "Python 이미지 필터", "Python 배치 이미지", "Python GIF 생성", or any task requiring image processing within a Python script or notebook.

Do NOT use for CLI-only one-liners without Python context (use vips-toolkit or imagemagick-toolkit). Do NOT use for metadata-only operations (use exiftool-toolkit). Do NOT use for video processing (use ffmpeg-toolkit). Do NOT use for computer vision, ML inference, or real-time video (use opencv-toolkit). Do NOT use for performance-critical batch processing of 10K+ large images (use vips-toolkit for lower memory footprint).

## Installation

```bash
# pip
pip install Pillow

# Verify
python3 -c "from PIL import Image; print(Image.__version__)"
```

Optional dependencies for extended format support:
```bash
brew install libjpeg libtiff little-cms2 libwebp openjpeg
# Pillow auto-detects these at install time
```

## Step 0: Probe Input (Always Start Here)

```python
from PIL import Image

img = Image.open("photo.jpg")
print(f"Format: {img.format}")           # JPEG, PNG, TIFF, etc.
print(f"Mode: {img.mode}")               # RGB, RGBA, L, P, CMYK, etc.
print(f"Size: {img.size}")               # (width, height)
print(f"Info: {img.info}")               # format-specific metadata dict
print(f"Palette: {img.palette}")          # None or palette object for mode P
print(f"Is animated: {getattr(img, 'is_animated', False)}")
print(f"Frames: {getattr(img, 'n_frames', 1)}")

# EXIF data (basic -- for full EXIF use exiftool-toolkit)
exif = img.getexif()
for tag_id, value in exif.items():
    from PIL.ExifTags import TAGS
    tag_name = TAGS.get(tag_id, tag_id)
    print(f"  {tag_name}: {value}")
```

## Operation Categories

### Category 1: Open, Save & Format Conversion

```python
from PIL import Image

# Open and save (format inferred from extension)
img = Image.open("input.png")
img.save("output.jpg", quality=85, optimize=True)

# Explicit format specification
img.save("output.webp", format="WEBP", quality=80, method=6)

# JPEG save options
img.save("out.jpg",
    quality=85,          # 1-95, higher = better
    optimize=True,       # smaller file, slower encode
    progressive=True,    # progressive JPEG
    subsampling=0,       # 4:4:4 chroma (best quality)
)

# PNG save options
img.save("out.png",
    optimize=True,
    compress_level=6,    # 0-9 (0=fast, 9=small)
)

# TIFF save options (print/archival)
img.save("out.tiff",
    compression="tiff_lzw",  # lossless
    dpi=(300, 300),
)

# WebP (lossy and lossless)
img.save("lossy.webp", quality=80)
img.save("lossless.webp", lossless=True)

# Convert mode before saving (RGBA → RGB for JPEG)
if img.mode == "RGBA":
    bg = Image.new("RGB", img.size, (255, 255, 255))
    bg.paste(img, mask=img.split()[3])  # alpha as mask
    bg.save("out.jpg", quality=90)

# Read from bytes (e.g., API response, S3 download)
from io import BytesIO
img = Image.open(BytesIO(raw_bytes))

# Save to bytes (e.g., for API upload)
buffer = BytesIO()
img.save(buffer, format="PNG")
png_bytes = buffer.getvalue()

# Open from URL
import urllib.request
urllib.request.urlretrieve("https://example.com/img.jpg", "/tmp/dl.jpg")
img = Image.open("/tmp/dl.jpg")
```

### Category 2: Resize & Thumbnail

```python
from PIL import Image

img = Image.open("photo.jpg")

# Resize to exact dimensions (may distort aspect ratio)
resized = img.resize((800, 600), Image.Resampling.LANCZOS)

# Resize preserving aspect ratio (fit within box)
img.thumbnail((800, 800), Image.Resampling.LANCZOS)
# NOTE: thumbnail modifies in-place and never enlarges

# Scale by factor
w, h = img.size
half = img.resize((w // 2, h // 2), Image.Resampling.LANCZOS)

# Fit within box, preserving aspect ratio (returns new image)
from PIL import ImageOps
fitted = ImageOps.fit(img, (400, 400), Image.Resampling.LANCZOS)
# Crops to exact size (center crop)

# Contain within box (no crop, adds padding)
contained = ImageOps.contain(img, (400, 400), Image.Resampling.LANCZOS)

# Pad to exact size with background color
padded = ImageOps.pad(img, (400, 400), Image.Resampling.LANCZOS,
                       color=(255, 255, 255))

# Resampling methods (quality order, slowest first):
# LANCZOS > BICUBIC > BILINEAR > BOX > NEAREST
```

### Category 3: Crop & Transform

```python
from PIL import Image, ImageOps

img = Image.open("photo.jpg")

# Crop (left, upper, right, lower)
cropped = img.crop((100, 50, 500, 400))

# Center crop to square
w, h = img.size
side = min(w, h)
left = (w - side) // 2
top = (h - side) // 2
square = img.crop((left, top, left + side, top + side))

# Rotate (counterclockwise, degrees)
rotated = img.rotate(45, expand=True, fillcolor=(255, 255, 255))
# expand=True: resize canvas to fit rotated image

# Auto-orient based on EXIF rotation tag
oriented = ImageOps.exif_transpose(img)
# Essential before processing phone photos

# Flip
h_flip = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
v_flip = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

# Perspective transform (4-point)
from PIL import Image
coeffs = [1.2, 0.1, -50, 0.05, 1.0, -20, 0.0001, 0.0002]
transformed = img.transform(img.size, Image.Transform.PERSPECTIVE,
                            coeffs, Image.Resampling.BICUBIC)

# Affine transform (scale + rotate + translate)
import math
angle = math.radians(15)
cos_a, sin_a = math.cos(angle), math.sin(angle)
affine = img.transform(img.size, Image.Transform.AFFINE,
    (cos_a, sin_a, 0, -sin_a, cos_a, 0),
    Image.Resampling.BICUBIC)
```

### Category 4: Color Operations

```python
from PIL import Image, ImageOps, ImageEnhance

img = Image.open("photo.jpg")

# Convert between modes
gray = img.convert("L")           # Grayscale
rgba = img.convert("RGBA")        # Add alpha
rgb = rgba.convert("RGB")         # Drop alpha (loses transparency)
bw = img.convert("1")             # Binary (1-bit)
cmyk = img.convert("CMYK")        # For print

# Split and merge channels
r, g, b = img.split()
merged = Image.merge("RGB", (b, g, r))  # swap R and B

# Invert colors
inverted = ImageOps.invert(img.convert("RGB"))

# Autocontrast
auto = ImageOps.autocontrast(img, cutoff=1)

# Equalize histogram
eq = ImageOps.equalize(img)

# Posterize (reduce color depth)
poster = ImageOps.posterize(img, bits=3)  # 2^3 = 8 levels per channel

# Colorize grayscale
gray = img.convert("L")
colorized = ImageOps.colorize(gray, black="navy", white="lightyellow")

# Enhancement controls
enhancer = ImageEnhance.Brightness(img)
bright = enhancer.enhance(1.3)      # >1 brighter, <1 darker

enhancer = ImageEnhance.Contrast(img)
contrast = enhancer.enhance(1.5)

enhancer = ImageEnhance.Sharpness(img)
sharp = enhancer.enhance(2.0)

enhancer = ImageEnhance.Color(img)
saturated = enhancer.enhance(1.5)   # >1 more colorful, 0 = grayscale
```

### Category 5: Filters & Effects

```python
from PIL import Image, ImageFilter

img = Image.open("photo.jpg")

# Built-in filters
blurred = img.filter(ImageFilter.BLUR)
sharp = img.filter(ImageFilter.SHARPEN)
detail = img.filter(ImageFilter.DETAIL)
smooth = img.filter(ImageFilter.SMOOTH_MORE)
edges = img.filter(ImageFilter.FIND_EDGES)
contour = img.filter(ImageFilter.CONTOUR)
emboss = img.filter(ImageFilter.EMBOSS)

# Gaussian blur (adjustable radius)
gauss = img.filter(ImageFilter.GaussianBlur(radius=5))

# Unsharp mask (professional sharpening)
unsharp = img.filter(ImageFilter.UnsharpMask(
    radius=2,        # blur radius
    percent=150,     # strength
    threshold=3,     # minimum brightness delta
))

# Box blur (fast, uniform)
box = img.filter(ImageFilter.BoxBlur(radius=3))

# Median filter (noise reduction, preserves edges)
median = img.filter(ImageFilter.MedianFilter(size=5))

# Min/Max filters (morphological erosion/dilation)
eroded = img.filter(ImageFilter.MinFilter(size=3))
dilated = img.filter(ImageFilter.MaxFilter(size=3))

# Mode filter (most common pixel value in neighborhood)
mode_f = img.filter(ImageFilter.ModeFilter(size=5))

# Custom kernel
kernel = ImageFilter.Kernel(
    size=(3, 3),
    kernel=[0, -1, 0,
            -1,  5, -1,
            0, -1, 0],
    scale=1,
    offset=0,
)
custom = img.filter(kernel)

# Rank filter
rank = img.filter(ImageFilter.RankFilter(size=5, rank=12))
# rank=0 → min, rank=size*size-1 → max, middle → median
```

### Category 6: Drawing & Text

```python
from PIL import Image, ImageDraw, ImageFont

# Create blank canvas
canvas = Image.new("RGB", (800, 600), color=(30, 30, 30))
draw = ImageDraw.Draw(canvas)

# Lines
draw.line([(10, 10), (790, 590)], fill="red", width=3)

# Rectangle
draw.rectangle([(50, 50), (200, 150)], outline="white", width=2)
draw.rectangle([(250, 50), (400, 150)], fill="blue", outline="white")

# Rounded rectangle
draw.rounded_rectangle([(50, 200), (250, 300)], radius=15,
                        fill="green", outline="white")

# Ellipse / circle
draw.ellipse([(300, 200), (500, 350)], fill="purple", outline="white")

# Polygon
draw.polygon([(550, 200), (700, 200), (650, 350)], fill="orange")

# Arc and pieslice
draw.arc([(50, 370), (250, 530)], start=0, end=270, fill="cyan", width=3)
draw.pieslice([(300, 370), (500, 530)], start=0, end=270, fill="yellow")

# Text with custom font
try:
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size=36)
except OSError:
    font = ImageFont.load_default(size=36)

draw.text((50, 540), "Hello, Pillow!", fill="white", font=font)

# Text with anchor (centered)
draw.text((400, 300), "Centered", fill="white", font=font, anchor="mm")
# Anchors: "lt"=left-top, "mm"=middle-middle, "rb"=right-bottom

# Multi-line text
draw.multiline_text((550, 370), "Line 1\nLine 2\nLine 3",
                    fill="white", font=font, spacing=8)

# Get text bounding box (for positioning)
bbox = draw.textbbox((0, 0), "Measure me", font=font)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]

canvas.save("drawing.png")
```

### Category 7: Compositing & Watermark

```python
from PIL import Image, ImageDraw, ImageFont

# Paste image onto another
bg = Image.open("background.jpg")
overlay = Image.open("logo.png").convert("RGBA")

# Resize overlay to fit
overlay = overlay.resize((200, 200), Image.Resampling.LANCZOS)

# Paste with alpha transparency
bg.paste(overlay, (50, 50), mask=overlay)  # 3rd arg = alpha mask
bg.save("composited.jpg")

# Semi-transparent watermark
def add_watermark(img_path, text, output_path, opacity=128):
    base = Image.open(img_path).convert("RGBA")

    # Create transparent overlay
    watermark = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark)

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
    except OSError:
        font = ImageFont.load_default(size=48)

    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (base.width - tw) // 2
    y = (base.height - th) // 2

    draw.text((x, y), text, fill=(255, 255, 255, opacity), font=font)

    result = Image.alpha_composite(base, watermark)
    result.convert("RGB").save(output_path, quality=90)

add_watermark("photo.jpg", "(c) 2026 My Studio", "watermarked.jpg")

# Tiled watermark (diagonal repeat)
def tile_watermark(img_path, text, output_path, opacity=64):
    base = Image.open(img_path).convert("RGBA")
    watermark = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    except OSError:
        font = ImageFont.load_default(size=24)

    for y in range(0, base.height, 120):
        for x in range(-200, base.width, 300):
            txt_img = Image.new("RGBA", (280, 40), (0, 0, 0, 0))
            d = ImageDraw.Draw(txt_img)
            d.text((0, 0), text, fill=(255, 255, 255, opacity), font=font)
            rotated = txt_img.rotate(30, expand=True, fillcolor=(0, 0, 0, 0))
            watermark.paste(rotated, (x, y), rotated)

    result = Image.alpha_composite(base, watermark)
    result.convert("RGB").save(output_path, quality=90)

# Blend two images (50/50 mix)
img1 = Image.open("a.jpg")
img2 = Image.open("b.jpg").resize(img1.size)
blended = Image.blend(img1, img2, alpha=0.5)
```

### Category 8: Animated GIF & WebP

```python
from PIL import Image
import glob

# Create animated GIF from frames
frames = [Image.open(f) for f in sorted(glob.glob("frames/*.png"))]
frames[0].save(
    "animation.gif",
    save_all=True,
    append_images=frames[1:],
    duration=100,       # ms per frame
    loop=0,             # 0 = infinite loop
    optimize=True,
)

# Create animated WebP
frames[0].save(
    "animation.webp",
    save_all=True,
    append_images=frames[1:],
    duration=100,
    loop=0,
    quality=80,
)

# Read animated GIF frame by frame
gif = Image.open("animation.gif")
for i in range(gif.n_frames):
    gif.seek(i)
    frame = gif.copy()
    frame.save(f"frame_{i:04d}.png")

# Resize animated GIF (all frames)
gif = Image.open("animation.gif")
new_size = (gif.width // 2, gif.height // 2)
resized_frames = []
for i in range(gif.n_frames):
    gif.seek(i)
    resized_frames.append(gif.copy().resize(new_size, Image.Resampling.LANCZOS))

resized_frames[0].save(
    "small.gif",
    save_all=True,
    append_images=resized_frames[1:],
    duration=gif.info.get("duration", 100),
    loop=gif.info.get("loop", 0),
    optimize=True,
)

# Create simple progress bar GIF
def make_progress_gif(width=400, height=30, steps=20):
    frames = []
    for i in range(steps + 1):
        img = Image.new("RGB", (width, height), (40, 40, 40))
        draw = ImageDraw.Draw(img)
        fill_w = int(width * i / steps)
        draw.rectangle([(0, 0), (fill_w, height)], fill=(0, 180, 0))
        frames.append(img)
    frames[0].save("progress.gif", save_all=True,
                   append_images=frames[1:], duration=150, loop=0)

from PIL import ImageDraw
make_progress_gif()
```

### Category 9: NumPy & ML Integration

```python
from PIL import Image
import numpy as np

img = Image.open("photo.jpg")

# PIL → NumPy
arr = np.array(img)           # shape: (H, W, 3) for RGB
print(arr.shape, arr.dtype)   # (height, width, channels), uint8

# NumPy → PIL
result = Image.fromarray(arr)

# Grayscale conversions
gray_arr = np.array(img.convert("L"))  # shape: (H, W), dtype: uint8
gray_img = Image.fromarray(gray_arr, mode="L")

# RGBA
rgba_arr = np.array(img.convert("RGBA"))  # shape: (H, W, 4)

# PIL → OpenCV (BGR conversion)
import cv2
cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

# OpenCV → PIL
pil_img = Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))

# Numpy operations on image data
arr = np.array(img).astype(np.float32)
# Brightness adjustment
bright = np.clip(arr * 1.3, 0, 255).astype(np.uint8)
Image.fromarray(bright).save("bright.jpg")

# Channel swap
swapped = arr[:, :, ::-1]  # RGB → BGR

# Threshold
gray = np.array(img.convert("L"))
binary = ((gray > 128) * 255).astype(np.uint8)
Image.fromarray(binary).save("binary.png")

# ML preprocessing (normalize to [-1, 1])
normalized = (arr / 127.5) - 1.0

# Torch tensor (PyTorch)
# import torch
# tensor = torch.from_numpy(arr).permute(2, 0, 1).float() / 255.0
# Result: shape (C, H, W), range [0, 1]
```

### Category 10: Batch Processing Patterns

```python
from PIL import Image, ImageOps
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

def process_one(src: Path, dst_dir: Path, max_size: int = 1200):
    """Resize + auto-orient + optimize for web."""
    try:
        img = Image.open(src)
        img = ImageOps.exif_transpose(img)  # fix rotation
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

        if img.mode == "RGBA":
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3])
            img = bg

        out = dst_dir / f"{src.stem}.webp"
        img.save(out, format="WEBP", quality=80, method=4)
        return f"OK: {src.name} → {out.name}"
    except Exception as e:
        return f"FAIL: {src.name}: {e}"

def batch_process(src_dir: str, dst_dir: str, workers: int = 4):
    src_path = Path(src_dir)
    dst_path = Path(dst_dir)
    dst_path.mkdir(parents=True, exist_ok=True)

    files = list(src_path.glob("*.jpg")) + list(src_path.glob("*.png"))
    print(f"Processing {len(files)} files...")

    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(process_one, f, dst_path) for f in files]
        for fut in futures:
            print(fut.result())

# Usage:
# batch_process("photos/raw", "photos/web")

# Contact sheet (grid of thumbnails)
def contact_sheet(image_paths, cols=5, thumb_size=200, padding=10):
    thumbs = []
    for p in image_paths:
        img = Image.open(p)
        img = ImageOps.exif_transpose(img)
        img = ImageOps.fit(img, (thumb_size, thumb_size), Image.Resampling.LANCZOS)
        thumbs.append(img)

    rows = (len(thumbs) + cols - 1) // cols
    sheet_w = cols * (thumb_size + padding) + padding
    sheet_h = rows * (thumb_size + padding) + padding
    sheet = Image.new("RGB", (sheet_w, sheet_h), (30, 30, 30))

    for idx, thumb in enumerate(thumbs):
        r, c = divmod(idx, cols)
        x = padding + c * (thumb_size + padding)
        y = padding + r * (thumb_size + padding)
        sheet.paste(thumb, (x, y))

    return sheet

# Usage:
# paths = list(Path("photos").glob("*.jpg"))[:20]
# sheet = contact_sheet(paths)
# sheet.save("contact_sheet.jpg", quality=90)
```

### Category 11: Create Images from Scratch

```python
from PIL import Image, ImageDraw, ImageFont
import math

# Solid color
red = Image.new("RGB", (400, 300), (255, 0, 0))

# Gradient (horizontal)
def h_gradient(w, h, c1, c2):
    img = Image.new("RGB", (w, h))
    for x in range(w):
        t = x / (w - 1)
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        ImageDraw.Draw(img).line([(x, 0), (x, h)], fill=(r, g, b))
    return img

grad = h_gradient(800, 400, (20, 20, 80), (200, 100, 255))

# Checkerboard pattern
def checkerboard(w, h, sq=32):
    img = Image.new("RGB", (w, h))
    for y in range(0, h, sq):
        for x in range(0, w, sq):
            color = (200, 200, 200) if (x // sq + y // sq) % 2 == 0 else (60, 60, 60)
            ImageDraw.Draw(img).rectangle(
                [(x, y), (x + sq - 1, y + sq - 1)], fill=color)
    return img

# Placeholder image with dimensions label
def placeholder(w, h, bg=(200, 200, 200), text_color=(100, 100, 100)):
    img = Image.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", max(w, h) // 10)
    except OSError:
        font = ImageFont.load_default()
    label = f"{w} x {h}"
    draw.text((w // 2, h // 2), label, fill=text_color, font=font, anchor="mm")
    draw.rectangle([(0, 0), (w - 1, h - 1)], outline=text_color)
    return img

placeholder(1200, 630).save("og-placeholder.png")
```

## Performance Tips

| Scenario | Approach |
|----------|----------|
| Thumbnails at scale | Use `img.thumbnail()` (in-place, never enlarges) instead of `img.resize()` |
| JPEG decode speed | `img.draft("RGB", (target_w, target_h))` before `.load()` for JPEG downscale during decode |
| Large image scan | `Image.open()` is lazy; `.load()` triggers actual decode. Probe `.size` and `.format` without loading pixels |
| Batch 1K+ files | `ProcessPoolExecutor` (CPU-bound); release `img.close()` to free memory |
| Memory-critical | Process one image at a time; avoid holding lists of Image objects |
| Repeated operations | Cache fonts with `ImageFont.truetype()` outside the loop |

## Integration with Other Toolkits

### Pillow + vips (High-Performance Pipeline)

```python
# Use vips for heavy lifting (resize/crop), Pillow for finishing (text overlay, compositing)
import subprocess, io
from PIL import Image, ImageDraw, ImageFont

def vips_resize_then_pillow_annotate(src: str, dst: str, width: int, label: str):
    """vips handles the 2GB TIFF resize in streaming mode; Pillow adds watermark."""
    # Step 1: vips resize to temp PNG (streaming, ~80MB peak for 2GB input)
    tmp = "/tmp/_vips_resized.png"
    subprocess.run([
        "vips", "thumbnail", src, tmp, str(width),
        "--size", "down"  # never enlarge
    ], check=True)

    # Step 2: Pillow compositing (text overlay, logo paste)
    img = Image.open(tmp)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    except OSError:
        font = ImageFont.load_default()
    draw.text((10, img.height - 40), label, fill=(255, 255, 255, 180), font=font)
    img.save(dst, "WEBP", quality=85)
    img.close()
```

### Pillow + ExifTool (Metadata-Aware Processing)

```python
import subprocess, json
from PIL import Image, ImageOps

def process_with_metadata_preservation(src: str, dst: str):
    """Process image with Pillow, then copy full EXIF/IPTC/XMP via ExifTool."""
    img = Image.open(src)
    img = ImageOps.exif_transpose(img)  # fix orientation before processing
    img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
    img.save(dst, "JPEG", quality=85)
    img.close()

    # ExifTool copies ALL metadata (EXIF, IPTC, XMP, ICC profile) from original
    subprocess.run([
        "exiftool", "-TagsFromFile", src,
        "-all:all",              # copy everything
        "-ICC_Profile",          # include ICC profile
        "-overwrite_original",
        dst
    ], check=True)

def sort_photos_by_date(src_dir: str):
    """Use ExifTool for fast batch date extraction, Pillow for thumbnails."""
    result = subprocess.run(
        ["exiftool", "-json", "-DateTimeOriginal", "-r", src_dir],
        capture_output=True, text=True
    )
    photos = json.loads(result.stdout)
    # ExifTool reads dates 10-50x faster than Pillow's EXIF parser for batch
    return sorted(photos, key=lambda p: p.get("DateTimeOriginal", "9999"))
```

### Pillow + ffmpeg (Video Frame Extraction & Assembly)

```python
import subprocess, struct
from PIL import Image

def extract_frame_pillow(video: str, time_sec: float, size: tuple = None) -> Image.Image:
    """Extract a single video frame via ffmpeg, return as PIL Image."""
    cmd = ["ffmpeg", "-ss", str(time_sec), "-i", video,
           "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-v", "quiet"]
    # Get dimensions first
    probe = subprocess.run(
        ["ffprobe", "-v", "quiet", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", video],
        capture_output=True, text=True
    )
    w, h = map(int, probe.stdout.strip().split(","))
    cmd += ["pipe:1"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    frame = Image.frombytes("RGB", (w, h), raw)
    if size:
        frame.thumbnail(size, Image.Resampling.LANCZOS)
    return frame

def frames_to_gif(frames: list, dst: str, duration: int = 100):
    """Assemble PIL Image list into optimized GIF."""
    frames[0].save(
        dst, save_all=True, append_images=frames[1:],
        duration=duration, loop=0, optimize=True
    )
```

## Advanced: ICC Color Management

```python
from PIL import Image, ImageCms

# Load ICC profiles
srgb = ImageCms.createProfile("sRGB")
# For print workflows: load Adobe RGB or CMYK profile
adobergb_prof = ImageCms.getOpenProfile("/path/to/AdobeRGB1998.icc")

# Convert sRGB → Adobe RGB (photography workflow)
img = Image.open("photo.jpg")
transform = ImageCms.buildTransformFromOpenProfiles(
    srgb, adobergb_prof, "RGB", "RGB",
    renderingIntent=ImageCms.Intent.PERCEPTUAL
)
img_adobergb = ImageCms.applyTransform(img, transform)

# Convert RGB → CMYK (print-ready output)
cmyk_prof = ImageCms.getOpenProfile("/path/to/USWebCoatedSWOP.icc")
transform_cmyk = ImageCms.buildTransformFromOpenProfiles(
    srgb, cmyk_prof, "RGB", "CMYK",
    renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC
)
img_cmyk = ImageCms.applyTransform(img, transform_cmyk)
img_cmyk.save("print_ready.tif", "TIFF")

# Extract and embed ICC profile
icc_data = img.info.get("icc_profile")
if icc_data:
    out = img.resize((800, 600))
    out.save("resized.jpg", icc_profile=icc_data)  # preserve color profile
```

## Advanced: 16-bit / HDR Processing

```python
import numpy as np
from PIL import Image

# Pillow supports 16-bit per channel via mode "I;16" (grayscale) or NumPy bridge
# For full 16-bit RGB: use NumPy as intermediary

# Read 16-bit TIFF (scientific/medical imaging)
img16 = Image.open("scan_16bit.tiff")
arr = np.array(img16).astype(np.float32)  # shape (H, W), range 0-65535

# Normalize to 0-1 for processing
arr_norm = arr / 65535.0

# Apply processing in float space (no integer overflow)
arr_processed = np.clip(arr_norm * 1.3 + 0.05, 0, 1)  # brightness + offset

# Convert back to 16-bit
arr_16 = (arr_processed * 65535).astype(np.uint16)
result = Image.fromarray(arr_16, mode="I;16")
result.save("processed_16bit.tiff")

# HDR tone mapping (simple Reinhard operator)
def reinhard_tonemap(hdr_arr: np.ndarray, key: float = 0.18) -> np.ndarray:
    """Simple Reinhard global tone mapping for HDR float arrays."""
    luminance = 0.2126 * hdr_arr[..., 0] + 0.7152 * hdr_arr[..., 1] + 0.0722 * hdr_arr[..., 2]
    log_avg = np.exp(np.mean(np.log(luminance + 1e-6)))
    scaled = (key / log_avg) * luminance
    mapped = scaled / (1 + scaled)
    ratio = (mapped / (luminance + 1e-6))[..., np.newaxis]
    return np.clip(hdr_arr * ratio, 0, 1)

# Usage: load EXR via OpenCV, tonemap with Pillow pipeline
# import cv2
# hdr = cv2.imread("scene.exr", cv2.IMREAD_UNCHANGED).astype(np.float32)
# hdr_rgb = cv2.cvtColor(hdr, cv2.COLOR_BGR2RGB)
# ldr = reinhard_tonemap(hdr_rgb)
# Image.fromarray((ldr * 255).astype(np.uint8)).save("tonemapped.jpg", quality=95)
```

## Error Handling & Troubleshooting

| Error / Symptom | Root Cause | Fix |
|---|---|---|
| `DecompressionBombError` | Image exceeds safety pixel limit (178M px) | `Image.MAX_IMAGE_PIXELS = 300_000_000` (set before open); verify you truly need the full resolution |
| `OSError: cannot write mode RGBA as JPEG` | JPEG has no alpha channel support | `img.convert("RGB").save(...)` or composite onto white: `Image.alpha_composite(white_bg, img)` |
| `SyntaxError: not a PNG file` | File extension doesn't match actual format | Use `Image.open()` (auto-detects) not explicit loader; or `imghdr.what("file")` first |
| `AttributeError: 'NoneType' has no 'save'` | Used `img = img.thumbnail(...)` (returns None) | `img.thumbnail(size)` modifies in-place; don't reassign |
| `ValueError: images do not match` | Operand images differ in size or mode | Ensure same `.size` and `.mode` before `ImageChops` or paste operations |
| Sideways/rotated JPEG output | EXIF orientation tag not applied | Add `img = ImageOps.exif_transpose(img)` as first operation after open |
| Memory grows unbounded in loop | File handles not closed | Use `img.close()` after each iteration or `img.load(); img.close()` pattern |
| `Image.open()` is slow for many files | Pillow reads header lazily but stat() still runs | Use `glob` + multiprocessing; or `img.draft(mode, size)` to skip full decode |

```python
# Debug: inspect image internal state
from PIL import Image
img = Image.open("photo.jpg")
print(f"Format: {img.format}, Mode: {img.mode}, Size: {img.size}")
print(f"Info dict: {img.info}")  # EXIF, DPI, ICC profile, etc.
print(f"Palette: {'yes' if img.palette else 'no'}")
print(f"Is animated: {getattr(img, 'is_animated', False)}")

# Validate file is a valid image (catch corrupted files in batch)
from PIL import Image
def validate_image(path: str) -> bool:
    try:
        with Image.open(path) as img:
            img.verify()  # checks structure without decoding pixels
        with Image.open(path) as img:
            img.load()    # actually decode pixels — catches truncated files
        return True
    except Exception as e:
        print(f"Invalid: {path} — {e}")
        return False

# Memory-efficient batch processing pattern
from pathlib import Path
for p in Path("photos").glob("*.jpg"):
    img = Image.open(p)
    img = ImageOps.exif_transpose(img)
    img.thumbnail((800, 800), Image.LANCZOS)
    img.save(f"thumbs/{p.name}", quality=85, optimize=True)
    img.close()  # explicit cleanup
```

## Gotchas

- **JPEG does not support alpha**: Saving RGBA as JPEG silently drops alpha or raises an error. Convert to RGB first with a white background composite.
- **thumbnail() is in-place**: `img.thumbnail()` modifies the Image object and returns `None`. Do not assign: `img = img.thumbnail(...)` overwrites with `None`.
- **EXIF orientation**: Phone photos often have EXIF rotation flags. Without `ImageOps.exif_transpose()`, images appear sideways. Always call it before processing.
- **Coordinate order**: Pillow uses `(width, height)` for `.resize()` and `.new()`, matching `img.size`. NumPy arrays are `(height, width, channels)`. Mixing them up is the #1 bug source.
- **Palette mode (P)**: Some PNGs and GIFs use palette mode. Operations like `.filter()` or `.paste()` may require `.convert("RGB")` or `.convert("RGBA")` first.
- **Integer overflow**: Pixel math on `uint8` arrays wraps around (255 + 1 = 0). Cast to `float32` before arithmetic, then clip back.
- **File handle leak**: `Image.open()` keeps the file handle open until garbage collected. In loops, explicitly call `img.close()` or use `with` context (available for some operations).
- **WebP animation**: Pillow can create animated WebP but reading individual frames requires seeking. Memory usage can spike for long animations.
