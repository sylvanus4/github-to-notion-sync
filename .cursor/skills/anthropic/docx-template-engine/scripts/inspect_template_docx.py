#!/usr/bin/env python3
"""
Inspect a DOCX template: extract styles, bookmarks, placeholder markers
({{...}}), header/footer content, and section structure. Outputs JSON to stdout.
"""

import json
import sys
import zipfile
import xml.etree.ElementTree as ET

NSMAP = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def _find_text(elem):
    """Extract all text from an element and its children."""
    texts = []
    for t in elem.iter(f'{{{NSMAP["w"]}}}t'):
        if t.text:
            texts.append(t.text)
    return "".join(texts)


def inspect(docx_path: str) -> dict:
    result = {
        "file": docx_path,
        "styles": [],
        "bookmarks": [],
        "placeholder_markers": [],
        "headings": [],
        "sections": [],
        "headers": [],
        "footers": [],
    }

    with zipfile.ZipFile(docx_path, "r") as zf:
        # Extract styles
        if "word/styles.xml" in zf.namelist():
            tree = ET.parse(zf.open("word/styles.xml"))
            root = tree.getroot()
            for style in root.findall(f'{{{NSMAP["w"]}}}style'):
                style_id = style.get(f'{{{NSMAP["w"]}}}styleId', "")
                style_type = style.get(f'{{{NSMAP["w"]}}}type', "")
                name_elem = style.find(f'{{{NSMAP["w"]}}}name')
                name = name_elem.get(f'{{{NSMAP["w"]}}}val', "") if name_elem is not None else style_id
                result["styles"].append({
                    "id": style_id,
                    "name": name,
                    "type": style_type,
                })

        # Extract document.xml content
        if "word/document.xml" in zf.namelist():
            tree = ET.parse(zf.open("word/document.xml"))
            root = tree.getroot()

            # Bookmarks
            for bm_start in root.iter(f'{{{NSMAP["w"]}}}bookmarkStart'):
                bm_name = bm_start.get(f'{{{NSMAP["w"]}}}name', "")
                if bm_name and bm_name != "_GoBack":
                    result["bookmarks"].append(bm_name)

            # Placeholder markers and headings
            for para in root.iter(f'{{{NSMAP["w"]}}}p'):
                text = _find_text(para)
                if "{{" in text and "}}" in text:
                    import re
                    markers = re.findall(r'\{\{(\w+)\}\}', text)
                    result["placeholder_markers"].extend(markers)

                ppr = para.find(f'{{{NSMAP["w"]}}}pPr')
                if ppr is not None:
                    pstyle = ppr.find(f'{{{NSMAP["w"]}}}pStyle')
                    if pstyle is not None:
                        val = pstyle.get(f'{{{NSMAP["w"]}}}val', "")
                        if val.startswith("Heading") or val == "Title":
                            result["headings"].append({
                                "style": val,
                                "text": text[:100],
                            })

            # Sections
            for sectPr in root.iter(f'{{{NSMAP["w"]}}}sectPr'):
                section = {"type": "section"}
                pgSz = sectPr.find(f'{{{NSMAP["w"]}}}pgSz')
                if pgSz is not None:
                    section["page_width"] = pgSz.get(f'{{{NSMAP["w"]}}}w', "")
                    section["page_height"] = pgSz.get(f'{{{NSMAP["w"]}}}h', "")
                result["sections"].append(section)

        # Headers and footers
        for name in zf.namelist():
            if name.startswith("word/header"):
                tree = ET.parse(zf.open(name))
                text = _find_text(tree.getroot())
                if text.strip():
                    result["headers"].append({"file": name, "text": text.strip()[:200]})
            elif name.startswith("word/footer"):
                tree = ET.parse(zf.open(name))
                text = _find_text(tree.getroot())
                if text.strip():
                    result["footers"].append({"file": name, "text": text.strip()[:200]})

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: inspect_template_docx.py <file.docx>", file=sys.stderr)
        sys.exit(1)

    data = inspect(sys.argv[1])
    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
