---
name: screen-description
description: 러프한 사용자 입력을 받아 구조화된 화면 설명 문서(Markdown)를 생성/업데이트합니다. 화면 설명, 기획서, 화면 기획, 스크린 디스크립션, UI 명세, 화면 스펙 작성 시 사용합니다. Do NOT use for 코드 생성(fsd-development), Figma 디자인 변환(figma-to-tds).
metadata:
  version: 1.1.0
  category: generation
---

# Screen Description Generator

러프한 텍스트 입력을 받아 구조화된 화면 설명 문서(Markdown)를 생성/업데이트한다.

## Storage path

```
ai-platform/frontend/docs/screens/
├── workloads/
│   ├── workloads-list.md
│   └── workloads-detail.md
├── templates/
│   ├── templates-list.md
│   └── templates-create.md
└── ...
```

- 폴더명: 페이지 도메인 (kebab-case)
- 파일명: `{도메인}-{화면명}.md`

## Workflow

### Step 0 – Figma 디자인 데이터 수집 (선택)

Figma URL이 제공된 경우에만 실행. `figma-to-tds` Skill의 Step 1~3을 참조.

1. Figma MCP로 `get_design_context` + `get_screenshot` 병렬 호출
2. 레이아웃 구조, 컴포넌트 목록, 색상/간격 토큰을 추출
3. 결과를 아래 Step 2의 **레이아웃 구조**, **컴포넌트 구성** 섹션에 반영

### Step 1 – 입력 분석

1. 러프한 텍스트에서 **대상 화면**과 **핵심 내용**을 파악
2. 기존 문서 확인: `ai-platform/frontend/docs/screens/{domain}/`
3. 기존 페이지 컴포넌트가 있으면 현재 구현 상태 참고: `src/pages/{domain}/`
4. Swagger/API 명세가 제공되면 "API 연동" 섹션 자동 채움

### Step 2 – 문서 생성 또는 업데이트

- **신규**: 문서 템플릿([references/document-template.md](references/document-template.md))으로 새 문서 생성
- **업데이트**: 해당 섹션만 수정, 변경 이력 추가
- **Figma 데이터 있으면**: "레이아웃 구조"와 "컴포넌트 구성" 섹션을 Figma 분석 결과로 채움

### Step 3 – 사용자 확인

생성/수정한 문서의 요약을 보여주고 추가 수정 여부를 확인.

## Section usage rules

| 섹션 | 필수 여부 | 적용 기준 |
|------|----------|-----------|
| 화면 개요 | **필수** | 항상 포함 |
| 레이아웃 구조 | 권장 | 레이아웃 언급 시 |
| 컴포넌트 구성 | 선택 | 구현 관련 언급 시 |
| 인터랙션 정의 | 권장 | 동작/이벤트 언급 시 |
| 상태별 화면 | 권장 | 상태 분기 언급 시 |
| API 연동 | 선택 | API 언급 시 |
| 다국어 | 선택 | i18n 언급 시 |
| 접근성 | 선택 | 접근성 언급 시 |

**입력이 러프할수록**: 필수 + 권장만 채우고 나머지는 `{TODO: 추후 정의}` 플레이스홀더.
**입력이 상세할수록**: 해당하는 모든 섹션을 채움.

## Naming conventions

- **폴더명**: 페이지 라우트와 일치 (예: `src/pages/workload/` → `docs/screens/workloads/`)
- **파일명**: `{도메인}-{화면동작}.md` (예: `workloads-list.md`, `workloads-deploy.md`)
- **복합 화면**: 탭/모달이 포함된 경우 메인 화면 파일에 서브섹션으로 작성

## Update rules

1. 기존 내용을 **절대 삭제하지 않는다** (명시적 요청 제외)
2. 변경된 섹션만 수정
3. **변경 이력** 테이블에 날짜와 변경 내용 추가
4. `마지막 업데이트` 날짜 갱신

## Cross-reference

| 상황 | 연결 Skill |
|------|-----------|
| Figma URL이 주어졌을 때 | `figma-to-tds` → Step 0에서 디자인 데이터 수집 |
| 기획서 완성 후 구현 시 | `implement-screen` → Phase 3으로 코드 생성 진행 |
| i18n 키 정리 필요 시 | Rule: `06-i18n-rules.mdc` → 기획서 i18n 섹션 기반 키 추가 |

## Checklist

- [ ] 대상 화면 식별 완료
- [ ] 저장 경로 확인 (`docs/screens/{domain}/{file}.md`)
- [ ] 기존 문서 존재 여부 확인
- [ ] 필수 섹션(화면 개요) 포함
- [ ] 업데이트 시 변경 이력 추가

## Examples

### Example 1: 러프한 텍스트로 신규 기획서 생성
User says: "워크로드 목록 화면 기획서 만들어줘. 테이블로 보여주고 생성/삭제 기능 필요"
Actions:
1. `docs/screens/workloads/workloads-list.md` 경로에 신규 문서 생성
2. 화면 개요, 레이아웃 구조, 인터랙션 정의(생성/삭제) 섹션 채움
3. 상세하지 않은 부분은 TODO 플레이스홀더로 남김
Result: 구조화된 기획서가 생성되어 implement-screen에서 바로 사용 가능

### Example 2: Figma URL + 텍스트로 기획서 업데이트
User says: "templates-create.md 기획서에 Figma 디자인 반영해줘. Figma: https://figma.com/design/abc/..."
Actions:
1. 기존 기획서 읽기 + Figma MCP로 디자인 데이터 수집
2. 레이아웃 구조, 컴포넌트 구성 섹션을 Figma 분석 결과로 업데이트
3. 변경 이력에 업데이트 기록 추가
Result: Figma 디자인이 반영된 기획서로 업데이트됨

## Troubleshooting

### 기존 기획서 내용이 덮어씌워짐
Cause: 전체 문서를 새로 쓰면서 기존 섹션이 유실됨
Solution: Update rules 준수 — 변경된 섹션만 수정하고, 기존 내용은 절대 삭제하지 않음

### Figma 데이터가 기획서에 반영되지 않음
Cause: Step 0 (Figma 수집)을 건너뛰거나, MCP 호출 실패
Solution: Figma URL이 있으면 반드시 Step 0을 실행. MCP 에러 시 사용자에게 알리고 텍스트 기반으로 진행
