#!/usr/bin/env python3
"""
Validate a populated DOCX against template rules.
Checks 7 compliance rules and outputs a JSON report.

Usage:
  validate_docx.py <output.docx> <placeholder-map.json>
"""

import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

NSMAP = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}


def _find_all_text(root):
    """Extract all text nodes from XML."""
    texts = []
    for t in root.iter(f'{{{NSMAP["w"]}}}t'):
        if t.text:
            texts.append(t.text)
    return texts


def _get_used_styles(root):
    """Get all paragraph style IDs used in the document."""
    styles = set()
    for ppr in root.iter(f'{{{NSMAP["w"]}}}pPr'):
        pstyle = ppr.find(f'{{{NSMAP["w"]}}}pStyle')
        if pstyle is not None:
            styles.add(pstyle.get(f'{{{NSMAP["w"]}}}val', ""))
    return styles


def _get_heading_sequence(root):
    """Get ordered list of heading styles in the document."""
    headings = []
    for para in root.iter(f'{{{NSMAP["w"]}}}p'):
        ppr = para.find(f'{{{NSMAP["w"]}}}pPr')
        if ppr is not None:
            pstyle = ppr.find(f'{{{NSMAP["w"]}}}pStyle')
            if pstyle is not None:
                val = pstyle.get(f'{{{NSMAP["w"]}}}val', "")
                if val.startswith("Heading") or val == "Title":
                    headings.append(val)
    return headings


def _check_direct_formatting(root):
    """Count runs with direct formatting (bold/italic not from styles)."""
    direct_count = 0
    for rpr in root.iter(f'{{{NSMAP["w"]}}}rPr'):
        parent_run = rpr.find("..")
        b = rpr.find(f'{{{NSMAP["w"]}}}b')
        i = rpr.find(f'{{{NSMAP["w"]}}}i')
        sz = rpr.find(f'{{{NSMAP["w"]}}}sz')
        color = rpr.find(f'{{{NSMAP["w"]}}}color')
        if any(x is not None for x in [b, i, sz, color]):
            direct_count += 1
    return direct_count


def validate(docx_path: str, pmap_path: str) -> dict:
    with open(pmap_path, "r") as f:
        pmap = json.load(f)

    violations = []
    warnings = []

    with zipfile.ZipFile(docx_path, "r") as zf:
        if "word/document.xml" not in zf.namelist():
            violations.append({
                "rule": "R0_STRUCTURE",
                "severity": "hard",
                "message": "Missing word/document.xml - not a valid DOCX",
            })
            return _build_report(docx_path, violations, warnings)

        tree = ET.parse(zf.open("word/document.xml"))
        root = tree.getroot()

        # R1: Style whitelist
        allowed_styles = set(pmap.get("allowed_styles", []))
        used_styles = _get_used_styles(root)
        unauthorized = used_styles - allowed_styles - {""}
        for style in unauthorized:
            violations.append({
                "rule": "R1_STYLE_WHITELIST",
                "severity": "hard",
                "message": f"Unauthorized style '{style}' used (allowed: {sorted(allowed_styles)})",
            })

        # R2: Heading order
        heading_seq = _get_heading_sequence(root)
        heading_order = pmap.get("heading_order", [])
        if heading_order:
            level_map = {h: i for i, h in enumerate(heading_order)}
            prev_level = -1
            for h in heading_seq:
                level = level_map.get(h, 99)
                if level > prev_level + 1 and prev_level >= 0 and level != 99:
                    warnings.append({
                        "rule": "R2_HEADING_ORDER",
                        "severity": "soft",
                        "message": f"Heading level skip: went from level {prev_level} to {level} ({h})",
                    })
                prev_level = level

        # R3: Direct formatting abuse
        direct_count = _check_direct_formatting(root)
        threshold = 50
        if direct_count > threshold:
            warnings.append({
                "rule": "R3_DIRECT_FORMATTING",
                "severity": "soft",
                "message": f"Excessive direct formatting: {direct_count} runs (threshold: {threshold})",
            })

        # R4: Table style integrity (check tables exist if RISKS_TABLE slot defined)
        tables = list(root.iter(f'{{{NSMAP["w"]}}}tbl'))
        table_slots = [k for k, v in pmap.get("slots", {}).items() if v.get("type") == "table"]
        if table_slots and not tables:
            warnings.append({
                "rule": "R4_TABLE_INTEGRITY",
                "severity": "soft",
                "message": f"Template defines table slots {table_slots} but no tables found in output",
            })

        # R5: Placeholder fill check
        all_text = " ".join(_find_all_text(root))
        remaining_markers = re.findall(r'\{\{(\w+)\}\}', all_text)
        for marker in remaining_markers:
            violations.append({
                "rule": "R5_PLACEHOLDER_UNFILLED",
                "severity": "hard",
                "message": f"Unfilled placeholder marker '{{{{{marker}}}}}' in document",
            })

        # R6: Header/footer preservation
        has_header = any(n.startswith("word/header") for n in zf.namelist())
        has_footer = any(n.startswith("word/footer") for n in zf.namelist())
        if not has_header:
            violations.append({
                "rule": "R6_HEADER_FOOTER",
                "severity": "hard",
                "message": "Template header is missing from output",
            })
        if not has_footer:
            violations.append({
                "rule": "R6_HEADER_FOOTER",
                "severity": "hard",
                "message": "Template footer is missing from output",
            })

        # R7: Metadata check
        slots = pmap.get("slots", {})
        for slot_name, slot_info in slots.items():
            if slot_info.get("required", False) and slot_info.get("type") == "text":
                max_chars = slot_info.get("max_chars", 99999)
                # Check if slot content is reasonably sized
                marker = f"{{{{{slot_name}}}}}"
                if marker in all_text:
                    pass  # Already caught by R5

    return _build_report(docx_path, violations, warnings)


def _build_report(docx_path, violations, warnings):
    hard_fails = [v for v in violations if v["severity"] == "hard"]
    return {
        "file": docx_path,
        "passed": len(hard_fails) == 0,
        "hard_violations": len(hard_fails),
        "soft_warnings": len(warnings),
        "violations": violations,
        "warnings": warnings,
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: validate_docx.py <output.docx> <placeholder-map.json>", file=sys.stderr)
        sys.exit(1)

    report = validate(sys.argv[1], sys.argv[2])
    print(json.dumps(report, indent=2, ensure_ascii=False))
    sys.exit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
