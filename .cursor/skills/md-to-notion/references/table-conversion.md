# Pipe Table to Bulleted List Conversion

Notion API does not render markdown pipe tables. They appear as raw text
with pipe characters. This reference defines the conversion algorithm.

## Detection

A pipe table block is a contiguous group of lines where:

1. Each line starts and ends with `|`
2. The second line is a separator: all cells match the pattern `-+`
   (optionally with `:` for alignment, e.g., `|:---|:---:|---:|`)

Example input:

```
| Priority | Owner | Task |
|----------|-------|------|
| P0 | 김팀장 | API 설계 |
| P1 | 박개발 | DB 마이그레이션 |
```

## Algorithm

1. **Split** the table block into lines
2. **Parse header row** (line 0): extract cell values, trim whitespace
3. **Skip separator row** (line 1)
4. **For each data row** (lines 2+):
   - Extract cell values, trim whitespace
   - Emit: `- **{Header1}**: {Value1} | **{Header2}**: {Value2} | ...`

## Output Format

The example above converts to:

```
- **Priority**: P0 | **Owner**: 김팀장 | **Task**: API 설계
- **Priority**: P1 | **Owner**: 박개발 | **Task**: DB 마이그레이션
```

## Edge Cases

- **Empty cells**: Omit the field entirely (`- **A**: val | **C**: val`)
- **Single-column table**: `- **Header**: value` (no pipe separator needed)
- **Nested pipes in values**: If a cell value contains `\|` (escaped pipe),
  preserve it as a literal `|` in the output
- **Tables inside code blocks**: Skip tables inside fenced code blocks
  (` ``` `) — only convert tables in regular content
- **Alignment markers** (`:---`, `:---:`, `---:`): Ignore them; they are
  visual-only and have no effect in bulleted list format

## Pseudocode

```
function convertTables(markdown):
  lines = markdown.split("\n")
  result = []
  i = 0
  inCodeBlock = false

  while i < lines.length:
    if lines[i].startsWith("```"):
      inCodeBlock = !inCodeBlock
      result.append(lines[i])
      i++
      continue

    if inCodeBlock:
      result.append(lines[i])
      i++
      continue

    if isTableStart(lines, i):
      headers = parseCells(lines[i])
      i += 2  // skip header + separator
      while i < lines.length and isTableRow(lines[i]):
        values = parseCells(lines[i])
        parts = []
        for j in range(min(headers.length, values.length)):
          if values[j].strip():
            parts.append("**" + headers[j].strip() + "**: " + values[j].strip())
        result.append("- " + " | ".join(parts))
        i++
    else:
      result.append(lines[i])
      i++

  return "\n".join(result)
```
