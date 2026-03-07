---
name: refactor-simulator
description: >-
  Before making any code change, simulate the blast radius by analyzing all
  call sites, import chains, type dependencies, and test coverage for the
  affected area. Produces a "what-if" impact report with risk scores — without
  touching any code. Use when the user asks about "blast radius", "impact
  analysis", "refactor simulator", "what if I change", "what if I rename",
  "what if I move", "리팩토링 시뮬레이션", "영향 분석", "before refactoring",
  or wants to understand the consequences of a proposed change before executing it.
  Do NOT use for executing refactors (use simplify or generalPurpose), code
  review of existing code (use deep-review), or debugging (use diagnose).
metadata:
  author: thaki
  version: 1.0.0
---

# Refactor Simulator — Pre-Change Blast Radius Analysis

Predict the impact of a code change before you make it. Maps dependencies, counts call sites, checks test coverage, and produces a risk-scored impact report — all without modifying a single file.

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

### Step 2: Build Dependency Graph

For the target symbol, trace all connections:

#### 2a. Downstream Dependencies (what uses this?)

Use `rg -F` (fixed-string / literal) for the initial scan to avoid regex escaping issues, then refine with context:

```bash
# Find all import statements referencing the target (literal match)
rg -F "{target}" --type ts --type py -l

# Find call sites (regex needed for parenthesis pattern)
rg "{target}\s*\(" --type ts --type py -l

# Find JSX usage (React components)
rg "<{target}[\s/>]" --glob "*.tsx" -l

# Find re-exports
rg -F "{target}" --glob "**/index.ts" --glob "**/index.tsx" -l
```

Replace `{target}` with the actual symbol name. If the symbol contains regex special characters (e.g., `$`, `.`), always use `rg -F`.

#### 2b. Upstream Dependencies (what does this use?)

Read the target file and extract all its imports, inherited types, and called functions.

#### 2c. Re-export Chains

Check if the symbol is re-exported through barrel files (`index.ts`, `__init__.py`):

```bash
rg "export.*{target}" --type ts -l
rg "from.*{module}.*import.*{target}" --type py -l
```

### Step 3: Enumerate Call Sites

For each file that references the target, collect:
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

For the affected files, determine test coverage:

1. Find test files that import or test the target:
   ```bash
   rg -F "{target}" --glob "**/*test*" --glob "**/*spec*" --glob "**/__tests__/**" -l
   ```
2. Check if affected call sites have corresponding tests
3. Calculate coverage ratio: `tested_call_sites / total_call_sites`

### Step 5: Calculate Risk Score

```
risk_score = (call_site_count * call_site_weight)
           + (untested_sites * untested_weight)
           + (type_chain_depth * type_weight)
           + (re_export_count * re_export_weight)

Where:
  call_site_weight  = 1.0
  untested_weight   = 3.0  (untested sites are 3x riskier)
  type_weight       = 2.0  (type changes cascade)
  re_export_weight  = 2.0  (re-exports multiply blast radius)
```

Risk levels:
- **LOW** (score < 10): Few call sites, good test coverage
- **MEDIUM** (score 10-30): Moderate impact, some untested paths
- **HIGH** (score 30-60): Many call sites or significant untested code
- **CRITICAL** (score > 60): Widespread impact with poor test coverage

### Step 6: Generate Impact Report

```
Refactor Simulation Report
===========================
Proposed Change: [description]
Target: [symbol] in [file]
Action: [rename|move|delete|extract|split|modify-signature]

Blast Radius:
  Files affected:     [N] production + [N] test
  Call sites:         [N] total ([N] tested, [N] untested)
  Type references:    [N]
  Re-export chains:   [N]

Risk Score: [score] ([LOW|MEDIUM|HIGH|CRITICAL])

Files That Would Change:
  1. [file] — [reason: update import path / rename reference / remove usage]
  2. [file] — [reason]
  ...

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

### Step 7: Simulation Variants

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
| Symbol not found in codebase | Report with suggestions for similar names |
| Ambiguous symbol (multiple definitions) | List all definitions, ask user to choose |
| Dynamic imports or string references | Flag as "potentially affected, verify manually" |
| Circular dependencies detected | Report the cycle and warn about cascade risk |
| Very large blast radius (100+ files) | Summarize by directory; offer detailed drill-down |

## Troubleshooting

- **Symbol not found**: Ensure the exact casing matches. Try `rg -Fi "{target}"` for case-insensitive search.
- **False positives in search**: `rg -F` matches substrings. For `get`, it matches `getUser`, `forget`. Use `rg -Fw "{target}"` for whole-word matching.
- **Dynamic imports missed**: `import()` expressions and `require()` calls won't match standard import patterns. Check for `rg "require.*{target}"` separately.
- **Monorepo scope**: If the project spans multiple packages, scope the search with `--glob "packages/my-app/**"` to avoid cross-package noise.
