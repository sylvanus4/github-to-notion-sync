## Define Problem

Apply the 5D Problem Definition Framework (Describe, Decompose, Diagnose, Define, Document) to properly frame a problem before jumping to solutions. Produces a structured Problem Definition Document (PDD).

### Usage

```
# Scoping modes
/define-problem                                # deep mode (default) — full 5D analysis
/define-problem quick                          # single-pass problem statement
/define-problem team                           # collaborative workshop template
/define-problem deep                           # explicit deep mode

# With initial description
/define-problem "API latency exceeds SLO"      # deep mode with starting context
/define-problem quick "Login broken on mobile"  # quick mode with starting context

# Scoped to codebase area
/define-problem deep src/api/                  # deep mode focused on a directory
```

### Workflow

1. **Describe** — Gather raw symptoms via Socratic questioning
2. **Decompose** — Break into sub-elements; detect anti-patterns (symptom-as-problem, solution-as-problem, scope bundling)
3. **Diagnose** — 5 Whys, multi-perspective analysis (user, engineering, business), form testable hypotheses
4. **Define** — Synthesize a precise, measurable problem statement with scope and success criteria
5. **Document** — Produce the Problem Definition Document (PDD)

### Output

A structured PDD containing: observed symptoms, decomposition, root cause hypotheses with confidence levels, stakeholder perspectives, a testable problem statement, scope boundaries, and measurable success criteria.

### Execution

Read and follow the `problem-definition` skill (`.cursor/skills/problem-definition/SKILL.md`) for the full framework, output template, examples, and error handling.
