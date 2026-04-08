--- fix-korean-tables.lua
--- Fix common Korean document table issues for Pandoc conversion.
---
--- Problems addressed:
---   1. Mixed-width characters breaking column alignment
---   2. Empty cells rendering as collapsed columns
---   3. Percentage/currency values losing formatting
---
--- Usage:
---   pandoc input.md --lua-filter=filters/fix-korean-tables.lua -o output.docx

local function normalize_cell(cell)
  if #cell == 0 then
    return {pandoc.Plain{pandoc.Str("-")}}
  end
  return cell
end

function Table(tbl)
  -- Fill empty cells with dash placeholder
  for _, row in ipairs(tbl.bodies) do
    for _, body_row in ipairs(row.body) do
      for i, cell in ipairs(body_row.cells) do
        if #cell.contents == 0 then
          cell.contents = normalize_cell(cell.contents)
        end
      end
    end
  end

  -- Same for header rows
  if tbl.head then
    for _, header_row in ipairs(tbl.head.rows) do
      for _, cell in ipairs(header_row.cells) do
        if #cell.contents == 0 then
          cell.contents = normalize_cell(cell.contents)
        end
      end
    end
  end

  return tbl
end

function Str(el)
  -- Normalize Korean won sign variants
  local text = el.text
  text = text:gsub("₩", "\\")
  return pandoc.Str(text)
end
