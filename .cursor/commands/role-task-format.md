---
description: "Define a precise role, task, and output format for structured generation (Role:Task:Format pattern)"
argument-hint: "role:<role> task:<task description> format:<output format>"
---

# Structured Prompt Template (Role:Task:Format)

Explicit three-field prompt: who you are, what to do, and how to format the output. Removes all ambiguity.

## Usage

```
/role-task-format role:Senior SRE task:Design an incident response runbook for database failover format:numbered checklist with severity tags
/role-task-format role:Financial Analyst task:Evaluate the ROI of migrating to Kubernetes format:executive memo with tables
/role-task-format role:UX Researcher task:Create interview questions for onboarding flow usability format:grouped by theme with follow-up probes
/role-task-format role:시니어 PM task:Q4 로드맵 우선순위 정리 format:RICE 점수 테이블
```

## Your Task

User input: $ARGUMENTS

### Workflow

1. **Parse three fields:**
   - `role:` → The persona to adopt (expertise, vocabulary, priorities)
   - `task:` → The specific work to produce
   - `format:` → The output structure and style
2. **Activate role** — Set expertise domain, communication style, and decision framework
3. **Execute task** — Produce the deliverable under the persona's lens
4. **Apply format** — Structure the output exactly as specified
5. **Validate** — Confirm all three fields are satisfied:
   - ✅ Role: Does this sound like a [role] wrote it?
   - ✅ Task: Is the [task] fully completed?
   - ✅ Format: Does the output match [format]?

### Output Format

```
## [Task Title]
> Role: [Role] | Format: [Format]

[Structured output matching the specified format]
```

### Constraints

- All three fields (`role:`, `task:`, `format:`) are required — prompt for missing fields
- The role must genuinely influence the content, not just the introduction
- The format must be followed precisely — "table" means a table, "checklist" means checkboxes
- If the role and task conflict (e.g., "role:intern task:design system architecture"), note the tension but proceed

### Execution

Reference `prompt-architect` (`.cursor/skills/standalone/prompt-architect/SKILL.md`) for the RTF (Role-Task-Format) framework methodology.
