# CONTEXT.md Format

CONTEXT.md defines the shared language for a project. It's the domain glossary that humans and agents both use.

## Format

```markdown
# Context

## Terms

**term-name** — One-sentence definition that eliminates ambiguity. [Optional: contrast with what it's NOT.]

**another-term** — Definition. Related to: **term-name**.
```

## Rules

1. **Be opinionated.** "A widget is X" not "A widget could be X or Y." If there's ambiguity, resolve it.
2. **Flag conflicts.** If a term means different things in different parts of the codebase, call it out explicitly.
3. **Keep definitions to one sentence.** If you need more, the term is probably two terms.
4. **Show relationships.** "Related to: **other-term**" helps build the mental model.
5. **Version is implicit.** CONTEXT.md evolves with the codebase. Don't add version numbers.

## When to Add a Term

Add a term when:

- Two people use different words for the same thing
- One word is used to mean different things
- A concept is central to the domain but not obvious from code
- The agent keeps misunderstanding something

## Example

```markdown
# Context

## Terms

**materialization** — The process of creating a file on disk for a lesson that was previously virtual (metadata-only). Not the same as "publishing" (making available to students).

**section** — A named group of lessons within a course. Sections define order and grouping but have no content of their own. Related to: **lesson**, **course**.

**lesson** — An individual piece of content (video, exercise, text). Always belongs to exactly one **section**. Can be virtual (no file) or materialized (has file).

**materialization cascade** — When materializing a lesson triggers the materialization of its parent section and any dependent resources. This is the operation, not the state.
```
