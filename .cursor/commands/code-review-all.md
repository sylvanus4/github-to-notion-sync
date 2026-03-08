## Code Review All

Run a full-project adversarial code review: 7-item crash/bug checklist, 30 abnormal behavior scenarios, and hacker-perspective security review with stack-aware conditional checks and 10-point scoring. All output in Korean.

### Usage

```
/code-review-all                     # full project review
```

### Workflow

1. **Stack detection** — Detect Rust/Tauri/Node/Frontend/Python/Go flags
2. **Code collection** — Gather source files based on detected stack
3. **3 parallel agents** — Checklist Agent, Scenario Agent, Security Agent
4. **Aggregate** — Merge, deduplicate, calculate 10-point score
5. **Report** — Korean report with checklist table, scenario table, security findings, score, verdict

### Execution

Read and follow the `code-review-all` skill (`.cursor/skills/code-review-all/SKILL.md`) for agent prompts, reference files, output format, and error handling.

### Examples

Full adversarial review of the project:
```
/code-review-all
```
