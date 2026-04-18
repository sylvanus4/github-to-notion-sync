#!/usr/bin/env python3
"""
Korean Education Table Generator — HWPX output via python-hwpx.

Generates HWPX files for 7 built-in table templates:
  1. curriculum_progress  — 교과 진도표
  2. lesson_plan          — 교수학습과정안
  3. rubric               — 평가 루브릭
  4. observation_record   — 학생 관찰 기록표
  5. research_report      — 연구 과제 보고서 표
  6. classroom_management — 학급 운영 계획
  7. timetable            — 시간표
"""

import argparse
import json
import sys
import xml.etree.ElementTree as ET

import lxml.etree as lxml_et
from hwpx import HwpxDocument

# ---------------------------------------------------------------------------
# Monkey-patch: python-hwpx uses stdlib ET.SubElement internally, but when
# lxml is installed, some parent elements are lxml._Element instances.
# This patch transparently routes to the correct SubElement implementation.
# ---------------------------------------------------------------------------
_original_SubElement = ET.SubElement


def _patched_SubElement(parent, tag, attrib={}, **extra):
    if isinstance(parent, lxml_et._Element):
        return lxml_et.SubElement(parent, tag, attrib, **extra)
    return _original_SubElement(parent, tag, attrib, **extra)


ET.SubElement = _patched_SubElement

# ---------------------------------------------------------------------------
# Constants (HWPX units: 1/100 mm)
# ---------------------------------------------------------------------------
A4_W = 21000
A4_H = 29700
MARGIN_TOP = 1500
MARGIN_BOTTOM = 1500
MARGIN_LEFT = 2000
MARGIN_RIGHT = 2000
MARGIN_HEADER = 1000
MARGIN_FOOTER = 1000

# Korean teacher-style table formatting constants
_HH = "{http://www.hancom.co.kr/hwpml/2011/head}"
_HC = "{http://www.hancom.co.kr/hwpml/2011/core}"
_HP = "{http://www.hancom.co.kr/hwpml/2011/paragraph}"

COLOR_HEADER_BG = "#F2F2F2"
COLOR_FIRST_COL_BG = "#F9F9F9"

BORDER_FILL_HEADER = "10"
BORDER_FILL_DATA = "11"
BORDER_FILL_FIRST_COL = "12"

# Cell margins in 1/100 mm: 6pt ~ 212, 8pt ~ 282
CELL_MARGIN_TB = "212"
CELL_MARGIN_LR = "282"


def _register_border_fills(doc: HwpxDocument):
    """Register Korean teacher-style borderFill definitions in the document header."""
    header = doc.oxml._headers[0]
    bf_container = header._border_fills_element(create=True)

    def _add_bf(bf_id, top_w, bottom_w, left_w, right_w,
                top_c="#000000", bottom_c="#000000",
                left_c="#BFBFBF", right_c="#BFBFBF",
                bg_color=None):
        bf = lxml_et.SubElement(bf_container, f"{_HH}borderFill", {
            "id": bf_id, "threeD": "0", "shadow": "0",
            "centerLine": "NONE", "breakCellSeparateLine": "0",
        })
        lxml_et.SubElement(bf, f"{_HH}slash",
                           {"type": "NONE", "Crooked": "0", "isCounter": "0"})
        lxml_et.SubElement(bf, f"{_HH}backSlash",
                           {"type": "NONE", "Crooked": "0", "isCounter": "0"})
        lxml_et.SubElement(bf, f"{_HH}leftBorder",
                           {"type": "Solid", "width": left_w, "color": left_c})
        lxml_et.SubElement(bf, f"{_HH}rightBorder",
                           {"type": "Solid", "width": right_w, "color": right_c})
        lxml_et.SubElement(bf, f"{_HH}topBorder",
                           {"type": "Solid", "width": top_w, "color": top_c})
        lxml_et.SubElement(bf, f"{_HH}bottomBorder",
                           {"type": "Solid", "width": bottom_w, "color": bottom_c})
        lxml_et.SubElement(bf, f"{_HH}diagonal",
                           {"type": "SOLID", "width": "0.1 mm", "color": "#000000"})
        if bg_color:
            fill = lxml_et.SubElement(bf, f"{_HC}fillBrush")
            lxml_et.SubElement(fill, f"{_HC}winBrush",
                               {"faceColor": bg_color, "hatchColor": bg_color, "alpha": "0"})

    _add_bf(BORDER_FILL_HEADER,
            top_w="1.50 mm", bottom_w="1.00 mm",
            left_w="1.50 mm", right_w="1.50 mm",
            top_c="#000000", bottom_c="#808080",
            left_c="#000000", right_c="#000000",
            bg_color=COLOR_HEADER_BG)

    _add_bf(BORDER_FILL_DATA,
            top_w="0.50 mm", bottom_w="0.50 mm",
            left_w="0.25 mm", right_w="0.25 mm",
            top_c="#808080", bottom_c="#808080")

    _add_bf(BORDER_FILL_FIRST_COL,
            top_w="0.50 mm", bottom_w="0.50 mm",
            left_w="0.25 mm", right_w="0.25 mm",
            top_c="#808080", bottom_c="#808080",
            bg_color=COLOR_FIRST_COL_BG)

    header._update_border_fills_item_count(bf_container)


def _apply_table_style(table, num_rows: int, num_cols: int, header_row: int = 0):
    """Apply Korean teacher-style borders, shading, and margins to all cells."""
    for ri in range(num_rows):
        for ci in range(num_cols):
            try:
                cell = table.cell(ri, ci)
            except Exception:
                continue
            cell_el = cell.element
            if ri == header_row:
                cell_el.set("borderFillIDRef", BORDER_FILL_HEADER)
            elif ci == 0:
                cell_el.set("borderFillIDRef", BORDER_FILL_FIRST_COL)
            else:
                cell_el.set("borderFillIDRef", BORDER_FILL_DATA)

            margin_el = cell_el.find(f"{_HP}cellMargin")
            if margin_el is not None:
                margin_el.set("left", CELL_MARGIN_LR)
                margin_el.set("right", CELL_MARGIN_LR)
                margin_el.set("top", CELL_MARGIN_TB)
                margin_el.set("bottom", CELL_MARGIN_TB)


def _setup_doc(header_text: str = "", landscape: bool = False) -> HwpxDocument:
    doc = HwpxDocument.new()
    sec = doc.sections[0]
    props = sec.properties
    if landscape:
        props.set_page_size(width=A4_H, height=A4_W)
    else:
        props.set_page_size(width=A4_W, height=A4_H)
    props.set_page_margins(
        top=MARGIN_TOP, bottom=MARGIN_BOTTOM,
        left=MARGIN_LEFT, right=MARGIN_RIGHT,
        header=MARGIN_HEADER, footer=MARGIN_FOOTER,
    )
    if header_text:
        try:
            props.set_header_text(header_text)
        except Exception:
            pass
    _register_border_fills(doc)
    return doc


def _bold_para(doc, text: str):
    p = doc.add_paragraph(text)
    for r in p.runs:
        r.bold = True
    return p


def _cell_bold(table, row, col, text):
    table.set_cell_text(row, col, text)
    cell = table.cell(row, col)
    for p in cell.paragraphs:
        for r in p.runs:
            r.bold = True


def _cell_multiline(table, row, col, lines):
    if isinstance(lines, list):
        text = "\n".join(lines)
    else:
        text = str(lines)
    table.set_cell_text(row, col, text)


# ===========================================================================
# Template generators
# ===========================================================================

def gen_curriculum_progress(doc: HwpxDocument, data: dict):
    """교과 진도표"""
    year = data.get("year", "")
    semester = data.get("semester", "")
    grade = data.get("grade", "")
    subject = data.get("subject", "")
    units = data.get("units", [])

    _bold_para(doc, f"{year}학년도 {semester}학기 교과 진도표")
    p = doc.add_paragraph(f"{grade}학년 | 교과: {subject}")

    headers = ["단원", "단원명", "배당 주", "차시", "학습 내용", "교과서"]
    num_rows = 1 + len(units)
    table = doc.add_table(rows=num_rows, cols=len(headers))

    for ci, h in enumerate(headers):
        _cell_bold(table, 0, ci, h)

    for ri, u in enumerate(units, start=1):
        table.set_cell_text(ri, 0, str(u.get("unit_number", "")))
        table.set_cell_text(ri, 1, u.get("unit_title", ""))
        _cell_multiline(table, ri, 2, u.get("planned_weeks", []))
        table.set_cell_text(ri, 3, str(u.get("periods", "")))
        _cell_multiline(table, ri, 4, u.get("learning_content", []))
        table.set_cell_text(ri, 5, u.get("textbook_pages", ""))

    _apply_table_style(table, num_rows, len(headers))


def gen_lesson_plan(doc: HwpxDocument, data: dict):
    """교수학습과정안"""
    subject = data.get("subject", "")
    grade = data.get("grade", "")
    unit = data.get("unit_title", "")
    lesson_num = data.get("lesson_number", "")
    total = data.get("total_lessons", "")
    date = data.get("date", "")
    period = data.get("period", "")
    competency = data.get("core_competency", "")
    teacher = data.get("teacher_name", "")
    objectives = data.get("lesson_objectives", [])
    activities = data.get("activities", [])

    _bold_para(doc, "교수·학습 과정안")

    info_table = doc.add_table(rows=4, cols=4)
    _cell_bold(info_table, 0, 0, "교과")
    info_table.set_cell_text(0, 1, subject)
    _cell_bold(info_table, 0, 2, "학년")
    info_table.set_cell_text(0, 3, f"{grade}학년")

    _cell_bold(info_table, 1, 0, "단원")
    info_table.set_cell_text(1, 1, unit)
    _cell_bold(info_table, 1, 2, "차시")
    info_table.set_cell_text(1, 3, f"{lesson_num}/{total}")

    _cell_bold(info_table, 2, 0, "일시")
    info_table.set_cell_text(2, 1, date)
    _cell_bold(info_table, 2, 2, "교시")
    info_table.set_cell_text(2, 3, str(period))

    _cell_bold(info_table, 3, 0, "핵심역량")
    info_table.set_cell_text(3, 1, competency)
    _cell_bold(info_table, 3, 2, "수업자")
    info_table.set_cell_text(3, 3, teacher)

    doc.add_paragraph("")
    _bold_para(doc, "학습 목표")
    for obj in objectives:
        doc.add_paragraph(f"• {obj}")

    doc.add_paragraph("")
    headers = ["단계", "시간(분)", "교사 활동", "학생 활동", "자료 및 유의점"]
    num_rows = 1 + len(activities)
    act_table = doc.add_table(rows=num_rows, cols=len(headers))
    for ci, h in enumerate(headers):
        _cell_bold(act_table, 0, ci, h)

    for ri, a in enumerate(activities, start=1):
        act_table.set_cell_text(ri, 0, a.get("phase", ""))
        act_table.set_cell_text(ri, 1, str(a.get("duration_min", "")))
        act_table.set_cell_text(ri, 2, a.get("teacher_activity", ""))
        act_table.set_cell_text(ri, 3, a.get("student_activity", ""))
        act_table.set_cell_text(ri, 4, a.get("materials_notes", ""))

    _apply_table_style(info_table, 4, 4, header_row=-1)
    _apply_table_style(act_table, num_rows, len(headers))


def gen_rubric(doc: HwpxDocument, data: dict):
    """평가 루브릭"""
    subject = data.get("subject", "")
    grade = data.get("grade", "")
    title = data.get("assessment_title", "")
    standard = data.get("achievement_standard", "")
    atype = data.get("assessment_type", "")
    criteria = data.get("criteria", [])

    _bold_para(doc, f"평가 루브릭 — {title}")
    doc.add_paragraph(f"{grade}학년 {subject} | {atype}")
    doc.add_paragraph(f"성취기준: {standard}")
    doc.add_paragraph("")

    headers = ["평가 기준", "배점(%)", "상", "중", "하"]
    num_rows = 1 + len(criteria)
    table = doc.add_table(rows=num_rows, cols=len(headers))
    for ci, h in enumerate(headers):
        _cell_bold(table, 0, ci, h)

    for ri, c in enumerate(criteria, start=1):
        table.set_cell_text(ri, 0, c.get("criterion", ""))
        table.set_cell_text(ri, 1, str(c.get("weight_percent", "")))
        levels = c.get("levels", {})
        table.set_cell_text(ri, 2, levels.get("상", ""))
        table.set_cell_text(ri, 3, levels.get("중", ""))
        table.set_cell_text(ri, 4, levels.get("하", ""))

    _apply_table_style(table, num_rows, len(headers))


def gen_observation_record(doc: HwpxDocument, data: dict):
    """학생 관찰 기록표"""
    class_num = data.get("class_number", "")
    subject = data.get("subject", "")
    period = data.get("observation_period", "")
    domains = data.get("domains", [])
    students = data.get("students", [])

    _bold_para(doc, "학생 관찰 기록표")
    doc.add_paragraph(f"{class_num} | {subject} | 관찰 기간: {period}")
    doc.add_paragraph("")

    headers = ["번호", "이름"] + domains + ["종합 소견"]
    num_rows = 1 + len(students)
    table = doc.add_table(rows=num_rows, cols=len(headers))
    for ci, h in enumerate(headers):
        _cell_bold(table, 0, ci, h)

    for ri, s in enumerate(students, start=1):
        table.set_cell_text(ri, 0, str(s.get("number", "")))
        table.set_cell_text(ri, 1, s.get("name", ""))
        records = s.get("records", {})
        for di, d in enumerate(domains):
            table.set_cell_text(ri, 2 + di, records.get(d, ""))
        table.set_cell_text(ri, 2 + len(domains), s.get("narrative", ""))

    _apply_table_style(table, num_rows, len(headers))


def gen_research_report(doc: HwpxDocument, data: dict):
    """연구 과제 보고서 표"""
    title = data.get("title", "")
    researcher = data.get("researcher", "")
    period = data.get("research_period", "")
    sections = data.get("sections", [])

    _bold_para(doc, title)
    doc.add_paragraph(f"연구자: {researcher} | 연구 기간: {period}")
    doc.add_paragraph("")

    for sec_data in sections:
        sec_title = sec_data.get("section_title", "")
        rows_data = sec_data.get("rows", [])
        _bold_para(doc, sec_title)

        if rows_data and "phase" in rows_data[0]:
            headers = ["단계", "기간", "추진 과제", "산출물"]
            num_rows = 1 + len(rows_data)
            table = doc.add_table(rows=num_rows, cols=len(headers))
            for ci, h in enumerate(headers):
                _cell_bold(table, 0, ci, h)
            for ri, r in enumerate(rows_data, start=1):
                table.set_cell_text(ri, 0, r.get("phase", ""))
                table.set_cell_text(ri, 1, r.get("period", ""))
                table.set_cell_text(ri, 2, r.get("task", ""))
                table.set_cell_text(ri, 3, r.get("output", ""))
            _apply_table_style(table, num_rows, len(headers))
        else:
            headers = ["구분", "내용"]
            num_rows = 1 + len(rows_data)
            table = doc.add_table(rows=num_rows, cols=len(headers))
            for ci, h in enumerate(headers):
                _cell_bold(table, 0, ci, h)
            for ri, r in enumerate(rows_data, start=1):
                table.set_cell_text(ri, 0, r.get("category", ""))
                table.set_cell_text(ri, 1, r.get("content", ""))
            _apply_table_style(table, num_rows, len(headers))

        doc.add_paragraph("")


def gen_classroom_management(doc: HwpxDocument, data: dict):
    """학급 운영 계획"""
    year = data.get("year", "")
    grade = data.get("grade", "")
    class_number = data.get("class_number", "")
    goal = data.get("class_goal", "")
    plans = data.get("monthly_plans", [])

    _bold_para(doc, f"{year}학년도 학급 운영 계획")
    doc.add_paragraph(f"{grade}학년 {class_number}반")
    doc.add_paragraph(f"학급 목표: {goal}")
    doc.add_paragraph("")

    headers = ["월", "중점 사항", "학교 행사", "학급 활동"]
    num_rows = 1 + len(plans)
    table = doc.add_table(rows=num_rows, cols=len(headers))
    for ci, h in enumerate(headers):
        _cell_bold(table, 0, ci, h)

    for ri, p in enumerate(plans, start=1):
        table.set_cell_text(ri, 0, f"{p.get('month', '')}월")
        table.set_cell_text(ri, 1, p.get("focus", ""))
        table.set_cell_text(ri, 2, p.get("events", ""))
        table.set_cell_text(ri, 3, p.get("activities", ""))

    _apply_table_style(table, num_rows, len(headers))


def gen_timetable(doc: HwpxDocument, data: dict):
    """시간표"""
    year = data.get("year", "")
    semester = data.get("semester", "")
    grade = data.get("grade", "")
    class_number = data.get("class_number", "")
    periods = data.get("periods_per_day", 6)
    lunch_after = data.get("lunch_after_period", 4)
    times = data.get("period_times", [])
    schedule = data.get("schedule", {})

    _bold_para(doc, f"{year}학년도 {semester}학기 시간표")
    doc.add_paragraph(f"{grade}학년 {class_number}반")
    doc.add_paragraph("")

    days = ["월", "화", "수", "목", "금"]
    extra_rows = 1 if lunch_after and lunch_after < periods else 0
    num_rows = 1 + periods + extra_rows
    num_cols = 2 + len(days)

    table = doc.add_table(rows=num_rows, cols=num_cols)
    _cell_bold(table, 0, 0, "교시")
    _cell_bold(table, 0, 1, "시간")
    for di, d in enumerate(days):
        _cell_bold(table, 0, 2 + di, d)

    row_idx = 1
    for pi in range(periods):
        if extra_rows and pi == lunch_after:
            _cell_bold(table, row_idx, 0, "점심")
            table.set_cell_text(row_idx, 1, "12:10-13:10")
            try:
                table.merge_cells(row_idx, 2, row_idx, num_cols - 1)
            except Exception:
                pass
            table.set_cell_text(row_idx, 2, "점심시간")
            row_idx += 1

        table.set_cell_text(row_idx, 0, str(pi + 1))
        if pi < len(times):
            table.set_cell_text(row_idx, 1, times[pi])
        for di, d in enumerate(days):
            subj_list = schedule.get(d, [])
            subj = subj_list[pi] if pi < len(subj_list) else ""
            table.set_cell_text(row_idx, 2 + di, subj)
        row_idx += 1

    _apply_table_style(table, num_rows, num_cols)


# ===========================================================================
# Generator registry
# ===========================================================================
GENERATORS = {
    "curriculum_progress": ("교과 진도표", gen_curriculum_progress, True),
    "lesson_plan": ("교수학습과정안", gen_lesson_plan, False),
    "rubric": ("평가 루브릭", gen_rubric, False),
    "observation_record": ("학생 관찰 기록표", gen_observation_record, True),
    "research_report": ("연구 과제 보고서 표", gen_research_report, False),
    "classroom_management": ("학급 운영 계획", gen_classroom_management, False),
    "timetable": ("시간표", gen_timetable, False),
}


def generate_hwpx(data: dict, output_path: str, landscape: bool = False):
    ttype = data.get("template_type", "")
    if ttype not in GENERATORS:
        print(f"ERROR: unknown template_type '{ttype}'", file=sys.stderr)
        sys.exit(1)

    korean_name, gen_fn, default_landscape = GENERATORS[ttype]
    use_landscape = landscape or default_landscape

    doc = _setup_doc(header_text=korean_name, landscape=use_landscape)
    gen_fn(doc, data)
    doc.save_to_path(output_path)
    print(f"✓ {output_path} ({korean_name})")


def main():
    parser = argparse.ArgumentParser(
        description="Korean Education Table Generator — HWPX output"
    )
    parser.add_argument("--data", type=str, required=True, help="Path to JSON input file")
    parser.add_argument("--output", "-o", type=str, required=True, help="Output .hwpx path")
    parser.add_argument("--landscape", action="store_true", help="Force landscape orientation")
    args = parser.parse_args()

    with open(args.data, "r", encoding="utf-8") as f:
        data = json.load(f)

    generate_hwpx(data, args.output, landscape=args.landscape)


if __name__ == "__main__":
    main()
