#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
# @lat: [[nano-banana#fetch_prompts]]
"""
Download Nano Banana Pro prompts from GitHub and classify into a 4-tier taxonomy.

Outputs:
  data/prompts.json   — full prompt dataset (7,691 items)
  data/taxonomy.json  — classification index with category tree and prompt IDs

Usage:
  uv run fetch_prompts.py                          # default paths
  uv run fetch_prompts.py --output-dir /tmp/nb     # custom output
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

SOURCE_URL = (
    "https://raw.githubusercontent.com/"
    "ImgEdify/awesome-nano-banana-pro-prompts/main/data/prompts.json"
)

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = SKILL_DIR / "data"

TAXONOMY_RULES: dict[str, dict[str, list[str]]] = {
    "photography": {
        "portrait": ["portrait", "headshot", "selfie", "face", "model shoot"],
        "landscape": ["landscape", "scenery", "nature", "sunset", "mountain", "ocean"],
        "product": ["product", "packshot", "cosmetic", "bottle", "packaging"],
        "food": ["food", "dish", "cuisine", "meal", "recipe", "dessert", "cake"],
        "architecture": ["architecture", "building", "interior", "exterior", "room"],
        "animal": ["animal", "pet", "dog", "cat", "bird", "wildlife"],
        "cinematic": ["cinematic", "film", "movie", "scene", "dramatic lighting"],
        "fashion": ["fashion", "runway", "outfit", "clothing", "dress", "style"],
        "street": ["street", "urban", "city", "downtown"],
        "macro": ["macro", "close-up", "detail", "texture"],
    },
    "design": {
        "logo": ["logo", "brand", "emblem", "monogram", "icon design"],
        "poster": ["poster", "flyer", "banner", "billboard"],
        "packaging": ["package design", "label design", "box design"],
        "typography": ["typography", "lettering", "font", "type design"],
        "infographic": ["infographic", "data viz", "chart", "diagram"],
        "mockup": ["mockup", "mock-up", "presentation template"],
    },
    "creative": {
        "3d_render": ["3d", "render", "blender", "cgi", "octane"],
        "illustration": ["illustration", "drawing", "sketch", "watercolor", "ink"],
        "anime": ["anime", "manga", "cel shading", "japanese style"],
        "abstract": ["abstract", "surreal", "conceptual", "psychedelic"],
        "character": ["character", "mascot", "avatar", "creature", "fantasy"],
        "vintage": ["vintage", "retro", "nostalgic", "film grain", "polaroid"],
        "pixel_art": ["pixel art", "8-bit", "16-bit", "sprite"],
        "fantasy": ["fantasy", "dragon", "wizard", "magic", "medieval"],
        "sci_fi": ["sci-fi", "cyberpunk", "futuristic", "space", "neon"],
    },
    "ui_ux": {
        "app_ui": ["app", "mobile app", "ios", "android", "screen"],
        "dashboard": ["dashboard", "admin panel", "analytics", "metrics"],
        "web_ui": ["website", "landing page", "web design", "homepage"],
        "ux_flow": ["ux", "user flow", "wireframe", "prototype"],
    },
}


def _normalize(text: str) -> str:
    return text.lower().strip()


def _classify_prompt(prompt: dict) -> tuple[str, str]:
    """Return (tier, subcategory) for a prompt based on title keywords."""
    title = _normalize(prompt.get("title", ""))
    tags_raw = prompt.get("tags", [])
    tags = " ".join(_normalize(t) for t in tags_raw) if tags_raw else ""
    category = _normalize(prompt.get("category", ""))
    style = _normalize(prompt.get("style", ""))

    searchable = f"{title} {tags} {category} {style}"

    best_tier = ""
    best_sub = ""
    best_score = 0

    for tier, subcategories in TAXONOMY_RULES.items():
        for sub, keywords in subcategories.items():
            score = 0
            for kw in keywords:
                if kw in searchable:
                    bonus = 2 if kw in title else 1
                    score += bonus
            if score > best_score:
                best_score = score
                best_tier = tier
                best_sub = sub

    if best_score == 0:
        if category in ("portrait", "landscape", "product", "food", "architecture", "animal"):
            return ("photography", category)
        if style in ("anime",):
            return ("creative", "anime")
        if style in ("3d",):
            return ("creative", "3d_render")
        if "character" in category:
            return ("creative", "character")
        if "abstract" in category:
            return ("creative", "abstract")
        return ("photography", "portrait")

    return (best_tier, best_sub)


def _build_taxonomy(prompts: list[dict]) -> dict:
    """Build the taxonomy index from classified prompts."""
    tree: dict[str, dict[str, list[str]]] = {}
    for tier in TAXONOMY_RULES:
        tree[tier] = {}
        for sub in TAXONOMY_RULES[tier]:
            tree[tier][sub] = []

    for p in prompts:
        pid = p.get("id", "")
        tier, sub = _classify_prompt(p)
        p["_tier"] = tier
        p["_subcategory"] = sub
        if sub not in tree.get(tier, {}):
            tree.setdefault(tier, {})[sub] = []
        tree[tier][sub].append(pid)

    summary: dict = {"total": len(prompts), "tiers": {}}
    for tier, subs in tree.items():
        tier_total = sum(len(ids) for ids in subs.values())
        summary["tiers"][tier] = {
            "count": tier_total,
            "subcategories": {
                sub: {"count": len(ids), "prompt_ids": ids}
                for sub, ids in subs.items()
                if ids
            },
        }

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch & classify Nano Banana prompts")
    parser.add_argument(
        "--output-dir", "-o",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"출력 디렉토리 (기본값: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument("--url", default=SOURCE_URL, help="프롬프트 JSON URL")
    args = parser.parse_args()

    output_dir: Path = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading prompts from {args.url} ...")
    try:
        req = urllib.request.Request(args.url, headers={"User-Agent": "nano-banana/2.0"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read()
    except Exception as exc:
        print(f"Error: 프롬프트 다운로드 실패 — {exc}", file=sys.stderr)
        return 1

    try:
        prompts = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"Error: JSON 파싱 실패 — {exc}", file=sys.stderr)
        return 2

    if not isinstance(prompts, list):
        print("Error: 예상과 다른 JSON 구조입니다 (리스트가 아님).", file=sys.stderr)
        return 3

    print(f"Downloaded {len(prompts)} prompts.")

    prompts_path = output_dir / "prompts.json"
    prompts_path.write_text(json.dumps(prompts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved prompts → {prompts_path}")

    print("Classifying prompts into 4-tier taxonomy ...")
    taxonomy = _build_taxonomy(prompts)

    taxonomy_path = output_dir / "taxonomy.json"
    taxonomy_path.write_text(json.dumps(taxonomy, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved taxonomy → {taxonomy_path}")

    print("\n=== Taxonomy Summary ===")
    for tier, info in taxonomy["tiers"].items():
        print(f"  {tier}: {info['count']} prompts ({len(info['subcategories'])} subcategories)")
    print(f"  Total: {taxonomy['total']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
