# Example Tables

Annotated examples for each of the 7 built-in table templates.
Each example includes sample data, rendering notes, and expected layout.

---

## 1. 교과 진도표 (Curriculum Progress Table)

### Sample Data

```json
{
  "template_type": "curriculum_progress",
  "subject": "국어",
  "grade": 3,
  "semester": 1,
  "year": 2025,
  "teacher_name": "김영희",
  "school_name": "서울행복초등학교",
  "units": [
    {
      "unit_number": 1,
      "unit_title": "감동을 나누어요",
      "planned_weeks": ["3/4", "3/11", "3/18"],
      "periods": 10,
      "textbook_pages": "12-45"
    },
    {
      "unit_number": 2,
      "unit_title": "문단의 짜임",
      "planned_weeks": ["3/25", "4/1"],
      "periods": 8,
      "textbook_pages": "46-73"
    },
    {
      "unit_number": 3,
      "unit_title": "알맞은 높임 표현",
      "planned_weeks": ["4/8", "4/15", "4/22"],
      "periods": 10,
      "textbook_pages": "74-109"
    }
  ]
}
```

### Expected Layout

```
<표 1> 2025학년도 1학기 3학년 국어 교과 진도표

┌────┬──────┬─────────────────┬──────┬────────────┬──────────┬──────┐
│ 월 │  주  │     단원        │ 차시 │  학습 내용  │  교과서  │ 비고 │
├────┼──────┼─────────────────┼──────┼────────────┼──────────┼──────┤
│    │ 3/4  │                 │  3   │ 시 읽기    │ 12-20    │      │
│ 3  │ 3/11 │ 1. 감동을       │  4   │ 이야기읽기 │ 21-34    │      │
│    │ 3/18 │    나누어요     │  3   │ 감상문쓰기 │ 35-45    │      │
│    ├──────┼─────────────────┼──────┼────────────┼──────────┼──────┤
│    │ 3/25 │ 2. 문단의       │  4   │ 문단 구조  │ 46-60    │      │
├────┼──────┤    짜임         ├──────┼────────────┼──────────┼──────┤
│    │ 4/1  │                 │  4   │ 문단 쓰기  │ 61-73    │      │
│    ├──────┼─────────────────┼──────┼────────────┼──────────┼──────┤
│ 4  │ 4/8  │                 │  4   │ 높임법이해 │ 74-88    │      │
│    │ 4/15 │ 3. 알맞은       │  3   │ 높임법활용 │ 89-99    │      │
│    │ 4/22 │    높임 표현    │  3   │ 단원정리   │ 100-109  │      │
└────┴──────┴─────────────────┴──────┴────────────┴──────────┴──────┘
```

### Rendering Notes

- **Month column**: vertically merged for rows in the same month
- **Unit column**: vertically merged for rows in the same unit
- **비고 column**: left blank for teacher to mark ○/× during semester
- Header row: #F2F2F2 background, bold, centered
- Border: 1.5pt outer, 0.5pt inner horizontal, 0.25pt inner vertical (gray)

---

## 2. 교수학습과정안 (Lesson Plan)

### Sample Data

```json
{
  "template_type": "lesson_plan",
  "subject": "수학",
  "grade": 4,
  "unit": "3. 곱셈과 나눗셈",
  "lesson_number": 5,
  "total_lessons": 12,
  "date": "2025-04-15",
  "period": 3,
  "teacher_name": "박지수",
  "learning_objective": "세 자리 수 × 두 자리 수의 곱셈을 할 수 있다.",
  "core_competency": "문제 해결, 추론",
  "activities": [
    {
      "phase": "도입",
      "duration_min": 5,
      "teacher_activity": "전시 학습 확인 및 동기 유발\n- 일상생활에서 곱셈이 필요한 상황 제시",
      "student_activity": "전시 학습 내용 발표\n- 곱셈이 필요한 상황 이야기하기",
      "materials_notes": "◈ PPT 슬라이드\n※ 학생의 다양한 답변을 수용한다"
    },
    {
      "phase": "전개",
      "duration_min": 30,
      "teacher_activity": "세 자리 수 × 두 자리 수 풀이 과정 안내\n- 부분곱 방법 시범\n- 모둠별 연습 문제 제시",
      "student_activity": "부분곱 방법으로 풀기\n- 모둠별 협력 학습\n- 풀이 과정 발표",
      "materials_notes": "◈ 학습지, 수 모형\n◈ 모둠 활동판\n※ 계산 과정을 반드시 쓰도록 지도"
    },
    {
      "phase": "정리",
      "duration_min": 5,
      "teacher_activity": "핵심 정리 및 차시 예고\n- 형성평가 문제 제시",
      "student_activity": "학습 내용 정리\n- 형성평가 풀기\n- 차시 예고 확인",
      "materials_notes": "◈ 형성평가지"
    }
  ]
}
```

### Expected Layout

```
<표 2> 교수·학습 과정안

┌──────────┬────────────────┬──────────┬─────────────────┐
│ 교 과    │ 수학           │ 학 년    │ 4학년           │
├──────────┼────────────────┼──────────┼─────────────────┤
│ 단 원    │ 3. 곱셈과 나눗셈│ 차 시   │ 5/12            │
├──────────┼────────────────┼──────────┼─────────────────┤
│ 일 시    │ 2025.04.15.    │ 교시     │ 3교시           │
├──────────┼────────────────┼──────────┼─────────────────┤
│ 핵심역량 │ 문제 해결, 추론 │ 지도교사 │ 박지수          │
├──────────┴────────────────┴──────────┴─────────────────┤
│ 학습 목표: 세 자리 수 × 두 자리 수의 곱셈을 할 수 있다. │
├──────┬──────┬──────────────┬──────────────┬────────────┤
│ 단계 │ 시간 │  교사 활동    │  학생 활동    │ 자료 및    │
│      │ (분) │              │              │ 유의점(※)  │
├──────┼──────┼──────────────┼──────────────┼────────────┤
│      │      │ 전시 학습    │ 전시 학습    │ ◈ PPT     │
│ 도입 │  5   │ 확인 및      │ 내용 발표    │ 슬라이드   │
│      │      │ 동기 유발    │              │ ※ 다양한  │
│      │      │              │              │ 답변 수용  │
├──────┼──────┼──────────────┼──────────────┼────────────┤
│      │      │ 풀이 과정    │ 부분곱       │ ◈ 학습지  │
│ 전개 │  30  │ 안내         │ 방법으로     │ ◈ 수 모형 │
│      │      │ - 부분곱     │ 풀기         │ ◈ 모둠    │
│      │      │   시범       │ - 모둠별     │ 활동판     │
│      │      │ - 모둠별     │   협력 학습  │ ※ 계산    │
│      │      │   연습       │ - 발표       │ 과정 필수  │
├──────┼──────┼──────────────┼──────────────┼────────────┤
│ 정리 │  5   │ 핵심 정리    │ 학습 내용    │ ◈ 형성    │
│      │      │ 차시 예고    │ 정리         │ 평가지     │
│      │      │ 형성평가     │ 형성평가     │            │
└──────┴──────┴──────────────┴──────────────┴────────────┘
```

### Rendering Notes

- **Header section**: 4-column key-value layout with merged rows
- **Learning objective row**: full-width merge across all columns
- **Phase column**: vertically merged within each phase
- **Time column**: centered, Arabic numerals
- **Materials column**: uses ◈ prefix for materials, ※ prefix for cautions
- Phase differentiation: text labels only (도입/전개/정리), no background colors

---

## 3. 평가 루브릭 (Assessment Rubric)

### Sample Data

```json
{
  "template_type": "rubric",
  "subject": "국어",
  "grade": 5,
  "unit": "4. 글의 짜임",
  "achievement_standard": "[6국03-04]",
  "assessment_type": "수행평가",
  "assessment_title": "설명문 쓰기",
  "criteria": [
    {
      "criterion": "글의 구조",
      "weight_percent": 40,
      "levels": {
        "상": "처음-가운데-끝 구조를 갖추고, 단락 간 연결이 자연스러움",
        "중": "처음-가운데-끝 구조를 갖추었으나, 단락 연결이 부자연스러운 부분이 있음",
        "하": "글의 구조가 불분명하거나 단락 구분이 되지 않음"
      }
    },
    {
      "criterion": "내용 전개",
      "weight_percent": 35,
      "levels": {
        "상": "주제에 맞는 내용을 다양한 방법(예시, 비교, 분류)으로 전개함",
        "중": "주제에 맞는 내용이나 전개 방법이 단조로움",
        "하": "주제와 관련 없는 내용이 포함되거나 전개 방법이 보이지 않음"
      }
    },
    {
      "criterion": "표현과 어법",
      "weight_percent": 25,
      "levels": {
        "상": "문장이 정확하고, 어법에 맞으며, 적절한 어휘를 사용함",
        "중": "대체로 어법에 맞으나, 일부 문장이 어색함",
        "하": "맞춤법, 띄어쓰기 오류가 많고 문장이 불명확함"
      }
    }
  ]
}
```

### Expected Layout

```
<표 3> 설명문 쓰기 수행평가 루브릭

┌──────────┬────────────────────────────────────────────────┐
│ 교과     │ 국어                                           │
├──────────┼────────────────────────────────────────────────┤
│ 학년     │ 5학년                                          │
├──────────┼────────────────────────────────────────────────┤
│ 성취기준 │ [6국03-04] 적절한 설명 방법을 사용하여 대상의  │
│          │ 특성이 드러나게 설명하는 글을 쓴다.             │
├──────────┼────────────────────────────────────────────────┤
│ 평가유형 │ 수행평가                                       │
├──────────┼──────┬──────────┬──────────┬──────────────────┤
│          │      │          │          │    성취수준       │
│ 평가기준 │비중(%│    상    │    중    │       하         │
│          │     )│          │          │                  │
├──────────┼──────┼──────────┼──────────┼──────────────────┤
│          │      │ 처음-    │ 처음-    │ 글의 구조가      │
│ 글의 구조│  40  │ 가운데-끝│ 가운데-끝│ 불분명하거나     │
│          │      │ 구조,    │ 구조이나 │ 단락 구분이      │
│          │      │ 자연스러 │ 연결이   │ 되지 않음        │
│          │      │ 운 연결  │ 부자연스 │                  │
│          │      │          │ 러운 부분│                  │
├──────────┼──────┼──────────┼──────────┼──────────────────┤
│          │      │ 다양한   │ 주제에   │ 관련 없는        │
│ 내용 전개│  35  │ 방법으로 │ 맞으나   │ 내용 포함 또는   │
│          │      │ 전개     │ 단조로움 │ 방법 미비        │
├──────────┼──────┼──────────┼──────────┼──────────────────┤
│ 표현과   │      │ 정확하고 │ 대체로   │ 맞춤법/띄어쓰기  │
│ 어법     │  25  │ 적절한   │ 어법에   │ 오류 많고        │
│          │      │ 어휘     │ 맞음     │ 문장 불명확      │
└──────────┴──────┴──────────┴──────────┴──────────────────┘

출처: 2022 개정 교육과정 국어과 성취기준 (교육부, 2022)
```

### Rendering Notes

- **Header info section**: 2-column key-value layout
- **Achievement standard**: displays official code in brackets
- **Level columns** (상/중/하): equal width, left-aligned descriptive text
- **Weight column**: centered, numeric with %
- **Criterion column**: vertically merged when descriptors span multiple lines
- Source citation required when referencing NCIC standards

---

## 4. 학생 관찰 기록표 (Student Observation Record)

### Sample Data

```json
{
  "template_type": "observation_record",
  "subject": "사회",
  "grade": 3,
  "semester": 1,
  "observation_period": "2025.03 - 2025.07",
  "class_number": "3학년 2반",
  "domains": ["학습 태도", "협력 활동", "발표 능력", "과제 수행"],
  "students": [
    {
      "number": 1,
      "name": "가나다",
      "records": {
        "학습 태도": "○",
        "협력 활동": "○",
        "발표 능력": "△",
        "과제 수행": "○"
      },
      "narrative": "수업에 적극적으로 참여하나 발표 시 자신감이 부족함. 모둠 활동에서 협력적인 태도를 보임."
    },
    {
      "number": 2,
      "name": "라마바",
      "records": {
        "학습 태도": "△",
        "협력 활동": "○",
        "발표 능력": "○",
        "과제 수행": "△"
      },
      "narrative": "발표를 좋아하고 의견 표현이 활발함. 개별 과제 마무리에 시간이 더 필요함."
    }
  ]
}
```

### Expected Layout

```
<표 4> 3학년 2반 사회 학생 관찰 기록표 (2025.03-2025.07)

┌────┬──────┬──────┬──────┬──────┬──────┬────────────────────────┐
│번호│ 이름 │학습  │협력  │발표  │과제  │     종합 관찰 소견      │
│    │      │태도  │활동  │능력  │수행  │                        │
├────┼──────┼──────┼──────┼──────┼──────┼────────────────────────┤
│ 1  │가나다│  ○  │  ○  │  △  │  ○  │ 수업에 적극적으로       │
│    │      │      │      │      │      │ 참여하나 발표 시       │
│    │      │      │      │      │      │ 자신감이 부족함.       │
│    │      │      │      │      │      │ 모둠 활동에서 협력적.  │
├────┼──────┼──────┼──────┼──────┼──────┼────────────────────────┤
│ 2  │라마바│  △  │  ○  │  ○  │  △  │ 발표를 좋아하고 의견    │
│    │      │      │      │      │      │ 표현이 활발함.         │
│    │      │      │      │      │      │ 개별 과제 마무리에     │
│    │      │      │      │      │      │ 시간이 더 필요함.      │
├────┼──────┼──────┼──────┼──────┼──────┼────────────────────────┤
│ …  │ …    │      │      │      │      │                        │
└────┴──────┴──────┴──────┴──────┴──────┴────────────────────────┘
```

### Rendering Notes

- **Domain columns**: centered, uses ○/△/× symbols
- **Narrative column**: widest, left-aligned, multi-line
- **Number column**: narrow (15mm), centered
- **Name column**: centered, 20mm
- Print on landscape if class size exceeds 30 students with many domains

---

## 5. 연구 과제 보고서 표 (Research Report Table)

### Sample Data

```json
{
  "template_type": "research_report",
  "title": "프로젝트 기반 학습이 초등학생 문제 해결 능력에 미치는 영향",
  "researcher": "이미영",
  "research_period": "2025.03 - 2025.12",
  "sections": [
    {
      "section_title": "연구 대상 및 기간",
      "rows": [
        { "category": "연구 대상", "content": "서울특별시 ○○초등학교 5학년 2개 반 (실험반 28명, 대조반 27명)" },
        { "category": "연구 기간", "content": "2025년 3월 ~ 12월 (10개월)" },
        { "category": "연구 방법", "content": "준실험 설계 (사전-사후 검사)" }
      ]
    },
    {
      "section_title": "실행 과제 및 일정",
      "rows": [
        { "phase": "1단계", "period": "3-4월", "task": "사전 검사 및 프로젝트 기반 학습 설계", "output": "검사 도구, 학습 설계안" },
        { "phase": "2단계", "period": "5-9월", "task": "프로젝트 기반 학습 적용 및 수업 실행", "output": "수업 기록, 관찰 일지" },
        { "phase": "3단계", "period": "10-11월", "task": "사후 검사 및 결과 분석", "output": "검사 결과, 분석 자료" },
        { "phase": "4단계", "period": "12월", "task": "보고서 작성 및 일반화 방안 도출", "output": "연구 보고서" }
      ]
    }
  ]
}
```

### Expected Layout

```
<표 5> 연구 과제 실행 계획

┌──────────────────────────────────────────────────────────┐
│ 연구 주제: 프로젝트 기반 학습이 초등학생 문제 해결       │
│           능력에 미치는 영향                              │
├──────────┬───────────────────────────────────────────────┤
│ 연구자   │ 이미영                                        │
├──────────┼───────────────────────────────────────────────┤
│ 연구 기간│ 2025.03 - 2025.12                             │
├──────────┴───────────────────────────────────────────────┤

[연구 대상 및 기간]

┌──────────┬───────────────────────────────────────────────┐
│ 연구 대상│ 서울특별시 ○○초등학교 5학년 2개 반            │
│          │ (실험반 28명, 대조반 27명)                     │
├──────────┼───────────────────────────────────────────────┤
│ 연구 기간│ 2025년 3월 ~ 12월 (10개월)                    │
├──────────┼───────────────────────────────────────────────┤
│ 연구 방법│ 준실험 설계 (사전-사후 검사)                   │
└──────────┴───────────────────────────────────────────────┘

[실행 과제 및 일정]

┌──────┬────────┬──────────────────────┬──────────────────┐
│ 단계 │  기간  │      과제 내용       │     산출물       │
├──────┼────────┼──────────────────────┼──────────────────┤
│1단계 │ 3-4월  │ 사전 검사 및         │ 검사 도구,       │
│      │        │ PBL 설계             │ 학습 설계안      │
├──────┼────────┼──────────────────────┼──────────────────┤
│2단계 │ 5-9월  │ PBL 적용 및          │ 수업 기록,       │
│      │        │ 수업 실행            │ 관찰 일지        │
├──────┼────────┼──────────────────────┼──────────────────┤
│3단계 │10-11월 │ 사후 검사 및         │ 검사 결과,       │
│      │        │ 결과 분석            │ 분석 자료        │
├──────┼────────┼──────────────────────┼──────────────────┤
│4단계 │ 12월   │ 보고서 작성 및       │ 연구 보고서      │
│      │        │ 일반화 방안 도출     │                  │
└──────┴────────┴──────────────────────┴──────────────────┘
```

### Rendering Notes

- **Research title**: full-width merged row, left-aligned
- **Section sub-headers**: displayed between separate table blocks
- **Phase column**: centered, uses Korean ordinal labels
- **Period column**: centered, compact date range
- **Task/Output columns**: left-aligned for readability

---

## 6. 학급 운영 계획 (Classroom Management Plan)

### Sample Data

```json
{
  "template_type": "classroom_management",
  "grade": 2,
  "class_number": 3,
  "year": 2025,
  "teacher_name": "정수민",
  "class_goal": "서로 존중하고 배려하는 행복한 교실",
  "monthly_plans": [
    { "month": 3, "focus": "학급 규칙 세우기", "events": "입학식, 학부모 상담", "activities": "자기소개 활동, 역할 정하기" },
    { "month": 4, "focus": "바른 학습 습관 형성", "events": "과학의 날", "activities": "독서 습관 프로그램 시작" },
    { "month": 5, "focus": "친구 사이 존중", "events": "어린이날, 스승의 날", "activities": "감사 편지 쓰기, 협동 놀이" },
    { "month": 6, "focus": "1학기 마무리", "events": "현장체험학습", "activities": "1학기 반성, 여름 독서 계획" }
  ]
}
```

### Expected Layout

```
<표 6> 2025학년도 2학년 3반 학급 운영 계획

┌──────────────────────────────────────────────────────┐
│ 학급 목표: 서로 존중하고 배려하는 행복한 교실         │
├──────┬──────────────┬────────────┬───────────────────┤
│  월  │  중점 지도    │  학교 행사  │   학급 활동       │
├──────┼──────────────┼────────────┼───────────────────┤
│  3   │ 학급 규칙    │ 입학식,    │ 자기소개 활동,    │
│      │ 세우기       │ 학부모 상담│ 역할 정하기       │
├──────┼──────────────┼────────────┼───────────────────┤
│  4   │ 바른 학습    │ 과학의 날  │ 독서 습관         │
│      │ 습관 형성    │            │ 프로그램 시작     │
├──────┼──────────────┼────────────┼───────────────────┤
│  5   │ 친구 사이    │ 어린이날,  │ 감사 편지 쓰기,   │
│      │ 존중         │ 스승의 날  │ 협동 놀이         │
├──────┼──────────────┼────────────┼───────────────────┤
│  6   │ 1학기        │ 현장체험   │ 1학기 반성,       │
│      │ 마무리       │ 학습       │ 여름 독서 계획    │
└──────┴──────────────┴────────────┴───────────────────┘
```

### Rendering Notes

- **Class goal row**: full-width merge, left-aligned, slightly larger font (10pt)
- **Month column**: centered, simple Arabic number
- **All body content**: left-aligned for readability
- Compact format — one table covers the entire semester at a glance

---

## 7. 시간표 (Weekly Timetable)

### Sample Data

```json
{
  "template_type": "timetable",
  "grade": 4,
  "class_number": 1,
  "semester": 1,
  "year": 2025,
  "periods_per_day": 6,
  "schedule": {
    "월": ["국어", "국어", "수학", "사회", "체육", "창체"],
    "화": ["수학", "과학", "국어", "음악", "영어", "도덕"],
    "수": ["국어", "수학", "사회", "미술", "미술", "—"],
    "목": ["수학", "국어", "과학", "과학", "체육", "영어"],
    "금": ["국어", "수학", "실과", "실과", "창체", "창체"]
  },
  "period_times": [
    "09:00-09:40",
    "09:50-10:30",
    "10:40-11:20",
    "11:30-12:10",
    "13:10-13:50",
    "14:00-14:40"
  ],
  "lunch_after_period": 4
}
```

### Expected Layout

```
<표 7> 2025학년도 1학기 4학년 1반 주간 시간표

┌──────┬─────────────┬──────┬──────┬──────┬──────┬──────┐
│ 교시 │    시간      │  월  │  화  │  수  │  목  │  금  │
├──────┼─────────────┼──────┼──────┼──────┼──────┼──────┤
│  1   │ 09:00-09:40 │ 국어 │ 수학 │ 국어 │ 수학 │ 국어 │
├──────┼─────────────┼──────┼──────┼──────┼──────┼──────┤
│  2   │ 09:50-10:30 │ 국어 │ 과학 │ 수학 │ 국어 │ 수학 │
├──────┼─────────────┼──────┼──────┼──────┼──────┼──────┤
│  3   │ 10:40-11:20 │ 수학 │ 국어 │ 사회 │ 과학 │ 실과 │
├──────┼─────────────┼──────┼──────┼──────┼──────┼──────┤
│  4   │ 11:30-12:10 │ 사회 │ 음악 │ 미술 │ 과학 │ 실과 │
├──────┼─────────────┼──────┼──────┼──────┼──────┼──────┤
│      │ 12:10-13:10 │            점심              │
├──────┼─────────────┼──────┼──────┼──────┼──────┼──────┤
│  5   │ 13:10-13:50 │ 체육 │ 영어 │ 미술 │ 체육 │ 창체 │
├──────┼─────────────┼──────┼──────┼──────┼──────┼──────┤
│  6   │ 14:00-14:40 │ 창체 │ 도덕 │  —   │ 영어 │ 창체 │
└──────┴─────────────┴──────┴──────┴──────┴──────┴──────┘
```

### Rendering Notes

- **Lunch row**: full-width merge across all day columns, light gray (#F2F2F2) background, centered "점심" label
- **Period column**: centered, narrow (15mm)
- **Time column**: centered, fixed width (30mm)
- **Day columns**: centered, equal width (remainder ÷ 5)
- **Empty periods**: em dash (—)
- All cells same height for uniform grid appearance
- Suitable for A4 portrait — compact enough to fit on one page

---

## Output Validation

Each generated table should pass these checks:

1. **Structural**: header row exists, all cells have borders, column widths sum correctly
2. **Content**: Korean text is grammatically correct, symbols are consistent
3. **Style**: fonts, sizes, colors match style-guide.md specifications
4. **Print**: table fits A4 page without overflow, readable at standard print resolution
5. **Numbering**: `<표 N>` format is applied correctly
