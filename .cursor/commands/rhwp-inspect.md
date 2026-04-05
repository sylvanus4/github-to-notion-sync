# /rhwp-inspect

Inspect the structure of an HWP/HWPX document.

## Arguments

- `file`: Path to the HWP/HWPX file (required)
- `mode`: Inspection mode — `layout` (default), `dump`, `overlay`
- `page`: Page number for layout/overlay mode (0-indexed, default: 0)
- `section`: Section number for dump mode (default: 0)
- `paragraph`: Paragraph number for dump mode (optional)

## Instruction

Read and follow the `rhwp-viewer` skill at `.cursor/skills/standalone/rhwp-viewer/SKILL.md`.

Select the appropriate viewing mode based on the `mode` argument:
- `layout` → Step 3c (Page Layout Mode)
- `dump` → Step 3d (Structure Dump Mode)
- `overlay` → Step 3e (Debug Overlay Mode)

Report key structural observations.

## Examples

```
/rhwp-inspect file=report.hwp
/rhwp-inspect file=report.hwp mode=dump section=2 paragraph=10
/rhwp-inspect file=report.hwp mode=overlay page=3
```
