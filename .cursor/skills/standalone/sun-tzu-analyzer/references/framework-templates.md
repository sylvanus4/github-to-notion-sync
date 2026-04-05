# Sun Tzu Competitive Analyzer — Output Templates

Reference templates for each operating mode. The agent uses these structures when generating analysis output.

---

## Template 1: Standalone / Competitive / Trading Mode

```markdown
# 손자병법 전략 분석: {상황 제목}

**분석 일자**: {YYYY-MM-DD}
**모드**: {Standalone | Competitive | Trading}
**신뢰도**: {High | Medium | Low} — {근거 한 줄}

---

## 지형 재해석

이 전장은 당신이 생각하는 것과 다르다.

{Factor 1 분석 — 실제 전장의 구조와 통제권 분석. 2-3 단락, 각 단락이 판결처럼.}

## 진짜 적

{Factor 2 분석 — 감정적 프레이밍을 벗기고 실제 대항력을 명명. 경쟁사가 아닌 경우 그 이유.}

## 상대적 강약점

{Factor 3 분석}

**아군 강점**:
{실제로 우위에 있는 영역}

**아군 약점**:
{취약한 영역, 솔직하게}

**적의 강점**:
{상대의 실제 우위}

**적의 과잉투입/사각지대**:
{상대가 과도하게 집중하거나 놓치고 있는 영역}

## 정보 비대칭

{Factor 4 분석}

**우리가 아는 것 (상대 모름)**: {구체적으로}
**상대가 아는 것 (우리 모름)**: {구체적으로}
**획득해야 할 정보**: {행동 전에 반드시 알아야 할 것}

## 타이밍 판단

{Factor 5 분석 — 기세의 방향, 진격/대기/후퇴 중 하나를 명확히}

---

## 전략적 처방

### 1단계: 지형 판독
{실제 전장에 대한 한 단락 판결}

### 2단계: 적 명명
{실제 대항력에 대한 한 단락 판결}

### 3단계: 허점 식별
{상대의 방어 불가능한 취약점. 정밀 타격 지점.}

### 4단계: 정확한 행동 지시
- **행동**: {7일 이내 실행 가능한 구체적 액션}
- **담당**: {실행 주체}
- **기한**: {YYYY-MM-DD, 7일 이내}
- **측정 기준**: {성공 여부를 판단하는 구체적 기준}

### 5단계: 피해야 할 함정
{매력적으로 보이지만 상대에게 유리한 한 가지 행동. 왜 함정인지 구체적 근거.}

### 6단계: 지배 원리
> {손자병법 원리 한 줄} — {해당 편 이름 (예: 제6편 허실)}

---

## 참고 챕터
- {편 번호}: {편 이름} — {이 분석에서 적용한 이유 한 줄}
```

---

## Template 2: Role Layer Mode (Concise Brief)

Used when invoked by `role-cso`, `role-ceo`, or other role-dispatcher pipeline steps. Must stay under 200 words.

```markdown
# 전략 지형 브리프: {토픽}

**관련도**: {N}/10
**모드**: Role Layer (CSO/CEO 서브분석)

## 핵심 지형 (2-3 bullets)
- {지형 재해석 핵심 1}
- {지형 재해석 핵심 2}
- {지형 재해석 핵심 3 (optional)}

## 진짜 적 (1 bullet)
- {실제 대항력 — 가장 중요한 적을 하나만}

## 허점과 처방 (2-3 bullets)
- **허점**: {상대의 방어 불가능 취약점}
- **처방**: {7일 이내 구체적 행동}
- **함정**: {피해야 할 매력적 실수}

## 지배 원리
> {손자병법 원리 한 줄} — {편 이름}
```

---

## Template 3: Trading Mode Adaptations

When `--trading` is active, the 5 factors use market-specific language:

| Standard Factor | Trading Factor | Analysis Focus |
|-----------------|---------------|----------------|
| 지형 | 시장 구조 | Sector rotation, liquidity conditions, market regime |
| 적 | 진짜 대항력 | Fed policy, momentum reversal, sector rotation, own cognitive bias |
| 강약점 | 포지션 대비 | Current portfolio positioning vs. market regime alignment |
| 정보 비대칭 | 미반영 정보 | What the market has NOT priced in |
| 타이밍 | 기술적 신호 | RSI, ADX, volume divergence, earnings calendar, macro events |

**Safety Constraint**: Trading mode output MUST NOT contain specific buy/sell/hold recommendations for individual tickers. Frame as strategic positioning guidance only. Include this footer:

```markdown
---
⚠️ 이 분석은 전략적 포지셔닝 가이드이며, 개별 종목 매매 추천이 아닙니다.
구체적 매매 실행은 daily-stock-check 및 tossinvest-trading 스킬을 참조하세요.
```

---

## Template 4: Competitive Overlay Mode

When `--competitive` is active, the analysis integrates competitive intelligence data:

```markdown
# 손자병법 경쟁 전략 분석: {상황 제목}

**분석 일자**: {YYYY-MM-DD}
**모드**: Competitive
**데이터 소스**: {kwp-product-management-competitive-analysis | kwp-marketing-competitive-analysis | manual input}
**신뢰도**: {High | Medium | Low} — {근거 한 줄}

---

## 경쟁 지형도

이 전장은 당신이 생각하는 것과 다르다.

{Standard terrain analysis enriched with competitive data}

### 경쟁사 포지셔닝 매핑
| 경쟁사 | 표면적 위협 | 실제 위협 | 취약점 |
|--------|-----------|----------|--------|
| {이름1} | {보이는 것} | {실제} | {gap} |
| {이름2} | {보이는 것} | {실제} | {gap} |

## 진짜 적

{Factor 2 — 가장 위험한 경쟁사는 가장 눈에 띄는 경쟁사가 아닐 수 있다}

{Remaining factors and prescription follow the Standalone template}
```

---

## Template 5: First Principles Pre-Pass

When `--with-first-principles` is active, prepend:

```markdown
## 전제 분해 (First Principles Pre-Pass)

손자병법 분석에 앞서, 상황의 기본 전제를 분해합니다.

### 제거된 가정
1. {가정 1} — {왜 이 가정이 의심스러운가}
2. {가정 2} — {왜 이 가정이 의심스러운가}
3. {가정 3} — {왜 이 가정이 의심스러운가}

### 근본 진실 (Bedrock Truths)
1. {증명 가능한 진실 1}
2. {증명 가능한 진실 2}
3. {증명 가능한 진실 3}

---

{Then proceed with standard Sun Tzu analysis, now grounded in stripped assumptions}
```

---

## Template 6: SCQA Output Format

When `--output scqa` is active, format the verdict section as:

```markdown
## 전략적 판결 (SCQA)

### Situation (상황)
{현재 전장의 객관적 상태 — 지형 재해석에서 도출}

### Complication (위기)
{진짜 적과 정보 비대칭이 만드는 구체적 위협}

### Question (핵심 질문)
{이 상황에서 답해야 할 단 하나의 전략적 질문}

### Answer (처방)
{정확한 행동 지시 — 4단계 형식 유지}
- **행동**: {구체적 액션}
- **담당**: {실행자}
- **기한**: {7일 이내}
- **측정 기준**: {성공 기준}

### 함정 경고
{5단계 — 피해야 할 행동}

### 지배 원리
> {손자병법 원리} — {편 이름}
```

---

## Output File Paths

| Mode | Path Pattern |
|------|-------------|
| Standalone | `outputs/sun-tzu/{YYYY-MM-DD}/analysis-{slug}.md` |
| Competitive | `outputs/sun-tzu/{YYYY-MM-DD}/competitive-{slug}.md` |
| Trading | `outputs/sun-tzu/{YYYY-MM-DD}/trading-{slug}.md` |
| Role Layer | `outputs/role-analysis/{slug}/sun-tzu-brief.md` |
| First Principles | Same as base mode with `-fp` suffix |
| SCQA | Same as base mode with `-scqa` suffix |

**Slug Generation**: Extract 3-5 keywords from the situation, lowercase, hyphenated.
Example: "SaaS 제품이 대기업 경쟁사의 가격 인하에 직면" → `saas-price-war-enterprise`

---

## Binary Eval Gate Checklist

Before finalizing any output, verify:

- [ ] **EVAL 1 — Terrain Reframe**: "지형 재해석" presents a battlefield framing that differs from the user's initial description
- [ ] **EVAL 2 — Five Factors Complete**: All 5 factors contain non-empty, specific analysis (no generic "경쟁이 치열하다")
- [ ] **EVAL 3 — Actionable Prescription**: "정확한 행동 지시" has: specific action + 담당 + 기한 (7일 이내) + 측정 기준
- [ ] **EVAL 4 — Trap Identification**: Names exactly one specific attractive-but-wrong move with concrete reasoning
