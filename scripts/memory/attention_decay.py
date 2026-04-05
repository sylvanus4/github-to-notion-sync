#!/usr/bin/env python3
"""Score MEMORY.md pointer entries with attention decay and tier them as HOT/WARM/COLD.

Scoring factors (0.0-1.0):
  - Recency:   exponential decay from entry date (half-life ~14 days)
  - Category weight: decisions/constraints decay slower than session summaries
  - Protection: architecture decisions never drop below WARM (0.35 floor)

Tiers:
  HOT  (>0.6)  — stays in MEMORY.md index
  WARM (0.3-0.6) — stays in topic file, removed from MEMORY.md
  COLD (<0.3)  — archived to memory/archive/YYYY-MM.md

Usage:
  python scripts/memory/attention_decay.py              # dry-run, show scores
  python scripts/memory/attention_decay.py --apply       # prune COLD, remove WARM from index
  python scripts/memory/attention_decay.py --max-hot 50  # keep at most 50 HOT entries
"""

import argparse
import math
import re
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MEMORY_INDEX = PROJECT_ROOT / "MEMORY.md"
ARCHIVE_DIR = PROJECT_ROOT / "memory" / "archive"

DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
CATEGORY_RE = re.compile(r"^\s*-\s*\[(\w+)\]")

CATEGORY_WEIGHTS = {
    "decision": 1.0,
    "constraint": 0.85,
    "runbook": 0.8,
    "preference": 0.9,
    "tech_debt": 0.7,
    "session_summary": 0.5,
}

DECAY_HALF_LIFE_DAYS = 14
PROTECTED_CATEGORIES = {"decision"}
PROTECTED_FLOOR = 0.35

HOT_THRESHOLD = 0.6
WARM_THRESHOLD = 0.3


def parse_entries(content: str) -> list[dict]:
    entries = []
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- ["):
            continue
        cat_match = CATEGORY_RE.match(stripped)
        date_match = DATE_RE.search(stripped)
        category = cat_match.group(1) if cat_match else "unknown"
        date_str = date_match.group(1) if date_match else None
        entries.append({
            "line": line,
            "category": category,
            "date": date_str,
        })
    return entries


def compute_score(entry: dict, now: datetime) -> float:
    cat_weight = CATEGORY_WEIGHTS.get(entry["category"], 0.5)

    if entry["date"]:
        try:
            entry_date = datetime.strptime(entry["date"], "%Y-%m-%d")
            days_old = (now - entry_date).days
        except ValueError:
            days_old = 30
    else:
        days_old = 30

    recency = math.exp(-0.693 * days_old / DECAY_HALF_LIFE_DAYS)
    score = recency * cat_weight

    if entry["category"] in PROTECTED_CATEGORIES:
        score = max(score, PROTECTED_FLOOR)

    return round(min(score, 1.0), 3)


def tier(score: float) -> str:
    if score > HOT_THRESHOLD:
        return "HOT"
    if score > WARM_THRESHOLD:
        return "WARM"
    return "COLD"


def archive_entries(cold_entries: list[dict]) -> None:
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    by_month: dict[str, list[str]] = {}
    for entry in cold_entries:
        month_key = entry["date"][:7] if entry.get("date") else "undated"
        by_month.setdefault(month_key, []).append(entry["line"].strip())

    for month, lines in by_month.items():
        archive_file = ARCHIVE_DIR / f"{month}.md"
        existing = archive_file.read_text() if archive_file.exists() else f"# Archived Memory — {month}\n"
        new_lines = [ln for ln in lines if ln not in existing]
        if new_lines:
            with open(archive_file, "a") as f:
                f.write("\n".join(new_lines) + "\n")


def run(apply: bool = False, max_hot: int = 50, verbose: bool = False) -> dict:
    if not MEMORY_INDEX.exists():
        print("MEMORY.md not found", file=sys.stderr)
        sys.exit(1)

    content = MEMORY_INDEX.read_text()
    entries = parse_entries(content)
    now = datetime.now()

    scored = []
    for entry in entries:
        score = compute_score(entry, now)
        t = tier(score)
        scored.append({**entry, "score": score, "tier": t})

    hot = [e for e in scored if e["tier"] == "HOT"]
    warm = [e for e in scored if e["tier"] == "WARM"]
    cold = [e for e in scored if e["tier"] == "COLD"]

    if len(hot) > max_hot:
        hot.sort(key=lambda e: e["score"], reverse=True)
        overflow = hot[max_hot:]
        hot = hot[:max_hot]
        warm.extend(overflow)

    stats = {
        "total": len(scored),
        "hot": len(hot),
        "warm": len(warm),
        "cold": len(cold),
        "max_hot": max_hot,
    }

    if verbose or not apply:
        print(f"\nAttention Decay Report ({now.strftime('%Y-%m-%d')})")
        print(f"{'='*60}")
        for e in sorted(scored, key=lambda x: x["score"], reverse=True):
            marker = " *PROTECTED*" if e["category"] in PROTECTED_CATEGORIES else ""
            print(f"  [{e['tier']:4s}] {e['score']:.3f} [{e['category']}] {e['date'] or 'N/A'}{marker}")
            if verbose:
                print(f"         {e['line'].strip()[:100]}")
        print(f"\nSummary: {stats['hot']} HOT, {stats['warm']} WARM, {stats['cold']} COLD")

    if apply:
        if cold:
            archive_entries(cold)
            print(f"Archived {len(cold)} COLD entries to memory/archive/")

        lines_to_keep = set()
        for e in hot:
            lines_to_keep.add(e["line"])

        new_lines = []
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("- [") and line not in lines_to_keep:
                continue
            new_lines.append(line)

        MEMORY_INDEX.write_text("\n".join(new_lines) + "\n")
        print(f"MEMORY.md pruned: kept {len(hot)} HOT entries, removed {len(warm) + len(cold)}")

    return stats


def main():
    parser = argparse.ArgumentParser(description="Score and tier memory entries by attention decay")
    parser.add_argument("--apply", action="store_true", help="Actually prune MEMORY.md and archive COLD entries")
    parser.add_argument("--max-hot", type=int, default=50, help="Maximum HOT entries to keep in index")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show entry details")
    args = parser.parse_args()
    run(apply=args.apply, max_hot=args.max_hot, verbose=args.verbose)


if __name__ == "__main__":
    main()
