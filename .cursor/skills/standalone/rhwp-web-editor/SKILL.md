---
name: rhwp-web-editor
description: >-
  Guide for embedding the rhwp HWP editor web component (@rhwp/editor) in web
  applications and using @rhwp/core for programmatic HWP document processing.
  Covers iframe-based editor embedding, WASM-based parser/renderer API, and
  hwpctl API compatibility layer for Hancom web editor migration. Use when the
  user asks to "embed HWP editor", "HWP web editor", "HWP 웹 에디터",
  "@rhwp/editor", "@rhwp/core", "hwpctl", "rhwp-web-editor", "HWP 웹 컴포넌트",
  "embed HWP in web app", or wants to integrate HWP viewing/editing in a web
  application. Do NOT use for CLI-based viewing (use rhwp-viewer). Do NOT use
  for CLI-based conversion (use rhwp-converter). Do NOT use for installation
  (use rhwp-setup).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
---
# rhwp Web Editor — HWP Editor Web Component Integration

Embed the rhwp HWP editor in web applications using `@rhwp/editor` (iframe-based
web component) or process HWP documents programmatically using `@rhwp/core`
(WASM parser/renderer).

## Packages

| Package | Type | Purpose |
|---------|------|---------|
| `@rhwp/editor` | Web component (iframe) | Full HWP editor UI for embedding |
| `@rhwp/core` | WASM module | Programmatic HWP parsing and rendering |

## Workflow

### Step 1: Install Packages

```bash
npm install @rhwp/editor @rhwp/core
```

### Step 2a: Embed @rhwp/editor (Full Editor UI)

The `@rhwp/editor` package provides an iframe-based editor that can be
embedded in 3 lines:

```html
<div id="editor" style="width:100%; height:100vh;"></div>
<script type="module">
  import { createEditor } from '@rhwp/editor';
  const editor = await createEditor('#editor');
</script>
```

The editor includes text editing (insert, delete, undo/redo), character and
paragraph formatting dialogs, table creation with row/column manipulation and
cell formula support, and an hwpctl-compatible API layer.

### Step 2b: Use @rhwp/core (Programmatic API)

The `@rhwp/core` package provides a WASM-based API for loading, parsing, and
rendering HWP documents. It requires a `measureTextWidth` polyfill and explicit
WASM initialization:

```javascript
import init, { HwpDocument } from '@rhwp/core';

// Required: text measurement polyfill
globalThis.measureTextWidth = (font, text) => {
  const ctx = document.createElement('canvas').getContext('2d');
  ctx.font = font;
  return ctx.measureText(text).width;
};

// Initialize WASM
await init({ module_or_path: '/rhwp_bg.wasm' });

// Load and render
const resp = await fetch('document.hwp');
const doc = new HwpDocument(new Uint8Array(await resp.arrayBuffer()));
document.getElementById('viewer').innerHTML = doc.renderPageSvg(0);
```

For Node.js server-side use, provide an equivalent `measureTextWidth` using
`canvas` or `@napi-rs/canvas` npm package.

### Step 3: hwpctl API Compatibility Layer

For projects migrating from Hancom's web editor (한컴 웹기안기), `rhwp` provides
an hwpctl-compatible API layer with 30 actions and Field API support:

**Supported Actions** (partial list): TableCreate, InsertText, CharShape,
ParagraphShape, and 26 more.

**Field API**: GetFieldList, PutFieldText, GetFieldText — enables template
data binding where HWP documents with named fields can be populated
programmatically.

**ParameterSet/ParameterArray API**: Matches the Hancom parameter passing
convention for complex operations.

This layer enables gradual migration from Hancom's proprietary API to the
open-source rhwp engine without rewriting all integration code.

### Step 4: Server-Side Rendering (Node.js)

For server-side or pipeline use, prefer the `rhwp` CLI over WASM in Node.js
for better performance and simpler setup:

```bash
rhwp export-svg document.hwp -o output/
```

If Node.js WASM is required (e.g., dynamic in-process rendering), provide the
`measureTextWidth` polyfill via `@napi-rs/canvas` and initialize WASM as shown
in Step 2b.

## Architecture

```
@rhwp/editor (iframe-based editor, 3-line embed)
  └── Full editor UI: toolbar, canvas, virtual scroll, zoom
      └── Internally uses @rhwp/core for parsing/rendering

@rhwp/core (WASM module)
  ├── init({ module_or_path }) → initialize WASM runtime
  ├── HwpDocument(Uint8Array) → document instance
  ├── doc.renderPageSvg(pageIndex) → SVG string
  └── hwpctl compatibility layer (30 Actions + Field API)
```

## Supported Rendering Features

- Paragraph layout (line spacing, indentation, alignment, tab stops)
- Tables (cell merging, border styles, cell formulas: SUM/AVG/PRODUCT)
- Multi-column layout
- Paragraph numbering/bullets
- Vertical text
- Header/footer (odd/even page separation)
- Master pages
- Equations (fractions, square roots, subscript/superscript)
- Object placement (TopAndBottom, treat-as-char, in-front-of/behind text)

## HWPUNIT Reference

- 1 inch = 7,200 HWPUNIT
- 1 inch = 25.4 mm
- 1 HWPUNIT ≈ 0.00353 mm

## Examples

### Quick Embed

User: "웹 페이지에 HWP 편집기 넣어줘"

```html
<div id="editor" style="width:100%;height:600px"></div>
<script type="module">
  import '@rhwp/editor';
  const editor = document.createElement('rhwp-editor');
  document.getElementById('editor').appendChild(editor);
</script>
```

### Load and Display a Document

```javascript
import init, { HwpDocument } from '@rhwp/core';

await init();
const buffer = await fetch('/doc.hwp').then(r => r.arrayBuffer());
const doc = new HwpDocument(new Uint8Array(buffer));
const svg = doc.renderPageSvg(0);
document.getElementById('viewer').innerHTML = svg;
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| WASM initialization fails | Ensure `init()` is called before `HwpDocument` |
| Editor iframe blank | Check CSP headers allow iframe embedding |
| `@rhwp/core` import error | Verify npm install completed: `npm ls @rhwp/core` |
| `@rhwp/editor` not rendering | Ensure target div has explicit width and height |
| `measureTextWidth` missing | Provide polyfill via `@napi-rs/canvas` for Node.js SSR |

## Best Practices

- Use `@rhwp/editor` when you need a complete editor interface with toolbar
- Use `@rhwp/core` when you need programmatic control or server-side processing
- For pipeline integration, prefer the CLI (`rhwp` command) over Node.js WASM for performance
- The hwpctl layer is for migration — prefer native @rhwp/core API for new code
