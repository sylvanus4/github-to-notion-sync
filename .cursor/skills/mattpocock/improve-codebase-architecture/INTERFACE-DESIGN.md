# Interface Design Principles

Concrete guidelines for designing deep module interfaces.

## The Golden Rule

**The best interface is one the caller already knows how to use.** Before inventing something new, check if there's a pattern the caller is already familiar with — a standard library convention, a project idiom, or a well-known design pattern.

## Fewer, More Powerful Methods

A deep module has fewer methods, each of which does more work. This is counterintuitive — it feels like more methods = more flexibility. But each additional method is a concept the caller must learn.

**Signs you have too many methods:**
- Several methods are always called together in the same sequence
- Methods share most of their parameters
- Removing a method would not reduce the module's capability (it's just a convenience wrapper)

**Fix:** Merge related methods. The combined method should handle the common cases internally, not force callers to compose them.

**Exception:** When two operations are genuinely independent and callers commonly need one without the other, keep them separate.

## Parameter Reduction

Every parameter is a decision the caller must make. Reduce parameters by:

1. **Absorbing decisions into the module.** If a parameter has an obvious right answer 90% of the time, make it a default.
2. **Combining related parameters into a named concept.** Instead of `(host, port, username, password)`, accept `ConnectionConfig`.
3. **Eliminating parameters by redesign.** If a parameter exists because of an implementation detail, hide that detail.

## Return Value Design

The return value is part of the interface. Simplify it:

- **Return the thing the caller needs**, not the thing the module happens to have. Transform internally if needed.
- **Avoid returning errors when you can handle them internally.** If a retry fixes the problem, retry internally — don't make the caller retry.
- **Avoid returning optional values when a default is sensible.** `getOrDefault` is simpler than `get` + null check.

## Pass-Through Detection

A **pass-through method** is a method that does nothing but delegate to another method with the same (or nearly the same) signature. It adds interface complexity without hiding anything.

**Detection:** If you can describe a method as "it just calls X with the same arguments," it's a pass-through.

**Fixes:**
- **Eliminate the pass-through.** Have callers call the underlying method directly.
- **Give it responsibility.** If the pass-through exists for a reason (logging, validation, transformation), make that reason explicit and substantial.
- **Merge the two layers.** If the pass-through and the underlying method are always used together, they may belong in the same module.

## Exception Reduction

Exceptions are part of the interface — every exception a method can throw is a concept the caller must handle.

**Strategies to reduce exceptions:**

1. **Define errors out of existence.** Redesign the interface so the error condition can't happen. Example: instead of throwing "key not found," return a default value.

2. **Mask exceptions internally.** If the module can handle the error without the caller knowing, do it. Retries, fallbacks, and graceful degradation belong inside the module.

3. **Aggregate exceptions.** Instead of many specific exceptions, use one exception type with a category. Callers who don't care about the specific cause can catch one thing.

4. **Crash early for bugs.** Programming errors (null where non-null is expected, invalid state) should crash, not throw recoverable exceptions. These are bugs, not runtime conditions.

## Configuration Design

Configuration is interface. Every config option is a decision the caller must make.

**Rules:**
- **Fewer options.** Each option must earn its place. If you can pick a sensible default, do it.
- **Opinionated defaults.** Don't be "flexible" — be useful. A module that works well out of the box is more valuable than one that requires 20 config options to do anything.
- **Layered overrides.** Provide a simple path (zero config) and an advanced path (full control). Most callers should never need the advanced path.
