---
name: scheduled-hf-trending
description: >-
  Remote agent용 HuggingFace 트렌딩 인텔리전스 자동화. HF REST API(WebFetch)로
  논문/모델/스페이스 트렌드 수집, Slack Incoming Webhook(curl)으로 #agent-work 채널에
  리포트 전송, Google Drive MCP connector로 리포트 아카이빙.
  schedule routine에서만 사용. 로컬 실행은 hf-trending-intelligence 스킬 사용.
---

# Scheduled HF Trending Intelligence

Remote agent 환경에서 동작하는 HuggingFace 트렌딩 인텔리전스 파이프라인.

## Architecture

```
Remote Agent (Anthropic Cloud)
  ├── HF REST API (WebFetch) → daily_papers, models, datasets, spaces
  ├── Slack Webhook (curl)   → #agent-work 채널 리포트 전송
  ├── Google Drive MCP       → 리포트 아카이빙 (Google Docs)
  └── Git Repo               → 리포트 저장 + commit
```

## Do NOT Use Locally

이 스킬은 `/schedule` routine 전용. 로컬에서는:
- HF 트렌딩 분석 -> `hf-trending-intelligence`
- HF 논문 브라우징 -> `hf-papers`
- 토픽 중심 스캔 -> `hf-topic-radar`

---

## 원격 환경 제약

- Slack MCP, HuggingFace MCP 커넥터는 원격 루틴에서 사용 불가 (directory 커넥터 미지원)
- Google MCP 커넥터 (Calendar, Drive, Gmail) 만 시스템 커넥터로 동작
- Slack -> curl Incoming Webhook 사용
- HuggingFace -> WebFetch로 REST API 직접 호출

## 출력 언어

**모든 출력물은 한국어로 작성한다.** 논문 제목, 모델명, 데이터셋명 등 고유명사는 원어 그대로 유지.

## Tool Mapping (로컬 vs 원격)

| 기존 (로컬) | 원격 루틴 |
|---|---|
| `hf papers ls` CLI / `mcp__hf__paper_search` | `WebFetch https://huggingface.co/api/daily_papers` |
| `hf models ls` CLI / `mcp__hf__hub_repo_search` | `WebFetch https://huggingface.co/api/models?search=QUERY&sort=downloads&limit=10` |
| `hf datasets ls` CLI | `WebFetch https://huggingface.co/api/datasets?search=QUERY&sort=downloads&limit=10` |
| `hf spaces ls` CLI / `mcp__hf__space_search` | `WebFetch https://huggingface.co/api/spaces?search=QUERY&sort=likes&limit=10` |
| `kwp-slack-slack-messaging` / `mcp__slack__slack_send_message` | `curl -s -X POST -H 'Content-type: application/json' --data '{"text":"MSG"}' WEBHOOK_URL` |
| `md-to-notion` | `mcp__Google-Drive__create_file` (시스템 MCP 커넥터) |
| `parallel-web-search` | `WebSearch` tool |

## Slack Webhook

```bash
curl -s -X POST -H 'Content-type: application/json' \
  --data '{"text":"MESSAGE"}' \
  '$SLACK_WEBHOOK_URL'
```
- #agent-work 채널로 자동 라우팅
- Thread reply 미지원 -- 모든 내용을 단일 메시지에 포함
- mrkdwn 포맷, JSON 내 큰따옴표 이스케이프 필수

## Pipeline (Sequential)

### Phase 1: Paper Scan

HF REST API로 오늘의 트렌딩 논문 수집.

1. `WebFetch https://huggingface.co/api/daily_papers` 호출
2. 논문별 ID, 제목, upvote, 저자 추출
3. 키워드 리스트 생성 (크로스-레퍼런스용)

**Output:** 30개 논문 목록 (IDs, titles, keywords, upvotes)

### Phase 2: Cross-Reference

상위 10개 논문에 대해 생태계 영향도 측정.

1. **모델 연관:** `WebFetch https://huggingface.co/api/models?search=KEYWORD&sort=downloads&limit=10`
2. **데이터셋 연관:** `WebFetch https://huggingface.co/api/datasets?search=KEYWORD&sort=downloads&limit=10`
3. **스페이스 연관:** `WebFetch https://huggingface.co/api/spaces?search=KEYWORD&sort=likes&limit=10`

**Output per paper:** `{model_count, dataset_count, space_count}`

### Phase 3: Web Enrichment

상위 5개 논문의 외부 반응 수집.

`WebSearch` tool로 논문별 검색:
- `"PAPER_TITLE" AI research 2026`
- `"PAPER_TITLE" github implementation`

**Output per paper:** `{web_mentions, github_repos}`

### Phase 4: Trend Scoring

복합 점수 계산:

```
trend_score = (
  0.30 * normalize(paper_upvotes) +
  0.25 * normalize(model_count) +
  0.20 * normalize(dataset_count) +
  0.15 * normalize(space_count) +
  0.10 * normalize(web_mentions)
)
```

분류:
- Score >= 0.7: **HOT** -- 2주 내 메인스트림 예상
- Score 0.4-0.7: **WARM** -- 부상 중, 모니터링 필요
- Score < 0.4: **COOL** -- 초기 단계

### Phase 5: Intelligence Report

한국어 마크다운 리포트 생성:

```markdown
# AI 리서치 레이더 -- YYYY-MM-DD

## 요약
(오늘의 트렌드 2-3문장 요약)

## 트렌딩 TOP 5

### 1. [PAPER_TITLE] -- HOT
- **점수:** 0.85
- **논문:** PAPER_ID (upvotes N)
- **모델:** N개
- **데이터셋:** N개
- **스페이스:** N개 데모
- **핵심 인사이트:** (중요성 1문장)

## 모델 지형 변화
(부상/하락 모델)

## 실행 제언
(ThakiCloud 팀 관점 권장 사항)
```

리포트 파일: `outputs/hf-trending/YYYY-MM-DD-radar.md`

### Phase 6: Slack Notification

curl Incoming Webhook으로 `#agent-work` 채널에 리포트 전송.

**방법:** Bash에서 curl 실행 (위 Slack Webhook 섹션 참조)

메시지 포맷 (mrkdwn, 단일 메시지):
```
:microscope: *HF 트렌딩 인텔리전스* | YYYY-MM-DD

:page_facing_up: *수집 논문:* N편 | *분석:* Top 10 크로스-레퍼런스

*Executive Summary*
{2-3문장 트렌드 요약}

:fire: *HOT*
1. {논문 제목} (score: 0.XX, upvotes: N) -- {1문장 인사이트}
2. ...

:thermometer: *WARM*
1. {논문 제목} (score: 0.XX) -- {1문장 인사이트}
2. ...

:memo: *ThakiCloud 실행 제언*
1. {구체적 액션}
2. {구체적 액션}

*HOT 논문 상세*
(각 HOT 논문의 관련 모델/데이터셋/스페이스 수, 웹 반응 1줄 요약)
```

### Phase 7: Google Drive Archive

Google Drive 시스템 MCP connector로 리포트를 Google Docs로 아카이빙.

**Tool:** `mcp__Google-Drive__create_file`
- 파일명: `HF-Trending-YYYY-MM-DD`
- 형식: Google Docs
- 내용: Phase 5에서 생성한 마크다운 리포트

### Phase 8: Git Commit

리포트 파일을 git에 저장:
- `outputs/hf-trending/YYYY-MM-DD-radar.md` 저장
- `chore: HF trending intelligence YYYY-MM-DD` 커밋
- main에 push

---

## Error Handling

| Phase | Error | Recovery |
|-------|-------|----------|
| 1 | HF API 호출 실패 | WebSearch fallback으로 논문 검색, 실패 시 Slack에 에러 전송 후 종료 |
| 1 | 오늘 논문 없음 | 어제 날짜로 fallback, "오늘 논문 없음" 표기 |
| 2 | Cross-reference 검색 실패 | 가용 데이터로 계속, 누락 차원 표기 |
| 3 | WebSearch 실패 | 웹 enrichment 스킵, 4차원으로 스코어링 |
| 6 | Slack webhook 실패 | 리포트 파일만 저장 후 commit |
| 7 | Google Drive 실패 | 스킵, 리포트는 git에만 저장 |

## Safety Rules

- HF API rate limit 준수 (요청 간 적절한 간격)
- 논문 본문을 Slack에 전체 복사하지 않음 (요약만)
- git push 실패 시 force push 금지
