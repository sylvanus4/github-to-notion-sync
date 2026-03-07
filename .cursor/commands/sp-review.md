## Superpowers Code Review

Principled code review using Superpowers — either requesting a review (self-review before PR) or receiving review feedback (with technical rigor, not performative agreement).

### Usage

```
/sp-review [--request | --receive]
```

- `--request` (default): Self-review your own changes before creating a PR
- `--receive`: Process review feedback on an existing PR with technical rigor

### Mode 1: Requesting Review (`--request`)

Read and follow the Superpowers `requesting-code-review` skill.

**Step 1: Gather Changes**

```bash
git diff main..HEAD --stat
git log --oneline main..HEAD
```

**Step 2: Self-Review Checklist**

Before asking anyone else to review:
- Does every changed function have tests?
- Are error cases handled?
- Are there any TODOs or temporary code left?
- Does the code follow existing patterns in the codebase?
- Is the commit history clean and logical?

**Step 3: Domain-Specific Review**

Use Task subagents with project domain skills based on changed files:
- **backend-expert** (`.cursor/skills/backend-expert/SKILL.md`) for `services/**` changes
- **frontend-expert** (`.cursor/skills/frontend-expert/SKILL.md`) for `frontend/**` changes
- **db-expert** (`.cursor/skills/db-expert/SKILL.md`) for `db/**` or migration changes
- **security-expert** (`.cursor/skills/security-expert/SKILL.md`) for auth/PII/secret changes

**Step 4: Generate Review Summary**

Use **pr-review-captain** (`.cursor/skills/pr-review-captain/SKILL.md`) to produce:
- Change summary with risk assessment
- Review checklist
- Release notes draft

**Step 5: Commit Cleanup**

Use **domain-commit** (`.cursor/skills/domain-commit/SKILL.md`) to ensure commits are properly split by domain before the PR.

### Mode 2: Receiving Review (`--receive`)

Read and follow the Superpowers `receiving-code-review` skill.

**Principles:**
- Technical rigor, not performative agreement
- Don't blindly implement every suggestion — verify it's correct first
- If feedback seems wrong, investigate and respond with evidence
- If feedback is valid, fix it properly (not just "close enough")

**Process:**
1. Read each review comment carefully
2. For each suggestion:
   - Is it technically correct? (verify, don't assume)
   - Does it align with project patterns?
   - Would it introduce regressions? (run tests)
3. Implement valid suggestions following TDD
4. Respond to incorrect suggestions with evidence, not argument

### Difference from `/reviewer` and `/pr-review`

Existing commands focus on review output format and automation. This command adds Superpowers' principled approach: thorough self-review before requesting, and technical rigor (not blind agreement) when receiving.

### Output

**For `--request`:**
- Self-review findings and fixes applied
- Domain-specific review results
- PR-ready change summary with risk assessment
- Clean, domain-split commits

**For `--receive`:**
- Each comment addressed with evidence
- Valid suggestions implemented and tested
- Invalid suggestions responded to with reasoning
