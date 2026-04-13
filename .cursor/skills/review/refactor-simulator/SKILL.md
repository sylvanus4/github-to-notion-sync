---
name: refactor-simulator
description: >-
  Before making any code change, simulate the blast radius by analyzing all
  call sites, import chains, type dependencies, and test coverage for the
  affected area. Uses code-review-graph AST-based MCP tools when available for
  precise structural analysis (100% recall), with rg pattern fallback.
  Produces a "what-if" impact report with risk scores — without
  touching any code. Use when the user asks about "blast radius", "impact
  analysis", "refactor simulator", "what if I change", "what if I rename", "what
  if I move", "리팩토링 시뮬레이션", "영향 분석", "before refactoring", or wants to
  understand the consequences of a proposed change before executing it. Do NOT
  use for executing refactors (use simplify or generalPurpose), code review of
  existing code (use deep-review), or debugging (use diagnose).
metadata:
  author: "thaki"
  version: "2.0.0"
  category: "execution"
---
# Refactor Simulator — Pre-Change Blast Radius Analysis

Predict the impact of a code change before you make it. Uses AST-based code-review-graph for precise structural analysis when available, with ripgrep fallback. Maps dependencies, counts call sites, checks test coverage, and produces a risk-scored impact report — all without modifying a single file.

## Usage

```
/refactor-simulator "rename getUserById to findUserById"
/refactor-simulator "move src/utils/auth.ts to src/lib/auth/"
/refactor-simulator "delete UserProfile component"
/refactor-simulator "extract validateInput into a shared module"
/refactor-simulator --symbol "useAuth" --action rename
/refactor-simulator --file src/api/handler.ts --action split
```

## Workflow

### Step 1: Parse the Proposed Change

Extract from user input:
- **Target symbol**: function, class, component, type, or file being changed
- **Action type**: `rename | move | delete | extract | split | modify-signature`
- **Source location**: current file/module path
- **Destination**: new name, path, or signature (if applicable)

If ambiguous, ask the user to clarify the exact change.

### Step 2: Build Dependency Graph (Graph-First, rg Fallback)

#### 2-PRIMARY: AST-Based Analysis via code-review-graph MCP

When the `code-review-graph` MCP server is available, use these tools for precise structural analysis:

1. **Query the target node**:
   - `query_graph_tool` with `node_name: "{target}"`, `query_type: "callers"` → all direct callers
   - `query_graph_tool` with `node_name: "{target}"`, `query_type: "callees"` → all callees (upstream deps)
   - `query_graph_tool` with `node_name: "{target}"`, `query_type: "imports"` → import chain

2. **Compute blast radius**:
   - `get_impact_radius_tool` with `changed_files: ["{target_file}"]` → full transitive blast radius with test gap analysis

3. **Check affected execution flows**:
   - `get_affected_flows_tool` with `changed_files: ["{target_file}"]` → critical flows impacted

4. **Preview rename (for rename actions)**:
   - `refactor_tool` with `action: "rename"`, `target: "{symbol}"` → dry-run rename preview showing all locations that would change

5. **Detect dead code (for delete actions)**:
   - `refactor_tool` with `action: "dead_code"`, `target: "{symbol}"` → verify no live references remain

6. **Get structural context**:
   - `get_review_context_tool` with `changed_files: ["{target_file}"]` → token-optimized summary for report context

**Advantages over rg**: AST-based analysis catches indirect callers through interfaces, type inheritance, and re-export chains without regex false positives. Reports 100% recall on structural dependencies.

#### 2-FALLBACK: rg Pattern Analysis

When the MCP server is unavailable, fall back to ripgrep-based analysis:

**2a. Downstream Dependencies (what uses this?)**

Use `rg -F` (fixed-string / literal) for the initial scan to avoid regex escaping issues, then refine with context:

```bash
rg -F "{target}" --type ts --type py --type go -l
rg "{target}\s*\(" --type ts --type py --type go -l
rg "<{target}[\s/>]" --glob "*.tsx" -l
rg -F "{target}" --glob "**/index.ts" --glob "**/index.tsx" -l
```

Replace `{target}` with the actual symbol name. If the symbol contains regex special characters (e.g., `$`, `.`), always use `rg -F`.

**2b. Upstream Dependencies (what does this use?)**

Read the target file and extract all its imports, inherited types, and called functions.

**2c. Re-export Chains**

Check if the symbol is re-exported through barrel files (`index.ts`, `__init__.py`):

```bash
rg "export.*{target}" --type ts -l
rg "from.*{module}.*import.*{target}" --type py -l
```

### Step 3: Enumerate Call Sites

**Graph mode**: The `query_graph_tool` callers result already provides structured call-site data with file paths, node types, and relationship types. Classify each as production/test based on file path patterns.

**Fallback mode**: For each file that references the target, collect:
- File path and line numbers
- Usage type: `import | call | type-reference | jsx | inheritance | re-export`
- Whether the usage is in production code, test code, or configuration

```
Call Sites for getUserById:
  File                            | Line | Usage Type     | Context
  --------------------------------|------|----------------|----------
  src/api/users/handler.ts        | 23   | call           | production
  src/api/users/handler.ts        | 45   | call           | production
  src/components/UserProfile.tsx  | 12   | import + call  | production
  tests/api/users.test.ts         | 8    | import + call  | test
  src/lib/index.ts                | 5    | re-export      | barrel
```

### Step 4: Assess Test Coverage

**Graph mode**: `get_impact_radius_tool` already includes test gap analysis in its output. Extract `untested_paths` directly.

**Fallback mode**:
1. Find test files that import or test the target:
   ```bash
   rg -F "{target}" --glob "**/*test*" --glob "**/*spec*" --glob "**/__tests__/**" -l
   ```
2. Check if affected call sites have corresponding tests
3. Calculate coverage ratio: `tested_call_sites / total_call_sites`

### Step 5: Assess Flow Impact (Graph Mode Only)

When graph is available, add flow-level analysis:
- `get_affected_flows_tool` shows which high-criticality execution flows pass through the changed symbol
- Flows with criticality > 0.7 increase risk score by 10 per flow
- Report affected flows in the impact report under a dedicated section

### Step 6: Calculate Risk Score

```
risk_score = (call_site_count * call_site_weight)
           + (untested_sites * untested_weight)
           + (type_chain_depth * type_weight)
           + (re_export_count * re_export_weight)
           + (critical_flows * flow_weight)        # graph mode only

Where:
  call_site_weight  = 1.0
  untested_weight   = 3.0  (untested sites are 3x riskier)
  type_weight       = 2.0  (type changes cascade)
  re_export_weight  = 2.0  (re-exports multiply blast radius)
  flow_weight       = 10.0 (each critical flow affected)
```

Risk levels:
- **LOW** (score < 10): Few call sites, good test coverage
- **MEDIUM** (score 10-30): Moderate impact, some untested paths
- **HIGH** (score 30-60): Many call sites or significant untested code
- **CRITICAL** (score > 60): Widespread impact with poor test coverage

### Step 7: Generate Impact Report

```
Refactor Simulation Report
===========================
Proposed Change: [description]
Target: [symbol] in [file]
Action: [rename|move|delete|extract|split|modify-signature]
Analysis Method: [AST graph (code-review-graph) | rg pattern fallback]

Blast Radius:
  Files affected:     [N] production + [N] test
  Call sites:         [N] total ([N] tested, [N] untested)
  Type references:    [N]
  Re-export chains:   [N]
  Execution flows:    [N] affected ([N] critical)     # graph mode

Risk Score: [score] ([LOW|MEDIUM|HIGH|CRITICAL])

Files That Would Change:
  1. [file] — [reason: update import path / rename reference / remove usage]
  2. [file] — [reason]
  ...

Affected Flows (graph mode):                           # graph mode
  1. [flow_name] (criticality: 0.9) — [description]
  2. [flow_name] (criticality: 0.7) — [description]

Rename Preview (graph mode, rename action):            # graph mode
  [refactor_tool dry-run output]

Tests That May Break:
  1. [test file] — [which test and why]
  2. [test file] — [which test and why]

Untested Paths (highest risk):
  1. [file:line] — [no test covers this call site]
  2. [file:line] — [no test covers this call site]

Estimated Effort:
  Mechanical changes:    [N files, ~X minutes]
  Logic changes needed:  [N files, ~X minutes]
  New tests needed:      [N tests]

Recommendations:
  1. [write tests for untested paths before refactoring]
  2. [update barrel exports in src/lib/index.ts]
  3. [coordinate with team — bus factor 1 on this module]
```

### Step 8: Simulation Variants

If the user asks "what if" follow-ups, re-run the analysis with modified parameters:
- "What if I move it instead of renaming?" → re-run with `action: move`
- "What if I also rename the type?" → add the type to the target set and re-run
- "What's the blast radius if I do it in two stages?" → split analysis

## Examples

### Example 1: Rename a function

User: `/refactor-simulator "rename getUserById to findUserById in src/api/users/service.ts"`

Output: 12 call sites across 6 files, 3 untested, risk score 24 (MEDIUM). Recommends writing tests for the 3 untested call sites before renaming.

### Example 2: Delete a component

User: "What happens if I delete the LegacyModal component?"

Output: 4 files still import LegacyModal, 2 are in active routes. Risk score 18 (MEDIUM). Recommends migrating to NewModal first, provides the import locations.

### Example 3: Move a module

User: "What if I move src/utils/auth.ts to src/lib/auth/index.ts?"

Output: 23 files import from the old path, 5 barrel re-exports. Risk score 52 (HIGH). Recommends using a re-export shim at the old path temporarily.

## Error Handling

| Scenario | Action |
|----------|--------|
| MCP server unavailable | Fall back to rg-based analysis; note in report |
| Symbol not found in graph | Try `semantic_search_nodes_tool`, then fall back to rg |
| Symbol not found in codebase | Report with suggestions for similar names |
| Ambiguous symbol (multiple definitions) | List all definitions, ask user to choose |
| Dynamic imports or string references | Flag as "potentially affected, verify manually" |
| Circular dependencies detected | Report the cycle and warn about cascade risk |
| Very large blast radius (100+ files) | Use `list_communities_tool` to group by community |

## Troubleshooting

- **MCP server not responding**: Run `code-review-graph status` to check. Rebuild with `code-review-graph build` if needed. Analysis will use rg fallback automatically.
- **Stale graph results**: Run `code-review-graph update` to sync the graph with recent file changes.
- **Symbol not found**: Ensure the exact casing matches. Try `rg -Fi "{target}"` for case-insensitive search.
- **False positives in rg search**: `rg -F` matches substrings. For `get`, it matches `getUser`, `forget`. Use `rg -Fw "{target}"` for whole-word matching.
- **Dynamic imports missed**: `import()` expressions and `require()` calls won't match standard import patterns. Check for `rg "require.*{target}"` separately.
- **Monorepo scope**: If the project spans multiple packages, scope the search with `--glob "packages/my-app/**"` to avoid cross-package noise.
