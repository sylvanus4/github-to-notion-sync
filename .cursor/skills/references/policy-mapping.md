# Policy-to-Text Mapping Rules

Rules for connecting product policies to UX text generation.

## Policy Priority

When multiple policies apply to the same state:

| Priority | Category | Examples |
|----------|----------|---------|
| 1 (highest) | Legal/Compliance | 개인정보보호법, 전자상거래법 |
| 2 | Safety/Security | 본인인증, 결제 보안 |
| 3 | Business rules | 이용 제한, 환불 정책 |
| 4 (lowest) | UX conventions | 일반 안내, 톤 가이드 |

## Conflict Resolution

When two policies produce contradictory text requirements:

1. Higher priority policy wins
2. If same priority, flag for human review
3. Never silently drop a policy requirement

## Mandatory Text Elements by Policy Type

| Policy Type | Required in Text |
|-------------|-----------------|
| 개인정보 수집 | 수집 항목, 목적, 보유 기간 |
| 결제/환불 | 취소/환불 조건, 고객센터 연락처 |
| 연령 제한 | 연령 확인 안내, 미성년자 접근 제한 사유 |
| 약관 동의 | 필수/선택 구분, 전문 보기 링크 |
| 마케팅 동의 | 수신 동의 해지 방법 |

## Citation Format

Every policy-derived text must include a citation:

```
[정책: POL-XXX] — [정책 제목 요약]
```

For multiple policies in one text:

```
[정책: POL-001, POL-003] — [각각의 정책 제목]
```
