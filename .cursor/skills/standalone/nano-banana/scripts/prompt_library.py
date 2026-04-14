#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
# @lat: [[nano-banana#prompt_library]]
"""
Nano Banana Prompt Library CLI.

Browse, search, and generate images from 7,900+ curated prompts
(7,600+ main + 301 BananaX infographic + 30 BananaX business).

Usage:
  uv run prompt_library.py search "sunset landscape"
  uv run prompt_library.py browse photography/portrait --limit 5
  uv run prompt_library.py browse bananax --limit 5
  uv run prompt_library.py random --tier creative
  uv run prompt_library.py stats
  uv run prompt_library.py generate --id 12445 --resolution 2K
  uv run prompt_library.py generate --id nano_01 --resolution 2K
  uv run prompt_library.py show --id nano_01
"""

from __future__ import annotations

import argparse
import json
import random as rand_mod
import subprocess
import sys
import textwrap
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"
PROMPTS_FILE = DATA_DIR / "prompts.json"
TAXONOMY_FILE = DATA_DIR / "taxonomy.json"
BANANAX_EVAL_FILE = DATA_DIR / "bananax_evaluation.json"
BANANAX_BIZ_FILE = DATA_DIR / "bananax_business.json"
GENERATE_SCRIPT = SKILL_DIR / "scripts" / "generate_image.py"


def _normalize_bananax_eval(items: list[dict]) -> list[dict]:
    """Normalize evaluation_data.json items to the common prompt schema."""
    result = []
    for item in items:
        tags = item.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]
        result.append({
            "id": item["id"],
            "title": item.get("name", "Untitled"),
            "prompt": item.get("yaml", ""),
            "category": "infographic-evaluation",
            "style": ", ".join(tags[:3]) if tags else "infographic",
            "tags": tags,
            "author": "BananaX",
            "_source": "bananax_evaluation",
            "_tier": "bananax",
            "_subcategory": "infographic",
            "_scores": item.get("scores", {}),
        })
    return result


def _normalize_bananax_biz(items: list[dict]) -> list[dict]:
    """Normalize business_prompts.json items to the common prompt schema."""
    result = []
    for item in items:
        result.append({
            "id": item["id"],
            "title": item.get("name_en") or item.get("name", "Untitled"),
            "prompt": item.get("yaml", ""),
            "category": item.get("category_en", "business"),
            "style": "business-infographic",
            "tags": [item.get("category_en", ""), item.get("name_en", "")],
            "author": "BananaX",
            "_source": "bananax_business",
            "_tier": "bananax",
            "_subcategory": "business",
        })
    return result


def _load_prompts() -> list[dict]:
    if not PROMPTS_FILE.exists():
        print(f"Error: 프롬프트 파일이 없습니다: {PROMPTS_FILE}", file=sys.stderr)
        print("  먼저 fetch_prompts.py를 실행하세요.", file=sys.stderr)
        sys.exit(1)
    prompts = json.loads(PROMPTS_FILE.read_text(encoding="utf-8"))

    if BANANAX_EVAL_FILE.exists():
        raw = json.loads(BANANAX_EVAL_FILE.read_text(encoding="utf-8"))
        prompts.extend(_normalize_bananax_eval(raw))
    if BANANAX_BIZ_FILE.exists():
        raw = json.loads(BANANAX_BIZ_FILE.read_text(encoding="utf-8"))
        prompts.extend(_normalize_bananax_biz(raw))

    return prompts


def _load_taxonomy() -> dict:
    if not TAXONOMY_FILE.exists():
        print(f"Error: 분류 파일이 없습니다: {TAXONOMY_FILE}", file=sys.stderr)
        print("  먼저 fetch_prompts.py를 실행하세요.", file=sys.stderr)
        sys.exit(1)
    return json.loads(TAXONOMY_FILE.read_text(encoding="utf-8"))


def _structured_to_natural(prompt_obj: dict) -> str:
    """Convert a BananaX 7-part structured prompt to natural language."""
    parts: list[str] = []

    tone = prompt_obj.get("tone", "")
    if tone:
        parts.append(f"Create an image with a {tone} tone.")

    vi = prompt_obj.get("visual_identity", "")
    if vi:
        parts.append(vi if vi[0].isupper() else vi.capitalize())

    img_style = prompt_obj.get("image_style", {})
    if isinstance(img_style, dict):
        main = img_style.get("main_style", "")
        specifics = img_style.get("specific_styles", [])
        cam = img_style.get("camera_settings", {})
        style_parts = []
        if main:
            style_parts.append(f"Style: {main}")
        if specifics:
            style_parts.append(", ".join(specifics))
        if isinstance(cam, dict):
            cam_desc = [f"{k}: {v}" for k, v in cam.items() if v]
            if cam_desc:
                style_parts.append(f"Camera: {', '.join(cam_desc)}")
        if style_parts:
            parts.append(". ".join(style_parts) + ".")
    elif isinstance(img_style, str) and img_style:
        parts.append(f"Style: {img_style}.")

    typo = prompt_obj.get("typography", "")
    if typo:
        parts.append(f"Typography: {typo}.")

    cc = prompt_obj.get("content_connection", "")
    if cc:
        parts.append(cc if cc[0].isupper() else cc.capitalize())

    constraints = prompt_obj.get("constraints", [])
    if constraints:
        if isinstance(constraints, list):
            parts.append("Constraints: " + "; ".join(constraints) + ".")
        elif isinstance(constraints, str):
            parts.append(f"Constraints: {constraints}.")

    return " ".join(parts)


def _get_prompt_text(prompt: dict) -> str:
    """Extract the usable prompt text, converting structured prompts if needed."""
    raw = prompt.get("prompt", "")
    if isinstance(raw, dict):
        return _structured_to_natural(raw)
    return str(raw)


def _format_prompt(prompt: dict, verbose: bool = False) -> str:
    """Format a prompt for display."""
    pid = prompt.get("id", "?")
    title = prompt.get("title", "Untitled")
    category = prompt.get("category", "—")
    style = prompt.get("style", "—")
    tags = prompt.get("tags", [])
    tier = prompt.get("_tier", "")
    sub = prompt.get("_subcategory", "")

    lines = [
        f"[{pid}] {title[:80]}",
        f"  Category: {category} | Style: {style}",
    ]
    if tier:
        lines.append(f"  Taxonomy: {tier}/{sub}")
    if tags:
        lines.append(f"  Tags: {', '.join(tags[:8])}")

    if verbose:
        text = _get_prompt_text(prompt)
        wrapped = textwrap.fill(text, width=78, initial_indent="  ", subsequent_indent="  ")
        lines.append(f"  Prompt:\n{wrapped}")

        author = prompt.get("author", "")
        if author:
            lines.append(f"  Author: {author}")
        images = prompt.get("images", [])
        if images:
            lines.append(f"  Images: {len(images)} reference(s)")

    return "\n".join(lines)


def _parse_id(raw: str) -> int | str:
    """Parse a prompt ID string, returning int for numeric IDs or str for BananaX IDs."""
    try:
        return int(raw)
    except ValueError:
        return raw


def _build_index(prompts: list[dict]) -> dict[int | str, dict]:
    return {p["id"]: p for p in prompts if "id" in p}


def cmd_search(args: argparse.Namespace) -> int:
    prompts = _load_prompts()
    query = args.query.lower()
    results = []

    for p in prompts:
        title = (p.get("title") or "").lower()
        tags = " ".join(t.lower() for t in (p.get("tags") or []))
        category = (p.get("category") or "").lower()
        style = (p.get("style") or "").lower()
        prompt_text = ""
        raw = p.get("prompt", "")
        if isinstance(raw, str):
            prompt_text = raw.lower()

        searchable = f"{title} {tags} {category} {style} {prompt_text}"
        if query in searchable:
            results.append(p)

    if not results:
        print(f"'{args.query}'에 대한 검색 결과가 없습니다.")
        return 0

    limit = args.limit or 10
    print(f"검색 결과: {len(results)}개 (상위 {min(limit, len(results))}개 표시)\n")
    for p in results[:limit]:
        print(_format_prompt(p, verbose=args.verbose))
        print()
    return 0


def _get_bananax_virtual_tier(prompts: list[dict]) -> dict:
    """Build a virtual tier structure for BananaX prompts from loaded data."""
    subs: dict[str, list] = {}
    for p in prompts:
        if p.get("_tier") != "bananax":
            continue
        sub = p.get("_subcategory", "other")
        subs.setdefault(sub, []).append(p["id"])

    result: dict[str, dict] = {}
    total = 0
    for sub_name, ids in sorted(subs.items()):
        result[sub_name] = {"count": len(ids), "prompt_ids": ids}
        total += len(ids)
    return {"count": total, "subcategories": result}


def cmd_browse(args: argparse.Namespace) -> int:
    taxonomy = _load_taxonomy()
    prompts = _load_prompts()
    index = _build_index(prompts)
    bananax_tier = _get_bananax_virtual_tier(prompts)

    all_tiers = {**taxonomy.get("tiers", {})}
    if bananax_tier["count"] > 0:
        all_tiers["bananax"] = bananax_tier
    all_total = taxonomy.get("total", 0) + bananax_tier["count"]

    path = args.path
    if not path:
        print("=== Prompt Library Tiers ===\n")
        for tier, info in all_tiers.items():
            count = info.get("count", 0)
            subs = info.get("subcategories", {})
            sub_names = [f"{s}({d['count']})" for s, d in subs.items() if d.get("count", 0) > 0]
            print(f"  {tier}: {count} prompts")
            if sub_names:
                print(f"    └─ {', '.join(sub_names)}")
        print(f"\nTotal: {all_total} prompts")
        print("\nUsage: browse <tier> 또는 browse <tier>/<subcategory>")
        return 0

    parts = path.strip("/").split("/")
    tier_name = parts[0]
    tier_data = all_tiers.get(tier_name)
    if not tier_data:
        print(f"Error: '{tier_name}' 티어를 찾을 수 없습니다.", file=sys.stderr)
        print(f"  사용 가능: {', '.join(all_tiers.keys())}", file=sys.stderr)
        return 1

    if len(parts) == 1:
        print(f"=== {tier_name} ({tier_data['count']} prompts) ===\n")
        for sub, data in tier_data.get("subcategories", {}).items():
            if data.get("count", 0) > 0:
                print(f"  {sub}: {data['count']} prompts")
        print(f"\nUsage: browse {tier_name}/<subcategory>")
        return 0

    sub_name = parts[1]
    sub_data = tier_data.get("subcategories", {}).get(sub_name)
    if not sub_data:
        available = [s for s, d in tier_data.get("subcategories", {}).items() if d.get("count", 0) > 0]
        print(f"Error: '{sub_name}' 서브카테고리를 찾을 수 없습니다.", file=sys.stderr)
        print(f"  사용 가능: {', '.join(available)}", file=sys.stderr)
        return 1

    ids = sub_data.get("prompt_ids", [])
    limit = args.limit or 10
    print(f"=== {tier_name}/{sub_name} ({len(ids)} prompts, 상위 {min(limit, len(ids))}개) ===\n")

    shown = 0
    for pid in ids[:limit]:
        p = index.get(pid)
        if p:
            print(_format_prompt(p, verbose=args.verbose))
            print()
            shown += 1
    if not shown:
        print("  (표시할 프롬프트가 없습니다)")
    return 0


def cmd_random(args: argparse.Namespace) -> int:
    prompts = _load_prompts()
    taxonomy = _load_taxonomy()

    if args.tier:
        if args.tier == "bananax":
            candidates = [p for p in prompts if p.get("_tier") == "bananax"]
            if not candidates:
                print("Error: bananax 프롬프트를 찾을 수 없습니다.", file=sys.stderr)
                return 1
        else:
            tier_data = taxonomy.get("tiers", {}).get(args.tier)
            if not tier_data:
                print(f"Error: '{args.tier}' 티어를 찾을 수 없습니다.", file=sys.stderr)
                return 1
            valid_ids: set[int | str] = set()
            for sub_data in tier_data.get("subcategories", {}).values():
                valid_ids.update(sub_data.get("prompt_ids", []))
            candidates = [p for p in prompts if p.get("id") in valid_ids]
    else:
        candidates = prompts

    if not candidates:
        print("조건에 맞는 프롬프트가 없습니다.")
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
    bananax_tier = _get_bananax_virtual_tier(prompts)

    main_total = taxonomy.get("total", 0)
    bananax_total = bananax_tier["count"]
    combined_total = len(prompts)

    print("=== Nano Banana Prompt Library Statistics ===\n")
    print(f"Total prompts: {combined_total}")
    print(f"  Main library: {main_total}")
    print(f"  BananaX infographic: {bananax_total}")

    structured = sum(1 for p in prompts if isinstance(p.get("prompt"), dict))
    bananax_count = sum(1 for p in prompts if p.get("_source"))
    plain = len(prompts) - structured - bananax_count
    print(f"\nPlain text prompts: {plain}")
    print(f"Structured (BananaX 7-part) prompts: {structured}")
    print(f"BananaX infographic prompts: {bananax_count}")

    authors: set[str] = set()
    for p in prompts:
        a = p.get("author", "")
        if a:
            authors.add(a)
    print(f"Unique authors: {len(authors)}")

    all_tiers = {**taxonomy.get("tiers", {})}
    if bananax_total > 0:
        all_tiers["bananax"] = bananax_tier

    print(f"\n{'Tier':<16} {'Count':>6}  Subcategories")
    print("─" * 60)
    for tier, info in all_tiers.items():
        count = info.get("count", 0)
        subs = info.get("subcategories", {})
        active = sum(1 for d in subs.values() if d.get("count", 0) > 0)
        print(f"{tier:<16} {count:>6}  {active} active subcategories")
        for sub, data in subs.items():
            sc = data.get("count", 0)
            if sc > 0:
                print(f"  └─ {sub:<12} {sc:>6}")

    print()
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    prompts = _load_prompts()
    index = _build_index(prompts)

    p = index.get(args.id)
    if not p:
        print(f"Error: ID {args.id}인 프롬프트를 찾을 수 없습니다.", file=sys.stderr)
        return 1

    print(_format_prompt(p, verbose=True))
    print()

    raw = p.get("prompt", "")
    if isinstance(raw, dict):
        print("  [Structured BananaX prompt — natural language conversion:]")
        nl = _structured_to_natural(raw)
        wrapped = textwrap.fill(nl, width=78, initial_indent="  ", subsequent_indent="  ")
        print(wrapped)
        print()

    images = p.get("images", [])
    if images:
        print("  Reference images:")
        for img in images:
            print(f"    {img}")

    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    prompts = _load_prompts()
    index = _build_index(prompts)

    p = index.get(args.id)
    if not p:
        print(f"Error: ID {args.id}인 프롬프트를 찾을 수 없습니다.", file=sys.stderr)
        return 1

    prompt_text = _get_prompt_text(p)
    print(f"Prompt [{args.id}]: {p.get('title', '')[:60]}")
    print(f"Text: {prompt_text[:120]}...")
    print()

    if not GENERATE_SCRIPT.exists():
        print(f"Error: generate_image.py를 찾을 수 없습니다: {GENERATE_SCRIPT}", file=sys.stderr)
        return 1

    filename = args.filename or f"nb_{args.id}.png"
    cmd = [
        "uv", "run", str(GENERATE_SCRIPT),
        "--prompt", prompt_text,
        "--filename", filename,
    ]
    if args.resolution:
        cmd.extend(["--resolution", args.resolution])
    if args.output_dir:
        cmd.extend(["--output-dir", args.output_dir])
    if args.api_key:
        cmd.extend(["--api-key", args.api_key])

    print(f"Executing: {' '.join(cmd[:6])} ...")
    return subprocess.call(cmd)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Nano Banana Prompt Library — browse, search, and generate from 7,900+ prompts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # search
    sp_search = sub.add_parser("search", help="키워드로 프롬프트 검색")
    sp_search.add_argument("query", help="검색어")
    sp_search.add_argument("--limit", "-l", type=int, default=10, help="결과 수 (기본: 10)")
    sp_search.add_argument("--verbose", "-v", action="store_true", help="프롬프트 전문 표시")

    # browse
    sp_browse = sub.add_parser("browse", help="카테고리별 프롬프트 탐색")
    sp_browse.add_argument("path", nargs="?", default="", help="tier 또는 tier/subcategory (예: photography, bananax, bananax/infographic)")
    sp_browse.add_argument("--limit", "-l", type=int, default=10, help="결과 수 (기본: 10)")
    sp_browse.add_argument("--verbose", "-v", action="store_true", help="프롬프트 전문 표시")

    # random
    sp_random = sub.add_parser("random", help="랜덤 프롬프트 추천")
    sp_random.add_argument("--tier", "-t", help="특정 티어 필터 (photography/design/creative/ui_ux/bananax)")
    sp_random.add_argument("--count", "-c", type=int, default=1, help="추천 수 (기본: 1)")

    # stats
    sub.add_parser("stats", help="라이브러리 통계")

    # show
    sp_show = sub.add_parser("show", help="ID로 프롬프트 상세 조회")
    sp_show.add_argument("--id", type=_parse_id, required=True, help="프롬프트 ID (숫자 또는 문자열, 예: 12445, nano_01)")

    # generate
    sp_gen = sub.add_parser("generate", help="라이브러리 프롬프트로 이미지 생성")
    sp_gen.add_argument("--id", type=_parse_id, required=True, help="프롬프트 ID (숫자 또는 문자열, 예: 12445, nano_01)")
    sp_gen.add_argument("--filename", "-f", help="출력 파일명 (기본: nb_<id>.png)")
    sp_gen.add_argument("--resolution", "-r", choices=["512", "1K", "2K", "4K"], help="해상도")
    sp_gen.add_argument("--output-dir", "-o", help="출력 디렉토리")
    sp_gen.add_argument("--api-key", "-k", help="Gemini API 키")

    args = parser.parse_args()

    dispatch = {
        "search": cmd_search,
        "browse": cmd_browse,
        "random": cmd_random,
        "stats": cmd_stats,
        "show": cmd_show,
        "generate": cmd_generate,
    }
    return dispatch[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
