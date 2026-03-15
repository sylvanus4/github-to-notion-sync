# Skill Composer — Composition Patterns Reference

## Supported Workflow Patterns

### 1. Sequential

Tasks execute in a predetermined order. Each step processes inputs and passes results to the next.

- **Use when:** Tasks have dependencies — step B needs step A's output.
- **Pattern reference:** `workflow-sequential`
- **Example:** Review → Commit → PR → Slack

### 2. Parallel

Independent tasks run simultaneously. Results are aggregated after all complete (fan-out/fan-in).

- **Use when:** Tasks are independent and benefit from concurrent execution.
- **Pattern reference:** `workflow-parallel`
- **Constraints:** Max 4 concurrent subagents per workflow-patterns rule.

### 3. Eval-Opt (Evaluator-Optimizer)

Two roles in a loop: one generates content, another evaluates it, and the generator refines based on feedback. Continues until quality threshold or max iterations.

- **Use when:** First-draft quality consistently falls short and measurable quality criteria exist.
- **Pattern reference:** `workflow-eval-opt`
- **Requirements:** Quality threshold, max iteration count, stopping criteria.

### 4. Conditional

Branches based on conditions (e.g., success/failure, input flags).

- **Use when:** Different paths based on runtime conditions.
- **Implementation:** Composed from `workflow-sequential` with conditional skip steps or explicit branches in the workflow definition.

---

## Trigger Condition Syntax

| Keyword | Meaning | Example |
|---------|---------|---------|
| `when` | On-demand or event-driven | "When user runs /ship" |
| `whenever` | Recurring or event-based | "Whenever I finish a code review" |
| `after` | Post-condition | "After tests pass" |
| `before` | Pre-condition | "Before pushing to main" |
| `on` | Event or action | "On PR merge" |

**Parsing rules:**
1. Extract the temporal/conditional phrase (when/whenever/after/before/on + clause).
2. Map to workflow invocation context (manual command vs. hook vs. scheduled).
3. Store as `trigger.condition` in the workflow definition.

---

## Skill Dependency Resolution Algorithm

1. **Extract action verbs** from the natural language description (e.g., "commit", "create PR", "post to Slack").
2. **Search** `.cursor/skills/` SKILL.md files for matching descriptions and triggers.
3. **Rank matches** by:
   - Exact trigger/keyword match
   - Semantic overlap with action verb
   - Category fit (e.g., domain-commit for "commit")
4. **Resolve dependencies**:
   - If skill A's output is needed by skill B, A must precede B.
   - If skills are independent, consider `workflow-parallel`.
5. **Validate** all selected skills exist and have non-empty SKILL.md.

---

## Input/Output Contract Definition Format

```yaml
workflow:
  name: post-review-ship
  trigger: whenever finish code review
  contracts:
    - from: deep-review
      to: domain-commit
      output: changed_files, lint_status
      input: files_to_commit
    - from: domain-commit
      to: release-ship
      output: commit_sha, branch
      input: branch, push_target
```

**Fields:**
- `from` / `to`: skill identifiers
- `output`: keys produced by `from` that `to` may consume
- `input`: keys that `to` expects (may come from `from` or user/env)

---

## Example Compositions

### Simple Chain (Sequential)

**User:** "Whenever I finish a code review, commit changes, create a PR, and post to Slack."

```
deep-review → domain-commit → release-ship → Slack MCP / kwp-slack
```

**Workflow definition:** `workflow-sequential` with steps: [deep-review, domain-commit, release-ship, slack-post].

### Parallel Fan-Out

**User:** "Run a full quality audit: security review, test coverage, lint, and dependency check in parallel."

```
[security-expert | test-suite | simplify | dependency-auditor] → aggregate → report
```

**Workflow definition:** `workflow-parallel` for the four tasks, then `workflow-sequential` for aggregation.

### Conditional Branching

**User:** "After tests pass, if there are changes, commit and push; otherwise just report status."

```
test-suite → (changed? → domain-commit → release-ship : report-status)
```

**Workflow definition:** `workflow-sequential` with a conditional step that checks `changed_files` and branches.
