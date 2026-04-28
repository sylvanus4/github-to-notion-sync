# Shared Language for Architecture

These terms form the vocabulary for discussing codebase architecture. Use them consistently.

## Core Terms

**Module** — A unit of code that has an interface and an implementation. Can be a function, class, package, or service. The unit boundary is whatever makes sense in context.

**Interface** — What callers see: exported functions, types, API endpoints, CLI flags. The "surface area" of a module.

**Implementation** — What callers don't see: private functions, internal state, algorithms, database queries. The "volume" behind the interface.

**Depth** — The ratio of implementation complexity hidden behind interface simplicity. Deep = small interface, lots of hidden work. Shallow = big interface, little hidden work.

## Boundaries

**Seam** — A boundary in the code where one implementation can be substituted for another without changing callers. Good seams make testing and evolution easy.

**Adapter** — A thin wrapper that makes an external dependency conform to an internal interface. Adapters live at seams. They should be shallow by design -- their job is translation, not logic.

## Quality Measures

**Leverage** — How much capability a module delivers per unit of interface complexity. High leverage = "I call one function and a lot happens." Low leverage = "I call ten functions to do one thing."

**Locality** — How contained a change is within a single module. High locality = changing a feature means editing one module. Low locality = changing a feature means touching many modules.

## Principles

1. **Maximize depth** — Hide complexity behind simple interfaces
2. **Seams at boundaries** — Put substitution points where dependencies cross trust/ownership boundaries
3. **Adapters stay thin** — If an adapter has logic, it's not an adapter anymore
4. **Leverage over coverage** — One deep module beats five shallow ones
5. **Locality enables velocity** — If changes scatter, the module boundaries are wrong

## Relationships

```
Interface --(defines surface of)--> Module
Implementation --(is hidden by)--> Interface
Seam --(enables substitution at)--> Module boundary
Adapter --(lives at)--> Seam
Depth = Implementation complexity / Interface complexity
Leverage = Capability / Interface complexity
Locality = Changes contained / Total changes needed
```
