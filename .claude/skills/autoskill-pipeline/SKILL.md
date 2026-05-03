---
name: autoskill-pipeline
description: >-
  Orchestrates the full AutoSkill adaptation: research analysis, multi-role
  strategy, skill creation, infrastructure, QA. Use when the user asks to "run
  autoskill pipeline", "autoskill adaptation", "adapt a learning framework",
  "AutoSkill 파이프라인", "학습 프레임워크 적용", "연구 논문 기반 스킬 생성". Do NOT use for evolution
  loop only (use autoskill-evolve), single-transcript extraction (use
  autoskill-extract), evolution status (use autoskill-status), or paper review
  without implementation (use paper-review).
---

# AutoSkill Pipeline

End-to-end meta-skill that orchestrates the complete AutoSkill adaptation process: research paper analysis, multi-role strategy assessment, skill creation, infrastructure integration, and quality assurance. Encapsulates the full workflow from analyzing an experience-driven lifelong learning methodology to implementing it as Cursor skills, rules, and commands.

## Instructions

### Pipeline Phases

The pipeline has 4 phases, each runnable independently or as a full sequence.

#### Phase 1: Research Analysis (`--phase analyze`)

1. **Paper Ingestion**: Download the research paper (PDF/arXiv URL), extract content using `anthropic-pdf` skill, and get structured overview via `alphaxiv-paper-lookup`
2. **Repository Analysis**: Use GitHub MCP or `defuddle` to analyze the paper's implementation repository — extract key modules, prompts, data models, and configuration
3. **Paper Review**: Run `paper-review` pipeline (Ingest → Review → PM Analysis → DOCX) to produce a structured Korean review with multi-perspective PM analysis
4. **Technical Documentation**: Create `docs/research/<topic>-analysis.md` with architecture diagrams (mermaid), module breakdown, key prompts, and gap analysis vs current infrastructure

**Skills used**: `anthropic-pdf`, `alphaxiv-paper-lookup`, `defuddle`, `paper-review`, `visual-explainer`

#### Phase 2: Strategy Assessment (`--phase strategy`)

1. **Multi-Role Analysis**: Run 6 role analyses in 2 parallel batches using the `role-dispatcher` pattern:
   - Batch 1 (4 parallel): CTO, PM, Developer, Security Engineer
   - Batch 2 (2 parallel): UX Designer, CSO
2. **Executive Briefing**: Synthesize role analyses using `executive-briefing` — identify cross-role consensus, conflicts, and priority actions
3. **PM Frameworks**: Apply product strategy frameworks via `pm-product-strategy`:
   - Lean Canvas for the adaptation project
   - SWOT analysis
   - PRD with OKRs and feature requirements
4. **Strategy Document**: Generate `docs/strategy/<topic>-adaptation.md` with decision matrix scoring each component on feasibility, impact, effort, and risk

**Skills used**: `role-cto`, `role-pm`, `role-developer`, `role-security-engineer`, `role-ux-designer`, `role-cso`, `executive-briefing`, `pm-product-strategy`, `pm-execution`, `anthropic-docx`

#### Phase 3: Implementation (`--phase implement`)

1. **Create Skills**: For each new skill identified in the strategy:
   - Create SKILL.md following the `create-skill` template
   - Adapt prompts from the research paper for the Cursor environment
   - Create reference documents in `references/` subdirectory
2. **Create Rules**: Write `.cursor/rules/*.mdc` files for behavioral integration
3. **Create Commands**: Write `.cursor/commands/*.md` trigger commands
4. **Extend Infrastructure**: Modify existing scripts and rules as specified in the strategy

**Skills used**: `create-skill`, `prompt-transformer`, `technical-writer`

#### Phase 4: Quality Assurance (`--phase optimize`)

1. **Skill Optimization**: Run `skill-optimizer` audit on all new skills
   - Check: frontmatter compliance, progressive disclosure, composability, trigger accuracy, redundancy
   - Fix all CRITICAL and HIGH severity findings
2. **Integration Test**: Run `autoskill-extractor` on a sample transcript to verify:
   - Extraction produces valid skill candidates
   - Judge decisions are reasonable
   - Merge flow produces valid SKILL.md updates
3. **Security Validation**: Run `semantic-guard` on all new skill content
   - Scan each new SKILL.md and reference doc for injection patterns, sensitive data
   - Block any skill that returns BLOCKED status
   - Log results in the pipeline report
4. **IA Baseline**: Run `intent-alignment-tracker` to establish baseline scores
   - For each new skill, record IA baseline as "pending first use"
   - For existing skills modified by the pipeline, record current IA score for comparison
   - Include IA section in the final pipeline report
5. **Report**: Generate final pipeline execution report

**Skills used**: `skill-optimizer`, `autoskill-evolve`, `ecc-verification-loop`, `semantic-guard`, `intent-alignment-tracker`

### Flags

```
/autoskill-pipeline --phase all          # full pipeline (default)
/autoskill-pipeline --phase analyze      # Phase 1 only
/autoskill-pipeline --phase strategy     # Phase 2 only
/autoskill-pipeline --phase implement    # Phase 3 only
/autoskill-pipeline --phase optimize     # Phase 4 only
/autoskill-pipeline --paper <url>        # paper URL (required for Phase 1)
/autoskill-pipeline --repo <url>         # GitHub repo URL (optional)
/autoskill-pipeline --topic <name>       # topic name for output paths
```

### Output Structure

```
outputs/<topic>/
  paper-extracted.md          # Phase 1: Paper content
  github-analysis.md          # Phase 1: Repo analysis
  paper-review.md             # Phase 1: Korean review

outputs/role-analysis/<topic>/
  role-cto.md                 # Phase 2: Role analyses
  role-pm.md
  role-developer.md
  role-security-engineer.md
  role-ux-designer.md
  role-cso.md

docs/research/<topic>-analysis.md     # Phase 1: Technical docs
docs/strategy/<topic>-adaptation.md   # Phase 2: Strategy document

.cursor/skills/<new-skills>/SKILL.md  # Phase 3: New skills
.cursor/rules/<new-rules>.mdc         # Phase 3: New rules
.cursor/commands/<new-commands>.md     # Phase 3: New commands
```


## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
