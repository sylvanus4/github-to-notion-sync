## Refactor Simulator

Simulate the blast radius of a proposed code change — dependency graph, call sites, test coverage, and risk score — without modifying any code.

### Usage

```
/refactor-simulator "rename getUserById to findUserById"
/refactor-simulator "move src/utils/auth.ts to src/lib/auth/"
/refactor-simulator "delete UserProfile component"
/refactor-simulator "extract validateInput into a shared module"
/refactor-simulator --symbol "useAuth" --action rename
```

### Workflow

1. **Parse change** — Extract target symbol, action type, source/destination
2. **Build dependency graph** — Trace imports, call sites, type references, re-exports
3. **Assess test coverage** — Find tests that exercise affected code paths
4. **Calculate risk score** — Weighted formula: call sites, untested paths, type chains
5. **Generate impact report** — Files affected, tests at risk, estimated effort

### Execution

Read and follow the `refactor-simulator` skill (`.cursor/skills/refactor-simulator/SKILL.md`) for search patterns, risk formula, and report format.

### Examples

Rename a function:
```
/refactor-simulator "rename getUserById to findUserById in src/api/users/service.ts"
```

Delete a component:
```
/refactor-simulator "delete LegacyModal component"
```

Move a module:
```
/refactor-simulator "move src/utils/auth.ts to src/lib/auth/index.ts"
```
