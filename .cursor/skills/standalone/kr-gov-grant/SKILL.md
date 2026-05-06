---
name: kr-gov-grant
description: |
  Korean government grant/subsidy program search, application writing, review, and schedule management.
  Covers all applicant types: startups, SMEs, researchers, nonprofits, individuals.
  4 modes: program discovery, application drafting, review/feedback, timeline/checklist.
  Use when the user asks to "정부 지원사업 찾아줘", "사업계획서 써줘", "신청서 검토해줘",
  "마감일 체크리스트", "government grant", "subsidy search", "grant application",
  "kr-gov-grant", "지원금", "공모전 신청", "정부 과제", "예비창업패키지", "초기창업패키지",
  "TIPS 신청", "소상공인 지원", "전통시장 활성화", "수출바우처", "스마트공장",
  "사회적기업", "관광벤처", "농식품 창업", "R&D 과제", "연구비 신청",
  or mentions any Korean government support program.
  Do NOT use for legal document filing (use legal skills).
  Do NOT use for stock/fund investment recommendations (use trading skills).
  Do NOT use for academic R&D-only grant writing (use grant-writer reference or paper-review).
  Do NOT use for actual submission or proxy filing (information and drafting only).
user-invocable: true
version: 1.0.0
---

# Korean Government Grant Analysis & Application Skill

Unified assistant for Korean government grants and subsidies. Matches applicant profile to optimal programs, drafts high-scoring applications, reviews documents against evaluation criteria, and manages submission timelines.

> For academic/R&D-focused grants (NRF, IITP, KIAT), see `references/grant-writer-guide.md` for specialized templates.

---

## Applicant Profiling

On any request, identify two facts from conversation context (don't ask if already known):

**1. Applicant Type** (pick one)
- 예비창업자 (pre-startup, no business registration)
- 초기창업자 (early startup, within 3 years)
- 성장기 스타트업 (growth stage, 3-7 years)
- 소상공인/자영업자 (small business owner)
- 중소/중견기업 (SME / mid-cap)
- 연구자/연구기관 (researcher / institute)
- 비영리단체/협동조합/사회적기업 (nonprofit / social enterprise)
- 개인 (freelancer, youth, farmer, etc.)

**2. Support Purpose** (one or more)
- 창업 자금 / 사업화 / R&D 기술개발
- 시설/장비 / 운영자금
- 마케팅/수출 / 해외진출
- 인력 채용/교육 / 컨설팅
- 공간/플랫폼 / 콘텐츠 제작

---

## MODE 1 -- Program Discovery

**Triggers:** "맞는 지원사업 찾아줘", "어떤 거 받을 수 있어", "지원금 뭐 있어"

### Procedure

1. Profile applicant (above)
2. Select 3-5 candidates from `references/programs.md`
3. Web-search for current announcements: `"[사업명] 2026 공고"`, `site:k-startup.go.kr`, `site:bizinfo.go.kr`
4. Output using template below

### Output Template

```
## [신청자 상황] 맞춤 지원사업 추천

### 1순위: [사업명]
- 주관기관:
- 지원 규모:
- 지원 대상:
- 신청 가능 여부: 가능 / 조건 확인 필요 / 해당 없음
- 추천 이유: (매칭 근거 2-3줄)
- 핵심 평가 지표:
- 경쟁 난이도: 낮음 / 보통 / 높음
- 공고 시기: (공식 사이트 확인 필수)
- 공식 정보: [URL]

[2순위, 3순위 동일 형식]

---
### 현재 조건으로 신청 불가한 사업 및 이유
### 다음 단계
1. 공고문 원문 확인: K-Startup 또는 각 기관 사이트
2. 신청서 작성 필요 시: "○○ 신청서 써줘"
```

---

## MODE 2 -- Application Drafting

**Triggers:** "신청서 써줘", "사업계획서 초안 만들어줘", "지원서 작성 도와줘"

### Required Info (mark `[추후 기입]` if missing)

1. 어떤 사업에 신청하는가?
2. 사업 아이템 한 줄 소개 (무엇을 / 누구에게 / 어떻게)
3. 핵심 차별점 (왜 우리만 할 수 있는가)
4. 신청자/팀 역량 (대표 경력, 핵심 팀원)
5. 보유 성과 (매출, 특허, 수상, 투자, 고객 등)

### Writing Principles

- **수치로 말하기**: "큰 시장" -> "국내 시장 규모 2조원, 연 15% 성장"
- **차별성 선공**: 첫 문단에 경쟁 우위 명확히
- **평가 항목 균형**: 사업성/기술성/팀역량/실현가능성 골고루 커버
- **약점 선제 대응**: 특허/매출 없음 등 약점은 보완 전략 먼저 제시
- **사업별 언어**: 창업="혁신/시장 검증", R&D="TRL 단계/정량 목표", 전통시장="지역 상생/활성화"

### Section Output Format

```
## [항목 번호]. [항목명]

### 작성 가이드
이 항목에서 심사위원이 보고 싶은 것: ...
주의할 점: ...

### 초안
[실제 신청서에 들어갈 내용]

### 보강 포인트
- 추가하면 점수 올라가는 내용: ...
- 현재 약점 및 대응 방안: ...
```

### Program-Specific Section Structure

**예비창업패키지 / 초기창업패키지**
1. 창업 아이템 개요 (문제->솔루션->목표고객)
2. 차별성/혁신성
3. 시장 분석 (TAM/SAM/SOM)
4. 사업화 계획 (로드맵/수익모델/고객확보)
5. 대표자 및 팀 역량
6. 지원금 사용 계획

**TIPS**
1. 기술 혁신성 (원천기술/특허/논문)
2. 팀 역량 + 팁스운영사 연계
3. 글로벌 시장 진출 가능성
4. R&D 목표 및 개발 계획 (TRL 명시)
5. Exit 전략 (IPO/M&A)

**전통시장/소상공인 활성화**
1. 현황 및 문제점 (지역 상권 데이터)
2. 사업 추진 방향 (상생/활성화 키워드)
3. 세부 추진 계획 및 일정
4. 기대 효과 (방문자 수/매출 증대/일자리 수치)
5. 지속 가능성 방안

**중소기업 기술개발(R&D)**
1. 개발 목표 및 최종 결과물 규격 (정량 목표 필수)
2. 국내외 기술 수준 및 개발 필요성
3. 수행기관 역량/협력기관
4. 연차별 세부 개발 계획 (간트차트 권장)
5. 기술 사업화 방안 (매출 예측)
6. 연구개발비 산정 근거

**관광벤처/문화콘텐츠**
1. 사업 아이디어 및 관광/문화적 가치
2. 차별화된 체험/콘텐츠 요소
3. 타깃 고객 (내국인/외국인/MZ세대 등)
4. 운영 계획 및 수익 모델
5. 지역 연계 및 파급 효과

### Document File Output

After drafting, chain to existing project skills for file generation:
- **Word (.docx)**: `anthropic-docx`
- **HWP/HWPX**: `rhwp-pipeline` (Mode E for native HWPX, Mode A for DOCX->HWP conversion)
- **Excel (.xlsx)**: `anthropic-xlsx` (for budget tables, timelines)

---

## MODE 3 -- Review & Feedback

**Triggers:** "신청서 검토해줘", "사업계획서 봐줘", "심사 기준으로 보면 어때"

### Evaluation Checklist

| 평가 항목 | 배점(일반) | 핵심 체크 포인트 |
|----------|----------|----------------|
| 사업성 | 30-40% | 시장 규모 수치, 수익 모델 구체성, 경쟁사 대비 차별점 |
| 기술성 | 20-30% | 기술 독창성, 구현 가능성 근거, 특허/논문 연계 |
| 팀 역량 | 20-25% | 관련 경력, 역할 분담 명확성, 외부 자문 |
| 실현가능성 | 15-20% | 일정 현실성, 예산 집행 계획, 리스크 대응 |
| 전달력 | 가산 | 핵심 메시지 위치, 수치/근거 활용, 오탈자/비문 |

### Output Template

```
## 종합 평가
전체 완성도: (5점 만점)

### 강점
- [구체적 강점]

### 반드시 보완 (TOP 3)
1. [항목] -- 현재: "..." -> 개선안: "..."
2. [항목] -- 현재: "..." -> 개선안: "..."
3. [항목] -- 현재: "..." -> 개선안: "..."

---
## 항목별 상세 피드백
### 사업성 / 기술성 / 팀 역량 / 실현가능성 / 전달력
[각 항목별 세부 의견 + 구체적 수정 방향]
```

---

## MODE 4 -- Timeline & Checklist

**Triggers:** "마감일 체크리스트", "준비 일정표", "언제까지 뭘 해야 해"

### Reverse-Schedule Template

```
## [사업명] 신청 준비 일정
마감일: YYYY년 MM월 DD일 (오늘 기준 D-N일)

| D-Day | 날짜  | 할 일                              | 완료 |
|-------|-------|------------------------------------|------|
| D-30  | MM/DD | 공고문 전체 정독 및 자격 최종 확인  | [ ]  |
| D-25  | MM/DD | 사업계획서 초안 작성 시작           | [ ]  |
| D-15  | MM/DD | 초안 내부 검토 및 피드백 반영       | [ ]  |
| D-10  | MM/DD | 외부 멘토/전문가 검토 (선택)        | [ ]  |
| D-7   | MM/DD | 필수 첨부서류 전체 수집 완료        | [ ]  |
| D-3   | MM/DD | 최종 완성본, 시스템 사전 테스트     | [ ]  |
| D-1   | MM/DD | 최종 제출 (당일 오류 대비)          | [ ]  |

> 마감 당일 오전 11시 이후 시스템 과부하로 접수 실패 사례 다수. D-1 제출 강력 권장.
```

### Common Required Documents

```
공통 서류
- [ ] 사업자등록증 사본 (예비창업자는 주민등록등본 등)
- [ ] 신청서 (시스템 입력 또는 별도 양식)
- [ ] 사업계획서 (사업별 양식)
- [ ] 개인정보 수집/이용 동의서

기업 서류 (해당 시)
- [ ] 법인등기부등본 또는 사업자등록 사실확인서
- [ ] 주주명부 (법인)
- [ ] 재무제표 (전년도, 필요시 2개년)

역량 증빙 서류 (해당 시)
- [ ] 특허 등록증/출원서 사본
- [ ] 수상/인증 증빙
- [ ] 투자 계약서 사본

사업별 특이 서류는 반드시 공고문에서 별도 확인.
```

---

## Post-Processing

Application drafts go through `sentence-polisher` for Korean grammar/spell check (Step 3.5 Barunhangeul) and `korean-tone-reviewer` for formality alignment before final delivery.

---

## Web Search Policy

Variable info (deadlines, amounts, headcount) is ALWAYS verified via web search.

Key announcement sites:
- 창업: https://www.k-startup.go.kr
- 중소기업: https://www.bizinfo.go.kr
- R&D: https://www.iris.go.kr / https://www.nrf.re.kr
- 전통시장: https://www.semas.or.kr
- 문화/관광: https://www.mcst.go.kr / https://www.kto.or.kr
- 농식품: https://www.mafra.go.kr

Always cite source URLs and recommend verifying against official announcements.

---

## Duplicate Funding Restrictions

- 동일 목적 지원사업 동시 수혜 제한 (창업패키지 계열 내 중복 불가)
- 동일 내용 다른 기관 중복 신청 금지
- TIPS 수혜 후 일부 창업 지원사업 제한 (공고문 확인 필수)
- 부정 수급 적발 시 환수/제재

---

## Do NOT Use For

- 법인 등기/세금 신고 등 법적 서류 작성 (법무사/세무사 영역)
- 금융 투자 상품 추천
- 종료된 공고 신청서 작성 (먼저 현재 공고 여부 확인)
- 신청 대행/실제 제출 행위 (정보 제공 및 초안 작성만 지원)
- 학술/연구 중심 과제는 grant-writer 레퍼런스 참고
