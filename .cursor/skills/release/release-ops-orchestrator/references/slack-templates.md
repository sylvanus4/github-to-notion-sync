# Slack Message Templates

> **Bilingual support / 이중 언어 지원**: Template headings and fixed labels are shown in Korean as the primary language. Variable content (`{title}`, `{failure_reason}`, etc.) can be filled in Korean or English — whichever the author prefers.

## Channel Routing / 채널 라우팅

| Channel | Purpose / 용도 | Content / 내용 |
|---|---|---|
| `#release-control` | Regular release operations / 정규 릴리즈 운영 | Collection, QA status, deploy confirmation, blockers |
| `#hotfix-alert` | Hotfix-only communications / 핫픽스 전용 | Urgent candidates, business impact, deploy status |

---

## 1. Tuesday Collection Summary / 화요일 취합 요약 (`#release-control`)

### Main Message

```
:package: *Weekly Release Candidate List — 주간 릴리즈 후보 목록 — {YYYY-MM-DD}*

총 *{total_count}건* 수집 (Total collected) | :white_check_mark: 완료(Ready) {ready_count} | :warning: 보완 필요(Incomplete) {incomplete_count} | :x: 제외(Excluded) {excluded_count}

*수집 마감: 화요일 오전 완료 (Collection closed: Tuesday AM)*
```

### Thread — Per-App Breakdown

```
:label: *{app_name}* — {item_count}건 (items)

{for each item}
• `{pr_number}` {title} — @{assignee}
  상태(Status): {status} | 리스크(Risk): {risk} | QA: {qa_status}
  {missing_items_if_any}
{end}
```

### Thread — Missing Items Alert

```
:rotating_light: *보완 필요 항목 (Items requiring completion)*

{for each incomplete item}
• `{pr_number}` {title}
  누락(Missing): {missing_fields — e.g., "롤백 계획(Rollback plan)", "QA 방법(QA method)", "앱 라벨(App label)"}
{end}

> 목요일 배포에 포함되려면 수요일 QA 전까지 보완 필요합니다.
> Items must be completed before Wednesday QA to be included in Thursday's deployment.
```

---

## 2. Wednesday QA Status Update / 수요일 QA 현황 (`#release-control`)

### Main Message

```
:test_tube: *QA 현황 (QA Status) — {YYYY-MM-DD} 릴리즈*

:white_check_mark: Pass: {pass_count}건 | :x: Fail: {fail_count}건 | :hourglass_flowing_sand: 진행중(In progress): {in_progress_count}건

{if fail_count > 0}
> :warning: Fail 항목은 Hold 처리되었습니다. 수정 후 재QA가 필요합니다.
> Failed items have been put on Hold. Fixes and re-QA are required.
{end}
```

### Thread — QA Results Detail

```
:clipboard: *QA 상세 결과 (QA Results Detail)*

:white_check_mark: *Pass / 통과*
{for each passed item}
• `{pr_number}` {title} — @{assignee} → Ready for Release (배포 준비 완료)
{end}

:x: *Fail → Hold / 실패 → 보류*
{for each failed item}
• `{pr_number}` {title} — @{assignee}
  사유(Reason): {failure_reason}
{end}

:hourglass_flowing_sand: *진행중 (In Progress)*
{for each in_progress item}
• `{pr_number}` {title} — @{assignee}
  예상 완료(ETA): {expected_completion}
{end}
```

---

## 3. Thursday Pre-Deploy Announcement / 목요일 배포 예정 공지 (`#release-control`)

### Main Message

```
:rocket: *배포 예정 공지 (Pre-Deploy Announcement) — {YYYY-MM-DD}*

배포 항목(Items): *{deploy_count}건* | 배포 시간(Deploy time): *{deploy_time}*

:lock: 릴리즈 목록이 확정되었습니다. 핫픽스 외 추가 불가.
Release list is locked. No additions except hotfixes.
```

### Thread — Deploy Items

```
:page_facing_up: *배포 목록 (Deploy List)*

{for each app}
*{app_name}* ({item_count}건/items)
{for each item}
• `{pr_number}` {title} — @{assignee} | 리스크(Risk): {risk}
{end}
{end}

*롤백 담당(Rollback owner)*: @{rollback_owner}
```

---

## 4. Thursday Post-Deploy Confirmation / 목요일 배포 완료 확인 (`#release-control`)

### Main Message

```
:white_check_mark: *배포 완료 (Deploy Complete) — {YYYY-MM-DD}*

총 *{deployed_count}건* 배포 완료 (deployed) | 모니터링 중 (monitoring)

{if issues_found}
:warning: 이슈 발견(Issues found): {issue_count}건 — 아래 쓰레드 확인 (see thread)
{else}
:green_circle: 현재까지 이슈 없음 (No issues so far)
{end}
```

### Thread — Retro Points

```
:memo: *이번 주 개선 포인트 3가지 (Top 3 Improvements This Week)*

1. {improvement_1}
2. {improvement_2}
3. {improvement_3}

> 다음 주 화요일까지 반영 예정
> To be applied by next Tuesday.
```

---

## 5. Hotfix Alert / 핫픽스 알림 (`#hotfix-alert`)

### Main Message

```
:rotating_light: *핫픽스 요청 (Hotfix Request) — {app_name}*

*긴급도(Urgency)*: {urgency}
*고객/비즈니스 영향(Business Impact)*: {impact_summary}
*요청 배경(Background)*: {background}
*PR*: {pr_url}
*담당자(Assignee)*: @{assignee}

상태(Status): {status}
```

### Thread — Status Updates

```
:arrow_right: *상태 업데이트 (Status Update)*

• 비즈니스팀 공유(Biz team notified): {yes/no}
• QA 완료(QA done): {yes/no}
• 배포(Deploy): {status}
{if deployed}
• 배포 시간(Deploy time): {deploy_time}
{end}
```

---

## 6. Blocker Escalation / 블로커 에스컬레이션 (`#release-control`)

### Main Message

```
:no_entry: *블로커 발생 — 에스컬레이션 필요 (Blocker — Escalation Required)*

*항목(Item)*: `{pr_number}` {title}
*앱(App)*: {app_name}
*블로커 유형(Blocker type)*: {blocker_type — e.g., "QA 환경 불가(QA env unavailable)", "의존성 미해결(Unresolved dependency)", "승인 대기(Pending approval)"}
*영향(Impact)*: {impact_description}

> @{decision_maker} 의사결정이 필요합니다. (Decision required.)
```
