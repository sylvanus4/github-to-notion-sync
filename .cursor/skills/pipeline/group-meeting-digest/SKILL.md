---
name: group-meeting-digest
description: >-
  Analyze company-wide meeting transcripts and compress them into group-specific
  actionable summaries with decision routing to Slack. 3-phase pipeline:
  meeting-digest (extract decisions/actions/announcements) → long-form-compressor
  (compress from a specific group's perspective, default AI Platform Group) →
  decision-router (route decision items to #효정-의사결정 or #ai-리더방).
  Input: Notion URL, local file path, or pasted transcript.
  Output: compressed Korean summary + Slack decision posts.
  Use when the user asks to "group meeting digest", "전사 회의 요약", "그룹 관점 회의 정리",
  "AI 플랫폼 회의 요약", "회의록 그룹 요약", "compress meeting for my team",
  "meeting summary for AI Platform", "그룹 미팅 다이제스트", or wants a team-perspective
  meeting summary with decision routing. Do NOT use for full meeting analysis without
  group filtering (use meeting-digest). Do NOT use for document compression without
  meeting context (use long-form-compressor). Do NOT use for decision routing without
  meeting source (use decision-router inline).
---

# Group Meeting Digest

전사 회의록을 특정 그룹(기본: AI 플랫폼 그룹) 관점으로 압축 요약하고,
의사결정 항목을 Slack 채널로 자동 라우팅하는 3-Phase 파이프라인.

## Output Rules

- **언어**: 모든 출력물(추출, 압축, Slack 메시지, 최종 보고서)은 **반드시 한글**로 작성한다. 원문이 영어여도 한글로 번역하여 출력한다.
- **저장 형식**: 모든 Phase 산출물과 최종 보고서는 `.md` (마크다운) 파일로 저장한다.
- **저장 경로**: `outputs/group-meeting-digest/{date}/` 하위에 Phase별 파일과 최종 보고서를 저장한다.

## Output Rules

- **언어**: 모든 출력물(추출, 압축, Slack 메시지, 최종 보고서)은 **반드시 한글**로 작성한다. 원문이 영어여도 한글로 번역하여 출력한다.
- **저장 형식**: 모든 Phase 산출물과 최종 보고서는 `.md` (마크다운) 파일로 저장한다.
- **저장 경로**: `outputs/group-meeting-digest/{date}/` 하위에 Phase별 파일과 최종 보고서를 저장한다.
- **최종 보고서**: 파이프라인 완료 시 전체 결과를 통합한 `outputs/group-meeting-digest/{date}/group-meeting-digest-{date}.md`를 생성한다.

## Input Modes

| Mode | Example |
|------|---------|
| Notion URL | `https://www.notion.so/...` |
| Local file | `/path/to/transcript.md` |
| Raw text | 사용자가 직접 붙여넣은 회의 텍스트 |

## Parameters

| Param | Default | Description |
|-------|---------|-------------|
| `group` | `AI 플랫폼 그룹` | 관점을 적용할 그룹명 |
| `format` | `executive-summary` | 압축 포맷: `bullet-brief`, `executive-summary`, `one-page`, `custom` |
| `word_limit` | `500` | custom 포맷 시 목표 단어 수 |
| `priority` | `decision-first` | 보존 우선순위: `decision-first`, `data-first`, `balanced` |

## Pipeline

```
Phase 1: Meeting Digest (추출)
    ↓ structured markdown (decisions, actions, announcements)
Phase 2: Group Compression (압축)
    ↓ group-filtered compressed summary
Phase 3: Decision Routing (라우팅)
    → #효정-의사결정 (개인/트레이딩/도구)
    → #ai-리더방 (인프라/전략/파트너십/예산)
```

---

## Phase 1: Meeting Digest (추출)

meeting-digest 방법론을 적용하여 회의 원문에서 구조화된 정보를 추출한다.

### 1-1. Ingest

- **Notion URL**: Notion MCP `get_page` → markdown 변환
- **Local file**: Read tool로 직접 읽기
- **Raw text**: 그대로 사용

### 1-2. Extract

회의 내용에서 아래 4가지를 구조화하여 추출:

```markdown
## 의사결정 사항
- [결정 1]: 배경 + 결정 내용 + 담당자
- [결정 2]: ...

## 액션 아이템
- [ ] 담당: OOO | 기한: YYYY-MM-DD | 내용: ...
- [ ] 담당: OOO | 기한: YYYY-MM-DD | 내용: ...

## 공지 / 공유 사항
- [공지 1]: 전사 영향 요약
- [공지 2]: ...

## 주요 논의 (요약)
- 논의 1: 핵심 포인트 2-3줄
- 논의 2: ...
```

### 1-3. Persist

추출 결과를 `outputs/group-meeting-digest/{date}/phase-1-extract.md`에 저장.

---

## Phase 2: Group Compression (압축)

long-form-compressor 방법론을 적용하여 Phase 1 결과를 그룹 관점으로 압축한다.

### 2-1. Group Filter

Phase 1 결과에서 `{group}` 파라미터에 해당하는 항목을 우선 선별:

**선별 기준** (AI 플랫폼 그룹 기본):
- 직접 언급된 항목 (그룹명, 담당자명, 관련 제품/서비스)
- 인프라/GPU/클라우드/K8s/MLOps 관련 사항
- 전사 공통 정책 중 기술팀 영향 항목
- 예산/인력/조직 변동 중 해당 그룹 영향 항목

**제외 기준**:
- 다른 그룹 전용 사항 (마케팅 캠페인, 영업 목표 등)
- 이미 완료된 과거 사항

### 2-2. Compress

선별된 내용을 `{format}` 포맷으로 압축:

**보존 우선순위** (`{priority}`):
- `decision-first`: 의사결정 → 액션 아이템 → 공지 → 논의
- `data-first`: 수치/일정/데이터 → 의사결정 → 나머지
- `balanced`: 모든 카테고리 균등 압축

**압축 규칙**:
1. 핵심 논점(thesis) 추출
2. 포인트를 임팩트 순으로 정렬
3. 하위 항목부터 제거
4. 중복 제거 및 문장 압축
5. 출처 귀속 보존 (누가 말했는지)
6. 원문 대비 정확성 검증

### 2-3. Output Format

```markdown
# {group} 회의 브리핑 — {date}

## 📋 핵심 요약
[1-3문장 종합 요약]

## 🔴 우리 그룹 의사결정
- [결정]: 내용 (담당: OOO)

## 🟡 액션 아이템
- [ ] 담당: OOO | 기한: MM/DD | 내용

## 📢 전사 공유 (그룹 영향)
- [공지]: 영향 요약

## 💡 참고 논의
- 논의 요약 (필요시만)

---
*원문 대비 압축률: X% | 제외 항목: N건*
```

### 2-4. Persist

압축 결과를 `outputs/group-meeting-digest/{date}/phase-2-compress.md`에 저장.

---

## Phase 3: Decision Routing (라우팅)

decision-router 방법론을 적용하여 Phase 2에서 추출된 의사결정 항목을 Slack으로 라우팅한다.

### 3-1. Decision Detection

Phase 2 결과의 `의사결정` 및 `액션 아이템` 섹션에서 의사결정 항목 탐지:
- "결정", "승인", "확정" 키워드 포함 항목
- 기한이 명시된 액션 아이템
- 예산/인력/정책 변경 사항

### 3-2. Scope Classification

| 분류 | 채널 | 기준 |
|------|------|------|
| **개인** | `#효정-의사결정` | 개인 업무, 도구 선택, 학습 관련 |
| **팀/CTO** | `#ai-리더방` | 인프라 변경, 전략, 파트너십, 예산, 인력 |

### 3-3. Slack Post

Slack MCP `slack_send_message`로 각 채널에 포스팅:

```
🔔 [회의 의사결정] {제목}

📌 결정 사항: {내용}
👤 담당: {담당자}
⏰ 기한: {기한 또는 "미정"}
🏷️ 출처: {회의명}

---
💬 배경: {1-2줄 배경 설명}
```

### 3-4. Summary Post

모든 라우팅 완료 후 `#효정-할일`에 종합 요약 포스팅:

```
📝 그룹 회의 브리핑 완료 — {date}

• 의사결정: {N}건 (개인 {n1} / 팀 {n2})
• 액션 아이템: {M}건
• 라우팅: #효정-의사결정 {n1}건, #ai-리더방 {n2}건

[전문은 outputs/group-meeting-digest/{date}/ 참조]
```

---

## Final Report (최종 보고서)

파이프라인 완료 후 Phase 1~3 결과를 통합한 최종 마크다운 보고서를 생성한다.

### 저장 경로

`outputs/group-meeting-digest/{date}/group-meeting-digest-{date}.md`

### 보고서 구조

```markdown
# {group} 회의 다이제스트 — {date}

> 생성 일시: {timestamp} | 원문 소스: {source_type}

---

## 1. 핵심 요약
[1-3문장 종합 요약]

## 2. 우리 그룹 의사결정
- [결정]: 내용 (담당: OOO)

## 3. 액션 아이템
| 담당 | 기한 | 내용 | 라우팅 채널 |
|------|------|------|-------------|
| OOO | MM/DD | 내용 | #채널명 |

## 4. 전사 공유 (그룹 영향)
- [공지]: 영향 요약

## 5. 참고 논의
- 논의 요약

## 6. 의사결정 라우팅 결과
- #효정-의사결정: {n1}건
- #ai-리더방: {n2}건

---
*원문 대비 압축률: X% | 제외 항목: N건*
*Phase 1 원본: phase-1-extract.md | Phase 2 압축: phase-2-compress.md*
```

### Persist

최종 보고서를 `outputs/group-meeting-digest/{date}/group-meeting-digest-{date}.md`에 저장한다.
Phase별 중간 산출물도 동일 디렉토리에 `.md` 형식으로 보존한다:
- `phase-1-extract.md` — 구조화 추출 결과
- `phase-2-compress.md` — 그룹 관점 압축 결과

---

## Execution Checklist

```
Task Progress:
- [ ] Phase 1: 회의 원문 수집 및 구조화 추출 → phase-1-extract.md 저장
- [ ] Phase 2: 그룹 관점 필터링 및 압축 → phase-2-compress.md 저장
- [ ] Phase 3: 의사결정 Slack 라우팅
- [ ] 최종 보고서 생성 → group-meeting-digest-{date}.md 저장
- [ ] 종합 요약 Slack 포스팅
```

## Error Handling

- Notion 접근 실패 → 로컬 파일 또는 텍스트 입력으로 폴백
- Slack 채널 미발견 → `slack_search_channels` → `slack_search_public_and_private` 순서로 탐색
- 의사결정 항목 0건 → Phase 3 스킵, Phase 2 결과만 `#효정-할일`에 포스팅
- 그룹 관련 항목 0건 → "해당 그룹 관련 사항 없음" 메시지와 전사 공통 사항만 요약
