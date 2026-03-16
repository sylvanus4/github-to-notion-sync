# Pipe Table to Notion Table Conversion

Notion API does not render standard markdown pipe tables. They appear as raw
text with pipe characters. This reference documents the conversion to Notion's
`<table>` HTML block format, which renders as a proper structured table.

## Detection

A pipe table block is a contiguous group of lines where:

1. Each line starts and ends with `|`
2. The second line is a separator: all cells match `-+`
   (optionally with `:` for alignment)

Example input:

```
| Priority | Owner | Task |
|----------|-------|------|
| P0 | 김팀장 | API 설계 |
| P1 | 박개발 | DB 마이그레이션 |
```

## Output Format — Notion `<table>` Block

```html
<table header-row="true">
	<tr>
		<td>Priority</td>
		<td>Owner</td>
		<td>Task</td>
	</tr>
	<tr>
		<td>P0</td>
		<td>김팀장</td>
		<td>API 설계</td>
	</tr>
	<tr>
		<td>P1</td>
		<td>박개발</td>
		<td>DB 마이그레이션</td>
	</tr>
</table>
```

Key points:
- `header-row="true"` makes the first row a bold header in Notion
- Each cell uses `<td>`, even for headers
- Markdown formatting inside cells (bold, code, links) is preserved
- Tab indentation is conventional but not required

## Bundled Script

The conversion is automated by `scripts/convert_tables.py`. The script:

1. Scans lines sequentially, tracking fenced code block state
2. When a table-start pattern is detected outside code blocks, collects all
   contiguous table rows
3. Converts the collected rows to a `<table>` block
4. Leaves everything else (including tables inside code blocks) untouched

Usage:

```bash
python scripts/convert_tables.py [--threshold 15000] file1.md file2.md
```

Outputs JSON files to `/tmp/notion_page_N.json` with converted content.

## Edge Cases

- **Tables inside code blocks**: Skipped entirely (preserves ASCII art, examples)
- **Empty cells**: Rendered as empty `<td></td>`
- **Mismatched column counts**: Padded with empty cells to match header width
- **Single-column table**: Still converted to `<table>` format
- **Alignment markers** (`:---`, `:---:`, `---:`): Stripped during conversion;
  Notion tables do not support per-cell alignment
- **No separator row**: Not treated as a table (plain text preserved)
