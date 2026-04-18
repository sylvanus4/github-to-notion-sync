# Template Schemas

JSON schemas for the 7 built-in education table types. Each schema defines
required/optional fields, column structure, merge map, and default dimensions.

---

## 1. 교과 진도표 (Curriculum Progress Table)

Tracks unit-by-unit lesson coverage across weeks and months for a semester.

### Schema

```json
{
  "template_type": "curriculum_progress",
  "required": {
    "subject": "string — 교과명 (e.g., '국어', '수학')",
    "grade": "integer — 학년 (1-6)",
    "semester": "integer — 학기 (1 or 2)",
    "year": "integer — 연도",
    "units": [
      {
        "unit_number": "integer",
        "unit_title": "string",
        "planned_weeks": ["string — e.g., '3/4', '3/11'"],
        "periods": "integer — 배당 차시",
        "textbook_pages": "string — optional"
      }
    ]
  },
  "optional": {
    "teacher_name": "string",
    "school_name": "string",
    "notes_column": "boolean — default true",
    "completion_check": "boolean — default true"
  }
}
```

### Column Structure

| Column | Width (mm) | Content |
|---|---|---|
| 월 (Month) | 15 | Month number, merged vertically |
| 주 (Week) | 15 | Week number or date range |
| 단원 (Unit) | 40 | Unit number + title |
| 차시 (Period) | 15 | Number of periods |
| 학습 내용 (Content) | 50 | Brief lesson topic |
| 교과서 (Textbook) | 20 | Page references |
| 비고 (Notes) | 15 | Completion mark / notes |

**Total width**: 170mm (A4 usable)

### Merge Map

- Month column: merge rows sharing the same month
- Unit column: merge rows within the same unit when spanning multiple weeks

---

## 2. 교수학습과정안 (Lesson Plan / Teaching-Learning Plan)

Detailed lesson execution plan for a single class session or unit.

### Schema

```json
{
  "template_type": "lesson_plan",
  "required": {
    "subject": "string",
    "grade": "integer",
    "unit_title": "string",
    "lesson_title": "string",
    "lesson_objectives": ["string — 학습 목표, 1-3 items"],
    "duration_minutes": "integer — 총 시간 (e.g., 40)",
    "activities": [
      {
        "phase": "string — '도입' | '전개' | '정리'",
        "duration_minutes": "integer",
        "teacher_activity": "string — 교사 활동",
        "student_activity": "string — 학생 활동",
        "materials": "string — optional, 자료 및 유의점"
      }
    ]
  },
  "optional": {
    "teacher_name": "string",
    "date": "string — YYYY-MM-DD",
    "period_number": "integer — 교시",
    "prior_knowledge": "string — 선수 학습",
    "assessment_plan": "string — 평가 계획",
    "differentiation": "string — 수준별 지도",
    "cross_curricular": ["string — 범교과 학습"],
    "core_competencies": ["string — 핵심역량"]
  }
}
```

### Column Structure (main activity table)

| Column | Width (mm) | Content |
|---|---|---|
| 단계 (Phase) | 20 | 도입/전개/정리, merged vertically |
| 시간 (Time) | 15 | Minutes allocation |
| 교수·학습 활동 (Activities) | — | Split into sub-columns |
| ├ 교사 활동 (Teacher) | 55 | Teacher instructions |
| └ 학생 활동 (Student) | 55 | Student actions |
| 자료(◈) 및 유의점(※) | 25 | Materials and cautions |

**Total width**: 170mm

### Header Section (above main table)

A separate info block rendered as a 2-column key-value table:

| Field | Content |
|---|---|
| 교과 | Subject name |
| 단원 | Unit title |
| 차시 | Period/lesson number |
| 학습 목표 | Learning objectives (can span full width) |
| 핵심역량 | Core competencies |

### Merge Map

- Phase column: merge all rows belonging to the same phase (도입/전개/정리)
- Learning objectives row: merge across all columns

---

## 3. 평가 루브릭 (Assessment Rubric)

Criteria-by-level evaluation matrix aligned with NCIC achievement standards.

### Schema

```json
{
  "template_type": "rubric",
  "required": {
    "subject": "string",
    "grade": "integer",
    "assessment_title": "string — 평가 과제명",
    "criteria": [
      {
        "criterion_name": "string — 평가 기준",
        "weight_percent": "integer — optional, 배점 비율",
        "levels": {
          "excellent": "string — 매우 잘함 / 상",
          "good": "string — 잘함 / 중",
          "needs_improvement": "string — 노력 요함 / 하"
        }
      }
    ]
  },
  "optional": {
    "unit_title": "string",
    "assessment_type": "string — '수행평가' | '형성평가' | '총괄평가'",
    "achievement_standard_code": "string — e.g., '[4국01-03]'",
    "level_count": "integer — 3 (default) or 4 or 5",
    "level_labels": ["string — custom level names"]
  }
}
```

### Column Structure

| Column | Width (mm) | Content |
|---|---|---|
| 평가 기준 (Criterion) | 35 | Criterion name |
| 배점 (Weight) | 15 | Percentage or points |
| 매우 잘함 / 상 (Excellent) | 40 | Level descriptor |
| 잘함 / 중 (Good) | 40 | Level descriptor |
| 노력 요함 / 하 (Needs work) | 40 | Level descriptor |

**Total width**: 170mm

### Merge Map

- No vertical merges (each criterion occupies one row)
- Header row: single level with all column headers

---

## 4. 학생 관찰 기록표 (Student Observation Record)

Per-student tracking grid for behavior, participation, and academic progress.

### Schema

```json
{
  "template_type": "observation_record",
  "required": {
    "grade": "integer",
    "class_number": "integer — 반",
    "observation_items": [
      {
        "item_name": "string — 관찰 항목 (e.g., '학습 태도', '협력')",
        "scale": "string — '상중하' | '○△×' | '1-5' | 'text'"
      }
    ],
    "student_count": "integer — number of rows to generate"
  },
  "optional": {
    "subject": "string",
    "semester": "integer",
    "date_range": "string — observation period",
    "student_names": ["string — pre-fill names"],
    "notes_column": "boolean — default true"
  }
}
```

### Column Structure

| Column | Width (mm) | Content |
|---|---|---|
| 번호 (No.) | 10 | Student number |
| 이름 (Name) | 20 | Student name |
| 관찰 항목 1 | dynamic | Rating/observation |
| 관찰 항목 2 | dynamic | Rating/observation |
| ... | dynamic | Additional items |
| 종합 의견 (Notes) | 30 | Teacher comments |

**Width calculation**: Remaining width = 170 - 10 - 20 - 30 = 110mm, divided equally among observation items.

### Merge Map

- No vertical merges; one row per student
- Header may have a 2-level structure if observation items are grouped by domain

---

## 5. 연구 과제 보고서 표 (Research Report Table)

Structured data presentation table for teacher research projects or school reports.

### Schema

```json
{
  "template_type": "research_report",
  "required": {
    "title": "string — 연구 과제명",
    "columns": [
      {
        "header": "string — column header",
        "width_mm": "integer — column width in mm",
        "align": "string — 'left' | 'center' | 'right'"
      }
    ],
    "rows": [
      ["string — cell values matching column order"]
    ]
  },
  "optional": {
    "table_number": "integer — for <표 N> numbering",
    "table_caption": "string — caption below table",
    "header_groups": [
      {
        "group_label": "string",
        "span_columns": [0, 2]
      }
    ],
    "summary_row": ["string — 합계/평균 row"],
    "source_citation": "string — 출처"
  }
}
```

### Column Structure

Fully user-defined via the `columns` array. Validation rule: sum of all
`width_mm` must equal 170.

### Merge Map

- Defined by `header_groups` for multi-level headers
- Summary row may merge leftmost columns for a "합계" label

---

## 6. 학급 운영 계획 (Classroom Management Plan)

Overview table for class goals, organization, roles, and scheduled activities.

### Schema

```json
{
  "template_type": "classroom_management",
  "required": {
    "grade": "integer",
    "class_number": "integer",
    "year": "integer",
    "sections": [
      {
        "section_title": "string — e.g., '학급 목표', '1인 1역할'",
        "content_type": "string — 'text' | 'list' | 'key_value' | 'grid'",
        "content": "object — varies by content_type"
      }
    ]
  },
  "optional": {
    "teacher_name": "string",
    "class_motto": "string — 학급 훈",
    "student_count": "integer",
    "monthly_plan": [
      {
        "month": "integer",
        "activities": ["string"]
      }
    ]
  }
}
```

### Content Type Details

- **text**: Single merged row spanning full width
- **list**: Bulleted/numbered items in a single cell
- **key_value**: 2-column layout (label | value)
- **grid**: Multi-column sub-table (e.g., role assignments)

### Column Structure

Varies by section. Default 2-column layout:

| Column | Width (mm) | Content |
|---|---|---|
| 항목 (Category) | 40 | Section title / label |
| 내용 (Content) | 130 | Section content |

**Total width**: 170mm

### Merge Map

- Section title cells merge vertically when a section spans multiple rows
- Full-width content rows merge across all columns

---

## 7. 시간표 (Weekly Timetable)

Standard weekly class schedule grid.

### Schema

```json
{
  "template_type": "timetable",
  "required": {
    "grade": "integer",
    "class_number": "integer",
    "periods_per_day": "integer — 교시 수 (typically 5-6)",
    "schedule": {
      "월": ["string — subject per period"],
      "화": ["string"],
      "수": ["string"],
      "목": ["string"],
      "금": ["string"]
    }
  },
  "optional": {
    "semester": "integer",
    "year": "integer",
    "period_times": [
      {
        "period": "integer",
        "start": "string — HH:MM",
        "end": "string — HH:MM"
      }
    ],
    "saturday": ["string — if applicable"],
    "special_rows": [
      {
        "label": "string — e.g., '아침 활동', '점심'",
        "position": "string — 'before:1' | 'after:4'"
      }
    ],
    "teacher_name": "string",
    "effective_date": "string — YYYY-MM-DD"
  }
}
```

### Column Structure

| Column | Width (mm) | Content |
|---|---|---|
| 교시 (Period) | 20 | Period number |
| 시간 (Time) | 25 | Start-end time |
| 월 (Mon) | 25 | Subject |
| 화 (Tue) | 25 | Subject |
| 수 (Wed) | 25 | Subject |
| 목 (Thu) | 25 | Subject |
| 금 (Fri) | 25 | Subject |

**Total width**: 170mm

### Merge Map

- Special rows (아침 활동, 점심) merge across all day columns
- No vertical merges in the main grid

---

## Common Schema Conventions

### Field Naming

- Korean terms in comments for teacher-facing documentation
- English camelCase for JSON keys
- All string values support Korean characters (UTF-8)

### Validation Rules

1. `grade` must be 1-6 (elementary school)
2. `semester` must be 1 or 2
3. Column width sums must not exceed 170mm
4. `activities.phase` in lesson plan must be one of: 도입, 전개, 정리
5. Rubric levels default to 3 (상/중/하) unless `level_count` overrides

### Default Values

| Field | Default |
|---|---|
| `grade` | 3 |
| `semester` | 1 |
| `year` | Current year |
| `notes_column` | `true` |
| `level_count` (rubric) | 3 |
| `periods_per_day` (timetable) | 6 |
| `completion_check` (progress) | `true` |
