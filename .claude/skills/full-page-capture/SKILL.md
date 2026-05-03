---
name: full-page-capture
description: >-
  Capture full-page screenshots of local HTML files or web pages using
  Playwright CLI. Supports viewport width control, color scheme forcing,
  chart/animation wait, and automatic sectional capture for pages exceeding
  Chromium's 16384px height limit. Use when the user asks to "capture full
  page", "screenshot entire page", "full page image", "capture HTML", "save
  page as image", "전체 페이지 캡처", "풀페이지 스크린샷", "HTML 이미지 변환", "전체 화면 캡처", "페이지
  캡처", "브라우저 캡처", "전체 스크린샷", or any request to convert a web page or local
  HTML file into a single image. Do NOT use for interactive browser automation
  (use agent-browser or cursor-ide-browser MCP). Do NOT use for Playwright E2E
  test suites (use e2e-testing). Do NOT use for web content extraction to
  markdown (use defuddle or WebFetch).
disable-model-invocation: true
---

# Full Page Capture — Browser Screenshot Tool

Capture complete web pages as high-fidelity PNG/JPEG images using Playwright CLI.

## Prerequisites

```bash
npx playwright --version || npm install -g playwright
```

Playwright must be installed with Chromium browser support.

## Core Command

```bash
npx playwright screenshot [OPTIONS] <URL> <OUTPUT_PATH>
```

## Parameters

| Parameter | Flag | Default | Description |
|-----------|------|---------|-------------|
| Full page | `--full-page` | off | Capture entire scrollable content, not just viewport |
| Viewport size | `--viewport-size "WIDTH, HEIGHT"` | `1280, 720` | Set browser viewport (width × height); use **comma**, not `×` |
| Color scheme | `--color-scheme <light\|dark\|no-preference>` | system | Force light or dark mode rendering |
| Wait timeout | `--wait-for-timeout <ms>` | 0 | Wait for charts/animations before capture (recommend 2000-3000) |
| Device | `--device "<name>"` | none | Emulate a device (e.g., "iPhone 13") |
| Browser | `--browser <chromium\|firefox\|webkit>` | chromium | Choose rendering engine |

**Output format:** The CLI saves **PNG** when the output path ends in `.png` (default for this skill). The CLI does **not** expose `--type` or `--quality`. For **JPEG** with a **quality** setting (0–100), use a short Node + Playwright API snippet (see [JPEG output](#jpeg-output-and-quality)) after capturing, or convert PNG → JPEG with ImageMagick/`sips`.

## Standard Workflow

### Step 1: Determine the URL

- **Local HTML file**: Convert path to `file://` URL
  ```bash
  # Example: local file
  URL="file:///absolute/path/to/file.html"
  ```
- **Remote page**: Use the URL directly
  ```bash
  URL="https://example.com"
  ```

### Step 2: Execute Capture

```bash
npx playwright screenshot \
  --full-page \
  --viewport-size "1280, 720" \
  --wait-for-timeout 2000 \
  --color-scheme light \
  "$URL" \
  "/path/to/output.png"
```

### Step 3: Verify Output

```bash
file /path/to/output.png
# Expected: PNG image data, 1280 x NNNN, 8-bit/color RGB, non-interlaced
```

Read the output image with the Read tool to verify visual quality.

## JPEG output and quality

`npx playwright screenshot` always writes PNG for typical `.png` paths. For **JPEG** with **quality** (recommended 80–90 for web):

```bash
node -e "
const { chromium } = require('playwright');
(async () => {
  const url = process.argv[1];
  const out = process.argv[2];
  const quality = parseInt(process.argv[3] || '85', 10);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  await page.goto(url);
  await page.waitForTimeout(2000);
  await page.screenshot({ path: out, type: 'jpeg', quality, fullPage: true });
  await browser.close();
})();
" "$URL" "/path/to/output.jpg" 85
```

Or capture PNG via CLI, then convert: `magick input.png -quality 85 output.jpg` (ImageMagick).

## Advanced: Tall Page Sectional Capture

Chromium has a **16,384px height limit** for screenshots. Pages taller than this will show repeated/blank content below that threshold.

### Detection

```bash
# Check page height with a quick Node.js script
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  await page.goto('$URL');
  await page.waitForTimeout(2000);
  const height = await page.evaluate(() => document.documentElement.scrollHeight);
  console.log('Page height:', height, height > 16384 ? '⚠️ EXCEEDS LIMIT' : '✅ OK');
  await browser.close();
})();
"
```

### Sectional Capture (for pages > 16384px)

If the page exceeds the limit, capture in sections and stitch:

```bash
# Use a Python script with Pillow for stitching
python3 -c "
from PIL import Image
import subprocess, json, math

url = '$URL'
output = '$OUTPUT'
max_h = 16000  # safe margin below 16384

# Get page height
result = subprocess.run([
    'node', '-e',
    f\"const {{chromium}} = require('playwright'); (async () => {{ const b = await chromium.launch(); const p = await b.newPage({{viewport:{{width:1280,height:720}}}}); await p.goto('{url}'); await p.waitForTimeout(2000); console.log(await p.evaluate(() => document.documentElement.scrollHeight)); await b.close(); }})();\"
], capture_output=True, text=True)
total_h = int(result.stdout.strip())
sections = math.ceil(total_h / max_h)

images = []
for i in range(sections):
    sec_file = f'/tmp/section_{i}.png'
    clip_top = i * max_h
    clip_h = min(max_h, total_h - clip_top)
    subprocess.run([
        'node', '-e',
        f\"const {{chromium}} = require('playwright'); (async () => {{ const b = await chromium.launch(); const p = await b.newPage({{viewport:{{width:1280,height:{total_h}}}}}); await p.goto('{url}'); await p.waitForTimeout(2000); await p.screenshot({{path:'{sec_file}', clip:{{x:0,y:{clip_top},width:1280,height:{clip_h}}}}}); await b.close(); }})();\"
    ])
    images.append(Image.open(sec_file))

final = Image.new('RGB', (1280, total_h))
y_offset = 0
for img in images:
    final.paste(img, (0, y_offset))
    y_offset += img.height
final.save(output)
print(f'Stitched {sections} sections → {output} ({1280}x{total_h})')
"
```

## Tips

1. **Charts (Chart.js, D3, etc.)**: Always use `--wait-for-timeout 2000` or higher to let JavaScript charts render
2. **Dark mode**: Use `--color-scheme dark` to force dark theme rendering
3. **High DPI**: Playwright renders at 1x by default. For Retina-quality, use `--device "Desktop Chrome HiDPI"`
4. **Korean fonts**: Ensure the system has Korean fonts installed (macOS includes them by default)
5. **SVG diagrams**: SVG renders natively in the browser — no special handling needed
6. **Batch capture**: Loop over files with a shell for-loop

## Common Patterns

### Local HTML to PNG (most common)
```bash
npx playwright screenshot --full-page --wait-for-timeout 2000 \
  "file:///path/to/document.html" output.png
```

### Dark mode capture
```bash
npx playwright screenshot --full-page --color-scheme dark \
  --wait-for-timeout 2000 "https://example.com" dark-capture.png
```

### Wide viewport for diagrams
```bash
npx playwright screenshot --full-page --viewport-size "1920, 1080" \
  --wait-for-timeout 2000 "file:///path/to/diagram.html" wide-capture.png
```

## Constraints

- Maximum single-capture height: **16,384px** (Chromium limit)
- Pages with lazy-loaded content may need `--wait-for-timeout` adjustments
- Authentication-required pages need a separate login step first
- PDF output is NOT supported by this tool — use browser print-to-PDF instead
