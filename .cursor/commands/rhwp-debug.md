# /rhwp-debug

Debug HWP/HWPX document rendering or structure issues.

## Arguments

- `file`: Path to the HWP/HWPX file with the issue (required)
- `compare`: Path to a second file for IR diff comparison (optional)
- `page`: Page number to focus on (0-indexed, optional)
- `section`: Section number (optional)
- `paragraph`: Paragraph number (optional)

## Instruction

Read and follow the `rhwp-debug` skill at `.cursor/skills/standalone/rhwp-debug/SKILL.md`.

Follow the systematic 3-step debugging process:
1. Debug overlay → identify problem area visually
2. Page layout dump → check element positioning
3. IR dump → inspect specific properties

If `compare` is provided, also run IR diff (Step 3).

Report findings in the structured table format.

## Examples

```
/rhwp-debug file=broken.hwp
/rhwp-debug file=broken.hwp page=5
/rhwp-debug file=doc.hwpx compare=doc.hwp
/rhwp-debug file=doc.hwp section=2 paragraph=45
```
