# Language of Complexity

This is the vocabulary for talking about software complexity. These definitions are adapted from *A Philosophy of Software Design* by John Ousterhout, with practical refinements.

## Core Concept: Complexity

**Complexity** is anything related to the structure of a system that makes it hard to understand and modify. It manifests as:

- **Change amplification** — a simple change requires modifications in many places
- **Cognitive load** — how much a developer needs to know to complete a task
- **Unknown unknowns** — it's not obvious what you need to know, or even that there's something you need to know

Complexity is not about the size of the system or the difficulty of the problem. A large system with clear modules and simple interfaces can be less complex than a small one with tangled dependencies.

## Modules

### Deep Module

A **deep module** has a simple interface relative to the functionality it provides. The implementation is substantial, but callers don't need to understand it. Most of the complexity is hidden.

```
┌──────────────────────────────────────┐  ← small interface
│                                      │
│                                      │
│          lots of hidden              │
│          functionality               │
│                                      │
│                                      │
└──────────────────────────────────────┘
```

**Examples:**
- Unix file I/O: five basic calls (`open`, `read`, `write`, `lseek`, `close`) hide enormous complexity (disk drivers, caching, filesystems, permissions)
- A `sendWelcomeEmail(user)` function that handles template selection, variable substitution, SMTP config, and retries

**Deep modules are the goal.** They reduce the cognitive load on callers and concentrate knowledge in one place.

### Shallow Module

A **shallow module** has an interface that is nearly as complex as its implementation. It doesn't hide much — the caller needs to know almost as much as the module itself.

```
┌──────────────────────────────────────┐  ← big interface
│          little hidden               │
│          functionality               │
└──────────────────────────────────────┘
```

**Examples:**
- A `LinkedList` class that wraps a few pointer operations but exposes all the same concepts (nodes, next, previous)
- A "service" class that takes 8 config parameters and just passes them to another service

**Shallow modules add complexity.** They introduce a new interface (which must be learned) without reducing what callers need to know.

## Information Hiding

### Information Hiding

**Information hiding** is the most important technique for creating deep modules. Each module encapsulates a few design decisions — its "knowledge" — and presents a simple interface that doesn't expose those decisions.

The knowledge hidden by a module is its **power**. The more significant the hidden knowledge, the deeper the module.

**Good information hiding:**
- A storage module hides whether data is in Postgres, DynamoDB, or a file
- A pricing module hides the rules for discounts, tiers, and promotions
- An auth module hides the token format, refresh logic, and session management

### Information Leakage

**Information leakage** occurs when a design decision is reflected in multiple modules. This means a change to that decision requires touching all of them.

**Common causes:**
- **Temporal decomposition** — organizing modules by "when" things happen (read file, then parse it, then validate it) rather than by information (a single module that understands the file format)
- **Back-door leakage** — modules that share assumptions about data formats, protocols, or conventions without making those assumptions explicit in an interface
- **Configuration leakage** — forcing callers to specify details that should be internal decisions

### Temporal Decomposition

**Temporal decomposition** is organizing modules around the sequence of operations rather than around information. It produces many shallow modules that each know about the same data.

**Example of temporal decomposition (bad):**
```
readRawFile() → parseLines() → validateEntries() → buildIndex()
```
Each function knows about the file format — the knowledge is spread across four modules.

**Information-hiding alternative (good):**
```
FileIndex.load(path)
```
One module owns the file format knowledge. The sequence of operations is hidden inside.

## Interface Design

### Define Errors Out of Existence

The best way to handle errors is to design interfaces so errors can't happen. If a method can't fail, its callers don't need error-handling code.

**Example:** Instead of:
```typescript
// Caller must handle "key not found"
const value = map.get(key);
if (value === undefined) { ... }
```

Consider:
```typescript
// Returns default, never fails
const value = map.getOrDefault(key, fallback);
```

### Pull Complexity Downward

When there's a choice between making a module's interface simpler or its implementation simpler, **make the interface simpler**. It's better for the module author to suffer complexity than to impose it on every caller.

A module has many callers but only one implementation. Pushing complexity into the implementation means dealing with it once. Pushing it into the interface means dealing with it everywhere.

### Defaults

Good defaults are a form of information hiding. When a module provides sensible defaults, most callers don't need to specify anything.

**Key principle:** Optimize the interface for the common case. Rare cases can use an escape hatch (additional parameters, a builder, a config object) but should not clutter the default path.

## Tactical vs Strategic Programming

### Tactical Programming

**Tactical programming** is focused on getting the current task done as quickly as possible. Each change takes the shortest path, with the attitude "I'll clean it up later."

Tactical programming creates complexity incrementally. Each shortcut is small, but they accumulate. After enough tactical changes, the system is a mess — but no single change was obviously wrong.

### Strategic Programming

**Strategic programming** treats working code as necessary but not sufficient. The primary goal is a clean design that will make future changes easy. The attitude is "spend a little extra now to reduce complexity."

Strategic programming is an investment mindset: 10-20% of development time spent on design pays off within months, not years. The cost of *not* investing is complexity that slows everything down.

**This doesn't mean over-engineering.** Strategic thinking means:
- Making the interface as simple as possible for the current use case
- Hiding decisions that might change
- Resisting the urge to add flexibility "just in case"
- Spending time on naming and documentation
