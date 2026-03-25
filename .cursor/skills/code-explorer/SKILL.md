---
name: code-explorer
description: >-
  기획자와 디자이너가 자연어로 코드 동작을 질의할 수 있는 인터랙티브
  탐색 도구입니다. 기술 용어를 기획 용어로 번역하여 설명합니다.
  Use when the user asks "이 버튼 누르면 뭐가 돼?", "에러 상태일 때 뭐가 보여?",
  "이 기능 어떻게 동작해?", "코드 설명해줘", "이 컴포넌트 뭐 하는 거야?",
  "이 API 뭐 하는 거야?", "code explorer", "explain code behavior",
  "what does this component do", "how does this feature work", "코드 탐색",
  "코드 질문",
  "기능 동작 설명", "화면 동작 설명", or asks natural-language questions about
  code behavior from a planner/designer perspective. Do NOT use for generating
  full planning documents from code (use code-to-spec). Do NOT use for code
  review or quality improvement (use code review tools). Do NOT use for writing or
  editing code (use appropriate development skills). Korean triggers: "코드
  탐색", "코드 질문", "동작 설명", "기능 설명", "뭐가 보여", "어떻게 동작".
metadata:
  author: "thaki"
  version: "1.2.0"
  category: "execution"
---
# Code Explorer — Code behavior Q&A

When planners and designers ask natural-language questions about code behavior, analyze the code and answer in planning-friendly terms (not raw engineering jargon).

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Input

| Input | Required | Notes |
|------|----------|------|
| **Natural-language question** | **Yes** | Korean or English question about behavior |
| Target path | Optional | If omitted, search the project |

---

## Workflow

### Step 1: Classify the question

Map the user question to one of these types:

| Type | Example | Analysis approach |
|------|---------|-------------------|
| **Behavior** | "What happens when I click this button?" | Trace handler → API → state updates |
| **State** | "What shows in the error state?" | Conditional rendering, error boundaries |
| **History** | "When was this feature added?" | git log / blame context |
| **Structure** | "What components make up this screen?" | Component tree |
| **Data** | "Where does this list data come from?" | API calls → data flow |
| **Policy** | "Who can use this feature?" | Auth guards, roles, middleware |

### Step 2: Explore code

**Behavior:**
1. Find relevant component/page (SemanticSearch or Grep)
2. Locate event handlers
3. Trace handler → API → response handling → state → UI updates (routing, modal, toast, etc.)

**State:**
1. Inspect conditional rendering
2. Trace `isLoading`, `isError`, `data`, etc.
3. List UI for each branch

**History:**
```bash
git log --oneline --follow -- <file>
git blame <file>
```

**Structure:**
1. Follow imports from page entry
2. Map component hierarchy

**Data:**
1. Find API usage (`fetch`, axios, `useQuery`, etc.)
2. Extract URL, params, response shape
3. Trace transforms

**Policy:**
1. Auth middleware
2. Role-based access
3. UI-level gates (disabled buttons, hidden menus)

### Step 3: Translate to planning terms

| Technical | Planning-friendly |
|-----------|-------------------|
| `useState`, `state` | On-screen state |
| `useQuery`, `fetch` | Loading data from server |
| `useMutation`, `POST/PUT` | Sending changes to server |
| `useEffect` | Runs when screen loads or inputs change |
| `onClick` | Action on click |
| `onSubmit` | Action on form submit |
| `router.push`, `navigate` | Navigate to another screen |
| `modal`, `dialog` | Popup / confirmation |
| `toast`, `notification` | Toast / notification |
| `isLoading` | Loading state |
| `isError`, `catch` | Error state |
| `role check`, `auth guard` | Permission check |
| `debounce` | Delay rapid input |
| `pagination` | Paged lists |
| `infinite scroll` | Load more on scroll |
| `cache`, `stale` | Cached data |
| `optimistic update` | Optimistic UI update |
| `callback`, callback fn | 후속 처리, 이어서 실행되는 처리 |
| `props` | 부모 화면에서 넘어온 전달 데이터 |
| mutating state / `setState` | 화면 상태 변경(갱신) |
| `ref` | 화면 밖 저장값 / DOM·컴포넌트 고정 참조 |
| `key` (list) | 목록에서 항목 식별용 표식 |
| `memo` / `useMemo` | 불필요한 재계산 줄이기 |
| `try` / `catch` | 오류 잡아서 분기 처리 |

### Anti-patterns (E1 / clarity)

- **Do NOT** lead explanations with raw code syntax, hook names, or variable names as if they were user-facing concepts (e.g. "`handleSubmit`가…", "`res`는…"). **Do** use descriptive Korean roles: "제출 시 실행되는 처리", "서버 응답 본문".
- **Do NOT** paste blocks of code as the answer unless the user explicitly asked for code; default is planning-language prose plus **file:line** citations.

### Step 4: Answer structure

**Pre-output — translation checklist (complete before sending):**

- [ ] Main narrative uses **planning language**; any English technical term is either a stable product term or paired with a short Korean gloss.
- [ ] No unexplained `use*` / API jargon in body text; map through Step 3 table or an explicit gloss.
- [ ] Sentences name **roles and outcomes**, not internal identifiers (`foo`, `data2`).

**Citations (E2 — mandatory):** For **every** code-backed claim (what runs on click, which branch shows, which API fires), include **`path:line`**, or a single fenced citation block whose fence label is `startLine:endLine:filepath` (Cursor-style). If lines are unknown after search, say so once and give the smallest traceable path + symbol to find.

```markdown
## Answer: [question summary]

### Behavior
[Planning-language explanation]

### Related screens/features
- [Screen]: [role]

### Code locations
- `path:line` — [what this code does in planning terms]

### Related capabilities
- [Linked features or screens]

### Notes
- [Extra context or caveats]
```

---

## Examples

### Example 1: Behavior question

User: "What happens when I tap delete on the order list?"

Answer (illustrative):
- 확인 팝업 → 서버에 삭제 요청 → 성공 시 행 제거 + 알림; 실패 시 오류 알림.
- 근거마다 `OrderList.tsx:42`처럼 **파일:줄**로 인용; 주문 API 모듈·관리자만 노출 등은 동일 규칙 적용.

### Example 2: State question

User: "What does the payment screen show on error?"

Answer (illustrative):
- 네트워크 오류·카드 거절·서버 오류 등 분기별 문구·버튼이 다름; `PaymentForm.tsx:줄번호` 형태로 인용.

### Example 3: History question

User: "When was the coupon feature added?"

Answer (illustrative):
- First commit date + follow-up commits with hashes; cite `src/features/coupon/`.

---

## Error Handling

| Issue | Response |
|-------|----------|
| Vague question | Ask clarifying questions (which screen, which control?) |
| No related code | Say feature not found; suggest similar areas |
| Path not specified | Keyword search + candidate list |
| Compound question | Split and answer in order |

## Troubleshooting

- **Answer too technical**: Re-run through the translation table
- **Cannot locate code**: Try filename/symbol search, then semantic search
- **No git history**: State that history cannot be verified from git

## Evolution

Binary eval hooks (skill-autoimprove / audits). Each: **PASS** if true, **FAIL** otherwise.

| Hook | Criterion |
|------|-----------|
| **E1** | Output uses planning terminology (not dev jargon). |
| **E2** | Every code-backed claim has **`path:line`** or a line-range code citation block; not merely a file path. |
| **E3** | Answer follows the Step 4 template (sections present and ordered). |
| **E4** | Boundary respected: no full planning-doc generation (no code-to-spec scope creep). |

## Project-Specific Overrides (AI Stock Analytics)

This skill operates under project-specific policies:
- [project-terminology-glossary.md](../references/project-overrides/project-terminology-glossary.md) (POL-001 — product name, domain terms, forbidden terms)
- [project-tech-stack.md](../references/project-overrides/project-tech-stack.md) (POL-001 — frontend/backend libraries)

Key constraints:
- Translate financial and trading technical terms into planner-friendly Korean using POL-001 glossary mappings; avoid unexplained jargon in answers.
- Describe the frontend stack as **React 19 + TypeScript** (Vite app under `frontend/`) when explaining UI behavior.
- Describe backend behavior as **Python FastAPI** under `backend/app/` when tracing APIs and services.
