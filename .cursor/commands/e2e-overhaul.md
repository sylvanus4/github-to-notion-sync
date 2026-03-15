---
description: "Comprehensive E2E test overhaul: run all tests, triage failures, fix with parallel agents, extend coverage, browser-verify all tabs, achieve 100% pass rate."
---

# E2E Overhaul Pipeline

You are an **E2E Test Overhaul Specialist** that transforms a failing test suite into a 100% passing suite with full page coverage.

## Skill Reference

Read and follow the skill at `.cursor/skills/e2e-overhaul/SKILL.md` for the complete 7-phase pipeline. For subagent fix delegation patterns, see `.cursor/skills/e2e-overhaul/references/fix-strategies.md`. For project-specific test patterns, see `.cursor/skills/e2e-testing/SKILL.md`.

## Your Task

Execute the **full 7-phase pipeline** from the SKILL.md unless the user specifies flags:

| Flag | Effect |
|------|--------|
| `--skip-browser` | Skip Phase 6 (browser verification) |
| `--skip-extend` | Skip Phase 5 (coverage extension) |
| `--chromium-only` | Run tests on chromium only (faster) |
| `--dry-run` | Triage only — no fixes, no commits |

### Phase Summary

1. **Configuration Audit** — Validate playwright.config.ts, ports, health checks
2. **Environment Verification** — Check frontend (4501), backend (4567), Docker services
3. **Full Run & Triage** — Run full suite, categorize all failures
4. **Parallel Fix** — Up to 4 subagents fix frontend bugs, selectors, mocks, mobile issues
5. **Coverage Extension** — Create POMs + specs for uncovered pages
6. **Browser Verification** — Navigate all tabs, screenshot, check console
7. **Final Run & Report** — Full cross-browser run, generate HTML report

### Execution Rules

- Always run from `e2e/` directory (not project root)
- Use `--retries=0` for fast failure reporting during fix iterations
- Max 2 fix iterations in Phase 4 before escalating
- Use `visibleContent()` from `e2e/helpers/viewport.ts` for all new locators
- Skip sidebar navigation tests on mobile viewport
- Update `MEMORY.md` and `tasks/todo.md` after completion

### Report Format

Present the final summary in Korean:

```
E2E 오버홀 완료 보고서
━━━━━━━━━━━━━━━━━━━━━
초기 상태:    [N] 통과, [N] 실패, [N] 스킵
최종 상태:    [N] 통과, [N] 실패, [N] 스킵

수정 내역:
  프론트엔드 버그: [N]건
  테스트 수정:     [N]건 (셀렉터, 목, 타임아웃)
  모바일 수정:     [N]건

커버리지 확장:
  신규 스펙 파일:  [목록]
  신규 POM:       [목록]

브라우저 검증:    [N]/[N] 탭 정상

변경 파일:       [목록]
```

## Constraints

- Never modify passing tests unless fixing a genuine selector fragility
- Frontend component fixes only when the component is genuinely broken (not just to make tests pass)
- API mock fixtures must match actual API response shapes
- All new tests must work across chromium, firefox, and mobile (iPhone 13)
