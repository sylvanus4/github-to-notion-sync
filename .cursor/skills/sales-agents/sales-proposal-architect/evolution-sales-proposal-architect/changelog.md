# Evolution Changelog — sales-proposal-architect

## Iteration 1

### Variants Designed
- **A (baseline)**: No changes — original skill after autoimprove
- **B (restructure + add-constraints)**: Added Step 0 input validation (minimum input checks, requirement count validation, security Q&A confidence gate), refined constraints (proposal length target 8-12 pages, value proposition deduplication, architecture diagram naming verification against KB, security claim traceability)
- **C (aggressive-compress)**: Merged Steps 1-2, removed inline segment template table, compressed constraints

### LLM-Judge Scores (5-dimension, 1-10)
| Variant | Accuracy | Procedure | Conciseness | Trigger Precision | Boundary Clarity | Composite |
|---------|----------|-----------|-------------|-------------------|------------------|-----------|
| A       | 7        | 7         | 7           | 8                 | 7                | 7.2       |
| B       | 8        | 8         | 7           | 8                 | 8                | 7.8       |
| C       | 7        | 7         | 8           | 7                 | 7                | 7.2       |

### Winner: Variant B
- **Rationale**: Input validation prevents generating proposals from insufficient context (empty inputs, too-few requirements, low-confidence security answers). Proposal length constraint keeps output executive-friendly. Deduplication prevents repeating the same value proposition across sections (common in multi-section proposals). Architecture diagram naming verification ensures only current ThakiCloud offering names appear in customer-facing documents. Security claim traceability links every security statement to its source Q&A answer.
- **Applied mutations**: Step 0 input validation (minimum input, requirement count, security confidence gate), 4 new constraints (proposal length, deduplication, architecture naming, security traceability)
