# Pandoc Lua Filters

Reusable Lua filters for Pandoc document transformations.

## Included Filters

| Filter | Purpose |
|--------|---------|
| `fix-korean-tables.lua` | Fill empty table cells, normalize Korean won sign |
| `korean-date-format.lua` | Convert ISO dates to Korean format in metadata |
| `signal-colors.lua` | Color-code BUY/SELL/HOLD signals for HTML/DOCX output |

## Usage

Apply a single filter:

```bash
pandoc input.md --lua-filter=filters/fix-korean-tables.lua -o output.docx
```

Chain multiple filters (applied in order):

```bash
pandoc input.md \
  --lua-filter=filters/fix-korean-tables.lua \
  --lua-filter=filters/korean-date-format.lua \
  --lua-filter=filters/signal-colors.lua \
  -o output.html
```

## Creating New Filters

See `references/lua-filters.md` for patterns and the Pandoc Lua filters guide.
Key types: `Str`, `Para`, `Table`, `Meta`, `Header`, `Span`, `Div`, `Code`, `CodeBlock`.
