---
description: Expert panel content scoring, quality gate, editorial brain — rubrics, 90-point threshold
argument-hint: "[content path or paste] [domain hint]"
---

## Marketing Content Ops

Expert panel content quality: assemble experts, score against rubrics, iterate to 90+ composite score.

### Execution

Read and follow the `marketing-content-ops` skill (`.cursor/skills/marketing/marketing-content-ops/SKILL.md`). Use `experts/`, `scoring-rubrics/`, and `references/` as documented; run Python tools from `scripts/` when appropriate.

### Scripts

| Script | Purpose |
|--------|---------|
| `scripts/content-quality-gate.py` | Quality gate workflow |
| `scripts/content-quality-scorer.py` | Multi-expert scoring |
| `scripts/content-transform.py` | Content transformation |
| `scripts/editorial-brain.py` | Editorial reasoning |
| `scripts/quote-mining-engine.py` | Quote mining |

### Examples

```bash
# From repo root; deps: pip install anthropic openai tiktoken
python .cursor/skills/marketing/marketing-content-ops/scripts/content-quality-scorer.py --help
python .cursor/skills/marketing/marketing-content-ops/scripts/content-quality-gate.py --help
```
