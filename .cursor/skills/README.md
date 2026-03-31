# Cursor Skills

Cursor AI 에이전트가 특정 키워드를 감지하면 자동으로 참조하는 스킬 모음.

## 스킬 목록

| 스킬                                                              | 트리거 키워드                 | 설명                                             |
| ----------------------------------------------------------------- | ----------------------------- | ------------------------------------------------ |
| [github-workflow-automation](github-workflow-automation/SKILL.md) | 이슈, 커밋, PR, 깃 워크플로우 | 이슈 → 브랜치 → 커밋 → PR 생성까지 GitHub 자동화 |
| [notion-docs-sync](notion-docs-sync/SKILL.md)                     | Notion, 문서 동기화           | Markdown 문서를 Notion에 동기화                  |

## 구조

```
.cursor/skills/
├── README.md                      ← 이 파일
├── docs/                          ← Notion 동기화 대상 문서
│   ├── .notion-sync.yaml
│   ├── NOTION-SYNC.md
│   └── guide/
├── github-workflow-automation/
│   └── SKILL.md
└── notion-docs-sync/
    ├── SKILL.md
    ├── scripts/
    └── templates/
```

## 사용법

에이전트가 트리거 키워드를 감지하면 해당 `SKILL.md`를 자동으로 읽고 절차를 따른다. 수동으로 참조하려면 채팅에서 `@SKILL.md` 형태로 멘션하면 된다.

## 문서

스킬별 상세 가이드는 [docs/guide/skills-index.md](docs/guide/skills-index.md)에 정리되어 있으며, Notion DB에도 동기화되어 있다.

## Notion 동기화

`docs/` 디렉토리의 문서를 Notion에 동기화하려면:

```bash
export NOTION_TOKEN="<Notion Integration Token>"
node .cursor/skills/notion-docs-sync/scripts/sync.mjs .cursor/skills/docs/.notion-sync.yaml
```

설정 및 작성 규칙은 [docs/NOTION-SYNC.md](docs/NOTION-SYNC.md) 참조.
