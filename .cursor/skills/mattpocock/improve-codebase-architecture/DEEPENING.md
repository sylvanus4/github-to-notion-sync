# Deepening Modules Safely

When deepening a module, classify its dependencies first. The classification determines your testing and refactoring strategy.

## Dependency Classification

### 1. In-Process Dependencies

Code in the same process that you own and can change.

**Strategy**: Inline or absorb. If the dependency is shallow, pull its implementation into the deeper module and delete the shallow one.

### 2. Local-Substitutable Dependencies

Dependencies that can be swapped via injection (interfaces, factories, config).

**Strategy**: Use seams. Define an internal interface, create an adapter for the real dependency, and inject a test double in tests.

### 3. Remote-But-Owned Dependencies

Services you own but that run in a separate process (your own microservices, databases you control).

**Strategy**: Contract tests. Test against the real dependency in CI, use test doubles locally. The contract test ensures the adapter stays in sync.

### 4. True External Dependencies

Third-party APIs, SaaS services, hardware.

**Strategy**: Adapter pattern. Never let external types leak into your domain. The adapter translates between external and internal types. Mock the adapter in tests.

## Deepening Checklist

- [ ] Classify each dependency
- [ ] For each dependency, choose the right strategy
- [ ] Add seams where missing
- [ ] Write tests at the correct level for each dependency type
- [ ] Verify the interface is simpler after deepening
- [ ] Verify no internal types leaked through the interface
