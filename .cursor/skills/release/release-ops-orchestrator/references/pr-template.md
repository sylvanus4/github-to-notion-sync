# Release PR Template

## Usage

This template is required for all PRs labeled `release:approved` or `hotfix`. Copy the template below into the PR description.

> **Bilingual support**: Each section heading is shown in both English and Korean. Fill in the content in whichever language you prefer — Korean or English. Both are accepted.

---

## Template

```markdown
## Changes / 변경 사항
<!-- What does this PR change? List specific modifications. -->
<!-- 이 PR이 무엇을 변경하나요? 구체적인 수정 내역을 나열해주세요. -->

-

## User Impact / 사용자 영향
<!-- How does this affect end users? Describe visible behavior changes. -->
<!-- 최종 사용자에게 어떤 영향이 있나요? 눈에 보이는 동작 변경을 설명해주세요. -->

-

## QA Method / QA 방법
<!-- How should this be tested? Include specific test steps, environments, and expected results. -->
<!-- 어떻게 테스트해야 하나요? 구체적인 테스트 단계, 환경, 예상 결과를 포함해주세요. -->

1.
2.
3.

**QA Environment / QA 환경**: <!-- e.g., staging, dev, local -->

## Rollback Method / 롤백 방법
<!-- How to revert if something goes wrong? Be specific about steps and data implications. -->
<!-- 문제 발생 시 어떻게 되돌리나요? 구체적인 단계와 데이터 영향을 기술해주세요. -->

1.
2.

**Data impact on rollback / 롤백 시 데이터 영향**: <!-- e.g., "None / 없음", "Requires DB migration rollback / DB 마이그레이션 롤백 필요", "Cache invalidation needed / 캐시 무효화 필요" -->

## Related Issue/Ticket / 관련 이슈
<!-- Link to the GitHub issue, Notion page, or Jira ticket that describes the requirement. -->
<!-- 요구사항이 기술된 GitHub 이슈, Notion 페이지 또는 Jira 티켓 링크를 걸어주세요. -->

- Resolves #
```

---

## Validation Rules

A release PR is considered **complete** when all 5 sections contain substantive content:

| Section | Validation |
|---|---|
| Changes | At least one bullet point describing a specific change |
| User Impact | At least one sentence describing user-visible effect, or explicit "No user-visible impact" |
| QA Method | At least one numbered test step with expected result |
| Rollback Method | At least one numbered rollback step |
| Related Issue/Ticket | At least one linked issue number or URL |

PRs missing any section are flagged during Tuesday collection and excluded from the release unless corrected before Wednesday QA.
