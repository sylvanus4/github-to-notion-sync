---
name: omc-talent-market
description: >-
  Dynamic Talent Market for the OneManCompany framework. Matches tasks to
  optimal agent configurations by scanning available skills, selecting model
  tiers, and composing heterogeneous agent teams. Implements on-demand hiring
  from the skill corpus. Triggers: "인재 매칭", "에이전트 매칭", "talent market",
  "팀 구성", "최적 에이전트 찾기", "스킬 매칭".
  Do NOT use for single-agent tasks (dispatch directly).
  Do NOT use for skill creation (use write-a-skill or omc-learner).
arguments: [task_description]
disable-model-invocation: true
---

# Talent Market: Dynamic Agent Composition

Implements the Talent Market concept from the OMC framework.
Core idea: agents are not permanently assigned. They are hired on-demand
from a pool of available capabilities, matched to task requirements.

## Talent = Identity + Capability

A Talent in Claude Code is composed of:

| Component | Claude Code Mapping |
|-----------|-------------------|
| Persona | Agent tool `subagent_type` + custom prompt preamble |
| Skills | Skill files loaded via Skill tool |
| Tools | MCP servers + built-in tools available to the agent |
| Scripts | Bash commands the agent can execute |
| Working Principles | Rules from `.claude/rules/` + memory feedback |

## Hiring Protocol

### Step 1: Task Analysis

Parse the task and extract:
- **Domain**: engineering / design / research / ops / writing / analysis
- **Actions**: read / write / create / review / test / deploy
- **Complexity**: S (single file) / M (multi-file) / L (cross-system)
- **Risk**: low (reversible) / medium (shared state) / high (production)

### Step 2: Candidate Retrieval

Scan the skill corpus for matches. Use this priority:

1. **Exact trigger match**: Skill description contains the task's domain keyword
2. **Capability overlap**: Skill's tools/actions match task requirements
3. **Agent type match**: Built-in subagent_types that fit the domain

**Built-in Agent Types (from Agent tool):**

| Domain | subagent_type | Best for |
|--------|--------------|----------|
| Architecture | backend-architect, Plan | System design, API design |
| Frontend | frontend-specialist, react-pro, nextjs-pro | UI implementation |
| Backend | golang-pro, python-pro, java-enterprise | Server implementation |
| DevOps | devops-engineer, kubernetes-expert, cloud-architect | Infrastructure |
| Testing | test-engineer, e2e-test-specialist, performance-tester | Quality assurance |
| Security | security-auditor | Vulnerability assessment |
| Documentation | documentation-writer, technical-writer | Writing |
| Review | code-reviewer | Code quality |
| Research | Explore | Codebase exploration |
| General | general-purpose | Multi-domain tasks |
| Orchestration | orchestrator | Sub-task coordination |

### Step 3: Model Tier Selection

| Task Characteristic | Model | Rationale |
|---|---|---|
| File reading, grep, simple lookup | haiku | 10x cheaper, sufficient |
| Standard implementation, writing | sonnet | Good balance |
| Multi-step reasoning, architecture | opus | Worth the cost for quality |
| Security-critical review | opus | Can't afford to miss issues |

### Step 4: Container Configuration

| Need | Container Config |
|------|-----------------|
| Code changes | `isolation: "worktree"` |
| Read-only research | No isolation |
| Parallel code changes | Separate worktrees per agent |
| Shared state needed | Sequential execution, same worktree |

### Step 5: Team Composition

Output the hiring plan:

```
## Talent Team for: [task]

### Role 1: [Name]
- Type: [subagent_type]
- Model: [haiku|sonnet|opus]
- Skills: [skill names to load]
- Isolation: [worktree|none]
- Deliverable: [expected output]

### Role 2: [Name]
...

### Execution Order
[DAG description: which roles run in parallel, which are sequential]

### Estimated Cost
[Agent count x model tier estimate]
```

## Heterogeneous Composition Rules

The power of OMC is mixing different agent types optimally:

1. **Don't use one model for everything.** A research phase in haiku + implementation in sonnet + review in opus is cheaper and better than all-opus.

2. **Match agent type to deliverable, not to topic.** A "frontend bug" doesn't need a frontend-specialist if the fix is in a config file -- use general-purpose.

3. **Prefer specialists over generalists** when the task is deep in one domain. A golang-pro will write better Go than a fullstack-engineer.

4. **Use orchestrator type sparingly.** Only when coordinating 3+ sub-agents. For 1-2 agents, the main session can coordinate directly.

5. **Load skills into agents** when the skill provides a structured workflow the agent should follow. Don't load skills just for domain knowledge -- the agent has that natively.

## Anti-Patterns

- Hiring 5 agents for a 10-line change
- Using opus for file exploration
- Loading 3+ skills into one agent (context pollution)
- Creating a "manager" agent that just relays messages
- Assigning overlapping tasks to multiple agents without clear ownership
