---
name: mermaid-render
description: >-
  Extract Mermaid code blocks from Markdown files and render them as PNG
  images via mmdc (Mermaid CLI). Supports single-block rendering,
  full-document extraction with image-reference replacement, and batch
  processing of multiple Markdown files. Use when the user asks to "render
  mermaid", "mermaid to png", "extract mermaid", "mermaid diagram", "convert
  mermaid to image", "render diagrams from markdown", "mermaid images for
  docx", or needs Mermaid blocks converted to static images for DOCX/PDF
  pipelines. Do NOT use for static architecture diagrams without Mermaid
  source (use architecture-diagram). Do NOT use for Mermaid-in-HTML rendering
  (browser handles natively). Do NOT use for general image manipulation (use
  image-optimizer). Do NOT use for Draw.io XML diagrams (use
  alphaear-logic-visualizer). Korean triggers: "머메이드 렌더링", "머메이드 PNG", "다이어그램
  이미지 변환", "머메이드 이미지", "마크다운 다이어그램 추출".
---

# Mermaid Render -- Markdown Diagrams to PNG

Extract ` ```mermaid``` ` code blocks from Markdown documents and render them
as high-resolution PNG images via `mmdc` (Mermaid CLI). The clean Markdown
output replaces each block with a standard `![Diagram N](path.png)` image
reference, ready for Pandoc, docx-js, or any downstream converter.

## Prerequisites

| Tool | Install | Purpose |
|------|---------|---------|
| `mmdc` | `npm install -g @mermaid-js/mermaid-cli` | Render `.mmd` → PNG |
| Python 3.9+ | System | Run `scripts/preprocess_mermaid.py` |

Verify: `mmdc --version` and `python3 --version`

> **Note:** On first run, mmdc downloads a bundled Chromium binary (~170 MB).
> If running in CI or air-gapped environments, pre-install Chromium or set
> `PUPPETEER_EXECUTABLE_PATH` to an existing Chrome/Chromium binary.

## Quick Reference

```bash
# Full document: extract all Mermaid blocks, render PNGs, output clean MD
python3 scripts/preprocess_mermaid.py input.md --output-dir diagrams/ --output clean.md

# Pipe to stdout (for chaining)
python3 scripts/preprocess_mermaid.py input.md --output-dir diagrams/

# Single block: render one .mmd file directly
mmdc -i diagram.mmd -o diagram.png -w 1200 -b transparent -s 2
```

## Mode 1: Single Block

Render one Mermaid definition file to PNG directly via `mmdc`.

```bash
# Write the Mermaid definition
cat > flowchart.mmd << 'EOF'
flowchart LR
    A[Start] --> B{Decision}
    B -->|Yes| C[Action]
    B -->|No| D[End]
EOF

# Render to PNG
mmdc -i flowchart.mmd -o flowchart.png -w 1200 -b transparent -s 2

# With a specific theme
mmdc -i flowchart.mmd -o flowchart.png -w 1200 -b transparent -t dark
```

**mmdc flags:**

| Flag | Default | Description |
|------|---------|-------------|
| `-i` | (required) | Input `.mmd` file |
| `-o` | (required) | Output image path (`.png`, `.svg`, `.pdf`) |
| `-w` | 800 | Width in pixels |
| `-b` | white | Background color (`transparent`, `#FFFFFF`, etc.) |
| `-s` | 1 | Scale factor for high-DPI (2 = retina) |
| `-t` | default | Theme: `default`, `dark`, `forest`, `neutral` |
| `-c` | -- | Custom config JSON file |

## Mode 2: Full Document

Extract all Mermaid blocks from a Markdown file, render each to PNG, and
output clean Markdown with image references replacing the original blocks.

```bash
python3 scripts/preprocess_mermaid.py input.md \
  --output-dir diagrams/ \
  --output clean.md \
  --width 1200 \
  --background transparent \
  --scale 2 \
  --theme neutral
```

**What the script does:**

1. Scans `input.md` for all ` ```mermaid ... ``` ` code blocks
2. Writes each block to `diagrams/diagram-N.mmd`
3. Renders each `.mmd` to `diagrams/diagram-N.png` via `mmdc`
4. Replaces each Mermaid block with `![Diagram N](diagrams/diagram-N.png)`
5. Strips `<details>`/`<summary>` HTML tags unsupported by DOCX converters
6. Writes clean Markdown to `--output` (or stdout if omitted)

**CLI flags:**

| Flag | Default | Description |
|------|---------|-------------|
| `input` | (required) | Path to source Markdown file |
| `--output-dir` | `diagrams` | Directory for rendered PNG files |
| `--output` | stdout | Write clean Markdown to this file |
| `--width` | 1200 | Diagram width in pixels |
| `--background` | transparent | Background color |
| `--scale` | 2 | Render scale for high-DPI |
| `--theme` | (mmdc default) | `default`, `dark`, `forest`, `neutral` |

## Mode 3: Batch

Process multiple Markdown files in a directory. Use a shell loop with the
script.

```bash
mkdir -p diagrams

for md in docs/*.md; do
  base=$(basename "$md" .md)
  python3 scripts/preprocess_mermaid.py "$md" \
    --output-dir "diagrams/${base}" \
    --output "docs-clean/${base}.md"
done
```

Each file gets its own subdirectory under `diagrams/` to prevent filename
collisions across documents.

## Configuration

### Theme Selection

| Theme | Best For |
|-------|----------|
| `default` | General documentation, light backgrounds |
| `dark` | Dark-mode documents, slides with dark backgrounds |
| `forest` | Nature/growth themes, eco-friendly branding |
| `neutral` | Corporate documents, DOCX reports, minimal styling |

### Width Guidelines

| Content | Recommended Width |
|---------|-------------------|
| Simple flowcharts | 800-1000 |
| Medium diagrams | 1200 (default) |
| Complex sequence diagrams | 1600-2000 |
| Large class diagrams | 2000+ |

### Custom mmdc Config

For advanced customization, create a config JSON:

```json
{
  "theme": "neutral",
  "themeVariables": {
    "primaryColor": "#1A3C6E",
    "primaryTextColor": "#fff",
    "lineColor": "#333"
  },
  "flowchart": { "curve": "basis" },
  "sequence": { "mirrorActors": false }
}
```

```bash
mmdc -i diagram.mmd -o diagram.png -c mermaid-config.json -w 1200 -b transparent
```

## Integration Points

### With `anthropic-docx` Skill (Mermaid-to-DOCX Pipeline)

```bash
# 1. Pre-process Mermaid blocks
python3 scripts/preprocess_mermaid.py report.md --output-dir diagrams/ --output clean.md

# 2. Generate DOCX from clean.md using docx-js with ImageRun for each PNG
#    (see anthropic-docx skill "Mermaid-to-DOCX Pipeline" section)
```

### With `pandoc` Skill (Mode 7)

```bash
# 1. Pre-process Mermaid blocks
python3 scripts/preprocess_mermaid.py input.md --output-dir diagrams/ --output input-for-docx.md

# 2. Convert to DOCX via Pandoc
pandoc input-for-docx.md -o output.docx --from markdown --to docx --resource-path=.
```

### With Korean DOCX Pipeline

```bash
# 1. Mermaid pre-processing
python3 scripts/preprocess_mermaid.py input.md --output-dir diagrams/ --output clean.md

# 2. Pandoc with Korean reference doc
pandoc clean.md -o output.docx --reference-doc=korean-reference.docx --resource-path=. --highlight-style=kate

# 3. python-docx post-processing (see anthropic-docx Korean Style Guide)
python3 korean_postprocess.py output.docx
```

### Programmatic Usage (Python Import)

```python
from scripts.preprocess_mermaid import preprocess

clean_md = preprocess(
    "report.md",
    output_dir="diagrams",
    width=1200,
    background="transparent",
    scale=2,
    theme="neutral",
)
```

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `mmdc not found` | Mermaid CLI not installed | `npm install -g @mermaid-js/mermaid-cli` |
| `Could not find Chromium` | Puppeteer Chromium download failed | Set `PUPPETEER_EXECUTABLE_PATH=/path/to/chrome` or run `npx puppeteer browsers install chrome` |
| `TimeoutError` on large diagrams | Complex diagram exceeds render timeout | Add `--puppeteerConfigFile` with `{ "timeout": 60000 }` |
| Blurry PNG output | Low scale factor | Use `--scale 2` or higher |
| White background on transparent | mmdc version < 10 | Upgrade: `npm install -g @mermaid-js/mermaid-cli@latest` |
| `SyntaxError` in `.mmd` | Invalid Mermaid syntax | Validate at [mermaid.live](https://mermaid.live) before rendering |
| No blocks found | Wrong fence format | Blocks must use triple backtick + `mermaid` (no space, no caps) |

## See Also

- `anthropic-docx` -- DOCX creation with ImageRun embedding for rendered Mermaid PNGs
- `pandoc` -- Mode 7 Mermaid-aware conversion using this skill's script
- `architecture-diagram` -- Self-contained HTML+SVG architecture diagrams (no Mermaid source needed)
- `visual-explainer` -- Mermaid-in-HTML visual pages (browser renders natively)
- `flowchart` -- Create Mermaid flowchart syntax (source generation, not rendering)
