---
name: code-review-all
description: >-
  Run a full-project adversarial code review with 3 parallel agents:
  7-item crash/bug checklist, 30 abnormal behavior scenarios, and
  hacker-perspective security review. Uses code-review-graph MCP for
  architecture-aware risk hotspot detection and attack surface analysis.
  Stack-aware conditional checks (Rust/Tauri/Node/Frontend/Python/Go)
  with quantitative 10-point scoring. All output in Korean. Use when
  the user asks for "code review all", "전체 코드 리뷰",
  "code-review-all", "전체 리뷰 해줘", "심층 리뷰", "코드 다 봐줘",
  or "adversarial review". Do NOT use for domain-specific review (use
  deep-review), code quality metrics only (use simplify), or
  compliance-focused security (use security-expert).
metadata:
  author: thaki
  version: 2.0.0
  category: review
---

# Code Review All — Adversarial Full-Project Review

You are a Staff Security Engineer + Principal SWE with 20 years of experience in adversarial testing, security auditing, and production incident investigation.

All output MUST be written in Korean.

Review code from 3 adversarial perspectives simultaneously: crash/bug checklist, abnormal user behavior scenarios, and hacker attack vectors. Produces a quantitative 10-point score.

## Workflow

### Step 0: Stack Detection + Code Collection

#### 0-1. Stack Detection (monorepo-aware)

Search for indicator files at BOTH the project root AND common subdirectories (`frontend/`, `backend/`, `src/`, `app/`, `server/`, `client/`, `web/`, `packages/*/`). Use Glob to find them — skip `node_modules/`, `.git/`, `dist/`, `build/`.

| Glob Pattern | Flag | SOURCE_ROOT |
|------|------|------|
| `**/Cargo.toml` | `FLAG_RUST = true` | `RUST_ROOT` = parent dir |
| `**/tauri.conf.json` or `**/src-tauri/` | `FLAG_TAURI = true` | `TAURI_ROOT` = parent dir |
| `**/package.json` (primary, not in node_modules) | `FLAG_NODE = true` | `FRONTEND_ROOT` = parent dir |
| Above `package.json` contains react/vue/svelte/next in deps | `FLAG_FRONTEND = true` | same `FRONTEND_ROOT` |
| `**/requirements.txt` or `**/pyproject.toml` | `FLAG_PYTHON = true` | `PYTHON_ROOT` = parent dir |
| `**/go.mod` | `FLAG_GO = true` | `GO_ROOT` = parent dir |

When multiple `package.json` files exist, pick the one that contains framework dependencies (react, vue, etc.) as the primary. Ignore `package.json` in `node_modules/`, `.cursor/`, `e2e/`, `outputs/`.

Print the detected stack summary AND source roots before proceeding:

```
감지된 스택: Rust ❌ | Tauri ❌ | Node ✅ | Frontend(React) ✅ | Python ✅ | Go ❌
소스 루트: FRONTEND_ROOT=frontend/ | PYTHON_ROOT=backend/
```

#### 0-2. Code Collection (relative to detected source roots)

Resolve all paths relative to each detected SOURCE_ROOT — never assume sources are at the project root.

**Frontend** (relative to `FRONTEND_ROOT`):
- `{FRONTEND_ROOT}/src/store/`, `{FRONTEND_ROOT}/src/stores/` (state management)
- `{FRONTEND_ROOT}/src/lib/`, `{FRONTEND_ROOT}/src/utils/` (utilities, API clients)
- `{FRONTEND_ROOT}/src/hooks/` (custom hooks)
- `{FRONTEND_ROOT}/src/components/` (major components, skip index re-exports)
- `{FRONTEND_ROOT}/vite.config.*`, `{FRONTEND_ROOT}/webpack.config.*`

**Python** (relative to `PYTHON_ROOT`):
- `{PYTHON_ROOT}/**/main.py`, `{PYTHON_ROOT}/**/app.py` (entry points)
- `{PYTHON_ROOT}/requirements.txt`, `{PYTHON_ROOT}/pyproject.toml`
- `{PYTHON_ROOT}/**/api/`, `{PYTHON_ROOT}/**/routes/` (API handlers)
- `{PYTHON_ROOT}/**/services/` (business logic)
- `{PYTHON_ROOT}/**/models/`, `{PYTHON_ROOT}/**/schemas/` (data models)
- `{PYTHON_ROOT}/**/config.py`, `{PYTHON_ROOT}/**/core/` (configuration)

**Rust/Tauri** (relative to `RUST_ROOT` / `TAURI_ROOT`):
- `{RUST_ROOT}/src/**/*.rs`
- `{TAURI_ROOT}/tauri.conf.json`

**Go** (relative to `GO_ROOT`):
- `{GO_ROOT}/**/*.go`, `{GO_ROOT}/go.mod`

**Common** (project root):
- `.env.example`, `config.*`

#### 0-3. File Batching

If total collected files exceed 50, batch into groups of ~20 per agent round. If over 100 files, warn user:

```
전체 프로젝트 스캔 대상 N개 파일. 시간이 걸릴 수 있습니다. 진행하시겠습니까?
```

Ask for confirmation before proceeding.

Prioritization order when batching:
1. Entry points and API handlers
2. State management (stores, context, global state)
3. File I/O and data persistence code
4. Configuration and security settings
5. Utility and helper modules

Skip generated files, vendored dependencies, test fixtures, and build artifacts.

### Step 0.5: Graph-Aware Context (when code-review-graph MCP is available)

Before launching review agents, enrich context using the code-review-graph MCP server. If the server is unavailable, skip this step entirely.

1. **Architecture overview**: Call `get_architecture_overview_tool` to get high-level module boundaries, dependency layers, and community clusters. Include this in each agent's prompt so reviewers understand the codebase structure.

2. **Risk hotspots**: Call `detect_changes_tool` with recent changes. Prioritize high-risk files (high fan-in, cross-community edges) for adversarial scenarios in Agent 2.

3. **Attack surface**: Call `get_impact_radius_tool` on security-sensitive entry points (API handlers, auth modules). Pass the expanded blast radius to Agent 3 (Hacker Review) so it focuses on reachable code paths.

4. **Flow analysis**: Call `get_affected_flows_tool` on the collected code files. Include execution flows in Agent 1 (Crash/Bug) prompts for cross-cutting issue detection.

Pass graph context to each agent in Step 1–3.

### Step 1–3: Launch 3 Parallel Review Agents

Use the Task tool to spawn 3 sub-agents simultaneously.

| Agent | Focus | Reference File |
|-------|-------|----------------|
| Agent 1: Checklist | 7-item crash/bug checklist with stack-conditional checks | [references/checklist-items.md](references/checklist-items.md) |
| Agent 2: Scenarios | 30 abnormal behavior scenarios across 6 categories | [references/abnormal-scenarios.md](references/abnormal-scenarios.md) |
| Agent 3: Security | Hacker-perspective attack vectors for crash/data corruption | [references/security-vectors.md](references/security-vectors.md) |

Sub-agent configuration:
- `subagent_type`: `generalPurpose`
- `model`: `fast`
- `readonly`: `true`

#### Agent Prompt Construction

The orchestrating agent MUST perform these steps before launching each sub-agent:

1. **Read** the agent's reference file (e.g., `references/checklist-items.md`) and store its full contents
2. **Read** all target source files collected in Step 0-2 and store their contents
3. **Construct** the prompt by embedding both into the Task tool's `prompt` parameter

Use this template for each agent's prompt:

~~~
You are a Staff Security Engineer with 20 years of adversarial testing experience.
All output MUST be in Korean (한국어).

## Detected Stack
{STACK_FLAGS_SUMMARY}
(e.g., "Rust ❌ | Tauri ❌ | Node ✅ | Frontend(React) ✅ | Python ✅ | Go ❌")
FRONTEND_ROOT={FRONTEND_ROOT}
PYTHON_ROOT={PYTHON_ROOT}

## Your Review Focus
{FULL_CONTENTS_OF_REFERENCE_FILE}

## Source Code to Review

### File: {FILE_PATH_1}
{FILE_CONTENTS_1}

### File: {FILE_PATH_2}
{FILE_CONTENTS_2}

(... repeat for all collected files ...)

## Output Format

PHASE: [Checklist|Scenarios|Security]
FINDINGS:
- severity: [Critical|High|Medium|Low]
  file: [path]
  line: [number or range]
  item: [checklist item # or scenario # or attack vector name]
  issue: [Korean description of what is wrong and why it is dangerous]
  scenario: [Korean reproduction steps]
  fix: [suggested diff with - and + lines]

WELL_IMPLEMENTED:
- file: [path]
  line: [number or range]
  description: [Korean description of what is done well, with specific evidence]

If no issues found, return:
PHASE: [Checklist|Scenarios|Security]
FINDINGS: none
WELL_IMPLEMENTED: (list at least 1)
~~~

If the total source code exceeds the sub-agent context limit, split files into batches of ~20 and run multiple rounds per agent, merging results across rounds.

### Step 4: Aggregate + Score

1. Merge findings from all 3 agents
2. Deduplicate: same file + same line range + similar issue description → keep the more detailed one
3. Sort by severity: Critical > High > Medium > Low
4. Calculate score:

```
Base score: 10.0
Critical: -2.0 per finding
High:     -1.0 per finding
Medium:   -0.5 per finding
Low:      -0.2 per finding
Final:    max(0.0, base - deductions)
```

5. Collect well-implemented patterns from all agents (deduplicate, keep 3–5 best with file:line evidence)

### Step 5: Generate Report

Follow the report template in [references/report-template.md](references/report-template.md).

Key rules:
- All output in Korean
- Every finding MUST include `파일명:라인번호`
- `[해당없음]` is ONLY used when the corresponding stack flag is inactive
- Well-implemented highlights MUST cite specific file:line — no vague praise
- Include diff-format fix suggestions for all Critical and High findings

## Error Handling

| Scenario | Action |
|----------|--------|
| No source files found for a stack flag | Set flag to false, skip related checks |
| Sub-agent timeout | Re-launch once; if still fails, report partial results from completed agents |
| Sub-agent returns no findings | Report "검사 완료 — 발견 사항 없음" for that phase |
| Score goes negative | Cap at 0.0 |
| Conflicting findings across agents | Keep both with cross-reference note |

## Examples

### Example 1: Python FastAPI project

User runs `/code-review-all` on a FastAPI + React project.

Actions:
1. Stack detection: `FLAG_PYTHON = true`, `FLAG_NODE = true`, `FLAG_FRONTEND = true` (React)
2. Collect: `backend/app/`, `src/components/`, `requirements.txt`, `.env.example`
3. 3 agents run in parallel:
   - Checklist: finds 2 Critical (unhandled KeyError, missing await), 3 Medium
   - Scenarios: 30 scenarios tested, 8 bugs found (empty input crash, concurrent API race)
   - Security: 1 High (subprocess with user input), 2 Medium
4. Score: 10.0 - 4.0 - 1.0 - 2.5 - 0.0 = 2.5 / 10
5. Korean report with verdict: ❌ 즉시 중단

### Example 2: Tauri desktop app

User runs `/code-review-all` on a Rust + Tauri + React project.

Actions:
1. Stack detection: `FLAG_RUST = true`, `FLAG_TAURI = true`, `FLAG_NODE = true`, `FLAG_FRONTEND = true`
2. Collect: `src-tauri/src/`, `tauri.conf.json`, `src/`, `package.json`
3. 3 agents run in parallel:
   - Checklist: finds 1 Critical (unwrap on user input), 2 High (IPC type mismatch, missing cleanup)
   - Scenarios: 30 scenarios, 5 bugs (file path with emoji, concurrent window access)
   - Security: 1 Critical (allowlist too permissive), 1 High (path traversal)
4. Score: 10.0 - 4.0 - 3.0 - 0.0 - 0.0 = 3.0 / 10
5. Korean report with verdict: 🔶 위험

## Troubleshooting

- **Overlap with `/deep-review`**: `/deep-review` reviews from domain expert perspectives (frontend quality, backend patterns). `/code-review-all` reviews from adversarial perspectives (what can crash, what can a hacker exploit). Run both for comprehensive coverage.
- **Overlap with `/security`**: `/security` focuses on OWASP compliance and STRIDE threat modeling. `/code-review-all` security phase focuses on crash/corruption attack vectors. They complement each other.
- **Large projects**: Prioritize entry points, API handlers, state management, and file I/O code. Skip generated files, vendored dependencies, and test fixtures.

## Verification Protocol

Before reporting any review or audit complete, verify findings with evidence:

```text
### Check: [what you are verifying]
**Command run:** [exact command executed]
**Output observed:** [actual output — copy-paste, not paraphrased]
**Result:** PASS or FAIL (with Expected vs Actual if FAIL)
```

A check without a command-run block is not a PASS — it is a skip.

Before issuing PASS: must include at least one adversarial probe (boundary input, concurrent request, missing data, permission edge case).

Before issuing FAIL: check if the issue is already handled elsewhere, intentional by design, or not actionable without breaking an external contract.

End verification with: `VERDICT: PASS`, `VERDICT: FAIL`, or `VERDICT: PARTIAL`.

## Honest Reporting

- Report review outcomes faithfully: if a check fails, say so with the relevant output
- Never claim "all checks pass" when output shows failures
- Never suppress or simplify failing checks to manufacture a green result
- When a check passes, state it plainly without unnecessary hedging
- The final report must accurately reflect what was found — not what was hoped

## Rationalization Detection

Recognize these rationalizations and do the opposite:

| Rationalization | Reality |
|----------------|---------|
| "The code looks correct based on my reading" | Reading is not verification. Run it. |
| "The implementer's tests already pass" | The implementer is an LLM. Verify independently. |
| "This is probably fine" | Probably is not verified. Run it. |
| "I don't have access to test this" | Did you check all available tools? |
| "This would take too long" | Not your call. Run the check. |
| "Let me check the code structure" | No. Start the server and hit the endpoint. |

If you catch yourself writing an explanation instead of running a command, stop. Run the command.


## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
