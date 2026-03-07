## Docs Tutor

Interactive quiz tutor that tracks concept-level proficiency across platform documentation. Discovers blind spots through targeted questions and drills weak areas.

### Usage

```
# Start a quiz session (auto-detects StudyVault)
/docs-tutor

# Quick hints for session types
/docs-tutor                   # choose session type interactively
```

### Session Types

| Type | When Available | Focus |
|------|---------------|-------|
| 진단 평가 | Unmeasured sections (⬜) exist | Broad assessment of new sections |
| 약점 집중 학습 | Weak sections (🟥/🟨) exist | Targeted practice on struggles |
| 섹션 선택 | Always | Study any section on demand |
| 하드 모드 복습 | All sections 🟩/🟦 | Challenge mastered material |

### Workflow

1. **Detect** — Find `StudyVault/` and read the learning dashboard
2. **Choose** — Present session options based on current proficiency (via AskQuestion)
3. **Quiz** — 4 questions per round, 4 options each, zero hints
4. **Grade** — Show results table, explain wrong answers
5. **Update** — Update concept files and dashboard with new proficiency data
6. **Repeat** — Loop for additional rounds if desired

### Progress Tracking

| Badge | Level | Rate |
|-------|-------|------|
| 🟥 | Weak | 0-39% |
| 🟨 | Fair | 40-69% |
| 🟩 | Good | 70-89% |
| 🟦 | Mastered | 90-100% |
| ⬜ | Unmeasured | No data |

### Prerequisites

Run `/docs-tutor-setup` first to generate the StudyVault from `docs/` files.

### Execution

Read and follow the `docs-tutor` skill (`.cursor/skills/docs-tutor/SKILL.md`) for quiz rules, grading, and file update protocol.
