# Pandoc Lua Filter Patterns

Reusable Lua filter patterns for Korean document processing, financial reports,
and pipeline integration.

Reference: <https://pandoc.org/lua-filters.html>

## Filter Basics

Lua filters receive the Pandoc AST and can modify it element-by-element.
Filters are applied via `--lua-filter=filter.lua` and can be chained.

```bash
pandoc input.md --lua-filter=filter1.lua --lua-filter=filter2.lua -o out.docx
```

Filters execute in order; each filter sees the output of the previous one.

---

## Pattern 1: Korean Date Formatter

Replace ISO dates (YYYY-MM-DD) with Korean-formatted dates in body text.

```lua
-- filters/korean-date.lua
function Str(el)
  local y, m, d = el.text:match("^(%d%d%d%d)%-(%d%d)%-(%d%d)$")
  if y then
    return pandoc.Str(y .. "년 " .. tonumber(m) .. "월 " .. tonumber(d) .. "일")
  end
end
```

Usage: `pandoc report.md --lua-filter=filters/korean-date.lua -o report.docx`

---

## Pattern 2: Financial Number Formatter

Format large numbers with comma separators (1234567 -> 1,234,567).

```lua
-- filters/comma-numbers.lua
function Str(el)
  local num = el.text:match("^(%d+)$")
  if num and #num >= 4 then
    local formatted = num:reverse():gsub("(%d%d%d)", "%1,"):reverse()
    if formatted:sub(1, 1) == "," then
      formatted = formatted:sub(2)
    end
    return pandoc.Str(formatted)
  end
end
```

---

## Pattern 3: Stock Ticker Highlighter

Wrap stock ticker symbols (e.g., $AAPL, $TSLA) in bold + colored span.

```lua
-- filters/ticker-highlight.lua
function Str(el)
  local ticker = el.text:match("^%$([A-Z]+)$")
  if ticker then
    return pandoc.Strong(pandoc.Str("$" .. ticker))
  end
end
```

For HTML output with color:

```lua
function Str(el)
  local ticker = el.text:match("^%$([A-Z]+)$")
  if ticker then
    return pandoc.Span(
      pandoc.Str("$" .. ticker),
      pandoc.Attr("", {"ticker"}, {{"style", "color: #0066cc; font-weight: bold;"}})
    )
  end
end
```

---

## Pattern 4: Auto-Generate Table of Contents Metadata

Inject TOC metadata if the document has 3+ headings.

```lua
-- filters/auto-toc.lua
function Pandoc(doc)
  local heading_count = 0
  doc:walk({
    Header = function(el)
      heading_count = heading_count + 1
    end
  })
  if heading_count >= 3 then
    doc.meta["toc"] = true
    doc.meta["toc-depth"] = 3
  end
  return doc
end
```

---

## Pattern 5: Admonition Boxes (Korean Labels)

Convert fenced divs like `::: warning` into formatted callout boxes
with Korean labels.

```lua
-- filters/korean-admonitions.lua
local labels = {
  warning = "⚠️ 경고",
  note    = "📝 참고",
  tip     = "💡 팁",
  danger  = "🚨 위험",
  info    = "ℹ️ 정보"
}

function Div(el)
  for class, label in pairs(labels) do
    if el.classes:includes(class) then
      local header = pandoc.Para(pandoc.Strong(pandoc.Str(label)))
      table.insert(el.content, 1, header)
      el.classes = {"callout-" .. class}
      return el
    end
  end
end
```

Markdown usage:

```markdown
::: warning
이 전략은 높은 변동성 환경에서 손실 위험이 있습니다.
:::
```

---

## Pattern 6: Remove Draft Sections

Strip any section whose heading contains "[DRAFT]" or "[초안]".

```lua
-- filters/remove-drafts.lua
function Header(el)
  local text = pandoc.utils.stringify(el)
  if text:find("%[DRAFT%]") or text:find("%[초안%]") then
    return {}
  end
end
```

For removing the entire section (heading + body until next same-level heading):

```lua
-- filters/remove-draft-sections.lua
function Pandoc(doc)
  local dominated = {}
  local dominated_level = nil

  local new_blocks = {}
  for _, block in ipairs(doc.blocks) do
    if block.t == "Header" then
      local text = pandoc.utils.stringify(block)
      if text:find("%[DRAFT%]") or text:find("%[초안%]") then
        dominated_level = block.level
      elseif dominated_level and block.level <= dominated_level then
        dominated_level = nil
        table.insert(new_blocks, block)
      end
    end
    if not dominated_level then
      table.insert(new_blocks, block)
    end
  end

  doc.blocks = new_blocks
  return doc
end
```

---

## Pattern 7: Signal Color Coding

Color-code BUY/SELL/HOLD signals in financial reports.

```lua
-- filters/signal-colors.lua
local signal_colors = {
  BUY   = "#22c55e",  -- green
  SELL  = "#ef4444",  -- red
  HOLD  = "#eab308",  -- yellow
  ["매수"] = "#22c55e",
  ["매도"] = "#ef4444",
  ["보유"] = "#eab308"
}

function Str(el)
  local color = signal_colors[el.text]
  if color then
    return pandoc.Span(
      pandoc.Strong(pandoc.Str(el.text)),
      pandoc.Attr("", {"signal"}, {{"style", "color: " .. color .. ";"}})
    )
  end
end
```

---

## Pattern 8: Metadata Injection

Inject project-standard metadata into every document.

```lua
-- filters/inject-metadata.lua
function Meta(meta)
  if not meta.author then
    meta.author = {pandoc.Inlines{pandoc.Str("ThakiCloud AI Analytics")}}
  end
  if not meta.lang then
    meta.lang = pandoc.Inlines{pandoc.Str("ko-KR")}
  end
  if not meta.date then
    meta.date = pandoc.Inlines{pandoc.Str(os.date("%Y-%m-%d"))}
  end
  return meta
end
```

---

## Pattern 9: Image Path Rewriter

Rewrite relative image paths for different output targets.

```lua
-- filters/rewrite-images.lua
-- Usage: pandoc input.md --lua-filter=filters/rewrite-images.lua
--        -M image-prefix=https://cdn.example.com/images/

function Image(el)
  local prefix = PANDOC_DOCUMENT.meta["image-prefix"]
  if prefix and not el.src:match("^https?://") then
    el.src = pandoc.utils.stringify(prefix) .. el.src
  end
  return el
end
```

---

## Pattern 10: Word Count Footer

Append a word count line to the document.

```lua
-- filters/word-count-footer.lua
function Pandoc(doc)
  local word_count = pandoc.utils.stringify(doc):gsub("%S+", ""):len()
  -- rough word count via space counting
  local body_text = pandoc.utils.stringify(doc)
  local count = 0
  for _ in body_text:gmatch("%S+") do
    count = count + 1
  end

  local footer = pandoc.Para(pandoc.Emph(
    pandoc.Str("총 단어 수: " .. tostring(count))
  ))
  table.insert(doc.blocks, pandoc.HorizontalRule())
  table.insert(doc.blocks, footer)
  return doc
end
```

---

## Composing Filters

Filters chain left-to-right. Order matters when filters depend on
each other's output.

Recommended order for financial reports:

```bash
pandoc input.md \
  --lua-filter=filters/inject-metadata.lua \
  --lua-filter=filters/remove-drafts.lua \
  --lua-filter=filters/korean-date.lua \
  --lua-filter=filters/comma-numbers.lua \
  --lua-filter=filters/signal-colors.lua \
  --lua-filter=filters/korean-admonitions.lua \
  --lua-filter=filters/word-count-footer.lua \
  -o report.docx
```

Or use a defaults file (see `cli-recipes.md`):

```yaml
# defaults/financial-report.yaml
filters:
  - filters/inject-metadata.lua
  - filters/remove-drafts.lua
  - filters/korean-date.lua
  - filters/comma-numbers.lua
  - filters/signal-colors.lua
  - filters/korean-admonitions.lua
  - filters/word-count-footer.lua
```

---

## Debugging Filters

Inspect the AST to understand what your filter receives:

```bash
pandoc input.md -t json | python -m json.tool | head -100
```

Add debug logging inside a filter:

```lua
function Header(el)
  io.stderr:write("DEBUG Header level=" .. el.level
    .. " text=" .. pandoc.utils.stringify(el) .. "\n")
  return el
end
```

Test a single filter in isolation:

```bash
echo "test $AAPL 2024-01-15" | pandoc -f markdown --lua-filter=filters/ticker-highlight.lua -t html
```
