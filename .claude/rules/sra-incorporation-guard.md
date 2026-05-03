# SRA Skill-First Protocol

Every user request triggers a skill scan BEFORE any action.
Based on: Skill Retrieval Augmentation (arXiv:2604.24594).

## Mandatory Flow (every turn)

```
User request arrives
    |
    v
[1. Retrieval] Scan skill list for candidates (mental, no tool call)
    |
    v
[2. Triage] Native task? or Skill-worthy task?
    |           |
    v           v
  Native     [3. Incorporation] Pick best skill, state reason
    |           |
    v           v
  Execute    Load via Skill tool -> Follow skill instructions
```

## Stage 1: Retrieval (always run, zero cost)

Mentally scan the available skills list for the user's task.
Look for: exact trigger phrases, domain keywords, workflow type.
Identify 0-3 candidate skills. This is a thought process, not a tool call.

## Stage 2: Triage (need-awareness check)

Classify the task:

| Type | Examples | Action |
|------|----------|--------|
| **Native** | file edit, git command, simple Q&A, code fix, grep | Skip skills. Execute directly. |
| **Skill-worthy** | structured writing, multi-step review, pipeline orchestration, domain-specific analysis, harness workflow, document generation | Proceed to Stage 3. |

Decision heuristic:
- Task requires ONLY built-in tools (Read, Edit, Bash, Grep, Agent)? -> Native
- Task benefits from a specific workflow, checklist, rubric, or orchestration pattern? -> Skill-worthy
- Unsure? Default to native. Skills are for structured workflows, not general knowledge.

## Stage 3: Incorporation (skill selection)

When a skill IS needed:
1. State: "Using [skill-name] for [one-line reason]."
2. Invoke via Skill tool
3. Follow the loaded skill's instructions

## Anti-Hallucination Rules

- Never load a skill just because its name partially matches user keywords
- If 2+ candidates are equally relevant, state candidates and ask user
- If no good match exists, say so -- don't substitute a vaguely related skill
- One skill per task unless workflow explicitly chains them (harness pattern)
- Can't articulate what the skill provides that you lack? Don't load it.

## Noise Resistance

With 1000+ skills in corpus, distractor noise is the primary accuracy risk.
- Filter by exact trigger phrase match first
- Then by description keyword overlap
- Ignore skills whose Do-NOT-use clauses match the current task
- When in doubt, fewer skills loaded = better accuracy (SRA Noise Problem)

## Examples

**User: "이 함수의 버그를 고쳐줘"**
Retrieval: `4phase-debugging`, `fix-implementer` detected.
Triage: Simple code fix -> Native. Execute directly.

**User: "이 PR을 전체 코드 리뷰해줘"**
Retrieval: `review`, `code-reviewer-expert`, `engineering-harness` detected.
Triage: Multi-domain structured review -> Skill-worthy.
Incorporation: Using `review` for single PR review workflow.

**User: "분기 재무 보고서 초안을 작성해줘"**
Retrieval: `financial-report-analyzer`, `draft-writer`, `executive-briefing` detected.
Triage: Structured document generation with domain rubric -> Skill-worthy.
Incorporation: Using `financial-report-analyzer` for finance domain template.

**User: "README.md에 설치 방법 추가해줘"**
Retrieval: `documentation-and-adrs`, `docs-tutor` detected.
Triage: Simple file edit -> Native. Execute directly.
