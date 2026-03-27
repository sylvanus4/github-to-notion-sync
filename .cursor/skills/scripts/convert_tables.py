#!/usr/bin/env python3
"""
Prepare markdown files for Notion upload.

- Extracts H1 heading as page title
- Converts pipe tables to Notion <table> HTML blocks (code-block-aware)
- Splits large content by H2 sections when over a character threshold
- Outputs JSON with title, content, and optional split parts
"""
import json
import os
import re
import sys


def convert_pipe_tables(content: str) -> str:
    """Convert pipe tables to Notion <table> blocks, skipping code blocks."""
    lines = content.split("\n")
    result = []
    i = 0
    in_code_block = False

    while i < len(lines):
        line = lines[i]

        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            result.append(line)
            i += 1
            continue

        if in_code_block:
            result.append(line)
            i += 1
            continue

        if (
            _is_table_row(line)
            and i + 1 < len(lines)
            and _is_separator_row(lines[i + 1])
        ):
            table_lines = [line]
            j = i + 1
            while j < len(lines) and _is_table_row(lines[j]):
                table_lines.append(lines[j])
                j += 1

            result.append(_pipe_table_to_notion(table_lines))
            i = j
        else:
            result.append(line)
            i += 1

    return "\n".join(result)


def extract_title(content: str, filepath: str) -> tuple[str, str]:
    """Return (title, body_without_h1). Falls back to filename-based title."""
    lines = content.split("\n")
    for idx, line in enumerate(lines):
        if line.startswith("# ") and not line.startswith("## "):
            title = line[2:].strip()
            body = "\n".join(lines[idx + 1 :]).strip()
            return title, body

    fallback = os.path.splitext(os.path.basename(filepath))[0]
    fallback = fallback.replace("-", " ").replace("_", " ").title()
    return fallback, content.strip()


def split_by_h2(content: str, threshold: int = 15000) -> list[dict]:
    """Split content into parts by H2 headings if over threshold.

    Merges consecutive small H2 sections into chunks that stay under the
    threshold, so a 50KB doc with 16 H2s becomes ~4 parts, not 16.

    Returns a list of {"subtitle": str, "body": str} dicts.
    If content is under the threshold, returns a single-element list.
    """
    if len(content) <= threshold:
        return [{"subtitle": "", "body": content}]

    lines = content.split("\n")
    sections: list[tuple[str, int]] = []

    for i, line in enumerate(lines):
        if line.startswith("## ") and not line.startswith("### "):
            sections.append((line[3:].strip(), i))

    if len(sections) < 2:
        return [{"subtitle": "", "body": content}]

    raw_parts = []
    for idx, (heading, start) in enumerate(sections):
        end = sections[idx + 1][1] if idx + 1 < len(sections) else len(lines)
        body = "\n".join(lines[start:end])
        raw_parts.append({"subtitle": heading, "body": body})

    preamble = "\n".join(lines[: sections[0][1]]).strip()
    if preamble:
        raw_parts[0]["body"] = preamble + "\n\n" + raw_parts[0]["body"]

    merged: list[dict] = []
    current_subtitle = raw_parts[0]["subtitle"]
    current_body = raw_parts[0]["body"]

    for part in raw_parts[1:]:
        combined_len = len(current_body) + len(part["body"]) + 2
        if combined_len <= threshold:
            current_body = current_body + "\n\n" + part["body"]
        else:
            merged.append({"subtitle": current_subtitle, "body": current_body})
            current_subtitle = part["subtitle"]
            current_body = part["body"]

    merged.append({"subtitle": current_subtitle, "body": current_body})

    if len(merged) == 1:
        return [{"subtitle": "", "body": content}]

    return merged


def process_file(
    filepath: str, split_threshold: int = 15000
) -> dict:
    """Full pipeline: read file, extract title, convert tables, optionally split."""
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    title, body = extract_title(raw, filepath)
    converted = convert_pipe_tables(body)

    result: dict = {
        "title": title,
        "filepath": filepath,
        "content_length": len(converted),
    }

    parts = split_by_h2(converted, threshold=split_threshold)
    if len(parts) == 1:
        result["content"] = parts[0]["body"]
        result["split"] = False
    else:
        result["split"] = True
        result["parts"] = parts

    return result


# --- internal helpers ---


def _is_table_row(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and s.endswith("|") and s.count("|") >= 2


def _is_separator_row(line: str) -> bool:
    s = line.strip()
    if not (s.startswith("|") and s.endswith("|")):
        return False
    cells = [c.strip() for c in s.strip("|").split("|")]
    return all(re.match(r"^[-:]+$", c) for c in cells if c)


def _parse_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _pipe_table_to_notion(table_lines: list[str]) -> str:
    header = _parse_row(table_lines[0])
    data_rows = [
        _parse_row(ln) for ln in table_lines[2:] if not _is_separator_row(ln)
    ]

    out = ['<table header-row="true">']
    out.append("\t<tr>")
    for cell in header:
        out.append(f"\t\t<td>{cell}</td>")
    out.append("\t</tr>")

    for row in data_rows:
        out.append("\t<tr>")
        while len(row) < len(header):
            row.append("")
        for cell in row[: len(header)]:
            out.append(f"\t\t<td>{cell}</td>")
        out.append("\t</tr>")

    out.append("</table>")
    return "\n".join(out)


if __name__ == "__main__":
    import tempfile

    threshold = 15000
    outdir = ""
    files = []
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--threshold" and i + 1 < len(sys.argv):
            threshold = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--outdir" and i + 1 < len(sys.argv):
            outdir = sys.argv[i + 1]
            i += 2
        else:
            files.append(sys.argv[i])
            i += 1

    if not files:
        print(
            "Usage: convert_tables.py [--threshold N] [--outdir DIR] <file1.md> [file2.md ...]"
        )
        sys.exit(1)

    if not outdir:
        outdir = tempfile.mkdtemp(prefix="notion-upload-")

    os.makedirs(outdir, exist_ok=True)
    print(f"OUTDIR={outdir}")

    results = []
    for f in files:
        r = process_file(f, split_threshold=threshold)
        results.append(r)
        status = f"SPLIT into {len(r['parts'])} parts" if r["split"] else "OK"
        print(f"[{status}] {r['title']}  ({r['content_length']} chars)  ← {f}")

    for idx, r in enumerate(results):
        outfile = os.path.join(outdir, f"notion_page_{idx}.json")
        with open(outfile, "w", encoding="utf-8") as fout:
            json.dump(r, fout, ensure_ascii=False, indent=2)
        print(f"  → {outfile}")
