#!/usr/bin/env python3
"""Extract SFT JSONL from Claude Code session transcripts.

Walks ~/.claude/projects/<encoded-repo>/*.jsonl, normalizes each (user, assistant)
pair into a chat-format example, preserves tool_use / tool_result blocks, and
writes to outputs/training-data/sft/<session-uuid>.jsonl.

Mechanical / no LLM API calls.

Usage:
    python3 extract_sft.py --since 7d
    python3 extract_sft.py --since 2026-04-25
    python3 extract_sft.py --session <uuid>
    python3 extract_sft.py --discover           # just list candidates
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(Path(__file__).parent))
from redact import redact_obj  # noqa: E402

DEFAULT_PROJECTS_DIR = Path.home() / ".claude" / "projects"


def encode_repo_path(repo_root: Path) -> str:
    """Claude Code encodes repo paths as `-Users-foo-bar-baz`."""
    s = str(repo_root)
    return s.replace("/", "-")


def parse_since(s: str) -> datetime:
    if s == "last-session":
        return datetime.fromtimestamp(0, tz=timezone.utc)  # caller picks newest
    if re.match(r"^\d+d$", s):
        days = int(s[:-1])
        return datetime.now(timezone.utc) - timedelta(days=days)
    if re.match(r"^\d{4}-\d{2}-\d{2}$", s):
        return datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    raise ValueError(f"unrecognized --since: {s!r} (use Nd, YYYY-MM-DD, or last-session)")


def discover(projects_dir: Path, repo_root: Path, since: datetime) -> list[Path]:
    encoded = encode_repo_path(repo_root)
    proj = projects_dir / encoded
    if not proj.exists():
        print(f"WARN: project dir not found: {proj}", file=sys.stderr)
        return []
    out = []
    for p in sorted(proj.glob("*.jsonl"), key=lambda x: x.stat().st_mtime, reverse=True):
        mtime = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc)
        if mtime >= since:
            out.append(p)
    return out


def normalize_content(c) -> list:
    """Normalize content to a list of blocks. String → [{type:text,text:...}]."""
    if c is None:
        return []
    if isinstance(c, str):
        return [{"type": "text", "text": c}]
    if isinstance(c, list):
        return c
    return [{"type": "text", "text": str(c)}]


def is_pure_text(blocks: list) -> bool:
    return all(b.get("type") == "text" for b in blocks)


def text_concat(blocks: list) -> str:
    return "\n".join(b.get("text", "") for b in blocks if b.get("type") == "text")


def extract_examples_from_session(jsonl_path: Path, max_turns: int = 20,
                                  redact: bool = True) -> tuple[list[dict], dict]:
    """Read one session jsonl, emit a list of SFT examples (chunked).

    Returns (examples, redaction_hits).
    """
    msgs: list[dict] = []  # ordered (role, content_blocks) entries
    system: str | None = None

    with jsonl_path.open(encoding="utf-8") as f:
        for line in f:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            t = rec.get("type")
            if t in ("user", "assistant"):
                m = rec.get("message", {})
                role = m.get("role")
                content = normalize_content(m.get("content"))
                if not content:
                    continue
                msgs.append({"role": role, "content": content})
            elif t == "system" and system is None:
                # First system record (subtype=local_command etc) — ignore for now;
                # the real system prompt is injected by the harness, not stored here
                pass

    if not msgs:
        return [], {}

    # Chunk into windows of max_turns (a "turn" = one user + one assistant pair, roughly)
    # Simpler: chunk by message count = max_turns * 2
    examples = []
    window = max_turns * 2
    for start in range(0, len(msgs), window):
        chunk = msgs[start:start + window]
        if len(chunk) < 2:
            continue
        # Ensure chunk starts with user (drop leading orphan assistant)
        while chunk and chunk[0]["role"] != "user":
            chunk = chunk[1:]
        if not chunk:
            continue
        n_tool = sum(
            1 for m in chunk if m["role"] == "assistant"
            for b in m["content"] if b.get("type") == "tool_use"
        )
        ex = {
            "id": f"{jsonl_path.stem}:w{start // window}",
            "system": system,
            "messages": chunk,
            "metadata": {
                "source_session": jsonl_path.stem,
                "n_messages": len(chunk),
                "n_tool_calls": n_tool,
                "captured_at": datetime.fromtimestamp(
                    jsonl_path.stat().st_mtime, tz=timezone.utc
                ).isoformat(),
            },
        }
        examples.append(ex)

    total_hits: dict = {}
    if redact:
        redacted_examples = []
        for ex in examples:
            r, h = redact_obj(ex)
            redacted_examples.append(r)
            for k, v in h.items():
                total_hits[k] = total_hits.get(k, 0) + v
        examples = redacted_examples

    return examples, total_hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--projects-dir", default=str(DEFAULT_PROJECTS_DIR))
    ap.add_argument("--repo-root", default=str(REPO_ROOT))
    ap.add_argument("--since", default="7d", help="Nd | YYYY-MM-DD | last-session")
    ap.add_argument("--session", help="Specific session UUID (overrides --since)")
    ap.add_argument("--output", default=str(REPO_ROOT / "outputs" / "training-data" / "sft"))
    ap.add_argument("--max-turns-per-example", type=int, default=20)
    ap.add_argument("--no-redact", action="store_true")
    ap.add_argument("--discover", action="store_true",
                    help="List candidate jsonl files, don't extract")
    args = ap.parse_args()

    projects_dir = Path(args.projects_dir)
    repo_root = Path(args.repo_root)
    since = parse_since(args.since)
    out_dir = Path(args.output)

    if args.session:
        candidates = [projects_dir / encode_repo_path(repo_root) / f"{args.session}.jsonl"]
        candidates = [c for c in candidates if c.exists()]
    else:
        candidates = discover(projects_dir, repo_root, since)
        if args.since == "last-session" and candidates:
            candidates = [candidates[0]]

    if args.discover:
        print(f"projects_dir: {projects_dir}")
        print(f"repo_root: {repo_root}")
        print(f"since: {args.since} → {since.isoformat()}")
        print(f"candidates: {len(candidates)}")
        for p in candidates:
            mtime = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc)
            try:
                with p.open() as f:
                    n_lines = sum(1 for _ in f)
            except Exception:
                n_lines = -1
            print(f"  {p.name}  {p.stat().st_size:>10,} bytes  {n_lines:>5} lines  mtime={mtime.isoformat()}")
        return 0

    if not candidates:
        print("no candidates matched --since filter", file=sys.stderr)
        return 1

    out_dir.mkdir(parents=True, exist_ok=True)
    index = []
    total_examples = 0
    total_hits: dict = {}

    for p in candidates:
        examples, hits = extract_examples_from_session(
            p, max_turns=args.max_turns_per_example, redact=not args.no_redact,
        )
        if not examples:
            print(f"  skip {p.name} (no extractable msgs)")
            continue
        out_path = out_dir / f"{p.stem}.jsonl"
        with out_path.open("w", encoding="utf-8") as f:
            for ex in examples:
                f.write(json.dumps(ex, ensure_ascii=False) + "\n")
        total_examples += len(examples)
        for k, v in hits.items():
            total_hits[k] = total_hits.get(k, 0) + v
        n_msgs = sum(len(ex["messages"]) for ex in examples)
        n_tool = sum(ex["metadata"]["n_tool_calls"] for ex in examples)
        index.append({
            "session": p.stem,
            "examples": len(examples),
            "n_messages": n_msgs,
            "n_tool_calls": n_tool,
            "out": str(out_path.relative_to(REPO_ROOT)),
        })
        print(f"  {p.stem}: {len(examples)} examples ({n_msgs} msgs, {n_tool} tool calls)")

    (out_dir / "_index.json").write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "since": args.since,
        "repo_root": str(repo_root),
        "total_examples": total_examples,
        "redaction_hits": total_hits,
        "sessions": index,
    }, indent=2, ensure_ascii=False))

    print(f"\nwrote {total_examples} examples across {len(index)} sessions to {out_dir}")
    if total_hits:
        print(f"redactions: {total_hits}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
