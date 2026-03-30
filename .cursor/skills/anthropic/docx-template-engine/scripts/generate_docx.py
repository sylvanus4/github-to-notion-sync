#!/usr/bin/env python3
"""
Populate a DOCX template with content from a JSON spec.
Clones the template, replaces {{SLOT}} markers in the document XML,
and handles table slot replacement.

Usage:
  generate_docx.py <template.docx> <spec.json> <output.docx>
"""

import json
import re
import shutil
import sys
import zipfile
import os
import tempfile
import xml.etree.ElementTree as ET

NSMAP = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}

# Register namespaces to prevent ns0: prefixes
for prefix, uri in NSMAP.items():
    ET.register_namespace(prefix, uri)
ET.register_namespace("mc", "http://schemas.openxmlformats.org/markup-compatibility/2006")
ET.register_namespace("o", "urn:schemas-microsoft-com:office:office")
ET.register_namespace("m", "http://schemas.openxmlformats.org/officeDocument/2006/math")
ET.register_namespace("v", "urn:schemas-microsoft-com:vml")
ET.register_namespace("wp", "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing")
ET.register_namespace("a", "http://schemas.openxmlformats.org/drawingml/2006/main")
ET.register_namespace("wps", "http://schemas.microsoft.com/office/word/2010/wordprocessingShape")


def _xml_escape(text: str) -> str:
    """Escape XML special characters in text content."""
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    text = text.replace("'", "&apos;")
    return text


def _replace_text_in_xml(xml_content: str, replacements: dict) -> str:
    """Replace {{SLOT}} markers in XML text nodes."""
    for key, value in replacements.items():
        marker = f"{{{{{key}}}}}"
        if isinstance(value, list):
            value = "\n".join(str(v) for v in value)
        xml_content = xml_content.replace(marker, _xml_escape(str(value)))
    return xml_content


def _build_table_rows_xml(table_data: dict) -> str:
    """Build OOXML table rows from table spec data."""
    rows_xml = []
    ns = NSMAP["w"]

    for row in table_data.get("rows", []):
        cells_xml = []
        for cell_val in row:
            cells_xml.append(
                f'<w:tc xmlns:w="{ns}">'
                f'<w:p><w:r><w:t>{cell_val}</w:t></w:r></w:p>'
                f'</w:tc>'
            )
        rows_xml.append(f'<w:tr xmlns:w="{ns}">{"".join(cells_xml)}</w:tr>')

    return "".join(rows_xml)


def generate(template_path: str, spec_path: str, output_path: str):
    with open(spec_path, "r") as f:
        spec = json.load(f)

    # Build text replacements from sections
    replacements = {}
    for section in spec.get("sections", []):
        slot = section.get("slot", "")
        content = section.get("content", "")
        if slot:
            replacements[slot] = content

    # Add metadata replacements
    if "document_title" in spec:
        replacements.setdefault("COVER_TITLE", spec["document_title"])
    metadata = spec.get("metadata", {})
    if "subtitle" in metadata:
        replacements.setdefault("COVER_SUBTITLE", metadata["subtitle"])

    # Handle table replacements - replace marker rows
    table_specs = {}
    for table in spec.get("tables", []):
        slot = table.get("slot", "")
        if slot:
            # For table markers, we replace the placeholder text row
            for i, row in enumerate(table.get("rows", [])):
                for j, cell in enumerate(row):
                    replacements[f"{slot.replace('_TABLE', '')}_{i+1}"] = cell
                    # Also handle indexed markers like RISK_1, IMPACT_1, MITIGATION_1
                    headers = table.get("headers", [])
                    if j < len(headers):
                        replacements[f"{headers[j].upper()}_{i+1}"] = cell

    # Copy template and modify
    shutil.copy2(template_path, output_path)

    with zipfile.ZipFile(output_path, "r") as zin:
        file_contents = {}
        for name in zin.namelist():
            file_contents[name] = zin.read(name)

    # Replace in document.xml
    if "word/document.xml" in file_contents:
        doc_xml = file_contents["word/document.xml"].decode("utf-8")
        doc_xml = _replace_text_in_xml(doc_xml, replacements)
        file_contents["word/document.xml"] = doc_xml.encode("utf-8")

    # Write modified zip
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, content in file_contents.items():
            zout.writestr(name, content)

    # Report
    filled_slots = [k for k in replacements.keys() if not k.startswith("RISK") and not k.startswith("IMPACT") and not k.startswith("MITIGATION")]
    print(json.dumps({
        "status": "success",
        "output": output_path,
        "slots_filled": len(replacements),
        "replacement_keys": list(replacements.keys()),
    }, indent=2))


def main():
    if len(sys.argv) < 4:
        print("Usage: generate_docx.py <template.docx> <spec.json> <output.docx>", file=sys.stderr)
        sys.exit(1)
    generate(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()
