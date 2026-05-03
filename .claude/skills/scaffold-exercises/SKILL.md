---
name: scaffold-exercises
description: >-
  Create structured exercise directories with problems, starter code,
  solutions, explainers, and test harnesses for courses, onboarding, and
  interactive learning materials. Use when the user asks to "create
  exercises", "scaffold exercises", "build course content", "generate practice
  problems", "onboarding exercises", "coding katas", "workshop materials", "교육
  콘텐츠 생성", "연습 문제 만들기", "온보딩 자료", "코딩 카타", "워크숍 자료", or needs structured
  learning content with progressive difficulty. Do NOT use for reference docs
  without exercises (use technical-writer), slide decks (use anthropic-pptx),
  quizzes from existing docs (use docs-tutor-setup), or full curricula with
  NotebookLM (use nlm-curriculum-builder).
---

# Scaffold Exercises

Generate complete exercise directory structures with sections, problems, solution files, explainer documents, and test harnesses — ready for course content, team onboarding, or interactive documentation.

## When to Use

- Building course content or tutorials with hands-on exercises
- Creating onboarding materials for new team members
- Documenting complex systems as interactive learning paths
- Generating coding katas or practice problem sets
- Building workshop or training materials with progressive difficulty

## When NOT to Use

- Writing reference documentation without exercises (use `technical-writer`)
- Creating slide decks or presentations (use `anthropic-pptx` or `presentation-strategist`)
- Generating quizzes from existing docs (use `docs-tutor-setup`)
- Building full course curricula with NotebookLM integration (use `nlm-curriculum-builder`)

## Workflow

### Phase 1: Define Exercise Structure

1. Gather from the user:
   - **Topic**: What subject area (e.g., "React hooks", "SQL joins", "Git branching")
   - **Audience**: Skill level (beginner, intermediate, advanced)
   - **Count**: Number of exercises (default: 5-10)
   - **Format**: Language/framework for code exercises
2. Determine section grouping:
   - Single flat set of exercises, or
   - Multiple sections with progressive difficulty

### Phase 2: Generate Directory Structure

Create the following structure:

```
exercises/
├── README.md                    # Overview, prerequisites, how to use
├── section-01-fundamentals/
│   ├── README.md                # Section overview and learning objectives
│   ├── 01-problem.md            # Problem statement with requirements
│   ├── 01-starter/              # Starter code (if applicable)
│   │   └── index.ts
│   ├── 01-solution/             # Reference solution
│   │   └── index.ts
│   ├── 01-explainer.md          # Why the solution works, concepts covered
│   ├── 01.test.ts               # Test file to verify solution
│   ├── 02-problem.md
│   ├── 02-starter/
│   │   └── index.ts
│   ├── 02-solution/
│   │   └── index.ts
│   ├── 02-explainer.md
│   └── 02.test.ts
├── section-02-intermediate/
│   └── ...
└── section-03-advanced/
    └── ...
```

### Phase 3: Write Exercise Content

For each exercise, generate:

1. **Problem file** (`NN-problem.md`):
   - Clear problem statement
   - Input/output examples
   - Constraints and edge cases
   - Hints (progressive, spoiler-tagged)

2. **Starter code** (`NN-starter/`):
   - Function signatures with TODO comments
   - Type definitions (for TypeScript)
   - Import statements pre-configured

3. **Solution code** (`NN-solution/`):
   - Clean, idiomatic implementation
   - Comments explaining non-obvious decisions
   - Multiple approaches if instructive

4. **Explainer** (`NN-explainer.md`):
   - Concept being taught
   - Why this approach works
   - Common mistakes and how to avoid them
   - Links to further reading

5. **Test file** (`NN.test.ts`):
   - Happy path tests
   - Edge case tests
   - Tests that guide the learner (descriptive names)

### Phase 4: Generate Index and Metadata

1. Create root `README.md` with:
   - Course title and description
   - Prerequisites
   - How to run exercises (`npm test`, `vitest`, etc.)
   - Table of contents linking to each section and exercise
   - Estimated time per exercise
2. Add difficulty ratings per exercise (easy / medium / hard)
3. Add dependency notes (which exercises build on previous ones)

## Exercise Design Principles

- **Progressive difficulty**: Each exercise builds on concepts from the previous one
- **One concept per exercise**: Avoid combining too many new ideas
- **Runnable from day one**: Starter code should compile/run with failing tests
- **Self-contained**: Each exercise should work independently after the section prereqs
- **Real-world relevant**: Use realistic scenarios, not abstract puzzles

## Gotchas

1. **Starter code that doesn't compile = immediate learner frustration.** The starter must build and run cleanly — only the tests should fail. If `npm test` crashes instead of showing red tests, the exercise is broken.
2. **Solutions that don't match tests = trust destroyed.** Always verify that the solution file passes every test before shipping. A single failing test in a "reference solution" undermines the entire exercise set.
3. **Too many concepts per exercise = confusion.** Each exercise should teach exactly one new idea. If a problem requires knowledge of 3 new concepts, split it into 3 exercises.
4. **Missing dependency chain documentation.** If exercise 05 requires concepts from exercise 03, say so explicitly. Learners who skip ahead will blame the exercise, not themselves.

## Verification

After completing all phases:
1. Run the test runner against all starter code — every test must fail (not error/crash)
2. Run the test runner against all solution code — every test must pass
3. Confirm each problem file is under 200 words for the core requirement
4. Verify exercise numbering is zero-padded and filesystem-sortable
5. Check that `README.md` includes setup instructions and a table of contents

## Anti-Example

```markdown
# BAD: Starter code that crashes instead of failing tests
# starter/index.ts contains:
import { nonExistentModule } from './missing'  # Build error, not test failure

# BAD: Problem statement that teaches 3 concepts at once
"Implement a debounced async React hook that uses generics and AbortController"
→ Should be 3 separate exercises: generics → AbortController → debounced hook

# BAD: No test file provided
# exercises/01-problem.md exists but 01.test.ts is missing
# → Learner has no way to verify their solution
```

## Constraints

- Starter code must compile/run without errors (tests should fail, not the build)
- Solutions must pass all provided tests
- Explainers should be understandable without reading the solution first
- Exercise numbering should be zero-padded for filesystem sorting (01, 02, ... 10)
- Keep problem statements concise — under 200 words for the core requirement
- Include a `package.json` or equivalent config file so learners can run tests immediately
- Do NOT generate more than 15 exercises in a single run — quality degrades with volume; split into multiple sections instead

## Output

1. Complete directory structure with all files
2. Root README with table of contents, prerequisites, and setup instructions
3. Per-section README with learning objectives
4. Per-exercise: problem, starter, solution, explainer, and tests
5. Configuration file for the test runner (e.g., `vitest.config.ts`)
