# DOCX Code Patterns — Korean Teacher-Style Tables

Reference patterns for inline `python-docx` generation when `edu_table_generator.py` is unavailable.

## Constants

```python
from docx import Document
from docx.shared import Pt, Mm
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BORDER_OUTER_SZ = 12       # 1.5pt (half-points)
BORDER_HEADER_BOTTOM = 8   # 1.0pt
BORDER_INNER_H = 4         # 0.5pt horizontal
BORDER_INNER_V = 2         # 0.25pt vertical
COLOR_HEADER_BG = "F2F2F2"
COLOR_FIRST_COL = "F9F9F9"
```

## Page Setup

```python
doc = Document()
section = doc.sections[0]
for attr in ("page_width", "page_height"):
    setattr(section, attr, Mm(210 if "width" in attr else 297))
for attr in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
    setattr(section, attr, Mm(20))
```

## Table Borders

```python
table = doc.add_table(rows=R, cols=C)
table.alignment = WD_TABLE_ALIGNMENT.CENTER

borders = OxmlElement("w:tblBorders")
for edge in ("top", "left", "bottom", "right"):
    el = OxmlElement(f"w:{edge}")
    el.set(qn("w:sz"), str(BORDER_OUTER_SZ))
    el.set(qn("w:val"), "single")
    el.set(qn("w:color"), "000000")
    borders.append(el)
# Thin inner lines — horizontal visible, vertical minimal
for edge, sz, color in [("insideH", BORDER_INNER_H, "808080"),
                         ("insideV", BORDER_INNER_V, "BFBFBF")]:
    el = OxmlElement(f"w:{edge}")
    el.set(qn("w:sz"), str(sz))
    el.set(qn("w:val"), "single")
    el.set(qn("w:color"), color)
    borders.append(el)
table._tbl.tblPr.append(borders)
```

## Cell Margins

```python
def set_cell_margins(cell):
    margins = OxmlElement("w:tcMar")
    for edge, val in [("top", 120), ("bottom", 120),
                      ("start", 160), ("end", 160)]:
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:w"), str(val))
        el.set(qn("w:type"), "dxa")
        margins.append(el)
    cell._tc.get_or_add_tcPr().append(margins)
```
