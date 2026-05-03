---
name: onboarding-accelerator
description: >-
  Generate a complete "new developer kit" by orchestrating 8 existing skills:
  architecture analysis, code ownership maps, interactive diagrams, study
  materials, getting-started guides, environment setup docs, and
  infrastructure overview. Produces a comprehensive onboarding package in
  docs/onboarding/. Use when the user asks about "onboarding", "new
  developer", "onboard", "getting started kit", "온보딩", "신규 개발자", "new team
  member", "developer onboarding", or wants to create documentation for
  someone joining the project. Do NOT use for code review (use deep-review),
  running the dev environment (use local-dev-runner), or creating study
  quizzes only (use docs-tutor).
---

# Onboarding Accelerator — New Developer Kit Generator

Turn weeks of onboarding into hours. Automatically generates a comprehensive onboarding package by analyzing the codebase and orchestrating 8 specialized skills.

## Usage

```
/onboarding-accelerator                        # full onboarding kit
/onboarding-accelerator --role frontend        # frontend-focused kit
/onboarding-accelerator --role backend         # backend-focused kit
/onboarding-accelerator --role fullstack       # everything (default)
/onboarding-accelerator --section architecture # specific section only
/onboarding-accelerator --output docs/onboarding/  # custom output path
```

## Pipeline Overview

```
Group A (parallel): Analyze
  ├─ deep-review          → Architecture scan, component boundaries, patterns
  └─ codebase-archaeologist → Code ownership, bus factor, churn hotspots

    ↓

Group B (parallel): Visualize
  ├─ visual-explainer     → Interactive architecture diagrams
  └─ design-architect     → Design system overview, UI patterns

    ↓

Group C (parallel): Document
  ├─ technical-writer     → Getting started guide, conventions doc
  └─ docs-tutor-setup     → StudyVault with concept notes and quizzes

    ↓

Group D (parallel): Environment
  ├─ local-dev-runner     → Dev environment setup instructions
  └─ sre-devops-expert    → Service topology, infra overview
```

## Workflow

### Step 1: Determine Scope

Parse user input for:
- **Role focus**: `frontend | backend | fullstack` (default: fullstack)
- **Specific section**: maps to pipeline groups as follows:

  | `--section` value | Groups run |
  |-------------------|-----------|
  | `architecture` | A + B |
  | `docs` | A + C |
  | `environment` | D |
  | `full` (default) | A + B + C + D |

- **Output path**: where to save the kit (default: `docs/onboarding/`). Create with `mkdir -p` if it doesn't exist.

### Step 2: Group A — Analyze (Parallel)

Launch 2 sub-agents:

**Agent 1: deep-review (architecture scan)**
- `subagent_type: generalPurpose`, `model: fast`, `readonly: true`
- Prompt: Read and follow `.cursor/skills/review/deep-review/SKILL.md`. Scope: full project. Focus on architecture — identify component boundaries, data flow patterns, key abstractions, shared libraries, and design decisions. Return a structured architecture summary.
- Expected output: component list, dependency graph, key patterns, tech stack

**Agent 2: codebase-archaeologist (ownership analysis)**
- `subagent_type: generalPurpose`, `model: fast`, `readonly: true`
- Prompt: Read and follow `.cursor/skills/review/codebase-archaeologist/SKILL.md`. Run `--mode full` on the entire project. Return ownership map, bus factor, and top 10 churn hotspots.
- Expected output: who-to-ask-about-what map, key contributors per module

### Step 3: Group B — Visualize (Parallel)

**Agent 3: visual-explainer (architecture diagrams)**
- Prompt: Using the architecture analysis from Group A, generate an interactive HTML page showing:
  - System architecture diagram (services, databases, message queues)
  - Frontend component tree
  - API endpoint map
  - Data flow for key user journeys
- Save to: `{output}/architecture-overview.html`

**Agent 4: design-architect (design system overview)** (skip if no `.tsx`, `.jsx`, `.css`, or `.scss` files exist in the project)
- Prompt: Read and follow `.cursor/skills/frontend/design-architect/SKILL.md`. Produce a design system summary: color palette, typography, component library, layout patterns.
- Expected output: design system reference for the onboarding kit

### Step 4: Group C — Document (Parallel)

**Agent 5: technical-writer (getting started guide)**
- Prompt: Read and follow `.cursor/skills/standalone/technical-writer/SKILL.md`. Using all analysis from Groups A and B, create:
  - `{output}/01-getting-started.md` — Prerequisites, clone, setup, first run
  - `{output}/02-architecture.md` — Architecture overview with diagrams
  - `{output}/03-conventions.md` — Coding conventions, naming, file structure
  - `{output}/04-who-to-ask.md` — Code ownership map from codebase-archaeologist
  - `{output}/05-key-workflows.md` — Common development workflows (commit, PR, deploy)

**Agent 6: docs-tutor-setup (study vault)**
- Prompt: Read and follow `.cursor/skills/standalone/docs-tutor-setup/SKILL.md`. Transform the generated docs into a StudyVault with concept notes, practice questions, and a learning dashboard.
- Save to: `{output}/study-vault/`

### Step 5: Group D — Environment (Parallel)

**Agent 7: local-dev-runner (environment setup)**
- `readonly: true`
- Prompt: Read and follow `.cursor/skills/infra/local-dev-runner/SKILL.md`. Document the exact steps to set up the local development environment. Include prerequisites, services, ports, common issues and solutions.
- Integrate into: `{output}/01-getting-started.md`

**Agent 8: sre-devops-expert (infrastructure overview)**
- `readonly: true`
- Prompt: Read and follow `.cursor/skills/infra/sre-devops-expert/SKILL.md`. Produce a service topology document: all services, their roles, communication patterns, deployment targets, and monitoring endpoints.
- Save to: `{output}/06-infrastructure.md`

### Step 6: Assemble Kit

Combine all deliverables into a structured package:

```
docs/onboarding/
├── README.md                    ← Table of contents + how to use this kit
├── 01-getting-started.md        ← Prerequisites, setup, first run
├── 02-architecture.md           ← Architecture with embedded diagrams
├── 03-conventions.md            ← Coding standards, naming, patterns
├── 04-who-to-ask.md             ← Code ownership + contact map
├── 05-key-workflows.md          ← Git, CI/CD, review, deploy workflows
├── 06-infrastructure.md         ← Service topology, infra overview
├── architecture-overview.html   ← Interactive architecture diagrams
└── study-vault/                 ← StudyVault with quizzes
    ├── concepts/
    ├── questions/
    └── dashboard.md
```

Generate `README.md` as the entry point linking all sections with recommended reading order.

### Step 7: Onboarding Report

```
Onboarding Accelerator Report
===============================
Role focus: [frontend|backend|fullstack]
Output: [output path]

Deliverables:
  ✓ Getting Started Guide        — 01-getting-started.md
  ✓ Architecture Overview        — 02-architecture.md + .html
  ✓ Coding Conventions           — 03-conventions.md
  ✓ Code Ownership Map           — 04-who-to-ask.md
  ✓ Key Workflows                — 05-key-workflows.md
  ✓ Infrastructure Overview      — 06-infrastructure.md
  ✓ Interactive Diagrams         — architecture-overview.html
  ✓ StudyVault                   — study-vault/ ([N] concepts, [N] questions)

Skills used: [8]
Estimated onboarding time saved: ~[N] days

Suggested reading order for new developer:
  1. README.md (5 min)
  2. 01-getting-started.md (30 min setup)
  3. 02-architecture.md (20 min read)
  4. architecture-overview.html (10 min explore)
  5. 04-who-to-ask.md (5 min reference)
  6. study-vault/ (self-paced quizzes)
```

## Examples

### Example 1: Full onboarding kit

User: `/onboarding-accelerator`

8 skills run across 4 groups. Produces 7 markdown files, 1 interactive HTML page, and a StudyVault with concept notes and quizzes.

### Example 2: Frontend-focused onboarding

User: `/onboarding-accelerator --role frontend`

Skips backend infrastructure details. Focuses on React component architecture, design system, and frontend conventions.

### Example 3: Single section

User: `/onboarding-accelerator --section architecture`

Runs only Groups A and B. Produces architecture analysis and interactive diagrams.

## Error Handling

| Scenario | Action |
|----------|--------|
| Project has no docs/ directory | Create the output directory |
| codebase-archaeologist finds shallow git history | Warn; use available history |
| Design system not found | Skip design-architect; note in report |
| Sub-agent produces empty output | Re-run once with more specific prompt |
| Output directory already has content | Check each file with `test -f`. If exists, ask user via AskQuestion tool whether to overwrite or skip. |
| Very large project (1000+ files) | Limit analysis to key directories; note coverage in report |

## Troubleshooting

- **Empty architecture output**: The deep-review agent needs files to analyze. Verify `git diff --name-only` returns results or specify a target directory.
- **design-architect skipped unexpectedly**: The skill auto-detects frontend files (`.tsx`, `.css`). If your project uses `.vue` or `.svelte`, the detection may miss them -- run with `--section architecture` to force Group B.
- **StudyVault empty**: docs-tutor-setup requires markdown input files. Ensure Group C (technical-writer) completes before Group C (docs-tutor-setup) runs.
- **Output directory permission error**: Verify write permissions on the output path. Try a different path with `--output ./onboarding-kit/`.


## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
