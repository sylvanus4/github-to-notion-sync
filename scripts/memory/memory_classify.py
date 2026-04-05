#!/usr/bin/env python3
"""Classify a memory entry into one of 6 categories and route to the appropriate topic file.

Categories:
  session_summary — daily work summary
  decision        — architecture/tool/pattern choices
  runbook         — operational procedures, troubleshooting guides
  constraint      — workspace facts, env requirements, API quirks
  tech_debt       — known debt, structural issues
  preference      — user preferences, doc standards

Usage:
  python scripts/memory/memory_classify.py "entry text here"
  python scripts/memory/memory_classify.py --category decision "chose Option B Hybrid for multi-cluster"
  echo "entry" | python scripts/memory/memory_classify.py --stdin
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MEMORY_DIR = PROJECT_ROOT / "memory"
TOPICS_DIR = MEMORY_DIR / "topics"
MEMORY_INDEX = PROJECT_ROOT / "MEMORY.md"
HASH_FILE = MEMORY_DIR / ".cache" / "hashes.json"

CATEGORY_FILES = {
    "session_summary": None,
    "decision": MEMORY_DIR / "decisions.md",
    "runbook": TOPICS_DIR / "runbooks.md",
    "constraint": TOPICS_DIR / "workspace-facts.md",
    "tech_debt": TOPICS_DIR / "tech-debt.md",
    "preference": TOPICS_DIR / "preferences.md",
}

CATEGORY_KEYWORDS = {
    "decision": [
        "decided", "chose", "option", "architecture decision", "selected",
        "approved", "rejected", "adopt", "replaced", "switched to",
    ],
    "preference": [
        "always", "never", "prefer", "default to", "user wants",
        "respond in korean", "must be", "should be", "convention",
    ],
    "runbook": [
        "how to", "steps to", "procedure", "troubleshoot", "workaround",
        "install", "configure", "setup", "command", "cli",
    ],
    "tech_debt": [
        "debt", "todo", "hack", "workaround", "temporary", "needs refactor",
        "brittle", "broken", "flaky", "deprecat",
    ],
    "constraint": [
        "requires", "depends on", "port", "endpoint", "api", "path",
        "channel", "id", "token", "env var", "directory", "repo",
    ],
    "session_summary": [
        "session", "today", "completed", "worked on", "pipeline ran",
        "morning", "evening",
    ],
}

MAX_POINTER_LEN = 150


def load_hashes() -> dict:
    if HASH_FILE.exists():
        return json.loads(HASH_FILE.read_text())
    return {}


def save_hashes(hashes: dict) -> None:
    HASH_FILE.parent.mkdir(parents=True, exist_ok=True)
    HASH_FILE.write_text(json.dumps(hashes, indent=2, ensure_ascii=False) + "\n")


def content_hash(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text.strip().lower())
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]


def classify(text: str) -> str:
    text_lower = text.lower()
    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        scores[category] = sum(1 for kw in keywords if kw in text_lower)
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return "constraint"
    return best


def make_pointer(category: str, text: str) -> str:
    first_line = text.strip().split("\n")[0].strip()
    first_line = re.sub(r"^[-*#]+\s*", "", first_line)
    first_line = re.sub(r"^\[[\w_]+\]\s*", "", first_line)
    topic_file = CATEGORY_FILES.get(category)
    suffix = f" → {topic_file.relative_to(PROJECT_ROOT)}" if topic_file else ""
    pointer = f"[{category}] {first_line}{suffix}"
    if len(pointer) > MAX_POINTER_LEN:
        trim_to = MAX_POINTER_LEN - len(suffix) - len(f"[{category}] ") - 3
        first_line = first_line[:trim_to] + "..."
        pointer = f"[{category}] {first_line}{suffix}"
    return pointer


def append_to_topic_file(category: str, text: str) -> Path | None:
    target = CATEGORY_FILES.get(category)
    if target is None:
        return None
    target.parent.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    entry = f"\n- ({date_str}) {text.strip()}\n"
    with open(target, "a") as f:
        f.write(entry)
    return target


def append_to_index(pointer: str) -> None:
    if not MEMORY_INDEX.exists():
        MEMORY_INDEX.write_text(f"# Session Memory — Pointer Index\n\n- {pointer}\n")
        return
    content = MEMORY_INDEX.read_text()
    session_header = "## Session Summaries"
    topic_header = "## Topic Pointers"
    if session_header in content and "[session_summary]" in pointer:
        idx = content.index(session_header)
        newline_after = content.index("\n", idx) + 1
        content = content[:newline_after] + f"\n- {pointer}" + content[newline_after:]
    elif topic_header in content:
        idx = content.index(topic_header)
        newline_after = content.index("\n", idx) + 1
        content = content[:newline_after] + f"\n- {pointer}" + content[newline_after:]
    else:
        content += f"\n- {pointer}\n"
    MEMORY_INDEX.write_text(content)


def run(text: str, category: str | None = None) -> dict:
    h = content_hash(text)
    hashes = load_hashes()
    if h in hashes:
        return {"status": "duplicate", "hash": h, "original_date": hashes[h]}

    cat = category or classify(text)
    pointer = make_pointer(cat, text)
    topic_path = append_to_topic_file(cat, text)
    append_to_index(pointer)

    hashes[h] = datetime.now().strftime("%Y-%m-%d")
    save_hashes(hashes)

    return {
        "status": "classified",
        "category": cat,
        "pointer": pointer,
        "topic_file": str(topic_path.relative_to(PROJECT_ROOT)) if topic_path else None,
        "hash": h,
    }


def main():
    parser = argparse.ArgumentParser(description="Classify and route a memory entry")
    parser.add_argument("text", nargs="?", default="", help="Memory entry text")
    parser.add_argument("--category", choices=list(CATEGORY_FILES.keys()),
                        help="Override auto-classification")
    parser.add_argument("--stdin", action="store_true", help="Read from stdin")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    text = sys.stdin.read().strip() if args.stdin else args.text
    if not text:
        print("Error: no text provided", file=sys.stderr)
        sys.exit(1)

    result = run(text, category=args.category)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if result["status"] == "duplicate":
            print(f"SKIP (duplicate, first seen {result['original_date']}): hash={result['hash']}")
        else:
            print(f"Classified as [{result['category']}]")
            print(f"  Pointer: {result['pointer']}")
            if result["topic_file"]:
                print(f"  Written to: {result['topic_file']}")
            print(f"  Hash: {result['hash']}")


if __name__ == "__main__":
    main()
