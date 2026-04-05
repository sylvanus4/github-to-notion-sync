#!/usr/bin/env python3
"""Extract Cursor agent transcripts (JSONL) into structured markdown for long-term memory."""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

TRANSCRIPTS_DIR = Path.home() / ".cursor/projects/Users-hanhyojung-work-thakicloud-ai-model-event-stock-analytics/agent-transcripts"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SESSIONS_DIR = PROJECT_ROOT / "memory" / "sessions"
CACHE_DIR = PROJECT_ROOT / "memory" / ".cache"
PROCESSED_FILE = CACHE_DIR / "processed.txt"
HASH_FILE = CACHE_DIR / "hashes.json"

SYSTEM_TAG_RE = re.compile(
    r"<(?:system_reminder|attached_files|external_links|user_info|git_status|open_and_recently_viewed_files|"
    r"rules|agent_transcripts|agent_skills|available_skills|agent_requestable_workspace_rules|"
    r"always_applied_workspace_rules|always_applied_workspace_rule|agent_requestable_workspace_rule|"
    r"user_rules|user_rule|mcp_file_system|mcp_file_system_servers|mcp_file_system_server|"
    r"tone_and_style|tool_calling|making_code_changes|citing_code|terminal_files_information|"
    r"task_management|mode_selection|linter_errors|no_thinking_in_code_or_commands|"
    r"committing-changes-with-git|creating-pull-requests|managing-long-running-commands|"
    r"other-common-operations|inline_line_numbers|cursor_commands|mermaid_syntax)[^>]*>.*?</(?:system_reminder|"
    r"attached_files|external_links|user_info|git_status|open_and_recently_viewed_files|"
    r"rules|agent_transcripts|agent_skills|available_skills|agent_requestable_workspace_rules|"
    r"always_applied_workspace_rules|always_applied_workspace_rule|agent_requestable_workspace_rule|"
    r"user_rules|user_rule|mcp_file_system|mcp_file_system_servers|mcp_file_system_server|"
    r"tone_and_style|tool_calling|making_code_changes|citing_code|terminal_files_information|"
    r"task_management|mode_selection|linter_errors|no_thinking_in_code_or_commands|"
    r"committing-changes-with-git|creating-pull-requests|managing-long-running-commands|"
    r"other-common-operations|inline_line_numbers|cursor_commands|mermaid_syntax)[^>]*>",
    re.DOTALL,
)

USER_QUERY_RE = re.compile(r"<user_query>(.*?)</user_query>", re.DOTALL)
FILE_PATH_RE = re.compile(r'(?:/[a-zA-Z0-9._-]+){3,}(?:\.[a-zA-Z0-9]+)?')
SLASH_CMD_RE = re.compile(r"^\s*/[a-z-]+\s*$")


def load_processed() -> set[str]:
    if PROCESSED_FILE.exists():
        return set(PROCESSED_FILE.read_text().strip().splitlines())
    return set()


def save_processed(processed: set[str]) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_FILE.write_text("\n".join(sorted(processed)) + "\n")


def load_hashes() -> dict:
    if HASH_FILE.exists():
        return json.loads(HASH_FILE.read_text())
    return {}


def save_hashes(hashes: dict) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    HASH_FILE.write_text(json.dumps(hashes, indent=2, ensure_ascii=False) + "\n")


def content_hash(messages: list[str]) -> str:
    """SHA256 of normalized concatenated user messages for dedup."""
    normalized = " ".join(re.sub(r"\s+", " ", m.strip().lower()) for m in messages)
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]


def extract_user_query(text: str) -> str:
    """Extract content from <user_query> tags, or return cleaned text."""
    match = USER_QUERY_RE.search(text)
    if match:
        return match.group(1).strip()
    return text


def clean_message(text: str) -> str:
    """Remove system tags and extract the meaningful user content."""
    cleaned = SYSTEM_TAG_RE.sub("", text)
    cleaned = extract_user_query(cleaned) if "<user_query>" in cleaned else cleaned
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    return cleaned


def is_meaningful(text: str) -> bool:
    """Check if the message is substantive (not just a slash command or empty)."""
    if not text or len(text.strip()) < 5:
        return False
    if SLASH_CMD_RE.match(text):
        return False
    return True


def extract_title(messages: list[str], max_len: int = 80) -> str:
    """Generate a title from the first meaningful user message."""
    for msg in messages:
        text = msg.strip()
        if len(text) < 5:
            continue
        first_line = text.split("\n")[0].strip()
        first_line = re.sub(r"[#*`]", "", first_line).strip()
        if len(first_line) > max_len:
            first_line = first_line[:max_len].rsplit(" ", 1)[0] + "..."
        if first_line:
            return first_line
    return "Untitled Session"


def extract_files_touched(all_text: str) -> list[str]:
    """Extract file paths mentioned in the session."""
    paths = set()
    for match in FILE_PATH_RE.finditer(all_text):
        path = match.group(0)
        if any(path.startswith(prefix) for prefix in ["/Users/", "/tmp/", "/var/", "/etc/"]):
            continue
        parts = path.split("/")
        if any(p in ("node_modules", ".git", "__pycache__", ".cache") for p in parts):
            continue
        if path.count("/") >= 2:
            paths.add(path)
    # Also look for relative paths that look like project files
    rel_path_re = re.compile(r'(?:(?:backend|frontend|scripts|docs|\.cursor)/[a-zA-Z0-9._/-]+(?:\.[a-zA-Z0-9]+))')
    for match in rel_path_re.finditer(all_text):
        paths.add(match.group(0))
    return sorted(paths)[:20]


def process_transcript(jsonl_path: Path) -> dict | None:
    """Parse a single JSONL transcript into structured data."""
    user_messages = []
    all_text_parts = []

    with open(jsonl_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            role = obj.get("role", "")
            content_items = obj.get("message", {}).get("content", [])

            for item in content_items:
                raw_text = item.get("text", "")
                all_text_parts.append(raw_text)

                if role == "user":
                    cleaned = clean_message(raw_text)
                    if is_meaningful(cleaned):
                        user_messages.append(cleaned)

    if not user_messages:
        return None

    mtime = datetime.fromtimestamp(jsonl_path.stat().st_mtime)
    session_id = jsonl_path.stem
    title = extract_title(user_messages)
    full_text = "\n".join(all_text_parts)
    files_touched = extract_files_touched(full_text)

    return {
        "date": mtime.strftime("%Y-%m-%d"),
        "time": mtime.strftime("%H%M"),
        "session_id": session_id,
        "title": title,
        "messages": user_messages,
        "message_count": len(user_messages),
        "files_touched": files_touched,
    }


def write_session_md(data: dict) -> Path:
    """Write extracted session data as a markdown file."""
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"{data['date']}-{data['time']}-{data['session_id'][:8]}.md"
    filepath = SESSIONS_DIR / filename

    files_yaml = "\n".join(f"  - {f}" for f in data["files_touched"]) if data["files_touched"] else "  []"

    frontmatter = f"""---
date: {data['date']}
session_id: {data['session_id']}
title: "{data['title'].replace('"', '\\"')}"
type: session-log
messages: {data['message_count']}
files_touched:
{files_yaml}
---"""

    body_parts = []
    for i, msg in enumerate(data["messages"], 1):
        body_parts.append(f"### Message {i}\n\n{msg}")

    content = frontmatter + "\n\n" + "\n\n".join(body_parts) + "\n"
    filepath.write_text(content)
    return filepath


def run(incremental: bool = True, verbose: bool = False) -> None:
    if not TRANSCRIPTS_DIR.exists():
        print(f"Transcripts directory not found: {TRANSCRIPTS_DIR}", file=sys.stderr)
        sys.exit(1)

    processed = load_processed() if incremental else set()
    hashes = load_hashes()
    transcript_dirs = sorted(TRANSCRIPTS_DIR.iterdir())

    new_count = 0
    skip_count = 0
    dedup_count = 0
    error_count = 0

    for tdir in transcript_dirs:
        if not tdir.is_dir():
            continue
        uuid = tdir.name
        if uuid in processed:
            skip_count += 1
            continue

        jsonl_path = tdir / f"{uuid}.jsonl"
        if not jsonl_path.exists():
            continue

        try:
            data = process_transcript(jsonl_path)
            if data is None:
                if verbose:
                    print(f"  SKIP (no user messages): {uuid[:8]}")
                processed.add(uuid)
                continue

            h = content_hash(data["messages"])
            if h in hashes:
                if verbose:
                    print(f"  DEDUP (hash={h}, original={hashes[h]}): {uuid[:8]}")
                processed.add(uuid)
                dedup_count += 1
                continue

            filepath = write_session_md(data)
            processed.add(uuid)
            hashes[h] = uuid[:8]
            new_count += 1
            if verbose:
                print(f"  OK: {filepath.name} ({data['message_count']} messages)")
        except Exception as e:
            error_count += 1
            print(f"  ERROR processing {uuid[:8]}: {e}", file=sys.stderr)

    save_processed(processed)
    save_hashes(hashes)
    print(f"\nExtraction complete: {new_count} new, {skip_count} skipped, {dedup_count} deduped, {error_count} errors")


def main():
    parser = argparse.ArgumentParser(description="Extract Cursor agent transcripts into markdown")
    parser.add_argument("--incremental", action="store_true", default=True,
                        help="Only process new transcripts (default)")
    parser.add_argument("--full", action="store_true",
                        help="Reprocess all transcripts")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show per-file progress")
    args = parser.parse_args()

    incremental = not args.full
    run(incremental=incremental, verbose=args.verbose)


if __name__ == "__main__":
    main()
