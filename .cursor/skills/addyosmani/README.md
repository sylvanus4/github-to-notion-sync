# addyosmani/agent-skills — Imported Skill Package

**Source**: [github.com/addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
**Commit**: `c0c9fb46a2bf23bb2e4e1241bbdecbc27c35542f` (2026-04-05)
**Imported**: 2026-04-06
**Namespace**: `.cursor/skills/addyosmani/`

## Overview

20 general-purpose software engineering skills from Addy Osmani's agent-skills repository, adapted for this project with namespace isolation and overlap routing.

These skills provide **process philosophy and methodology** — complementing our existing project-specific skills that integrate with concrete tools (Playwright, FastAPI, TDS, SEFO, etc.).

## Skill List

| Skill | Description |
|---|---|
| api-and-interface-design | Design stable, well-documented APIs with Contract First and Hyrum's Law awareness |
| browser-testing-with-devtools | Test and debug browser applications using DevTools and real browser workflows |
| ci-cd-and-automation | Set up CI/CD pipelines, automate quality gates, and manage deployment workflows |
| code-review-and-quality | Multi-axis code review: correctness, readability, architecture, security, performance |
| code-simplification | Refactor code for clarity without changing behavior — reduce complexity and duplication |
| context-engineering | Optimize agent context setup: AGENTS.md, file structure, progressive disclosure |
| debugging-and-error-recovery | Systematic root-cause debugging with hypothesis-driven fault isolation |
| deprecation-and-migration | Manage deprecation, sunset old APIs, and migrate users between implementations |
| documentation-and-adrs | Write Architecture Decision Records, API docs, and developer-facing documentation |
| frontend-ui-engineering | Build production-quality UIs with accessibility, performance, and component architecture |
| git-workflow-and-versioning | Structure git commits, branches, conflict resolution, and versioning practices |
| idea-refine | Refine ideas through structured divergent and convergent thinking phases |
| incremental-implementation | Deliver changes incrementally — slice large features into reviewable units |
| performance-optimization | Measure and optimize application performance: profiling, CWV, anti-patterns |
| planning-and-task-breakdown | Break work into ordered, verifiable tasks with scope estimation and parallelism |
| security-and-hardening | Secure development practices: OWASP Top 10, input validation, threat modeling |
| shipping-and-launch | Prepare production launches: checklists, monitoring, staged rollout, rollback strategy |
| spec-driven-development | Write structured specifications before coding — requirements, constraints, acceptance |
| test-driven-development | Drive development with failing tests first, then implementation, then refactoring |
| using-agent-skills | Meta-skill for discovering and invoking other agent skills at session start |

## Agents

| Agent Persona | Role |
|---|---|
| code-reviewer.md | Code review specialist with multi-dimension analysis |
| security-auditor.md | Security-focused reviewer for vulnerability detection |
| test-engineer.md | Testing specialist for coverage and quality assessment |

## References

| Checklist | Purpose |
|---|---|
| accessibility-checklist.md | WCAG and a11y compliance checklist |
| performance-checklist.md | Performance optimization checklist |
| security-checklist.md | Security hardening checklist |
| testing-patterns.md | Common testing patterns and strategies |

## Overlap Mapping

These skills coexist with existing project skills. The addyosmani skills provide general SWE methodology; project skills provide tool-integrated, project-specific implementations.

| addyosmani Skill | Existing Project Skill(s) | Relationship |
|---|---|---|
| code-review-and-quality | `deep-review`, `simplify`, `code-review-all` | Complementary: process vs tool-integrated |
| test-driven-development | `sp-tdd`, `qa-test-expert`, `test-suite` | Complementary: philosophy vs test framework |
| security-and-hardening | `security-expert`, `compliance-gate` | Complementary: checklist vs scanner |
| performance-optimization | `performance-profiler` | Complementary: methodology vs profiling |
| debugging-and-error-recovery | `diagnose`, `sp-debugging` | Complementary: framework vs 3-agent system |
| git-workflow-and-versioning | `domain-commit`, `ship`, `release-ship` | Complementary: workflow vs automation |
| ci-cd-and-automation | `ci-quality-gate`, `sre-devops-expert` | Complementary: practices vs pipeline |
| code-simplification | `simplify`, `omc-ai-slop-cleaner` | Complementary: principles vs automated fix |
| frontend-ui-engineering | `frontend-expert`, `design-architect` | Complementary: patterns vs FSD/TDS specific |
| api-and-interface-design | `backend-expert` | Complementary: design principles vs FastAPI/Go |
| documentation-and-adrs | `technical-writer` | Complementary: patterns vs project-specific |
| shipping-and-launch | `release-commander`, `ship` | Complementary: philosophy vs pipeline |
| context-engineering | `ce-*` skills (13 skills) | Complementary: overview vs deep specialization |
| spec-driven-development | `pm-execution`, `prd-research-factory` | Complementary: methodology vs PM tools |
| planning-and-task-breakdown | `sp-writing-plans`, `full-stack-planner` | Complementary: framework vs skill-aware |
| idea-refine | `sp-brainstorming` | Complementary: structured phases vs YC framework |
| browser-testing-with-devtools | `agent-browser`, `playwright-runner` | Complementary: methodology vs CLI tools |
| deprecation-and-migration | *(no direct equivalent)* | **Unique addition** |
| incremental-implementation | `sp-executing-plans` | Complementary: slicing strategy vs plan runner |
| using-agent-skills | `skill-guide` | Complementary: general meta-skill vs project-specific |

## Usage Guidance

**When to prefer addyosmani skills:**
- General SWE methodology questions (e.g., "how should I approach TDD?")
- Process-oriented guidance without project-specific tool integration
- Teaching or onboarding on software engineering practices
- When existing project skills are too opinionated for the task

**When to prefer existing project skills:**
- Tasks requiring integration with project tools (Playwright, FastAPI, TDS, SEFO)
- Project-specific workflows (FSD architecture, domain-commit, today pipeline)
- Automated fix-and-commit workflows
- Tasks scoped to this codebase's conventions

Each addyosmani SKILL.md includes `Do NOT use` clauses directing to the appropriate project skill when overlap exists.
