# UX Text Templates

Reusable Korean UX text patterns by state type.

## Error States

### Pattern: Actionable Error

```
[무엇이 안 되었는지] + [왜 안 되었는지 (선택)] + [어떻게 해결하는지]
```

Examples:
- "결제가 처리되지 않았어요. 카드 정보를 확인하고 다시 시도해 주세요."
- "파일을 업로드할 수 없어요. 10MB 이하 파일만 지원됩니다."

### Pattern: System Error (cause unknown)

```
[문제 인정] + [재시도 안내] + [지속 시 대안]
```

Examples:
- "일시적인 오류가 발생했어요. 잠시 후 다시 시도해 주세요. 문제가 계속되면 고객센터(1234-5678)로 문의해 주세요."

## Empty States

### Pattern: First-time Empty

```
[환영/안내] + [첫 행동 유도]
```

Examples:
- "아직 등록된 프로젝트가 없어요. 새 프로젝트를 만들어 시작해 보세요."

### Pattern: Filtered Empty

```
[검색/필터 결과 없음 설명] + [조건 변경 안내]
```

Examples:
- "검색 결과가 없어요. 다른 키워드로 검색하거나 필터를 변경해 보세요."

## Success States

### Pattern: Action Confirmation

```
[완료된 작업] + [다음 단계 (선택)]
```

Examples:
- "저장이 완료되었어요."
- "회원가입이 완료되었어요. 이메일 인증을 진행해 주세요."

## Permission/Restriction States

### Pattern: Access Denied

```
[접근 불가 안내] + [권한 획득 방법]
```

Examples:
- "이 페이지에 접근 권한이 없어요. 관리자에게 요청해 주세요."

## Tone Guidelines

| Tone | 특징 | 예시 어미 |
|------|------|----------|
| Formal | 존댓말, 간결 | ~합니다, ~하세요 |
| Friendly | 존댓말, 부드러움 | ~해요, ~해 보세요 |
| Neutral | 존댓말, 중립 | ~됩니다, ~해 주세요 |
