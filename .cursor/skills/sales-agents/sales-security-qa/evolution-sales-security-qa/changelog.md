# Evolution Changelog — sales-security-qa

## Iteration 1

### Variants Designed
- **A (baseline)**: No changes — original skill after autoimprove
- **B (restructure + add-constraints)**: Added Step 0 input validation (relevance check, batch splitting with sequential IDs, KB freshness warning), refined constraints (answer length by complexity tier, specific evidence links, batch response limit, verbatim quote requirement for factual claims)
- **C (aggressive-compress)**: Merged Steps 1-2, removed inline customer segment table, compressed constraints

### LLM-Judge Scores (5-dimension, 1-10)
| Variant | Accuracy | Procedure | Conciseness | Trigger Precision | Boundary Clarity | Composite |
|---------|----------|-----------|-------------|-------------------|------------------|-----------|
| A       | 7        | 7         | 7           | 8                 | 7                | 7.2       |
| B       | 8        | 9         | 8           | 8                 | 8                | 8.2       |
| C       | 7        | 7         | 8           | 7                 | 7                | 7.2       |

### Winner: Variant B
- **Rationale**: Input validation prevents wasted cycles on irrelevant questions routed to the security agent. Batch splitting with sequential IDs enables structured processing of multi-question RFP security sections. KB freshness warning prevents stale policy answers from reaching customers. Complexity-tiered answer length prevents padding simple yes/no questions while allowing depth for novel ones. Verbatim quote requirement strengthens evidence chain.
- **Applied mutations**: Step 0 input validation (relevance check, batch split, KB freshness), complexity-tiered answer length constraints, batch response limit (20 per run), verbatim evidence requirement for factual claims
