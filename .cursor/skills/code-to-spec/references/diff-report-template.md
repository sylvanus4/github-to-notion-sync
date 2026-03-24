# Diff report template (implementation vs planned spec)

Use for **code-spec-comparator** outputs. **Write the final report in Korean**; keep technical identifiers in English.

## Report structure

```markdown
# Gap Analysis Report — {Feature/Module}

**생성일:** YYYY-MM-DD  
**코드 소스:** {repo path or PR URL}  
**기획 소스:** {Notion page title + URL}  
**분석 범위:** {scope description}  

---

## 요약

| 카테고리 | 건수 | Critical | High | Medium | Low |
|----------|-----|----------|------|--------|-----|
| 기획에만 존재 | N | … | … | … | … |
| 코드에만 존재 | N | … | … | … | … |
| 스키마 불일치 | N | … | … | … | … |
| 상태 전이 불일치 | N | … | … | … | … |
| **합계** | **N** | … | … | … | … |

---

## 상세

### 1. 기획에 있으나 코드에 없는 항목

| # | 항목 | 기획서 위치 | 심각도 | 비고 |
|---|------|-----------|--------|------|
| 1 | {API/기능명} | {Section ref} | {severity} | {추가 설명} |

### 2. 코드에 있으나 기획에 없는 항목

| # | 항목 | 코드 위치 | 심각도 | 비고 |
|---|------|----------|--------|------|
| 1 | {API/기능명} | {file:line} | {severity} | {추가 설명} |

### 3. 스키마 불일치

| # | 필드/파라미터 | 기획서 정의 | 실제 코드 | 심각도 |
|---|-------------|-----------|----------|--------|
| 1 | {field name} | {planned type/enum} | {actual type/enum} | {severity} |

### 4. 상태 전이 불일치

| # | 전이 | 기획서 | 실제 코드 | 심각도 |
|---|------|--------|----------|--------|
| 1 | {transition name} | {planned flow} | {actual flow} | {severity} |

---

## 권장 조치

| 우선순위 | 항목 | 조치 내용 | 담당 |
|----------|------|----------|------|
| 1 | {item} | {action} | 기획/개발 |
```

## Severity criteria

| Severity | Definition |
|----------|------------|
| CRITICAL | 핵심 기능 누락 또는 상태 머신 깨짐 — 즉시 수정 필요 |
| HIGH | 클라이언트 통합에 영향을 주는 스키마 차이 |
| MEDIUM | 문서화되지 않은 API 또는 추가 필드 |
| LOW | 네이밍 불일치, 사소한 차이 |
