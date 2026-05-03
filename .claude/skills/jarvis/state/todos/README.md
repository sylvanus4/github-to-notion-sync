# Jarvis TODO Wiki

LLM-friendly wiki-style TODO system. 각 TODO는 frontmatter 메타 + 마크다운 본문을 가진 독립 파일이며, INDEX는 자동/수동 큐레이션. Goal Mode와 분리 — Goal은 "지금 자동 추구할 단일 목표", TODO는 "백로그 + 의사결정 대기열".

## 디자인 원칙 (LLM 위키 본떠)

| 원칙 | 적용 |
|------|------|
| **One file = one entity** | TODO 1건 = `todo-{slug}.md` 1파일 (검색 단순) |
| **Frontmatter 메타** | YAML frontmatter — id/status/priority/cost/tags/관련 항목 |
| **Wiki backlinks** | `related_todos`, `related_skills`, `related_goals`, `source` 필드로 그래프 |
| **Append-only history** | 본문 하단 `## History` 섹션에 상태 변경 시각/이유 누적 |
| **Markdown 본문** | Context / Acceptance criteria / Notes / Implementation hint 표준 섹션 |
| **Status FSM** | `open → in-progress → done` 또는 `open → blocked → open` 또는 `* → archived` |
| **Goal 승격** | TODO `promote` 시 `state/goals/<id>.json`로 변환 + frontmatter `promoted_to_goal` 기록 |
| **자동 검증 (선택)** | acceptance criterion에 `check_cmd` 부착 시 `goal-continuation.py` 재사용 |

## 디렉토리

```
state/todos/
├── README.md           # 본 문서
├── INDEX.md            # 모든 TODO 한눈에 (status별 그룹)
├── BACKLOG.md          # 우선순위 큐레이션 (P0/P1/P2/P3)
├── todo-{slug}.md      # 개별 TODO
└── _archive/
    └── todo-{slug}.md  # done/cleared 후 이동
```

## TODO 파일 템플릿

```markdown
---
id: <kebab-slug>
title: <한 줄 제목>
status: open|in-progress|blocked|done|archived
priority: P0|P1|P2|P3
estimated_cost_usd: 0.00
estimated_time: 10min|2h|...
related_todos: []
related_skills: []
related_goals: []
source: <원본 파일 경로 또는 ref>
tags: []
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
---

# <title>

## Context
왜 필요한가, 출처/계기

## Acceptance criteria
- [ ] criterion 1 (`check_cmd: ...` 옵션)
- [ ] criterion 2

## Notes / Implementation hint
구현 힌트, 회피책, 위험요소

## History
- YYYY-MM-DD HH:MM — created (source: ...)
- YYYY-MM-DD HH:MM — status: open → in-progress (reason)
```

## Sub-commands (jarvis SKILL.md에서 호출)

```
jarvis todo add: <title>             # 새 TODO 생성 (interactive)
jarvis todo list [--status=open]     # 필터 가능
jarvis todo show <id>                # 상세
jarvis todo done <id>                # done 처리 + History 추가
jarvis todo archive <id>             # _archive/로 이동
jarvis todo block <id>: <reason>     # blocked 처리
jarvis todo unblock <id>             # blocked → open
jarvis todo promote <id>             # Goal로 승격
jarvis todo reindex                  # INDEX.md / BACKLOG.md 재생성
```

## INDEX vs BACKLOG

- **INDEX.md** — 단순 status별 전체 목록 (자동 생성 가능)
- **BACKLOG.md** — 사람이 큐레이션하는 우선순위 (P0 위쪽, "다음에 할 것")

둘 다 source-of-truth 아님. **개별 todo 파일이 진실원**.

## Status FSM

```
        ┌──────────┐
        │   open   │◄────────┐
        └────┬─────┘         │
             │ work begins   │ unblock
             ▼               │
   ┌──────────────────┐      │
   │  in-progress     │──────┤
   └────┬─────────────┘  block
        │ acceptance met
        ▼
   ┌──────────┐
   │   done   │
   └────┬─────┘
        │ (archive 7일 후 자동)
        ▼
   ┌────────────┐
   │  archived  │   _archive/로 이동
   └────────────┘
```

## Goal과의 관계

- TODO: 백로그 항목, 사람이 트리거할 때 작업 시작
- Goal: 다중 턴 자동 추구 (Ralph Loop), evaluation_criteria 필수

전이: TODO `promote` → Goal 생성 (acceptance criteria → evaluation_criteria 매핑). TODO frontmatter에 `promoted_to_goal: <goal-id>` 기록되어 양방향 연결.
