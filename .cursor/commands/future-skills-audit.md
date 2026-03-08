## Future Skills Audit

Run a comprehensive audit across all 6 AI future skills areas, evaluating the project's maturity in each domain and generating an improvement roadmap.

### Usage

```
/future-skills-audit                      # Full audit across all 6 areas
/future-skills-audit quick                # Quick assessment (1 top finding per area)
/future-skills-audit <area>               # Audit a specific area only
```

Available areas: `workflow`, `pipeline`, `context`, `quality`, `systems`, `automation`

### Workflow

1. **AI Workflow Integration** — Assess how well AI is integrated into analysis workflows (via `ai-workflow-integrator`)
2. **No-Code Pipeline Building** — Review pipeline automation maturity (via `pipeline-builder`)
3. **Context Engineering** — Audit knowledge architecture freshness and completeness (via `context-engineer`)
4. **AI Quality Evaluation** — Check if quality gates exist and are effective (via `ai-quality-evaluator`)
5. **System Thinking** — Evaluate whether processes are designed as systems or ad-hoc tasks (via `system-thinker`)
6. **Strategic Automation** — Assess automation coverage and human-in-the-loop design (via `automation-strategist`)

### Execution

For each area, launch a subagent (up to 4 in parallel) that reads the corresponding skill and runs its audit/assessment mode. Aggregate results into a maturity scorecard:

| Area | Maturity (1-5) | Top Finding | Recommended Action |
|------|---------------|-------------|-------------------|
| AI Workflow | ? | ... | ... |
| Pipeline | ? | ... | ... |
| Context | ? | ... | ... |
| Quality | ? | ... | ... |
| Systems | ? | ... | ... |
| Automation | ? | ... | ... |

Maturity levels:
- **1 — Ad hoc**: No structure, fully manual
- **2 — Repeatable**: Some scripts, but manual triggers
- **3 — Defined**: Documented processes, some automation
- **4 — Managed**: Automated with monitoring and quality gates
- **5 — Optimized**: Feedback loops, continuous improvement, self-healing

### Skills Referenced

| Area | Skill | Path |
|------|-------|------|
| Workflow | ai-workflow-integrator | `.cursor/skills/ai-workflow-integrator/SKILL.md` |
| Pipeline | pipeline-builder | `.cursor/skills/pipeline-builder/SKILL.md` |
| Context | context-engineer | `.cursor/skills/context-engineer/SKILL.md` |
| Quality | ai-quality-evaluator | `.cursor/skills/ai-quality-evaluator/SKILL.md` |
| Systems | system-thinker | `.cursor/skills/system-thinker/SKILL.md` |
| Automation | automation-strategist | `.cursor/skills/automation-strategist/SKILL.md` |

### Examples

Full audit:
```
/future-skills-audit
```

Quick assessment:
```
/future-skills-audit quick
```

Single area deep dive:
```
/future-skills-audit quality
```
