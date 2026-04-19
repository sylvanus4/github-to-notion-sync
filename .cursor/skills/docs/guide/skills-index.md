## 개요

`.cursor/skills/`에 포함된 Cursor AI 에이전트 스킬의 사용 가이드 모음이다. 스킬은 특정 키워드를 포함한 요청을 하면 에이전트가 자동으로 인식하여 실행한다.

## 스킬 사용 방법

에이전트에게 자연어로 요청하면 된다. 키워드가 포함되면 해당 스킬이 자동 트리거된다.

```
"커밋해줘"             → GitHub 워크플로우 스킬
"새 도메인 추가해줘"   → FSD 개발 스킬
"Notion에 동기화해줘"  → Notion 동기화 스킬
```

## 하위 문서

레포지토리: [ThakiCloud/ai-platform-strategy](https://github.com/ThakiCloud/ai-platform-strategy) (`.cursor/skills/`)

| 문서 | 스킬 | 설명 |
|------|------|------|
| [FSD 개발 가이드](fsd-development.md) | `fsd-development` | 새 도메인 생성, 레거시 마이그레이션 요청 방법 |
| [GitHub 워크플로우 가이드](github-workflow.md) | `github-workflow-automation` | 이슈, 커밋, PR 요청 방법 |
| [Notion 동기화 가이드](notion-docs-sync.md) | `notion-docs-sync` | 문서 작성 후 Notion 동기화 요청 방법 |

## 공통 구조

모든 스킬은 동일한 디렉토리 패턴을 따른다.

```
.cursor/skills/{skill-name}/
├── SKILL.md          # 에이전트 진입점 (필수)
├── templates/        # 초기화 시 복사할 템플릿
└── scripts/          # 자동화 스크립트
```
