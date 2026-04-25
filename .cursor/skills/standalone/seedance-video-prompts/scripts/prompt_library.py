#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Seedance 2.0 Video Prompt Library CLI.

Browse, search, and discover 605+ curated video generation prompts.

Usage:
  uv run prompt_library.py search "cinematic rain"
  uv run prompt_library.py browse cinematic --limit 5
  uv run prompt_library.py by-category
  uv run prompt_library.py random --category cinematic --count 3
  uv run prompt_library.py stats
  uv run prompt_library.py show --id 13389
"""

from __future__ import annotations

import argparse
import json
import random as rand_mod
import sys
import textwrap
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"
PROMPTS_FILE = DATA_DIR / "prompts.json"
TAXONOMY_FILE = DATA_DIR / "taxonomy.json"


def _load_prompts() -> list[dict]:
    if not PROMPTS_FILE.exists():
        print(f"Error: prompts file not found: {PROMPTS_FILE}", file=sys.stderr)
        sys.exit(1)
    return json.loads(PROMPTS_FILE.read_text(encoding="utf-8"))


def _load_taxonomy() -> dict:
    if not TAXONOMY_FILE.exists():
        print(f"Error: taxonomy file not found: {TAXONOMY_FILE}", file=sys.stderr)
        sys.exit(1)
    return json.loads(TAXONOMY_FILE.read_text(encoding="utf-8"))


def _build_index(prompts: list[dict]) -> dict[int, dict]:
    return {p["id"]: p for p in prompts if "id" in p}


def _format_prompt(prompt: dict, verbose: bool = False) -> str:
    pid = prompt.get("id", "?")
    title = prompt.get("title", "Untitled")
    title_ko = prompt.get("title_ko", "")
    category = prompt.get("category", "—")
    style = prompt.get("style", "—")
    tags = prompt.get("tags", [])
    tags_ko = prompt.get("tags_ko", [])
    lang = prompt.get("language", "")

    display_title = f"{title_ko} ({title})" if title_ko else title
    lines = [
        f"[{pid}] {display_title[:120]}",
        f"  Category: {category} | Style: {style} | Lang: {lang}",
    ]
    display_tags = tags_ko if tags_ko else tags
    if display_tags:
        lines.append(f"  태그: {', '.join(str(t) for t in display_tags[:8])}")

    if verbose:
        text = prompt.get("prompt", "")
        wrapped = textwrap.fill(text, width=78, initial_indent="  ", subsequent_indent="  ")
        lines.append(f"  Prompt:\n{wrapped}")

        prompt_ko = prompt.get("prompt_ko", "")
        if prompt_ko:
            wrapped_ko = textwrap.fill(prompt_ko, width=78, initial_indent="  ", subsequent_indent="  ")
            lines.append(f"  한국어:\n{wrapped_ko}")

        author = prompt.get("author", "")
        if author:
            lines.append(f"  Author: {author}")
        videos = prompt.get("videos", [])
        if videos:
            lines.append(f"  Videos: {len(videos)} reference(s)")
        source = prompt.get("source_url", "")
        if source:
            lines.append(f"  Source: {source}")

    return "\n".join(lines)


def cmd_search(args: argparse.Namespace) -> int:
    prompts = _load_prompts()
    query = args.query.lower()
    results = []

    for p in prompts:
        searchable_parts = [
            (p.get("title") or "").lower(),
            (p.get("title_ko") or "").lower(),
            " ".join(str(t).lower() for t in (p.get("tags") or [])),
            " ".join(str(t).lower() for t in (p.get("tags_ko") or [])),
            (p.get("category") or "").lower(),
            (p.get("style") or "").lower(),
            (p.get("prompt") or "").lower(),
            (p.get("prompt_ko") or "").lower(),
        ]
        if query in " ".join(searchable_parts):
            results.append(p)

    if not results:
        print(f"No results for '{args.query}'.")
        return 0

    limit = args.limit or 10
    print(f"Search results: {len(results)} (showing top {min(limit, len(results))})\n")
    for p in results[:limit]:
        print(_format_prompt(p, verbose=args.verbose))
        print()
    return 0


def cmd_browse(args: argparse.Namespace) -> int:
    taxonomy = _load_taxonomy()
    prompts = _load_prompts()
    index = _build_index(prompts)
    tiers = taxonomy.get("tiers", {})

    category = args.category
    if not category:
        print("=== Seedance 2.0 Video Prompt Categories ===\n")
        for name, info in tiers.items():
            count = info.get("count", 0)
            print(f"  {name:<22} {count:>4} prompts")
        print(f"\n  Total: {taxonomy.get('total', 0)} prompts")
        print("\nUsage: browse <category>  (e.g. browse cinematic)")
        return 0

    tier_data = tiers.get(category)
    if not tier_data:
        print(f"Error: category '{category}' not found.", file=sys.stderr)
        print(f"  Available: {', '.join(tiers.keys())}", file=sys.stderr)
        return 1

    ids = tier_data.get("prompt_ids", [])
    limit = args.limit or 10
    print(f"=== {category} ({len(ids)} prompts, showing top {min(limit, len(ids))}) ===\n")

    shown = 0
    for pid in ids[:limit]:
        p = index.get(pid)
        if p:
            print(_format_prompt(p, verbose=args.verbose))
            print()
            shown += 1
    if not shown:
        print("  (no prompts to display)")
    return 0


def cmd_by_category(args: argparse.Namespace) -> int:
    taxonomy = _load_taxonomy()
    tiers = taxonomy.get("tiers", {})
    total = taxonomy.get("total", 0)

    print("=== Seedance 2.0 — Prompts by Category ===\n")
    print(f"{'Category':<22} {'Count':>6}  {'%':>5}  Bar")
    print("─" * 55)

    max_count = max((t.get("count", 0) for t in tiers.values()), default=1)
    for name, info in tiers.items():
        count = info.get("count", 0)
        pct = (count / total * 100) if total else 0
        bar_len = int(count / max_count * 25) if max_count else 0
        bar = "█" * bar_len
        print(f"{name:<22} {count:>6}  {pct:>4.1f}%  {bar}")

    print(f"\n{'Total':<22} {total:>6}")
    return 0


def cmd_random(args: argparse.Namespace) -> int:
    prompts = _load_prompts()
    taxonomy = _load_taxonomy()

    if args.category:
        tier_data = taxonomy.get("tiers", {}).get(args.category)
        if not tier_data:
            print(f"Error: category '{args.category}' not found.", file=sys.stderr)
            return 1
        valid_ids = set(tier_data.get("prompt_ids", []))
        candidates = [p for p in prompts if p.get("id") in valid_ids]
    else:
        candidates = prompts

    if not candidates:
        print("No prompts match the criteria.")
        return 0

    count = min(args.count or 1, len(candidates))
    picks = rand_mod.sample(candidates, count)

    print(f"=== Random Prompt{'s' if count > 1 else ''} ===\n")
    for p in picks:
        print(_format_prompt(p, verbose=True))
        print()
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    taxonomy = _load_taxonomy()
    prompts = _load_prompts()
    total = len(prompts)

    print("=== Seedance 2.0 Video Prompt Library Statistics ===\n")
    print(f"Total prompts: {total}")
    print(f"Model: {taxonomy.get('model', 'seedance-2.0')}")

    langs: dict[str, int] = {}
    for p in prompts:
        lang = p.get("language", "unknown")
        langs[lang] = langs.get(lang, 0) + 1
    print(f"\nLanguage distribution:")
    for lang, cnt in sorted(langs.items(), key=lambda x: -x[1]):
        print(f"  {lang}: {cnt}")

    has_ko = sum(1 for p in prompts if p.get("prompt_ko"))
    has_title_ko = sum(1 for p in prompts if p.get("title_ko"))
    has_tags_ko = sum(1 for p in prompts if p.get("tags_ko"))
    print(f"\nKorean translations:")
    print(f"  prompt_ko: {has_ko}/{total}")
    print(f"  title_ko:  {has_title_ko}/{total}")
    print(f"  tags_ko:   {has_tags_ko}/{total}")

    authors: dict[str, int] = {}
    for p in prompts:
        a = p.get("author", "unknown")
        authors[a] = authors.get(a, 0) + 1
    print(f"Unique authors: {len(authors)}")
    top_authors = sorted(authors.items(), key=lambda x: -x[1])[:5]
    for a, cnt in top_authors:
        print(f"  {a}: {cnt}")

    with_video = sum(1 for p in prompts if p.get("videos"))
    print(f"\nPrompts with video references: {with_video}")

    tiers = taxonomy.get("tiers", {})
    print(f"\n{'Category':<22} {'Count':>6}")
    print("─" * 30)
    for name, info in tiers.items():
        print(f"{name:<22} {info.get('count', 0):>6}")

    print()
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    prompts = _load_prompts()
    index = _build_index(prompts)

    p = index.get(args.id)
    if not p:
        print(f"Error: prompt with ID {args.id} not found.", file=sys.stderr)
        return 1

    print(_format_prompt(p, verbose=True))
    print()

    videos = p.get("videos", [])
    if videos:
        print("  Video URLs:")
        for v in videos:
            print(f"    {v}")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Seedance 2.0 Video Prompt Library — browse, search, and discover 605+ prompts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sp_search = sub.add_parser("search", help="Search prompts by keyword")
    sp_search.add_argument("query", help="Search term")
    sp_search.add_argument("--limit", "-l", type=int, default=10)
    sp_search.add_argument("--verbose", "-v", action="store_true", help="Show full prompt text")

    sp_browse = sub.add_parser("browse", help="Browse prompts by category")
    sp_browse.add_argument("category", nargs="?", default="", help="Category name (e.g. cinematic)")
    sp_browse.add_argument("--limit", "-l", type=int, default=10)
    sp_browse.add_argument("--verbose", "-v", action="store_true", help="Show full prompt text")

    sub.add_parser("by-category", help="Show prompt distribution by category")

    sp_random = sub.add_parser("random", help="Get random prompt(s)")
    sp_random.add_argument("--category", "-c", help="Filter by category")
    sp_random.add_argument("--count", "-n", type=int, default=1, help="Number of prompts (default: 1)")

    sub.add_parser("stats", help="Library statistics")

    sp_show = sub.add_parser("show", help="Show prompt details by ID")
    sp_show.add_argument("--id", type=int, required=True, help="Prompt ID")

    args = parser.parse_args()

    dispatch = {
        "search": cmd_search,
        "browse": cmd_browse,
        "by-category": cmd_by_category,
        "random": cmd_random,
        "stats": cmd_stats,
        "show": cmd_show,
    }
    return dispatch[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
