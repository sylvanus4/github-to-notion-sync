---
description: "Analyze a topic from 3-5 distinct professional perspectives, then synthesize areas of consensus and conflict"
argument-hint: "<topic or decision to analyze from multiple perspectives>"
---

# Multi-Perspective Analysis

Examine a topic through 3-5 distinct professional lenses, identify where they agree and disagree, then synthesize a balanced conclusion.

## Usage

```
/multi-perspective Should we build or buy an ML inference platform?
/multi-perspective Adopting Kubernetes for a 10-person startup
/multi-perspective --roles cto,pm,finance Launching a free tier for enterprise SaaS
/multi-perspective 자체 GPU 클러스터 구축 vs 클라우드 GPU 임대
/multi-perspective --deep Impact of EU AI Act on our product roadmap
```

## Your Task

User input: $ARGUMENTS

### Mode Selection

Parse `$ARGUMENTS` for flags:

- **No flags** — Auto-select 3-5 relevant perspectives (default)
- `--roles <role1,role2,...>` — Use specific roles (e.g., `cto,pm,finance,legal,ux`)
- `--deep` — Each perspective produces a longer analysis (paragraph instead of bullets)
- `--adversarial` — Force each perspective to argue against the others' positions

### Workflow

1. **Parse topic** — Extract the question or decision from `$ARGUMENTS`
2. **Select perspectives** — Choose 3-5 relevant professional roles:
   - Default selection based on topic domain (technical → CTO, PM, Security; business → CEO, Finance, Sales; product → PM, UX, Developer)
   - Override with `--roles` flag
3. **Generate each perspective** — For each role:
   - State the role's primary concern
   - List 3-5 key observations from that lens
   - Identify risks visible only from this perspective
   - State a recommendation
4. **Cross-reference** — Find areas of consensus and conflict across perspectives
5. **Synthesize** — Produce a balanced conclusion acknowledging trade-offs

### Output Format

```
## Multi-Perspective Analysis: [Topic]

### 🔧 [Role 1] Perspective
**Primary concern:** [What this role cares most about]
- [Observation 1]
- [Observation 2]
- [Observation 3]
**Recommendation:** [This role's preferred action]

### 📊 [Role 2] Perspective
...

### Consensus & Conflict
| Point | Agrees | Disagrees |
|-------|--------|-----------|
| [Topic A] | [Roles] | [Roles] |

### Synthesis
[Balanced conclusion acknowledging key trade-offs and a recommended path forward]
```

### Constraints

- Each perspective must be genuinely distinct — not restating the same point in different jargon
- At least one perspective must challenge the majority view (anti-sycophancy)
- Conflicts must be real trade-offs, not manufactured disagreements
- The synthesis must not simply side with the majority — it must weigh the quality of each argument

### Execution

Reference `role-dispatcher` (`.cursor/skills/role/role-dispatcher/SKILL.md`) for the multi-role analysis pattern. For parallel perspective generation, reference `workflow-parallel` (`.cursor/skills/workflow/workflow-parallel/SKILL.md`).
