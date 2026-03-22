---
description: "Generate a code draft and draft PR from a GitHub issue — codebase analysis, implementation, tests, and PR creation"
---

## Issue to Code

Turn a GitHub issue into a working code draft with tests and a draft PR.

### Usage

```
/issue-to-code #42                          # generate code from issue #42
/issue-to-code #42 --draft-only             # generate code but skip PR creation
/issue-to-code #42 --with-tests             # include test generation (default: yes)
/issue-to-code #42 --no-tests               # skip test generation
```

### Execution

Read and follow the skill at `.cursor/skills/issue-to-code/SKILL.md`.

User input: $ARGUMENTS

1. Parse the issue number from arguments
2. Fetch issue details via GitHub MCP
3. Analyze codebase for relevant files and patterns
4. Generate implementation code following project conventions
5. Create tests for the new code
6. Create a draft PR linking back to the issue
