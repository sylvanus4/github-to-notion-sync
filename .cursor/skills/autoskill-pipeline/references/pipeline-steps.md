# AutoSkill Pipeline — Detailed Step Reference

## Pipeline Execution Flow

```mermaid
flowchart TD
    subgraph P1 ["Phase 1: Research Analysis"]
        P1A[Download Paper PDF] --> P1B[Extract with anthropic-pdf]
        P1A --> P1C[alphaxiv-paper-lookup]
        P1D[GitHub Repo Analysis] --> P1E[Extract Prompts & Models]
        P1B --> P1F[paper-review Pipeline]
        P1C --> P1F
        P1E --> P1G[Technical Documentation]
        P1F --> P1G
    end

    subgraph P2 ["Phase 2: Strategy Assessment"]
        P2A["Role Analysis Batch 1\n(CTO, PM, Dev, Security)"]
        P2B["Role Analysis Batch 2\n(UX, CSO)"]
        P2A --> P2C[Executive Briefing]
        P2B --> P2C
        P2C --> P2D["PM Frameworks\n(Lean Canvas, SWOT, PRD)"]
        P2D --> P2E[Strategy Document + DOCX]
    end

    subgraph P3 ["Phase 3: Implementation"]
        P3A[Create Skills] --> P3D[Extend Infrastructure]
        P3B[Create Rules] --> P3D
        P3C[Create Commands] --> P3D
    end

    subgraph P4 ["Phase 4: Quality Assurance"]
        P4A[skill-optimizer Audit] --> P4B[Fix CRITICAL/HIGH]
        P4B --> P4C[Integration Test]
        P4C --> P4D[Final Report]
    end

    P1 --> P2 --> P3 --> P4
```

## Skill Composition Matrix

| Phase | Skills Used | Parallelism |
|-------|------------|-------------|
| 1A | `anthropic-pdf` | — |
| 1B | `alphaxiv-paper-lookup`, `defuddle` | Parallel with 1A |
| 1C | `paper-review` (PM sub-skills) | After 1A+1B |
| 1D | `visual-explainer`, `technical-writer` | After 1C |
| 2A | `role-cto`, `role-pm`, `role-developer`, `role-security-engineer` | 4 parallel |
| 2B | `role-ux-designer`, `role-cso` | 2 parallel |
| 2C | `executive-briefing`, `pm-product-strategy`, `pm-execution` | Sequential |
| 2D | `anthropic-docx` | After 2C |
| 3A | `create-skill`, `prompt-transformer` | Per-skill parallel |
| 3B | Direct file creation | Sequential |
| 3C | Direct file creation | Sequential |
| 4A | `skill-optimizer` | Per-skill sequential |
| 4B | `autoskill-evolve` (dry-run test) | After 4A |

## Error Recovery

- Phase 1 failure: Can be retried independently
- Phase 2 failure: Can skip individual roles and proceed
- Phase 3 failure: Skill creation is idempotent (overwrite-safe)
- Phase 4 failure: Audit findings are informational, don't block

## Estimated Runtime

| Phase | Time | Notes |
|-------|------|-------|
| Phase 1 | 15-20 min | PDF download + paper review |
| Phase 2 | 10-15 min | 6 parallel role analyses |
| Phase 3 | 25-35 min | Skill creation + infrastructure |
| Phase 4 | 10-15 min | Audit + integration test |
| **Total** | **60-85 min** | With parallel execution |
