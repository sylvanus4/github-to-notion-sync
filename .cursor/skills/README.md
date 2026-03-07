# Cursor Skills

Cursor AI 에이전트가 특정 키워드를 감지하면 자동으로 참조하는 스킬 모음.

## 종합 가이드

전체 스킬 목록, 카테고리별 분류, 활용 예시는 **[docs/skill-guides/README.md](../../docs/skill-guides/README.md)** 를 참조하세요.

- **코어 프로젝트 스킬**: 73개 (코드 리뷰, 개발 전문가, 테스팅, DevOps, 보안, Git, 디자인, 문서화, PM, AI/프롬프트, 유틸리티, GWS)
- **KWP 도메인 스킬**: 93개 (영업, 마케팅, 데이터, 디자인, 엔지니어링, 재무, 인사, 법무 등)
- **전체 레지스트리**: [mission-control/references/skill-registry.md](mission-control/references/skill-registry.md)

## 구조

```
.cursor/skills/
├── README.md                          ← 이 파일
├── {skill-name}/
│   ├── SKILL.md                       ← 스킬 정의 (에이전트가 자동 로드)
│   └── references/                    ← 참조 문서 (선택)
├── mission-control/
│   ├── SKILL.md
│   └── references/
│       └── skill-registry.md          ← 전체 스킬 레지스트리
└── docs/                              ← Notion 동기화 대상 문서
```

## 사용법

에이전트가 트리거 키워드를 감지하면 해당 `SKILL.md`를 자동으로 읽고 절차를 따른다. 수동으로 참조하려면 채팅에서 `@SKILL.md` 형태로 멘션하면 된다.

## Notion 동기화

`docs/` 디렉토리의 문서를 Notion에 동기화하려면:

```bash
export NOTION_TOKEN="<Notion Integration Token>"
node .cursor/skills/notion-docs-sync/scripts/sync.mjs .cursor/skills/docs/.notion-sync.yaml
```

설정 및 작성 규칙은 [docs/NOTION-SYNC.md](docs/NOTION-SYNC.md) 참조.
