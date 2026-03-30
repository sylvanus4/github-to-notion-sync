# Policy Text Output Template

## 생성 결과 출력 형식

```markdown
# 정책 기반 문구 생성 결과

**생성일**: {date}
**정책 소스**: {policy_source}
**문구 유형**: {text_type}
**대상 화면/상황**: {context}

---

## 생성 문구

### 후보 1 (권장)
> {generated_text_1}

- **근거 정책**: {policy_clause_ref}
- **톤**: {tone}
- **글자수**: {char_count}

### 후보 2
> {generated_text_2}

- **근거 정책**: {policy_clause_ref}
- **톤**: {tone}
- **글자수**: {char_count}

### 후보 3
> {generated_text_3}

- **근거 정책**: {policy_clause_ref}
- **톤**: {tone}
- **글자수**: {char_count}

---

## 일관성 검증 결과

| 검증 항목 | 결과 | 비고 |
|-----------|------|------|
| 용어 통일성 | PASS/FAIL | {note} |
| 톤 일관성 | PASS/FAIL | {note} |
| 정책 정합성 | PASS/FAIL | {note} |
| 접근성 | PASS/FAIL | {note} |

## 불일치 항목 (있을 경우)

| 기존 문구 | 문제점 | 개선안 |
|-----------|--------|--------|
| {existing} | {issue} | {suggestion} |

---

## 적용 정책 조항 요약

| 조항 번호 | 핵심 내용 | 반영 위치 |
|-----------|----------|----------|
| {clause_id} | {summary} | 후보 {n} |
```
