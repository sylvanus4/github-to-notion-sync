# Templates Reference — Docs Tutor Setup

## Vault Folder Structure

```
StudyVault/
  00-Dashboard/          # MOC + Quick Reference
  01-<Section1>/         # Concept notes per domain
  02-<Section2>/
  ...
  NN-<SectionN>/
```

---

## Dashboard MOC Template

```markdown
---
source_docs: [all sections]
section: dashboard
keywords: MOC, study map, ai-platform, onboarding
---

# AI Platform Study Map

#dashboard #ai-platform

## Overview

- Platform: AI Platform WebUI — multi-tenant AI inference & orchestration platform
- Docs source: `docs/` directory
- Generated: <date>

## Section Map

| # | Section | Topics | Notes | Status |
|---|---------|--------|-------|--------|
| 01 | Platform Architecture | system design, components | [[01-Platform-Architecture/개요]] | [ ] |
| 02 | Infrastructure | K8s, deployment, CI/CD | [[02-Infrastructure/개요]] | [ ] |
| ... | ... | ... | ... | ... |

## Practice Notes

| Section | Questions | Link |
|---------|-----------|------|
| Platform Architecture | N questions | [[01-Platform-Architecture/연습문제]] |
| Infrastructure | N questions | [[02-Infrastructure/연습문제]] |

## Study Tools

| Tool | Description | Link |
|------|-------------|------|
| Quick Reference | Key concepts cheat sheet | [[00-Dashboard/빠른-참조]] |

## Tag Index

| Tag | Description | Rule |
|-----|-------------|------|
| `#arch-*` | Architecture concepts | System design patterns |
| `#infra-*` | Infrastructure & deployment | K8s, Docker, CI/CD |
| `#api-*` | API endpoints & contracts | REST, gRPC, WebSocket |
| `#ops-*` | Operational procedures | Runbooks, incident response |
| `#security-*` | Security & compliance | RBAC, auth, secrets |
| `#feature-*` | Feature specifications | PRDs, planned features |
| `#test-*` | Testing strategies | E2E, unit, integration |
| `#admin-*` | Admin portal | User/resource management |

> **Tag rule**: English kebab-case only. Detail tags co-attach parent category tag.

## Weak Areas

- [ ] <area> → [[Relevant Note]]

> Updated automatically by the docs-tutor skill after quiz sessions.

## Learning Path

> Recommended reading order for platform newcomers:

1. [[Platform Architecture 개요]] — big picture
2. [[Infrastructure 개요]] — how the platform is deployed
3. [[Security & Auth]] — authentication and authorization
4. [[Admin Portal]] — management interface
5. [[Operational Runbooks]] — day-to-day operations
6. [[Practice Questions]] — test your understanding
```

---

## Quick Reference Template

```markdown
---
source_docs: [all sections]
section: dashboard
keywords: quick-reference, cheat-sheet, key-concepts
---

# Quick Reference

#dashboard #quick-reference

## Platform Architecture → [[01-Platform-Architecture/개요]]

| Concept | Summary |
|---------|---------|
| <concept> | <one-line description> |

## Infrastructure → [[02-Infrastructure/개요]]

| Concept | Summary |
|---------|---------|
| <concept> | <one-line description> |

## Key Commands

| Action | Command |
|--------|---------|
| Start dev stack | `<command>` |
| Run tests | `<command>` |
| Deploy | `<command>` |

## Architecture Patterns

| Pattern | Where Used | Notes |
|---------|-----------|-------|
| <pattern> | <component> | → [[Note]] |

## Must-Know Concepts

| # | Concept | Why It Matters | → Note |
|---|---------|----------------|--------|
| 1 | <concept> | <reason> | [[Note]] |
```

---

## Concept Note Template

```markdown
---
source_docs:
  - docs/<section>/<file1>.md
  - docs/<section>/<file2>.md
section: <section-name>
keywords: <3-5 English keywords>
---

# <Title> (<Importance: ★~★★★>)

#<tag-from-registry> #<tag-from-registry>

## Overview Table

| Item | Key Point |
|------|-----------|
| Purpose | <what this is about> |
| Scope | <what it covers> |
| Dependencies | <what it depends on> |

## <Concept 1>

Concise explanation (3-5 lines max).
- Bullet points for key facts
- Use **bold** for critical terms

## <Concept 2>

...

---

## Architecture / Flow

```text
<ASCII diagram showing relevant architecture, data flow, or process>
```

## Key Decisions & Trade-offs

| Decision | Rationale | Alternative Considered |
|----------|-----------|----------------------|
| <decision> | <why> | <what else was considered> |

## Configuration

| Config Key / Env Var | Purpose | Default |
|---------------------|---------|---------|
| `<var>` | <what it controls> | <default value> |

## Related Notes

- [[Other Note 1]]
- [[Other Note 2]]
```

### Formatting Rules

- `[[wiki-links]]` for cross-references
- `> [!tip]`, `> [!important]`, `> [!warning]` callouts
- Comparison tables over prose; bold for key vocabulary
- Content language matches source material

### Visualization Rule

Include ASCII diagrams when applicable:
- Architecture components → block diagram
- Request/data flow → flow DAG
- Decision processes → decision tree
- State-based behavior → state transition diagram
- Deployment topology → infrastructure diagram

### Simplification-with-Exceptions Rule

General statements must check for edge cases — add `> [!warning]` or link to exception details.

---

## Practice Question Template

```markdown
---
source_docs:
  - docs/<section>/<file1>.md
section: <section-name>
keywords: practice, <topic keywords>
---

# <Section> 연습문제 (N questions)

#practice #<section-tag>

## Related Concepts

- [[Concept Note 1]]
- [[Concept Note 2]]

> [!hint]- 핵심 패턴 (클릭하여 보기)
> | Keyword | Answer |
> |---------|--------|
> | pattern 1 | **Solution** |

---

## Question 1 — <Short Label> [recall]

> <Scenario summary in one line>

> [!answer]- 정답 보기
> Answer text here with explanation.

---

## Question 2 — <Short Label> [application]

> <Given this scenario, what would you do?>

> [!answer]- 정답 보기
> Answer with applied reasoning.

---

## Question 3 — <Short Label> [analysis]

> <Compare X and Y in this context. Which is better and why?>

> [!answer]- 정답 보기
> Comparative analysis answer.

---

## Question 4 — <Short Label> [troubleshooting]

> <Given symptom X in the logs, what is the most likely root cause?>

> [!answer]- 정답 보기
> Troubleshooting steps and root cause explanation.

---

> [!summary]- 패턴 요약 (클릭하여 보기)
> | Keyword | Answer |
> |---------|--------|
> | ... | ... |
```

### Practice Question Rules

- Every section folder MUST have a practice file (8+ questions)
- **Answer hiding**: ALL answers use `> [!answer]- 정답 보기` fold callout
- **Patterns**: `> [!hint]-` / `> [!summary]-` fold callouts (MANDATORY)
- **Question type diversity**: tag `[recall]`, `[application]`, `[analysis]`, `[troubleshooting]` in heading
  - ≥40% recall, ≥20% application, ≥2 analysis, ≥2 troubleshooting per file
- Scenario in one `>` blockquote line; answer 1-3 lines in fold
- `## Related Concepts` with `[[wiki-links]]` (MANDATORY)

### Platform-Specific Question Patterns

| Type | Example Pattern |
|------|----------------|
| Architecture | "Why does the platform use X pattern instead of Y?" |
| Operational | "What is the incident response procedure when X occurs?" |
| Configuration | "How would you set up X for a production deployment?" |
| Troubleshooting | "A user reports X error. What is the most likely cause?" |
| API | "What HTTP status code is returned when X happens?" |
| Security | "What RBAC role is required to perform X?" |
