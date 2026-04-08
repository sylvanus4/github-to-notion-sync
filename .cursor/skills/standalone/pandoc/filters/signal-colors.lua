--- signal-colors.lua
--- Highlight BUY/SELL/HOLD signals with colored spans for HTML/DOCX output.
---
--- Usage:
---   pandoc input.md --lua-filter=filters/signal-colors.lua -o output.html

local signal_colors = {
  BUY      = "#22c55e",  -- green
  SELL     = "#ef4444",  -- red
  HOLD     = "#f59e0b",  -- amber
  STRONG   = "#16a34a",  -- dark green
  WEAK     = "#dc2626",  -- dark red
  NEUTRAL  = "#6b7280",  -- gray
  ["매수"] = "#22c55e",
  ["매도"] = "#ef4444",
  ["보유"] = "#f59e0b",
}

function Str(el)
  local color = signal_colors[el.text]
  if color then
    return pandoc.Span(
      {pandoc.Strong{pandoc.Str(el.text)}},
      {style = "color: " .. color .. "; font-weight: bold;"}
    )
  end
  return nil
end
