---
description: Pre-mortem risk analysis on PRD, launch plan, or feature
argument-hint: "<PRD, launch plan, or feature description>"
---

# PM Pre-Mortem

Run a pre-mortem risk analysis on a PRD, launch plan, or feature. Assume the initiative has failed — what went wrong? Classify risks (Tigers, Paper Tigers, Elephants) and produce a Go/No-Go checklist. Uses pm-execution skill, pre-mortem sub-skill.

## Usage
```
/pm-pre-mortem Analyze risks for this PRD before we start
/pm-pre-mortem 이 PRD에 대한 사전 사망 분석 해줘
/pm-pre-mortem Launch plan for Q2 feature X
/pm-pre-mortem 출시 전 리스크 분석
```

## Workflow

### Step 1: Ingest Artifact
- Accept PRD, launch plan, feature brief, or narrative description
- Extract: goals, scope, stakeholders, timeline, dependencies, success criteria

### Step 2: Assume Failure
- Set scenario: "It's 6 months later. This initiative has failed. Why?"
- Brainstorm 10–20 potential failure causes without filtering
- Encourage specific, concrete causes (not generic "poor execution")

### Step 3: Classify Risks
- **Tigers**: Real threats — high likelihood, high impact. Need mitigation plans
- **Paper Tigers**: Overblown concerns — low likelihood or impact. Document and deprioritize
- **Elephants**: Unspoken risks — politically or socially sensitive, often undiscussed. Surface for honest conversation

### Step 4: Go/No-Go Checklist
- List must-resolve items before launch
- Each item: criterion, owner, status (Go / No-Go / Conditional)
- Highlight blockers that would warrant delay

## Notes
- Pre-mortems work best when the team participates; consider running as a workshop
- Elephants require psychological safety — frame as "what could we be blind to?"
- Revisit checklist at key milestones (design complete, dev complete, beta)
