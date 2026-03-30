#!/usr/bin/env python3
"""Convert markdown pipe tables to Notion HTML <table> blocks and strip H1 title.

Usage:
    python convert_for_notion.py <file.md> [file2.md ...]

Outputs converted content to stdout (single file) or writes to
<outdir>/notion_<basename>.md (multiple files via --outdir).

Preserves:
  - Tables inside fenced code blocks (```)
  - Mermaid diagram blocks
  - All non-table content
"""

import re
import sys
from pathlib import Path


def _parse_row(line: str) -> list[str]:
    """Split a pipe-delimited row into cell contents."""
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def _is_separator(line: str) -> bool:
    """Check if a line is a markdown table separator (|---|---|)."""
    stripped = line.strip()
    return bool(stripped) and all(c in "-| :" for c in stripped)


def convert_pipe_tables(content: str) -> str:
    """Transform markdown pipe tables into Notion <table> HTML blocks.

    Tables inside fenced code blocks are preserved unchanged.
    """
    lines = content.split("\n")
    result: list[str] = []
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
            "|" in line
            and line.strip().startswith("|")
            and line.strip().endswith("|")
        ):
            table_lines: list[str] = []
            while (
                i < len(lines)
                and lines[i].strip().startswith("|")
                and lines[i].strip().endswith("|")
            ):
                table_lines.append(lines[i])
                i += 1

            if len(table_lines) >= 2:
                header_cells = _parse_row(table_lines[0])

                has_header = len(table_lines) >= 2 and _is_separator(
                    table_lines[1]
                )

                data_start = 2 if has_header else 1

                html = (
                    f'<table header-row="{"true" if has_header else "false"}">\n'
                )

                if has_header:
                    html += "\t<tr>\n"
                    for cell in header_cells:
                        html += f"\t\t<td>**{cell}**</td>\n"
                    html += "\t</tr>\n"

                for data_line in table_lines[data_start:]:
                    cells = _parse_row(data_line)
                    html += "\t<tr>\n"
                    for cell in cells:
                        html += f"\t\t<td>{cell}</td>\n"
                    html += "\t</tr>\n"

                html += "</table>"
                result.append(html)
            else:
                result.extend(table_lines)
        else:
            result.append(line)
            i += 1

    return "\n".join(result)


def extract_and_remove_h1(content: str) -> tuple[str, str]:
    """Extract the first H1 title and return (title, body_without_h1)."""
    lines = content.split("\n")
    title = ""
    body_lines: list[str] = []
    found_h1 = False

    for line in lines:
        if not found_h1 and line.startswith("# ") and not line.startswith("## "):
            title = line[2:].strip()
            found_h1 = True
            continue
        body_lines.append(line)

    while body_lines and body_lines[0].strip() == "":
        body_lines.pop(0)

    return title, "\n".join(body_lines)


def process_file(filepath: str) -> tuple[str, str]:
    """Read a markdown file and return (title, converted_body)."""
    content = Path(filepath).read_text(encoding="utf-8")
    title, body = extract_and_remove_h1(content)

    if not title:
        title = Path(filepath).stem.replace("-", " ").replace("_", " ").title()

    converted = convert_pipe_tables(body)
    return title, converted


def main() -> None:
    import tempfile

    outdir = ""
    files: list[str] = []
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--outdir" and i + 1 < len(sys.argv):
            outdir = sys.argv[i + 1]
            i += 2
        else:
            files.append(sys.argv[i])
            i += 1

    if not files:
        print(
            "Usage: convert_for_notion.py [--outdir DIR] <file.md> [file2.md ...]",
            file=sys.stderr,
        )
        sys.exit(1)

    if len(files) == 1 and not outdir:
        _title, body = process_file(files[0])
        print(body)
    else:
        if not outdir:
            outdir = tempfile.mkdtemp(prefix="notion-upload-")
        Path(outdir).mkdir(parents=True, exist_ok=True)
        print(f"OUTDIR={outdir}")

        for filepath in files:
            title, body = process_file(filepath)
            out_name = Path(filepath).stem
            out_path = Path(outdir) / f"notion_{out_name}.md"
            out_path.write_text(body, encoding="utf-8")
            print(f"[OK] {title} → {out_path}")


if __name__ == "__main__":
    main()
