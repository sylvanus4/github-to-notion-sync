# /rhwp-convert

Convert HWP/HWPX documents to SVG or PDF.

## Arguments

- `file`: Path to the HWP/HWPX file (required)
- `format`: Output format — `svg` (default) or `pdf`
- `pages`: Specific page numbers (optional, e.g., `0,1,2`)
- `output`: Output directory (default: `outputs/rhwp/{date}/`)

## Instruction

Read and follow the `rhwp-converter` skill at `.cursor/skills/standalone/rhwp-converter/SKILL.md`.

For batch conversion (directory of HWP files), use Step 3c of the skill.
For PDF output, use Step 3d (SVG → PDF conversion).

Report the conversion results table.

## Examples

```
/rhwp-convert file=report.hwp
/rhwp-convert file=report.hwp format=pdf
/rhwp-convert file=./docs/ format=svg   # batch mode
```
