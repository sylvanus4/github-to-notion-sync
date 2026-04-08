--- korean-date-format.lua
--- Convert ISO dates (YYYY-MM-DD) to Korean format (YYYY년 MM월 DD일) in metadata.
---
--- Usage:
---   pandoc input.md --lua-filter=filters/korean-date-format.lua -o output.docx

function Meta(meta)
  if meta.date then
    local date_str = pandoc.utils.stringify(meta.date)
    local y, m, d = date_str:match("^(%d%d%d%d)-(%d%d)-(%d%d)$")
    if y and m and d then
      meta.date = pandoc.MetaInlines{
        pandoc.Str(y .. "년 " .. m .. "월 " .. d .. "일")
      }
    end
  end
  return meta
end
