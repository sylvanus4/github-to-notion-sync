#!/usr/bin/env python3
"""Extract weak-label preference pairs (DPO/GRPO-compatible) from transcripts.

Detects user-correction signals in turn N+1 to mark assistant turn N as
'rejected'. The next assistant attempt (after the correction) becomes 'chosen'.

Strategy A only (no LLM synthesis). For strategy B, see SKILL.md.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(Path(__file__).parent))
from redact import redact_obj  # noqa: E402
from extract_sft import (  # noqa: E402
    DEFAULT_PROJECTS_DIR, encode_repo_path, parse_since, discover, normalize_content,
)

# Korean + English correction patterns (case-insensitive)
CORRECTION_PATTERNS = [
    (re.compile(r"\b/rewind\b|\b/redo\b|\b/undo\b", re.I), "rewind"),
    (re.compile(r"^(아니|그게 아니|wrong|no[,.\s]|nope[,.\s]|정정|다시 해줘|다시 하|undo)", re.I | re.M), "user_correction"),
    (re.compile(r"잘못|이상하다|이상해|틀렸|버그|이게 아닌데|왜 이래", re.I), "explicit_negative"),
    (re.compile(r"^(다시|retry|redo)", re.I | re.M), "repeat_request"),
]


def first_text(blocks: list) -> str:
    for b in blocks:
        if b.get("type") == "text":
            return b.get("text", "")
    return ""


def detect_signal(user_text: str) -> str | None:
    if not user_text:
        return None
    # Skip very long messages (likely not corrections, just new instructions)
    if len(user_text) > 500:
        return None
    for pat, label in CORRECTION_PATTERNS:
        if pat.search(user_text):
            return label
    return None


def extract_pairs_from_session(jsonl_path: Path, redact: bool = True) -> tuple[list[dict], dict]:
    msgs: list[dict] = []
    with jsonl_path.open(encoding="utf-8") as f:
        for line in f:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("type") in ("user", "assistant"):
                m = rec.get("message", {})
                msgs.append({"role": m.get("role"), "content": normalize_content(m.get("content"))})

    pairs = []
    # Walk: find triples (user_a, assistant_a, user_b) where user_b is a correction
    # Then look for next assistant_b to use as 'chosen'
    for i in range(len(msgs) - 2):
        if msgs[i]["role"] != "user" or msgs[i + 1]["role"] != "assistant":
            continue
        if msgs[i + 2]["role"] != "user":
            continue
        ut = first_text(msgs[i + 2]["content"])
        signal = detect_signal(ut)
        if not signal:
            continue
        # Find next assistant after the correction
        chosen_idx = None
        for j in range(i + 3, min(i + 6, len(msgs))):
            if msgs[j]["role"] == "assistant":
                chosen_idx = j
                break
        if chosen_idx is None:
            continue
        prompt = first_text(msgs[i]["content"])[:2000]
        rejected = first_text(msgs[i + 1]["content"])[:3000]
        chosen = first_text(msgs[chosen_idx]["content"])[:3000]
        if not (prompt and rejected and chosen) or rejected == chosen:
            continue
        pairs.append({
            "id": f"{jsonl_path.stem}:t{i}",
            "prompt": prompt,
            "chosen": chosen,
            "rejected": rejected,
            "signal": signal,
            "correction_text": ut[:500],
            "confidence": 0.6 if signal == "user_correction" else 0.5,
        })

    total_hits: dict = {}
    if redact:
        out = []
        for p in pairs:
            r, h = redact_obj(p)
            out.append(r)
            for k, v in h.items():
                total_hits[k] = total_hits.get(k, 0) + v
        pairs = out

    return pairs, total_hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--projects-dir", default=str(DEFAULT_PROJECTS_DIR))
    ap.add_argument("--repo-root", default=str(REPO_ROOT))
    ap.add_argument("--since", default="7d")
    ap.add_argument("--session", help="Specific session UUID")
    ap.add_argument("--output", default=str(REPO_ROOT / "outputs" / "training-data" / "preference"))
    ap.add_argument("--no-redact", action="store_true")
    args = ap.parse_args()

    projects_dir = Path(args.projects_dir)
    repo_root = Path(args.repo_root)
    since = parse_since(args.since)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.session:
        candidates = [projects_dir / encode_repo_path(repo_root) / f"{args.session}.jsonl"]
        candidates = [c for c in candidates if c.exists()]
    else:
        candidates = discover(projects_dir, repo_root, since)

    total = 0
    sigs: dict = {}
    total_hits: dict = {}
    index = []

    for p in candidates:
        pairs, hits = extract_pairs_from_session(p, redact=not args.no_redact)
        if not pairs:
            continue
        out_path = out_dir / f"{p.stem}.jsonl"
        with out_path.open("w", encoding="utf-8") as f:
            for pair in pairs:
                f.write(json.dumps(pair, ensure_ascii=False) + "\n")
                sigs[pair["signal"]] = sigs.get(pair["signal"], 0) + 1
        total += len(pairs)
        for k, v in hits.items():
            total_hits[k] = total_hits.get(k, 0) + v
        index.append({"session": p.stem, "pairs": len(pairs), "out": str(out_path.relative_to(REPO_ROOT))})
        print(f"  {p.stem}: {len(pairs)} preference pairs")

    (out_dir / "_index.json").write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "since": args.since,
        "total_pairs": total,
        "by_signal": sigs,
        "redaction_hits": total_hits,
        "sessions": index,
    }, indent=2, ensure_ascii=False))

    print(f"\nwrote {total} preference pairs to {out_dir}")
    if sigs:
        print(f"by signal: {sigs}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
