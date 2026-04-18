## Model Debate

Put multiple AI perspectives into a structured debate to stress-test ideas, find blind spots, and surface the strongest arguments.

### Usage

```
/model-debate "should we build vs buy an auth system?"
/model-debate --rounds 3 "monorepo vs polyrepo for our platform"
/model-debate --roles "CTO,PM,Security" "API key vs OAuth for our SDK"
```

### Workflow

1. **Frame** — Define the debate topic and assign opposing positions
2. **Argue** — Each side presents its strongest case with evidence
3. **Rebut** — Counter-arguments and stress-testing of weak points
4. **Synthesize** — Judge panel evaluates arguments, identifies consensus and open questions
5. **Verdict** — Produce a structured recommendation with confidence levels

### Execution

Read and follow the `autoreason` skill (`.cursor/skills/automation/autoreason/SKILL.md`) for 3-way tournament self-refinement with blind judging. For role-based multi-perspective analysis, use `role-dispatcher` (`.cursor/skills/role/role-dispatcher/SKILL.md`).

### Examples

Architecture debate:
```
/model-debate "serverless vs containers for our inference API"
```

Role-based debate:
```
/model-debate --roles "CTO,CFO,VP-Eng" "invest in internal tools vs hire more engineers"
```
