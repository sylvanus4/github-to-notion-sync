# Design It Twice

When deepening a module, explore at least two radically different interface designs before committing.

## Process

### 1. Frame the problem

State clearly:

- What the module does (behavior)
- Who calls it (consumers)
- What constraints exist (performance, backward compatibility, etc.)

### 2. Generate designs

Create 2-3 designs with different trade-offs:

- **Design A**: Optimize for simplicity (fewest methods, simplest types)
- **Design B**: Optimize for flexibility (extensibility, configurability)
- **Design C** (optional): Optimize for performance or some other constraint

Each design should be a sketch -- function signatures, type definitions, usage examples. Not full implementation.

### 3. Compare

For each design, evaluate:

| Criterion | Design A | Design B | Design C |
|-----------|----------|----------|----------|
| Interface size (methods/params) | | | |
| Depth (hidden complexity) | | | |
| Testability | | | |
| Migration effort from current | | | |
| Flexibility for future changes | | | |

### 4. Present and discuss

Show the user the comparison table and your recommendation. Let them challenge and refine.

## Rules

- Never go with the first design that comes to mind
- Each design must be genuinely different, not a minor variation
- It's fine to synthesize a hybrid from the best parts of each design
- Document the chosen design and rationale in an ADR if the decision is hard to reverse
