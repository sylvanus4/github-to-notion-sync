---
name: today-agent-work
description: >-
  Remote agent용 today 스킬 변형. 주식 데이터 동기화, 스크리닝, 기술적 분석, 한국어 리포트
  파이프라인을 원격 세션에서 실행. Google 시스템 MCP connector(Calendar/Drive/Gmail)와
  Slack Incoming Webhook(curl)으로 #agent-work 채널에 결과 전송.
  schedule routine에서만 사용. 로컬 실행은 today 스킬 사용.
---

# today-agent-work

`today` 스킬의 스케줄러/원격 세션 전용 변형. 콜드 세션에서도 self-contained 하게 동작.

## Architecture

```
Remote Agent (Anthropic Cloud)
  ├── Google MCP (시스템)   → Calendar, Drive, Gmail API
  ├── Slack Webhook (curl) → #agent-work 채널 알림
  ├── Data APIs (WebFetch) → 주가 데이터 수집
  └── Git Repo             → 리포트 저장 + commit
```

## Do NOT Use Locally

이 스킬은 `/schedule` routine 전용. 로컬에서는:
- 주식 분석 -> `today`
- 데이터 동기화 -> `daily-db-sync`
- 기술적 분석 -> `trading-technical-analyst`

---

## 원격 환경 제약

- Slack MCP 커넥터는 원격 루틴에서 사용 불가 (directory 커넥터 미지원)
- Google MCP 커넥터 (Calendar, Drive, Gmail) 는 시스템 커넥터로 정상 동작
- Slack -> curl Incoming Webhook 사용
- Python 스크립트/DB 접근 불가 -> WebFetch로 공개 API 직접 호출

## 핵심 차이 (vs `today`)

| 항목 | `today` (로컬) | `today-agent-work` (원격) |
|------|----------------|---------------------------|
| 호출 컨텍스트 | 사용자 인터랙티브 | 스케줄러 / 원격 에이전트 (콜드 세션) |
| Slack 도구 | `kwp-slack-slack-messaging` / 프로젝트 기본 | curl Incoming Webhook |
| Slack 채널 | `#h-report` | `#agent-work` |
| Google 연동 | 로컬 MCP | `mcp__Google-Calendar__*`, `mcp__Google-Drive__*`, `mcp__Gmail__*` (시스템 커넥터) |
| 데이터 소스 | Python + DB/CSV | WebFetch (공개 API) |

## Google MCP 도구

| 서비스 | 도구 |
|--------|------|
| Calendar | `mcp__Google-Calendar__list_events`, `mcp__Google-Calendar__get_event` |
| Gmail | `mcp__Gmail__search_threads`, `mcp__Gmail__get_thread`, `mcp__Gmail__create_draft` |
| Drive | `mcp__Google-Drive__create_file`, `mcp__Google-Drive__search_files` |

## Slack Webhook

```bash
curl -s -X POST -H 'Content-type: application/json' \
  --data '{"text":"MESSAGE"}' \
  '$SLACK_WEBHOOK_URL'
```
- #agent-work 채널로 자동 라우팅
- Thread reply 미지원 -- 모든 내용을 단일 메시지에 포함
- mrkdwn 포맷, JSON 내 큰따옴표 이스케이프 필수

## Pipeline Phases (스케줄러용)

1. **Preflight**
   - 작업 일자 = 호출 시점 KST 기준 영업일. 주말이면 `total_stocks=0` 처리 후 단계 4-9 스킵, 단계 10만 실행.
   - `outputs/today/{date}/` 디렉터리 생성, `manifest.json` 초기화.
2. **Data Sync**: WebFetch로 공개 주가 API 호출하여 데이터 수집. Yahoo Finance, 기타 공개 API 활용.
3. **Hot Stock Discovery**: NASDAQ / KOSPI / KOSDAQ 핫 종목 추출.
4. **Multi-Factor Screening**: P/E, RSI, volume, MA crossovers, FCF yield.
5. **Technical Analysis**: 추적 종목 전체에 대해 SMA 20/55/200, RSI, MACD, Stochastic, ADX.
6. **News & Sentiment** (옵션): WebSearch로 뉴스 수집 후 감성 분석.
7. **Report Generation**: 한국어 매수/매도 리포트 (markdown) 생성.
8. **Strategy Engine**: 7-strategy 백테스트 카드, 상위 10개 산출.
9. **Google Drive Archive** (시스템 MCP 커넥터):
   - `mcp__Google-Drive__create_file` 로 리포트와 `manifest.json` 업로드
   - 업로드 위치: 사용자 Drive 의 `Trading/today/{YYYY-MM-DD}/` 경로 (없으면 생성)
   - 반환된 `file_id` 와 `web_view_link` 를 manifest 에 기록
10. **Slack Distribution** (curl Incoming Webhook + `#agent-work`):
    - curl로 root 메시지 전송 (위 Slack Webhook 섹션 참조)
    - 단일 메시지에 BUY / NEUTRAL / SELL 그룹 모두 포함
    - 포함: 분석 일자, 시그널 카운트, Drive 링크, 주말/휴장 시 안내 배너
11. **Calendar Hook** (옵션):
    - `mcp__Google-Calendar__list_events` 로 당일 KST 09:00-18:00 이벤트 조회
    - 시장 관련 키워드 (실적/배당/CPI/FOMC) 매칭 시 Slack 메시지에 "오늘 일정" 섹션 추가
12. **Email Digest** (옵션):
    - 사용자가 `--email` 옵션을 명시했거나, manifest 에 `email_digest=true` 일 때만
    - `mcp__Gmail__create_draft` 로 본인 메일에 한국어 요약 초안 생성 (자동 발송 X)
13. **KB Ingest**: 산출물을 `trading-daily` 지식베이스로 라우팅.

## 단계간 게이트

- 1, 2 단계 실패 -> 3-9 스킵, 10 단계에서 `[데이터 미동기화]` 배너로만 보고
- 7 단계 (리포트 생성) 실패 -> 9 단계 Drive 업로드 스킵, 10 단계 텍스트만 전송
- 10 단계 실패 -> 1회 재시도 후 halt; manifest 에 `slack_error` 기록

## Slack 메시지 템플릿 (root, mrkdwn)

```
:sunrise: *Today Agent-Work -- {date} (KST)*
분석 종목 {total_stocks}개 | :large_green_circle: BUY {buy} | :white_circle: NEUTRAL {neutral} | :red_circle: SELL {sell}
_데이터 소스: {data_source}_
{drive_link_line}

_Turtle: SMA(20,55,200) + Donchian | Bollinger: BB(20,2σ) + %B + Squeeze_
_본 메시지는 자동화된 분석이며 투자 자문이 아닙니다._
```

`{drive_link_line}` 은 9 단계 성공 시 `:open_file_folder: <web_view_link|Drive 리포트>`, 실패 시 빈 문자열.

## Output

- `outputs/today/{date}/manifest.json` (Drive `file_id`, 단계별 status 포함)
- 한국어 리포트 (로컬 markdown + Drive)
- `#agent-work` Slack 메시지 (BUY/SELL/NEUTRAL 분류)
- (옵션) Gmail 초안

## Options (스케줄러 프롬프트에서 인자로 전달)

- `--skip-tradingview`: TradingView 단계 스킵 (스케줄러 기본값 권장)
- `--email`: Gmail 초안 활성화

## 휴장 / 주말 처리

- 주말 또는 KST 기준 미국/한국 동시 휴장일: 단계 2-9 스킵
- Slack 메시지에 `:beach_with_umbrella: 시장 휴장` 배너 추가 후 마지막 영업일 manifest 링크만 첨부

## Error Handling

| Phase | Error | Recovery |
|-------|-------|----------|
| 2 | 데이터 API 호출 실패 | 가용한 대체 API 시도, 전부 실패 시 단계 3-9 스킵 |
| 7 | 리포트 생성 실패 | Drive 업로드 스킵, Slack에 텍스트만 전송 |
| 9 | Google Drive MCP 실패 | 스킵, 리포트는 git에만 저장 |
| 10 | Slack webhook 실패 | 1회 재시도 후 halt, manifest에 에러 기록 |
| 11 | Google Calendar MCP 실패 | 일정 섹션 스킵 |

## Safety Rules

- git push 실패 시 force push 금지
- 자동 매매 실행 금지 -- 분석과 리포트만
- 이메일 자동 발송 금지 -- draft만 생성

## 트리거 예시

- 스케줄러 cron `0 7 * * 1-5` (KST) -> 본 스킬 실행 프롬프트 발사
- 사용자: "today agent-work 실행해줘" -> 동일 파이프라인 인터랙티브 실행
- 사용자: "오늘 자동 today 결과 다시 보내줘" -> manifest 재로드 후 Slack 재전송
