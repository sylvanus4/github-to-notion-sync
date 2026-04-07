# Release Checklists / 릴리즈 체크리스트

> **Bilingual support / 이중 언어 지원**: Checklist items are shown in both English and Korean. Fill in notes or comments in whichever language you prefer.

## 1. Tuesday Collection Checklist / 화요일 취합 체크리스트

Run by / 담당: **효정님** (Release Owner)

- [ ] `release:approved` 라벨이 붙은 PR 전체 스캔 (Scan GitHub for all PRs with `release:approved` label)
- [ ] 필수 라벨 확인: `app:*`, `risk:*`, `qa:needed` (Verify each PR has required labels)
- [ ] PR 본문에 5개 필수 섹션 포함 여부 확인 (Verify PR body contains all 5 template sections: Changes, User Impact, QA Method, Rollback, Related Issue)
- [ ] 각 PR에 담당자(assignee) 지정 확인 (Check each PR has an assignee)
- [ ] 미비 항목 플래그 → Slack 쓰레드로 담당자 알림 (Flag incomplete items — notify owners via Slack thread)
- [ ] Notion `Weekly Release - {YYYY-MM-DD}` 페이지 생성/업데이트 (Create/update Notion page)
- [ ] 유효 후보를 Notion에 `Collected` 상태로 추가 (Add all valid candidates to Notion with `Collected` status)
- [ ] `#release-control`에 "후보 목록 v1" 게시 (Post "Candidate List v1" to `#release-control`)
- [ ] 고영향 항목 식별 → 비즈니스팀 사전 공유 (Identify high-impact items for pre-sharing with business team)
- [ ] 수요일 QA 환경 가용 여부 확인 (Confirm QA environment availability for Wednesday)

---

## 2. Wednesday QA Checklist / 수요일 QA 체크리스트

Run by / 담당: **QA Manager**

- [ ] Notion에서 `Ready for QA` 상태 항목 검토 (Review all items with `Ready for QA` status in Notion)
- [ ] PR의 QA 방법에 따라 각 항목 QA 실행 (Execute QA for each item per the QA Method in the PR)
- [ ] Notion에 QA 결과 기록: `Pass`, `Fail`, `Conditional Pass` (Record QA result in Notion)
- [ ] Fail 항목: 재현 단계 기록, 상태를 `Hold`로 변경 (For failed items: add reproduction steps and set status to `Hold`)
- [ ] Pass 항목: 상태를 `QA Passed`로 변경, GitHub에 `qa:done` 라벨 추가 (For passed items: set status to `QA Passed`, add `qa:done` label on GitHub)
- [ ] `#release-control`에 QA 현황 요약 게시 (Post QA status summary to `#release-control`)
- [ ] 의사결정 필요한 블로커 에스컬레이션 (Escalate any blockers that require decision-making)
- [ ] `QA Passed` 항목의 롤백 계획 검토 완료 확인 (Confirm all `QA Passed` items have rollback plans reviewed)

---

## 3. Thursday Deploy Checklist / 목요일 배포 체크리스트

Run by / 담당: **효정님** (Release Owner) + **App Owners / 앱 오너**

### Pre-Deploy / 배포 전

- [ ] Notion의 모든 항목이 `Ready for Release` 상태 (All items in Notion have `Ready for Release` status)
- [ ] 화요일 마감 이후 추가된 항목 없음 — 승인된 핫픽스 제외 (No items added after Tuesday deadline, except approved hotfixes)
- [ ] 각 항목의 앱 오너 참석 확인 (Each item has a confirmed app owner present)
- [ ] 고위험 항목 롤백 계획 검토 완료 (Rollback plans reviewed for all high-risk items)
- [ ] 고영향 변경사항 비즈니스팀 통보 (Business team notified of high-impact changes)
- [ ] 배포 타임라인 QA팀 통보 (QA team notified of deployment timeline)
- [ ] `#release-control`에 배포 예정 공지 게시 (Post pre-deploy announcement to `#release-control`)
- [ ] Notion에서 릴리즈 목록 잠금 (Lock the release list in Notion)

### Deploy / 배포

- [ ] 앱별 배포 실행 (Execute deployment per app)
- [ ] 배포된 각 항목 프로덕션 검증 (Verify each deployed item in production)
- [ ] Notion 상태를 `Released`로 업데이트 (Update Notion status to `Released` for each deployed item)

### Post-Deploy / 배포 후

- [ ] `#release-control`에 배포 완료 게시 (Post deployment completion to `#release-control`)
- [ ] 배포 후 1시간 모니터링 (Monitor for 1 hour post-deploy)
- [ ] 발생 이슈 기록 (Record any issues encountered)
- [ ] 다음 주 개선 포인트 3가지 수집 (Collect 3 improvement points for next week)
- [ ] 쓰레드에 회고 포인트 게시 (Post retro points in thread)

---

## 4. Post-Deploy Retrospective Template / 배포 후 회고 템플릿

```markdown
## Weekly Release Retro / 주간 릴리즈 회고 — {YYYY-MM-DD}

### Stats / 통계
- Total items / 전체 항목: {N}
- Deployed / 배포 완료: {N}
- Held/Deferred / 보류/연기: {N}
- Hotfixes this week / 이번 주 핫픽스: {N}

### What went well / 잘된 점
1. 

### What could improve / 개선할 점
1. 
2. 
3. 

### Action items for next week / 다음 주 액션 아이템
- [ ] 
```
