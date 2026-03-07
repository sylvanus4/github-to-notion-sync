# HTML Artifact Structure

The HTML artifact must be single-file, self-contained. Use `templates/viewer.html` as the literal starting point — this reference shows the minimal structure when the template is not available.

## Single Artifact Structure

```html
<!DOCTYPE html>
<html>
<head>
  <!-- p5.js from CDN - always available -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js"></script>
  <style>
    /* All styling inline - clean, minimal */
    /* Canvas on top, controls below */
  </style>
</head>
<body>
  <div id="canvas-container"></div>
  <div id="controls">
    <!-- All parameter controls -->
  </div>
  <script>
    // ALL p5.js code inline here
    // Parameter objects, classes, functions
    // setup() and draw()
    // UI handlers
    // Everything self-contained
  </script>
</body>
</html>
```

**CRITICAL**: Single artifact. No external files, no imports (except p5.js CDN). Everything inline.

## Sidebar Structure

**1. Seed (FIXED)** — Always include exactly as shown in template:
- Seed display
- Prev/Next/Random/Jump buttons

**2. Parameters (VARIABLE)** — Create controls for the art:

```html
<div class="control-group">
    <label>Parameter Name</label>
    <input type="range" id="param" min="..." max="..." step="..." value="..." oninput="updateParam('param', this.value)">
    <span class="value-display" id="param-value">...</span>
</div>
```

Add as many control-group divs as there are parameters.

**3. Colors (OPTIONAL/VARIABLE)** — Include if the art needs adjustable colors:
- Add color pickers if users should control palette
- Skip if the art uses fixed colors or is monochrome

**4. Actions (FIXED)** — Always include exactly as shown:
- Regenerate button
- Reset button
- Download PNG button

## Requirements

- Seed controls must work (prev/next/random/jump/display)
- All parameters must have UI controls
- Regenerate, Reset, Download buttons must work
- Keep Anthropic branding (UI styling, not art colors)
