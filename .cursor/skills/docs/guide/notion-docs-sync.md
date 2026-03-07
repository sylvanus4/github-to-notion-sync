## 개요

Markdown 문서를 Notion에 동기화하는 스킬이다. 문서를 작성하거나 수정한 뒤 "Notion에 동기화해줘"라고 요청하면 에이전트가 자동으로 처리한다.

> 트리거 키워드: Notion, 문서 동기화

## 사전 조건

- Node.js 18+
- `NOTION_TOKEN` 환경변수 (Notion Integration Token)
- 동기화할 문서 폴더에 `.notion-sync.yaml`이 있어야 한다 (없으면 에이전트가 `init.sh`로 자동 초기화)

프로젝트 루트뿐 아니라 개별 문서 폴더에도 `.notion-sync.yaml`을 배치할 수 있다. 예: `.cursor/skills/docs/`, `docs/infra/` 등 폴더마다 독립적인 동기화 설정이 가능하다.

## 절차

### 1. 최초 설정 (한 번만)

동기화할 폴더에 `.notion-sync.yaml`이 없으면 에이전트에게 요청한다.

```
"Notion 동기화 설정해줘"
"docs/infra 디렉토리에 Notion 동기화 초기화해줘"
".cursor/skills/docs에 Notion 동기화 설정해줘"
```

에이전트가 수행하는 작업:
- `init.sh`로 `.notion-sync.yaml` 템플릿, `NOTION-SYNC.md`(작성 규칙) 복사
- `spec/`, `guide/` 디렉토리 생성
- npm 의존성 설치

### 2. 문서 작성

문서를 직접 작성하거나 에이전트에게 요청한다.

```
"API 설계 규칙 문서 작성해줘"
"배포 프로세스 가이드 만들어줘"
```

에이전트는 `NOTION-SYNC.md`에 정의된 작성 규칙(헤딩, 리스트 깊이, 파일명 등)을 자동으로 따른다.

### 3. yaml에 문서 등록

새 문서를 만들었으면 `.notion-sync.yaml`에 등록해야 한다. 직접 해도 되고 에이전트에게 요청해도 된다.

```
"방금 만든 문서를 notion-sync.yaml에 추가해줘"
```

### 4. Notion에 동기화

문서 작성이 끝나면 동기화를 요청한다.

```
"Notion에 동기화해줘"
"spec/api-design.md만 Notion에 동기화해줘"
"전체 문서 동기화해줘"
```

에이전트가 `sync.mjs`를 실행하여 Notion 페이지 내용을 초기화한 뒤 Markdown을 Notion 블록으로 변환하여 업로드한다.

### 5. 문서 수정 후 재동기화

기존 문서를 수정한 뒤 다시 동기화하면 Notion 페이지가 최신 내용으로 갱신된다.

```
"api-design.md 수정했으니 Notion에 다시 동기화해줘"
```

## 검증

- Notion에서 해당 페이지를 열어 내용이 반영되었는지 확인한다
- 동기화 스크립트 실행 후 터미널에 성공/실패 로그가 출력된다

## 트러블슈팅

| 증상 | 원인 | 해결 |
|------|------|------|
| `NOTION_TOKEN` 에러 | 환경변수 미설정 | `export NOTION_TOKEN="<토큰>"` 실행 |
| 페이지가 생성되지 않음 | Notion DB에 `Sync ID` 속성 없음 | DB에 rich_text 타입 `Sync ID` 속성 추가 |
| 내용이 깨짐 | H1 사용, 리스트 3단계 등 규칙 위반 | `NOTION-SYNC.md` 작성 규칙 확인 |
| yaml 파일을 못 찾음 | CWD에 `.notion-sync.yaml` 없음 | yaml 경로를 명시하거나 해당 디렉토리에서 실행 |
