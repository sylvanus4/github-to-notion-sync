# Evolution Changelog — sales-rfp-interpreter

## Iteration 1

### Variants Designed
- **A (baseline)**: No changes — original skill after autoimprove
- **B (restructure + add-constraints)**: Added Step 0 input validation, deduplication logic, JSON output size limit, evidence requirement for risk flags
- **C (aggressive-compress)**: Merged Steps 1-2, removed taxonomy table inline, compressed constraints

### LLM-Judge Scores (5-dimension, 1-10)
| Variant | Accuracy | Procedure | Conciseness | Trigger Precision | Boundary Clarity | Composite |
|---------|----------|-----------|-------------|-------------------|------------------|-----------|
| A       | 7        | 7         | 7           | 8                 | 7                | 7.2       |
| B       | 8        | 9         | 7           | 8                 | 8                | 8.0       |
| C       | 7        | 7         | 8           | 7                 | 7                | 7.2       |

### Winner: Variant B
- **Rationale**: Input validation prevents wasted cycles on empty/corrupted inputs. Deduplication handles multi-department RFP overlap. Size constraint and evidence requirement improve downstream skill consumption.
- **Applied mutations**: Step 0 input validation, Step 2.5 deduplication, 2 new constraints (JSON size limit, verbatim evidence for risk flags)
