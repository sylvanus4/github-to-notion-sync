#!/usr/bin/env python3
"""Split base-image Notion body into chunked payloads for MCP upload."""
import json
import re
from pathlib import Path

SPEC = Path(__file__).resolve().parent / "notion-upload-base-image-spec.json"
OUT_DIR = Path(__file__).resolve().parent
MARKER_LINE = "<<<NOTION_APPEND>>>"
MARKER = f"\n\n{MARKER_LINE}\n"


def main() -> None:
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    body = spec["pages"][0]["content"]
    parts = re.split(r"(?=\n## )", body)
    merged: list[str] = []
    buf = ""
    for p in parts:
        if len(buf) + len(p) < 7000:
            buf += p
        else:
            if buf:
                merged.append(buf)
            buf = p
    if buf:
        merged.append(buf)

    parent = spec["parent"]
    title = spec["pages"][0]["properties"]["title"]

    create_payload = {
        "parent": parent,
        "pages": [{"properties": {"title": title}, "content": merged[0] + MARKER}],
    }
    (OUT_DIR / "notion-base-chunk-create.json").write_text(
        json.dumps(create_payload, ensure_ascii=False), encoding="utf-8"
    )

    for idx, chunk in enumerate(merged[1:], start=1):
        is_last = idx == len(merged) - 1
        tail = "" if is_last else MARKER
        upd = {
            "page_id": "PLACEHOLDER_PAGE_ID",
            "command": "update_content",
            "content_updates": [
                {
                    "old_str": MARKER_LINE,
                    "new_str": MARKER_LINE + "\n\n" + chunk + tail,
                }
            ],
        }
        (OUT_DIR / f"notion-base-chunk-update-{idx}.json").write_text(
            json.dumps(upd, ensure_ascii=False), encoding="utf-8"
        )

    print("chunks", len(merged), "lens", [len(x) for x in merged])
    print("create_bytes", (OUT_DIR / "notion-base-chunk-create.json").stat().st_size)


if __name__ == "__main__":
    main()
